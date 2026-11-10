# -*- coding: utf-8 -*-
import sqlite3
import json
import os

BASE_DIR = r"C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai"
os.chdir(BASE_DIR)

with open("trac_nghiem_bai3_glucid_200_cau.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

db_path = "unimaster.db"
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Get subject_id for HOASINH_CTUMP
c.execute("SELECT id FROM subjects WHERE code = 'HOASINH_CTUMP'")
row = c.fetchone()
if not row:
    print("Subject HOASINH_CTUMP not found!")
    exit(1)
subject_id = row[0]

# Remove previously seeded Bai 3 questions if any
c.execute("DELETE FROM questions WHERE subject_id = ? AND topic_tag LIKE 'Bài 3%'", (subject_id,))
print(f"Removed {c.rowcount} old 'Bài 3' questions from database.")

# Also remove old 47 glucid questions to avoid duplicates/outdated versions
c.execute("DELETE FROM questions WHERE subject_id = ? AND topic_tag = 'Hóa sinh Glucid (Molish, Fehling, Benedict, Glucose)'", (subject_id,))
print(f"Removed {c.rowcount} legacy glucid questions to prevent outdated duplicates.")

# Insert the 200 high-yield, anti-biased questions
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
        q["explanation"],
        q.get("difficulty", "medium"),
        "",
        "mcq",
        "",
        q["topic_tag"]
    ))
    inserted_count += 1

conn.commit()

# Check total questions for subject 10
c.execute("SELECT COUNT(*) FROM questions WHERE subject_id = ?", (subject_id,))
total_q = c.fetchone()[0]

# Check topic tags breakdown
c.execute("SELECT topic_tag, COUNT(*) FROM questions WHERE subject_id = ? GROUP BY topic_tag ORDER BY topic_tag", (subject_id,))
tags = c.fetchall()

conn.close()

print(f"\nSuccessfully inserted {inserted_count} questions into unimaster.db!")
print(f"Total questions now in Subject {subject_id} (HOASINH_CTUMP): {total_q}")
print("\nTopic Breakdown:")
for tag, count in tags:
    print(f"  - {tag}: {count} câu")
