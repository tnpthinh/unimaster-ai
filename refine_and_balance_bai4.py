import json
import random

# Load all 7 parts
all_questions = []
for p in range(1, 8):
    with open(f'bai4_part{p}_raw.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        all_questions.extend(data)

print(f"Total raw questions loaded: {len(all_questions)}")

# Enrich distractors if correct answer is the longest, so that correct answer is NOT the longest!
def balance_options_length(q):
    opts = {
        'A': q['option_a'],
        'B': q['option_b'],
        'C': q['option_c'],
        'D': q['option_d']
    }
    corr_key = q['correct_option']
    corr_len = len(opts[corr_key])
    
    # Check lengths
    other_lens = [len(opts[k]) for k in opts if k != corr_key]
    max_other = max(other_lens)
    
    # Enriching phrases for distractors
    enrich_bank = [
        " (do thay đổi tính thấm và chuyển hóa lipid mô ngoại vi)",
        " (theo cơ chế điều hòa sinh hóa ngược âm tính nội bào)",
        " (thường biểu hiện rõ nét ở giai đoạn tiến triển lâm sàng)",
        " (dẫn đến rối loạn bài tiết dịch sinh học và điện giải)",
        " (đòi hỏi phải chuẩn hóa lại điều kiện đo quang phổ kế)",
        " (liên quan trực tiếp đến hoạt tính của enzym xúc tác đặc hiệu)",
        " (gây cản trở đáng kể đến độ hấp thụ ánh sáng ở bước sóng đo)",
        " (phù hợp với các tiêu chuẩn chẩn đoán thực hành phòng thí nghiệm)"
    ]
    
    # If correct answer is strictly longer than all other options, enrich distractors
    if corr_len > max_other:
        # Pick 2 shortest distractors and enrich them
        sorted_keys = sorted([k for k in opts if k != corr_key], key=lambda k: len(opts[k]))
        for idx, k in enumerate(sorted_keys[:2]):
            phrase = enrich_bank[(q['id'] + idx * 3) % len(enrich_bank)]
            if not opts[k].endswith(')'):
                opts[k] = opts[k] + phrase
            else:
                opts[k] = opts[k] + " trong điều kiện thử nghiệm chuẩn"
                
    q['option_a'] = opts['A']
    q['option_b'] = opts['B']
    q['option_c'] = opts['C']
    q['option_d'] = opts['D']
    return q

for q in all_questions:
    balance_options_length(q)

# Target: exactly 50 A, 50 B, 50 C, 50 D (25% each)
target_letters = ['A'] * 50 + ['B'] * 50 + ['C'] * 50 + ['D'] * 50
random.seed(42)
random.shuffle(target_letters)

for i, q in enumerate(all_questions):
    target_l = target_letters[i]
    current_l = q['correct_option']
    if current_l != target_l:
        # Swap options
        curr_text = q[f'option_{current_l.lower()}']
        targ_text = q[f'option_{target_l.lower()}']
        q[f'option_{current_l.lower()}'] = targ_text
        q[f'option_{target_l.lower()}'] = curr_text
        q['correct_option'] = target_l

# Double check length statistics
longest_count = 0
shortest_count = 0
equal_count = 0

for q in all_questions:
    lens = {
        'A': len(q['option_a']),
        'B': len(q['option_b']),
        'C': len(q['option_c']),
        'D': len(q['option_d'])
    }
    c_len = lens[q['correct_option']]
    max_len = max(lens.values())
    min_len = min(lens.values())
    
    # If correct option is uniquely the longest
    if c_len == max_len and list(lens.values()).count(max_len) == 1:
        longest_count += 1
    elif c_len == min_len and list(lens.values()).count(min_len) == 1:
        shortest_count += 1
    else:
        equal_count += 1

letter_counts = {
    'A': sum(1 for q in all_questions if q['correct_option'] == 'A'),
    'B': sum(1 for q in all_questions if q['correct_option'] == 'B'),
    'C': sum(1 for q in all_questions if q['correct_option'] == 'C'),
    'D': sum(1 for q in all_questions if q['correct_option'] == 'D'),
}

print("\n--- STATISTICAL VALIDATION FOR BAI 4 (200 QUESTIONS) ---")
print(f"Total questions: {len(all_questions)}")
print(f"Correct answer distribution: {letter_counts}")
print(f"Correct answer is longest: {longest_count} ({longest_count / len(all_questions) * 100:.1f}%)")
print(f"Correct answer is shortest: {shortest_count} ({shortest_count / len(all_questions) * 100:.1f}%)")
print(f"Correct answer is average/tied: {equal_count} ({equal_count / len(all_questions) * 100:.1f}%)")
print(f"Rate NOT the longest: {(len(all_questions) - longest_count) / len(all_questions) * 100:.1f}%")

# Save combined 200 questions file
with open('trac_nghiem_bai4_lipid_nuoc_tieu_200_cau.json', 'w', encoding='utf-8') as f:
    json.dump(all_questions, f, ensure_ascii=False, indent=2)

# Save 7 sub-parts
parts_def = [
    (0, 30, 'bai4_phan1_cholesterol_30_cau.json'),
    (30, 60, 'bai4_phan2_triglycerid_30_cau.json'),
    (60, 90, 'bai4_phan3_hdl_ldl_friedewald_30_cau.json'),
    (90, 115, 'bai4_phan4_the_ceton_25_cau.json'),
    (115, 140, 'bai4_phan5_cybow3_25_cau.json'),
    (140, 170, 'bai4_phan6_may_10_thong_so_30_cau.json'),
    (170, 200, 'bai4_phan7_nguyen_ly_10_thong_so_30_cau.json'),
]

for start, end, filename in parts_def:
    sub = all_questions[start:end]
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(sub, f, ensure_ascii=False, indent=2)
    print(f"Saved {filename} with {len(sub)} questions.")
