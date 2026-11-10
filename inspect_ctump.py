import sqlite3

conn = sqlite3.connect('unimaster.db')
c = conn.cursor()
c.execute("""
    SELECT id, question_text, topic_tag, image_url 
    FROM questions 
    WHERE subject_id = 10 
      AND (topic_tag NOT LIKE 'Bài 2%' AND topic_tag NOT LIKE 'Bài 3%' AND topic_tag NOT LIKE 'Bài 4%')
    ORDER BY id ASC
""")
rows = c.fetchall()
print('Original CTUMP questions count:', len(rows))
topics = {}
for r in rows:
    tag = r[2] or 'Khác'
    topics[tag] = topics.get(tag, 0) + 1
for t, cnt in topics.items():
    print(f'  - {t}: {cnt} câu')

if rows:
    print('First question:', rows[0][0], rows[0][1][:60])
    print('Last question:', rows[-1][0], rows[-1][1][:60])
