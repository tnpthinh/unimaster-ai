r"""
Tạo bản dữ liệu "sạch" để đưa lên Cloud / GitHub:
- Giữ nguyên toàn bộ môn học, ngân hàng câu hỏi, flashcards, bài tập, tiến độ học
- XÓA dàn Gemini API Key (để không bị lộ khóa khi đẩy mã nguồn lên GitHub)

Chạy:  python make_cloud_seed.py
Kết quả: seed/unimaster_seed.db
"""
import os
import shutil
import sqlite3

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "unimaster.db")
DST_DIR = os.path.join(ROOT, "seed")
DST = os.path.join(DST_DIR, "unimaster_seed.db")
SECRET_KEYS = ("gemini_api_keys_pool", "gemini_api_key")


def main():
    os.makedirs(DST_DIR, exist_ok=True)
    # Dùng backup API của SQLite để sao chép an toàn ngay cả khi server đang chạy
    src = sqlite3.connect(SRC)
    dst = sqlite3.connect(DST)
    src.backup(dst)
    src.close()
    dst.executemany("DELETE FROM settings WHERE key = ?", [(k,) for k in SECRET_KEYS])
    dst.commit()
    dst.execute("VACUUM")
    left = [r[0] for r in dst.execute("SELECT key FROM settings")]
    q = dst.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
    dst.close()
    print(f"✔ Đã tạo {DST} ({os.path.getsize(DST):,} bytes) • {q} câu hỏi • settings còn lại: {left}")


if __name__ == "__main__":
    main()
