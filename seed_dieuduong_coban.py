"""
Khởi tạo tự động Ngân hàng đề Điều Dưỡng Cơ Bản (10 Bài - 600 Câu chuẩn giáo trình)
- 10 bài x 60 câu/bài = 600 câu trắc nghiệm bám sát 100% nội dung sách giáo khoa (không hỏi ngoài bài, đáp án chống lộ).
- Tự động nạp idempotent khi khởi động server trên cả Local PC và Render Cloud.
"""
import json
import os
import database as db

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SEED_JSON_PATH = os.path.join(BASE_DIR, "seed", "dieuduong_coban_600.json")

SUBJECT_CODE = "DIEUDUONG_CB"
SUBJECT_NAME = "Điều Dưỡng Cơ Bản (10 Bài - 600 Câu)"
SUBJECT_ICON = "🩺"
SUBJECT_CATEGORY = "Y Dược & Lâm sàng"
SUBJECT_DESC = (
    "Trọn bộ 600 câu hỏi trắc nghiệm Điều Dưỡng Cơ Bản bám sát 100% nội dung giáo trình "
    "(10 bài × 60 câu/bài: Bài 7, 8, 9, 12, 14, 15, 19, 21, 23, 27 — đáp án nhiễu cao, không hỏi ngoài bài)."
)


def ensure_dieuduong_coban_seeded(force_replace: bool = False) -> dict:
    if not os.path.exists(SEED_JSON_PATH):
        return {"seeded": False, "reason": "seed json missing"}

    with open(SEED_JSON_PATH, "r", encoding="utf-8") as f:
        questions = json.load(f)

    if not isinstance(questions, list) or not questions:
        return {"seeded": False, "reason": "empty seed json"}

    conn = db.get_connection()
    try:
        cur = conn.cursor()
        row = cur.execute("SELECT id FROM subjects WHERE code = ?", (SUBJECT_CODE,)).fetchone()
        if row:
            sid = row[0]
            cur.execute(
                "UPDATE subjects SET name = ?, icon = ?, category = ?, description = ? WHERE id = ?",
                (SUBJECT_NAME, SUBJECT_ICON, SUBJECT_CATEGORY, SUBJECT_DESC, sid),
            )
        else:
            cur.execute(
                "INSERT INTO subjects (code, name, icon, category, description) VALUES (?, ?, ?, ?, ?)",
                (SUBJECT_CODE, SUBJECT_NAME, SUBJECT_ICON, SUBJECT_CATEGORY, SUBJECT_DESC),
            )
            sid = cur.lastrowid

        existing_cnt = cur.execute(
            "SELECT COUNT(*) FROM questions WHERE subject_id = ?", (sid,)
        ).fetchone()[0]

        if force_replace or existing_cnt < len(questions):
            cur.execute("DELETE FROM questions WHERE subject_id = ?", (sid,))
            for q in questions:
                cur.execute(
                    """
                    INSERT INTO questions (
                        subject_id, question_text, code_snippet, image_url, q_type,
                        option_a, option_b, option_c, option_d,
                        correct_option, explanation, difficulty, topic_tag
                    ) VALUES (?, ?, '', '', 'mcq', ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        sid,
                        str(q.get("question_text", "")).strip(),
                        str(q.get("option_a", "")).strip(),
                        str(q.get("option_b", "")).strip(),
                        str(q.get("option_c", "")).strip(),
                        str(q.get("option_d", "")).strip(),
                        str(q.get("correct_option", "A")).strip().upper(),
                        str(q.get("explanation", "")).strip(),
                        str(q.get("difficulty", "medium")).strip().lower(),
                        str(q.get("topic_tag", "")).strip(),
                    ),
                )
            conn.commit()
            return {"seeded": True, "subject_id": sid, "count": len(questions), "replaced": True}

        conn.commit()
        return {"seeded": True, "subject_id": sid, "count": existing_cnt, "replaced": False}
    finally:
        conn.close()


if __name__ == "__main__":
    print(ensure_dieuduong_coban_seeded(force_replace=True))
