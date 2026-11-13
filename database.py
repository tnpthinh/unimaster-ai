"""
Database manager for UniMaster AI using SQLite
Updated with multi-format questions (MCQ, True/False, Short Answer, Essay/Coding) and Exercises
"""
import sqlite3
import json
import os
import re
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

def load_env_file(env_path=None):
    """Load simple KEY=VALUE pairs from .env without requiring python-dotenv."""
    if env_path is None:
        env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if not os.path.isfile(env_path):
        return False
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for raw_line in f:
                line = raw_line.strip()
                if not line or line.startswith("#"):
                    continue
                if line.startswith("export "):
                    line = line[7:].strip()
                if "=" not in line:
                    continue
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip()
                if not key:
                    continue
                if len(val) >= 2 and ((val[0] == '"' and val[-1] == '"') or (val[0] == "'" and val[-1] == "'")):
                    val = val[1:-1]
                if key not in os.environ or os.environ.get(key, "") == "":
                    os.environ[key] = val
        return True
    except Exception:
        return False


load_env_file()


def get_connection():
    conn = sqlite3.connect(DB_PATH, timeout=15.0)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.execute("PRAGMA busy_timeout=10000")
        conn.execute("PRAGMA temp_store=MEMORY")
        conn.execute("PRAGMA cache_size=-16000")
    except Exception:
        pass
    return conn

def init_db():
    conn = get_connection()
    try:
        conn.execute("PRAGMA journal_mode=WAL")
    except Exception:
        pass
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

    # Tiến trình học dở (Save & Resume drafts per account/browser profile)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS study_progress (
        account_id TEXT NOT NULL,
        draft_key TEXT NOT NULL,
        progress_type TEXT NOT NULL DEFAULT 'exam',
        subject_id INTEGER,
        chapter_tag TEXT DEFAULT '',
        title TEXT DEFAULT '',
        payload_json TEXT NOT NULL DEFAULT '{}',
        current_index INTEGER DEFAULT 0,
        total_items INTEGER DEFAULT 0,
        answered_count INTEGER DEFAULT 0,
        updated_at TEXT NOT NULL,
        PRIMARY KEY (account_id, draft_key)
    )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_study_progress_acc_updated ON study_progress(account_id, updated_at DESC)")

    # Core query performance indices (6,800+ questions, flashcards, exams, discussions)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_questions_subject_type ON questions(subject_id, q_type)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_questions_subject_topic ON questions(subject_id, topic_tag)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_flashcards_subject ON flashcards(subject_id, interval_days)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_exercises_subject ON exercises(subject_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_exam_results_subject_time ON exam_results(subject_id, created_at DESC)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_exam_results_user ON exam_results(user_id, created_at DESC)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_discussions_question ON question_discussions(question_id, is_verified DESC, upvotes DESC)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_archived_history_type_time ON archived_history(history_type, archived_at DESC)")

    # Bảng quản lý API Keys an toàn (gitignored DB, không đưa lên cloud seed)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ai_api_keys (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        provider TEXT NOT NULL DEFAULT 'gemini',
        label TEXT NOT NULL DEFAULT '',
        api_key TEXT NOT NULL UNIQUE,
        masked_key TEXT NOT NULL DEFAULT '',
        key_type TEXT NOT NULL DEFAULT 'gemini',
        is_enabled INTEGER NOT NULL DEFAULT 1,
        status TEXT NOT NULL DEFAULT 'ready',
        model TEXT DEFAULT '',
        latency_ms INTEGER,
        calls INTEGER NOT NULL DEFAULT 0,
        failovers INTEGER NOT NULL DEFAULT 0,
        last_error TEXT DEFAULT '',
        last_checked_at TEXT DEFAULT '',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ai_api_keys_provider ON ai_api_keys(provider, id ASC)")

    # Bảng phiên & lịch sử hội thoại Gia Sư AI (hỗ trợ soft-archive & khôi phục theo tài khoản)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ai_chat_sessions (
        session_id TEXT PRIMARY KEY,
        account_id TEXT NOT NULL DEFAULT 'acc_default',
        title TEXT NOT NULL DEFAULT 'Phiên hỏi đáp AI',
        subject_id INTEGER,
        subject_name TEXT DEFAULT '',
        mode TEXT DEFAULT 'explain',
        persona TEXT DEFAULT 'professor',
        is_archived INTEGER NOT NULL DEFAULT 0,
        message_count INTEGER NOT NULL DEFAULT 0,
        last_message_preview TEXT DEFAULT '',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ai_chat_sessions_acc_arch ON ai_chat_sessions(account_id, is_archived, updated_at DESC)")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tutor_chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        account_id TEXT NOT NULL DEFAULT 'acc_default',
        role TEXT NOT NULL DEFAULT 'user',
        content TEXT NOT NULL,
        mode TEXT DEFAULT 'explain',
        context_json TEXT DEFAULT '{}',
        provider_used TEXT DEFAULT '',
        model_used TEXT DEFAULT '',
        masked_key TEXT DEFAULT '',
        latency_ms INTEGER,
        created_at TEXT NOT NULL
    )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tutor_chats_session ON tutor_chats(session_id, id ASC)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tutor_chats_account ON tutor_chats(account_id, id DESC)")

    conn.commit()

    # ---------------------------------------------------------------------
    # Vá dữ liệu 11 bài "Thực Hành Code" bị sinh sai từ script seed cũ.
    #
    # Vì sao phải vá Ở ĐÂY (trong init_db) mà không chỉ sửa file seed:
    #   Trên cloud, `data/unimaster.db` đã tồn tại từ lần deploy đầu tiên.
    #   `database.py` chỉ COPY seed -> data KHI file data CHƯA có. Nghĩa là
    #   sửa `seed/unimaster_seed.db` sẽ KHÔNG ảnh hưởng gì tới bản đang chạy.
    #   Vì vậy phải có một bước migration chạy mỗi lần khởi động, tự sửa
    #   dữ liệu đã nằm trong DB thật.
    # ---------------------------------------------------------------------
    try:
        import coding_exercise_fixes
        fixed = coding_exercise_fixes.repair_coding_exercises(conn)
        if fixed:
            print(f"[init_db] Đã vá {fixed} bài Thực Hành Code bị lỗi dữ liệu.")
    except Exception as _e:
        print(f"[init_db] Bỏ qua bước vá bài tập: {_e}")

    conn.close()


def _utc_iso_now():
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc)
    iso = now.strftime("%Y-%m-%dT%H:%M:%S.") + f"{now.microsecond // 1000:03d}Z"
    return iso, int(now.timestamp() * 1000)


def _iso_to_ms(iso_str: str) -> int:
    from datetime import datetime, timezone
    if not iso_str:
        return 0
    s = str(iso_str).strip()
    try:
        if s.endswith("Z"):
            s = s[:-1] + "+00:00"
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return int(dt.timestamp() * 1000)
    except Exception:
        return 0


def _sanitize_account_id(account_id: str) -> str:
    acc = (account_id or "").strip()
    if not acc:
        return "acc_default"
    return acc[:128]


def _sanitize_draft_key(draft_key: str) -> str:
    key = (draft_key or "").strip()
    return key[:128]


def _serialize_progress_row(row) -> dict:
    d = dict(row)
    raw_payload = d.get("payload_json") or "{}"
    try:
        parsed = json.loads(raw_payload)
        if not isinstance(parsed, (dict, list)):
            parsed = {}
    except Exception:
        parsed = {}
    d["payload"] = parsed
    d["payload_json"] = raw_payload if isinstance(raw_payload, str) else json.dumps(parsed, ensure_ascii=False)
    d["current_index"] = int(d.get("current_index") or 0)
    d["total_items"] = int(d.get("total_items") or 0)
    d["answered_count"] = int(d.get("answered_count") or 0)
    d["updated_at_ms"] = _iso_to_ms(d.get("updated_at") or "")
    return d


def list_study_progress(account_id="acc_default", progress_type=None, subject_id=None, limit=50):
    acc = _sanitize_account_id(account_id)
    lim = max(1, min(200, int(limit or 50)))
    conn = get_connection()
    try:
        query = "SELECT * FROM study_progress WHERE account_id = ?"
        params = [acc]
        if progress_type:
            query += " AND progress_type = ?"
            params.append(str(progress_type).strip()[:64])
        if subject_id is not None and str(subject_id).strip() != "":
            try:
                query += " AND subject_id = ?"
                params.append(int(subject_id))
            except (TypeError, ValueError):
                pass
        query += " ORDER BY updated_at DESC LIMIT ?"
        params.append(lim)
        rows = conn.execute(query, tuple(params)).fetchall()
        return [_serialize_progress_row(r) for r in rows]
    finally:
        conn.close()


def get_study_progress(account_id, draft_key):
    acc = _sanitize_account_id(account_id)
    dkey = _sanitize_draft_key(draft_key)
    if not dkey:
        return None
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM study_progress WHERE account_id = ? AND draft_key = ?",
            (acc, dkey),
        ).fetchone()
        return _serialize_progress_row(row) if row else None
    finally:
        conn.close()


def upsert_study_progress(
    account_id,
    draft_key,
    progress_type="exam",
    subject_id=None,
    chapter_tag="",
    title="",
    payload=None,
    payload_json=None,
    current_index=0,
    total_items=0,
    answered_count=0,
):
    acc = _sanitize_account_id(account_id)
    dkey = _sanitize_draft_key(draft_key)
    if not dkey:
        raise ValueError("draft_key is required")

    ptype = (str(progress_type or "exam").strip() or "exam")[:64]
    subj_val = None
    if subject_id is not None and str(subject_id).strip() != "":
        try:
            subj_val = int(subject_id)
        except (TypeError, ValueError):
            subj_val = None

    chap = str(chapter_tag or "").strip()[:256]
    ttl = str(title or "").strip()[:256]

    if payload_json is not None and isinstance(payload_json, str) and payload_json.strip():
        p_str = payload_json.strip()
        try:
            json.loads(p_str)
        except Exception:
            p_str = json.dumps({"raw": p_str}, ensure_ascii=False)
    elif payload is not None:
        if isinstance(payload, str):
            p_str = payload.strip() or "{}"
        else:
            p_str = json.dumps(payload, ensure_ascii=False)
    else:
        p_str = "{}"

    if len(p_str.encode("utf-8")) > 2 * 1024 * 1024:
        raise ValueError("payload exceeds 2MB limit")

    try:
        cur_idx = max(0, int(current_index or 0))
    except (TypeError, ValueError):
        cur_idx = 0
    try:
        tot_items = max(0, int(total_items or 0))
    except (TypeError, ValueError):
        tot_items = 0
    try:
        ans_cnt = max(0, int(answered_count or 0))
    except (TypeError, ValueError):
        ans_cnt = 0

    iso_now, _ = _utc_iso_now()
    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO study_progress (
                account_id, draft_key, progress_type, subject_id, chapter_tag,
                title, payload_json, current_index, total_items, answered_count, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(account_id, draft_key) DO UPDATE SET
                progress_type = excluded.progress_type,
                subject_id = excluded.subject_id,
                chapter_tag = excluded.chapter_tag,
                title = excluded.title,
                payload_json = excluded.payload_json,
                current_index = excluded.current_index,
                total_items = excluded.total_items,
                answered_count = excluded.answered_count,
                updated_at = excluded.updated_at
            """,
            (acc, dkey, ptype, subj_val, chap, ttl, p_str, cur_idx, tot_items, ans_cnt, iso_now),
        )
        conn.commit()
        row = conn.execute(
            "SELECT * FROM study_progress WHERE account_id = ? AND draft_key = ?",
            (acc, dkey),
        ).fetchone()
        return _serialize_progress_row(row) if row else None
    finally:
        conn.close()


def delete_study_progress(account_id, draft_key) -> bool:
    acc = _sanitize_account_id(account_id)
    dkey = _sanitize_draft_key(draft_key)
    if not dkey:
        return False
    conn = get_connection()
    try:
        cur = conn.execute(
            "DELETE FROM study_progress WHERE account_id = ? AND draft_key = ?",
            (acc, dkey),
        )
        conn.commit()
        return cur.rowcount > 0
    finally:
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


# ==========================================
# AI API KEYS POOL & PERSISTENT TUTOR CHATS
# ==========================================
def list_ai_api_keys(provider: str = "gemini") -> list[dict]:
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM ai_api_keys WHERE provider = ? ORDER BY id ASC",
            (str(provider or "gemini").strip(),),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def upsert_ai_api_key(
    api_key: str,
    provider: str = "gemini",
    label: str = "",
    masked_key: str = "",
    key_type: str = "gemini",
    is_enabled: bool = True,
    status: str = "ready",
    model: str = "",
    latency_ms=None,
    last_error: str = "",
    last_checked_at: str = "",
) -> dict:
    raw_k = str(api_key or "").strip()
    if not raw_k:
        raise ValueError("api_key is required")
    iso_now, _ = _utc_iso_now()
    prov = str(provider or "gemini").strip()[:32]
    lbl = str(label or "").strip()[:80]
    mk = str(masked_key or "").strip()[:64]
    kt = str(key_type or "gemini").strip()[:32]
    conn = get_connection()
    try:
        existing = conn.execute("SELECT * FROM ai_api_keys WHERE api_key = ?", (raw_k,)).fetchone()
        if existing:
            conn.execute(
                """
                UPDATE ai_api_keys
                SET provider = ?,
                    label = COALESCE(NULLIF(?, ''), label),
                    masked_key = COALESCE(NULLIF(?, ''), masked_key),
                    key_type = COALESCE(NULLIF(?, ''), key_type),
                    updated_at = ?
                WHERE id = ?
                """,
                (prov, lbl, mk, kt, iso_now, existing["id"]),
            )
            conn.commit()
            row = conn.execute("SELECT * FROM ai_api_keys WHERE id = ?", (existing["id"],)).fetchone()
            return dict(row)
        cnt = conn.execute("SELECT COUNT(*) FROM ai_api_keys WHERE provider = ?", (prov,)).fetchone()[0]
        if not lbl:
            lbl = f"Key #{cnt + 1}"
        conn.execute(
            """
            INSERT INTO ai_api_keys (
                provider, label, api_key, masked_key, key_type, is_enabled,
                status, model, latency_ms, calls, failovers, last_error,
                last_checked_at, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 0, ?, ?, ?, ?)
            """,
            (
                prov, lbl, raw_k, mk, kt, 1 if is_enabled else 0,
                str(status or "ready")[:32], str(model or "")[:80],
                int(latency_ms) if latency_ms is not None else None,
                str(last_error or "")[:300], str(last_checked_at or "")[:64],
                iso_now, iso_now,
            ),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM ai_api_keys WHERE api_key = ?", (raw_k,)).fetchone()
        return dict(row)
    finally:
        conn.close()


def sync_ai_api_keys_pool(entries: list[dict], provider: str = "gemini") -> list[dict]:
    """Synchronize ai_api_keys table with the ordered pool while keeping telemetry."""
    prov = str(provider or "gemini").strip()[:32]
    iso_now, _ = _utc_iso_now()
    conn = get_connection()
    try:
        existing_rows = {
            r["api_key"]: dict(r)
            for r in conn.execute("SELECT * FROM ai_api_keys WHERE provider = ?", (prov,)).fetchall()
        }
        desired_keys = []
        for idx, item in enumerate(entries or []):
            k = str(item.get("key") or item.get("api_key") or "").strip()
            if not k:
                continue
            desired_keys.append(k)
            lbl = str(item.get("label") or f"Key #{idx + 1}").strip()[:80]
            mk = str(item.get("masked_key") or "").strip()[:64]
            kt = str(item.get("key_type") or "gemini").strip()[:32]
            if k in existing_rows:
                conn.execute(
                    "UPDATE ai_api_keys SET label = ?, masked_key = COALESCE(NULLIF(?, ''), masked_key), key_type = COALESCE(NULLIF(?, ''), key_type), updated_at = ? WHERE api_key = ?",
                    (lbl, mk, kt, iso_now, k),
                )
            else:
                conn.execute(
                    """
                    INSERT INTO ai_api_keys (
                        provider, label, api_key, masked_key, key_type, is_enabled,
                        status, model, latency_ms, calls, failovers, last_error,
                        last_checked_at, created_at, updated_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, '', NULL, 0, 0, '', '', ?, ?)
                    """,
                    (prov, lbl, k, mk, kt, 1 if item.get("is_enabled", True) else 0, str(item.get("status") or "ready")[:32], iso_now, iso_now),
                )
        for old_k in list(existing_rows.keys()):
            if old_k not in desired_keys:
                conn.execute("DELETE FROM ai_api_keys WHERE provider = ? AND api_key = ?", (prov, old_k))
        conn.commit()
        rows = conn.execute("SELECT * FROM ai_api_keys WHERE provider = ? ORDER BY id ASC", (prov,)).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def toggle_ai_api_key(key_id: int = None, api_key: str = None, enabled: bool = None) -> dict | None:
    conn = get_connection()
    try:
        if key_id is not None:
            row = conn.execute("SELECT * FROM ai_api_keys WHERE id = ?", (int(key_id),)).fetchone()
        elif api_key:
            row = conn.execute("SELECT * FROM ai_api_keys WHERE api_key = ?", (str(api_key).strip(),)).fetchone()
        else:
            return None
        if not row:
            return None
        new_val = (1 if enabled else 0) if enabled is not None else (0 if row["is_enabled"] else 1)
        iso_now, _ = _utc_iso_now()
        new_status = row["status"] if new_val else "disabled"
        if new_val and row["status"] == "disabled":
            new_status = "ready"
        conn.execute(
            "UPDATE ai_api_keys SET is_enabled = ?, status = ?, updated_at = ? WHERE id = ?",
            (new_val, new_status, iso_now, row["id"]),
        )
        conn.commit()
        updated = conn.execute("SELECT * FROM ai_api_keys WHERE id = ?", (row["id"],)).fetchone()
        return dict(updated) if updated else None
    finally:
        conn.close()


def update_ai_api_key_telemetry(
    api_key: str,
    status: str = None,
    model: str = None,
    latency_ms=None,
    calls_inc: int = 0,
    failovers_inc: int = 0,
    last_error: str = None,
    last_checked_at: str = None,
) -> None:
    raw_k = str(api_key or "").strip()
    if not raw_k:
        return
    iso_now, _ = _utc_iso_now()
    conn = get_connection()
    try:
        row = conn.execute("SELECT * FROM ai_api_keys WHERE api_key = ?", (raw_k,)).fetchone()
        if not row:
            return
        new_status = str(status if status is not None else row["status"])[:32]
        if not row["is_enabled"]:
            new_status = "disabled"
        new_model = str(model if model is not None else (row["model"] or ""))[:80]
        new_lat = int(latency_ms) if latency_ms is not None else row["latency_ms"]
        new_calls = int(row["calls"] or 0) + int(calls_inc or 0)
        new_failovers = int(row["failovers"] or 0) + int(failovers_inc or 0)
        new_err = str(last_error if last_error is not None else (row["last_error"] or ""))[:300]
        new_chk = str(last_checked_at if last_checked_at is not None else (row["last_checked_at"] or ""))[:64]
        conn.execute(
            """
            UPDATE ai_api_keys
            SET status = ?, model = ?, latency_ms = ?, calls = ?, failovers = ?,
                last_error = ?, last_checked_at = ?, updated_at = ?
            WHERE id = ?
            """,
            (new_status, new_model, new_lat, new_calls, new_failovers, new_err, new_chk, iso_now, row["id"]),
        )
        conn.commit()
    finally:
        conn.close()


def _serialize_chat_message(row) -> dict:
    d = dict(row)
    raw_ctx = d.pop("context_json", "{}") or "{}"
    try:
        ctx = json.loads(raw_ctx)
        if not isinstance(ctx, dict):
            ctx = {}
    except Exception:
        ctx = {}
    d["context"] = ctx
    return d


def _serialize_chat_session(row, messages=None) -> dict:
    d = dict(row)
    d["is_archived"] = bool(d.get("is_archived"))
    d["message_count"] = int(d.get("message_count") or 0)
    if messages is not None:
        d["messages"] = messages
    return d


def save_tutor_chat_turn(
    account_id: str = "acc_default",
    session_id: str = None,
    title: str = "",
    subject_id=None,
    subject_name: str = "",
    mode: str = "explain",
    persona: str = "professor",
    role: str = "user",
    content: str = "",
    context=None,
    provider_used: str = "",
    model_used: str = "",
    masked_key: str = "",
    latency_ms=None,
    messages: list = None,
    replace: bool = False,
) -> dict:
    import secrets as _secrets
    acc = _sanitize_account_id(account_id)
    sid_str = str(session_id or "").strip()[:128] or f"sess_{int(datetime.now().timestamp())}_{_secrets.token_hex(4)}"
    iso_now, _ = _utc_iso_now()

    subj_val = None
    if subject_id is not None and str(subject_id).strip() != "":
        try:
            subj_val = int(subject_id)
        except (TypeError, ValueError):
            subj_val = None

    sname = str(subject_name or "").strip()[:160]
    m_val = str(mode or "explain").strip()[:32]
    p_val = str(persona or "professor").strip()[:32]
    ttl = str(title or "").strip()[:200]

    msg_items = []
    if isinstance(messages, list) and messages:
        for m in messages:
            if not isinstance(m, dict):
                continue
            mc = str(m.get("content") or m.get("text") or "").strip()
            if not mc:
                continue
            mr = "model" if str(m.get("role") or "user").strip() in ("model", "assistant") else "user"
            mctx = m.get("context") if isinstance(m.get("context"), dict) else (context if isinstance(context, dict) else {})
            msg_items.append({
                "role": mr,
                "content": mc,
                "mode": str(m.get("mode") or m_val)[:32],
                "context_json": json.dumps(mctx, ensure_ascii=False),
                "provider_used": str(m.get("provider_used") or provider_used or "")[:64],
                "model_used": str(m.get("model_used") or model_used or "")[:80],
                "masked_key": str(m.get("masked_key") or masked_key or "")[:64],
                "latency_ms": int(m["latency_ms"]) if m.get("latency_ms") is not None else (int(latency_ms) if latency_ms is not None else None),
            })
    elif str(content or "").strip():
        mr = "model" if str(role or "user").strip() in ("model", "assistant") else "user"
        ctx_dict = context if isinstance(context, dict) else {}
        msg_items.append({
            "role": mr,
            "content": str(content).strip(),
            "mode": m_val,
            "context_json": json.dumps(ctx_dict, ensure_ascii=False),
            "provider_used": str(provider_used or "")[:64],
            "model_used": str(model_used or "")[:80],
            "masked_key": str(masked_key or "")[:64],
            "latency_ms": int(latency_ms) if latency_ms is not None else None,
        })

    if not ttl and msg_items:
        first_txt = re.sub(r"\s+", " ", msg_items[0]["content"]).strip()
        prefix = f"{sname} — " if sname else ""
        ttl = (prefix + first_txt)[:120]
    if not ttl:
        ttl = f"Hội thoại {sname or 'Gia sư AI'}"

    conn = get_connection()
    try:
        existing = conn.execute(
            "SELECT * FROM ai_chat_sessions WHERE session_id = ? AND account_id = ?",
            (sid_str, acc),
        ).fetchone()
        if not existing:
            conn.execute(
                """
                INSERT INTO ai_chat_sessions (
                    session_id, account_id, title, subject_id, subject_name,
                    mode, persona, is_archived, message_count, last_message_preview,
                    created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, 0, 0, '', ?, ?)
                """,
                (sid_str, acc, ttl, subj_val, sname, m_val, p_val, iso_now, iso_now),
            )
        else:
            conn.execute(
                """
                UPDATE ai_chat_sessions
                SET subject_id = COALESCE(?, subject_id),
                    subject_name = COALESCE(NULLIF(?, ''), subject_name),
                    mode = COALESCE(NULLIF(?, ''), mode),
                    persona = COALESCE(NULLIF(?, ''), persona),
                    is_archived = 0,
                    updated_at = ?
                WHERE session_id = ? AND account_id = ?
                """,
                (subj_val, sname, m_val, p_val, iso_now, sid_str, acc),
            )

        if replace and isinstance(messages, list) and messages:
            conn.execute("DELETE FROM tutor_chats WHERE session_id = ? AND account_id = ?", (sid_str, acc))

        for item in msg_items:
            conn.execute(
                """
                INSERT INTO tutor_chats (
                    session_id, account_id, role, content, mode, context_json,
                    provider_used, model_used, masked_key, latency_ms, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    sid_str, acc, item["role"], item["content"], item["mode"], item["context_json"],
                    item["provider_used"], item["model_used"], item["masked_key"], item["latency_ms"], iso_now,
                ),
            )

        cnt = conn.execute(
            "SELECT COUNT(*) FROM tutor_chats WHERE session_id = ? AND account_id = ?",
            (sid_str, acc),
        ).fetchone()[0]
        last_row = conn.execute(
            "SELECT content FROM tutor_chats WHERE session_id = ? AND account_id = ? ORDER BY id DESC LIMIT 1",
            (sid_str, acc),
        ).fetchone()
        preview = re.sub(r"\s+", " ", (last_row["content"] if last_row else ""))[:180]
        conn.execute(
            "UPDATE ai_chat_sessions SET message_count = ?, last_message_preview = ?, updated_at = ? WHERE session_id = ? AND account_id = ?",
            (cnt, preview, iso_now, sid_str, acc),
        )
        conn.commit()

        srow = conn.execute(
            "SELECT * FROM ai_chat_sessions WHERE session_id = ? AND account_id = ?",
            (sid_str, acc),
        ).fetchone()
        mrows = conn.execute(
            "SELECT * FROM tutor_chats WHERE session_id = ? AND account_id = ? ORDER BY id ASC",
            (sid_str, acc),
        ).fetchall()
        return _serialize_chat_session(srow, [_serialize_chat_message(r) for r in mrows])
    finally:
        conn.close()


def list_tutor_chat_sessions(
    account_id: str = "acc_default",
    archived: str = "all",
    query: str = "",
    session_id: str = None,
    limit: int = 50,
) -> dict:
    acc = _sanitize_account_id(account_id)
    lim = max(1, min(200, int(limit or 50)))
    arch_filter = str(archived or "all").strip().lower()
    q_str = str(query or "").strip().lower()

    conn = get_connection()
    try:
        active_cnt = conn.execute(
            "SELECT COUNT(*) FROM ai_chat_sessions WHERE account_id = ? AND is_archived = 0",
            (acc,),
        ).fetchone()[0]
        arch_cnt = conn.execute(
            "SELECT COUNT(*) FROM ai_chat_sessions WHERE account_id = ? AND is_archived = 1",
            (acc,),
        ).fetchone()[0]

        sql = "SELECT * FROM ai_chat_sessions WHERE account_id = ?"
        params = [acc]
        if session_id:
            sql += " AND session_id = ?"
            params.append(str(session_id).strip()[:128])
        elif arch_filter in ("0", "false", "active"):
            sql += " AND is_archived = 0"
        elif arch_filter in ("1", "true", "archived", "archive"):
            sql += " AND is_archived = 1"

        if q_str:
            like = f"%{q_str}%"
            sql += (
                " AND (LOWER(title) LIKE ? OR LOWER(subject_name) LIKE ? "
                "OR LOWER(last_message_preview) LIKE ? "
                "OR EXISTS (SELECT 1 FROM tutor_chats tc WHERE tc.session_id = ai_chat_sessions.session_id "
                "AND tc.account_id = ai_chat_sessions.account_id "
                "AND (LOWER(tc.content) LIKE ? OR LOWER(tc.context_json) LIKE ?)))"
            )
            params.extend([like, like, like, like, like])

        sql += " ORDER BY updated_at DESC LIMIT ?"
        params.append(lim)
        srows = conn.execute(sql, tuple(params)).fetchall()

        sessions = []
        sids = [r["session_id"] for r in srows]
        msg_map = {sid: [] for sid in sids}
        if sids:
            placeholders = ",".join("?" * len(sids))
            mrows = conn.execute(
                f"SELECT * FROM tutor_chats WHERE account_id = ? AND session_id IN ({placeholders}) ORDER BY id ASC",
                tuple([acc] + sids),
            ).fetchall()
            for mr in mrows:
                msg_map[mr["session_id"]].append(_serialize_chat_message(mr))

        for sr in srows:
            sessions.append(_serialize_chat_session(sr, msg_map.get(sr["session_id"], [])))

        return {
            "account_id": acc,
            "sessions": sessions,
            "active_count": active_cnt,
            "archived_count": arch_cnt,
            "total_count": active_cnt + arch_cnt,
        }
    finally:
        conn.close()


def archive_tutor_chat_sessions(
    account_id: str = "acc_default",
    session_id: str = None,
    session_ids: list = None,
    archive_all_active: bool = False,
    restore: bool = False,
) -> int:
    acc = _sanitize_account_id(account_id)
    target_val = 0 if restore else 1
    iso_now, _ = _utc_iso_now()
    conn = get_connection()
    try:
        if archive_all_active:
            cur = conn.execute(
                "UPDATE ai_chat_sessions SET is_archived = ?, updated_at = ? WHERE account_id = ? AND is_archived = ?",
                (target_val, iso_now, acc, 1 if restore else 0),
            )
        else:
            ids = []
            if session_id:
                ids.append(str(session_id).strip()[:128])
            if isinstance(session_ids, list):
                for s in session_ids:
                    sv = str(s or "").strip()[:128]
                    if sv and sv not in ids:
                        ids.append(sv)
            if not ids:
                return 0
            placeholders = ",".join("?" * len(ids))
            cur = conn.execute(
                f"UPDATE ai_chat_sessions SET is_archived = ?, updated_at = ? WHERE account_id = ? AND session_id IN ({placeholders})",
                tuple([target_val, iso_now, acc] + ids),
            )
        conn.commit()
        return cur.rowcount
    finally:
        conn.close()


def delete_tutor_chat_session(account_id: str = "acc_default", session_id: str = "") -> bool:
    acc = _sanitize_account_id(account_id)
    sid = str(session_id or "").strip()[:128]
    if not sid:
        return False
    conn = get_connection()
    try:
        conn.execute("DELETE FROM tutor_chats WHERE account_id = ? AND session_id = ?", (acc, sid))
        cur = conn.execute("DELETE FROM ai_chat_sessions WHERE account_id = ? AND session_id = ?", (acc, sid))
        conn.commit()
        return cur.rowcount > 0
    finally:
        conn.close()
