# -*- coding: utf-8 -*-
"""
import_100_csharp_oop.py
Kiểm tra nghiêm ngặt 100 câu C# OOP và nạp vào:
1. unimaster.db (subject_id = 5)
2. ExamBank.json (oop_questions)
3. Chạy make_cloud_seed.py
4. Chạy generate_standalone.py
"""
import os
import sys
import sqlite3
import json
import subprocess

# Nạp Part 1
import build_complete_100_questions
questions_part1 = build_complete_100_questions.questions_part1
print(f"Loaded Part 1: {len(questions_part1)} questions.")

# Nạp Part 2
sys.path.insert(0, r"C:\Users\PC\Desktop")
import generate_part2_fixed
questions_part2 = generate_part2_fixed.questions_part2
print(f"Loaded Part 2: {len(questions_part2)} questions.")

all_100_questions = questions_part1 + questions_part2
assert len(all_100_questions) == 100, f"Expected 100 questions, got {len(all_100_questions)}"

print("\n=== KIỂM TRA RÀNG BUỘC CỦA TOÀN BỘ 100 CÂU HỎI ===")
forbidden_phrases = ["theo như tài liệu", "theo tài liệu"]
distribution = {"A": 0, "B": 0, "C": 0, "D": 0}

for idx, q in enumerate(all_100_questions, start=1):
    corr = q["corr"].strip().upper()
    assert corr in ["A", "B", "C", "D"], f"Câu {idx}: đáp án đúng {corr} không hợp lệ!"
    distribution[corr] += 1
    
    corr_txt = q[corr].strip()
    distractor_lens = [len(q[opt].strip()) for opt in ["A", "B", "C", "D"] if opt != corr]
    max_distractor_len = max(distractor_lens)
    
    # Ràng buộc: Đáp án đúng KHÔNG ĐƯỢC dài hơn các đáp án khác (len(corr) <= max(distractor_lens))
    if len(corr_txt) > max_distractor_len:
        raise ValueError(
            f"LỖI ĐỘ DÀI tại câu {idx}: Đáp án đúng {corr} dài {len(corr_txt)} ký tự > đáp án nhiễu dài nhất ({max_distractor_len} ký tự)!\n"
            f"Nội dung: {corr_txt}"
        )
    
    # Ràng buộc: Không chứa cụm từ 'theo như tài liệu' hoặc 'theo tài liệu'
    full_text = f"{q['q']} {q['A']} {q['B']} {q['C']} {q['D']} {q['exp']}".lower()
    for phrase in forbidden_phrases:
        if phrase in full_text:
            raise ValueError(f"LỖI TỪ CẤM tại câu {idx}: chứa cụm từ '{phrase}'")

print("TẤT CẢ 100 CÂU ĐÃ THỎA MÃN 100% CÁC RÀNG BUỘC:")
print("1. len(đáp án đúng) <= max(đáp án sai) trên từng câu hỏi.")
print("2. Tuyệt đối không chứa 'theo như tài liệu' hay 'theo tài liệu'.")
print("3. Phân bổ đáp án:", distribution)

# Nạp vào database unimaster.db
db_path = "unimaster.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Kiểm tra số lượng trước khi thêm
cur.execute("SELECT COUNT(*) FROM questions WHERE subject_id = 5")
count_before = cur.fetchone()[0]
print(f"\nSố lượng câu hỏi môn 5 trước khi nạp: {count_before}")

# Kiểm tra các câu đã tồn tại chưa để tránh trùng lặp
cur.execute("SELECT question_text FROM questions WHERE subject_id = 5")
existing_q_texts = set(row[0].strip() for row in cur.fetchall())

inserted_db = 0
for q in all_100_questions:
    q_text = q["q"].strip()
    if q_text in existing_q_texts:
        continue
    
    cur.execute("""
        INSERT INTO questions (
            subject_id, topic_id, question_text,
            option_a, option_b, option_c, option_d,
            correct_option, explanation, difficulty,
            code_snippet, q_type, image_url, topic_tag
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        5, None, q_text,
        q["A"].strip(), q["B"].strip(), q["C"].strip(), q["D"].strip(),
        q["corr"].strip().upper(), q["exp"].strip(), q.get("diff", "medium"),
        "", "multiple_choice", None, q.get("tag", "C# OOP")
    ))
    inserted_db += 1

conn.commit()
cur.execute("SELECT COUNT(*) FROM questions WHERE subject_id = 5")
count_after = cur.fetchone()[0]
print(f"Đã nạp vào unimaster.db: {inserted_db} câu mới. Tổng số câu môn 5 hiện tại: {count_after}")
conn.close()

# Cập nhật ExamBank.json
exambank_path = "ExamBank.json"
if os.path.exists(exambank_path):
    with open(exambank_path, "r", encoding="utf-8") as f:
        bank_data = json.load(f)
    
    existing_bank_q = bank_data.get("oop_questions", [])
    bank_q_texts = set(x.get("question_text", "").strip() for x in existing_bank_q)
    
    added_bank = 0
    for q in all_100_questions:
        q_text = q["q"].strip()
        if q_text in bank_q_texts:
            continue
        existing_bank_q.append({
            "question_text": q_text,
            "code_snippet": "",
            "option_a": q["A"].strip(),
            "option_b": q["B"].strip(),
            "option_c": q["C"].strip(),
            "option_d": q["D"].strip(),
            "correct_option": q["corr"].strip().upper(),
            "explanation": q["exp"].strip(),
            "difficulty": q.get("diff", "medium"),
            "topic_tag": q.get("tag", "C# OOP")
        })
        added_bank += 1
    
    bank_data["oop_questions"] = existing_bank_q
    bank_data["questions_count"] = len(existing_bank_q)
    with open(exambank_path, "w", encoding="utf-8") as f:
        json.dump(bank_data, f, ensure_ascii=False, indent=2)
    print(f"Đã cập nhật ExamBank.json: thêm {added_bank} câu. Tổng câu OOP trong ExamBank: {len(existing_bank_q)}")

# Chạy make_cloud_seed.py
print("\nĐang tạo seed db cho Cloud / GitHub (make_cloud_seed.py)...")
sub_seed = subprocess.run([sys.executable, "make_cloud_seed.py"], capture_output=True, text=True, encoding="utf-8")
print(sub_seed.stdout)

# Chạy generate_standalone.py
print("\nĐang sinh file HTML chạy offline (generate_standalone.py)...")
sub_html = subprocess.run([sys.executable, "generate_standalone.py"], capture_output=True, text=True, encoding="utf-8")
print(sub_html.stdout)

print("\n=== HOÀN TẤT NHIỆM VỤ NẠP 100 CÂU C# OOP THÀNH CÔNG ===")
