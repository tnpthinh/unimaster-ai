srv_path = r'C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai\server.py'
with open(srv_path, 'r', encoding='utf-8') as f:
    srv = f.read()

target = 'return json_resp({"success": True, "comments": comments})'
replacement = 'return json_resp({"success": True, "comments": comments, "discussions": comments})'

if target in srv:
    srv = srv.replace(target, replacement, 1)
    with open(srv_path, 'w', encoding='utf-8') as f:
        f.write(srv)
    print("Updated server.py get_question_discussions_handler to return both keys")
else:
    print("Target not found in server.py")
