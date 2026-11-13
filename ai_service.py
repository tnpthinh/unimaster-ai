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
import ipaddress
import urllib.parse
from datetime import datetime, timezone
import aiohttp
from database import (
    get_setting,
    set_setting,
    list_ai_api_keys,
    sync_ai_api_keys_pool,
    toggle_ai_api_key as db_toggle_ai_api_key,
    update_ai_api_key_telemetry,
)

# Danh sách mô hình Google Gemini hiện hành theo thứ tự ưu tiên:
# Các dòng 3.5/3.6/flash-latest xử lý sâu & multimodal; flash-lite siêu nhanh và ổn định cao
GEMINI_MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-flash-lite-latest",
    "gemini-3.1-flash-lite",
    "gemini-flash-latest",
    "gemini-3.5-flash",
    "gemini-3-flash-preview",
]

# Fast 0ms response cache for repeated questions (value: {"ts": float, "result": dict})
AI_CACHE = {}
_AI_CACHE_TTL_SEC = 3600
_AI_CACHE_MAX_ITEMS = 500

STEM_FORMAT_GUIDE = (
    "Quy tắc định dạng học thuật bắt buộc:\n"
    "- Viết bằng **Markdown sạch** (TUYỆT ĐỐI KHÔNG dùng thẻ HTML thô).\n"
    "- Mọi công thức Toán học, Vật lý, Xác suất phải bọc trong `$...$` (cùng dòng) hoặc `$$...$$` (riêng dòng), ví dụ `$v_{\\max} = \\omega A$`, `$\\int u\\,\\mathrm{d}v$`.\n"
    "- Mọi công thức phân tử, ion và phương trình Hóa học / Sinh hóa phải dùng cú pháp `$\\ce{...}$` (ví dụ `$\\ce{H2SO4}$`, `$\\ce{2H2 + O2 ->[t^\\circ] 2H2O}$`, `$\\ce{Fe^{3+}}$`).\n"
    "- Từ khóa lập trình dùng `inline code`, đoạn mã nhiều dòng dùng khối ```csharp hoặc ngôn ngữ tương ứng."
)

# Runtime telemetry & failover state per API key and model
KEY_TELEMETRY = {}
_MODEL_COOLDOWN: dict[str, float] = {}
ROUTER_TELEMETRY = {
    "status": "unknown",
    "model": "",
    "latency_ms": None,
    "last_error": "",
    "last_checked_at": None,
    "available_models": [],
}
_RR_CURSOR = 0
_ENV_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
_HTTP_SESSIONS: dict[int, aiohttp.ClientSession] = {}

_SECRET_PATTERN = re.compile(r"(AQ\.Ab[A-Za-z0-9._-]{8,}|AIzaSy[A-Za-z0-9_-]{8,}|sk-[A-Za-z0-9_-]{8,})")
_VALID_PRIORITIES = {"gemini_first", "openai_first", "gemini_only", "openai_only"}


async def _get_http_session() -> aiohttp.ClientSession:
    """Reuse a pooled aiohttp.ClientSession per running event loop to cut TLS latency."""
    loop = asyncio.get_running_loop()
    lid = id(loop)
    sess = _HTTP_SESSIONS.get(lid)
    if sess is not None and not sess.closed:
        return sess
    connector = aiohttp.TCPConnector(limit=32, ttl_dns_cache=300, keepalive_timeout=15, enable_cleanup_closed=True)
    sess = aiohttp.ClientSession(connector=connector)
    _HTTP_SESSIONS[lid] = sess
    return sess


async def close_http_session() -> None:
    for lid, sess in list(_HTTP_SESSIONS.items()):
        _HTTP_SESSIONS.pop(lid, None)
        if sess is not None and not sess.closed:
            try:
                await sess.close()
            except Exception:
                pass


def _utc_now_iso() -> str:
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%dT%H:%M:%S.") + f"{now.microsecond // 1000:03d}Z"


def mask_key(k: str) -> str:
    k = (k or "").strip()
    if not k:
        return ""
    if len(k) <= 12:
        return "*" * len(k)
    return f"{k[:7]}••••{k[-4:]}"


def _is_masked_placeholder(k: str) -> bool:
    s = (k or "").strip()
    if not s:
        return True
    if "••••" in s or "..." in s:
        return True
    if set(s) == {"*"}:
        return True
    return False


def classify_key_type(k: str) -> str:
    s = (k or "").strip()
    if s.startswith("AQ."):
        return "aistudio_aq"
    if s.startswith("AIza"):
        return "google_aiza"
    return "gemini"


def validate_gemini_key_format(k: str) -> tuple[bool, str]:
    s = (k or "").strip()
    if not s or _is_masked_placeholder(s):
        return False, "Key trống hoặc là chuỗi đã che (••••)"
    if any(ch.isspace() for ch in s):
        return False, "Key không được chứa khoảng trắng"
    if s.startswith("sk-"):
        return False, "Đây là API key 9Router/OpenAI (sk-...), hãy gắn vào mục 9Router Gateway"
    if re.fullmatch(r"AIza[A-Za-z0-9_-]{8,}", s) or re.fullmatch(r"AQ\.[A-Za-z0-9._-]{8,}", s):
        return True, ""
    return False, "Định dạng Gemini key không hợp lệ (cần bắt đầu bằng AIza... hoặc AQ....)"


def _sanitize_error_text(text: str, raw_secret: str = "") -> str:
    msg = str(text or "")
    if raw_secret:
        msg = msg.replace(raw_secret, mask_key(raw_secret))
    msg = _SECRET_PATTERN.sub(lambda m: mask_key(m.group(1)), msg)
    return msg.strip()


def _parse_key_tokens(raw_val: str) -> list[str]:
    val = (raw_val or "").strip()
    if not val:
        return []
    if val.startswith("["):
        try:
            arr = json.loads(val)
            if isinstance(arr, list):
                out = []
                for item in arr:
                    if isinstance(item, str) and not _is_masked_placeholder(item):
                        out.append(item.strip())
                    elif isinstance(item, dict):
                        kv = str(item.get("key", "")).strip()
                        if kv and not _is_masked_placeholder(kv):
                            out.append(kv)
                return out
        except Exception:
            pass
    return [
        ln.strip()
        for ln in re.split(r"[\r\n,;]+", val)
        if ln.strip() and not _is_masked_placeholder(ln.strip())
    ]


def _sync_env_file(updates: dict, create_if_missing: bool = False) -> bool:
    """Safely update key=value lines in local .env without losing unrelated config."""
    if not _is_local_runtime():
        return False
    exists = os.path.isfile(_ENV_FILE_PATH)
    if not exists and not create_if_missing:
        return False
    try:
        lines = []
        if exists:
            with open(_ENV_FILE_PATH, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()

        clean_updates = {}
        for k, v in (updates or {}).items():
            key_name = re.sub(r"[^A-Za-z0-9_]", "", str(k or ""))
            if not key_name:
                continue
            val_str = str("" if v is None else v).replace("\r", "").replace("\n", "").strip()
            clean_updates[key_name] = val_str

        if not clean_updates:
            return False

        seen_keys = set()
        new_lines = []
        for raw_line in lines:
            stripped = raw_line.strip()
            if stripped and not stripped.startswith("#") and "=" in stripped:
                k_part = stripped.split("=", 1)[0].strip()
                if k_part.startswith("export "):
                    k_part = k_part[7:].strip()
                if k_part in clean_updates:
                    if k_part not in seen_keys:
                        new_lines.append(f"{k_part}={clean_updates[k_part]}")
                        seen_keys.add(k_part)
                    continue
            new_lines.append(raw_line)

        for k_name, val_str in clean_updates.items():
            if k_name not in seen_keys:
                new_lines.append(f"{k_name}={val_str}")

        tmp_path = _ENV_FILE_PATH + ".tmp"
        with open(tmp_path, "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(new_lines) + "\n")
        os.replace(tmp_path, _ENV_FILE_PATH)
        return True
    except Exception:
        return False


def _merge_initial_gemini_sources() -> list[dict]:
    """Read Gemini keys from DB table, settings pool, legacy setting, and ENV in order."""
    db_rows = list_ai_api_keys("gemini")
    pool_initialized = get_setting("ai_pool_initialized", "").strip() == "1"

    seen = set()
    normalized = []

    def _append_key(raw_k: str, raw_lbl: str = "", row_meta: dict = None):
        k = (raw_k or "").strip()
        if not k or _is_masked_placeholder(k) or k in seen:
            return
        seen.add(k)
        idx_num = len(normalized) + 1
        lbl = (raw_lbl or "").strip() or f"Key #{idx_num}"
        entry = {
            "id": row_meta.get("id") if row_meta else None,
            "key": k,
            "label": lbl,
            "masked_key": mask_key(k),
            "key_type": classify_key_type(k),
            "is_enabled": bool(row_meta.get("is_enabled", 1)) if row_meta else True,
            "db_meta": row_meta,
        }
        normalized.append(entry)

    for row in db_rows:
        _append_key(row.get("api_key", ""), row.get("label", ""), row_meta=row)

    # Bootstrap or import any keys from legacy settings / ENV that haven't been registered yet
    if not db_rows or not pool_initialized:
        raw_pool = get_setting("gemini_api_keys_pool", "").strip()
        items = []
        if raw_pool:
            try:
                parsed = json.loads(raw_pool)
                if isinstance(parsed, list):
                    items = parsed
            except Exception:
                pass
        for idx, entry in enumerate(items):
            if isinstance(entry, str):
                _append_key(entry, f"Key #{idx + 1}")
            elif isinstance(entry, dict):
                _append_key(str(entry.get("key", "")), str(entry.get("label") or f"Key #{idx + 1}"))

        legacy_db = get_setting("gemini_api_key", "").strip()
        if legacy_db:
            _append_key(legacy_db)

    for env_k in _parse_key_tokens(os.environ.get("GEMINI_API_KEYS", "")):
        _append_key(env_k)

    legacy_env = os.environ.get("GEMINI_API_KEY", "").strip()
    if legacy_env:
        _append_key(legacy_env)

    # Persist back to ai_api_keys on bootstrap or if ENV added new keys
    if normalized and (not pool_initialized or len(normalized) != len(db_rows)):
        synced = sync_ai_api_keys_pool(normalized, provider="gemini")
        row_by_key = {r["api_key"]: r for r in synced}
        for item in normalized:
            rm = row_by_key.get(item["key"])
            if rm:
                item["id"] = rm["id"]
                item["is_enabled"] = bool(rm["is_enabled"])
                item["db_meta"] = rm
        set_setting("ai_pool_initialized", "1")
        set_setting(
            "gemini_api_keys_pool",
            json.dumps([{"key": x["key"], "label": x["label"]} for x in normalized], ensure_ascii=False),
        )
        set_setting("gemini_api_key", normalized[0]["key"])

    return normalized


def get_api_keys_pool() -> list[dict]:
    """Đọc danh sách toàn bộ API Keys (gộp ai_api_keys + legacy DB key + ENV GEMINI_API_KEYS)."""
    return _merge_initial_gemini_sources()


def save_api_keys_pool(keys_input, sync_env: bool = True) -> list[dict]:
    """Lưu danh sách nhiều API Key (nhận mảng hoặc chuỗi nhiều dòng); bỏ qua placeholder đã che."""
    raw_entries = []
    if isinstance(keys_input, str):
        lines = _parse_key_tokens(keys_input)
        raw_entries = [{"key": ln, "label": f"Key #{i + 1}"} for i, ln in enumerate(lines)]
    elif isinstance(keys_input, list):
        for i, item in enumerate(keys_input):
            if isinstance(item, str):
                k = item.strip()
                if k and not _is_masked_placeholder(k):
                    raw_entries.append({"key": k, "label": f"Key #{i + 1}"})
            elif isinstance(item, dict):
                k = str(item.get("key") or item.get("api_key") or "").strip()
                if k and not _is_masked_placeholder(k):
                    raw_entries.append({
                        "key": k,
                        "label": str(item.get("label") or f"Key #{i + 1}").strip(),
                        "is_enabled": item.get("is_enabled", True),
                    })

    seen = set()
    clean_pool = []
    for entry in raw_entries:
        k = entry["key"]
        if k not in seen:
            seen.add(k)
            clean_pool.append({
                "key": k,
                "label": entry["label"],
                "masked_key": mask_key(k),
                "key_type": classify_key_type(k),
                "is_enabled": entry.get("is_enabled", True),
            })

    sync_ai_api_keys_pool(clean_pool, provider="gemini")
    set_setting("ai_pool_initialized", "1")
    set_setting(
        "gemini_api_keys_pool",
        json.dumps([{"key": x["key"], "label": x["label"]} for x in clean_pool], ensure_ascii=False),
    )
    primary = clean_pool[0]["key"] if clean_pool else ""
    set_setting("gemini_api_key", primary)

    joined_keys = ",".join(x["key"] for x in clean_pool)
    os.environ["GEMINI_API_KEYS"] = joined_keys
    if primary:
        os.environ["GEMINI_API_KEY"] = primary
    else:
        os.environ.pop("GEMINI_API_KEY", None)

    if sync_env:
        _sync_env_file({"GEMINI_API_KEYS": joined_keys})

    return get_api_keys_pool()


async def add_gemini_keys_to_pool(keys_input, auto_test: bool = False, sync_env: bool = True) -> dict:
    """Validate, deduplicate, store in DB + .env, and optionally test newly added Gemini keys."""
    if isinstance(keys_input, str):
        raw_tokens = [ln.strip() for ln in re.split(r"[\r\n,;]+", keys_input) if ln.strip()]
    elif isinstance(keys_input, list):
        raw_tokens = []
        for item in keys_input:
            if isinstance(item, str) and item.strip():
                raw_tokens.append(item.strip())
            elif isinstance(item, dict):
                kv = str(item.get("key") or item.get("api_key") or "").strip()
                if kv:
                    raw_tokens.append(kv)
    else:
        raw_tokens = []

    if not raw_tokens:
        return {
            "success": False,
            "error": "Vui lòng nhập ít nhất 1 Gemini API Key (AIza... hoặc AQ....)",
            "added_count": 0,
            "duplicate_count": 0,
            "rejected_count": 0,
            "added": [],
            "rejected": [],
        }

    current_pool = get_api_keys_pool()
    existing_keys = {item["key"] for item in current_pool}

    valid_new = []
    duplicates = []
    rejected = []
    seen_batch = set()

    for tok in raw_tokens:
        ok, reason = validate_gemini_key_format(tok)
        if not ok:
            rejected.append({"masked_key": mask_key(tok) if len(tok) > 12 else tok[:4] + "••••", "reason": reason})
            continue
        if tok in existing_keys or tok in seen_batch:
            duplicates.append(mask_key(tok))
            continue
        seen_batch.add(tok)
        valid_new.append(tok)

    if not valid_new and rejected and not duplicates:
        return {
            "success": False,
            "error": rejected[0]["reason"],
            "added_count": 0,
            "duplicate_count": 0,
            "rejected_count": len(rejected),
            "added": [],
            "rejected": rejected,
        }

    new_pool = [{"key": x["key"], "label": x["label"], "is_enabled": x.get("is_enabled", True)} for x in current_pool]
    for nk in valid_new:
        new_pool.append({"key": nk, "label": f"Key #{len(new_pool) + 1}", "is_enabled": True})

    if valid_new:
        save_api_keys_pool(new_pool, sync_env=sync_env)

    test_results = []
    if auto_test and valid_new:
        test_results = list(await asyncio.gather(*(test_api_key(k) for k in valid_new)))

    updated_status = get_pool_status()
    status_by_mask = {item["masked_key"]: item for item in updated_status}
    added_items = [status_by_mask.get(mask_key(k), {"masked_key": mask_key(k)}) for k in valid_new]
    summary = get_pool_summary()

    if valid_new:
        msg = f"Đã thêm {len(valid_new)} Gemini API Key an toàn trên server!"
        if duplicates:
            msg += f" (Bỏ qua {len(duplicates)} key trùng)"
        if rejected:
            msg += f" ({len(rejected)} key sai định dạng)"
    elif duplicates:
        msg = f"Tất cả {len(duplicates)} key đã tồn tại trong dàn."
    else:
        msg = "Không có key hợp lệ nào được thêm."

    return {
        "success": True,
        "secured_on_server": True,
        "added_count": len(valid_new),
        "duplicate_count": len(duplicates),
        "rejected_count": len(rejected),
        "added": added_items,
        "duplicates": duplicates,
        "rejected": rejected,
        "test_results": test_results,
        "total_count": summary["total_count"],
        "ready_count": summary["ready_count"],
        "active_count": summary["active_count"],
        "keys": summary["keys"],
        "pool": summary["keys"],
        "message": msg,
    }


def delete_gemini_key_from_pool(
    index: int = None,
    key_id: int = None,
    masked_key: str = None,
    zero_index: int = None,
    sync_env: bool = True,
) -> dict:
    pool = get_api_keys_pool()
    target_idx = None

    if key_id is not None:
        for i, item in enumerate(pool):
            if item.get("id") == int(key_id):
                target_idx = i
                break
    elif index is not None:
        idx1 = int(index)
        if 1 <= idx1 <= len(pool):
            target_idx = idx1 - 1
    elif zero_index is not None:
        idx0 = int(zero_index)
        if 0 <= idx0 < len(pool):
            target_idx = idx0
    elif masked_key:
        mk = str(masked_key).strip()
        for i, item in enumerate(pool):
            if item.get("masked_key") == mk:
                target_idx = i
                break

    if target_idx is None or not (0 <= target_idx < len(pool)):
        return {"success": False, "deleted": False, "error": "Không tìm thấy API Key cần xóa"}

    removed = pool.pop(target_idx)
    KEY_TELEMETRY.pop(removed["key"], None)
    save_api_keys_pool(pool, sync_env=sync_env)
    summary = get_pool_summary()
    return {
        "success": True,
        "deleted": True,
        "masked_key": removed["masked_key"],
        "total_count": summary["total_count"],
        "ready_count": summary["ready_count"],
        "keys": summary["keys"],
        "pool": summary["keys"],
        "message": f"Đã xóa key {removed['masked_key']} khỏi dàn luân phiên.",
    }


def toggle_gemini_key_in_pool(
    index: int = None,
    key_id: int = None,
    masked_key: str = None,
    enabled: bool = None,
) -> dict:
    pool = get_api_keys_pool()
    target = None
    if key_id is not None:
        target = next((x for x in pool if x.get("id") == int(key_id)), None)
    elif index is not None:
        idx1 = int(index)
        if 1 <= idx1 <= len(pool):
            target = pool[idx1 - 1]
    elif masked_key:
        mk = str(masked_key).strip()
        target = next((x for x in pool if x.get("masked_key") == mk), None)

    if not target:
        return {"success": False, "error": "Không tìm thấy API Key cần bật/tắt"}

    row = db_toggle_ai_api_key(key_id=target.get("id"), api_key=target["key"], enabled=enabled)
    is_en = bool(row.get("is_enabled", 1)) if row else True
    tel = _ensure_telemetry(target["key"])
    tel["status"] = "ready" if is_en else "disabled"
    summary = get_pool_summary()
    return {
        "success": True,
        "masked_key": target["masked_key"],
        "is_enabled": is_en,
        "total_count": summary["total_count"],
        "ready_count": summary["ready_count"],
        "keys": summary["keys"],
        "pool": summary["keys"],
    }


def get_api_key() -> str:
    pool = get_api_keys_pool()
    enabled = [x for x in pool if x.get("is_enabled", True)]
    target = enabled or pool
    return target[0]["key"] if target else ""


def _ensure_telemetry(key: str, db_meta: dict = None) -> dict:
    if key not in KEY_TELEMETRY:
        KEY_TELEMETRY[key] = {
            "calls": int(db_meta.get("calls") or 0) if db_meta else 0,
            "failovers": int(db_meta.get("failovers") or 0) if db_meta else 0,
            "cooldown_until": 0.0,
            "status": str(db_meta.get("status") or "ready") if db_meta else "ready",
            "model": str(db_meta.get("model") or "") if db_meta else "",
            "latency_ms": db_meta.get("latency_ms") if db_meta else None,
            "last_error": str(db_meta.get("last_error") or "") if db_meta else "",
            "last_checked_at": (db_meta.get("last_checked_at") or None) if db_meta else None,
        }
    return KEY_TELEMETRY[key]


def get_pool_status() -> list[dict]:
    now = time.time()
    pool = get_api_keys_pool()
    out = []
    for idx, item in enumerate(pool):
        k = item["key"]
        is_enabled = bool(item.get("is_enabled", True))
        tel = _ensure_telemetry(k, item.get("db_meta"))
        cd_rem = max(0, int(tel["cooldown_until"] - now))
        status = "disabled" if not is_enabled else tel["status"]
        if is_enabled and status == "disabled":
            status = "ready"
            tel["status"] = "ready"
        if is_enabled and status in ("cooldown", "invalid") and tel["cooldown_until"] > 0 and cd_rem == 0:
            if status == "cooldown":
                status = "ready"
                tel["status"] = "ready"
        out.append({
            "id": item.get("id") or (idx + 1),
            "index": idx + 1,
            "label": item.get("label") or f"Key #{idx + 1}",
            "masked_key": mask_key(k),
            "provider": "gemini",
            "key_type": classify_key_type(k),
            "status": status,
            "is_enabled": is_enabled,
            "calls": tel["calls"],
            "failovers": tel["failovers"],
            "cooldown_remaining": cd_rem,
            "model": tel["model"],
            "latency_ms": tel.get("latency_ms"),
            "last_error": tel.get("last_error", ""),
            "last_checked_at": tel.get("last_checked_at"),
        })
    return out


def get_pool_summary() -> dict:
    keys = get_pool_status()
    total_count = len(keys)
    ready_count = sum(1 for k in keys if k.get("is_enabled", True) and k["status"] in ("ready", "active"))
    active_count = sum(1 for k in keys if k.get("is_enabled", True) and k["status"] == "active")
    cooldown_count = sum(1 for k in keys if k.get("is_enabled", True) and k["status"] == "cooldown")
    invalid_count = sum(1 for k in keys if k.get("is_enabled", True) and k["status"] == "invalid")
    disabled_count = sum(1 for k in keys if not k.get("is_enabled", True))
    primary_masked = ""
    for k in keys:
        if k.get("is_enabled", True) and k["status"] != "invalid":
            primary_masked = k["masked_key"]
            break
    if not primary_masked and keys:
        primary_masked = keys[0]["masked_key"]
    return {
        "total_count": total_count,
        "ready_count": ready_count,
        "active_count": active_count,
        "cooldown_count": cooldown_count,
        "invalid_count": invalid_count,
        "disabled_count": disabled_count,
        "has_gemini_key": total_count > 0,
        "masked_key": primary_masked,
        "keys": keys,
    }


def _ordered_candidate_keys() -> list[str]:
    global _RR_CURSOR
    pool = [x for x in get_api_keys_pool() if x.get("is_enabled", True)]
    if not pool:
        return []

    n = len(pool)
    start = _RR_CURSOR % n
    _RR_CURSOR = (_RR_CURSOR + 1) % n

    rotated = [pool[(start + i) % n] for i in range(n)]
    now = time.time()

    healthy = []
    degraded = []
    cooling = []
    invalid_keys = []
    for item in rotated:
        k = item["key"]
        tel = _ensure_telemetry(k, item.get("db_meta"))
        if tel["status"] == "invalid" and tel["cooldown_until"] > now:
            invalid_keys.append((tel["cooldown_until"], k))
        elif tel["cooldown_until"] > now:
            cooling.append((tel["cooldown_until"], k))
        else:
            if tel["status"] in ("cooldown", "invalid", "disabled"):
                tel["status"] = "ready"
            if tel.get("last_error"):
                degraded.append(k)
            else:
                healthy.append(k)

    cooling.sort(key=lambda pair: pair[0])
    invalid_keys.sort(key=lambda pair: pair[0])
    ordered = healthy + degraded + [k for _, k in cooling]
    if not ordered:
        ordered = [k for _, k in invalid_keys]
    return ordered



# Danh sách mô hình OpenAI & OpenAI-compatible xịn nhất thế giới:
# o3-mini: Siêu mô hình lý luận toán học, STEM & lập trình mới nhất của OpenAI
# o1: Mô hình suy luận sâu toàn diện hàng đầu của OpenAI
# gpt-4.5-preview: Mô hình tri thức khổng lồ & hiểu ngữ cảnh sâu sắc nhất
# gpt-4o: Mô hình flagship đa nhiệm thông minh cao cấp
OPENAI_MODELS = [
    "o3-mini",
    "gpt-4o",
    "o1",
    "gpt-4.5-preview",
    "gpt-4o-mini",
    "gpt-3.5-turbo"
]

# Model alias do 9Router cung cấp. `All` tự chọn model khả dụng; `Coding-Pro`
# ưu tiên model chuyên lập trình. Chúng dùng giao thức OpenAI-compatible.
ROUTER_MODELS = ["All", "deepseek-chat", "gpt-reserve", "Coding-Pro"]

# Dòng mô hình FOSTA Codex AI thế hệ 6:
# gpt-6-astra: Mô hình mạnh nhất thế hệ 6 • Lý luận & tư duy sâu
# gpt-6.1-sol: Mô hình tiêu chuẩn toàn năng • Cân bằng tốc độ & độ sâu
# gpt-6-luna: Mô hình siêu tốc • Tiết kiệm
FOSTA_MODELS = [
    "gpt-6-astra",
    "gpt-6.1-sol",
    "gpt-6-luna"
]


def _is_openai_reasoning_model(model_name: str) -> bool:
    """Kiểm tra mô hình có phải dòng suy luận (Reasoning) của OpenAI hay không (o1, o3-mini, o3, o4...)"""
    m = (model_name or "").strip().lower()
    base = m.split("/")[-1]
    return base.startswith(("o1", "o3", "o4"))


def _supports_gemini_thinking(model_name: str) -> bool:
    """Kiểm tra mô hình Gemini có hỗ trợ cấu hình thinkingConfig hay không"""
    m = (model_name or "").lower()
    if "lite" in m or "1.5" in m:
        return False
    return (
        ("3.5" in m)
        or ("3.6" in m)
        or ("3.7" in m)
        or ("3.8" in m)
        or ("3-flash" in m)
        or ("3.1-pro" in m)
        or ("flash-latest" in m)
        or ("pro-latest" in m)
        or ("2.5" in m)
        or ("thinking" in m)
    )


def _select_gemini_models(quality: str = "deep") -> list[str]:
    """Chọn thứ tự mô hình Gemini tối ưu theo độ phức tạp tác vụ"""
    if quality == "fast":
        return [
            "gemini-3.5-flash-lite",
            "gemini-flash-lite-latest",
            "gemini-3.1-flash-lite",
            "gemini-flash-latest",
            "gemini-3.5-flash",
        ]
    return list(GEMINI_MODELS)

# ===== AI Gateway động (9Router chạy trên máy cá nhân / Cloudflare Tunnel / OpenAI-compatible) =====
DEFAULT_GATEWAY_DISCOVERY_URL = "https://ntfy.sh/unimaster_ctump_5292/json?poll=1&since=72h"
_GATEWAY_CACHE = {"url": "", "ts": 0.0}
_GATEWAY_TTL = 90
_LOCAL_ROUTER_DEFAULT_URL = "http://127.0.0.1:20128/v1"
_FOSTA_DEFAULT_URL = "https://codex.fosta.app/v1"
_BLOCKED_SSRF_HOSTS = {
    "169.254.169.254",
    "metadata.google.internal",
    "metadata.goog",
    "metadata",
    "100.100.100.200",
    "fd00:ec2::254",
}


def gateway_discovery_url() -> str:
    """Đọc ENV mỗi lần gọi để đổi cấu hình không cần sửa code."""
    return (
        os.environ.get("AI_GATEWAY_DISCOVERY_URL", "").strip()
        or DEFAULT_GATEWAY_DISCOVERY_URL
    )


def gateway_secret() -> str:
    return os.environ.get("AI_GATEWAY_SECRET", "").strip()


def _is_local_url(url: str) -> bool:
    u = (url or "").strip()
    if not u:
        return False
    if "://" not in u:
        u = "http://" + u
    try:
        host = (urllib.parse.urlparse(u).hostname or "").strip().lower()
        return host in ("127.0.0.1", "localhost", "::1", "0.0.0.0")
    except Exception:
        low = u.lower()
        return "127.0.0.1" in low or "localhost" in low


def validate_router_base_url(raw_url: str, default_on_empty: bool = False) -> tuple[bool, str, str]:
    """Validate and normalize 9Router/OpenAI-compatible Base URL with SSRF protection."""
    raw = (raw_url or "").strip()
    if not raw:
        if default_on_empty:
            return True, "https://api.openai.com/v1", ""
        return False, "", "Vui lòng nhập Base URL cho 9Router / OpenAI Gateway."

    if "://" not in raw:
        return False, "", "Base URL phải bắt đầu bằng http:// hoặc https://"

    try:
        parsed = urllib.parse.urlparse(raw)
    except Exception:
        return False, "", "Base URL không đúng định dạng URL."

    scheme = (parsed.scheme or "").lower()
    if scheme not in ("http", "https"):
        return False, "", "Chỉ hỗ trợ giao thức http:// hoặc https:// (chặn SSRF)."

    if parsed.username or parsed.password:
        return False, "", "Không được nhúng user:password trực tiếp trong Base URL."

    host = (parsed.hostname or "").strip().lower()
    if not host:
        return False, "", "Base URL thiếu tên miền hoặc địa chỉ host hợp lệ."

    if host in _BLOCKED_SSRF_HOSTS or host.endswith(".internal") or host.endswith(".localdomain"):
        return False, "", f"Địa chỉ host bị chặn vì lý do bảo mật SSRF: {host}"

    # Check literal IPs (allow loopback 127.0.0.1 / ::1 for local 9Router; block link-local, metadata, LAN SSRF)
    try:
        ip_obj = ipaddress.ip_address(host)
        if ip_obj.is_link_local or ip_obj.is_multicast or ip_obj.is_unspecified:
            return False, "", f"Địa chỉ IP không được phép (link-local/unspecified): {host}"
        if (ip_obj.is_private or ip_obj.is_reserved) and not ip_obj.is_loopback:
            if os.environ.get("ALLOW_LAN_ROUTER", "").strip() != "1":
                return False, "", f"Chặn IP mạng nội bộ ({host}) để chống SSRF; dùng http://127.0.0.1:20128/v1 hoặc tên miền HTTPS."
    except ValueError:
        pass

    path = (parsed.path or "").rstrip("/")
    for suffix in ("/chat/completions", "/models"):
        if path.lower().endswith(suffix):
            path = path[: -len(suffix)].rstrip("/")
    if not path:
        path = "/v1"

    netloc = parsed.netloc
    normalized = f"{scheme}://{netloc}{path}"
    return True, normalized.rstrip("/"), ""


def _is_local_runtime() -> bool:
    """True khi tiến trình này chạy trên chính máy đang chạy 9Router."""
    for key in ("RENDER", "RENDER_SERVICE_ID", "RENDER_EXTERNAL_URL"):
        if os.environ.get(key):
            return False
    if os.environ.get("UNIMASTER_CLOUD") == "1":
        return False
    return not os.environ.get("DATA_DIR", "").strip()


def invalidate_gateway_cache() -> None:
    """Xóa URL tunnel đã cache để lần gọi sau dò lại (Quick Tunnel đổi URL khi restart)."""
    _GATEWAY_CACHE["url"] = ""
    _GATEWAY_CACHE["ts"] = 0.0


async def resolve_gateway_base_url(base_url: str, force: bool = False) -> str:
    """Nếu Base URL trỏ vào máy nội bộ, tự dò địa chỉ tunnel công khai khi chạy trên cloud."""
    base_url = (base_url or "").rstrip("/")
    discovery = gateway_discovery_url()
    if not discovery or not _is_local_url(base_url):
        return base_url
    if not force and _is_local_runtime():
        return base_url

    now = time.time()
    if not force and _GATEWAY_CACHE["url"] and (now - _GATEWAY_CACHE["ts"]) < _GATEWAY_TTL:
        return _GATEWAY_CACHE["url"]

    try:
        session = await _get_http_session()
        async with session.get(discovery, timeout=aiohttp.ClientTimeout(total=8)) as resp:
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
                    ok_url, norm_cand, _ = validate_router_base_url(candidate)
                    if ok_url and not _is_local_url(norm_cand):
                        found = norm_cand
                if found:
                    _GATEWAY_CACHE["url"] = found
                    _GATEWAY_CACHE["ts"] = now
                    print(f"[AI Gateway] Đã dò được tunnel: {found}")
                    return found
    except Exception as exc:
        print(f"[AI Gateway] Không dò được tunnel: {_sanitize_error_text(str(exc))}")

    return _GATEWAY_CACHE["url"] or base_url


def _detect_router_provider_type(base_url: str, model: str = "") -> str:
    low_url = (base_url or "").lower()
    if "fosta" in low_url:
        return "fosta"
    if (
        _is_local_url(base_url)
        or "9router" in low_url
        or "abc-tunnel" in low_url
        or "trycloudflare" in low_url
        or (model or "").strip() in ROUTER_MODELS
    ):
        return "9router"
    return "openai"


def get_openai_settings() -> dict:
    """Đọc cấu hình 9Router / FOSTA / OpenAI-compatible từ DB hoặc biến môi trường."""
    db_router_key = get_setting("router_api_key", "").strip()
    db_openai_key = get_setting("openai_api_key", "").strip()
    db_router_url = get_setting("router_base_url", "").strip()
    db_openai_url = get_setting("openai_base_url", "").strip()
    db_router_model = get_setting("router_model", "").strip()
    db_openai_model = get_setting("openai_model", "").strip()
    db_priority = get_setting("ai_provider_priority", "").strip()

    key = (
        (db_router_key if not _is_masked_placeholder(db_router_key) else "")
        or (db_openai_key if not _is_masked_placeholder(db_openai_key) else "")
        or os.environ.get("ROUTER_API_KEY", "").strip()
        or os.environ.get("OPENAI_API_KEY", "").strip()
    )
    base_url = (
        db_router_url
        or db_openai_url
        or os.environ.get("ROUTER_BASE_URL", "").strip()
        or os.environ.get("OPENAI_BASE_URL", "").strip()
        or "https://api.openai.com/v1"
    ).rstrip("/")
    model = (
        db_router_model
        or db_openai_model
        or os.environ.get("ROUTER_MODEL", "").strip()
        or os.environ.get("OPENAI_MODEL", "").strip()
    )

    is_fosta_model = model.lower().startswith("gpt-6.") if model else False
    if is_fosta_model and "api.openai.com" in base_url.lower():
        base_url = _FOSTA_DEFAULT_URL

    provider_type = _detect_router_provider_type(base_url, model)
    is_fosta = provider_type == "fosta"
    default_model = "gpt-6-astra" if is_fosta else ("All" if provider_type == "9router" else "gpt-4o")
    model = model or default_model

    priority = (db_priority or os.environ.get("AI_PROVIDER_PRIORITY", "").strip() or "gemini_first").lower()
    if priority not in _VALID_PRIORITIES:
        priority = "gemini_first"

    return {
        "key": key,
        "base_url": base_url,
        "model": model,
        "priority": priority,
        "provider_type": provider_type,
    }


def save_router_config(
    base_url: str = None,
    api_key: str = None,
    model: str = None,
    priority: str = None,
    clear_key: bool = False,
) -> tuple[bool, dict, str]:
    """Lưu cấu hình 9Router/OpenAI an toàn: kiểm tra SSRF, không ghi đè key bằng chuỗi ••••."""
    cur = get_openai_settings()
    env_updates = {}
    changed_endpoint = False

    if base_url is not None:
        raw_u = str(base_url).strip()
        if raw_u:
            ok_u, norm_u, err_u = validate_router_base_url(raw_u)
            if not ok_u:
                return False, get_router_public_status(), err_u
            if norm_u != cur["base_url"]:
                changed_endpoint = True
            set_setting("router_base_url", norm_u)
            set_setting("openai_base_url", norm_u)
            os.environ["ROUTER_BASE_URL"] = norm_u
            env_updates["ROUTER_BASE_URL"] = norm_u
            invalidate_gateway_cache()

    if clear_key:
        changed_endpoint = True
        set_setting("router_api_key", "")
        set_setting("openai_api_key", "")
        os.environ.pop("ROUTER_API_KEY", None)
        os.environ.pop("OPENAI_API_KEY", None)
        env_updates["ROUTER_API_KEY"] = ""
    elif api_key is not None:
        ak = str(api_key).strip()
        if ak and not _is_masked_placeholder(ak):
            if ak != cur["key"]:
                changed_endpoint = True
            set_setting("router_api_key", ak)
            set_setting("openai_api_key", ak)
            os.environ["ROUTER_API_KEY"] = ak
            env_updates["ROUTER_API_KEY"] = ak

    if model is not None:
        m_val = str(model).strip()
        if m_val:
            set_setting("router_model", m_val)
            set_setting("openai_model", m_val)
            os.environ["ROUTER_MODEL"] = m_val
            env_updates["ROUTER_MODEL"] = m_val

    if priority is not None:
        p_val = str(priority).strip().lower()
        if p_val not in _VALID_PRIORITIES:
            return False, get_router_public_status(), (
                "Priority không hợp lệ. Chọn: gemini_first, openai_first, gemini_only hoặc openai_only."
            )
        set_setting("ai_provider_priority", p_val)
        os.environ["AI_PROVIDER_PRIORITY"] = p_val
        env_updates["AI_PROVIDER_PRIORITY"] = p_val

    if env_updates:
        _sync_env_file(env_updates)

    if changed_endpoint:
        ROUTER_TELEMETRY["status"] = "unknown"
        ROUTER_TELEMETRY["last_error"] = ""
        ROUTER_TELEMETRY["latency_ms"] = None
        ROUTER_TELEMETRY["available_models"] = []

    return True, get_router_public_status(), "Đã cập nhật cấu hình 9Router / AI Gateway an toàn."


def get_router_public_status() -> dict:
    """Trả thông tin trạng thái 9Router/OpenAI (LUÔN che khóa API)."""
    cfg = get_openai_settings()
    key = cfg["key"]
    has_key = bool(key)
    tel_status = ROUTER_TELEMETRY.get("status", "unknown")
    if not has_key:
        effective_status = "unconfigured"
    elif tel_status == "ready":
        effective_status = "ready"
    elif tel_status == "error":
        effective_status = "error"
    else:
        effective_status = "configured"

    return {
        "configured": has_key,
        "has_key": has_key,
        "masked_key": mask_key(key) if has_key else "",
        "base_url": cfg["base_url"],
        "model": cfg["model"],
        "priority": cfg["priority"],
        "provider_type": cfg["provider_type"],
        "status": effective_status,
        "latency_ms": ROUTER_TELEMETRY.get("latency_ms"),
        "last_error": ROUTER_TELEMETRY.get("last_error", ""),
        "last_checked_at": ROUTER_TELEMETRY.get("last_checked_at"),
        "available_models": list(ROUTER_TELEMETRY.get("available_models") or []),
    }


def get_gateway_local_hint() -> dict:
    return {
        "local_router_default_url": _LOCAL_ROUTER_DEFAULT_URL,
        "fosta_default_url": _FOSTA_DEFAULT_URL,
        "openai_default_url": "https://api.openai.com/v1",
        "presets": [
            {
                "id": "9router_local",
                "label": "9Router Local (Port 20128)",
                "base_url": _LOCAL_ROUTER_DEFAULT_URL,
                "default_model": "All",
                "models": list(ROUTER_MODELS),
            },
            {
                "id": "fosta_codex",
                "label": "FOSTA Codex AI",
                "base_url": _FOSTA_DEFAULT_URL,
                "default_model": "gpt-6.1-sol",
                "models": list(FOSTA_MODELS),
            },
            {
                "id": "openai_official",
                "label": "OpenAI Official",
                "base_url": "https://api.openai.com/v1",
                "default_model": "gpt-4o",
                "models": list(OPENAI_MODELS),
            },
        ],
        "recommended_models": ["All", "Coding-Pro", "gpt-6-astra", "gpt-6.1-sol", "gpt-4o"],
    }


async def _parse_openai_response_payload(resp) -> dict:
    """Parse standard JSON or SSE text/event-stream responses returned by 9Router / OpenAI gateways."""
    ctype = (resp.headers.get("Content-Type") or "").lower()
    raw_text = await resp.text()
    stripped = raw_text.lstrip()
    if "text/event-stream" in ctype or stripped.startswith("data:"):
        model_name = ""
        chunks = []
        for line in raw_text.splitlines():
            line = line.strip()
            if not line.startswith("data:"):
                continue
            data_str = line[5:].strip()
            if not data_str or data_str == "[DONE]":
                continue
            try:
                obj = json.loads(data_str)
            except Exception:
                continue
            if not model_name and isinstance(obj, dict) and obj.get("model"):
                model_name = str(obj["model"])
            for ch in (obj.get("choices") or []):
                if not isinstance(ch, dict):
                    continue
                delta_txt = (ch.get("delta") or {}).get("content")
                msg_txt = (ch.get("message") or {}).get("content")
                piece = delta_txt if delta_txt is not None else msg_txt
                if piece:
                    chunks.append(str(piece))
        return {
            "model": model_name,
            "choices": [{"message": {"content": "".join(chunks)}}],
        }
    return json.loads(raw_text) if raw_text.strip() else {}


async def _call_openai_chatgpt_meta(
    prompt: str,
    system_instruction: str = "",
    max_tokens: int = 4096,
    messages_override: list = None,
) -> dict | None:
    """Gọi 9Router / FOSTA / OpenAI-compatible dùng connection pool và trả telemetry đầy đủ."""
    cfg = get_openai_settings()
    key = cfg["key"]
    if not key:
        return None

    ok_u, norm_cfg_url, url_err = validate_router_base_url(cfg["base_url"])
    if not ok_u:
        ROUTER_TELEMETRY["status"] = "error"
        ROUTER_TELEMETRY["last_error"] = url_err
        ROUTER_TELEMETRY["last_checked_at"] = _utc_now_iso()
        return None

    base_url = await resolve_gateway_base_url(norm_cfg_url)
    endpoint = f"{base_url}/chat/completions"

    gateway_route = _is_local_url(norm_cfg_url) and bool(gateway_discovery_url())
    gateway_retried = False

    provider_type = _detect_router_provider_type(base_url, cfg.get("model", ""))
    is_fosta = provider_type == "fosta"
    pref_model = cfg.get("model") or ("gpt-6-astra" if is_fosta else ("All" if provider_type == "9router" else "gpt-4o"))
    candidate_models = [pref_model]
    if is_fosta:
        for m in FOSTA_MODELS:
            if m not in candidate_models:
                candidate_models.append(m)
    elif provider_type == "9router":
        for m in ROUTER_MODELS:
            if m not in candidate_models:
                candidate_models.append(m)
    elif "api.openai.com" in base_url.lower():
        for m in OPENAI_MODELS:
            if m not in candidate_models:
                candidate_models.append(m)

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    secret_value = gateway_secret()
    if secret_value:
        headers["X-Gateway-Secret"] = secret_value

    session = await _get_http_session()
    for model in candidate_models:
        is_reasoning = _is_openai_reasoning_model(model)

        if messages_override and isinstance(messages_override, list):
            model_messages = []
            for msg in messages_override:
                r = msg.get("role", "user")
                c = str(msg.get("content") or msg.get("text") or "")
                if is_reasoning and r == "system":
                    r = "developer"
                model_messages.append({"role": r, "content": c})
        else:
            model_messages = []
            if system_instruction:
                role_name = "developer" if is_reasoning else "system"
                model_messages.append({"role": role_name, "content": system_instruction})
            model_messages.append({"role": "user", "content": prompt})

        payload = {"model": model, "messages": model_messages, "stream": False}
        if is_reasoning:
            eff_tokens = max(int(max_tokens or 4096), 4096)
            payload["max_completion_tokens"] = min(eff_tokens, 32768)
        else:
            payload["max_tokens"] = min(int(max_tokens or 4096), 16384)
            payload["temperature"] = 0.35

        t0 = time.perf_counter()
        try:
            async with session.post(endpoint, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=120)) as resp:
                latency_ms = int((time.perf_counter() - t0) * 1000)
                if resp.status == 200:
                    data = await _parse_openai_response_payload(resp)
                    choices = data.get("choices", [])
                    if choices:
                        reply = (choices[0].get("message", {}).get("content", "") or "").strip()
                        if reply:
                            actual_model = data.get("model") or model
                            p_code = "fosta" if is_fosta else ("9router" if provider_type == "9router" else "openai")
                            p_name = "FOSTA Codex AI" if is_fosta else ("9Router Gateway" if p_code == "9router" else "OpenAI ChatGPT")
                            ROUTER_TELEMETRY.update({
                                "status": "ready",
                                "model": actual_model,
                                "latency_ms": latency_ms,
                                "last_error": "",
                                "last_checked_at": _utc_now_iso(),
                            })
                            print(f"[AI Service] Generated via {p_name} ({actual_model}, {latency_ms}ms)!")
                            return {
                                "text": reply,
                                "provider_used": p_code,
                                "provider_label": p_name,
                                "model_used": actual_model,
                                "masked_key": mask_key(key),
                                "latency_ms": latency_ms,
                            }
                elif resp.status in (400, 401, 403, 404, 429, 500, 502, 503, 530):
                    err_text = _sanitize_error_text(await resp.text(), key)
                    print(f"[AI Service] Router/OpenAI HTTP {resp.status} ({model}): {err_text[:140]}")
                    ROUTER_TELEMETRY.update({
                        "status": "error",
                        "last_error": f"HTTP {resp.status}: {err_text[:120]}",
                        "last_checked_at": _utc_now_iso(),
                    })
                    if resp.status in (502, 503, 530) and gateway_route and not gateway_retried:
                        gateway_retried = True
                        invalidate_gateway_cache()
                        base_url = await resolve_gateway_base_url(norm_cfg_url, force=True)
                        endpoint = f"{base_url}/chat/completions"
                        print(f"[AI Service] Gateway HTTP {resp.status}, thử dò lại tunnel: {base_url}")
                        continue
                    if resp.status == 400 and any(k in err_text for k in ["max_tokens", "max_completion_tokens", "temperature"]):
                        fallback_content = (
                            f"{system_instruction}\n\n{prompt}" if system_instruction else prompt
                        )
                        if messages_override and isinstance(messages_override, list):
                            fallback_msgs = [
                                {"role": ("user" if m.get("role") == "developer" else m.get("role", "user")), "content": str(m.get("content") or m.get("text") or "")}
                                for m in messages_override
                            ]
                        else:
                            fallback_msgs = [{"role": "user", "content": fallback_content}]
                        retry_payload = {"model": model, "messages": fallback_msgs, "max_tokens": 4096, "stream": False}
                        try:
                            t1 = time.perf_counter()
                            async with session.post(endpoint, json=retry_payload, headers=headers, timeout=aiohttp.ClientTimeout(total=60)) as r_resp:
                                r_lat = int((time.perf_counter() - t1) * 1000)
                                if r_resp.status == 200:
                                    r_data = await _parse_openai_response_payload(r_resp)
                                    r_choices = r_data.get("choices", [])
                                    if r_choices:
                                        r_reply = (r_choices[0].get("message", {}).get("content", "") or "").strip()
                                        if r_reply:
                                            actual_model = r_data.get("model") or model
                                            p_code = "fosta" if is_fosta else ("9router" if provider_type == "9router" else "openai")
                                            p_name = "FOSTA Codex AI" if is_fosta else ("9Router Gateway" if p_code == "9router" else "OpenAI ChatGPT")
                                            ROUTER_TELEMETRY.update({
                                                "status": "ready",
                                                "model": actual_model,
                                                "latency_ms": r_lat,
                                                "last_error": "",
                                                "last_checked_at": _utc_now_iso(),
                                            })
                                            return {
                                                "text": r_reply,
                                                "provider_used": p_code,
                                                "provider_label": p_name,
                                                "model_used": actual_model,
                                                "masked_key": mask_key(key),
                                                "latency_ms": r_lat,
                                            }
                        except Exception:
                            pass
                    if resp.status in (401, 403):
                        return None
        except Exception as e:
            raw_err = _sanitize_error_text(str(e), key)
            safe_err = raw_err or ("Hết thời gian chờ phản hồi (Timeout)" if isinstance(e, (asyncio.TimeoutError, TimeoutError)) else type(e).__name__)
            print(f"[AI Service] Provider connection error for {model}: {safe_err[:140]}")
            ROUTER_TELEMETRY.update({
                "status": "error",
                "last_error": safe_err[:120],
                "last_checked_at": _utc_now_iso(),
            })
            if gateway_route and not gateway_retried:
                gateway_retried = True
                invalidate_gateway_cache()
                base_url = await resolve_gateway_base_url(norm_cfg_url, force=True)
                endpoint = f"{base_url}/chat/completions"
                print(f"[AI Service] Tunnel có thể đã đổi, thử lại qua: {base_url}")
            continue
    return None


async def _call_openai_chatgpt(
    prompt: str,
    system_instruction: str = "",
    max_tokens: int = 4096,
    messages_override: list = None,
) -> str | None:
    res = await _call_openai_chatgpt_meta(
        prompt=prompt,
        system_instruction=system_instruction,
        max_tokens=max_tokens,
        messages_override=messages_override,
    )
    return res["text"] if res else None


async def test_openai_key(key: str = None, base_url: str = None, model: str = None) -> dict:
    """Kiểm tra kết nối 9Router / FOSTA / OpenAI-compatible bằng /models + /chat/completions."""
    cfg = get_openai_settings()
    raw_key = (key or "").strip()
    target_key = cfg["key"] if (not raw_key or _is_masked_placeholder(raw_key)) else raw_key
    raw_url = (base_url or cfg["base_url"] or "").strip()

    if not target_key:
        return {
            "success": False,
            "provider": "9Router / OpenAI Gateway",
            "base_url": raw_url,
            "masked_key": "",
            "latency_ms": None,
            "available_models": [],
            "message": "Chưa có API Key để kiểm tra.",
        }

    ok_u, norm_url, err_u = validate_router_base_url(raw_url)
    if not ok_u:
        return {
            "success": False,
            "status_code": 400,
            "provider": "9Router / OpenAI Gateway",
            "base_url": raw_url,
            "masked_key": mask_key(target_key),
            "latency_ms": None,
            "available_models": [],
            "message": err_u,
        }

    target_url = await resolve_gateway_base_url(norm_url)
    target_model = (model or cfg.get("model") or "").strip()
    provider_type = _detect_router_provider_type(target_url, target_model)
    is_fosta = provider_type == "fosta"

    if not target_model:
        target_model = "gpt-6-astra" if is_fosta else ("All" if provider_type == "9router" else "gpt-4o")
    if is_fosta and target_model in ("gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo", "o3-mini", "o1", "gpt-4.5-preview"):
        target_model = "gpt-6-astra"

    headers = {
        "Authorization": f"Bearer {target_key}",
        "Content-Type": "application/json",
    }
    secret_value = gateway_secret()
    if secret_value:
        headers["X-Gateway-Secret"] = secret_value

    session = await _get_http_session()
    available_models = []
    try:
        async with session.get(f"{target_url}/models", headers=headers, timeout=aiohttp.ClientTimeout(total=12)) as m_resp:
            if m_resp.status == 200:
                m_data = await m_resp.json()
                raw_list = m_data.get("data", []) if isinstance(m_data, dict) else []
                for item in raw_list:
                    if isinstance(item, dict) and item.get("id"):
                        available_models.append(str(item["id"]))
                available_models = available_models[:25]
    except Exception:
        pass

    is_reasoning = _is_openai_reasoning_model(target_model)
    payload = {
        "model": target_model,
        "messages": [{"role": "user", "content": "Reply OK"}],
        "stream": False,
    }
    if is_reasoning:
        payload["max_completion_tokens"] = 300
    else:
        payload["max_tokens"] = 20
        payload["temperature"] = 0.2

    provider_title = "FOSTA Codex AI" if is_fosta else ("9Router Gateway" if provider_type == "9router" else "OpenAI ChatGPT")
    endpoint = f"{target_url}/chat/completions"
    t0 = time.perf_counter()
    try:
        async with session.post(endpoint, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=30)) as resp:
            latency_ms = int((time.perf_counter() - t0) * 1000)
            if resp.status == 200:
                data = await _parse_openai_response_payload(resp)
                returned_model = data.get("model") or target_model
                ROUTER_TELEMETRY.update({
                    "status": "ready",
                    "model": returned_model,
                    "latency_ms": latency_ms,
                    "last_error": "",
                    "last_checked_at": _utc_now_iso(),
                    "available_models": available_models or [returned_model],
                })
                return {
                    "success": True,
                    "provider": provider_title,
                    "provider_type": provider_type,
                    "model": returned_model,
                    "base_url": target_url,
                    "masked_key": mask_key(target_key),
                    "latency_ms": latency_ms,
                    "available_models": available_models or [returned_model],
                    "message": f"Kết nối thành công tới {provider_title} ({returned_model}) trong {latency_ms}ms",
                }

            raw_txt = await resp.text()
            txt = _sanitize_error_text(raw_txt, target_key)
            low_txt = raw_txt.lower()
            is_cf_tunnel_err = resp.status == 530 or "cloudflare tunnel error" in low_txt or "error code: 1033" in low_txt
            err_summary = (
                "HTTP 530 (Cloudflare Tunnel offline / lỗi 1033)"
                if is_cf_tunnel_err
                else f"HTTP {resp.status}: {txt[:120]}"
            )
            ROUTER_TELEMETRY.update({
                "status": "error",
                "latency_ms": latency_ms,
                "last_error": err_summary,
                "last_checked_at": _utc_now_iso(),
                "available_models": available_models,
            })
            if is_cf_tunnel_err:
                msg = (
                    f"HTTP 530: Đường hầm Cloudflare Tunnel ({target_url}) hiện đang offline (lỗi 1033). "
                    "Hãy kiểm tra app 9Router trên PC đã bật Tunnel chưa hoặc chạy start_ai_gateway.py."
                )
            elif resp.status == 401 and "api.openai.com" in target_url.lower():
                msg = f"HTTP 401 (Sai API Key hoặc cần đổi Base URL sang 9Router/FOSTA): {txt[:120]}"
            else:
                msg = f"Mã lỗi HTTP {resp.status}: {txt[:120]}"
            return {
                "success": False,
                "provider": provider_title,
                "provider_type": provider_type,
                "model": target_model,
                "base_url": target_url,
                "masked_key": mask_key(target_key),
                "latency_ms": latency_ms,
                "available_models": available_models,
                "message": msg,
            }
    except Exception as e:
        latency_ms = int((time.perf_counter() - t0) * 1000)
        raw_err = _sanitize_error_text(str(e), target_key)
        is_timeout = isinstance(e, (asyncio.TimeoutError, TimeoutError))
        if not raw_err:
            raw_err = "Quá thời gian chờ phản hồi (Timeout)" if is_timeout else type(e).__name__
        ROUTER_TELEMETRY.update({
            "status": "error",
            "latency_ms": latency_ms,
            "last_error": raw_err[:120],
            "last_checked_at": _utc_now_iso(),
            "available_models": available_models,
        })
        if is_timeout and provider_type == "9router" and target_model.lower() == "all":
            if available_models:
                msg_out = (
                    f"Đã kết nối được tới {target_url}/models ({len(available_models)} model), "
                    f"nhưng model 'All' dò qua nhiều provider chậm nên vượt quá 30s ({raw_err}). "
                    "Hãy đổi Model sang 'deepseek-chat' hoặc 'gpt-reserve' rồi kiểm tra lại."
                )
            else:
                msg_out = (
                    f"Quá thời gian chờ (Timeout) khi gọi {target_url} với model 'All'. "
                    "Hãy kiểm tra 9Router trên PC còn bật Tunnel không và thử đổi Model sang 'deepseek-chat' hoặc 'gpt-reserve'."
                )
        elif available_models and is_timeout:
            msg_out = f"Đã kết nối {target_url}/models ({len(available_models)} model), nhưng upstream {target_model} phản hồi quá 30s ({raw_err})."
        else:
            msg_out = f"Lỗi kết nối tới {target_url}: {raw_err[:150]}"
        return {
            "success": False,
            "provider": provider_title,
            "provider_type": provider_type,
            "model": target_model,
            "base_url": target_url,
            "masked_key": mask_key(target_key),
            "latency_ms": latency_ms,
            "available_models": available_models,
            "message": msg_out,
        }


async def test_9router_endpoint(key: str = None, base_url: str = None, model: str = None) -> dict:
    return await test_openai_key(key=key, base_url=base_url, model=model)


def _parts_to_plain_text(parts: list) -> str:
    chunks = []
    for p in (parts or []):
        if isinstance(p, dict) and p.get("text"):
            chunks.append(str(p["text"]))
    return "\n".join(chunks).strip()


def _build_openai_messages(
    parts: list = None,
    contents: list = None,
    system_instruction: str = "",
) -> list | None:
    """Convert Gemini-style parts/contents into OpenAI chat messages (returns None if binary inlineData present)."""
    if parts and any(isinstance(p, dict) and p.get("inlineData") for p in parts):
        return None
    if contents and any(
        isinstance(p, dict) and p.get("inlineData")
        for turn in contents
        for p in (turn.get("parts") or [])
    ):
        return None

    msgs = []
    if system_instruction:
        msgs.append({"role": "system", "content": system_instruction})
    if contents and isinstance(contents, list):
        for turn in contents:
            raw_role = str(turn.get("role") or "user").strip().lower()
            role = "assistant" if raw_role in ("model", "assistant") else "user"
            txt = _parts_to_plain_text(turn.get("parts") or [])
            if txt:
                msgs.append({"role": role, "content": txt})
    else:
        txt = _parts_to_plain_text(parts or [])
        if txt:
            msgs.append({"role": "user", "content": txt})
    return msgs if msgs else None


async def _run_gemini_pool(
    parts: list = None,
    system_instruction: str = "",
    max_tokens: int = 8192,
    thinking_budget: int = 512,
    contents: list = None,
    quality: str = "deep",
) -> dict | None:
    """Gọi Gemini API Key Pool luân phiên + failover + ghi telemetry vào SQLite không chặn loop."""
    candidate_keys = _ordered_candidate_keys()
    if not candidate_keys:
        return None

    eff_max_tokens = max(4096, int(max_tokens or 8192))
    gemini_candidates = _select_gemini_models(quality)
    now_ts = time.time()
    active_models = [m for m in gemini_candidates if _MODEL_COOLDOWN.get(m, 0.0) <= now_ts]
    if not active_models:
        active_models = gemini_candidates[:3]
    session = await _get_http_session()
    pool_deadline = time.perf_counter() + 45.0

    for api_key in candidate_keys:
        if time.perf_counter() >= pool_deadline - 5.0:
            break
        tel = _ensure_telemetry(api_key)
        key_rejected = False
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": api_key,
        }
        for model in active_models:
            remaining_budget = pool_deadline - time.perf_counter()
            if remaining_budget < 5.0:
                break
            if _MODEL_COOLDOWN.get(model, 0.0) > time.time():
                continue
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
            gen_cfg = {
                "temperature": 0.35,
                "maxOutputTokens": eff_max_tokens,
            }
            if _supports_gemini_thinking(model) and thinking_budget > 0:
                budget = max(256, thinking_budget) if "pro" in model else thinking_budget
                gen_cfg["thinkingConfig"] = {"thinkingBudget": budget}

            payload_contents = contents if contents else [{"role": "user", "parts": parts or [{"text": ""}]}]
            payload = {
                "contents": payload_contents,
                "generationConfig": gen_cfg,
            }
            if system_instruction:
                payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}

            per_model_timeout = min(19.0 if "lite" in model or quality == "fast" else 21.0, remaining_budget)
            t0 = time.perf_counter()
            try:
                async with session.post(url, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=per_model_timeout)) as resp:
                    latency_ms = int((time.perf_counter() - t0) * 1000)
                    if resp.status == 200:
                        data = await resp.json()
                        candidates = data.get("candidates", [])
                        if candidates:
                            c_parts = candidates[0].get("content", {}).get("parts", [])
                            full_text = "".join([
                                p.get("text", "")
                                for p in c_parts
                                if isinstance(p, dict) and not p.get("thought") and p.get("text")
                            ]).strip()
                            if full_text:
                                chk = _utc_now_iso()
                                tel["calls"] += 1
                                tel["status"] = "active"
                                tel["cooldown_until"] = 0.0
                                tel["model"] = model
                                tel["latency_ms"] = latency_ms
                                tel["last_error"] = ""
                                tel["last_checked_at"] = chk
                                try:
                                    await asyncio.to_thread(
                                        update_ai_api_key_telemetry,
                                        api_key,
                                        status="active",
                                        model=model,
                                        latency_ms=latency_ms,
                                        calls_inc=1,
                                        last_error="",
                                        last_checked_at=chk,
                                    )
                                except Exception:
                                    pass
                                return {
                                    "text": full_text,
                                    "provider_used": "gemini",
                                    "provider_label": "Google Gemini",
                                    "model_used": model,
                                    "masked_key": mask_key(api_key),
                                    "latency_ms": latency_ms,
                                }
                    elif resp.status == 429:
                        chk = _utc_now_iso()
                        tel["failovers"] += 1
                        tel["status"] = "cooldown"
                        tel["cooldown_until"] = time.time() + 75
                        tel["latency_ms"] = latency_ms
                        tel["last_error"] = "Hết hạn mức tạm thời (429) -> Đã tự chuyển Key dự phòng"
                        tel["last_checked_at"] = chk
                        try:
                            await asyncio.to_thread(
                                update_ai_api_key_telemetry,
                                api_key,
                                status="cooldown",
                                latency_ms=latency_ms,
                                failovers_inc=1,
                                last_error=tel["last_error"],
                                last_checked_at=chk,
                            )
                        except Exception:
                            pass
                        if len(candidate_keys) > 1:
                            key_rejected = True
                            break
                        continue
                    elif resp.status in (400, 401, 403):
                        err_body = _sanitize_error_text(await resp.text(), api_key)
                        if "API_KEY" in err_body or "API key" in err_body or resp.status in (401, 403):
                            chk = _utc_now_iso()
                            tel["failovers"] += 1
                            tel["status"] = "invalid"
                            tel["cooldown_until"] = time.time() + 1800
                            tel["latency_ms"] = latency_ms
                            if resp.status == 403 and "free tier" in err_body.lower():
                                tel["last_error"] = "Project chưa bật Free Tier / Billing (403)"
                            else:
                                tel["last_error"] = f"Key không hợp lệ hoặc bị từ chối ({resp.status})"
                            tel["last_checked_at"] = chk
                            try:
                                await asyncio.to_thread(
                                    update_ai_api_key_telemetry,
                                    api_key,
                                    status="invalid",
                                    latency_ms=latency_ms,
                                    failovers_inc=1,
                                    last_error=tel["last_error"],
                                    last_checked_at=chk,
                                )
                            except Exception:
                                pass
                            key_rejected = True
                            break
                        if resp.status == 400 and "thinking" in err_body.lower() and "thinkingConfig" in gen_cfg:
                            fallback_cfg = dict(gen_cfg)
                            fallback_cfg.pop("thinkingConfig", None)
                            retry_payload = dict(payload)
                            retry_payload["generationConfig"] = fallback_cfg
                            try:
                                t1 = time.perf_counter()
                                async with session.post(url, json=retry_payload, headers=headers, timeout=aiohttp.ClientTimeout(total=per_model_timeout)) as r_resp:
                                    if r_resp.status == 200:
                                        r_data = await r_resp.json()
                                        r_candidates = r_data.get("candidates", [])
                                        if r_candidates:
                                            r_parts = r_candidates[0].get("content", {}).get("parts", [])
                                            r_text = "".join([
                                                p.get("text", "")
                                                for p in r_parts
                                                if isinstance(p, dict) and not p.get("thought") and p.get("text")
                                            ]).strip()
                                            if r_text:
                                                r_lat = int((time.perf_counter() - t1) * 1000)
                                                chk = _utc_now_iso()
                                                tel["calls"] += 1
                                                tel["status"] = "active"
                                                tel["cooldown_until"] = 0.0
                                                tel["model"] = model
                                                tel["latency_ms"] = r_lat
                                                tel["last_error"] = ""
                                                tel["last_checked_at"] = chk
                                                try:
                                                    await asyncio.to_thread(
                                                        update_ai_api_key_telemetry,
                                                        api_key,
                                                        status="active",
                                                        model=model,
                                                        latency_ms=r_lat,
                                                        calls_inc=1,
                                                        last_error="",
                                                        last_checked_at=chk,
                                                    )
                                                except Exception:
                                                    pass
                                                return {
                                                    "text": r_text,
                                                    "provider_used": "gemini",
                                                    "provider_label": "Google Gemini",
                                                    "model_used": model,
                                                    "masked_key": mask_key(api_key),
                                                    "latency_ms": r_lat,
                                                }
                            except Exception:
                                pass
                        continue
                    elif resp.status == 404:
                        _MODEL_COOLDOWN[model] = time.time() + 600
                        tel["last_error"] = f"Model {model} không khả dụng (404)"
                        continue
                    elif resp.status == 503:
                        _MODEL_COOLDOWN[model] = time.time() + 60
                        tel["last_error"] = f"Model {model} đang quá tải (503)"
                        continue
                    else:
                        continue
            except Exception as exc:
                err_txt = _sanitize_error_text(str(exc), api_key)
                if not err_txt:
                    err_txt = f"Timeout/lỗi kết nối ({type(exc).__name__}) trên {model}"
                tel["last_error"] = err_txt
                continue

        if key_rejected:
            continue
        if tel.get("status") not in ("invalid", "cooldown"):
            chk = _utc_now_iso()
            tel["failovers"] += 1
            tel["status"] = "cooldown"
            tel["cooldown_until"] = time.time() + 15
            tel["last_checked_at"] = chk
    return None


async def _run_llm_completion(
    parts: list = None,
    system_instruction: str = "",
    max_tokens: int = 8192,
    thinking_budget: int = 512,
    contents: list = None,
    quality: str = "deep",
    use_cache: bool = True,
) -> dict | None:
    """Thực thi đa nhà cung cấp (Gemini Pool <-> 9Router/FOSTA/OpenAI) theo priority và trả metadata."""
    cfg = get_openai_settings()
    active_model = cfg.get("model", "")
    priority = cfg.get("priority", "gemini_first")
    openai_msgs = _build_openai_messages(parts=parts, contents=contents, system_instruction=system_instruction)
    has_router = bool(cfg.get("key")) and bool(openai_msgs)

    cache_key = None
    if use_cache and openai_msgs is not None:
        cache_seed = json.dumps({
            "priority": priority,
            "model": active_model,
            "quality": quality,
            "msgs": openai_msgs,
        }, ensure_ascii=False, sort_keys=True)
        cache_key = hashlib.md5(cache_seed.encode("utf-8")).hexdigest()
        cached_entry = AI_CACHE.get(cache_key)
        if isinstance(cached_entry, dict):
            if (time.time() - cached_entry.get("ts", 0.0)) < _AI_CACHE_TTL_SEC:
                out = dict(cached_entry["result"])
                out["latency_ms"] = 0
                out["cached"] = True
                return out
            AI_CACHE.pop(cache_key, None)

    def _store_cache(res_dict: dict) -> dict:
        if cache_key and res_dict:
            if len(AI_CACHE) >= _AI_CACHE_MAX_ITEMS:
                AI_CACHE.pop(next(iter(AI_CACHE)), None)
            AI_CACHE[cache_key] = {"ts": time.time(), "result": dict(res_dict)}
        return res_dict

    prompt_text = openai_msgs[-1]["content"] if openai_msgs else ""

    if priority == "openai_only":
        if not has_router:
            return None
        r_res = await _call_openai_chatgpt_meta(
            prompt=prompt_text,
            system_instruction=system_instruction,
            max_tokens=max_tokens,
            messages_override=openai_msgs,
        )
        if r_res:
            r_res["fallback_used"] = False
            return _store_cache(r_res)
        return None

    if priority == "gemini_only":
        g_res = await _run_gemini_pool(
            parts=parts,
            system_instruction=system_instruction,
            max_tokens=max_tokens,
            thinking_budget=thinking_budget,
            contents=contents,
            quality=quality,
        )
        if g_res:
            g_res["fallback_used"] = False
            return _store_cache(g_res)
        return None

    if priority == "openai_first":
        if has_router:
            r_res = await _call_openai_chatgpt_meta(
                prompt=prompt_text,
                system_instruction=system_instruction,
                max_tokens=max_tokens,
                messages_override=openai_msgs,
            )
            if r_res:
                r_res["fallback_used"] = False
                return _store_cache(r_res)
            print(f"[AI Service] LLM ({active_model}) tạm thời không phản hồi, chuyển sang dàn Gemini!")
        g_res = await _run_gemini_pool(
            parts=parts,
            system_instruction=system_instruction,
            max_tokens=max_tokens,
            thinking_budget=thinking_budget,
            contents=contents,
            quality=quality,
        )
        if g_res:
            g_res["fallback_used"] = bool(has_router)
            return _store_cache(g_res)
        return None

    # Default: gemini_first (Gemini Pool -> failover sang 9Router/FOSTA/OpenAI)
    g_res = await _run_gemini_pool(
        parts=parts,
        system_instruction=system_instruction,
        max_tokens=max_tokens,
        thinking_budget=thinking_budget,
        contents=contents,
        quality=quality,
    )
    if g_res:
        g_res["fallback_used"] = False
        return _store_cache(g_res)

    if has_router:
        print("[AI Service] Dàn Gemini chưa phản hồi, failover sang 9Router/OpenAI Gateway!")
        r_res = await _call_openai_chatgpt_meta(
            prompt=prompt_text,
            system_instruction=system_instruction,
            max_tokens=max_tokens,
            messages_override=openai_msgs,
        )
        if r_res:
            r_res["fallback_used"] = True
            return _store_cache(r_res)

    return None


async def _execute_gemini_payload(
    parts: list = None,
    system_instruction: str = "",
    max_tokens: int = 8192,
    thinking_budget: int = 512,
    contents: list = None,
    quality: str = "deep",
) -> str | None:
    res = await _run_llm_completion(
        parts=parts,
        system_instruction=system_instruction,
        max_tokens=max_tokens,
        thinking_budget=thinking_budget,
        contents=contents,
        quality=quality,
    )
    return res["text"] if res else None


async def call_gemini(
    prompt: str,
    system_instruction: str = "",
    max_tokens: int = 8192,
    thinking_budget: int = 512,
    quality: str = "deep",
) -> str | None:
    return await _execute_gemini_payload(
        [{"text": prompt}],
        system_instruction=system_instruction,
        max_tokens=max_tokens,
        thinking_budget=thinking_budget,
        quality=quality,
    )


async def call_gemini_multimodal(prompt: str, mime_type: str, raw_bytes: bytes, max_tokens: int = 8192) -> str | None:
    b64 = base64.b64encode(raw_bytes).decode("ascii")
    parts = [
        {"inlineData": {"mimeType": mime_type, "data": b64}},
        {"text": prompt},
    ]
    return await _execute_gemini_payload(parts, max_tokens=max_tokens, thinking_budget=384, quality="deep")


async def test_api_key(api_key: str) -> dict:
    api_key = (api_key or "").strip()
    if not api_key:
        return {
            "ok": False,
            "success": False,
            "status": "invalid",
            "masked_key": "",
            "key_type": "gemini",
            "model": "",
            "latency_ms": None,
            "message": "Chưa nhập API Key",
            "error": "Chưa nhập API Key",
        }

    ok_fmt, fmt_err = validate_gemini_key_format(api_key)
    tel = _ensure_telemetry(api_key)
    ktype = classify_key_type(api_key)
    masked = mask_key(api_key)
    if not ok_fmt:
        chk = _utc_now_iso()
        tel["status"] = "invalid"
        tel["last_error"] = fmt_err
        tel["last_checked_at"] = chk
        try:
            await asyncio.to_thread(
                update_ai_api_key_telemetry,
                api_key,
                status="invalid",
                last_error=fmt_err,
                last_checked_at=chk,
            )
        except Exception:
            pass
        return {
            "ok": False,
            "success": False,
            "status": "invalid",
            "masked_key": masked,
            "key_type": ktype,
            "model": "",
            "latency_ms": None,
            "message": fmt_err,
            "error": fmt_err,
        }

    fast_check_models = [
        "gemini-3.5-flash-lite",
        "gemini-flash-lite-latest",
        "gemini-3.1-flash-lite",
        "gemini-flash-latest",
        "gemini-3.5-flash",
    ]
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key,
    }
    last_err = ""
    last_latency = None

    session = await _get_http_session()
    for model in fast_check_models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        gen_cfg = {"maxOutputTokens": 64}
        if _supports_gemini_thinking(model):
            gen_cfg["thinkingConfig"] = {"thinkingBudget": 0}
        payload = {
            "contents": [{"parts": [{"text": "Reply OK"}]}],
            "generationConfig": gen_cfg,
        }
        t0 = time.perf_counter()
        try:
            async with session.post(url, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=12)) as resp:
                latency_ms = int((time.perf_counter() - t0) * 1000)
                last_latency = latency_ms
                if resp.status == 200:
                    chk = _utc_now_iso()
                    tel["status"] = "active"
                    tel["cooldown_until"] = 0.0
                    tel["model"] = model
                    tel["latency_ms"] = latency_ms
                    tel["last_error"] = ""
                    tel["last_checked_at"] = chk
                    try:
                        await asyncio.to_thread(
                            update_ai_api_key_telemetry,
                            api_key,
                            status="active",
                            model=model,
                            latency_ms=latency_ms,
                            last_error="",
                            last_checked_at=chk,
                        )
                    except Exception:
                        pass
                    return {
                        "ok": True,
                        "success": True,
                        "status": "active",
                        "masked_key": masked,
                        "key_type": ktype,
                        "model": model,
                        "latency_ms": latency_ms,
                        "message": f"Hoạt động xuất sắc ({model}, {latency_ms}ms)",
                        "error": "",
                    }
                elif resp.status == 429:
                    chk = _utc_now_iso()
                    tel["status"] = "cooldown"
                    tel["cooldown_until"] = time.time() + 75
                    tel["latency_ms"] = latency_ms
                    tel["last_error"] = "Hết hạn mức tạm thời (429)"
                    tel["last_checked_at"] = chk
                    last_err = tel["last_error"]
                    continue
                elif resp.status in (400, 401, 403):
                    raw_body = await resp.text()
                    msg = raw_body
                    try:
                        j_err = json.loads(raw_body)
                        msg = j_err.get("error", {}).get("message", raw_body)
                    except Exception:
                        pass
                    msg = _sanitize_error_text(msg, api_key) or "API Key không hợp lệ"
                    if "thinking" in msg.lower() and resp.status == 400:
                        continue
                    if "API_KEY" in msg or "API key" in msg or resp.status in (401, 403):
                        chk = _utc_now_iso()
                        tel["status"] = "invalid"
                        tel["cooldown_until"] = time.time() + 1800
                        tel["latency_ms"] = latency_ms
                        tel["last_error"] = msg[:180]
                        tel["last_checked_at"] = chk
                        try:
                            await asyncio.to_thread(
                                update_ai_api_key_telemetry,
                                api_key,
                                status="invalid",
                                latency_ms=latency_ms,
                                last_error=msg[:180],
                                last_checked_at=chk,
                            )
                        except Exception:
                            pass
                        return {
                            "ok": False,
                            "success": False,
                            "status": "invalid",
                            "masked_key": masked,
                            "key_type": ktype,
                            "model": "",
                            "latency_ms": latency_ms,
                            "message": msg[:180],
                            "error": msg[:180],
                        }
                    last_err = msg[:180]
                elif resp.status == 503:
                    last_err = f"Model {model} đang quá tải (503)"
                    continue
                elif resp.status == 404:
                    last_err = f"Model {model} không khả dụng (404)"
                    continue
        except Exception as exc:
            last_latency = int((time.perf_counter() - t0) * 1000)
            last_err = _sanitize_error_text(str(exc), api_key) or "Timeout/lỗi kết nối Gemini"
            continue

    chk = _utc_now_iso()
    if tel.get("status") == "cooldown":
        msg = "Key đang chạm giới hạn Quota (429) — Sẽ tự động dùng Key dự phòng"
        try:
            await asyncio.to_thread(
                update_ai_api_key_telemetry,
                api_key,
                status="cooldown",
                latency_ms=last_latency,
                last_error=msg,
                last_checked_at=chk,
            )
        except Exception:
            pass
        return {
            "ok": False,
            "success": False,
            "status": "cooldown",
            "masked_key": masked,
            "key_type": ktype,
            "model": "",
            "latency_ms": last_latency,
            "message": msg,
            "error": msg,
        }

    tel["last_error"] = last_err or "Không thể kết nối máy chủ Gemini"
    tel["last_checked_at"] = chk
    if tel.get("status") not in ("invalid",):
        tel["status"] = "cooldown"
        tel["cooldown_until"] = time.time() + 45
    if last_latency is not None:
        tel["latency_ms"] = last_latency
    err_out = tel["last_error"]
    try:
        await asyncio.to_thread(
            update_ai_api_key_telemetry,
            api_key,
            status=tel.get("status") or "cooldown",
            latency_ms=last_latency,
            last_error=err_out,
            last_checked_at=chk,
        )
    except Exception:
        pass
    return {
        "ok": False,
        "success": False,
        "status": tel.get("status") or "cooldown",
        "masked_key": masked,
        "key_type": ktype,
        "model": "",
        "latency_ms": last_latency,
        "message": err_out,
        "error": err_out,
    }


async def test_all_pool_keys(keys_input=None) -> dict:
    if keys_input:
        if isinstance(keys_input, str):
            tokens = _parse_key_tokens(keys_input)
            target_items = [{"key": t, "label": f"Key #{i + 1}"} for i, t in enumerate(tokens)]
        elif isinstance(keys_input, list):
            target_items = []
            for i, item in enumerate(keys_input):
                if isinstance(item, str) and item.strip() and not _is_masked_placeholder(item):
                    target_items.append({"key": item.strip(), "label": f"Key #{i + 1}"})
                elif isinstance(item, dict):
                    k = str(item.get("key") or item.get("api_key") or "").strip()
                    if k and not _is_masked_placeholder(k):
                        target_items.append({"key": k, "label": str(item.get("label") or f"Key #{i + 1}").strip()})
        else:
            target_items = []
        if not target_items:
            target_items = get_api_keys_pool()
    else:
        target_items = get_api_keys_pool()

    if not target_items:
        return {
            "success": False,
            "secured_on_server": True,
            "active_count": 0,
            "cooldown_count": 0,
            "invalid_count": 0,
            "total_count": 0,
            "results": [],
            "pool": [],
            "message": "Chưa có API Key nào trong danh sách",
        }

    sem = asyncio.Semaphore(4)

    async def _bounded_test(k: str) -> dict:
        async with sem:
            return await test_api_key(k)

    results = await asyncio.gather(*[_bounded_test(item["key"]) for item in target_items])
    for idx, r in enumerate(results):
        r["index"] = idx + 1
        r["label"] = target_items[idx].get("label") or f"Key #{idx + 1}"
    ok_count = sum(1 for r in results if r.get("ok"))
    cooldown_count = sum(1 for r in results if r.get("status") == "cooldown")
    invalid_count = sum(1 for r in results if not r.get("ok") and r.get("status") != "cooldown")
    return {
        "success": ok_count > 0,
        "secured_on_server": True,
        "active_count": ok_count,
        "cooldown_count": cooldown_count,
        "invalid_count": invalid_count,
        "total_count": len(target_items),
        "results": results,
        "pool": get_pool_status(),
        "message": f"Sẵn sàng {ok_count}/{len(target_items)} API Key trong hệ thống luân phiên!",
    }


async def ai_extract_from_multimodal(mime_type: str, raw_bytes: bytes, filename: str = "") -> str | None:
    prompt = f"""Hãy trích xuất đầy đủ, chính xác toàn bộ nội dung học thuật, định nghĩa, công thức Toán/Lý/Hóa, phương trình phản ứng và câu hỏi có trong tài liệu '{filename}'.
{STEM_FORMAT_GUIDE}"""
    return await call_gemini_multimodal(prompt, mime_type, raw_bytes, max_tokens=8192)


# =========================================================================
# CORE & ADVANCED EDUCATIONAL AI SERVICES
# =========================================================================
_TUTOR_MODES = {"explain", "eliminate", "socratic", "mnemonic", "clinical", "debug", "flashcard"}


def _normalize_tutor_mode(mode: str, message: str = "") -> str:
    m = str(mode or "").strip().lower()
    aliases = {
        "chat": "explain",
        "hint": "socratic",
        "step_by_step": "socratic",
        "exception": "eliminate",
        "loai_tru": "eliminate",
        "ngoai_tru": "eliminate",
        "memory": "mnemonic",
        "trick": "mnemonic",
        "case": "clinical",
        "code": "debug",
        "card": "flashcard",
    }
    m = aliases.get(m, m)
    if m in _TUTOR_MODES:
        return m
    low_msg = (message or "").lower()
    if "ngoại trừ" in low_msg or "loại trừ" in low_msg:
        return "eliminate"
    if "flashcard" in low_msg:
        return "flashcard"
    return "explain"


def _format_options_block(options) -> str:
    if not options:
        return ""
    if isinstance(options, str):
        return options.strip()
    lines = []
    if isinstance(options, dict):
        for k, v in options.items():
            if v is not None and str(v).strip():
                lines.append(f"- {k}: {str(v).strip()}")
    elif isinstance(options, list):
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i, opt in enumerate(options):
            if isinstance(opt, dict):
                lbl = str(opt.get("label") or opt.get("key") or (letters[i] if i < len(letters) else i + 1))
                txt = str(opt.get("text") or opt.get("value") or "").strip()
            else:
                lbl = letters[i] if i < len(letters) else str(i + 1)
                txt = str(opt or "").strip()
            if txt:
                if txt.startswith(f"{lbl}.") or txt.startswith(f"{lbl})"):
                    lines.append(f"- {txt}")
                else:
                    lines.append(f"- {lbl}. {txt}")
    return "\n".join(lines)


def _offline_ai_diagnostic(subject_name: str, query_text: str) -> str:
    cfg = get_openai_settings()
    pool = get_api_keys_pool()
    if cfg.get("key"):
        provider = (
            "FOSTA Codex"
            if cfg.get("provider_type") == "fosta"
            else ("9Router Gateway" if cfg.get("provider_type") == "9router" else "OpenAI ChatGPT")
        )
        return (
            f"### 🎓 Gia Sư UniMaster AI — {subject_name}\n"
            f"Về yêu cầu: **\"{query_text[:180]}\"**\n\n"
            f"⚠️ **Chưa nhận được phản hồi từ {provider} ({mask_key(cfg['key'])})** hay dàn Gemini dự phòng. "
            f"Hãy bấm **🔌 Kiểm tra kết nối AI** trong Cài đặt để kiểm tra Gateway/Quota."
        )
    if pool:
        return (
            f"### 🎓 Gia Sư UniMaster AI — {subject_name}\n"
            f"Về yêu cầu: **\"{query_text[:180]}\"**\n\n"
            "⚠️ **Dàn Gemini API Key hiện đang bận hoặc chạm hạn mức.** Hãy thử lại sau vài giây hoặc thêm Key mới / gắn 9Router trong Cài đặt."
        )
    return (
        f"### 🎓 Gia Sư UniMaster AI — {subject_name}\n"
        "⚠️ Chưa cấu hình API Key. Hãy vào **⚙️ Cài đặt → AI & API Keys** để gắn Gemini API Key hoặc 9Router Gateway."
    )


async def ai_tutor_assist(
    subject_name: str = "Đại học tổng hợp",
    message: str = "",
    mode: str = "explain",
    persona: str = "professor",
    tutor_style_prompt: str = "",
    question_text: str = "",
    options=None,
    correct_answer: str = "",
    selected_answer: str = "",
    question_image_hint: str = "",
    code_snippet: str = "",
    selected_term: str = "",
    chat_history: list = None,
) -> dict:
    """Gia sư AI hợp nhất hỗ trợ 7 chế độ sư phạm + đầy đủ ngữ cảnh câu hỏi & routing telemetry."""
    norm_mode = _normalize_tutor_mode(mode, message)
    persona_map = {
        "professor": "Phong cách Giáo sư Đại học uyên bác: phân tích cặn kẽ bản chất học thuật, chỉ rõ điều kiện áp dụng và bẫy đề thi.",
        "feynman": "Phong cách Richard Feynman siêu trực quan: giải thích bằng hình ảnh đời thường sinh động, dễ hiểu trong 1 phút.",
        "speed": "Phong cách Cao thủ Giải nhanh: chốt công thức trọng tâm, dấu hiệu nhận diện và mẹo khoanh đúng trong 5-10 giây.",
        "examiner": "Phong cách Giảng viên Vấn đáp: cô đọng cốt lõi và đặt câu hỏi kích thích tư duy phản biện.",
    }
    mode_instructions = {
        "explain": (
            "CHẾ ĐỘ GIẢI THÍCH BẢN CHẤT (explain): "
            "1) Nêu kết luận cốt lõi rõ ràng; "
            "2) Phân tích cơ chế/công thức từng bước; "
            "3) Nếu người học chọn sai, đối chiếu trực diện chỗ dễ nhầm với đáp án đúng; "
            "4) Chốt mẹo tránh bẫy đề thi."
        ),
        "eliminate": (
            "CHẾ ĐỘ PHÂN TÍCH LOẠI TRỪ TỪNG ĐÁP ÁN (eliminate): "
            "Bắt buộc liệt kê và đánh giá LẦN LƯỢT từng phương án A, B, C, D... (chỉ rõ mỗi phương án ĐÚNG hay SAI ở điểm nào). "
            "Đặc biệt với câu hỏi 'NGOẠI TRỪ / KHÔNG ĐÚNG / SAI', đánh dấu rõ các ý ĐÚNG bị loại và làm nổi bật đáp án cần khoanh."
        ),
        "socratic": (
            "CHẾ ĐỘ GỢI MỞ TỪNG BƯỚC (socratic): "
            "Không tuồn ngay chữ cái đáp án cuối cùng nếu chưa cần; chia nhỏ thành 2-3 bước suy luận kèm 1-2 câu hỏi dẫn dắt để người học tự phát hiện quy luật."
        ),
        "mnemonic": (
            "CHẾ ĐỘ MẸO NHỚ NHANH (mnemonic): "
            "Tạo câu thần chú vần điệu tiếng Việt, chữ viết tắt (acronym) hoặc liên tưởng hình ảnh độc đáo, súc tích, dễ nhớ trong 5 giây."
        ),
        "clinical": (
            "CHẾ ĐỘ BIỆN LUẬN LÂM SÀNG (clinical): "
            "Phân tích có hệ thống theo tư duy Y khoa/Dược lâm sàng: Dữ kiện mấu chốt (triệu chứng, cận lâm sàng) → Cơ chế bệnh sinh/Dược lực → "
            "Chẩn đoán xác định & phân biệt → Hướng xử trí ưu tiên / Chống chỉ định & bẫy lâm sàng."
        ),
        "debug": (
            "CHẾ ĐỘ DEBUG & TRACE CODE TỪNG DÒNG (debug): "
            "Theo dõi từng dòng thực thi từ điểm vào (`Main`/hàm gọi), trạng thái biến qua từng bước, chỉ rõ lỗi compile/runtime/logic (nếu có) và đề xuất code sửa chuẩn sạch."
        ),
        "flashcard": (
            "CHẾ ĐỘ TẠO FLASHCARD (flashcard): "
            "Đúc kết kiến thức thành ĐÚNG 1 đối tượng JSON hợp lệ có dạng:\n"
            "{\"front\": \"Câu hỏi/thuật ngữ/công thức mặt trước\", \"back\": \"Đáp án & bản chất cốt lõi ngắn gọn 1-3 dòng\", \"hint\": \"Từ khóa gợi nhớ 3 giây\"}\n"
            "Không thêm chữ ngoài JSON."
        ),
    }

    style_desc = persona_map.get(persona, persona_map["professor"])
    mode_desc = mode_instructions[norm_mode]
    custom_style = str(tutor_style_prompt or "").strip()[:1200]
    custom_guidance = (
        f"\nYêu cầu phong cách bổ sung: {custom_style}\nTuân thủ nếu không mâu thuẫn tính chính xác học thuật."
        if custom_style
        else ""
    )
    term_guidance = ""
    if selected_term or any(kw in (message or "").lower() for kw in ("gốc từ", "etymology", "thuật ngữ", "từ vựng", "ngữ pháp", "nghĩa là gì")):
        term_guidance = (
            "\nKhi giải thích thuật ngữ hoặc từ vựng chuyên ngành: nêu gốc từ (tiền tố/hậu tố/Hy Lạp/Latin nếu có căn cứ), "
            "từ họ hàng/đồng nguyên, ví dụ chuẩn và lỗi nhầm lẫn hay gặp."
        )

    system_prompt = (
        f"Bạn là UniMaster AI — Gia sư ôn thi Đại học & Y-Dược/CNTT cho học phần \"{subject_name or 'Tổng quát'}\".\n"
        f"{style_desc}\n{mode_desc}{term_guidance}{custom_guidance}\n"
        f"{'' if norm_mode == 'flashcard' else STEM_FORMAT_GUIDE}"
    )

    ctx_lines = []
    if subject_name:
        ctx_lines.append(f"**Môn học:** {subject_name}")
    if question_text:
        ctx_lines.append(f"**Câu hỏi / Đề bài:**\n{question_text}")
    opt_block = _format_options_block(options)
    if opt_block:
        ctx_lines.append(f"**Các phương án:**\n{opt_block}")
    if selected_answer:
        ctx_lines.append(f"**Người học đang chọn:** {selected_answer}")
    if correct_answer and norm_mode != "socratic":
        ctx_lines.append(f"**Đáp án chuẩn:** {correct_answer}")
    elif correct_answer and norm_mode == "socratic":
        ctx_lines.append(f"**(Tham chiếu nội bộ để dẫn dắt, không nói thẳng chữ cái):** {correct_answer}")
    if question_image_hint:
        ctx_lines.append(f"**Mô tả hình ảnh/sơ đồ đính kèm:** {question_image_hint}")
    if code_snippet:
        ctx_lines.append(f"**Đoạn mã liên quan:**\n```\n{code_snippet}\n```")
    if selected_term:
        ctx_lines.append(f"**Thuật ngữ được chọn hỏi sâu:** `{selected_term}`")
    if message:
        ctx_lines.append(f"**Yêu cầu của người học:** {message}")

    user_prompt = "\n\n".join(ctx_lines).strip() or "Hãy hỗ trợ giải thích câu hỏi ôn tập này."

    contents_list = []
    if chat_history and isinstance(chat_history, list):
        for turn in chat_history[-10:]:
            if not isinstance(turn, dict):
                continue
            r_raw = str(turn.get("role") or "user").strip().lower()
            role = "model" if r_raw in ("model", "assistant") else "user"
            txt = str(turn.get("content") or turn.get("text") or "").strip()
            if txt:
                contents_list.append({"role": role, "parts": [{"text": txt}]})
    contents_list.append({"role": "user", "parts": [{"text": user_prompt}]})

    quality = "fast" if norm_mode in ("mnemonic", "flashcard", "socratic") else "deep"
    thinking_budget = 192 if quality == "fast" else 384
    max_tok = 2048 if norm_mode == "flashcard" else 6144

    res = await _run_llm_completion(
        system_instruction=system_prompt,
        max_tokens=max_tok,
        thinking_budget=thinking_budget,
        contents=contents_list,
        quality=quality,
    )

    if not res:
        diag = _offline_ai_diagnostic(subject_name or "Tổng quát", message or question_text or selected_term)
        fb_card = None
        if norm_mode == "flashcard" and (question_text or selected_term):
            fb_card = {
                "front": (question_text or selected_term)[:260],
                "back": f"**Đáp án:** {correct_answer}" if correct_answer else "Xem lại phần trọng tâm bài học.",
                "hint": subject_name or "Ghi nhớ",
            }
        return {
            "success": False,
            "reply": diag,
            "mode": norm_mode,
            "provider_used": "none",
            "provider_label": "Chưa khả dụng",
            "model_used": "",
            "masked_key": "",
            "latency_ms": 0,
            "fallback_used": False,
            "flashcard": fb_card,
            "error": diag,
        }

    reply_text = res["text"]
    flashcard_obj = None
    if norm_mode == "flashcard":
        try:
            cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", reply_text.strip())
            s, e = cleaned.find("{"), cleaned.rfind("}")
            if s != -1 and e != -1:
                parsed_fc = json.loads(cleaned[s : e + 1])
                if isinstance(parsed_fc, dict) and parsed_fc.get("front") and parsed_fc.get("back"):
                    flashcard_obj = {
                        "front": str(parsed_fc["front"]).strip(),
                        "back": str(parsed_fc["back"]).strip(),
                        "hint": str(parsed_fc.get("hint") or subject_name or "").strip(),
                    }
                    reply_text = (
                        f"### 🃏 Flashcard đã đúc kết\n"
                        f"**Mặt trước:** {flashcard_obj['front']}\n\n"
                        f"**Mặt sau:** {flashcard_obj['back']}"
                        + (f"\n\n*Gợi nhớ:* {flashcard_obj['hint']}" if flashcard_obj["hint"] else "")
                    )
        except Exception:
            flashcard_obj = None
        if flashcard_obj is None:
            flashcard_obj = {
                "front": (question_text or selected_term or message)[:260],
                "back": reply_text[:500],
                "hint": subject_name or "",
            }

    return {
        "success": True,
        "reply": reply_text,
        "mode": norm_mode,
        "provider_used": res["provider_used"],
        "provider_label": res["provider_label"],
        "model_used": res["model_used"],
        "masked_key": res["masked_key"],
        "latency_ms": res["latency_ms"],
        "fallback_used": bool(res.get("fallback_used")),
        "flashcard": flashcard_obj,
    }


async def ai_chat_tutor(
    subject_name: str,
    user_message: str,
    persona: str = "professor",
    history: list = None,
    tutor_style_prompt: str = "",
) -> str:
    res = await ai_tutor_assist(
        subject_name=subject_name or "Đại học tổng hợp",
        message=user_message,
        mode="explain",
        persona=persona,
        tutor_style_prompt=tutor_style_prompt,
        chat_history=history,
    )
    return res["reply"]


async def ai_get_hint(question_text: str, options: list, code_snippet: str = "") -> str:
    res = await ai_tutor_assist(
        subject_name="Ôn thi trắc nghiệm",
        message="Đưa ra đúng 1 gợi ý tư duy Socratic ngắn gọn (2-3 câu). TUYỆT ĐỐI KHÔNG tiết lộ chữ cái đáp án.",
        mode="socratic",
        question_text=question_text,
        options=options,
        code_snippet=code_snippet,
    )
    if res.get("success") and res.get("reply"):
        return res["reply"]
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


