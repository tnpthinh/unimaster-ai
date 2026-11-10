"""
Generate & Seed Comprehensive Exam Bank for UniMaster AI:
- OOP (C++, Java, C#) - 100 Multiple Choice Questions
- AVCB 3 (Anh van co ban 3 - B1/B2) - 200 Questions (Grammar, Vocab, Reading)
- Discrete Math & Algorithms - 60 Questions
- 20 Programming Practical Exercises (OOP & NNLT 1) with Unit Testcases
- 5 Essay Exam Prompts for Discrete Math & Algorithms
- Export to ExamBank.json & direct SQLite ingestion
"""

import sqlite3
import json
import os
import sys

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "unimaster.db")
EXAM_BANK_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ExamBank.json")

def upgrade_schema(conn):
    c = conn.cursor()
    # Check subjects columns
    c.execute("PRAGMA table_info(subjects)")
    cols = [r[1] for r in c.fetchall()]
    if "exam_date" not in cols:
        try:
            c.execute("ALTER TABLE subjects ADD COLUMN exam_date TEXT DEFAULT ''")
        except Exception:
            pass

    # Check exercises columns
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
    conn.commit()

print("Schema upgrade checked.")
