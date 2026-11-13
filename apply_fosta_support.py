with open('ai_service.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = '''OPENAI_MODELS = [
    "gpt-4o-mini",
    "gpt-4o",
    "gpt-3.5-turbo"
]

def get_openai_settings() -> dict:
    key = get_setting("openai_api_key", "").strip() or os.environ.get("OPENAI_API_KEY", "").strip()
    base_url = get_setting("openai_base_url", "").strip() or os.environ.get("OPENAI_BASE_URL", "").strip() or "https://api.openai.com/v1"
    base_url = base_url.rstrip("/")
    priority = get_setting("ai_provider_priority", "openai_first").strip()
    return {"key": key, "base_url": base_url, "priority": priority}

async def _call_openai_chatgpt(prompt: str, system_instruction: str = "", max_tokens: int = 4096) -> str:
    cfg = get_openai_settings()
    key = cfg["key"]
    if not key:
        return None
    base_url = cfg["base_url"]
    endpoint = f"{base_url}/chat/completions"
    
    messages = []
    if system_instruction:
        messages.append({"role": "system", "content": system_instruction})
    messages.append({"role": "user", "content": prompt})

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        for model in OPENAI_MODELS:
            payload = {
                "model": model,
                "messages": messages,
                "max_tokens": min(max_tokens, 4096),
                "temperature": 0.4
            }
            try:
                async with session.post(endpoint, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=20)) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        choices = data.get("choices", [])
                        if choices:
                            reply = choices[0].get("message", {}).get("content", "").strip()
                            if reply:
                                print(f"[AI Service] Generated via OpenAI ChatGPT ({model})!")
                                return reply
                    elif resp.status in (401, 403, 404, 429):
                        err_text = await resp.text()
                        print(f"[AI Service] OpenAI {model} returned {resp.status}: {err_text[:120]}")
            except Exception as e:
                print(f"[AI Service] OpenAI {model} connection error: {e}")
                continue
    return None

async def test_openai_key(key: str = None, base_url: str = None) -> dict:
    cfg = get_openai_settings()
    target_key = (key or cfg["key"]).strip()
    target_url = ((base_url or cfg["base_url"]).strip()).rstrip("/")
    if not target_key:
        return {"success": False, "message": "Chưa nhập API Key"}
    endpoint = f"{target_url}/chat/completions"
    headers = {"Authorization": f"Bearer {target_key}", "Content-Type": "application/json"}
    payload = {"model": "gpt-4o-mini", "messages": [{"role": "user", "content": "Reply OK"}], "max_tokens": 10}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    return {"success": True, "model": "gpt-4o-mini", "masked_key": mask_key(target_key), "message": "Hoạt động tốt (OpenAI ChatGPT)"}
                elif resp.status == 401:
                    txt = await resp.text()
                    is_relay_format = ("-" in target_key and not target_key.startswith("sk-proj-"))
                    if is_relay_format and target_url == "https://api.openai.com/v1":
                        return {
                            "success": False,
                            "masked_key": mask_key(target_key),
                            "message": "Khóa API này là định dạng Proxy / Codex / Relay (không phải key trực tiếp của platform.openai.com). Vui lòng nhập 'Base URL' của nhà cung cấp proxy (ví dụ: https://api.chatanywhere.tech/v1 hoặc proxy trường học) vào ô Base URL!"
                        }
                    return {"success": False, "masked_key": mask_key(target_key), "message": f"Mã lỗi 401 (Sai API Key hoặc sai Base URL): {txt[:120]}"}
                else:
                    txt = await resp.text()
                    return {"success": False, "masked_key": mask_key(target_key), "message": f"Mã lỗi HTTP {resp.status}: {txt[:120]}"}
    except Exception as e:
        return {"success": False, "masked_key": mask_key(target_key), "message": f"Lỗi kết nối: {str(e)}"}'''

replacement = '''OPENAI_MODELS = [
    "gpt-4o-mini",
    "gpt-4o",
    "gpt-3.5-turbo"
]

FOSTA_MODELS = [
    "gpt-6.1-sol",
    "gpt-6-astra",
    "gpt-6-luna"
]

def get_openai_settings() -> dict:
    key = get_setting("openai_api_key", "").strip() or os.environ.get("OPENAI_API_KEY", "").strip()
    base_url = get_setting("openai_base_url", "").strip() or os.environ.get("OPENAI_BASE_URL", "").strip() or "https://codex.fosta.app/v1"
    base_url = base_url.rstrip("/")
    is_fosta = "fosta" in base_url.lower()
    default_model = "gpt-6.1-sol" if is_fosta else "gpt-4o-mini"
    model = get_setting("openai_model", default_model).strip() or default_model
    priority = get_setting("ai_provider_priority", "openai_first").strip()
    return {"key": key, "base_url": base_url, "model": model, "priority": priority}

async def _call_openai_chatgpt(prompt: str, system_instruction: str = "", max_tokens: int = 4096) -> str:
    cfg = get_openai_settings()
    key = cfg["key"]
    if not key:
        return None
    base_url = cfg["base_url"]
    endpoint = f"{base_url}/chat/completions"
    
    is_fosta = "fosta" in base_url.lower()
    pref_model = cfg.get("model", "gpt-6.1-sol" if is_fosta else "gpt-4o-mini")
    candidate_models = [pref_model]
    if is_fosta:
        for m in FOSTA_MODELS:
            if m not in candidate_models:
                candidate_models.append(m)
    else:
        for m in OPENAI_MODELS:
            if m not in candidate_models:
                candidate_models.append(m)

    messages = []
    if system_instruction:
        messages.append({"role": "system", "content": system_instruction})
    messages.append({"role": "user", "content": prompt})

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        for model in candidate_models:
            payload = {
                "model": model,
                "messages": messages,
                "max_tokens": min(max_tokens, 4096),
                "temperature": 0.4
            }
            try:
                async with session.post(endpoint, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=25)) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        choices = data.get("choices", [])
                        if choices:
                            reply = choices[0].get("message", {}).get("content", "").strip()
                            if reply:
                                p_name = "FOSTA Codex AI" if is_fosta else "OpenAI"
                                print(f"[AI Service] Generated via {p_name} ({model})!")
                                return reply
                    elif resp.status in (400, 401, 403, 404, 429, 503):
                        err_text = await resp.text()
                        print(f"[AI Service] Provider returned {resp.status} for model {model}: {err_text[:120]}")
            except Exception as e:
                print(f"[AI Service] Provider connection error for {model}: {e}")
                continue
    return None

async def test_openai_key(key: str = None, base_url: str = None, model: str = None) -> dict:
    cfg = get_openai_settings()
    target_key = (key or cfg["key"]).strip()
    target_url = ((base_url or cfg["base_url"]).strip()).rstrip("/")
    if not target_key:
        return {"success": False, "message": "Chưa nhập API Key"}
    endpoint = f"{target_url}/chat/completions"
    
    is_fosta = "fosta" in target_url.lower()
    target_model = model or (cfg.get("model") if cfg.get("model") else ("gpt-6.1-sol" if is_fosta else "gpt-4o-mini"))
    if is_fosta and target_model in ("gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"):
        target_model = "gpt-6.1-sol"

    headers = {"Authorization": f"Bearer {target_key}", "Content-Type": "application/json"}
    payload = {"model": target_model, "messages": [{"role": "user", "content": "Reply OK"}], "max_tokens": 15}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=12)) as resp:
                provider_title = "FOSTA Codex AI" if is_fosta else "OpenAI ChatGPT"
                if resp.status == 200:
                    data = await resp.json()
                    returned_model = data.get("model", target_model)
                    return {
                        "success": True,
                        "model": returned_model,
                        "provider": provider_title,
                        "masked_key": mask_key(target_key),
                        "message": f"Hoạt động xuất sắc! Kết nối thành công tới {provider_title} ({returned_model})"
                    }
                elif resp.status == 401:
                    txt = await resp.text()
                    if is_fosta and target_url == "https://api.openai.com/v1":
                        return {
                            "success": False,
                            "masked_key": mask_key(target_key),
                            "message": "Khóa API này là của FOSTA Codex App! Vui lòng đổi Base URL thành: https://codex.fosta.app/v1"
                        }
                    return {"success": False, "masked_key": mask_key(target_key), "message": f"Mã lỗi 401 (Sai API Key hoặc sai Base URL): {txt[:120]}"}
                else:
                    txt = await resp.text()
                    return {"success": False, "masked_key": mask_key(target_key), "message": f"Mã lỗi HTTP {resp.status}: {txt[:120]}"}
    except Exception as e:
        return {"success": False, "masked_key": mask_key(target_key), "message": f"Lỗi kết nối: {str(e)}"}'''

if target in text:
    text = text.replace(target, replacement)
    with open('ai_service.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("SUCCESS: Updated ai_service.py with FOSTA support!")
else:
    print("FAILED: Target block not found in ai_service.py")
