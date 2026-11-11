r"""Tạo bản dữ liệu "sạch" để đưa lên Cloud / GitHub.

- Giữ nguyên: môn học, ngân hàng câu hỏi, flashcards, bài tập, đề tự luận.
- XÓA: API key (OpenAI + Gemini), tài khoản/mật khẩu, tiến độ học cá nhân,
  lịch sử thi, sổ tay câu sai, thảo luận, lịch sử lưu trữ.

Nhờ vậy file seed có thể commit lên GitHub mà không lộ bí mật, đồng thời
bản deploy cloud vẫn có đầy đủ 12 môn học kèm ngân hàng đề.

Chạy:  python make_cloud_seed.py
Kết quả: seed/unimaster_seed.db
"""
import os
import sqlite3

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "unimaster.db")
DST_DIR = os.path.join(ROOT, "seed")
DST = os.path.join(DST_DIR, "unimaster_seed.db")

# Khóa cấu hình có thể chứa bí mật hoặc dữ liệu riêng tư
SECRET_SETTING_KEYS = (
    "gemini_api_keys_pool",
    "gemini_api_key",
    "openai_api_key",
    "openai_base_url",
    "openai_model",
    "ai_provider_priority",
    "user_sync_state",
)

# Bảng chứa dữ liệu cá nhân — không được đưa lên kho mã công khai
PERSONAL_TABLES = (
    "users",
    "user_states",
    "exam_results",
    "mistake_notebook",
    "question_discussions",
    "archived_history",
)


def _table_exists(conn, name):
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (name,)
    ).fetchone()
    return row is not None


def build_clean_seed():
    """Sao chép database rồi xóa sạch bí mật và dữ liệu cá nhân."""
    if not os.path.exists(SRC):
        raise FileNotFoundError(f"Không tìm thấy database nguồn: {SRC}")

    os.makedirs(DST_DIR, exist_ok=True)
    for suffix in ("", "-journal", "-wal", "-shm"):
        candidate = DST + suffix
        if os.path.exists(candidate):
            os.remove(candidate)

    # Dùng backup API của SQLite để sao chép nhất quán ngay cả khi server đang chạy
    src = sqlite3.connect(SRC)
    dst = sqlite3.connect(DST)
    try:
        src.backup(dst)
    finally:
        src.close()

    try:
        dst.executemany(
            "DELETE FROM settings WHERE key = ?", [(k,) for k in SECRET_SETTING_KEYS]
        )
        for table in PERSONAL_TABLES:
            if _table_exists(dst, table):
                dst.execute(f"DELETE FROM {table}")
        dst.commit()
        # VACUUM ghi lại toàn bộ file để dữ liệu đã xóa không còn sót trong page rỗng
        dst.execute("VACUUM")

        subjects = dst.execute("SELECT COUNT(*) FROM subjects").fetchone()[0]
        questions = dst.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
        flashcards = dst.execute("SELECT COUNT(*) FROM flashcards").fetchone()[0]
        exercises = dst.execute("SELECT COUNT(*) FROM exercises").fetchone()[0]
        left_settings = [r[0] for r in dst.execute("SELECT key FROM settings")]
    finally:
        dst.close()

    return {
        "path": DST,
        "bytes": os.path.getsize(DST),
        "subjects": subjects,
        "questions": questions,
        "flashcards": flashcards,
        "exercises": exercises,
        "left_settings": left_settings,
    }


def main():
    info = build_clean_seed()
    print(
        f"✔ Đã tạo {info['path']} ({info['bytes']:,} bytes)\n"
        f"  • {info['subjects']} môn học • {info['questions']} câu hỏi • "
        f"{info['flashcards']} flashcards • {info['exercises']} bài tập\n"
        f"  • Settings còn lại: {info['left_settings']}\n"
        f"  • Đã xóa dữ liệu cá nhân: {', '.join(PERSONAL_TABLES)}"
    )


if __name__ == "__main__":
    main()
