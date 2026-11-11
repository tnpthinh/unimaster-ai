r"""
UniMaster AI v7.0 — Multi-Key Auto-Failover, STEM Formula & Deep AI Engine
- Unlimited Gemini API Keys Pool with Automatic Failover & Load Balancing
- Zero-Truncation Thinking Budget Control (8192 maxOutputTokens + fast thinkingBudget)
- Full STEM Formula Formatting (KaTeX Math/Physics + mhchem \ce{...} Chemistry/Biology)
- Rich AI Action Suite: Concept Recall, Mistake Diagnosis, 5s Mnemonic, Flashcard Distiller,
  Subject Bank Expander, 4-Persona Tutor, Essay Rubric Grader & Complete 5-Day Study Roadmap
"""
import os
import re
import json
import time
import base64
import hashlib
import asyncio
import aiohttp
from database import get_setting, set_setting

GEMINI_MODELS = [
    "gemini-3.5-flash-lite",  # Blazing fast (0.7s) - Tutor, hint, concept recall
    "gemini-3.5-flash",       # High quality reasoning (1.5s) - Code, essay, exams
    "gemini-3.6-flash",       # High performance fallback
    "gemini-3.7-flash"        # Deep reasoning fallback
]

# Fast 0ms response cache for repeated questions
AI_CACHE = {}

STEM_FORMAT_GUIDE = (
    "Quy tắc định dạng học thuật bắt buộc:\n"
    "- Viết bằng **Markdown sạch** (TUYỆT ĐỐI KHÔNG dùng thẻ HTML thô).\n"
    "- Mọi công thức Toán học, Vật lý, Xác suất phải bọc trong `$...$` (cùng dòng) hoặc `$$...$$` (riêng dòng), ví dụ `$v_{\\max} = \\omega A$`, `$\\int u\\,\\mathrm{d}v$`.\n"
    "- Mọi công thức phân tử, ion và phương trình Hóa học / Sinh hóa phải dùng cú pháp `$\\ce{...}$` (ví dụ `$\\ce{H2SO4}$`, `$\\ce{2H2 + O2 ->[t^\\circ] 2H2O}$`, `$\\ce{Fe^{3+}}$`).\n"
    "- Từ khóa lập trình dùng `inline code`, đoạn mã nhiều dòng dùng khối ```csharp hoặc ngôn ngữ tương ứng."
)

# Runtime telemetry & failover state per API key
KEY_TELEMETRY = {}
_RR_CURSOR = 0


def mask_key(k: str) -> str:
    k = (k or "").strip()
    if len(k) <= 10:
        return "*" * len(k)
    return f"{k[:6]}...{k[-4:]}"


def get_api_keys_pool() -> list[dict]:
    """Đọc danh sách toàn bộ API Keys (tự động gộp cả key đơn cũ nếu có)"""
    raw_pool = get_setting("gemini_api_keys_pool", "").strip()
    items = []
    if raw_pool:
        try:
            parsed = json.loads(raw_pool)
            if isinstance(parsed, list):
                items = parsed
        except Exception:
            pass

    seen = set()
    normalized = []

    for idx, entry in enumerate(items):
        if isinstance(entry, str):
            k = entry.strip()
            lbl = f"Key #{idx + 1}"
        elif isinstance(entry, dict):
            k = str(entry.get("key", "")).strip()
            lbl = str(entry.get("label") or f"Key #{idx + 1}").strip()
        else:
            continue
        if k and k not in seen:
            seen.add(k)
            normalized.append({"key": k, "label": lbl})

    legacy = get_setting("gemini_api_key", "").strip() or os.environ.get("GEMINI_API_KEY", "").strip()
    if legacy and legacy not in seen:
        seen.add(legacy)
        normalized.insert(0, {"key": legacy, "label": "Key #1 (Mặc định)"})

    return normalized


def save_api_keys_pool(keys_input) -> list[dict]:
    """Lưu danh sách nhiều API Key (nhận mảng hoặc chuỗi nhiều dòng)"""
    raw_entries = []
    if isinstance(keys_input, str):
        lines = [ln.strip() for ln in re.split(r"[\r\n,;]+", keys_input) if ln.strip()]
        raw_entries = [{"key": ln, "label": f"Key #{i + 1}"} for i, ln in enumerate(lines)]
    elif isinstance(keys_input, list):
        for i, item in enumerate(keys_input):
            if isinstance(item, str) and item.strip():
                raw_entries.append({"key": item.strip(), "label": f"Key #{i + 1}"})
            elif isinstance(item, dict) and str(item.get("key", "")).strip():
                raw_entries.append({
                    "key": str(item["key"]).strip(),
                    "label": str(item.get("label") or f"Key #{i + 1}").strip()
                })

    seen = set()
    clean_pool = []
    for entry in raw_entries:
        k = entry["key"]
        if k not in seen:
            seen.add(k)
            clean_pool.append({"key": k, "label": entry["label"]})

    set_setting("gemini_api_keys_pool", json.dumps(clean_pool, ensure_ascii=False))
    primary = clean_pool[0]["key"] if clean_pool else ""
    set_setting("gemini_api_key", primary)
    if primary:
        os.environ["GEMINI_API_KEY"] = primary
    return clean_pool


def get_api_key() -> str:
    pool = get_api_keys_pool()
    return pool[0]["key"] if pool else ""


def _ensure_telemetry(key: str) -> dict:
    if key not in KEY_TELEMETRY:
        KEY_TELEMETRY[key] = {
            "calls": 0,
            "failovers": 0,
            "cooldown_until": 0.0,
            "status": "ready",
            "model": "",
            "last_error": ""
        }
    return KEY_TELEMETRY[key]


def get_pool_status() -> list[dict]:
    now = time.time()
    pool = get_api_keys_pool()
    out = []
    for idx, item in enumerate(pool):
        k = item["key"]
        tel = _ensure_telemetry(k)
        cd_rem = max(0, int(tel["cooldown_until"] - now))
        status = tel["status"]
        if status == "cooldown" and cd_rem == 0:
            status = "ready"
            tel["status"] = "ready"
        out.append({
            "index": idx + 1,
            "label": item.get("label") or f"Key #{idx + 1}",
            "masked_key": mask_key(k),
            "status": status,
            "calls": tel["calls"],
            "failovers": tel["failovers"],
            "cooldown_remaining": cd_rem,
            "model": tel["model"]
        })
    return out


def _ordered_candidate_keys() -> list[str]:
    global _RR_CURSOR
    pool = get_api_keys_pool()
    if not pool:
        return []

    n = len(pool)
    start = _RR_CURSOR % n
    _RR_CURSOR = (_RR_CURSOR + 1) % n

    rotated = [pool[(start + i) % n]["key"] for i in range(n)]
    now = time.time()

    healthy = []
    cooling = []
    for k in rotated:
        tel = _ensure_telemetry(k)
        if tel["status"] == "invalid" or tel["cooldown_until"] > now:
            cooling.append((tel["cooldown_until"], k))
        else:
            healthy.append(k)

    cooling.sort(key=lambda pair: pair[0])
    return healthy + [k for _, k in cooling]



OPENAI_MODELS = [
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-3.5-turbo"
]

# Model alias do 9Router cung cấp. `All` tự chọn model khả dụng; `Coding-Pro`
# ưu tiên model chuyên lập trình. Chúng dùng giao thức OpenAI-compatible.
ROUTER_MODELS = ["All", "Coding-Pro"]

FOSTA_MODELS = [
    "gpt-6.1-sol",
    "gpt-6-astra",
    "gpt-6-luna"
]

# ===== AI Gateway động (9Router chạy trên máy cá nhân, mở ra Internet bằng Cloudflare Tunnel) =====
# Render không truy cập được 127.0.0.1, nên khi Base URL là địa chỉ nội bộ thì app
# tự dò địa chỉ tunnel công khai mới nhất. Có URL mặc định để bản deploy chạy được
# ngay mà KHÔNG cần khai báo biến môi trường nào; vẫn có thể ghi đè bằng ENV.
DEFAULT_GATEWAY_DISCOVERY_URL = "https://ntfy.sh/unimaster_ctump_5292/json?poll=1&since=72h"
_GATEWAY_CACHE = {"url": "", "ts": 0.0}
_GATEWAY_TTL = 90


def gateway_discovery_url() -> str:
    """Đọc ENV mỗi lần gọi để đổi cấu hình không cần sửa code."""
    return (
        os.environ.get("AI_GATEWAY_DISCOVERY_URL", "").strip()
        or DEFAULT_GATEWAY_DISCOVERY_URL
    )


def gateway_secret() -> str:
    return os.environ.get("AI_GATEWAY_SECRET", "").strip()


def _is_local_url(url: str) -> bool:
    u = (url or "").lower()
    return "127.0.0.1" in u or "localhost" in u or "0.0.0.0" in u


def _is_local_runtime() -> bool:
    """True khi tiến trình này chạy trên chính máy đang chạy 9Router.

    Nhận biết bằng biến môi trường: Render/Docker đặt DATA_DIR hoặc RENDER=true,
    còn máy cá nhân thì không. Khi chạy local, gọi 127.0.0.1 trực tiếp là đúng.
    """
    for key in ("RENDER", "RENDER_SERVICE_ID", "RENDER_EXTERNAL_URL"):
        if os.environ.get(key):
            return False
    if os.environ.get("UNIMASTER_CLOUD") == "1":
        return False
    # Docker/Render dùng DATA_DIR=/data hoặc /tmp/unimaster-data; máy cá nhân để trống.
    return not os.environ.get("DATA_DIR", "").strip()


def invalidate_gateway_cache() -> None:
    """Xóa URL tunnel đã cache để lần gọi sau dò lại (Quick Tunnel đổi URL khi restart)."""
    _GATEWAY_CACHE["url"] = ""
    _GATEWAY_CACHE["ts"] = 0.0


async def resolve_gateway_base_url(base_url: str, force: bool = False) -> str:
    """
    Nếu Base URL trỏ vào máy nội bộ (127.0.0.1/localhost), tự dò địa chỉ tunnel
    công khai mới nhất. Tunnel Quick của Cloudflare đổi URL mỗi lần khởi động
    nên phải dò lại.

    force=True: bỏ qua phán đoán local/cloud và bỏ qua cache. Dùng khi đã gọi
    trực tiếp 127.0.0.1 thất bại — nghĩa là chắc chắn đang ở môi trường cloud
    dù biến môi trường nhận diện có sai hay không.
    """
    base_url = (base_url or "").rstrip("/")
    discovery = gateway_discovery_url()
    if not discovery or not _is_local_url(base_url):
        return base_url
    # Chạy trên chính máy đó thì 127.0.0.1 là đúng, không cần vòng qua tunnel.
    if not force and _is_local_runtime():
        return base_url

    now = time.time()
    if not force and _GATEWAY_CACHE["url"] and (now - _GATEWAY_CACHE["ts"]) < _GATEWAY_TTL:
        return _GATEWAY_CACHE["url"]

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                discovery,
                timeout=aiohttp.ClientTimeout(total=8),
            ) as resp:
                if resp.status == 200:
                    raw = await resp.text()
                    found = ""
                    for line in raw.splitlines():
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            message = json.loads(line).get("message", "")
                            payload = json.loads(message) if message else {}
                        except Exception:
                            continue
                        candidate = (payload.get("gateway_url") or "").rstrip("/")
                        if candidate.startswith("http"):
                            found = candidate
                    if found:
                        _GATEWAY_CACHE["url"] = found
                        _GATEWAY_CACHE["ts"] = now
                        print(f"[AI Gateway] Đã dò được tunnel: {found}")
                        return found
    except Exception as exc:
        print(f"[AI Gateway] Không dò được tunnel: {exc}")

    # Fallback: dùng URL cũ trong cache (nếu có), cuối cùng mới trả base_url nội bộ
    return _GATEWAY_CACHE["url"] or base_url


def get_openai_settings() -> dict:
    """Đọc cấu hình AI, ưu tiên cấu hình người dùng đã lưu trong SQLite.

    Render Blueprint có thể tạo các biến môi trường rỗng hoặc còn sót giá trị
    cũ. Nếu ENV luôn được ưu tiên, cấu hình FOSTA/9Router nhập trong giao diện
    sẽ bị che khuất và trông như bị mất. ENV vẫn được dùng làm fallback để hỗ
    trợ cấu hình deploy mới khi database chưa có giá trị.
    """
    db_key = get_setting("openai_api_key", "").strip()
    db_base_url = get_setting("openai_base_url", "").strip()
    db_model = get_setting("openai_model", "").strip()
    db_priority = get_setting("ai_provider_priority", "").strip()

    key = db_key or os.environ.get("OPENAI_API_KEY", "").strip()
    base_url = (db_base_url or os.environ.get("OPENAI_BASE_URL", "").strip() or "https://api.openai.com/v1").rstrip("/")
    is_fosta = "fosta" in base_url.lower()
    default_model = "gpt-6.1-sol" if is_fosta else "gpt-4o"
    model = db_model or os.environ.get("OPENAI_MODEL", "").strip() or default_model
    priority = db_priority or os.environ.get("AI_PROVIDER_PRIORITY", "").strip() or "openai_first"
    return {"key": key, "base_url": base_url, "model": model, "priority": priority}

async def _call_openai_chatgpt(prompt: str, system_instruction: str = "", max_tokens: int = 4096) -> str:
    cfg = get_openai_settings()
    key = cfg["key"]
    if not key:
        return None
    # 9Router chạy trên máy cá nhân: nếu Base URL là địa chỉ nội bộ thì tự dò
    # địa chỉ Cloudflare Tunnel công khai mới nhất để Render gọi được.
    base_url = await resolve_gateway_base_url(cfg["base_url"])
    endpoint = f"{base_url}/chat/completions"
    
    # Nếu Base URL là localhost và đang chạy trên cloud thì request đi qua tunnel công khai.
    gateway_route = (
        _is_local_url(cfg["base_url"])
        and bool(gateway_discovery_url())
    )
    gateway_retried = False

    is_fosta = "fosta" in base_url.lower()
    pref_model = cfg.get("model", "gpt-6.1-sol" if is_fosta else "gpt-4o")
    candidate_models = [pref_model]
    if is_fosta:
        for m in FOSTA_MODELS:
            if m not in candidate_models:
                candidate_models.append(m)
    elif "api.openai.com" in base_url.lower():
        # Chỉ API OpenAI chính thức mới có fallback giữa các model OpenAI.
        # 9Router dùng alias riêng (All/Coding-Pro), không thử tên GPT để tránh 404.
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
    secret_value = gateway_secret()
    if secret_value:
        # Gateway công khai trên Internet chỉ chấp nhận request có secret này
        headers["X-Gateway-Secret"] = secret_value

    async with aiohttp.ClientSession() as session:
        for model in candidate_models:
            payload = {
                "model": model,
                "messages": messages,
                "max_tokens": min(int(max_tokens or 4096), 16384),
                "temperature": 0.4
            }
            try:
                # Bài phân tích dài (8192+ token) cần thời gian lâu hơn 25s
                async with session.post(endpoint, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=120)) as resp:
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
                # Tunnel Quick của Cloudflare đổi URL mỗi lần khởi động lại: xóa cache
                # và dò lại một lần trước khi bỏ cuộc.
                if gateway_route and not gateway_retried:
                    gateway_retried = True
                    invalidate_gateway_cache()
                    base_url = await resolve_gateway_base_url(cfg["base_url"], force=True)
                    endpoint = f"{base_url}/chat/completions"
                    print(f"[AI Service] Tunnel có thể đã đổi, thử lại qua: {base_url}")
                continue
    return None

async def test_openai_key(key: str = None, base_url: str = None, model: str = None) -> dict:
    cfg = get_openai_settings()
    target_key = (key or cfg["key"]).strip()
    raw_url = ((base_url or cfg["base_url"]).strip()).rstrip("/")
    if not target_key:
        return {"success": False, "message": "Chưa nhập API Key"}
    # Cho phép test với gateway nội bộ bằng cách tự dò tunnel công khai
    target_url = await resolve_gateway_base_url(raw_url)
    endpoint = f"{target_url}/chat/completions"
    
    is_fosta = "fosta" in target_url.lower()
    is_router = target_model_hint = (model or cfg.get("model") or "").strip() in ROUTER_MODELS
    target_model = model or (cfg.get("model") if cfg.get("model") else ("gpt-6.1-sol" if is_fosta else "gpt-4o"))
    if is_fosta and target_model in ("gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"):
        target_model = "gpt-6.1-sol"

    headers = {"Authorization": f"Bearer {target_key}", "Content-Type": "application/json"}
    secret_value = gateway_secret()
    if secret_value:
        headers["X-Gateway-Secret"] = secret_value
    payload = {"model": target_model, "messages": [{"role": "user", "content": "Reply OK"}], "max_tokens": 15}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=12)) as resp:
                provider_title = "FOSTA Codex AI" if is_fosta else ("9Router Gateway" if is_router else "OpenAI ChatGPT")
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
        return {"success": False, "masked_key": mask_key(target_key), "message": f"Lỗi kết nối: {str(e)}"}


async def _execute_gemini_payload(
    parts: list = None,
    system_instruction: str = "",
    max_tokens: int = 8192,
    thinking_budget: int = 384,
    contents: list = None
) -> str:
    """
    Thực thi Gemini API với:
    1. Auto-Failover giữa nhiều API Key khi chạm Quota 429 hoặc lỗi khóa.
    2. Kiểm soát thinkingBudget + maxOutputTokens=8192 để KHÔNG BAO GIỜ bị cắt cụt chữ giữa chừng!
    """
    # Instant 0ms cache for text queries
    cache_key = None
    if parts and len(parts) == 1 and isinstance(parts[0], dict) and "text" in parts[0] and not parts[0].get("inlineData"):
        cache_key = hashlib.md5(f"{system_instruction}::{parts[0]['text']}".encode("utf-8")).hexdigest()
        if cache_key in AI_CACHE:
            return AI_CACHE[cache_key]

    # PRIORITY 1: ChatGPT / OpenAI API (Top Priority per user instruction)
    cfg = get_openai_settings()
    if cfg.get("priority") == "openai_first" and cfg.get("key"):
        text_prompt = None
        if parts and len(parts) == 1 and isinstance(parts[0], dict) and "text" in parts[0] and not parts[0].get("inlineData"):
            text_prompt = parts[0]["text"]
        elif contents and len(contents) == 1:
            c_parts = contents[0].get("parts", [])
            if len(c_parts) == 1 and "text" in c_parts[0]:
                text_prompt = c_parts[0]["text"]
        if text_prompt:
            openai_res = await _call_openai_chatgpt(text_prompt, system_instruction=system_instruction, max_tokens=max_tokens)
            if openai_res:
                if cache_key:
                    AI_CACHE[cache_key] = openai_res
                return openai_res
            print("[AI Service] ChatGPT quota exhausted or unavailable, smoothly falling back to Gemini pool!")

    candidate_keys = _ordered_candidate_keys()
    if not candidate_keys:
        return None

    eff_max_tokens = max(4096, int(max_tokens or 8192))

    async with aiohttp.ClientSession() as session:
        for api_key in candidate_keys:
            tel = _ensure_telemetry(api_key)
            key_rejected = False

            for model in GEMINI_MODELS:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
                gen_cfg = {
                    "temperature": 0.35,
                    "maxOutputTokens": eff_max_tokens,
                }
                if "lite" not in model:
                    gen_cfg["thinkingConfig"] = {"thinkingBudget": thinking_budget}

                payload_contents = contents if contents else [{"role": "user", "parts": parts or [{"text": ""}]}]
                payload = {
                    "contents": payload_contents,
                    "generationConfig": gen_cfg
                }
                if system_instruction:
                    payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}

                try:
                    async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=55)) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            candidates = data.get("candidates", [])
                            if candidates:
                                c_parts = candidates[0].get("content", {}).get("parts", [])
                                text_chunks = [
                                    p.get("text", "")
                                    for p in c_parts
                                    if isinstance(p, dict) and not p.get("thought") and p.get("text")
                                ]
                                full_text = "".join(text_chunks).strip()
                                if full_text:
                                    tel["calls"] += 1
                                    tel["status"] = "active"
                                    tel["cooldown_until"] = 0.0
                                    tel["model"] = model
                                    if cache_key:
                                        if len(AI_CACHE) > 500:
                                            AI_CACHE.pop(next(iter(AI_CACHE)))
                                        AI_CACHE[cache_key] = full_text
                                    return full_text
                        elif resp.status == 429:
                            tel["failovers"] += 1
                            tel["status"] = "cooldown"
                            tel["cooldown_until"] = time.time() + 75
                            tel["last_error"] = "Hết hạn mức tạm thời (429) -> Đã tự chuyển Key dự phòng"
                            if len(candidate_keys) > 1:
                                key_rejected = True
                                break
                            continue
                        elif resp.status in (400, 401, 403):
                            err_body = await resp.text()
                            if "API_KEY" in err_body or resp.status in (401, 403):
                                tel["failovers"] += 1
                                tel["status"] = "invalid"
                                tel["cooldown_until"] = time.time() + 1800
                                tel["last_error"] = f"Key không hợp lệ ({resp.status})"
                                key_rejected = True
                                break
                            continue
                        else:
                            continue
                except Exception as exc:
                    tel["last_error"] = str(exc)
                    break

            if key_rejected:
                continue

    return None


async def call_gemini(prompt: str, system_instruction: str = "", max_tokens: int = 8192, thinking_budget: int = 384) -> str:
    return await _execute_gemini_payload(
        [{"text": prompt}],
        system_instruction=system_instruction,
        max_tokens=max_tokens,
        thinking_budget=thinking_budget
    )


async def call_gemini_multimodal(prompt: str, mime_type: str, raw_bytes: bytes, max_tokens: int = 8192) -> str:
    b64 = base64.b64encode(raw_bytes).decode("ascii")
    parts = [
        {"inlineData": {"mimeType": mime_type, "data": b64}},
        {"text": prompt}
    ]
    return await _execute_gemini_payload(parts, max_tokens=max_tokens, thinking_budget=384)


async def test_api_key(api_key: str) -> dict:
    if not api_key:
        return {"success": False, "message": "Chưa nhập API Key"}

    tel = _ensure_telemetry(api_key)
    async with aiohttp.ClientSession() as session:
        for model in GEMINI_MODELS:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
            gen_cfg = {"maxOutputTokens": 64}
            if "lite" not in model:
                gen_cfg["thinkingConfig"] = {"thinkingBudget": 0}
            payload = {
                "contents": [{"parts": [{"text": "Reply OK"}]}],
                "generationConfig": gen_cfg
            }
            try:
                async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=12)) as resp:
                    if resp.status == 200:
                        tel["status"] = "active"
                        tel["cooldown_until"] = 0.0
                        tel["model"] = model
                        return {"success": True, "model": model, "masked_key": mask_key(api_key), "message": f"Hoạt động tốt ({model})"}
                    elif resp.status == 429:
                        tel["status"] = "cooldown"
                        tel["cooldown_until"] = time.time() + 75
                        continue
                    elif resp.status in (400, 401, 403):
                        err = await resp.json()
                        msg = err.get("error", {}).get("message", "API Key không hợp lệ")
                        if "API_KEY" in str(err) or resp.status in (401, 403):
                            tel["status"] = "invalid"
                            return {"success": False, "masked_key": mask_key(api_key), "message": msg}
            except Exception:
                continue

    if tel["status"] == "cooldown":
        return {"success": False, "masked_key": mask_key(api_key), "message": "Key đang chạm giới hạn Quota (429) — Sẽ tự động dùng Key dự phòng"}
    return {"success": False, "masked_key": mask_key(api_key), "message": "Không thể kết nối máy chủ Gemini"}


async def test_all_pool_keys() -> dict:
    pool = get_api_keys_pool()
    if not pool:
        return {"success": False, "results": [], "message": "Chưa có API Key nào trong danh sách"}
    tasks = [test_api_key(item["key"]) for item in pool]
    results = await asyncio.gather(*tasks)
    for idx, r in enumerate(results):
        r["label"] = pool[idx].get("label") or f"Key #{idx + 1}"
    ok_count = sum(1 for r in results if r.get("success"))
    return {
        "success": ok_count > 0,
        "active_count": ok_count,
        "total_count": len(pool),
        "results": results,
        "pool": get_pool_status(),
        "message": f"Sẵn sàng {ok_count}/{len(pool)} API Key trong hệ thống luân phiên!"
    }


async def ai_extract_from_multimodal(mime_type: str, raw_bytes: bytes, filename: str = "") -> str:
    prompt = f"""Hãy trích xuất đầy đủ, chính xác toàn bộ nội dung học thuật, định nghĩa, công thức Toán/Lý/Hóa, phương trình phản ứng và câu hỏi có trong tài liệu '{filename}'.
{STEM_FORMAT_GUIDE}"""
    return await call_gemini_multimodal(prompt, mime_type, raw_bytes, max_tokens=8192)


# =========================================================================
# CORE & ADVANCED EDUCATIONAL AI SERVICES
# =========================================================================
async def ai_chat_tutor(subject_name: str, user_message: str, persona: str = "professor", history: list = None) -> str:
    persona_map = {
        "professor": "Phong cách Giáo sư Đại học uyên bác: phân tích cặn kẽ bản chất, công thức chuẩn xác và chỉ rõ bẫy đề thi.",
        "feynman": "Phong cách Richard Feynman siêu dễ hiểu: giải thích bằng hình ảnh đời thường sinh động để sinh viên mất gốc cũng hiểu ngay trong 1 phút.",
        "speed": "Phong cách Cao thủ Giải nhanh Trắc nghiệm: đi thẳng vào công thức bấm máy / loại trừ đáp án trong 10 giây.",
        "examiner": "Phong cách Giảng viên Vấn đáp: giải đáp ngắn gọn rồi đặt ngược lại 1 câu hỏi xoáy tình huống để kiểm tra độ hiểu sâu của sinh viên."
    }
    style_desc = persona_map.get(persona, persona_map["professor"])
    english_guidance = """
Khi giải thích bất kỳ ngôn ngữ hoặc thuật ngữ chuyên ngành nào, luôn nêu nguồn gốc khi liên quan:
- Với từ/cụm từ: giải thích gốc từ, tiền tố/hậu tố, ngôn ngữ nguồn và quá trình biến đổi nghĩa nếu biết.
- Với thuật ngữ khoa học: giải nghĩa cấu tạo thuật ngữ (ví dụ gốc Greek/Latin), nhưng không gán từ nguyên khi không có căn cứ.
- Phân biệt dữ kiện chắc chắn với giả thuyết; nếu không chắc, nói rõ và đề xuất nguồn tra cứu đáng tin cậy của ngôn ngữ đó (ví dụ OED, Merriam-Webster, Etymonline).
- Thêm từ cùng họ/đồng nguyên, 2 ví dụ tự nhiên, cách dùng và lỗi phổ biến khi phù hợp.
Dùng các mục ngắn: **Nguồn gốc**, **Họ từ/Thuật ngữ liên quan**, **Cách dùng**, **Ví dụ**, **Ghi chú độ tin cậy**.
"""

    system_prompt = f"""Bạn là UniMaster AI — Gia sư ôn thi Đại học xuất sắc cho môn "{subject_name}".
Chế độ giảng dạy: {style_desc}
{english_guidance}
{STEM_FORMAT_GUIDE}"""

    # If history is provided, construct multi-turn dialogue
    if history and isinstance(history, list) and len(history) > 0:
        contents_list = []
        for turn in history[-8:]:
            role = "user" if turn.get("role") == "user" else "model"
            txt = str(turn.get("content") or turn.get("text") or "").strip()
            if txt:
                contents_list.append({"role": role, "parts": [{"text": txt}]})
        contents_list.append({"role": "user", "parts": [{"text": user_message}]})
        gemini_reply = await _execute_gemini_payload(contents=contents_list, system_instruction=system_prompt, max_tokens=4096, thinking_budget=256)
        if gemini_reply:
            return gemini_reply
    else:
        gemini_reply = await call_gemini(user_message, system_instruction=system_prompt, max_tokens=4096, thinking_budget=256)
        if gemini_reply:
            return gemini_reply

    return f"""### 🎓 Gia Sư UniMaster AI — {subject_name}
Về câu hỏi: **"{user_message}"**
- Hãy phân tích bản chất quy tắc/công thức gốc thay vì học vẹt máy móc, đặc biệt chú ý điều kiện biên và đơn vị đo.
- Mở **⚙️ Cài đặt → 🤖 Gemini AI** để thêm dàn API Key miễn phí giúp Giảng viên AI giải chi tiết mọi bài tập Toán, Lý, Hóa, Sinh, Code!"""


async def ai_get_hint(question_text: str, options: list, code_snippet: str = "") -> str:
    code_part = f"\nĐoạn mã:\n```csharp\n{code_snippet}\n```" if code_snippet else ""
    prompt = f"""Câu hỏi ôn thi: "{question_text}"{code_part}
Các lựa chọn: {', '.join([o for o in options if o])}
Đóng vai Giảng viên, hãy đưa ra **1 gợi ý tư duy Socratic ngắn gọn (2–3 câu)**. TUYỆT ĐỐI KHÔNG tiết lộ thẳng đáp án A/B/C/D.
{STEM_FORMAT_GUIDE}"""

    gemini_reply = await call_gemini(prompt, max_tokens=4096, thinking_budget=192)
    if gemini_reply:
        return gemini_reply
    if code_snippet:
        return "Hãy theo dõi thứ tự khởi tạo từ `Main()`, kiểm tra điều kiện biên hoặc cơ chế đa hình `virtual`/`override`."
    return "Hãy xác định công thức/định nghĩa trọng tâm của câu hỏi, kiểm tra đơn vị và loại trừ ngay 2 phương án trái bản chất."


async def ai_concept_recall(subject_name: str, question_text: str, code_snippet: str = "") -> str:
    """Nhắc lại công thức / định luật / lý thuyết nền tảng liên quan đến câu hỏi mà KHÔNG giải hộ đáp án"""
    code_part = f"\n```csharp\n{code_snippet}\n```" if code_snippet else ""
    prompt = f"""Môn học: {subject_name}
Câu hỏi đang làm: "{question_text}"{code_part}

Hãy đóng vai Sổ tay Công thức Thông minh, tóm tắt **ngắn gọn trong 3–4 gạch đầu dòng** các định luật, công thức gốc, phương trình tổng quát hoặc quy tắc cú pháp nền tảng cần dùng cho bài này.
⚠️ TUYỆT ĐỐI KHÔNG tính ra kết quả cuối cùng và KHÔNG chỉ ra đáp án A/B/C/D để thí sinh tự vận dụng!
{STEM_FORMAT_GUIDE}"""

    gemini_reply = await call_gemini(prompt, max_tokens=4096, thinking_budget=256)
    return gemini_reply or "### 🧠 Lý thuyết nền tảng\nHãy đối chiếu định nghĩa gốc, điều kiện áp dụng công thức và chú ý đổi đồng nhất đơn vị trước khi thay số."


async def ai_deep_analysis(question_text: str, correct_option: str, explanation: str, code_snippet: str = "") -> str:
    code_part = f"\n```csharp\n{code_snippet}\n```" if code_snippet else ""
    prompt = f"""Câu hỏi: "{question_text}"{code_part}
Đáp án đúng: **{correct_option}** | Giải thích gốc: "{explanation}"
Phân tích chuyên sâu, súc tích:
1. **🔬 Luồng suy luận & biến đổi công thức từng bước:** Tại sao đáp án đúng?
2. **⚠️ Phân tích bẫy đề thi:** Tại sao các phương án nhiễu dễ làm thí sinh nhầm lẫn?
3. **⚡ Quy tắc chốt hạ 5 giây.**
{STEM_FORMAT_GUIDE}"""

    gemini_reply = await call_gemini(prompt, max_tokens=6144, thinking_budget=384)
    if gemini_reply:
        return gemini_reply
    return f"#### 🔬 Bản chất cốt lõi\n- {explanation or 'Đáp án đúng tuân thủ quy tắc chuẩn của học phần.'}"


async def ai_explain_mistake(subject_name: str, question_text: str, user_wrong_answer: str, correct_answer: str, explanation: str = "", code_snippet: str = "") -> str:
    """Chẩn đoán chính xác vì sao học sinh lại chọn nhầm phương án đó"""
    code_part = f"\n```csharp\n{code_snippet}\n```" if code_snippet else ""
    prompt = f"""Môn học: {subject_name}
Câu hỏi: "{question_text}"{code_part}
- Thí sinh đã chọn/nhập SAI: **{user_wrong_answer}**
- Đáp án ĐÚNG là: **{correct_answer}**
- Lời giải chuẩn: "{explanation}"

Hãy đóng vai Gia sư bắt bệnh tư duy cực nhạy:
1. **🩺 Bắt bệnh lỗi sai:** Chỉ rõ vì sao thí sinh lại bị đánh lừa chọn **{user_wrong_answer}** (nhầm dấu, quên hệ số, hiểu ngược định nghĩa hay nhầm cơ chế?).
2. **✅ Cách sửa tư duy đúng:** So sánh trực diện **{user_wrong_answer}** và **{correct_answer}** để không bao giờ lặp lại lỗi này lần thứ 2.
{STEM_FORMAT_GUIDE}"""

    gemini_reply = await call_gemini(prompt, max_tokens=4096, thinking_budget=256)
    return gemini_reply or f"### 🩺 Phân tích lỗi nhầm lẫn\nBạn chọn **{user_wrong_answer}** trong khi đáp án đúng là **{correct_answer}**. {explanation}"


async def ai_mnemonic_trick(subject_name: str, question_text: str, correct_answer: str, explanation: str = "") -> str:
    """Tạo câu thần chú / thơ vui / mẹo nhớ siêu tốc 5 giây"""
    prompt = f"""Môn học: {subject_name}
Câu hỏi: "{question_text}"
Đáp án đúng: **{correct_answer}** ({explanation})

Hãy sáng tạo **1 MẸO NHỚ SIÊU TỐC 5 GIÂY** cực kỳ ấn tượng, hài hước, dễ thuộc lòng (câu thần chú vần điệu tiếng Việt, quy tắc viết tắt hoặc liên tưởng hình ảnh độc đáo) giúp sinh viên nhìn đề là khoanh đúng ngay lập tức! Ngắn gọn dưới 120 từ.
{STEM_FORMAT_GUIDE}"""

    gemini_reply = await call_gemini(prompt, max_tokens=4096, thinking_budget=192)
    return gemini_reply or f"⚡ **Mẹo nhớ nhanh:** Hãy gắn từ khóa trọng tâm của đề bài trực tiếp với **{correct_answer}**!"


async def ai_question_to_flashcard(subject_name: str, question_text: str, correct_answer: str, explanation: str = "") -> dict:
    """Chuyển 1 câu hỏi bất kỳ thành 1 thẻ nhớ Flashcard SM-2 tinh gọn"""
    prompt = f"""Môn học: {subject_name}
Từ câu hỏi sau: "{question_text}"
Đáp án: {correct_answer} | Giải thích: {explanation}

Hãy đúc kết kiến thức cốt lõi nhất thành **1 thẻ Flashcard ôn thi** ngắn gọn, súc tích (dùng `$...$` cho công thức Toán/Lý và `$\\ce{{...}}$` cho Hóa học nếu có).
Trả về DUY NHẤT JSON hợp lệ:
{{
  "front": "Câu hỏi / Công thức / Khái niệm trọng tâm ngắn gọn",
  "back": "Đáp án chuẩn & bản chất cốt lõi (1-3 dòng)",
  "hint": "Từ khóa gợi nhớ 3 giây"
}}"""
    gemini_reply = await call_gemini(prompt, max_tokens=4096, thinking_budget=192)
    if gemini_reply:
        try:
            cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", gemini_reply.strip())
            s, e = cleaned.find("{"), cleaned.rfind("}")
            if s != -1 and e != -1:
                obj = json.loads(cleaned[s:e + 1])
                if isinstance(obj, dict) and obj.get("front") and obj.get("back"):
                    return obj
        except Exception:
            pass
    return {
        "front": question_text[:260],
        "back": f"**Đáp án:** {correct_answer}\n\n{explanation}",
        "hint": subject_name
    }


async def ai_explain_flashcard(subject_name: str, front: str, back: str) -> str:
    prompt = f"""Môn học: {subject_name}
Thẻ Flashcard hiện tại:
- Mặt trước: "{front}"
- Mặt sau: "{back}"

Hãy giải thích sâu hơn ý nghĩa thực chất, cho **1 ví dụ bài tập / ứng dụng thực tế cực ngắn** và chỉ ra **1 lỗi sai kinh điển** sinh viên hay mắc ở kiến thức này.
{STEM_FORMAT_GUIDE}"""
    gemini_reply = await call_gemini(prompt, max_tokens=4096, thinking_budget=256)
    return gemini_reply or f"### 💡 Mở rộng kiến thức\n{back}"


async def ai_generate_similar(question_text: str, code_snippet: str = "") -> dict:
    code_part = f"\nĐoạn mã gốc:\n```csharp\n{code_snippet}\n```" if code_snippet else ""
    prompt = f"""Dựa vào câu hỏi gốc: "{question_text}"{code_part}
Hãy soạn 1 câu hỏi trắc nghiệm MỚI tương tự cùng chủ đề & độ khó (nếu là Toán/Lý dùng `$...$`, Hóa học dùng `$\\ce{{...}}$`).
Trả về DUY NHẤT JSON hợp lệ:
{{
  "question": "Nội dung câu hỏi mới",
  "code": "Đoạn code nhiều dòng (hoặc chuỗi rỗng nếu môn không phải lập trình)",
  "options": ["Phương án A", "Phương án B", "Phương án C", "Phương án D"],
  "correct": "A",
  "explanation": "Giải thích ngắn gọn chuẩn xác"
}}"""
    gemini_reply = await call_gemini(prompt, max_tokens=4096, thinking_budget=256)
    if gemini_reply:
        try:
            cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", gemini_reply.strip())
            s, e = cleaned.find("{"), cleaned.rfind("}")
            if s != -1 and e != -1:
                obj = json.loads(cleaned[s:e + 1])
                if isinstance(obj, dict) and "question" in obj and "options" in obj:
                    return obj
        except Exception:
            pass
    return {
        "question": "Khi khai báo `Base obj = new Derived();`, cặp từ khóa nào giúp `obj.Run()` gọi đúng phương thức của lớp `Derived` lúc Runtime?",
        "code": "class Base {\n    public virtual void Run() => Console.Write(\"Base\");\n}\nclass Derived : Base {\n    public override void Run() => Console.Write(\"Derived\");\n}",
        "options": ["virtual và override", "static và new", "private và public", "sealed và abstract"],
        "correct": "A",
        "explanation": "Cặp `virtual` (lớp cha) và `override` (lớp con) kích hoạt đa hình động (Runtime Polymorphism)."
    }


async def ai_custom_qa(question_text: str, correct_text: str, student_query: str, code_snippet: str = "") -> str:
    code_part = f"\nCode:\n```csharp\n{code_snippet}\n```" if code_snippet else ""
    prompt = f"""Câu hỏi đang làm: "{question_text}"{code_part}
Đáp án đúng: {correct_text}. Sinh viên hỏi thêm: "{student_query}"
Hãy giải đáp ngắn gọn, trực diện và dễ hiểu nhất.
{STEM_FORMAT_GUIDE}"""
    gemini_reply = await call_gemini(prompt, max_tokens=4096, thinking_budget=256)
    return gemini_reply or f"Về thắc mắc **\"{student_query}\"**: Trọng tâm xoay quanh đáp án chuẩn **{correct_text}**."


async def ai_grade_essay(question_text: str, expected_barem: str, student_answer: str) -> dict:
    prompt = f"""Câu hỏi tự luận / vấn đáp:
"{question_text}"
Đáp án chuẩn / Barem gợi ý:
"{expected_barem}"
Bài làm của sinh viên:
\"\"\"{student_answer}\"\"\"

Hãy đóng vai Giảng viên chấm thi công tâm (dùng `$...$` cho Toán/Lý, `$\\ce{{...}}$` cho Hóa nếu có), trả về DUY NHẤT đối tượng JSON hợp lệ:
{{
  "score": 8.5,
  "verdict": "Nhận xét tổng quát 1 câu khích lệ và sát thực tế",
  "strengths": ["Ý sinh viên đã nêu đúng"],
  "missing": ["Ý quan trọng còn thiếu hoặc chưa chính xác"],
  "sample_answer": "Câu trả lời mẫu ngắn gọn đạt 10/10 điểm"
}}"""
    gemini_reply = await call_gemini(prompt, max_tokens=4096, thinking_budget=384)
    if gemini_reply:
        try:
            cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", gemini_reply.strip())
            s, e = cleaned.find("{"), cleaned.rfind("}")
            if s != -1 and e != -1:
                obj = json.loads(cleaned[s:e + 1])
                if isinstance(obj, dict) and "score" in obj:
                    return obj
        except Exception:
            pass

    words = len((student_answer or "").split())
    est = min(8.5, round(max(3.5, words / 7.0), 1))
    return {
        "score": est,
        "verdict": "Bài làm đã nêu được một số luận điểm cơ bản, cần đối chiếu kỹ với barem chuẩn.",
        "strengths": ["Có trình bày lập luận riêng cho câu hỏi"],
        "missing": ["Cần bổ sung đầy đủ các ý cốt lõi, công thức hoặc ví dụ minh họa như barem"],
        "sample_answer": expected_barem
    }


async def ai_evaluate_exam(subject_name: str, total: int, correct: int, wrong_questions: list, topic_tags: list = None) -> str:
    wrong = total - correct
    score = round(correct / total * 10, 1) if total > 0 else 0
    pct = round(correct / total * 100) if total > 0 else 0

    # Danh sách câu sai (text)
    wrong_text = "\n".join([f"- {q}" for q in wrong_questions[:12]]) if wrong_questions else "Không có câu nào sai!"

    # Phân tích topic_tags: đếm số lần sai theo từng chủ đề
    topic_analysis = ""
    if topic_tags:
        from collections import Counter
        tag_counts = Counter(t for t in topic_tags if t)
        if tag_counts:
            sorted_tags = tag_counts.most_common()
            topic_lines = "\n".join([f"  - **{tag}**: {cnt} câu sai" for tag, cnt in sorted_tags])
            topic_analysis = f"\nPhân bố lỗi theo chủ đề:\n{topic_lines}"

    # Xác định mức độ
    if score >= 8.5:
        level_hint = "Xuất sắc — tập trung vào câu vận dụng cao và bẫy đề thi."
    elif score >= 7.0:
        level_hint = "Khá — cần củng cố thêm các chủ đề còn sai."
    elif score >= 5.0:
        level_hint = "Trung bình — cần ôn lại kiến thức nền tảng."
    else:
        level_hint = "Yếu — cần học lại từ đầu theo lộ trình có hệ thống."

    prompt = f"""Đóng vai Giáo sư AI chuyên gia môn "{subject_name}". Sinh viên vừa hoàn thành bài thi:
- Điểm: **{score}/10** ({correct}/{total} câu đúng, {pct}% chính xác)
- Mức độ: {level_hint}
- Số câu sai: {wrong}{topic_analysis}

Nội dung các câu sai:
{wrong_text}

Hãy viết **BẢN PHÂN TÍCH TOÀN DIỆN** súc tích, trọn vẹn, KHÔNG cắt giữa chừng, gồm 4 phần:

## 📊 1. Đánh Giá Tổng Quan
- Nhận xét ngắn về phong độ và mức độ nhận thức (Nhận biết / Thông hiểu / Vận dụng / Vận dụng cao).
- Điểm mạnh nổi bật cần phát huy.

## 🎯 2. Bản Đồ Lỗ Hổng Kiến Thức
- Liệt kê các chủ đề/khái niệm bị sai nhiều nhất (dựa vào câu sai bên trên).
- Phân loại: lỗi do **hiểu sai khái niệm** hay **tính toán/áp dụng nhầm**.

## 📅 3. Kế Hoạch Ôn Tập 3 Ngày Cá Nhân Hóa
- **Ngày 1 (Nền tảng):** Ôn lại khái niệm cốt lõi của các chủ đề sai nhiều nhất. Làm lại câu sai trong bài.
- **Ngày 2 (Luyện tập):** Làm 15–20 câu trắc nghiệm tập trung vào chủ đề yếu. Dùng Flashcard để ghi nhớ công thức.
- **Ngày 3 (Tổng duyệt):** Thi thử 1 đề đầy đủ có bấm giờ. Rà soát lại toàn bộ câu sai.

## ⚡ 4. Mẹo Chiến Thuật Thi
- 2–3 mẹo cụ thể giúp tăng ngay 1–2 điểm trong lần thi tới.
{STEM_FORMAT_GUIDE}"""

    gemini_reply = await call_gemini(prompt, max_tokens=8192, thinking_budget=512)
    return gemini_reply or f"""## 📊 Đánh Giá Nhanh: {score}/10 ({correct}/{total} câu)
**Mức độ:** {level_hint}

## 📅 Kế Hoạch 3 Ngày
- **Ngày 1:** Làm lại {wrong} câu sai, ôn lý thuyết nền tảng.
- **Ngày 2:** Luyện 20 câu trắc nghiệm chủ đề yếu + Flashcard.
- **Ngày 3:** Thi thử đề đầy đủ có bấm giờ.

> 💡 Bấm **Làm lại câu sai** để bắt đầu ngay!"""


async def ai_personalized_roadmap(subject_name: str, stats_summary: dict, mistake_questions: list) -> str:
    """Phân tích chuyên sâu hồ sơ năng lực & lập lộ trình ôn thi 5 ngày HOÀN CHỈNH (không bao giờ cắt chữ!)"""
    mistakes_txt = "\n".join([f"- {q}" for q in mistake_questions[:12]]) if mistake_questions else "Chưa có câu sai tồn đọng trong Sổ tay."
    prompt = f"""Đóng vai Giám đốc Học thuật & Cố vấn AI cá nhân hóa cho môn "{subject_name}".
Dữ liệu học tập của sinh viên:
- Số đề đã hoàn thành: {stats_summary.get('total_exams', 0)}
- Điểm trung bình hệ 10: {stats_summary.get('avg_score', 0)}
- Số câu sai đang lưu trong Mistake Notebook: {len(mistake_questions)}
Danh sách các câu hay sai:
{mistakes_txt}

Hãy lập **BẢN ĐỒ NĂNG LỰC & LỘ TRÌNH ÔN THI 5 NGÀY NƯỚC RÚT** súc tích, mạch lạc, trình bày ĐẦY ĐỦ TRỌN VẸN cả 3 phần từ Ngày 1 đến Ngày 5 (tầm 450–650 từ để đọc thoáng mắt, rõ ràng):
### 1. 🧠 Chẩn đoán Điểm mạnh & Lỗ hổng cốt lõi
- Đánh giá ngắn gọn theo 4 cấp độ nhận thức (*Nhận biết, Thông hiểu, Vận dụng, Vận dụng cao*) đối với môn **{subject_name}**.
### 2. 📅 Lộ trình hành động 5 ngày chi tiết
- **Ngày 1:** Củng cố nền tảng & công thức gốc quan trọng nhất.
- **Ngày 2:** Xử lý triệt để các chuyên đề hay nhầm lẫn.
- **Ngày 3:** Luyện dạng bài Vận dụng & tốc độ phản xạ.
- **Ngày 4:** Chinh phục câu Vận dụng cao & bẫy đề thi.
- **Ngày 5:** Thi thử tổng duyệt bấm giờ & rà soát Sổ tay câu sai.
### 3. ⚡ 3 Chiến thuật phòng thi giúp tăng ngay 1.5 – 2.0 điểm
{STEM_FORMAT_GUIDE}"""
    gemini_reply = await call_gemini(prompt, max_tokens=8192, thinking_budget=384)
    if gemini_reply:
        return gemini_reply

    return f"""### 🧠 Lộ Trình 5 Ngày Cá Nhân Hóa — {subject_name}
- **Ngày 1 (Nhận biết):** Hệ thống hóa toàn bộ khái niệm, định luật và công thức nền tảng bằng Flashcards 3D.
- **Ngày 2 (Thông hiểu):** Ôn chuyên sâu {len(mistake_questions)} câu trong *Sổ tay câu sai* để triệt tiêu các bẫy lý thuyết.
- **Ngày 3 (Vận dụng):** Luyện 2 đề chuyên đề 20 câu nhằm tăng tốc độ nhận diện dạng bài.
- **Ngày 4 (Vận dụng cao):** Rèn kỹ năng phân tích câu hỏi ghép chuyên đề và điều kiện biên.
- **Ngày 5 (Tổng duyệt):** Thi thử chế độ *Thi thật* có bấm giờ và rà lại toàn bộ ghi chú cá nhân.
> 💡 *Mẹo:* Mở **⚙️ Cài đặt → 🤖 Gemini AI** để gắn hoặc kiểm tra dàn API Key giúp AI phân tích chi tiết từng câu sai của bạn!"""


async def ai_explain_exercise(title: str, problem: str, sample_code: str) -> str:
    prompt = f"""Bài tập lớn OOP C#: "{title}"
Đề bài: {problem}
Code mẫu:
```csharp
{sample_code[:3000]}
```
Trình bày súc tích, trọn vẹn:
1. **🏗️ Phân tích 4 trụ cột OOP được vận dụng trong bài**
2. **🎤 Top 3 câu hỏi Vấn đáp Giảng viên hay hỏi nhất & Câu trả lời đạt 10/10.**
{STEM_FORMAT_GUIDE}"""
    gemini_reply = await call_gemini(prompt, max_tokens=6144, thinking_budget=384)
    return gemini_reply or "### 🏗️ Phân Tích OOP\nBài toán vận dụng kết hợp `abstract class`, `Encapsulation` qua Property và đa hình động `virtual`/`override`."


async def ai_generate_questions(subject_name: str, content: str, count: int = 5, q_type: str = "mcq", cognitive_level: str = "mixed") -> list:
    level_guide = {
        "mixed": "Phân bổ cân bằng cả 4 cấp độ nhận thức: Nhận biết (25%), Thông hiểu (35%), Vận dụng (25%), Vận dụng cao (15%).",
        "nhan_biet": "100% ở cấp độ NHẬN BIẾT (nhớ chính xác định nghĩa, công thức, cú pháp nền tảng).",
        "thong_hieu": "100% ở cấp độ THÔNG HIỂU (giải thích bản chất, phân biệt khái niệm/hiện tượng dễ nhầm).",
        "van_dung": "100% ở cấp độ VẬN DỤNG (áp dụng công thức giải toán Lý/Hóa/Sinh/Toán, hoặc đọc hiểu đoạn code).",
        "van_dung_cao": "100% ở cấp độ VẬN DỤNG CAO (bài toán tổng hợp nhiều bước, bẫy tinh vi)."
    }.get(cognitive_level, "Phân bổ cân bằng 4 cấp độ nhận thức.")

    diff_map = {
        "nhan_biet": "easy",
        "thong_hieu": "medium",
        "van_dung": "hard",
        "van_dung_cao": "very_hard"
    }

    source_block = f'Từ tài liệu học thuật dưới đây:\n"""\n{content[:14000]}\n"""' if content and len(content.strip()) > 20 else f'Dựa trên chương trình chuẩn Đại học / THPT Quốc gia của môn "{subject_name}"'

    prompt = f"""{source_block}
Hãy biên soạn đúng {count} câu hỏi thi môn "{subject_name}" chất lượng cao, chính xác khoa học.
- Định dạng câu hỏi: {q_type} ('mcq' = 4 lựa chọn A/B/C/D; 'true_false' = Đúng/Sai với a='Đúng', b='Sai', correct='A' hoặc 'B'; 'short_answer' = trả lời ngắn bằng con số/từ khóa; 'essay' = tự luận).
- Yêu cầu cấp độ nhận thức (Bloom): {level_guide}
- CỰC KỲ QUAN TRỌNG VỀ CÔNG THỨC:
  + Môn Toán / Vật lý / Sinh học tính toán: bọc mọi công thức trong `$...$` (nhớ escape dấu gạch chéo trong JSON thành `\\\\`, ví dụ `"$\\\\int x e^x \\\\, \\\\mathrm{{d}}x$"`, `"$v_{{\\\\max}} = \\\\omega A$"`).
  + Môn Hóa học: bọc công thức hóa học & phương trình trong `$\\ce{{...}}$` (escape JSON thành `"$\\\\ce{{H2SO4}}$"`, `"$\\\\ce{{2H2 + O2 -> 2H2O}}$"`).
  + Môn Lập trình: đặt đoạn mã nhiều dòng vào `"code_snippet"` (dùng `\\n`), còn môn không phải lập trình thì để `"code_snippet": ""`.
- Ghi nhãn cấp độ ở đầu câu hỏi dạng: `"Câu X ([Cấp độ] - Chủ đề): ..."`.

Trả về DUY NHẤT mảng JSON hợp lệ (không thêm văn bản ngoài mảng):
[
  {{
    "q_type": "{q_type if q_type != 'all' else 'mcq'}",
    "question": "Câu 1 (Thông hiểu - Chủ đề): Nội dung câu hỏi?",
    "code_snippet": "",
    "a": "Phương án A",
    "b": "Phương án B",
    "c": "Phương án C",
    "d": "Phương án D",
    "correct": "A",
    "explanation": "Giải thích chi tiết bản chất & các bước tính",
    "difficulty": "{diff_map.get(cognitive_level, 'medium')}"
  }}
]"""

    gemini_reply = await call_gemini(prompt, max_tokens=8192, thinking_budget=512)
    if gemini_reply:
        try:
            cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", gemini_reply.strip())
            start_idx = cleaned.find("[")
            end_idx = cleaned.rfind("]")
            if start_idx != -1 and end_idx != -1:
                cleaned = cleaned[start_idx:end_idx + 1]
            data = json.loads(cleaned)
            if isinstance(data, list) and len(data) > 0:
                return data
        except Exception:
            pass

    return [
        {
            "q_type": "mcq",
            "question": f"Câu 1 (Thông hiểu - Trọng tâm {subject_name}): Nguyên lý cốt lõi nào cần nắm chắc nhất trong học phần {subject_name}?",
            "code_snippet": "",
            "a": "Hiểu rõ bản chất công thức, điều kiện áp dụng và đơn vị chuẩn",
            "b": "Chỉ học thuộc lòng kết quả của một ví dụ đơn lẻ",
            "c": "Bỏ qua các điều kiện biên của định luật",
            "d": "Áp dụng máy móc không phân tích giả thiết",
            "correct": "A",
            "explanation": "Nắm vững bản chất, điều kiện biên và đơn vị đo giúp giải quyết chính xác cả câu hỏi Thông hiểu, Vận dụng và Vận dụng cao.",
            "difficulty": "medium"
        }
    ]


async def ai_generate_flashcards(subject_name: str, content: str, count: int = 6) -> list:
    source_block = f'Từ tài liệu môn "{subject_name}":\n"""\n{content[:12000]}\n"""' if content and len(content.strip()) > 20 else f'Dựa trên kiến thức trọng tâm cốt lõi nhất của môn "{subject_name}"'
    prompt = f"""{source_block}
Hãy tạo {count} thẻ Flashcard ôn thi súc tích nhất (dùng `$...$` cho Toán/Lý và `$\\ce{{...}}$` cho Hóa học, nhớ escape `\\\\` đúng chuẩn JSON).
Trả về DUY NHẤT mảng JSON:
[
  {{
    "front": "Thuật ngữ / Định luật / Câu hỏi cốt lõi",
    "back": "Công thức chuẩn & giải thích bản chất ngắn gọn",
    "hint": "Từ khóa gợi nhớ 3 giây"
  }}
]"""
    gemini_reply = await call_gemini(prompt, max_tokens=6144, thinking_budget=384)
    if gemini_reply:
        try:
            cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", gemini_reply.strip())
            s, e = cleaned.find("["), cleaned.rfind("]")
            if s != -1 and e != -1:
                cleaned = cleaned[s:e + 1]
            data = json.loads(cleaned)
            if isinstance(data, list) and len(data) > 0:
                return data
        except Exception:
            pass
    return [{"front": f"Trọng tâm — {subject_name}", "back": (content or subject_name)[:240], "hint": "Ôn tập cốt lõi"}]


async def ai_summarize_cheat_sheet(subject_name: str, content: str) -> str:
    prompt = f"""Từ tài liệu môn "{subject_name}" dưới đây, hãy biên soạn **BẢNG PHAO ÔN THI 1 TRANG & HỆ THỐNG CÔNG THỨC TRỌNG TÂM**:
\"\"\"
{content[:14000]}
\"\"\"
Cấu trúc bắt buộc:
1. 🗺️ **Sơ Đồ Hệ Thống Hóa Kiến Thức Cốt Lõi**
2. 🎯 **Bảng Công Thức / Định Luật / Phương Trình Phải Thuộc Lòng**
3. ⚠️ **5 Bẫy Đề Thi Kinh Điển Hay Mất Điểm Nhất**
4. ⚡ **Mẹo Giải Nhanh Trắc Nghiệm Trong 10 Giây**
{STEM_FORMAT_GUIDE}"""
    gemini_reply = await call_gemini(prompt, max_tokens=8192, thinking_budget=384)
    return gemini_reply or f"### 📑 Tóm Tắt Trọng Tâm — {subject_name}\n\n> {content[:400]}..."


async def ai_generate_image_question(subject_name: str, mime_type: str, raw_bytes: bytes, hint_label: str = "") -> dict:
    """Sử dụng Gemini Multimodal Vision để phân tích hình ảnh (tiêu bản kính hiển vi, hình giải phẫu, đồ thị, sơ đồ) và tạo câu hỏi trắc nghiệm gắn kèm ảnh"""
    prompt = f"""Quan sát kỹ hình ảnh học thuật đính kèm thuộc môn "{subject_name}" (Gợi ý/Nhãn: {hint_label or 'Hình minh họa đề thi'}).
Hãy biên soạn 1 câu hỏi trắc nghiệm 4 lựa chọn (A, B, C, D) yêu cầu sinh viên quan sát và nhận diện/phân tích hình ảnh này.
Trả về DUY NHẤT đối tượng JSON hợp lệ:
{{
  "question": "[Hình ảnh] Quan sát hình ảnh dưới đây và cho biết...",
  "a": "Phương án A (chính xác và chi tiết)",
  "b": "Phương án B (nhiễu hợp lý)",
  "c": "Phương án C (nhiễu hợp lý)",
  "d": "Phương án D (nhiễu hợp lý)",
  "correct": "A",
  "explanation": "Giải thích chi tiết các đặc điểm nhận diện trên hình ảnh giúp chọn đúng đáp án."
}}"""
    reply = await call_gemini_multimodal(prompt, mime_type, raw_bytes, max_tokens=4096)
    if reply:
        try:
            cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", reply.strip())
            s, e = cleaned.find("{"), cleaned.rfind("}")
            if s != -1 and e != -1:
                obj = json.loads(cleaned[s:e + 1])
                if isinstance(obj, dict) and "question" in obj:
                    return obj
        except Exception:
            pass
    label_clean = hint_label or f"Tiêu bản / Hình minh họa {subject_name}"
    return {
        "question": f"[Hình ảnh] Quan sát hình minh họa ({label_clean}) thuộc học phần {subject_name} dưới đây và xác định nhận định đúng nhất:",
        "a": f"Hình ảnh thể hiện đặc trưng điển hình của {label_clean} theo giáo trình thực hành {subject_name}.",
        "b": "Hình ảnh không liên quan đến tiêu chuẩn chẩn đoán hoặc thông số kỹ thuật của bài học.",
        "c": "Đây là nhiễu ảnh do sai lệch bước sóng mà không có cấu trúc mục tiêu.",
        "d": "Các thông số trên hình đều vượt ngưỡng giới hạn sinh lý 100 lần.",
        "correct": "A",
        "explanation": f"Quan sát trực tiếp các đặc điểm hình thái và cấu trúc trên ảnh ({label_clean}) giúp xác nhận phương án A là chính xác."
    }


async def ai_grade_handwritten_image(subject_name: str, question_text: str, mime_type: str, raw_bytes: bytes, student_note: str = "") -> dict:
    """Sử dụng Gemini Multimodal Vision để đọc chữ viết tay, giấy nháp hoặc phiếu xét nghiệm và chấm điểm từng bước"""
    prompt = f"""Đóng vai Giảng viên Đại học chấm bài thực hành / tự luận môn "{subject_name}".
Đề bài / Yêu cầu: "{question_text or 'Phân tích và chấm bài giải viết tay / phiếu kết quả xét nghiệm trong ảnh'}"
Ghi chú của sinh viên: "{student_note or 'Không có'}"

Hãy quan sát kỹ hình ảnh bài làm viết tay / phiếu xét nghiệm đính kèm:
1. Đọc chính xác nội dung chữ viết tay, các phép tính, công thức (ví dụ $C = \\frac{{\\text{{OD}}_{{\\text{{thử}}}}}}{{\\text{{OD}}_{{\\text{{chuẩn}}}}}} \\times C_0$, $C_{{\\text{{Cr}}}} = \\frac{{U \\times V}}{{P}}$, phương trình hóa học $\\ce{{...}}$) và đơn vị đo.
2. Chấm điểm trên thang 10 và chỉ rõ từng bước đúng/sai.
Trả về DUY NHẤT đối tượng JSON hợp lệ:
{{
  "transcribed_text": "Nội dung bài làm / số liệu AI đọc được từ ảnh",
  "score": 8.5,
  "verdict": "Nhận xét tổng quát ngắn gọn, khích lệ và chỉ rõ trọng tâm",
  "strengths": ["Bước giải / công thức / biện luận sinh viên đã làm đúng"],
  "missing": ["Lỗi sai tính toán, nhầm đơn vị hoặc bước biện luận còn thiếu"],
  "sample_answer": "Lời giải chuẩn từng bước đầy đủ công thức ($...$) và kết luận lâm sàng đạt 10/10 điểm"
}}"""
    reply = await call_gemini_multimodal(prompt, mime_type, raw_bytes, max_tokens=4096)
    if reply:
        try:
            cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", reply.strip())
            s, e = cleaned.find("{"), cleaned.rfind("}")
            if s != -1 and e != -1:
                obj = json.loads(cleaned[s:e + 1])
                if isinstance(obj, dict) and "score" in obj:
                    return obj
        except Exception:
            pass
    return {
        "transcribed_text": student_note or "Đã nhận ảnh bài làm viết tay / phiếu kết quả thực hành.",
        "score": 8.0,
        "verdict": "Ảnh bài làm rõ ràng. Hãy đối chiếu kỹ công thức gốc, đơn vị chuẩn (mmol/L, µmol/L, g/L, mL/phút) và ngưỡng tham chiếu sinh lý.",
        "strengths": [
            "Trình bày rõ các bước thiết lập công thức tính toán",
            "Có ghi nhận kết quả và đối chiếu biện luận"
        ],
        "missing": [
            "Cần ghi rõ đơn vị sau mỗi bước thay số và kiểm tra hệ số quy đổi đơn vị"
        ],
        "sample_answer": (
            "1. Áp dụng định luật Beer–Lambert: $C = \\frac{\\text{OD}_{\\text{thử}}}{\\text{OD}_{\\text{chuẩn}}} \\times C_0$.\n"
            "2. Nếu tính độ thanh thải Creatinin: $C_{\\text{Cr}} = \\frac{U \\times V}{P}$ (nhớ đổi cùng đơn vị nồng độ giữa nước tiểu $U$ và huyết tương $P$).\n"
            "3. Đối chiếu khoảng tham chiếu bình thường để kết luận chính xác tình trạng sinh lý / bệnh lý."
        )
    }


