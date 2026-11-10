import sqlite3

# 1. Update SQLite Schema
conn = sqlite3.connect('unimaster.db')
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS archived_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    history_type TEXT NOT NULL,
    item_id TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    archived_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")
conn.commit()
conn.close()
print("Table archived_history created/verified in unimaster.db!")

# 2. Add methods to database.py
with open('database.py', 'r', encoding='utf-8') as f:
    db_code = f.read()

db_funcs = """
def save_archived_item(history_type: str, item_id: str, payload_json: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute(\"\"\"
    INSERT INTO archived_history (history_type, item_id, payload_json)
    VALUES (?, ?, ?)
    \"\"\", (history_type, item_id, payload_json))
    conn.commit()
    conn.close()

def get_archived_items(history_type: str = None, limit: int = 100):
    conn = get_connection()
    c = conn.cursor()
    if history_type:
        c.execute(\"\"\"
        SELECT id, history_type, item_id, payload_json, archived_at
        FROM archived_history
        WHERE history_type = ?
        ORDER BY archived_at DESC LIMIT ?
        \"\"\", (history_type, limit))
    else:
        c.execute(\"\"\"
        SELECT id, history_type, item_id, payload_json, archived_at
        FROM archived_history
        ORDER BY archived_at DESC LIMIT ?
        \"\"\", (limit,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def delete_archived_item(archive_id: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM archived_history WHERE id = ?", (archive_id,))
    conn.commit()
    conn.close()
"""

if "def save_archived_item(" not in db_code:
    db_code += "\n" + db_funcs
    with open('database.py', 'w', encoding='utf-8') as f:
        f.write(db_code)
    print("Added archive methods to database.py!")

# 3. Add endpoints to server.py
with open('server.py', 'r', encoding='utf-8') as f:
    srv_code = f.read()

srv_handlers = """
async def api_archive_save(request):
    try:
        data = await safe_get_json(request)
        htype = str(data.get("history_type", "exam"))
        item_id = str(data.get("item_id", "item_" + str(int(time.time()))))
        payload = json.dumps(data.get("payload", {}), ensure_ascii=False)
        db.save_archived_item(htype, item_id, payload)
        return json_resp({"success": True})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, status=500)

async def api_archive_list(request):
    try:
        htype = request.query.get("type", None)
        items = db.get_archived_items(htype)
        for it in items:
            try:
                it["payload"] = json.loads(it["payload_json"])
            except Exception:
                it["payload"] = {}
        return json_resp({"success": True, "items": items})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, status=500)
"""

if "async def api_archive_save(" not in srv_code:
    target_pos = "async def get_stats(request):"
    srv_code = srv_code.replace(target_pos, srv_handlers + "\n\n" + target_pos)

    # Add routes
    route_anchor = '    app.router.add_get("/api/stats", get_stats)\n'
    archive_routes = '    app.router.add_post("/api/history/archive", api_archive_save)\n    app.router.add_get("/api/history/archive", api_archive_list)\n'
    srv_code = srv_code.replace(route_anchor, archive_routes + route_anchor)
    with open('server.py', 'w', encoding='utf-8') as f:
        f.write(srv_code)
    print("Added archive endpoints and routes to server.py!")
