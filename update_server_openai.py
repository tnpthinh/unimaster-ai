import os

server_path = r'C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai\server.py'
with open(server_path, 'r', encoding='utf-8') as f:
    text = f.read()

old_block = '''        pool_status = ai.get_pool_status()
        return json_resp({
            "success": True,
            "key_count": len(pool_status),
            "pool": pool_status,
            "message": f"Đã cập nhật dàn {len(pool_status)} API Key luân phiên!"
        })'''

new_block = '''        if "openai_api_key" in data:
            db.set_setting("openai_api_key", str(data["openai_api_key"]).strip())
        if "openai_base_url" in data:
            db.set_setting("openai_base_url", str(data["openai_base_url"]).strip())
        if "ai_provider_priority" in data:
            db.set_setting("ai_provider_priority", str(data["ai_provider_priority"]).strip())

        pool_status = ai.get_pool_status()
        openai_cfg = ai.get_openai_settings()
        masked_openai = ai.mask_key(openai_cfg.get("key", "")) if openai_cfg.get("key") else ""
        return json_resp({
            "success": True,
            "key_count": len(pool_status),
            "pool": pool_status,
            "openai": {
                "has_key": bool(openai_cfg.get("key")),
                "masked_key": masked_openai,
                "base_url": openai_cfg.get("base_url"),
                "priority": openai_cfg.get("priority", "openai_first")
            },
            "message": f"Đã cập nhật dàn {len(pool_status)} API Key luân phiên và cấu hình AI!"
        })'''

if old_block in text:
    text = text.replace(old_block, new_block, 1)
    print("Replaced settings block")
else:
    print("Settings block already replaced or not found")

old_route = 'app.router.add_post("/api/ai/test-all-keys", test_all_keys_handler)'
new_route = 'app.router.add_post("/api/ai/test-all-keys", test_all_keys_handler)\n    app.router.add_post("/api/ai/test-openai", handle_test_openai_key)'

if old_route in text and '/api/ai/test-openai' not in text:
    text = text.replace(old_route, new_route, 1)
    print("Added /api/ai/test-openai route")

with open(server_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Done updating server.py")
