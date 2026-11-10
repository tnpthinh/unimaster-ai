# -*- coding: utf-8 -*-
import os
import sys
import json
import random
import sqlite3
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from make_part1 import QUESTIONS_PART1
from make_part2 import QUESTIONS_PART2
from make_part3 import QUESTIONS_PART3
from make_part4 import QUESTIONS_PART4
from make_part5 import QUESTIONS_PART5

all_raw = QUESTIONS_PART1 + QUESTIONS_PART2 + QUESTIONS_PART3 + QUESTIONS_PART4 + QUESTIONS_PART5
print(f"Total raw questions: {len(all_raw)}")
assert len(all_raw) == 200, f"Expected 200 questions, got {len(all_raw)}"

# Shuffle the options for each question so correct answer is balanced across A, B, C, D
random.seed(42)  # reproducible balance

processed_questions = []
for idx, item in enumerate(all_raw, 1):
    q_text = f"Câu {idx}: {item['q']}"
    orig_options = [item['a'], item['b'], item['c'], item['d']]
    # The correct answer in the source is item['a']
    correct_content = orig_options[0]

    # Create a shuffled list of options
    shuffled_options = orig_options.copy()
    random.shuffle(shuffled_options)

    # Determine which letter holds the correct content
    corr_idx = shuffled_options.index(correct_content)
    corr_letter = ['A', 'B', 'C', 'D'][corr_idx]

    processed_questions.append({
        "id_in_set": idx,
        "question_text": q_text,
        "option_a": shuffled_options[0],
        "option_b": shuffled_options[1],
        "option_c": shuffled_options[2],
        "option_d": shuffled_options[3],
        "correct_option": corr_letter,
        "explanation": item["exp"],
        "difficulty": item["diff"],
        "topic_tag": item["tag"],
        "q_type": "mcq"
    })

# Save JSON file
out_json_path = os.path.join(ROOT, "trac_nghiem_bai2_protid_200_cau.json")
with open(out_json_path, "w", encoding="utf-8") as f:
    json.dump(processed_questions, f, ensure_ascii=False, indent=2)
print(f"Saved 200 questions to {out_json_path}")

# Check answer distribution
counts = {"A": 0, "B": 0, "C": 0, "D": 0}
for q in processed_questions:
    counts[q["correct_option"]] += 1
print(f"Answer distribution: {counts}")

# Insert into unimaster.db
db_path = os.path.join(ROOT, "unimaster.db")
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Get subject_id for HOASINH_CTUMP
c.execute("SELECT id FROM subjects WHERE code = 'HOASINH_CTUMP'")
row = c.fetchone()
if not row:
    c.execute("INSERT INTO subjects (code, name, icon, category, description) VALUES (?, ?, ?, ?, ?)",
              ('HOASINH_CTUMP', 'Thực Hành Hóa Sinh Y Khoa (CTUMP)', '🔬', 'Y Dược & Khoa học sức khỏe', 'Bộ môn Hóa sinh - Trường Đại học Y Dược Cần Thơ'))
    sid = c.lastrowid
else:
    sid = row[0]

# Check existing questions for this topic tag
c.execute("DELETE FROM questions WHERE subject_id = ? AND topic_tag = 'Bài 2: Chuyển hóa Protid & Chức năng thận'", (sid,))
print(f"Cleaned previous entries with tag 'Bài 2: Chuyển hóa Protid & Chức năng thận'")

for q in processed_questions:
    c.execute("""
        INSERT INTO questions (subject_id, question_text, option_a, option_b, option_c, option_d, correct_option, explanation, difficulty, q_type, code_snippet, image_url, topic_tag)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, '', '', ?)
    """, (
        sid,
        q["question_text"],
        q["option_a"],
        q["option_b"],
        q["option_c"],
        q["option_d"],
        q["correct_option"],
        q["explanation"],
        q["difficulty"],
        q["q_type"],
        q["topic_tag"]
    ))

conn.commit()

# Total questions now in HOASINH_CTUMP
c.execute("SELECT COUNT(*) FROM questions WHERE subject_id = ?", (sid,))
total_hoasinh = c.fetchone()[0]
c.execute("SELECT COUNT(*) FROM questions")
total_all = c.fetchone()[0]
conn.close()

print(f"Successfully seeded into unimaster.db! Total in HOASINH_CTUMP: {total_hoasinh}, Total across all subjects: {total_all}")

# Backup to seed
seed_path = os.path.join(ROOT, "seed", "unimaster_seed.db")
shutil.copy2(db_path, seed_path)
print(f"Updated {seed_path}")

# Re-generate standalone HTML file so it contains all newly seeded questions
import server
html_standalone = server.generate_standalone_html_string()
with open(os.path.join(ROOT, "UniMaster_Chay_Moi_Noi_Khong_Can_PC.html"), "w", encoding="utf-8") as f:
    f.write(html_standalone)

with open(os.path.join(ROOT, "cloud_deploy_netlify", "index.html"), "w", encoding="utf-8") as f:
    f.write(html_standalone)

print(f"Re-exported standalone HTML files! Size: {len(html_standalone.encode('utf-8'))} bytes.")
