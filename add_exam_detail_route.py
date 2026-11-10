with open('server.py', 'r', encoding='utf-8') as f:
    content = f.read()

handler_code = """
async def get_exam_detail(request):
    try:
        eid = int(request.match_info["id"])
        res = db.get_exam_result(eid)
        if not res:
            return json_resp({"success": False, "error": "Exam result not found"}, status=404)
        if res.get("detail_json"):
            try:
                res["details"] = json.loads(res["detail_json"])
            except Exception:
                res["details"] = []
        return json_resp({"success": True, "exam": res})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, status=500)
"""

if "async def get_exam_detail(" not in content:
    target = "async def get_exercises(request):"
    assert target in content, "target not found"
    content = content.replace(target, handler_code + "\n\n" + target)

route_line = '    app.router.add_get("/api/exam/detail/{id}", get_exam_detail)\n'
if route_line not in content:
    target_route = '    app.router.add_post("/api/exam/submit", submit_exam)\n'
    assert target_route in content, "target_route not found"
    content = content.replace(target_route, target_route + route_line)

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated server.py successfully!")
