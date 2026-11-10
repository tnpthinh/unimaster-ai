with open('database.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if 'c.execute("SELECT * FROM exam_results ORDER BY created_at DESC LIMIT 10")' in line:
        new_lines.append('    c.execute("SELECT id, subject_id, total_questions, correct_answers, score, time_spent_seconds, created_at, exam_type, user_id FROM exam_results ORDER BY created_at DESC LIMIT 15")\n')
    else:
        new_lines.append(line)

content = "".join(new_lines)
if "def get_exam_result(" not in content:
    func = """
def get_exam_result(exam_id: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM exam_results WHERE id = ?", (exam_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None
"""
    content = content.replace("def get_stats():", func + "\ndef get_stats():")

with open('database.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated database.py cleanly!")
