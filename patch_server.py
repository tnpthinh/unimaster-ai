# -*- coding: utf-8 -*-
with open('server.py', 'r', encoding='utf-8') as f:
    c = f.read()

old_block = '''async def api_code_suggest(request):
    try:
        data = await safe_get_json(request)
        code = data.get("code", "")
        lang = data.get("language", "csharp")
        line = int(data.get("line_number", 1))
        col = int(data.get("column", 1))
        title = data.get("title", "")
        res = await code_engine.ai_suggest_next_code(code, lang, line_number=line, column=col, problem_title=title)
        return json_resp(res)
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)

async def api_code_inspect_line(request):
    try:
        data = await safe_get_json(request)
        code = data.get("code", "")
        lang = data.get("language", "csharp")
        line = int(data.get("line_number", 1))
        action = data.get("action", "ask")
        title = data.get("title", "")
        error = data.get("error", "")
        res = await code_engine.ai_inspect_line(code, lang, line_number=line, action=action, problem_title=title, current_error=error)
        return json_resp(res)
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)'''

new_block = '''async def api_code_suggest(request):
    try:
        data = await safe_get_json(request)
        code = data.get("code", "")
        lang = data.get("language", "csharp")
        line = int(data.get("line", data.get("line_number", 1)))
        col = int(data.get("column", 1))
        title = data.get("problem_title", data.get("title", ""))
        res = await code_engine.ai_suggest_next_code(code, lang, line_number=line, column=col, problem_title=title)
        inner = res.get("data", {}) if isinstance(res, dict) else {}
        sug_text = inner.get("suggestion", "")
        expl_text = inner.get("explanation", "")
        return json_resp({
            "ok": True,
            "success": True,
            "suggestion": sug_text,
            "explanation": expl_text,
            "data": inner
        })
    except Exception as e:
        return json_resp({"ok": False, "success": False, "error": str(e)}, 500)

async def api_code_inspect_line(request):
    try:
        data = await safe_get_json(request)
        code = data.get("code", "")
        lang = data.get("language", "csharp")
        line = int(data.get("line", data.get("line_number", 1)))
        action = data.get("action", "explain")
        title = data.get("problem_title", data.get("title", ""))
        error = data.get("current_error", data.get("error", ""))
        res = await code_engine.ai_inspect_line(code, lang, line_number=line, action=action, problem_title=title, current_error=error)
        inner = res.get("data", {}) if isinstance(res, dict) else {}
        return json_resp({
            "ok": True,
            "success": True,
            "line_number": line,
            "target_line_text": inner.get("target_code", inner.get("target_line_text", "")),
            "explanation": inner.get("detailed_explanation", inner.get("explanation", "")),
            "patched_line": inner.get("fixed_line", inner.get("patched_line", "")),
            "patched_code": inner.get("full_fixed_code", inner.get("patched_code", "")),
            "learning_points": inner.get("learning_points", []),
            "quick_tip": inner.get("quick_tip", ""),
            "data": inner
        })
    except Exception as e:
        return json_resp({"ok": False, "success": False, "error": str(e)}, 500)'''

if old_block in c:
    c = c.replace(old_block, new_block, 1)
    with open('server.py', 'w', encoding='utf-8') as f:
        f.write(c)
    print('Updated server.py routes successfully')
else:
    print('Old block not found in server.py')
