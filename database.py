"""
Database manager for UniMaster AI using SQLite
Updated with multi-format questions (MCQ, True/False, Short Answer, Essay/Coding) and Exercises
"""
import sqlite3
import json
import os
from datetime import datetime, date, timedelta

_BUNDLED_DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "unimaster.db")
# Bản dữ liệu sạch (đã gỡ API Key) dùng để khởi tạo trên Cloud — tạo bằng: python make_cloud_seed.py
_CLOUD_SEED_DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seed", "unimaster_seed.db")

# Khi chạy trên Cloud (Render / Railway / Fly.io), đặt biến môi trường DATA_DIR trỏ tới ổ đĩa bền vững
# (Persistent Volume) để dữ liệu không bị mất sau mỗi lần khởi động lại / triển khai lại.
_DATA_DIR = os.environ.get("DATA_DIR", "").strip()
if _DATA_DIR:
    os.makedirs(_DATA_DIR, exist_ok=True)
    DB_PATH = os.path.join(_DATA_DIR, "unimaster.db")
    if not os.path.exists(DB_PATH):
        _seed = _CLOUD_SEED_DB if os.path.exists(_CLOUD_SEED_DB) else _BUNDLED_DB
        if os.path.exists(_seed):
            import shutil
            shutil.copyfile(_seed, DB_PATH)  # Khởi tạo lần đầu bằng ngân hàng đề có sẵn
else:
    DB_PATH = _BUNDLED_DB

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Bảng cấu hình
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)
    
    # Bảng tài khoản người dùng & Phân quyền quản trị
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

    # Nhật ký đăng nhập: chỉ lưu IP do máy chủ quan sát và User-Agent trình duyệt.
    # Trình duyệt web không thể và không nên cung cấp MAC address của thiết bị.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS login_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        ip_address TEXT NOT NULL,
        user_agent TEXT DEFAULT '',
        event_type TEXT NOT NULL DEFAULT 'login',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # Bảng đồng bộ trạng thái & tiến độ học tập cá nhân (theo từng tài khoản)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_states (
        user_id INTEGER PRIMARY KEY,
        state_json TEXT NOT NULL DEFAULT '{}',
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    ''')

    # Bảng môn học
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        icon TEXT DEFAULT '📚',
        category TEXT DEFAULT 'Đại cương',
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Bảng chủ đề / chương
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS topics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        content TEXT,
        order_num INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
    )
    """)
    
    # Bảng câu hỏi đa định dạng: mcq, true_false, short_answer, essay
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_id INTEGER NOT NULL,
        topic_id INTEGER,
        q_type TEXT DEFAULT 'mcq', -- 'mcq', 'true_false', 'short_answer', 'essay'
        question_text TEXT NOT NULL,
        code_snippet TEXT DEFAULT '',
        option_a TEXT DEFAULT '',
        option_b TEXT DEFAULT '',
        option_c TEXT DEFAULT '',
        option_d TEXT DEFAULT '',
        correct_option TEXT NOT NULL, -- 'A','B','C','D' hoặc 'True'/'False' hoặc đáp án ngắn
        explanation TEXT DEFAULT '',
        difficulty TEXT DEFAULT 'medium',
        image_url TEXT DEFAULT '',
        topic_tag TEXT DEFAULT '',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
    )
    """)

    # Bảng Hỏi đáp & Thảo luận cộng đồng gắn với từng câu hỏi
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS question_discussions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id INTEGER NOT NULL,
        author_name TEXT NOT NULL,
        author_role TEXT DEFAULT 'student',
        content TEXT NOT NULL,
        upvotes INTEGER DEFAULT 1,
        is_verified INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
    )
    """)
    
    # Bảng Bài tập lớn / Tự luận thực hành (OOP Exercises, Case Studies)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS exercises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        problem TEXT NOT NULL,
        specs_json TEXT DEFAULT '[]',
        sample_code TEXT DEFAULT '',
        difficulty TEXT DEFAULT 'hard',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
    )
    """)

    # Bảng Flashcard (SM-2 Spaced Repetition)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS flashcards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_id INTEGER NOT NULL,
        front TEXT NOT NULL,
        back TEXT NOT NULL,
        hint TEXT,
        repetitions INTEGER DEFAULT 0,
        interval_days INTEGER DEFAULT 1,
        ease_factor REAL DEFAULT 2.5,
        next_review TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
    )
    """)
    
    # Lịch sử bền vững: bản sao server của lịch sử thi/chat từ trình duyệt.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS archived_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        history_type TEXT NOT NULL,
        item_id TEXT NOT NULL,
        payload_json TEXT NOT NULL,
        archived_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Bảng kết quả thi thử
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS exam_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_id INTEGER NOT NULL,
        exam_type TEXT DEFAULT 'mixed',
        total_questions INTEGER NOT NULL,
        correct_answers INTEGER NOT NULL,
        score REAL NOT NULL,
        time_spent_seconds INTEGER NOT NULL,
        detail_json TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
    )
    """)
    
    # Apply safe column migrations after tables exist (fresh and legacy databases).
    for table, column, definition in (
        ("questions", "image_url", "TEXT DEFAULT ''"),
        ("questions", "topic_tag", "TEXT DEFAULT ''"),
        ("flashcards", "image_url", "TEXT DEFAULT ''"),
        ("exam_results", "user_id", "INTEGER DEFAULT 1"),
        # Nhật ký đăng nhập v2: lưu cả tên đăng nhập đã gõ (kể cả khi sai) và kết quả thành công/thất bại
        ("login_events", "username", "TEXT DEFAULT ''"),
        ("login_events", "success", "INTEGER DEFAULT 1"),
        # Lần cuối thấy người dùng hoạt động (cookie phiên sống 30 ngày nên không phải lúc nào cũng đăng nhập lại)
        ("users", "last_seen", "TIMESTAMP"),
    ):
        columns = {row[1] for row in cursor.execute(f'PRAGMA table_info({table})')}
        if column not in columns:
            cursor.execute(f'ALTER TABLE {table} ADD COLUMN {column} {definition}')

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_login_events_user ON login_events(user_id, id DESC)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_login_events_time ON login_events(id DESC)")

    conn.commit()
    conn.close()

# Cài đặt
def get_setting(key, default=""):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT value FROM settings WHERE key = ?", (key,))
    row = c.fetchone()
    conn.close()
    return row['value'] if row else default

def set_setting(key, value):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, str(value)))
    conn.commit()
    conn.close()

# Môn học
def get_all_subjects():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
    SELECT s.*, 
        (SELECT COUNT(*) FROM questions q WHERE q.subject_id = s.id) as question_count,
        (SELECT COUNT(*) FROM flashcards f WHERE f.subject_id = s.id) as flashcard_count,
        (SELECT COUNT(*) FROM exercises e WHERE e.subject_id = s.id) as exercise_count
    FROM subjects s 
    ORDER BY s.id ASC
    """)
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def add_subject(code, name, icon='📚', category='Đại cương', description=''):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
    INSERT OR IGNORE INTO subjects (code, name, icon, category, description)
    VALUES (?, ?, ?, ?, ?)
    """, (code, name, icon, category, description))
    conn.commit()
    c.execute("SELECT id FROM subjects WHERE code = ?", (code,))
    row = c.fetchone()
    sid = row['id'] if row else c.lastrowid
    conn.close()
    return sid

def delete_subject(subject_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM subjects WHERE id = ?", (subject_id,))
    c.execute("DELETE FROM questions WHERE subject_id = ?", (subject_id,))
    c.execute("DELETE FROM flashcards WHERE subject_id = ?", (subject_id,))
    c.execute("DELETE FROM exercises WHERE subject_id = ?", (subject_id,))
    c.execute("DELETE FROM exam_results WHERE subject_id = ?", (subject_id,))
    conn.commit()
    conn.close()

# Câu hỏi
def get_questions_by_subject(subject_id, q_type=None, limit=None, random_order=False, topic_tag=None):
    conn = get_connection()
    c = conn.cursor()
    query = "SELECT * FROM questions WHERE subject_id = ?"
    params = [subject_id]
    
    if q_type and q_type != 'all':
        query += " AND q_type = ?"
        params.append(q_type)

    if topic_tag and topic_tag != 'all':
        query += " AND (topic_tag LIKE ? OR topic_tag = ?)"
        params.extend([f"%{topic_tag}%", topic_tag])
        
    if random_order:
        query += " ORDER BY RANDOM()"
    else:
        query += " ORDER BY id ASC"
        
    if limit:
        query += f" LIMIT {int(limit)}"
        
    c.execute(query, params)
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def add_question(subject_id, question_text, option_a='', option_b='', option_c='', option_d='', correct_option='A', explanation='', difficulty='medium', q_type='mcq', code_snippet='', image_url='', topic_tag=''):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
    INSERT INTO questions (subject_id, question_text, code_snippet, option_a, option_b, option_c, option_d, correct_option, explanation, difficulty, q_type, image_url, topic_tag)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (subject_id, question_text, code_snippet, option_a, option_b, option_c, option_d, str(correct_option).strip(), explanation, difficulty, q_type, image_url or '', topic_tag or ''))
    conn.commit()
    q_id = c.lastrowid
    conn.close()
    return q_id

# Bài tập lớn / Tự luận thực hành
def get_exercises_by_subject(subject_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM exercises WHERE subject_id = ? ORDER BY id ASC", (subject_id,))
    rows = [dict(r) for r in c.fetchall()]
    for r in rows:
        try:
            r['specs'] = json.loads(r.get('specs_json') or '[]')
        except Exception:
            r['specs'] = []
        try:
            r['test_cases'] = json.loads(r.get('test_cases_json') or '[]')
        except Exception:
            r['test_cases'] = []
    conn.close()
    return rows

def get_exercise_by_id(exercise_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM exercises WHERE id = ?", (exercise_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    r = dict(row)
    try:
        r['specs'] = json.loads(r.get('specs_json') or '[]')
    except Exception:
        r['specs'] = []
    try:
        r['test_cases'] = json.loads(r.get('test_cases_json') or '[]')
    except Exception:
        r['test_cases'] = []
    return r

def get_essay_prompts(subject_id=None):
    conn = get_connection()
    c = conn.cursor()
    if subject_id:
        c.execute("SELECT * FROM essay_prompts WHERE subject_id = ? ORDER BY id ASC", (subject_id,))
    else:
        c.execute("SELECT * FROM essay_prompts ORDER BY id ASC")
    rows = [dict(r) for r in c.fetchall()]
    for r in rows:
        try:
            r['rubric'] = json.loads(r.get('rubric_json') or '{}')
        except Exception:
            r['rubric'] = {}
    conn.close()
    return rows

def add_exercise(subject_id, title, problem, specs, sample_code, difficulty='hard'):
    conn = get_connection()
    c = conn.cursor()
    specs_json = json.dumps(specs, ensure_ascii=False) if isinstance(specs, list) else str(specs)
    c.execute("""
    INSERT INTO exercises (subject_id, title, problem, specs_json, sample_code, difficulty)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (subject_id, title, problem, specs_json, sample_code, difficulty))
    conn.commit()
    e_id = c.lastrowid
    conn.close()
    return e_id

# Flashcards với SM-2 Spaced Repetition
def get_flashcards_by_subject(subject_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM flashcards WHERE subject_id = ? ORDER BY id ASC", (subject_id,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def add_flashcard(subject_id, front, back, hint='', image_url=''):
    conn = get_connection()
    c = conn.cursor()
    today_str = date.today().isoformat()
    c.execute("""
    INSERT INTO flashcards (subject_id, front, back, hint, image_url, repetitions, interval_days, ease_factor, next_review)
    VALUES (?, ?, ?, ?, ?, 0, 1, 2.5, ?)
    """, (subject_id, front, back, hint, image_url or '', today_str))
    conn.commit()
    fc_id = c.lastrowid
    conn.close()
    return fc_id

def get_discussions_by_question(question_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
    SELECT * FROM question_discussions
    WHERE question_id = ?
    ORDER BY is_verified DESC, upvotes DESC, id ASC
    """, (question_id,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def add_discussion_comment(question_id, author_name, content, author_role='student', is_verified=0):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
    INSERT INTO question_discussions (question_id, author_name, author_role, content, upvotes, is_verified)
    VALUES (?, ?, ?, ?, 1, ?)
    """, (int(question_id), str(author_name or 'Sinh viên').strip(), str(author_role), str(content).strip(), int(is_verified)))
    conn.commit()
    cid = c.lastrowid
    conn.close()
    return cid

def upvote_discussion_comment(comment_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE question_discussions SET upvotes = upvotes + 1 WHERE id = ?", (int(comment_id),))
    conn.commit()
    c.execute("SELECT upvotes FROM question_discussions WHERE id = ?", (int(comment_id),))
    row = c.fetchone()
    conn.close()
    return row['upvotes'] if row else 1

def update_flashcard_review(card_id, rating):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM flashcards WHERE id = ?", (card_id,))
    card = c.fetchone()
    if not card:
        conn.close()
        return None
    
    rep = card['repetitions']
    interval = card['interval_days']
    ef = card['ease_factor']
    
    q = 2 if rating == 1 else (4 if rating == 2 else 5)
    
    if q >= 3:
        if rep == 0:
            interval = 1
        elif rep == 1:
            interval = 6
        else:
            interval = int(round(interval * ef))
        rep += 1
    else:
        rep = 0
        interval = 1
        
    ef = ef + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
    if ef < 1.3:
        ef = 1.3
        
    next_date = (date.today() + timedelta(days=interval)).isoformat()
    
    c.execute("""
    UPDATE flashcards 
    SET repetitions = ?, interval_days = ?, ease_factor = ?, next_review = ?
    WHERE id = ?
    """, (rep, interval, ef, next_date, card_id))
    
    conn.commit()
    conn.close()
    return {"repetitions": rep, "interval_days": interval, "next_review": next_date}

# Kết quả thi
def save_exam_result(subject_id, total_questions, correct_answers, score, time_spent_seconds, detail_json='[]', exam_type='mixed', user_id=1):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
    INSERT INTO exam_results (subject_id, total_questions, correct_answers, score, time_spent_seconds, detail_json, exam_type, user_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (subject_id, total_questions, correct_answers, score, time_spent_seconds, detail_json, exam_type, user_id))
    conn.commit()
    res_id = c.lastrowid
    conn.close()
    return res_id


def get_exam_result(exam_id: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM exam_results WHERE id = ?", (exam_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def get_stats():
    conn = get_connection()
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) as total_exams, AVG(score) as avg_score, SUM(total_questions) as total_q_answered FROM exam_results")
    stat_row = c.fetchone()
    
    c.execute("""
    SELECT s.name, s.code, COUNT(e.id) as exam_count, AVG(e.score) as avg_score
    FROM subjects s
    LEFT JOIN exam_results e ON s.id = e.subject_id
    GROUP BY s.id
    """)
    subject_stats = [dict(r) for r in c.fetchall()]
    
    c.execute("SELECT id, subject_id, total_questions, correct_answers, score, time_spent_seconds, created_at, exam_type, user_id FROM exam_results ORDER BY created_at DESC LIMIT 15")
    recent_exams = [dict(r) for r in c.fetchall()]
    
    conn.close()
    return {
        "total_exams": stat_row['total_exams'] or 0,
        "avg_score": round(stat_row['avg_score'] or 0, 1),
        "total_q_answered": stat_row['total_q_answered'] or 0,
        "subject_stats": subject_stats,
        "recent_exams": recent_exams
    }


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

def record_login_event(user_id: int, ip_address: str, user_agent: str = '', event_type: str = 'login',
                       username: str = '', success: bool = True):
    """Lưu nhật ký xác thực.

    event_type: 'login' | 'register' | 'logout' | 'login_failed' | 'session'
    - Đăng nhập sai vẫn được ghi (user_id = 0 nếu không khớp tài khoản nào) để admin phát hiện dò mật khẩu.
    - IP/User-Agent được cắt ngắn để tránh lưu dữ liệu thừa.
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO login_events (user_id, ip_address, user_agent, event_type, username, success) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (int(user_id or 0), str(ip_address or 'unknown')[:64], str(user_agent or '')[:512],
         str(event_type or 'login')[:32], str(username or '')[:64], 1 if success else 0)
    )
    # Giữ bảng gọn: chỉ giữ 5000 sự kiện gần nhất
    c.execute("DELETE FROM login_events WHERE id <= (SELECT MAX(id) FROM login_events) - 5000")
    conn.commit()
    conn.close()


def touch_user_seen(user_id: int, min_interval_seconds: int = 300):
    """Cập nhật 'lần cuối hoạt động'. Trả về True nếu đây là lần quay lại mới (đã lâu chưa thấy).

    Cookie phiên sống 30 ngày nên người dùng quay lại không cần đăng nhập lại ->
    nếu chỉ ghi lúc nhập mật khẩu thì sẽ trông như 'không ai đăng nhập'.
    """
    if not user_id:
        return False
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "SELECT CAST(strftime('%s','now') AS INTEGER) - CAST(strftime('%s', COALESCE(last_seen,'1970-01-01')) AS INTEGER) "
        "FROM users WHERE id = ?", (int(user_id),)
    )
    row = c.fetchone()
    is_new_visit = False
    if row is not None and (row[0] is None or row[0] >= int(min_interval_seconds)):
        c.execute("UPDATE users SET last_seen = CURRENT_TIMESTAMP WHERE id = ?", (int(user_id),))
        conn.commit()
        is_new_visit = row[0] is None or row[0] >= 1800  # >30 phút mới tính là lượt truy cập mới
    conn.close()
    return is_new_visit


def get_login_events(user_id: int, limit: int = 30):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT id, ip_address, user_agent, event_type, success, created_at
        FROM login_events WHERE user_id = ? ORDER BY id DESC LIMIT ?
    """, (int(user_id), max(1, min(int(limit), 100))))
    rows = [dict(row) for row in c.fetchall()]
    conn.close()
    return rows


def get_all_login_events(limit: int = 100, only_failed: bool = False):
    """Nhật ký toàn hệ thống (dành cho admin), kèm tên tài khoản."""
    conn = get_connection()
    c = conn.cursor()
    where = "WHERE e.success = 0" if only_failed else ""
    c.execute(f"""
        SELECT e.id, e.user_id, COALESCE(NULLIF(u.username,''), e.username, '') AS username,
               COALESCE(u.full_name, '') AS full_name, e.ip_address, e.user_agent,
               e.event_type, e.success, e.created_at
        FROM login_events e LEFT JOIN users u ON u.id = e.user_id
        {where}
        ORDER BY e.id DESC LIMIT ?
    """, (max(1, min(int(limit), 500)),))
    rows = [dict(row) for row in c.fetchall()]
    conn.close()
    return rows


def get_login_summary():
    """Số liệu tổng quan để admin biết hệ thống có đang được dùng không."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT
          COUNT(*) AS total,
          SUM(CASE WHEN event_type='login' AND success=1 THEN 1 ELSE 0 END) AS logins,
          SUM(CASE WHEN success=0 THEN 1 ELSE 0 END) AS failed,
          SUM(CASE WHEN created_at >= datetime('now','-1 day') THEN 1 ELSE 0 END) AS last_24h,
          COUNT(DISTINCT CASE WHEN created_at >= datetime('now','-7 day') AND user_id>0 THEN user_id END) AS active_users_7d
        FROM login_events
    """)
    row = dict(c.fetchone())
    c.execute("SELECT COUNT(*) FROM users")
    row["total_users"] = c.fetchone()[0]
    c.execute("SELECT MIN(created_at) FROM login_events")
    row["tracking_since"] = c.fetchone()[0]
    conn.close()
    return {k: (v or 0) if k not in ("tracking_since",) else v for k, v in row.items()}


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
        SELECT u.id, u.username, u.full_name, u.role, u.created_at, u.last_login, u.last_seen,
               (SELECT COUNT(*) FROM login_events le WHERE le.user_id = u.id AND le.event_type = 'login' AND le.success = 1) AS login_count,
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


def save_archived_item(history_type: str, item_id: str, payload_json: str):
    conn = get_connection()
    try:
        conn.execute("""
            INSERT INTO archived_history (history_type, item_id, payload_json)
            VALUES (?, ?, ?)
        """, (history_type, item_id, payload_json))
        conn.commit()
    finally:
        conn.close()

def get_archived_items(history_type: str = None, limit: int = 100):
    conn = get_connection()
    c = conn.cursor()
    if history_type:
        c.execute("""
        SELECT id, history_type, item_id, payload_json, archived_at
        FROM archived_history
        WHERE history_type = ?
        ORDER BY archived_at DESC LIMIT ?
        """, (history_type, limit))
    else:
        c.execute("""
        SELECT id, history_type, item_id, payload_json, archived_at
        FROM archived_history
        ORDER BY archived_at DESC LIMIT ?
        """, (limit,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def delete_archived_item(archive_id: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM archived_history WHERE id = ?", (archive_id,))
    conn.commit()
    conn.close()
