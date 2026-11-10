import sqlite3, json

conn = sqlite3.connect('unimaster.db')
c = conn.cursor()
c.execute("""
    SELECT id, question_text, topic_tag, image_url, option_a, option_b, option_c, option_d, correct_option
    FROM questions 
    WHERE subject_id = 10 
      AND (topic_tag NOT LIKE 'Bài 2%' AND topic_tag NOT LIKE 'Bài 3%' AND topic_tag NOT LIKE 'Bài 4%')
    ORDER BY id ASC
""")
rows = c.fetchall()
print(f"Total CTUMP core questions: {len(rows)}")

# Group by curriculum parts:
part1 = [] # An toàn PTN & Đo quang Beer-Lambert (Câu 1 - 27)
part2 = [] # Bệnh phẩm & Protein / Biuret (Câu 28 - 56)
part3 = [] # Chức năng Thận (Ure, Creatinin, Acid Uric) (Câu 57 - 130)
part4 = [] # Enzym học & Bilang Lipid máu (Câu 131 - 220)
part5 = [] # Nước tiểu 10 thông số & Cặn lắng kính hiển vi (Câu 221 - 312)

for i, r in enumerate(rows):
    idx = i + 1
    # Check by bank question number in question_text if available, else sequential
    # Question text often starts with "Câu X."
    import re
    m = re.match(r"^Câu\s+(\d+)", r[1])
    q_num = int(m.group(1)) if m else idx

    if q_num <= 27:
        part1.append(r[0])
    elif q_num <= 56:
        part2.append(r[0])
    elif q_num <= 130:
        part3.append(r[0])
    elif q_num <= 220:
        part4.append(r[0])
    else:
        part5.append(r[0])

print(f"Part 1 (An toàn PTN & Đo quang): {len(part1)} câu, ID range: {min(part1) if part1 else 0} - {max(part1) if part1 else 0}")
print(f"Part 2 (Bệnh phẩm & Protein Biuret): {len(part2)} câu, ID range: {min(part2) if part2 else 0} - {max(part2) if part2 else 0}")
print(f"Part 3 (Thận - Ure, Creatinin, Acid Uric): {len(part3)} câu, ID range: {min(part3) if part3 else 0} - {max(part3) if part3 else 0}")
print(f"Part 4 (Enzym & Lipid máu): {len(part4)} câu, ID range: {min(part4) if part4 else 0} - {max(part4) if part4 else 0}")
print(f"Part 5 (Nước tiểu & Soi cặn lắng): {len(part5)} câu, ID range: {min(part5) if part5 else 0} - {max(part5) if part5 else 0}")
