import asyncio
import code_engine

async def main():
    print("Testing code_engine...")
    sug = await code_engine.ai_suggest_next_code(
        code="def solve(n):\n    total = 0\n    for i in range(n):\n",
        language="python",
        line_number=3,
        column=22,
        problem_title="Tính tổng"
    )
    print("Suggest result:", sug.get("success"), sug.get("data", {}).get("suggestion"))
    assert sug["success"] is True

    insp = await code_engine.ai_inspect_line(
        code="def solve(n):\n    total = 0\n    for i in range(n):\n        total += i\n    return total\n",
        language="python",
        line_number=4,
        action="explain",
        problem_title="Tính tổng",
        current_error=""
    )
    print("Inspect explain:", insp.get("success"), insp.get("data", {}).get("detailed_explanation", "")[:60])
    assert insp["success"] is True

    insp_fix = await code_engine.ai_inspect_line(
        code="def solve(n):\n    total = 0\n    for i in rang(n):\n        total += i\n    return total\n",
        language="python",
        line_number=3,
        action="fix",
        problem_title="Tính tổng",
        current_error="NameError: name 'rang' is not defined"
    )
    print("Inspect fix:", insp_fix.get("success"), insp_fix.get("data", {}).get("fixed_line"))
    assert insp_fix["success"] is True
    print("ALL TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    asyncio.run(main())
