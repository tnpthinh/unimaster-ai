# -*- coding: utf-8 -*-
import os
import re

DB_PY_PATH = r"C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai\database.py"

with open(DB_PY_PATH, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update init_db() to include users and user_states tables
table_creation = """    # Bảng tài khoản người dùng & Phân quyền quản trị
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        salt TEXT NOT NULL,
        full_name TEXT NOT NULL,
        role TEXT DEFAULT 'student', -- 'admin' hoặc 'student'
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP
    )
    ''')

    # Bảng đồng bộ trạng thái & tiến độ học tập cá nhân (theo từng tài khoản)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_states (
        user_id INTEGER PRIMARY KEY,
        state_json TEXT NOT NULL DEFAULT '{}',
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    ''')
"""

if "CREATE TABLE IF NOT EXISTS users" not in code:
    code = code.replace("    # Bảng môn học\n    cursor.execute(\"\"\"\n    CREATE TABLE IF NOT EXISTS subjects (", table_creation + "\n    # Bảng môn học\n    cursor.execute(\"\"\"\n    CREATE TABLE IF NOT EXISTS subjects (")

# 2. Add migration for exam_results user_id column
if "ALTER TABLE exam_results ADD COLUMN user_id INTEGER DEFAULT 1" not in code:
    code = code.replace(
        "\"ALTER TABLE flashcards ADD COLUMN image_url TEXT DEFAULT ''\",",
        "\"ALTER TABLE flashcards ADD COLUMN image_url TEXT DEFAULT ''\",\n        \"ALTER TABLE exam_results ADD COLUMN user_id INTEGER DEFAULT 1\","
    )

# 3. Update save_exam_result to accept user_id
old_save_exam = """def save_exam_result(subject_id, total_questions, correct_answers, score, time_spent_seconds, detail_json='[]', exam_type='mixed'):
    conn = get_connection()
    c = conn.cursor()
    c.execute(\"\"\"
    INSERT INTO exam_results (subject_id, total_questions, correct_answers, score, time_spent_seconds, detail_json, exam_type)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    \"\"\", (subject_id, total_questions, correct_answers, score, time_spent_seconds, detail_json, exam_type))
    conn.commit()
    res_id = c.lastrowid
    conn.close()
    return res_id"""

new_save_exam = """def save_exam_result(subject_id, total_questions, correct_answers, score, time_spent_seconds, detail_json='[]', exam_type='mixed', user_id=1):
    conn = get_connection()
    c = conn.cursor()
    c.execute(\"\"\"
    INSERT INTO exam_results (subject_id, total_questions, correct_answers, score, time_spent_seconds, detail_json, exam_type, user_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    \"\"\", (subject_id, total_questions, correct_answers, score, time_spent_seconds, detail_json, exam_type, user_id))
    conn.commit()
    res_id = c.lastrowid
    conn.close()
    return res_id"""

code = code.replace(old_save_exam, new_save_exam)

# 4. Append user management functions to database.py
user_mgmt_functions = """

# ==========================================
# USER AUTHENTICATION & MULTI-ACCOUNT SYSTEM
# ==========================================
def hash_password(password: str, salt: str = None):
    import hashlib
    import secrets
    if not salt:
        salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000).hex()
    return hashed, salt

def create_user(username: str, password: str, full_name: str, role: str = "student"):
    username = username.strip().lower()
    full_name = full_name.strip()
    if not username or not password:
        raise ValueError("Tên đăng nhập và mật khẩu không được để trống")
    if len(username) < 3:
        raise ValueError("Tên đăng nhập phải có ít nhất 3 ký tự")
    if len(password) < 4:
        raise ValueError("Mật khẩu phải có ít nhất 4 ký tự")

    pwd_hash, salt = hash_password(password)
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO users (username, password_hash, salt, full_name, role) VALUES (?, ?, ?, ?, ?)",
            (username, pwd_hash, salt, full_name or username, role)
        )
        conn.commit()
        uid = c.lastrowid
    except sqlite3.IntegrityError:
        conn.close()
        raise ValueError(f"Tên đăng nhập '{username}' đã được sử dụng")
    
    conn.close()
    return {"id": uid, "username": username, "full_name": full_name or username, "role": role}

def verify_user(username: str, password: str):
    username = username.strip().lower()
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    if not row:
        conn.close()
        return None
    
    pwd_hash, _ = hash_password(password, row["salt"])
    import hmac
    if not hmac.compare_digest(pwd_hash, row["password_hash"]):
        conn.close()
        return None
    
    c.execute("UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?", (row["id"],))
    conn.commit()
    user_info = {
        "id": row["id"],
        "username": row["username"],
        "full_name": row["full_name"],
        "role": row["role"],
        "created_at": row["created_at"],
        "last_login": row["last_login"]
    }
    conn.close()
    return user_info

def get_user_by_id(user_id: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, username, full_name, role, created_at, last_login FROM users WHERE id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def get_all_users():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        SELECT u.id, u.username, u.full_name, u.role, u.created_at, u.last_login,
               COUNT(e.id) as exam_count,
               AVG(e.score) as avg_score
        FROM users u
        LEFT JOIN exam_results e ON u.id = e.user_id
        GROUP BY u.id
        ORDER BY CASE WHEN u.role = 'admin' THEN 0 ELSE 1 END, u.id ASC
    ''')
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def delete_user(user_id: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT role FROM users WHERE id = ?", (user_id,))
    row = c.fetchone()
    if not row:
        conn.close()
        return False
    if row["role"] == "admin":
        conn.close()
        raise ValueError("Không thể xóa tài khoản Quản trị viên tối cao!")
    c.execute("DELETE FROM users WHERE id = ?", (user_id,))
    c.execute("DELETE FROM user_states WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    return True

def ensure_admin_user(admin_pwd: str = "uni-5292"):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE role = 'admin'")
    row = c.fetchone()
    if not row:
        pwd_hash, salt = hash_password(admin_pwd)
        c.execute(
            "INSERT INTO users (username, password_hash, salt, full_name, role) VALUES (?, ?, ?, ?, ?)",
            ("admin", pwd_hash, salt, "Quản Trị Viên (Admin)", "admin")
        )
        conn.commit()
    conn.close()

def get_user_sync_state(user_id: int) -> dict:
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT state_json FROM user_states WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    if row and row["state_json"]:
        try:
            return json.loads(row["state_json"])
        except Exception:
            return {}
    return {}

def save_user_sync_state(user_id: int, incoming_state: dict):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT state_json FROM user_states WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    current = {}
    if row and row["state_json"]:
        try:
            current = json.loads(row["state_json"])
        except Exception:
            current = {}
    current.update(incoming_state)
    state_str = json.dumps(current, ensure_ascii=False)
    c.execute("INSERT OR REPLACE INTO user_states (user_id, state_json, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP)", (user_id, state_str))
    conn.commit()
    conn.close()
    return current
"""

if "def hash_password" not in code:
    code += user_mgmt_functions

with open(DB_PY_PATH, "w", encoding="utf-8") as f:
    f.write(code)

print("Updated database.py successfully! Total lines:", len(code.splitlines()))
