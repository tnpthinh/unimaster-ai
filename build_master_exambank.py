"""
Master Script: Ingest ExamBank into UniMaster DB & Export ExamBank.json
Subjects:
- OOP (C#/C++/Java): 100 MCQs + 10 Practical Coding Exercises
- NNLT 1 (C/C++): 10 Practical Coding Exercises
- Discrete Math & Algorithms: 60 MCQs + 5 Essay Prompts
- AVCB 3: 200 MCQs & Vocabulary Flashcards
"""

import sqlite3
import json
import os
import sys

from seed_oop_100_questions import get_oop_100_questions
from seed_avcb3_200_questions import get_avcb3_200_questions
from seed_algo_discrete_60_questions import get_algo_discrete_60_questions
from seed_20_coding_exercises import EXERCISES
from seed_5_essay_prompts import ESSAY_PROMPTS

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "unimaster.db")
EXAM_BANK_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ExamBank.json")

def build_exambank():
    print(f"Connecting to database: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # 1. Upgrade schema
    c.execute("PRAGMA table_info(subjects)")
    cols = [r[1] for r in c.fetchall()]
    if "exam_date" not in cols:
        try:
            c.execute("ALTER TABLE subjects ADD COLUMN exam_date TEXT DEFAULT ''")
        except Exception:
            pass

    c.execute("PRAGMA table_info(exercises)")
    ex_cols = [r[1] for r in c.fetchall()]
    if "test_cases_json" not in ex_cols:
        try:
            c.execute("ALTER TABLE exercises ADD COLUMN test_cases_json TEXT DEFAULT '[]'")
        except Exception:
            pass
    if "language" not in ex_cols:
        try:
            c.execute("ALTER TABLE exercises ADD COLUMN language TEXT DEFAULT 'cpp'")
        except Exception:
            pass
    if "solution_code" not in ex_cols:
        try:
            c.execute("ALTER TABLE exercises ADD COLUMN solution_code TEXT DEFAULT ''")
        except Exception:
            pass

    # Create essay_prompts table if not exists
    c.execute("""
    CREATE TABLE IF NOT EXISTS essay_prompts (
        id TEXT PRIMARY KEY,
        subject_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        topic TEXT NOT NULL,
        question_text TEXT NOT NULL,
        rubric_json TEXT DEFAULT '{}',
        model_solution TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
    )
    """)
    conn.commit()

    # 2. Setup Subjects
    target_subjects = [
        {
            "code": "OOP_CSHARP",
            "name": "Lập trình Hướng đối tượng OOP (C# / C++ / Java)",
            "icon": "💻",
            "category": "CNTT",
            "description": "Ôn thi OOP Thực hành (15/11) & Trắc nghiệm + Thực hành (26/11)",
            "exam_date": "15/11 & 26/11"
        },
        {
            "code": "DISCRETE_MATH_ALGO",
            "name": "Giải thuật & Toán rời rạc (Tự luận)",
            "icon": "📐",
            "category": "CNTT",
            "description": "Ôn thi Tự luận Giải thuật & Toán rời rạc (27/11) - Chứng minh logic, đồ thị, Big-O",
            "exam_date": "27/11"
        },
        {
            "code": "NNLT1",
            "name": "Ngôn ngữ Lập trình 1 (C / C++)",
            "icon": "⚙️",
            "category": "CNTT",
            "description": "Ôn thi Thực hành NNLT 1 (01/12) - Thao tác mảng, chuỗi, con trỏ, struct",
            "exam_date": "01/12"
        },
        {
            "code": "AVCB3",
            "name": "Anh văn cơ bản 3 (AVCB 3 - B1/B2)",
            "icon": "🌐",
            "category": "Ngoại ngữ",
            "description": "Ôn thi Trắc nghiệm Anh văn cơ bản 3 (04/12) - 200 câu ngữ pháp & từ vựng học thuật",
            "exam_date": "04/12"
        }
    ]

    subject_ids = {}
    for s in target_subjects:
        c.execute("SELECT id FROM subjects WHERE code = ?", (s["code"],))
        row = c.fetchone()
        if row:
            sid = row[0]
            c.execute("UPDATE subjects SET name = ?, icon = ?, category = ?, description = ?, exam_date = ? WHERE id = ?",
                      (s["name"], s["icon"], s["category"], s["description"], s["exam_date"], sid))
            subject_ids[s["code"]] = sid
        else:
            c.execute("INSERT INTO subjects (code, name, icon, category, description, exam_date) VALUES (?, ?, ?, ?, ?, ?)",
                      (s["code"], s["name"], s["icon"], s["category"], s["description"], s["exam_date"]))
            subject_ids[s["code"]] = c.lastrowid
    conn.commit()
    print("Subjects configured:", subject_ids)

    # 3. Insert Questions & Flashcards
    # A. OOP Questions (100)
    oop_qs = get_oop_100_questions()
    sid_oop = subject_ids["OOP_CSHARP"]
    # Clean previous generated questions for OOP to avoid duplicates
    c.execute("DELETE FROM questions WHERE subject_id = ? AND topic_tag IN ('Encapsulation', 'Inheritance', 'Polymorphism', 'Abstraction', 'Constructor', 'Destructor', 'Memory', 'Overloading', 'Overriding', 'C++ Specific', 'Java Specific', 'C# Specific', 'Design Patterns', 'Tracing', 'SOLID', 'Design')", (sid_oop,))
    
    for q in oop_qs:
        c.execute("""
        INSERT INTO questions (subject_id, q_type, question_text, code_snippet, option_a, option_b, option_c, option_d, correct_option, explanation, difficulty, topic_tag)
        VALUES (?, 'mcq', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (sid_oop, q["question_text"], q["code_snippet"], q["option_a"], q["option_b"], q["option_c"], q["option_d"], q["correct_option"], q["explanation"], q["difficulty"], q["topic_tag"]))
    
    # Add Flashcards for OOP
    c.execute("DELETE FROM flashcards WHERE subject_id = ?", (sid_oop,))
    for q in oop_qs[:20]:
        c.execute("""
        INSERT INTO flashcards (subject_id, front, back, hint)
        VALUES (?, ?, ?, ?)
        """, (sid_oop, q["question_text"][:200], f"Đáp án: {q['correct_option']}. {q['explanation']}", q["topic_tag"]))

    # B. AVCB 3 Questions (200)
    avcb_qs = get_avcb3_200_questions()
    sid_avcb = subject_ids["AVCB3"]
    c.execute("DELETE FROM questions WHERE subject_id = ?", (sid_avcb,))
    for q in avcb_qs:
        c.execute("""
        INSERT INTO questions (subject_id, q_type, question_text, code_snippet, option_a, option_b, option_c, option_d, correct_option, explanation, difficulty, topic_tag)
        VALUES (?, 'mcq', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (sid_avcb, q["question_text"], q["code_snippet"], q["option_a"], q["option_b"], q["option_c"], q["option_d"], q["correct_option"], q["explanation"], q["difficulty"], q["topic_tag"]))

    c.execute("DELETE FROM flashcards WHERE subject_id = ?", (sid_avcb,))
    for q in avcb_qs[:30]:
        c.execute("""
        INSERT INTO flashcards (subject_id, front, back, hint)
        VALUES (?, ?, ?, ?)
        """, (sid_avcb, q["question_text"][:200], f"Đáp án: {q['correct_option']}. {q['explanation']}", q["topic_tag"]))

    # C. Discrete Math & Algo Questions (60)
    algo_qs = get_algo_discrete_60_questions()
    sid_algo = subject_ids["DISCRETE_MATH_ALGO"]
    c.execute("DELETE FROM questions WHERE subject_id = ?", (sid_algo,))
    for q in algo_qs:
        c.execute("""
        INSERT INTO questions (subject_id, q_type, question_text, code_snippet, option_a, option_b, option_c, option_d, correct_option, explanation, difficulty, topic_tag)
        VALUES (?, 'mcq', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (sid_algo, q["question_text"], q["code_snippet"], q["option_a"], q["option_b"], q["option_c"], q["option_d"], q["correct_option"], q["explanation"], q["difficulty"], q["topic_tag"]))

    c.execute("DELETE FROM flashcards WHERE subject_id = ?", (sid_algo,))
    for q in algo_qs[:15]:
        c.execute("""
        INSERT INTO flashcards (subject_id, front, back, hint)
        VALUES (?, ?, ?, ?)
        """, (sid_algo, q["question_text"][:200], f"Đáp án: {q['correct_option']}. {q['explanation']}", q["topic_tag"]))

    # 4. Insert Practical Coding Exercises (20)
    c.execute("DELETE FROM exercises WHERE subject_id IN (?, ?)", (subject_ids["OOP_CSHARP"], subject_ids["NNLT1"]))
    for ex in EXERCISES:
        target_sid = subject_ids[ex["subject_code"]]
        c.execute("""
        INSERT INTO exercises (subject_id, title, problem, specs_json, sample_code, difficulty, test_cases_json, language, solution_code)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            target_sid,
            ex["title"],
            ex["problem"],
            json.dumps(ex["specs"], ensure_ascii=False),
            ex["sample_code"],
            ex["difficulty"],
            json.dumps(ex["test_cases"], ensure_ascii=False),
            ex["language"],
            ex["solution_code"]
        ))

    # 5. Insert Essay Prompts (5)
    c.execute("DELETE FROM essay_prompts")
    for ep in ESSAY_PROMPTS:
        target_sid = subject_ids[ep["subject_code"]]
        c.execute("""
        INSERT INTO essay_prompts (id, subject_id, title, topic, question_text, rubric_json, model_solution)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            ep["id"],
            target_sid,
            ep["title"],
            ep["topic"],
            ep["question_text"],
            json.dumps(ep["rubric"], ensure_ascii=False),
            ep["model_solution"]
        ))

    conn.commit()

    # 6. Export everything to ExamBank.json
    export_payload = {
        "version": "1.0",
        "description": "Comprehensive Exam Bank for UniMaster AI - Nov/Dec 2026 Exams",
        "subjects": target_subjects,
        "questions_count": {
            "OOP_CSHARP": len(oop_qs),
            "AVCB3": len(avcb_qs),
            "DISCRETE_MATH_ALGO": len(algo_qs)
        },
        "exercises_count": len(EXERCISES),
        "essay_prompts_count": len(ESSAY_PROMPTS),
        "oop_questions": oop_qs,
        "avcb3_questions": avcb_qs,
        "algo_discrete_questions": algo_qs,
        "exercises": EXERCISES,
        "essay_prompts": ESSAY_PROMPTS
    }

    with open(EXAM_BANK_JSON, "w", encoding="utf-8") as f:
        json.dump(export_payload, f, ensure_ascii=False, indent=2)

    print(f"Successfully generated {EXAM_BANK_JSON} ({os.path.getsize(EXAM_BANK_JSON)} bytes)")

    # Print summary counts in DB
    c.execute("SELECT s.code, s.name, COUNT(q.id) FROM subjects s LEFT JOIN questions q ON s.id = q.subject_id GROUP BY s.id")
    for r in c.fetchall():
        print(f"Subject: {r[0]:<20} | Name: {r[1]:<45} | Total Questions: {r[2]}")

    c.execute("SELECT COUNT(*) FROM exercises")
    print("Total Practical Exercises in DB:", c.fetchone()[0])
    c.execute("SELECT COUNT(*) FROM essay_prompts")
    print("Total Essay Prompts in DB:", c.fetchone()[0])

    conn.close()

if __name__ == "__main__":
    build_exambank()
