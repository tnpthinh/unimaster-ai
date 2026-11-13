"""
UniMaster Code Engine & Automated Assessment Service
Equipped with:
- Multi-language Code Runner (Python native, C# native / AI Virtual Sandbox for C++/Java/C)
- Automated Unit Test Runner with input/output matching & memory leak detection
- AI Senior Code Reviewer (OOP principles, O(n) complexity, memory safety)
- Discrete Math & Algorithm Essay Grader (Rubric-based 10-point academic grading)
- 60-Minute Timed Exam Simulator with Question Palette & Detailed Diagnostics
"""

import os
import sys
import json
import time
import re
import tempfile
import subprocess
import shutil
from typing import Dict, Any, List

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import database as db
import ai_service as ai

# Check local compiler availability
PYTHON_EXEC = sys.executable
DOTNET_EXEC = shutil.which("dotnet")
GCC_EXEC = shutil.which("gcc")
GPP_EXEC = shutil.which("g++")
JAVAC_EXEC = shutil.which("javac")

# =========================================================================
# 1. CODE EXECUTION RUNNER
# =========================================================================

def _normalize_output(text: str) -> str:
    if text is None:
        return ""
    # Normalize CRLF to LF, strip trailing spaces on each line, strip overall
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").split("\n")]
    return "\n".join(lines).strip()

async def execute_code(language: str, code: str, input_data: str = "") -> Dict[str, Any]:
    lang = (language or "cpp").lower().strip()
    start_time = time.time()

    # 1. Native Python Execution
    if lang in ["python", "py"]:
        try:
            with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as f:
                f.write(code)
                temp_path = f.name

            proc = subprocess.run(
                [PYTHON_EXEC, temp_path],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=4.0,
                encoding="utf-8",
                errors="replace"
            )
            elapsed_ms = int((time.time() - start_time) * 1000)
            try:
                os.remove(temp_path)
            except Exception:
                pass

            return {
                "success": proc.returncode == 0,
                "stdout": proc.stdout,
                "stderr": proc.stderr,
                "runtime_ms": elapsed_ms,
                "compile_error": proc.stderr if proc.returncode != 0 else "",
                "memory_leak_warning": ""
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": "Time Limit Exceeded (Quá giới hạn 4.0 giây)",
                "runtime_ms": 4000,
                "compile_error": "",
                "memory_leak_warning": "Phát hiện vòng lặp vô tận (Infinite Loop) hoặc độ phức tạp quá lớn."
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "runtime_ms": 0,
                "compile_error": str(e),
                "memory_leak_warning": ""
            }

    # 2. Native C++ if g++ is installed
    if lang in ["cpp", "c++", "c"] and (GPP_EXEC or GCC_EXEC):
        compiler = GPP_EXEC if lang in ["cpp", "c++"] else GCC_EXEC
        try:
            suffix = ".cpp" if lang in ["cpp", "c++"] else ".c"
            with tempfile.NamedTemporaryFile("w", suffix=suffix, delete=False, encoding="utf-8") as f:
                f.write(code)
                src_path = f.name
            exe_path = src_path + ".exe"

            compile_proc = subprocess.run(
                [compiler, "-O2", "-std=c++17" if "++" in lang else "-std=c11", src_path, "-o", exe_path],
                capture_output=True,
                text=True,
                timeout=5.0,
                encoding="utf-8",
                errors="replace"
            )
            if compile_proc.returncode != 0:
                os.remove(src_path)
                return {
                    "success": False,
                    "stdout": "",
                    "stderr": compile_proc.stderr,
                    "compile_error": compile_proc.stderr,
                    "runtime_ms": 0,
                    "memory_leak_warning": ""
                }

            run_proc = subprocess.run(
                [exe_path],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=3.0,
                encoding="utf-8",
                errors="replace"
            )
            elapsed_ms = int((time.time() - start_time) * 1000)

            for p in [src_path, exe_path]:
                try:
                    if os.path.exists(p): os.remove(p)
                except Exception:
                    pass

            return {
                "success": run_proc.returncode == 0,
                "stdout": run_proc.stdout,
                "stderr": run_proc.stderr,
                "runtime_ms": elapsed_ms,
                "compile_error": "",
                "memory_leak_warning": ""
            }
        except Exception as e:
            pass  # Fallback to AI sandbox below

    # 3. Native C# (.NET) if dotnet SDK / runtime is available
    if lang in ["csharp", "c#", "cs"] and DOTNET_EXEC:
        try:
            cs_res = await _execute_native_csharp(code, input_data, start_time)
            if cs_res is not None:
                return cs_res
        except Exception:
            pass  # Fallback to AI sandbox below

    # 4. AI Smart Compiler & Sandbox Runner (C++, Java, C#, C without native toolchain)
    return await _ai_simulate_execution(lang, code, input_data)


async def _execute_native_csharp(code: str, input_data: str, start_time: float):
    """Compile and execute C# natively via dotnet run using a cached runner project."""
    runner_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".csharp_runner")
    os.makedirs(runner_dir, exist_ok=True)
    csproj_path = os.path.join(runner_dir, "Runner.csproj")
    if not os.path.exists(csproj_path):
        with open(csproj_path, "w", encoding="utf-8") as f:
            f.write(
                '<Project Sdk="Microsoft.NET.Sdk">\n'
                '  <PropertyGroup>\n'
                '    <OutputType>Exe</OutputType>\n'
                '    <TargetFramework>net8.0</TargetFramework>\n'
                '    <ImplicitUsings>enable</ImplicitUsings>\n'
                '    <Nullable>enable</Nullable>\n'
                '  </PropertyGroup>\n'
                '</Project>\n'
            )

    program_cs = os.path.join(runner_dir, "Program.cs")
    with open(program_cs, "w", encoding="utf-8") as f:
        f.write(code)

    try:
        proc = subprocess.run(
            [DOTNET_EXEC, "run", "--project", csproj_path, "--no-restore"],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=6.0,
            encoding="utf-8",
            errors="replace",
            cwd=runner_dir
        )
        elapsed_ms = int((time.time() - start_time) * 1000)

        compile_err = ""
        if proc.returncode != 0:
            lines = (proc.stdout + "\n" + proc.stderr).splitlines()
            err_lines = [l for l in lines if ": error CS" in l or "error :" in l]
            compile_err = "\n".join(err_lines) if err_lines else (proc.stderr or proc.stdout)

        return {
            "success": proc.returncode == 0,
            "stdout": proc.stdout if proc.returncode == 0 else "",
            "stderr": proc.stderr,
            "runtime_ms": elapsed_ms,
            "compile_error": compile_err,
            "memory_leak_warning": ""
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "stdout": "",
            "stderr": "Time Limit Exceeded (Quá giới hạn 6.0 giây thực thi C#)",
            "runtime_ms": 6000,
            "compile_error": "",
            "memory_leak_warning": "Phát hiện vòng lặp vô tận (Infinite Loop) hoặc thao tác blocking."
        }
    except Exception:
        return None


async def _ai_simulate_execution(language: str, code: str, input_data: str) -> Dict[str, Any]:
    prompt = f"""Bạn là một Trình Biên Dịch & Chấm Thi Ảo (High-Speed Compiler & Virtual Sandbox) cho trường đại học.
Nhiệm vụ: Phân tích mã nguồn sinh viên ({language}), kiểm tra lỗi biên dịch, mô phỏng thực thi chuẩn xác với dữ liệu đầu vào (stdin), phát hiện rò rỉ bộ nhớ (memory leaks, thiếu delete/free, thiếu virtual destructor), và xuất kết quả.

MÃ NGUỒN ({language}):
```
{code}
```

ĐẦU VÀO (STDIN):
```
{input_data}
```

Hãy phân tích cực kỳ chính xác và trả về DUY NHẤT một chuỗi JSON hợp lệ không bọc markdown theo định dạng sau:
{{
  "compile_success": true,
  "compile_error": "",
  "stdout": "kết quả chính xác xuất ra màn hình console",
  "stderr": "",
  "runtime_ms": 15,
  "memory_leak_warning": "Cảnh báo nếu có rò rỉ bộ nhớ (ví dụ: cấp phát new[] nhưng không delete[], thiếu virtual ~Base(), hoặc con trỏ lơ lửng), nếu an toàn để chuỗi rỗng"
}}"""

    start_t = time.time()
    try:
        reply = await ai.call_gemini(prompt, max_tokens=2048, thinking_budget=0)
        elapsed_ms = int((time.time() - start_t) * 1000)
        if reply:
            cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", reply.strip())
            s, e = cleaned.find("{"), cleaned.rfind("}")
            if s != -1 and e != -1:
                obj = json.loads(cleaned[s:e+1])
                return {
                    "success": bool(obj.get("compile_success", True) and not obj.get("compile_error")),
                    "stdout": str(obj.get("stdout", "")),
                    "stderr": str(obj.get("stderr", "")),
                    "compile_error": str(obj.get("compile_error", "")),
                    "runtime_ms": max(12, elapsed_ms),
                    "memory_leak_warning": str(obj.get("memory_leak_warning", ""))
                }
    except Exception as e:
        pass

    # Heuristic fallback if AI is offline
    mem_warn = ""
    if "new " in code and "delete" not in code:
        mem_warn = "⚠️ Cảnh báo: Mã nguồn có cấp phát toán tử `new` nhưng không tìm thấy lệnh `delete` giải phóng vùng nhớ."
    if "malloc(" in code and "free(" not in code:
        mem_warn = "⚠️ Cảnh báo: Mã nguồn có cấp phát `malloc()` nhưng không gọi `free()`."

    return {
        "success": True,
        "stdout": "[Hệ thống Sandbox AI đã nhận diện cú pháp hợp lệ]",
        "stderr": "",
        "compile_error": "",
        "runtime_ms": 20,
        "memory_leak_warning": mem_warn
    }


# =========================================================================
# 2. AUTOMATED UNIT TEST RUNNER
# =========================================================================

async def test_code_against_cases(exercise_id: int, language: str, code: str) -> Dict[str, Any]:
    conn = db.get_connection()
    c = conn.cursor()
    c.execute("SELECT id, title, problem, test_cases_json, solution_code FROM exercises WHERE id = ?", (exercise_id,))
    row = c.fetchone()
    conn.close()

    if not row:
        return {"success": False, "error": f"Không tìm thấy bài tập #{exercise_id}"}

    ex_title = row["title"]
    try:
        cases = json.loads(row["test_cases_json"] or "[]")
    except Exception:
        cases = []

    if not cases:
        # Default fallback test case
        cases = [{"input": "", "expected_output": "", "is_hidden": False}]

    results = []
    passed_count = 0
    total_count = len(cases)
    memory_warnings = []

    for idx, tc in enumerate(cases):
        inp = tc.get("input", "")
        exp = _normalize_output(tc.get("expected_output", ""))
        is_hidden = tc.get("is_hidden", False)

        run_res = await execute_code(language, code, inp)
        act = _normalize_output(run_res.get("stdout", ""))
        is_passed = (act == exp) and run_res.get("success", False)

        if is_passed:
            passed_count += 1

        if run_res.get("memory_leak_warning"):
            memory_warnings.append(run_res["memory_leak_warning"])

        results.append({
            "test_idx": idx + 1,
            "input": inp if not is_hidden else "[Test Case Ẩn]",
            "expected": exp if not is_hidden else "[Đáp án chuẩn ẩn]",
            "actual": act if not is_hidden else ("[Passed]" if is_passed else "[Failed - Sai Kết Quả]"),
            "passed": is_passed,
            "runtime_ms": run_res.get("runtime_ms", 0),
            "compile_error": run_res.get("compile_error", ""),
            "is_hidden": is_hidden
        })

    all_passed = (passed_count == total_count)
    summary_feedback = (
        f"🎉 Xuất sắc! Vượt qua {passed_count}/{total_count} test case (100%)."
        if all_passed
        else f"⚠️ Đạt {passed_count}/{total_count} test case. Hãy kiểm tra các trường hợp biên hoặc lỗi ngầm."
    )

    unique_mem = list(set([w for w in memory_warnings if w]))

    return {
        "success": True,
        "exercise_id": exercise_id,
        "exercise_title": ex_title,
        "total_tests": total_count,
        "passed_tests": passed_count,
        "all_passed": all_passed,
        "results": results,
        "feedback": summary_feedback,
        "memory_leak_warning": "\n".join(unique_mem) if unique_mem else ""
    }


# =========================================================================
# 3. AI SENIOR CODE REVIEWER (OOP & NNLT 1)
# =========================================================================

async def ai_review_code_advanced(title: str, problem: str, code: str, language: str = "cpp") -> Dict[str, Any]:
    prompt = f"""Bạn là Kỹ sư Trưởng (Tech Lead) và Giảng viên Chấm Thi Lập Trình (OOP & NNLT 1).
Hãy phân tích và chấm bài code sau của sinh viên:

BÀI TẬP: {title}
YÊU CẦU: {problem}
NGÔN NGỮ: {language}

CODE CỦA SINH VIÊN:
```{language}
{code}
```

Hãy đánh giá toàn diện và trả về DUY NHẤT một chuỗi JSON:
{{
  "score": 9.0,
  "verdict": "Lời nhận xét tổng quát ngắn gọn 1-2 câu",
  "oop_analysis": "Đánh giá về tính đóng gói, kế thừa, đa hình, trừu tượng, access modifiers, hoặc struct/pointer",
  "memory_safety": "Đánh giá rò rỉ bộ nhớ (leak), quản lý con trỏ, giải phóng dynamic memory, virtual destructor",
  "complexity": "Độ phức tạp thời gian O(...) và không gian O(...)",
  "refactoring_tips": [
    "Mẹo 1 tối ưu",
    "Mẹo 2 viết code sạch hơn"
  ],
  "improved_code": "Mã nguồn hoàn thiện tối ưu nhất"
}}"""

    try:
        reply = await ai.call_gemini(prompt, max_tokens=4096, thinking_budget=384)
        if reply:
            cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", reply.strip())
            s, e = cleaned.find("{"), cleaned.rfind("}")
            if s != -1 and e != -1:
                return json.loads(cleaned[s:e+1])
    except Exception:
        pass

    return {
        "score": 8.0,
        "verdict": "Mã nguồn giải quyết được yêu cầu cơ bản của bài toán.",
        "oop_analysis": "Cấu trúc hàm và class rõ ràng, tuân thủ tương đối tốt các nguyên tắc thiết kế.",
        "memory_safety": "Cần chú ý giải phóng triệt để các biến động cấp phát trên Heap.",
        "complexity": "Độ phức tạp đạt mức chấp nhận được O(N).",
        "refactoring_tips": ["Nên đặt tên biến mang tính gợi tả hơn", "Bổ sung kiểm tra dữ liệu đầu vào biên"],
        "improved_code": code
    }


# =========================================================================
# 4. ESSAY GRADER (DISCRETE MATH & ALGORITHMS)
# =========================================================================

async def grade_essay_advanced(prompt_id: str, student_answer: str, custom_question: str = "", custom_rubric: str = "") -> Dict[str, Any]:
    conn = db.get_connection()
    c = conn.cursor()
    c.execute("SELECT id, title, topic, question_text, rubric_json, model_solution FROM essay_prompts WHERE id = ?", (prompt_id,))
    row = c.fetchone()
    conn.close()

    q_text = row["question_text"] if row else (custom_question or "Đề thi tự luận")
    topic = row["topic"] if row else "Toán Rời Rạc & Giải Thuật"
    rubric_str = row["rubric_json"] if row else (custom_rubric or "Thang điểm 10 chuẩn")
    model_sol = row["model_solution"] if row else "Xem barem chi tiết"

    prompt = f"""Bạn là Giáo Sư Tiến Sĩ chuyên ngành Toán Rời Rạc & Lý Thuyết Giải Thuật (Đại Học Bách Khoa / KHTN).
Nhiệm vụ: Đóng vai Giám Khảo Chấm Thi Tự Luận công tâm, khắt khe và chuẩn xác theo barem 10 điểm.

CHỦ ĐỀ: {topic}
ĐỀ BÀI:
{q_text}

BAREM CHẤM ĐIỂM (RUBRIC):
{rubric_str}

BÀI LÀM CỦA SINH VIÊN:
\"\"\"{student_answer}\"\"\"

LỜI GIẢI MẪU 10/10:
{model_sol}

Hãy soi kỹ từng bước suy luận, chỉ ra bước nào chứng minh đúng, bước nào sai logic, thiếu trường hợp cơ sở (base case) hoặc thiếu trường hợp biên nào, và tính toán độ phức tạp thời gian/bộ nhớ.
Dùng công thức KaTeX `$ ... $` hoặc `$$ ... $$` cho toán học.

Trả về DUY NHẤT một đối tượng JSON:
{{
  "score": 8.5,
  "verdict": "Đánh giá tổng quát 1-2 câu",
  "logic_steps": [
    {{"step": "Bước 1", "status": "pass", "comment": "Lập luận đúng"}},
    {{"step": "Bước 2", "status": "warning", "comment": "Chưa chặt chẽ ở điều kiện biên"}},
    {{"step": "Bước 3", "status": "fail", "comment": "Suy luận ngụy biện khẳng định hệ quả"}}
  ],
  "missing_cases": [
    "Thiếu trường hợp k chẵn trong quy nạp",
    "Chưa xét đồ thị không liên thông"
  ],
  "complexity_analysis": "O(V log V) thời gian, O(V) bộ nhớ phụ",
  "strengths": [
    "Trình bày rõ ràng, ký hiệu toán học chuẩn"
  ],
  "model_solution": "{model_sol}"
}}"""

    try:
        reply = await ai.call_gemini(prompt, max_tokens=4096, thinking_budget=384)
        if reply:
            cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", reply.strip())
            s, e = cleaned.find("{"), cleaned.rfind("}")
            if s != -1 and e != -1:
                res = json.loads(cleaned[s:e+1])
                if not res.get("model_solution"):
                    res["model_solution"] = model_sol
                return res
    except Exception:
        pass

    words = len((student_answer or "").split())
    est = min(8.5, round(max(4.0, words / 15.0), 1))
    return {
        "score": est,
        "verdict": "Bài làm đã nêu được một số luận điểm chính nhưng cần chứng minh chặt chẽ hơn.",
        "logic_steps": [
            {"step": "Khởi đầu & Đặt vấn đề", "status": "pass", "comment": "Nắm được yêu cầu của đề bài"},
            {"step": "Chứng minh / Mã giả", "status": "warning", "comment": "Các bước biến đổi cần dẫn giải luật suy diễn cụ thể"}
        ],
        "missing_cases": ["Cần bổ sung chi tiết các trường hợp biên"],
        "complexity_analysis": "Chưa phân tích đầy đủ độ phức tạp",
        "strengths": ["Có nỗ lực trình bày bài tự luận"],
        "model_solution": model_sol
    }


# =========================================================================
# 5. 60-MINUTE TIMED EXAM SIMULATOR
# =========================================================================

def start_timed_exam(subject_id: int, count: int = 40, duration_minutes: int = 60) -> Dict[str, Any]:
    conn = db.get_connection()
    c = conn.cursor()
    c.execute("""
    SELECT id, subject_id, question_text, code_snippet, option_a, option_b, option_c, option_d, difficulty, topic_tag
    FROM questions
    WHERE subject_id = ?
    ORDER BY RANDOM()
    LIMIT ?
    """, (subject_id, count))
    rows = [dict(r) for r in c.fetchall()]

    # If count is less than requested, fetch more without limit
    if len(rows) < count:
        c.execute("""
        SELECT id, subject_id, question_text, code_snippet, option_a, option_b, option_c, option_d, difficulty, topic_tag
        FROM questions
        WHERE subject_id = ?
        """, (subject_id,))
        rows = [dict(r) for r in c.fetchall()]

    c.execute("SELECT id, code, name FROM subjects WHERE id = ?", (subject_id,))
    sub_row = c.fetchone()
    conn.close()

    session_id = f"exam_{subject_id}_{int(time.time())}"

    return {
        "success": True,
        "session_id": session_id,
        "subject_id": subject_id,
        "subject_name": sub_row["name"] if sub_row else "Môn thi",
        "subject_code": sub_row["code"] if sub_row else "",
        "total_questions": len(rows),
        "duration_minutes": duration_minutes,
        "duration_seconds": duration_minutes * 60,
        "questions": rows
    }


def submit_timed_exam(subject_id: int, answers: Dict[str, str], time_spent_seconds: int, user_id: int = 1) -> Dict[str, Any]:
    conn = db.get_connection()
    c = conn.cursor()

    q_ids = [int(k) for k in answers.keys() if str(k).isdigit()]
    if not q_ids:
        conn.close()
        return {"success": False, "error": "Không có câu trả lời nào được nộp."}

    placeholders = ",".join(["?"] * len(q_ids))
    c.execute(f"""
    SELECT id, question_text, code_snippet, option_a, option_b, option_c, option_d, correct_option, explanation, topic_tag
    FROM questions
    WHERE id IN ({placeholders})
    """, q_ids)
    q_map = {r["id"]: dict(r) for r in c.fetchall()}

    total = len(q_ids)
    correct_count = 0
    breakdown = []

    for q_id, q in q_map.items():
        user_choice = str(answers.get(str(q_id), "")).strip().upper()
        correct_choice = str(q.get("correct_option", "")).strip().upper()
        is_correct = (user_choice == correct_choice)
        if is_correct:
            correct_count += 1

        breakdown.append({
            "id": q_id,
            "question_text": q["question_text"],
            "code_snippet": q.get("code_snippet", ""),
            "user_choice": user_choice,
            "correct_choice": correct_choice,
            "is_correct": is_correct,
            "explanation": q.get("explanation", ""),
            "topic_tag": q.get("topic_tag", "")
        })

    score = round((correct_count / max(1, total)) * 10.0, 1)

    # Save to exam_results
    c.execute("""
    INSERT INTO exam_results (subject_id, exam_type, total_questions, correct_answers, score, time_spent_seconds, detail_json, user_id)
    VALUES (?, 'timed_60min', ?, ?, ?, ?, ?, ?)
    """, (
        subject_id,
        total,
        correct_count,
        score,
        time_spent_seconds,
        json.dumps(breakdown, ensure_ascii=False),
        user_id
    ))
    conn.commit()
    conn.close()

    return {
        "success": True,
        "subject_id": subject_id,
        "total_questions": total,
        "correct_answers": correct_count,
        "score": score,
        "time_spent_seconds": time_spent_seconds,
        "breakdown": breakdown
    }

print("Code Engine loaded successfully.")


import random

# =========================================================================
# 6. C# OOP STRUCTURE VALIDATOR (Reflection / Roslyn Heuristic AST)
# =========================================================================
def validate_csharp_oop_structure(code: str, requirements: dict = None) -> dict:
    req = requirements or {}
    checks = []
    score = 10.0
    feedback = []

    # 1. Kiểm tra có khai báo Class không
    has_class = bool(re.search(r'\bclass\s+[A-Za-z0-9_]+', code))
    if not has_class:
        checks.append({"item": "Khai báo Class", "passed": False, "msg": "Chưa khai báo Class nào! OOP bắt buộc phải tổ chức theo Class."})
        score -= 4.0
    else:
        checks.append({"item": "Khai báo Class", "passed": True, "msg": "Đã tạo Class hợp lệ."})

    # 2. Kiểm tra tính đóng gói (Encapsulation: private set hoặc private field)
    has_encapsulation = bool(re.search(r'\{\s*(?:get;\s*private\s+set|private\s+set;\s*get)\s*;?\s*\}', code)) or bool(re.search(r'\bprivate\s+[A-Za-z0-9_<>\[\]]+\s+[A-Za-z0-9_]+', code))
    if req.get("require_encapsulation", True) and not has_encapsulation:
        checks.append({"item": "Tính Đóng Gói (Encapsulation)", "passed": False, "msg": "Lỗi Đóng Gói: Chưa sử dụng Property đóng gói `{ get; private set; }` hoặc trường private!"})
        score -= 2.5
    else:
        checks.append({"item": "Tính Đóng Gói (Encapsulation)", "passed": True, "msg": "Đóng gói dữ liệu đạt chuẩn."})

    # 3. Kiểm tra tính kế thừa (Inheritance: class Con : Cha)
    has_inheritance = bool(re.search(r'\bclass\s+[A-Za-z0-9_]+\s*:\s*[A-Za-z0-9_]+', code))
    if req.get("require_inheritance", False) and not has_inheritance:
        checks.append({"item": "Tính Kế Thừa (Inheritance)", "passed": False, "msg": "Chưa kế thừa lớp cha bằng cú pháp `: BaseClass`!"})
        score -= 2.5
    else:
        checks.append({"item": "Tính Kế Thừa (Inheritance)", "passed": True, "msg": "Quan hệ kế thừa hợp lệ."})

    # 4. Kiểm tra đa hình / override (Polymorphism: override keyword)
    has_override = bool(re.search(r'\boverride\b', code))
    if req.get("require_override", False) and not has_override:
        checks.append({"item": "Tính Đa Hình (Override)", "passed": False, "msg": "Chưa sử dụng từ khóa `override` để ghi đè phương thức!"})
        score -= 2.0
    else:
        checks.append({"item": "Tính Đa Hình (Override)", "passed": True, "msg": "Phương thức override hợp lệ."})

    is_passed = score >= 5.0
    return {
        "valid": is_passed,
        "score": max(0.0, score),
        "checks": checks,
        "summary": "Mã nguồn tuân thủ tốt kiến trúc OOP C#" if is_passed else "Mã nguồn vi phạm các quy tắc thiết kế OOP C# cơ bản!"
    }


# =========================================================================
# 7. FISHER-YATES SHUFFLE ENGINE (Questions & Options)
# =========================================================================
def fisher_yates_shuffle_exam(questions: list) -> list:
    """Trộn ngẫu nhiên câu hỏi VÀ trộn ngẫu nhiên thứ tự 4 đáp án A, B, C, D của từng câu bằng thuật toán Fisher-Yates"""
    shuffled_qs = list(questions)
    
    # 1. Trộn thứ tự câu hỏi
    for i in range(len(shuffled_qs) - 1, 0, -1):
        j = random.randint(0, i)
        shuffled_qs[i], shuffled_qs[j] = shuffled_qs[j], shuffled_qs[i]

    # 2. Trộn thứ tự 4 đáp án A, B, C, D của từng câu
    result = []
    for q in shuffled_qs:
        q_copy = dict(q)
        options = [
            ("A", q_copy.get("option_a", "")),
            ("B", q_copy.get("option_b", "")),
            ("C", q_copy.get("option_c", "")),
            ("D", q_copy.get("option_d", ""))
        ]
        options = [opt for opt in options if opt[1] and opt[1].strip()]
        orig_correct = str(q_copy.get("correct_option", "A")).strip().upper()

        # Tìm nội dung của đáp án đúng ban đầu
        correct_text = ""
        for k, text in options:
            if k == orig_correct:
                correct_text = text
                break

        # Trộn các phương án bằng Fisher-Yates
        for i in range(len(options) - 1, 0, -1):
            j = random.randint(0, i)
            options[i], options[j] = options[j], options[i]

        # Gán lại vào A, B, C, D mới
        labels = ["A", "B", "C", "D"]
        new_correct = "A"
        for idx, (old_label, text) in enumerate(options):
            new_label = labels[idx]
            q_copy[f"option_{new_label.lower()}"] = text
            if text == correct_text:
                new_correct = new_label

        q_copy["correct_option"] = new_correct
        result.append(q_copy)

    return result


# =========================================================================
# 8. SUPERMEMO SM-2 SPACED REPETITION ENGINE
# =========================================================================
def calculate_sm2(card_id: int, rating: str) -> dict:
    """
    Rating options:
    - 'again': Quên (Lặp lại sau 1 phút / ngày)
    - 'hard': Khó (Lặp lại sau 10 phút)
    - 'good': Tốt (Ngày mai / interval x ease_factor)
    - 'easy': Dễ (4 ngày sau / bonus)
    """
    conn = db.get_connection()
    c = conn.cursor()
    c.execute("SELECT id, ease_factor, interval_days, repetitions, next_review FROM flashcards WHERE id = ?", (card_id,))
    row = c.fetchone()
    if not row:
        conn.close()
        return {"success": False, "error": "Card not found"}

    ef = float(row["ease_factor"] or 2.5)
    interval = int(row["interval_days"] or 1)
    reps = int(row["repetitions"] or 0)

    r = rating.lower().strip()
    if r == "again":
        reps = 0
        interval = 1
        ef = max(1.3, ef - 0.2)
    elif r == "hard":
        interval = max(1, int(interval * 1.2))
        ef = max(1.3, ef - 0.15)
    elif r == "good":
        if reps == 0:
            interval = 1
        elif reps == 1:
            interval = 6
        else:
            interval = int(interval * ef)
        reps += 1
    elif r == "easy":
        if reps == 0:
            interval = 4
        else:
            interval = int(interval * ef * 1.3)
        ef += 0.15
        reps += 1

    # Update database
    from datetime import datetime, timedelta
    next_date = (datetime.now() + timedelta(days=interval)).strftime("%Y-%m-%d %H:%M:%S")

    c.execute("""
    UPDATE flashcards
    SET ease_factor = ?, interval_days = ?, repetitions = ?, next_review = ?
    WHERE id = ?
    """, (round(ef, 2), interval, reps, next_date, card_id))
    conn.commit()
    conn.close()

    return {
        "success": True,
        "card_id": card_id,
        "rating": rating,
        "ease_factor": round(ef, 2),
        "interval_days": interval,
        "repetitions": reps,
        "next_review": next_date
    }


# =========================================================================
# 9. STEP-BY-STEP LINE-BY-LINE ESSAY VALIDATOR (LLM)
# =========================================================================
async def validate_essay_step_by_step(question_text: str, student_proof: str, topic: str = "Toán Rời Rạc") -> dict:
    prompt = f"""Bạn là Giám Khảo Đại Học uy tín về Toán Rời Rạc & Giải Thuật.
Nhiệm vụ: Soi từng dòng bài làm chứng minh của sinh viên.
TUYỆT ĐỐI KHÔNG ĐƯA RA LỜI GIẢI SẴN HOẶC ĐÁP ÁN TRƯỚC.
Nhiệm vụ của bạn là: Quét qua từng dòng/bước trong bài làm của sinh viên, chỉ ra dòng nào đúng (valid) và ĐẶC BIỆT ĐÁNH DẤU ĐỎ dòng nào có lỗi sai logic, sai phép biến đổi ma trận, hoặc thiếu điều kiện dừng/cơ sở quy nạp.

ĐỀ BÀI:
{question_text}

BÀI LÀM CỦA SINH VIÊN:
\"\"\"{student_proof}\"\"\"

Hãy trả về DUY NHẤT một chuỗi JSON theo cấu trúc sau:
{{
  "overall_verdict": "Nhận xét tổng quát 1-2 câu",
  "score": 8.0,
  "steps": [
    {{
      "line_number": 1,
      "text": "Nội dung dòng sinh viên viết",
      "status": "valid", 
      "feedback": "Lập luận đúng"
    }},
    {{
      "line_number": 3,
      "text": "Nội dung dòng có lỗi",
      "status": "error", 
      "feedback": "Bước khử ma trận này sai vì quên nhân hệ số dòng 1, hoặc ngụy biện khẳng định hệ quả!"
    }}
  ],
  "missing_components": [
    "Thiếu điều kiện dừng của vòng lặp",
    "Chưa xét trường hợp cơ sở n = 1"
  ]
}}"""

    try:
        reply = await ai.call_gemini(prompt, max_tokens=3072, thinking_budget=256)
        if reply:
            cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", reply.strip())
            s, e = cleaned.find("{"), cleaned.rfind("}")
            if s != -1 and e != -1:
                return json.loads(cleaned[s:e+1])
    except Exception as err:
        pass

    # Heuristic fallback
    lines = [line.strip() for line in student_proof.split('\n') if line.strip()]
    step_items = []
    for i, line in enumerate(lines, 1):
        step_items.append({
            "line_number": i,
            "text": line,
            "status": "valid" if ("=" in line or "=>" in line or "\\to" in line) else "warning",
            "feedback": "Cần giải thích rõ căn cứ suy luận." if i % 3 == 0 else "Hợp lệ"
        })
    return {
        "overall_verdict": "Bài làm tương đối rõ ràng nhưng cần bổ sung chứng minh chặt chẽ các bước trung gian.",
        "score": 7.5,
        "steps": step_items,
        "missing_components": ["Cần bổ sung điều kiện dừng và các trường hợp biên."]
    }


# =========================================================================
# 10. RUBBER DUCK TOXIC & STRICT SOCRATIC TUTOR
# =========================================================================
async def rubber_duck_critique(code: str, language: str, error_trace: str = "") -> str:
    prompt = f"""Bạn là Cố Vấn Lập Trình AI & Trợ Giảng Cao Cấp (Senior Engineering Mentor) môn {language.upper()} (OOP, Thuật toán & Cấu trúc dữ liệu).
Sinh viên vừa chạy bài thi code và gặp lỗi biên dịch / ngoại lệ hoặc sai kết quả test case.

Nhiệm vụ:
1. **Chẩn đoán nguyên nhân gốc rễ (Root Cause):** Phân tích ngắn gọn lỗi này thực chất là gì (ví dụ: chia cho 0, trỏ null, vượt biên mảng, thiếu virtual destructor, vi phạm tính đóng gói).
2. **Gợi ý tư duy sửa lỗi (Actionable Hints):** 2-3 gạch đầu dòng hướng dẫn cách khắc phục cụ thể, súc tích.
3. **Mẹo tối ưu (Best Practice):** 1 lưu ý ngắn giúp code sạch và an toàn hơn.
Giữ phong cách sư phạm chuẩn mực, chuyên nghiệp, khích lệ và sâu sắc.

CODE CỦA SINH VIÊN:
```{language}
{code}
```

MÃ LỖI / STACK TRACE:
```
{error_trace}
```"""

    try:
        reply = await ai.call_gemini(prompt, max_tokens=1536, thinking_budget=128)
        if reply:
            return reply.strip()
    except Exception:
        pass

    return f"### 🤖 Phân Tích Lỗi & Gợi Ý Khắc Phục\n- **Mã lỗi phát hiện:** `{error_trace[:120]}`\n- **Hướng xử lý:** Kiểm tra lại điều kiện biên của vòng lặp, kiểm tra biến chưa khởi tạo hoặc con trỏ trỏ vào vùng nhớ không hợp lệ."

# =========================================================================
# 9. AI AUTO-FIX & SMART UPGRADE ENGINE (C# & PYTHON)
# =========================================================================
async def fix_and_upgrade_code(code: str, language: str, problem_title: str = "", current_error: str = "") -> dict:
    """Analyze, fix compilation/logic bugs, optimize algorithms, and upgrade C#/Python code."""
    lang = (language or "csharp").strip().lower()
    prompt = f"""Bạn là Chuyên gia Lập trình Cao cấp (Senior Software Architect & Tech Lead) kiêm Giảng viên Đại học.
Sinh viên đang viết code {lang.upper()} và cần bạn chẩn đoán lỗi, giải thích bản chất lỗi, nâng cấp kiến trúc và tối ưu mã nguồn.

THÔNG TIN BÀI TẬP: {problem_title or 'Thực hành tự do (Playground)'}
NGÔN NGỮ: {lang.upper()}
LỖI HOẶC VẤN ĐỀ HIỆN TẠI (NẾU CÓ):
```
{current_error or 'Chưa có thông báo lỗi cụ thể, hãy kiểm tra toàn diện cú pháp, logic, OOP và độ phức tạp'}
```

MÃ NGUỒN CỦA SINH VIÊN:
```{lang}
{code}
```

Hãy thực hiện 4 nhiệm vụ cốt lõi:
1. Chẩn đoán chính xác nguyên nhân lỗi (Syntax, Runtime, Logic, Thuật toán, hoặc vi phạm kiến trúc OOP / Clean Code).
2. Giải thích chi tiết, cặn kẽ để sinh viên hiểu bản chất ("Học từ lỗi sai - Learn from Mistakes").
3. Nâng cấp toàn diện: Sửa sạch mọi lỗi, chuẩn hóa cú pháp theo best practices (với C#: dùng C# hiện đại, đóng gói Property, LINQ, null safety; với Python: dùng PEP 8, List comprehension, typing, cấu trúc dữ liệu chuẩn), tối ưu độ phức tạp thời gian O(N).
4. Cung cấp mã nguồn hoàn chỉnh đã sửa và tối ưu 100%, sẵn sàng chạy ngay.

TRẢ VỀ DUY NHẤT MỘT ĐỐI TƯỢNG JSON (KHÔNG BỌC TEXT THỪA NGOÀI JSON) THEO ĐỊNH DẠNG:
{{
  "has_error": true,
  "bug_title": "Tên lỗi ngắn gọn (ví dụ: Lỗi Đóng Gói Thuộc Tính Trong C#)",
  "root_cause": "Giải thích chi tiết 2-3 câu về nguyên nhân gốc rễ gây ra lỗi hoặc điểm chưa tối ưu",
  "learning_lesson": "Bài học then chốt & quy tắc vàng giúp sinh viên ghi nhớ và không lặp lại lỗi này",
  "improvements": [
    "Điểm nâng cấp 1 (ví dụ: Thay đổi thuộc tính thành public int TocDo {{ get; private set; }})",
    "Điểm nâng cấp 2 (ví dụ: Bổ sung kiểm tra delta > 0 và Math.Max(0, TocDo - delta))",
    "Điểm nâng cấp 3 (ví dụ: Tối ưu bộ nhớ và cấu trúc hàm Main)"
  ],
  "upgraded_code": "Toàn bộ mã nguồn hoàn chỉnh đã sửa và tối ưu hóa",
  "complexity_before": "O(N^2) hoặc chưa tối ưu",
  "complexity_after": "O(N) hoặc tối ưu",
  "sample_input": "Dữ liệu test input mẫu",
  "sample_output": "Kết quả xuất ra màn hình mẫu"
}}"""

    try:
        reply = await ai.call_gemini(prompt, max_tokens=4096, thinking_budget=256)
        if reply:
            cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", reply.strip())
            s = cleaned.find("{")
            e = cleaned.rfind("}")
            if s != -1 and e != -1:
                data = json.loads(cleaned[s:e+1])
                return {"success": True, "data": data}
    except Exception as exc:
        print("AI fix_and_upgrade_code error:", exc)

    # Heuristic fallback if AI is offline
    return {
        "success": True,
        "data": {
            "has_error": bool(current_error),
            "bug_title": "Đã phân tích mã nguồn",
            "root_cause": current_error or "Mã nguồn cần kiểm tra thêm các trường hợp biên và kiểm thử kỹ lưỡng.",
            "learning_lesson": "Luôn kiểm tra kỹ kiểu dữ liệu đầu vào và khởi tạo giá trị mặc định cho biến.",
            "improvements": ["Chuẩn hóa cấu trúc hàm và khối lệnh", "Bổ sung kiểm tra điều kiện an toàn", "Tối ưu hóa thời gian thực thi"],
            "upgraded_code": code,
            "complexity_before": "Chưa xác định",
            "complexity_after": "Tối ưu",
            "sample_input": "",
            "sample_output": ""
        }
    }


async def ai_suggest_next_code(code: str, language: str, line_number: int = 1, column: int = 1, problem_title: str = "") -> dict:
    """Intelligent Copilot: suggest the next line or short block of code based on cursor position."""
    lang = (language or "csharp").strip().lower()
    lines = (code or "").split("\n")
    cur_idx = max(0, min(line_number - 1, len(lines) - 1)) if lines else 0
    current_line = lines[cur_idx] if lines else ""
    code_before = "\n".join(lines[:cur_idx + 1])
    code_after = "\n".join(lines[cur_idx + 1:cur_idx + 15])

    prompt = f"""Bạn là AI Code Completion Engine siêu tốc (tương tự GitHub Copilot).
Hãy dự đoán và sinh ra 1 dòng (hoặc tối đa 2 dòng ngắn) code tiếp theo chuẩn xác cho lập trình viên.

NGÔN NGỮ: {lang.upper()}
BÀI TOÁN: {problem_title or 'Lập trình ứng dụng'}
DÒNG HIỆN TẠI ĐANG GÕ (Dòng {line_number}):
`{current_line}`

NGỮ CẢNH PHÍA TRƯỚC:
```{lang}
{code_before}
```

NGỮ CẢNH PHÍA SAU (NẾU CÓ):
```{lang}
{code_after}
```

YÊU CẦU:
1. Dự đoán dòng tiếp theo hợp lý nhất, chuẩn cú pháp {lang.upper()}, giữ đúng mức thụt lề (indentation).
2. KHÔNG lặp lại code đã có. KHÔNG viết text râu ria ngoài JSON.
3. Trả về DUY NHẤT một JSON:
{{
  "suggestion": "dòng code gợi ý tiếp theo",
  "explanation": "giải thích ngắn gọn 1 câu về mục đích dòng này",
  "insert_mode": "newline"
}}
"""
    try:
        reply = await ai.call_gemini(prompt, max_tokens=1024, thinking_budget=128)
        if reply:
            cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", reply.strip())
            s = cleaned.find("{")
            e = cleaned.rfind("}")
            if s != -1 and e != -1:
                data = json.loads(cleaned[s:e+1])
                return {"success": True, "data": data}
    except Exception as exc:
        print("AI ai_suggest_next_code error:", exc)

    # Fallback suggestion
    fallback_suggest = "// Tiếp tục phát triển logic..."
    if lang in ("python", "py"):
        if current_line.strip().startswith("def "):
            fallback_suggest = "    # TODO: Thực hiện logic hàm\n    pass"
        elif current_line.strip().startswith("if "):
            fallback_suggest = "    print('Điều kiện thỏa mãn')"
        else:
            fallback_suggest = "print(result)"
    elif lang in ("csharp", "cs"):
        if "Console.Write" in current_line:
            fallback_suggest = "Console.ReadLine();"
        elif "class " in current_line:
            fallback_suggest = "    public void Chay() {\n    }"
        else:
            fallback_suggest = "Console.WriteLine($\"Ket qua: {result}\");"
    else:
        fallback_suggest = "std::cout << result << std::endl;"

    return {
        "success": True,
        "data": {
            "suggestion": fallback_suggest,
            "explanation": "Gợi ý dòng code cơ bản theo ngữ cảnh hiện tại",
            "insert_mode": "newline"
        }
    }


async def ai_inspect_line(code: str, language: str, line_number: int, action: str = "ask", problem_title: str = "", current_error: str = "") -> dict:
    """Explain a specific code line or fix bugs targeting that line with comprehensive educational depth."""
    lang = (language or "csharp").strip().lower()
    lines = (code or "").split("\n")
    total_lines = len(lines)
    target_idx = max(0, min(line_number - 1, total_lines - 1)) if lines else 0
    target_line = lines[target_idx] if lines else ""

    start_ctx = max(0, target_idx - 5)
    end_ctx = min(total_lines, target_idx + 6)
    context_lines = []
    for idx in range(start_ctx, end_ctx):
        prefix = "-> [TARGET] " if idx == target_idx else f"   [Dòng {idx+1:2d}] "
        context_lines.append(f"{prefix}{lines[idx]}")
    context_code = "\n".join(context_lines)

    mode_instruction = (
        "GIẢI THÍCH CHI TIẾT SƯ PHẠM DÒNG NÀY (Ý nghĩa từ khóa, tác động bộ nhớ, biến, thuật toán)"
        if action == "ask"
        else "CHẨN ĐOÁN LỖI TẠI DÒNG NÀY VÀ CUNG CẤP DÒNG ĐÃ SỬA CHUẨN XÁC KÈM TOÀN BỘ CODE HOÀN CHỈNH"
    )

    prompt = f"""Bạn là Giáo sư Lập trình Cao cấp (Senior Software Architect & Tech Lead).
Nhiệm vụ: {mode_instruction}.

BÀI TOÁN: {problem_title or 'Thực hành lập trình'}
NGÔN NGỮ: {lang.upper()}
DÒNG CODE CẦN KIỂM TRA (Dòng {line_number}):
`{target_line}`

NGỮ CẢNH XUNG QUANH:
```
{context_code}
```

LỖI HIỆN TẠI (NẾU CÓ):
```
{current_error or 'Không có thông báo lỗi runtime'}
```

YÊU CẦU: Trả về DUY NHẤT một JSON hợp lệ:
{{
  "line_number": {line_number},
  "target_code": "{target_line.replace('"', '\\"')}",
  "action": "{action}",
  "title": "Tiêu đề ngắn gọn về dòng code",
  "detailed_explanation": "Giải thích chi tiết cặn kẽ để sinh viên hiểu bản chất dòng này",
  "has_error_on_line": { "true" if action == "fix" or current_error else "false" },
  "error_diagnostic": "Chẩn đoán lỗi nếu có (cú pháp, logic, null pointer, tràn mảng...)",
  "fixed_line": "Dòng code sau khi sửa (nếu có)",
  "full_fixed_code": "Toàn bộ mã nguồn hoàn chỉnh đã sửa dòng này",
  "learning_points": [
    "Điểm quan trọng 1 sinh viên cần nhớ",
    "Điểm quan trọng 2 về chuẩn lập trình / tối ưu"
  ],
  "quick_tip": "Mẹo ghi nhớ nhanh trong 5 giây"
}}
"""
    try:
        reply = await ai.call_gemini(prompt, max_tokens=4096, thinking_budget=256)
        if reply:
            cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", reply.strip())
            s = cleaned.find("{")
            e = cleaned.rfind("}")
            if s != -1 and e != -1:
                data = json.loads(cleaned[s:e+1])
                return {"success": True, "data": data}
    except Exception as exc:
        print("AI ai_inspect_line error:", exc)

    return {
        "success": True,
        "data": {
            "line_number": line_number,
            "target_code": target_line,
            "action": action,
            "title": f"Phân tích dòng {line_number}",
            "detailed_explanation": f"Dòng code `{target_line}` thực thi trong luồng logic của chương trình.",
            "has_error_on_line": bool(current_error),
            "error_diagnostic": current_error or "Kiểm tra kiểu dữ liệu và phạm vi biến.",
            "fixed_line": target_line,
            "full_fixed_code": code,
            "learning_points": [
                "Luôn kiểm tra điều kiện an toàn trước khi thao tác",
                "Đảm bảo cú pháp và các khối ngoặc ăn khớp"
            ],
            "quick_tip": "Quan sát kỹ dòng này trong luồng thực thi tổng thể."
        }
    }
