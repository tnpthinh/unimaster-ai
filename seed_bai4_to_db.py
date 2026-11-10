import sqlite3
import json

BASE_DB = "unimaster.db"
JSON_FILE = "trac_nghiem_bai4_lipid_nuoc_tieu_200_cau.json"

with open(JSON_FILE, "r", encoding="utf-8") as f:
    questions = json.load(f)

print(f"Loaded {len(questions)} questions from {JSON_FILE}")

conn = sqlite3.connect(BASE_DB)
c = conn.cursor()

# Get subject_id for HOASINH_CTUMP
c.execute("SELECT id FROM subjects WHERE code = 'HOASINH_CTUMP'")
row = c.fetchone()
if not row:
    print("Error: HOASINH_CTUMP subject not found!")
    exit(1)
subject_id = row[0]
print(f"Target subject_id: {subject_id}")

# Remove previously seeded Bai 4 questions if any
c.execute("DELETE FROM questions WHERE subject_id = ? AND topic_tag LIKE 'Bài 4%'", (subject_id,))
print(f"Removed {c.rowcount} old 'Bài 4' questions from database.")

# Insert the 200 high-yield questions
inserted_count = 0
for q in questions:
    c.execute("""
        INSERT INTO questions (
            subject_id, topic_id, question_text, option_a, option_b, option_c, option_d,
            correct_option, explanation, difficulty, code_snippet, q_type, image_url, topic_tag
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        subject_id,
        None,
        q["question_text"],
        q["option_a"],
        q["option_b"],
        q["option_c"],
        q["option_d"],
        q["correct_option"],
        q.get("explanation", ""),
        q.get("difficulty", "medium"),
        "",
        "mcq",
        "",
        q["topic_tag"]
    ))
    inserted_count += 1

conn.commit()

# Check total question count for subject
c.execute("SELECT COUNT(*) FROM questions WHERE subject_id = ?", (subject_id,))
total_count = c.fetchone()[0]

print(f"\nSuccessfully inserted {inserted_count} questions into unimaster.db!")
print(f"Total questions for HOASINH_CTUMP now: {total_count}")

# Check breakdown by topic_tag
c.execute("SELECT topic_tag, COUNT(*) FROM questions WHERE subject_id = ? GROUP BY topic_tag ORDER BY topic_tag", (subject_id,))
tags = c.fetchall()
print("\n--- TOPIC BREAKDOWN IN DB ---")
for t, count in tags:
    print(f"  {t}: {count} câu")

conn.close()
