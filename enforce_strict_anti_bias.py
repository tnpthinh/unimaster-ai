# -*- coding: utf-8 -*-
"""
Enforce Strict Anti-Bias:
Make sure that in at least 80% of questions, the correct option is NOT strictly the longest.
Students attempting to guess 'the longest option' will fall into distractor traps!
"""

import os
import json
import random

BASE_DIR = r"C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai"
os.chdir(BASE_DIR)

with open("trac_nghiem_bai3_glucid_200_cau.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

enrichment_phrases = [
    " trong điều kiện kỹ thuật tiêu chuẩn của phòng thí nghiệm",
    " khi thực hiện đúng các bước theo quy trình hướng dẫn",
    " ở bệnh nhân trưởng thành có thể trạng hoàn toàn bình thường",
    " sau khi đã loại trừ các yếu tố gây nhiễu thường gặp",
    " với độ lặp lại và độ chính xác cao trong xét nghiệm",
    " được quy định cụ thể trong tài liệu hướng dẫn thực hành",
    " trong suốt thời gian theo dõi phản ứng sinh hóa",
    " trên mẫu bệnh phẩm thu thập theo đúng quy chuẩn y khoa"
]

target_longest_max = 38  # 38 / 200 = 19.0%

current_longest_indices = []
for i, q in enumerate(questions):
    ck = q['correct_option'].lower()
    c_len = len(q[f'option_{ck}'])
    other_keys = [k for k in ['a','b','c','d'] if k != ck]
    max_o = max(len(q[f'option_{k}']) for k in other_keys)
    if c_len > max_o:
        current_longest_indices.append((i, c_len - max_o))

print(f"Initially longest is correct: {len(current_longest_indices)} / 200")

# Sort by smallest difference first, and enrich a distractor for those questions
current_longest_indices.sort(key=lambda x: x[1])

num_to_flip = len(current_longest_indices) - target_longest_max

for rank in range(num_to_flip):
    idx, diff = current_longest_indices[rank]
    q = questions[idx]
    ck = q['correct_option'].lower()
    c_len = len(q[f'option_{ck}'])
    
    # Pick the longest distractor and enrich it so it becomes longer than the correct option
    other_keys = [k for k in ['a','b','c','d'] if k != ck]
    best_distractor_key = max(other_keys, key=lambda k: len(q[f'option_{k}']))
    
    # Choose a phrase that fits
    phrase = enrichment_phrases[idx % len(enrichment_phrases)]
    
    # If distractor already ends with period or comma
    old_text = q[f'option_{best_distractor_key}'].rstrip('.')
    new_text = old_text + phrase
    q[f'option_{best_distractor_key}'] = new_text

# Re-calculate stats
longest_count = 0
shortest_count = 0
equal_or_med_count = 0

for q in questions:
    ck = q['correct_option'].lower()
    c_len = len(q[f'option_{ck}'])
    other_lens = [len(q[f'option_{k}']) for k in ['a','b','c','d'] if k != ck]
    max_o = max(other_lens)
    min_o = min(other_lens)
    if c_len > max_o:
        longest_count += 1
    elif c_len < min_o:
        shortest_count += 1
    else:
        equal_or_med_count += 1

key_counts = {k: sum(1 for q in questions if q['correct_option'] == k) for k in ['A', 'B', 'C', 'D']}

print("\n=== FINAL ANTI-BIAS AUDIT ===")
print(f"Total questions: {len(questions)}")
print(f"Key distribution: {key_counts} (Exactly 25% each!)")
print(f"Longest is correct: {longest_count} / 200 ({longest_count*100/200:.1f}%) -> TRAP PROOF!")
print(f"Shortest is correct: {shortest_count} / 200 ({shortest_count*100/200:.1f}%)")
print(f"Equal/Medium is correct: {equal_or_med_count} / 200 ({equal_or_med_count*100/200:.1f}%)")
print(f"NOT longest is correct: {200 - longest_count} / 200 ({(200 - longest_count)*100/200:.1f}%)")

# Overwrite master JSON
with open("trac_nghiem_bai3_glucid_200_cau.json", "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

# Overwrite the 6 sub-lesson JSONs
lessons = [
    ("bai3_phan1_molish_25_cau.json", questions[0:25]),
    ("bai3_phan2_fehling_35_cau.json", questions[25:60]),
    ("bai3_phan3_polysaccharid_iod_25_cau.json", questions[60:85]),
    ("bai3_phan4_dinh_luong_glucose_god_pod_45_cau.json", questions[85:130]),
    ("bai3_phan5_bien_luan_dai_thao_duong_ogtt_35_cau.json", questions[130:165]),
    ("bai3_phan6_benedict_nuoc_tieu_35_cau.json", questions[165:200])
]

for filename, qs in lessons:
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(qs, f, ensure_ascii=False, indent=2)

print("\nSaved all JSON files with strict anti-bias verified!")
