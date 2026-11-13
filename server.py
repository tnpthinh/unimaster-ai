r"""
UniMaster AI v7.0 - High-Performance Async Backend Server (aiohttp)
Equipped with:
- Multi-API Key Auto-Failover Pool & Concurrent Health Check
- Universal Document Ingestion (.pdf, .pptx, .ppt, .docx, .doc, .xlsx, .csv, images, code)
- STEM Subjects (Math, Physics, Chemistry, Biology) + Smart Decimal Grading (2,24 == 2.24)
- Rich AI Action Endpoints: Concept Recall, Mistake Diagnosis, 5s Mnemonic, Flashcard Distiller,
  1-Click Curriculum Bank Expander, 4-Persona Tutor, Essay Grader & Complete 5-Day Study Roadmap
- Multi-Device Wi-Fi QR Sync & Standalone Offline App Exporter
"""
import os
import re
import json
import time
import hmac
import base64
import socket
import hashlib
import secrets
import random
import asyncio
import sqlite3
import tempfile
from datetime import datetime, timezone
import aiohttp
from aiohttp import web
import database as db
import ai_service as ai
import document_parser as doc_parser
import catalog_seed
import stem_seed
import seed_hoasinh_ctump
import extensions
import code_engine

# Ensure .env is loaded even if imported outside __main__
db.load_env_file()

# Cloud hosts (Render / Railway / Fly.io / Hugging Face) inject PORT; fallback 8080 for local PC
PORT = int(os.environ.get("PORT", "8080"))
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

# ==========================================
# Online Access Protection (bắt buộc khi đưa lên Internet)
# Đặt biến môi trường APP_PASSWORD để bật màn hình đăng nhập.
# Không đặt -> chạy chế độ nội bộ (PC / Wi-Fi gia đình) như cũ.
# ==========================================
APP_PASSWORD = os.environ.get("APP_PASSWORD", "").strip()
REQUIRE_AUTH = os.environ.get("REQUIRE_AUTH", "").strip().lower() in ("1", "true", "yes", "on")
AUTH_ENABLED = bool(APP_PASSWORD or REQUIRE_AUTH)
SESSION_COOKIE = "um_session"
SESSION_DAYS = 30
_SESSION_KEY = hashlib.sha256(
    (os.environ.get("SESSION_SECRET", "") + "|" + (APP_PASSWORD or os.environ.get("REQUIRE_AUTH", "")) + "|unimaster-v7").encode("utf-8")
).digest()
_LOGIN_FAILS = {}  # ip -> [fail_count, locked_until]
_RATE_LIMIT_BUCKETS = {}  # (bucket, ip) -> [timestamps]
AUTH_EXEMPT_PATHS = {
    "/login", "/api/login", "/api/auth/login", "/api/auth/register",
    "/manifest.json", "/icon.svg", "/healthz",
    "/ws/arena", "/api/export/anki", "/api/export/printable-exam"
}


def _make_session_token(user_id=1, role="admin"):
    expires = int(time.time()) + SESSION_DAYS * 86400
    nonce = secrets.token_hex(8)
    payload = f"{user_id}.{role}.{expires}.{nonce}"
    sig = hmac.new(_SESSION_KEY, payload.encode(), hashlib.sha256).hexdigest()
    return f"{payload}.{sig}"


def _parse_session_token(token: str):
    if not token:
        return None
    try:
        parts = token.split(".")
        if len(parts) == 5:
            uid, role, expires, nonce, sig = parts
            payload = f"{uid}.{role}.{expires}.{nonce}"
            expected = hmac.new(_SESSION_KEY, payload.encode(), hashlib.sha256).hexdigest()
            if hmac.compare_digest(sig, expected) and int(expires) > time.time():
                return {"id": int(uid), "role": role}
        elif len(parts) == 3:
            # Backwards compatibility for legacy session tokens
            expires, nonce, sig = parts
            expected = hmac.new(_SESSION_KEY, f"{expires}.{nonce}".encode(), hashlib.sha256).hexdigest()
            if hmac.compare_digest(sig, expected) and int(expires) > time.time():
                return {"id": 1, "role": "admin"}
    except Exception:
        pass
    return None


def _valid_session_token(token: str) -> bool:
    return _parse_session_token(token) is not None


def _client_ip(request):
    return (
        request.headers.get("CF-Connecting-IP")
        or request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
        or request.remote
        or "unknown"
    )


def _is_https(request):
    return request.secure or request.headers.get("X-Forwarded-Proto", "").lower() == "https"


def _storage_is_ephemeral() -> bool:
    """True nếu dữ liệu (tài khoản + nhật ký đăng nhập) sẽ MẤT khi Render khởi động lại/deploy lại.

    Render free không có ổ đĩa bền vững: mọi thứ ghi ngoài ổ đĩa gắn kèm (vd /tmp) bị xóa
    mỗi lần container ngủ dậy hoặc deploy -> database quay về bản seed (không có user, không có lịch sử).
    """
    path = os.path.abspath(db.DB_PATH).replace("\\", "/")
    on_cloud = bool(os.environ.get("RENDER") or os.environ.get("RAILWAY_ENVIRONMENT") or os.environ.get("FLY_APP_NAME"))
    return on_cloud and (path.startswith("/tmp") or not os.environ.get("DATA_DIR", "").strip())


# Chống ghi DB quá dày: mỗi người dùng chỉ được "chạm" tối đa 1 lần / 5 phút (trong RAM)
_SEEN_THROTTLE = {}


def _note_user_activity(request, user_info):
    """Ghi nhận người dùng quay lại bằng cookie phiên (không cần nhập lại mật khẩu).

    Cookie phiên sống 30 ngày -> phần lớn người dùng không đăng nhập lại, nên nếu chỉ log lúc
    nhập mật khẩu thì lịch sử trông như 'không ai đăng nhập'.
    """
    uid = user_info.get("id") if user_info else None
    if not uid or user_info.get("role") == "guest":
        return
    now = time.time()
    if now - _SEEN_THROTTLE.get(uid, 0) < 300:
        return
    _SEEN_THROTTLE[uid] = now
    try:
        if db.touch_user_seen(uid, 0):
            db.record_login_event(uid, _client_ip(request), request.headers.get("User-Agent", ""), "session")
    except Exception as exc:  # nhật ký không bao giờ được làm hỏng request chính
        print(f"⚠️ Không ghi được hoạt động người dùng: {exc}")


def _check_rate_limit(request, bucket: str = "ai_test", limit: int = 15, window_sec: int = 60) -> tuple[bool, int]:
    """Sliding-window rate limiter per (bucket, ip) protecting AI probe endpoints."""
    now = time.time()
    ip = _client_ip(request)
    key = (bucket, ip)
    recent = [ts for ts in _RATE_LIMIT_BUCKETS.get(key, []) if (now - ts) < window_sec]
    if len(recent) >= limit:
        _RATE_LIMIT_BUCKETS[key] = recent
        oldest = recent[0] if recent else now
        retry_after = max(1, int(window_sec - (now - oldest)))
        return False, retry_after
    recent.append(now)
    if len(_RATE_LIMIT_BUCKETS) > 1000:
        stale = [k for k, arr in _RATE_LIMIT_BUCKETS.items() if not arr or (now - arr[-1]) >= window_sec]
        for k in stale:
            _RATE_LIMIT_BUCKETS.pop(k, None)
    _RATE_LIMIT_BUCKETS[key] = recent
    return True, 0


def _require_admin_if_auth(request):
    """When APP_PASSWORD/REQUIRE_AUTH is active, require authenticated admin for server key/config actions."""
    if not AUTH_ENABLED:
        return None
    user_info = request.get("user") or {}
    if not request.get("_authenticated"):
        return json_resp({"success": False, "error": "Phiên đăng nhập đã hết hạn. Hãy đăng nhập lại.", "auth_required": True}, 401)
    if user_info.get("role") != "admin":
        return json_resp({"success": False, "error": "Chỉ Quản trị viên mới có quyền thao tác cấu hình API Key / 9Router trên server."}, 403)
    return None


@web.middleware
async def auth_middleware(request, handler):
    token = request.cookies.get(SESSION_COOKIE, "")
    if not token and request.headers.get("Authorization", "").startswith("Bearer "):
        token = request.headers.get("Authorization", "").split(" ", 1)[1].strip()

    user_info = _parse_session_token(token)
    if user_info:
        request["user"] = user_info
        request["_authenticated"] = True
        if request.path.startswith("/api/"):
            _note_user_activity(request, user_info)
    else:
        request["_authenticated"] = False
        request["user"] = {"id": 1, "role": "admin" if not AUTH_ENABLED else "guest"}

    if not AUTH_ENABLED or request.path in AUTH_EXEMPT_PATHS:
        return await handler(request)

    if user_info:
        return await handler(request)

    if request.path.startswith("/api/"):
        return json_resp({"success": False, "error": "Phiên đăng nhập đã hết hạn. Hãy đăng nhập lại.", "auth_required": True}, 401)
    raise web.HTTPFound("/login")


LOGIN_PAGE_HTML = """<!DOCTYPE html>
<html lang="vi" class="dark">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<meta name="theme-color" content="#090a0f" />
<title>UniMaster AI Pro • Đăng Nhập & Tạo Tài Khoản</title>
<link rel="icon" href="/icon.svg" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  *{box-sizing:border-box;margin:0;padding:0}
  body{
    min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px 16px;
    font-family:'Plus Jakarta Sans',system-ui,-apple-system,sans-serif;
    background:#08090d;color:#f3f4f6;
    background-image:
      radial-gradient(circle at 20% 15%, rgba(99,102,241,0.18), transparent 45%),
      radial-gradient(circle at 80% 85%, rgba(16,185,129,0.12), transparent 45%);
    background-attachment:fixed;
  }
  .card{
    width:100%;max-width:440px;background:#0f1118;
    border:1px solid rgba(255,255,255,0.08);border-radius:28px;
    padding:36px 32px;
    box-shadow:0 30px 80px -15px rgba(0,0,0,0.8), 0 0 1px 1px rgba(255,255,255,0.05);
    animation:cardIn .4s cubic-bezier(0.16, 1, 0.3, 1);
  }
  @keyframes cardIn{from{opacity:0;transform:translateY(16px) scale(0.97)}to{opacity:1;transform:none}}
  .logo-wrap{display:flex;align-items:center;gap:12px;margin-bottom:24px}
  .logo-icon{
    width:48px;height:48px;border-radius:16px;
    background:linear-gradient(135deg,#6366f1,#8b5cf6);
    display:flex;align-items:center;justify-content:center;
    font-size:22px;font-weight:800;color:#fff;
    box-shadow:0 10px 25px -5px rgba(99,102,241,0.45);
  }
  .logo-text h1{font-size:20px;font-weight:800;letter-spacing:-0.02em;color:#fff}
  .logo-text p{font-size:12px;color:#94a3b8;font-weight:500}
  
  .tabs{
    display:flex;background:#161922;padding:4px;border-radius:14px;
    margin-bottom:24px;border:1px solid rgba(255,255,255,0.05);
  }
  .tab-btn{
    flex:1;padding:10px 0;text-align:center;font-size:13px;font-weight:700;
    border:0;background:transparent;color:#94a3b8;border-radius:10px;cursor:pointer;
    transition:all .18s ease;
  }
  .tab-btn.active{background:#232736;color:#fff;box-shadow:0 2px 8px rgba(0,0,0,0.3)}
  
  .form-group{margin-bottom:16px}
  label{display:block;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.05em;color:#94a3b8;margin-bottom:6px}
  input{
    width:100%;padding:13px 16px;border-radius:14px;
    border:1px solid rgba(255,255,255,0.1);background:#141721;
    color:#fff;font-size:14px;font-family:inherit;outline:none;transition:all .18s;
  }
  input:focus{border-color:#818cf8;box-shadow:0 0 0 3px rgba(129,140,248,0.2)}
  
  .btn-submit{
    width:100%;padding:14px;border:0;border-radius:14px;margin-top:8px;
    background:linear-gradient(135deg,#6366f1,#4f46e5);color:#fff;
    font-size:14px;font-weight:700;cursor:pointer;transition:all .18s;
    box-shadow:0 10px 20px -5px rgba(99,102,241,0.4);
  }
  .btn-submit:hover{opacity:.95;transform:translateY(-1px)}
  .btn-submit:active{transform:translateY(0)}
  
  .btn-admin{
    width:100%;padding:11px;border:1px solid rgba(255,255,255,0.08);border-radius:12px;margin-top:14px;
    background:transparent;color:#cbd5e1;font-size:12px;font-weight:600;cursor:pointer;transition:all .18s;
    display:flex;align-items:center;justify-content:center;gap:6px;
  }
  .btn-admin:hover{background:rgba(255,255,255,0.04);border-color:rgba(255,255,255,0.16)}
  
  .alert{
    padding:12px 14px;border-radius:12px;font-size:12px;font-weight:600;margin-bottom:18px;
    display:none;animation:cardIn .25s ease;
  }
  .alert-err{background:rgba(239,68,68,0.12);border:1px solid rgba(239,68,68,0.3);color:#fca5a5}
  .alert-ok{background:rgba(16,185,129,0.12);border:1px solid rgba(16,185,129,0.3);color:#6ee7b7}
  
  .hint{font-size:11px;color:#64748b;text-align:center;margin-top:20px;line-height:1.5}
</style>
</head>
<body>
  <div class="card">
    <div class="logo-wrap">
      <div class="logo-icon">U</div>
      <div class="logo-text">
        <h1>UniMaster AI Pro</h1>
        <p>Hệ thống Ôn thi & Thực hành Đại học</p>
      </div>
    </div>

    <!-- Mode Tabs -->
    <div class="tabs">
      <button type="button" class="tab-btn active" id="tab-login" onclick="switchAuthTab('login')">Đăng Nhập</button>
      <button type="button" class="tab-btn" id="tab-register" onclick="switchAuthTab('register')">Tạo Tài Khoản Mới</button>
    </div>

    <div id="alert-box" class="alert alert-err"></div>

    <!-- Login Form -->
    <form id="form-login" onsubmit="handleLoginSubmit(event)">
      <div class="form-group">
        <label>Tên đăng nhập (hoặc để trống nếu là Quản trị)</label>
        <input type="text" id="login-username" placeholder="admin hoặc tên tài khoản" autocomplete="username" />
      </div>
      <div class="form-group">
        <label>Mật khẩu truy cập</label>
        <input type="password" id="login-password" placeholder="Nhập mật khẩu..." required autocomplete="current-password" />
      </div>
      <button type="submit" class="btn-submit" id="btn-login-submit">Đăng Nhập Ngay</button>
      <button type="button" class="btn-admin" onclick="fillAdminDefault()">
        <span>👑</span> Đăng nhập nhanh Quản Trị Viên (Admin)
      </button>
    </form>

    <!-- Register Form -->
    <form id="form-register" style="display:none" onsubmit="handleRegisterSubmit(event)">
      <div class="form-group">
        <label>Họ và tên sinh viên</label>
        <input type="text" id="reg-fullname" placeholder="VD: Nguyễn Văn A" required />
      </div>
      <div class="form-group">
        <label>Tên đăng nhập (viết liền không dấu)</label>
        <input type="text" id="reg-username" placeholder="VD: nguyen_a_ctump" required autocomplete="username" />
      </div>
      <div class="form-group">
        <label>Mật khẩu (tối thiểu 4 ký tự)</label>
        <input type="password" id="reg-password" placeholder="Nhập mật khẩu riêng..." required autocomplete="new-password" />
      </div>
      <button type="submit" class="btn-submit" id="btn-reg-submit" style="background:linear-gradient(135deg,#10b981,#059669)">Tạo Tài Khoản Sinh Viên</button>
    </form>

    <div class="hint">
      🔒 Phân quyền bảo mật: Chỉ có Quản trị viên tối cao mới có quyền quản lý hệ thống. Sinh viên sở hữu hồ sơ và tiến độ thi riêng biệt.
    </div>
  </div>

<script>
let currentMode = 'login';

function switchAuthTab(mode) {
  currentMode = mode;
  document.getElementById('tab-login').classList.toggle('active', mode === 'login');
  document.getElementById('tab-register').classList.toggle('active', mode === 'register');
  document.getElementById('form-login').style.display = (mode === 'login') ? 'block' : 'none';
  document.getElementById('form-register').style.display = (mode === 'register') ? 'block' : 'none';
  hideAlert();
}

function showAlert(msg, isOk = false) {
  const el = document.getElementById('alert-box');
  el.textContent = msg;
  el.className = isOk ? 'alert alert-ok' : 'alert alert-err';
  el.style.display = 'block';
}

function hideAlert() {
  document.getElementById('alert-box').style.display = 'none';
}

function fillAdminDefault() {
  document.getElementById('login-username').value = 'admin';
  document.getElementById('login-password').value = 'uni-5292';
  document.getElementById('login-password').focus();
}

async function handleLoginSubmit(e) {
  e.preventDefault();
  hideAlert();
  const btn = document.getElementById('btn-login-submit');
  const u = document.getElementById('login-username').value.trim();
  const p = document.getElementById('login-password').value;
  btn.disabled = true;
  btn.textContent = 'Đang xác thực...';

  try {
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: u, password: p })
    });
    const data = await res.json();
    if (data.success) {
      showAlert('✅ Đăng nhập thành công! Đang chuyển hướng...', true);
      setTimeout(() => { window.location.href = '/'; }, 400);
    } else {
      showAlert(data.error || 'Sai thông tin đăng nhập');
      btn.disabled = false;
      btn.textContent = 'Đăng Nhập Ngay';
    }
  } catch (err) {
    showAlert('Lỗi kết nối máy chủ: ' + err.message);
    btn.disabled = false;
    btn.textContent = 'Đăng Nhập Ngay';
  }
}

async function handleRegisterSubmit(e) {
  e.preventDefault();
  hideAlert();
  const btn = document.getElementById('btn-reg-submit');
  const fn = document.getElementById('reg-fullname').value.trim();
  const u = document.getElementById('reg-username').value.trim();
  const p = document.getElementById('reg-password').value;
  btn.disabled = true;
  btn.textContent = 'Đang khởi tạo tài khoản...';

  try {
    const res = await fetch('/api/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: u, password: p, full_name: fn })
    });
    const data = await res.json();
    if (data.success) {
      showAlert('🎉 Tạo tài khoản thành công! Đang vào hệ thống...', true);
      setTimeout(() => { window.location.href = '/'; }, 600);
    } else {
      showAlert(data.error || 'Không thể tạo tài khoản');
      btn.disabled = false;
      btn.textContent = 'Tạo Tài Khoản Sinh Viên';
    }
  } catch (err) {
    showAlert('Lỗi kết nối máy chủ: ' + err.message);
    btn.disabled = false;
    btn.textContent = 'Tạo Tài Khoản Sinh Viên';
  }
}
</script>
</body>
</html>"""



async def login_page(request):
    if not AUTH_ENABLED or _valid_session_token(request.cookies.get(SESSION_COOKIE, "")):
        raise web.HTTPFound("/")
    return web.Response(text=LOGIN_PAGE_HTML, content_type="text/html", charset="utf-8")


async def login_api(request):
    return await auth_login_api(request)


async def auth_login_api(request):
    ip = _client_ip(request)
    fails, locked_until = _LOGIN_FAILS.get(ip, [0, 0])
    now = time.time()
    if locked_until > now:
        return json_resp({"success": False, "error": f"Nhập sai quá nhiều lần. Thử lại sau {int(locked_until - now)} giây."}, 429)

    data = await safe_get_json(request)
    username = str(data.get("username", "")).strip().lower()
    pw = str(data.get("password", "")).strip()

    user = None
    # Quick Admin access: if username is 'admin' or blank
    if username in ["admin", ""]:
        user = db.verify_user("admin", pw)
        if not user and APP_PASSWORD and hmac.compare_digest(pw.encode("utf-8"), APP_PASSWORD.encode("utf-8")):
            db.ensure_admin_user(pw)
            user = db.verify_user("admin", pw)

    if not user and username:
        user = db.verify_user(username, pw)

    if user:
        _LOGIN_FAILS.pop(ip, None)
        db.record_login_event(user["id"], ip, request.headers.get("User-Agent", ""), "login", username=user.get("username", ""))
        _SEEN_THROTTLE[user["id"]] = time.time()
        try:
            db.touch_user_seen(user["id"], 0)
        except Exception:
            pass
        token = _make_session_token(user["id"], user["role"])
        resp = json_resp({"success": True, "user": user, "token": token})
        resp.set_cookie(
            SESSION_COOKIE, token, max_age=SESSION_DAYS * 86400,
            httponly=True, samesite="Lax", secure=_is_https(request), path="/"
        )
        return resp

    fails += 1
    lock = now + min(300, 15 * (2 ** (fails - 5))) if fails >= 5 else 0
    _LOGIN_FAILS[ip] = [fails, lock]
    # Ghi cả lần đăng nhập SAI (không lưu mật khẩu) để admin phát hiện người lạ dò mật khẩu
    try:
        db.record_login_event(0, ip, request.headers.get("User-Agent", ""), "login_failed",
                              username=username or "admin", success=False)
    except Exception as exc:
        print(f"⚠️ Không ghi được đăng nhập sai: {exc}")
    return json_resp({"success": False, "error": "Tên đăng nhập hoặc mật khẩu không chính xác."}, 401)


async def auth_register_api(request):
    data = await safe_get_json(request)
    username = str(data.get("username", "")).strip()
    password = str(data.get("password", "")).strip()
    full_name = str(data.get("full_name", "")).strip() or username
    try:
        user = db.create_user(username, password, full_name, role="student")
        db.record_login_event(user["id"], _client_ip(request), request.headers.get("User-Agent", ""), "register", username=user.get("username", ""))
        _SEEN_THROTTLE[user["id"]] = time.time()  # tránh ghi thêm 1 sự kiện 'session' thừa ngay sau khi đăng ký
        try:
            db.touch_user_seen(user["id"], 0)
        except Exception:
            pass
        token = _make_session_token(user["id"], user["role"])
        resp = json_resp({"success": True, "user": user, "token": token})
        resp.set_cookie(
            SESSION_COOKIE, token, max_age=SESSION_DAYS * 86400,
            httponly=True, samesite="Lax", secure=_is_https(request), path="/"
        )
        return resp
    except ValueError as e:
        return json_resp({"success": False, "error": str(e)}, 400)
    except Exception as e:
        return json_resp({"success": False, "error": f"Lỗi tạo tài khoản: {e}"}, 500)


async def auth_logout_api(request):
    user_info = request.get("user") or {}
    if user_info.get("id") and user_info.get("role") != "guest":
        try:
            db.record_login_event(user_info["id"], _client_ip(request), request.headers.get("User-Agent", ""), "logout")
        except Exception:
            pass
    resp = json_resp({"success": True})
    resp.del_cookie(SESSION_COOKIE, path="/")
    return resp


async def auth_me_api(request):
    user_info = request.get("user")
    if not user_info or user_info.get("role") == "guest":
        return json_resp({"success": False, "error": "Chưa đăng nhập", "auth_required": True}, 401)
    full_user = await asyncio.to_thread(db.get_user_by_id, user_info["id"])
    if not full_user and AUTH_ENABLED:
        # Cookie còn hạn nhưng tài khoản không còn trong DB (vd. Render khởi động lại làm DB về bản seed).
        # Xóa cookie để người dùng đăng nhập/đăng ký lại thay vì bị "đăng nhập ma".
        resp = json_resp({"success": False, "error": "Tài khoản không còn tồn tại trên máy chủ. Hãy đăng nhập lại.", "auth_required": True}, 401)
        resp.del_cookie(SESSION_COOKIE, path="/")
        return resp
    return json_resp({"success": True, "user": full_user or user_info})


async def auth_login_history_api(request):
    user_info = request.get("user")
    if not user_info or user_info.get("role") == "guest":
        return json_resp({"success": False, "error": "Chưa đăng nhập"}, 401)
    return json_resp({"success": True, "events": db.get_login_events(user_info["id"])})


async def admin_login_events_api(request):
    """Nhật ký đăng nhập toàn hệ thống — chỉ admin."""
    user_info = request.get("user", {})
    if user_info.get("role") != "admin":
        return json_resp({"success": False, "error": "Chỉ Quản trị viên mới xem được nhật ký đăng nhập toàn hệ thống."}, 403)
    try:
        limit = int(request.query.get("limit", "100"))
    except ValueError:
        limit = 100
    only_failed = request.query.get("failed", "") in ("1", "true", "yes")
    return json_resp({
        "success": True,
        "events": db.get_all_login_events(limit, only_failed),
        "summary": db.get_login_summary(),
        "ephemeral_storage": _storage_is_ephemeral(),
        "db_path": os.path.basename(os.path.dirname(os.path.abspath(db.DB_PATH))) or "",
    })


async def admin_get_users_api(request):
    user_info = request.get("user", {})
    if user_info.get("role") != "admin":
        return json_resp({"success": False, "error": "Chỉ Quản trị viên mới có quyền xem danh sách người dùng."}, 403)
    users = db.get_all_users()
    return json_resp({"success": True, "users": users})


async def admin_delete_user_api(request):
    user_info = request.get("user", {})
    if user_info.get("role") != "admin":
        return json_resp({"success": False, "error": "Chỉ Quản trị viên mới có quyền xóa người dùng."}, 403)
    target_id = int(request.match_info["id"])
    try:
        db.delete_user(target_id)
        return json_resp({"success": True})
    except ValueError as e:
        return json_resp({"success": False, "error": str(e)}, 400)
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


async def logout_api(request):
    resp = json_resp({"success": True})
    resp.del_cookie(SESSION_COOKIE, path="/")
    return resp


async def healthz(request):
    return web.Response(text="ok")


@web.middleware
async def no_cache_static_middleware(request, handler):
    try:
        resp = await handler(request)
        raised = None
    except web.HTTPException as exc:
        resp = exc
        raised = exc

    resp.headers.setdefault("X-Content-Type-Options", "nosniff")
    resp.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
    resp.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    if (
        request.path == "/"
        or request.path.startswith("/static/")
        or request.path.startswith("/api/ai/")
        or request.path in ("/api/settings", "/api/progress")
        or request.path.startswith("/api/progress/")
    ):
        resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"

    if raised is not None:
        raise raised
    return resp


def json_resp(data, status=200):
    return web.json_response(data, status=status)


async def safe_get_json(request):
    try:
        return await request.json()
    except Exception:
        raw = await request.read()
        if not raw:
            return {}
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            text = raw.decode("latin-1", errors="replace")
        return json.loads(text)


# ==========================================
# Handlers: Môn học
# ==========================================
async def get_subjects(request):
    subjects = await asyncio.to_thread(db.get_all_subjects)
    return json_resp({"success": True, "subjects": subjects})


async def create_subject(request):
    try:
        data = await safe_get_json(request)
        code = data.get("code", "").strip().upper()
        name = data.get("name", "").strip()
        icon = data.get("icon", "📚")
        category = data.get("category", "Đại cương")
        description = data.get("description", "")

        if not code or not name:
            return json_resp({"success": False, "error": "Mã môn và tên môn không được để trống"}, 400)

        sid = await asyncio.to_thread(db.add_subject, code, name, icon, category, description)
        return json_resp({"success": True, "id": sid, "subject_id": sid, "message": "Thêm môn học thành công!"})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


async def delete_subject(request):
    try:
        sid = int(request.match_info["id"])
        await asyncio.to_thread(db.delete_subject, sid)
        return json_resp({"success": True, "message": "Đã xóa môn học"})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


# ==========================================
# Handlers: Câu hỏi Đa Định Dạng & Thi Thử
# ==========================================
async def get_questions(request):
    try:
        sid = int(request.match_info["id"])
        limit = request.query.get("limit")
        random_order = request.query.get("random") == "1"
        q_type = request.query.get("type", "all")
        difficulty = request.query.get("difficulty", "all")
        topic_tag = request.query.get("topic_tag") or request.query.get("chapter")

        def _fetch():
            qs = db.get_questions_by_subject(
                sid, q_type=q_type, limit=limit, random_order=random_order, topic_tag=topic_tag
            )
            if difficulty and difficulty != "all":
                qs = [q for q in qs if q.get("difficulty") == difficulty]
            return qs

        questions = await asyncio.to_thread(_fetch)
        return json_resp({"success": True, "questions": questions})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


async def create_question(request):
    try:
        sid = int(request.match_info["id"])
        data = await safe_get_json(request)
        qid = db.add_question(
            subject_id=sid,
            question_text=data["question_text"],
            code_snippet=data.get("code_snippet", ""),
            option_a=data.get("option_a", ""),
            option_b=data.get("option_b", ""),
            option_c=data.get("option_c", ""),
            option_d=data.get("option_d", ""),
            correct_option=data["correct_option"],
            explanation=data.get("explanation", ""),
            difficulty=data.get("difficulty", "medium"),
            q_type=data.get("q_type", "mcq"),
            image_url=data.get("image_url", ""),
            topic_tag=data.get("topic_tag", "")
        )
        return json_resp({"success": True, "id": qid})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


def answers_match_short(user_ans: str, expected_ans: str) -> bool:
    u_raw = str(user_ans or "").strip()
    c_raw = str(expected_ans or "").strip()
    if not u_raw or not c_raw:
        return False
    u_norm = re.sub(r"\s+", " ", u_raw.lower())
    c_norm = re.sub(r"\s+", " ", c_raw.lower())
    if u_norm == c_norm:
        return True
    # Smart numeric comparison supporting Vietnamese comma decimal (e.g. "2,24" == "2.24")
    try:
        u_num = float(u_norm.replace(",", ".").replace(" ", ""))
        c_num = float(c_norm.replace(",", ".").replace(" ", ""))
        return abs(u_num - c_num) <= 1e-6
    except ValueError:
        return False


def _extract_account_id(request, data=None) -> str:
    acc = ""
    if isinstance(data, dict):
        acc = str(data.get("account_id") or "").strip()
    if not acc:
        acc = str(request.query.get("account_id") or "").strip()
    if not acc:
        acc = str(request.headers.get("X-Account-Id") or "").strip()
    return db._sanitize_account_id(acc)


async def submit_exam(request):
    """
    Chấm điểm chính xác toàn bộ đề thi (bao gồm câu chưa làm, câu xáo trộn đáp án,
    trắc nghiệm, đúng/sai, trả lời ngắn và tự luận).
    """
    try:
        data = await safe_get_json(request)
        subject_id = int(data.get("subject_id", 1))
        user_answers = data.get("answers", {})
        question_ids = data.get("question_ids", [])
        custom_correct_map = data.get("correct_map", {})
        essay_ai_scores = data.get("essay_ai_scores", {})
        time_spent = int(data.get("time_spent_seconds", 0))
        exam_type = data.get("exam_type", "mixed")
        draft_key = str(data.get("draft_key") or "").strip()
        acc_id = _extract_account_id(request, data)
        uid = (request.get("user") or {"id": 1}).get("id", 1)

        def _score_and_persist():
            all_q = db.get_questions_by_subject(subject_id)
            q_map = {str(q["id"]): q for q in all_q}
            target_ids = [str(qid) for qid in question_ids] if question_ids else list(user_answers.keys())

            correct_count = 0.0
            total_questions = len(target_ids)
            detail_results = []
            idx_map = {
                "0": "A", "1": "B", "2": "C", "3": "D",
                "TRUE": "A", "ĐÚNG": "A", "FALSE": "B", "SAI": "B",
            }

            for q_id_str in target_ids:
                if q_id_str not in q_map:
                    continue
                q = q_map[q_id_str]
                q_type = q.get("q_type", "mcq")
                user_ans = user_answers.get(q_id_str, "")
                expected_correct = custom_correct_map.get(q_id_str, q["correct_option"])

                if user_ans is None or str(user_ans).strip() == "":
                    is_correct = False
                elif q_type in ["mcq", "true_false"]:
                    c_opt = idx_map.get(str(expected_correct).strip().upper(), str(expected_correct).strip().upper())
                    u_ans = idx_map.get(str(user_ans).strip().upper(), str(user_ans).strip().upper())
                    is_correct = (u_ans == c_opt)
                elif q_type == "short_answer":
                    is_correct = answers_match_short(user_ans, expected_correct)
                else:
                    if q_id_str in essay_ai_scores:
                        ai_sc = float(essay_ai_scores[q_id_str])
                        is_correct = ai_sc >= 5.0
                    else:
                        is_correct = len(str(user_ans).strip()) >= 10

                if is_correct:
                    correct_count += 1

                detail_results.append({
                    "question_id": q["id"],
                    "question_text": q["question_text"],
                    "code_snippet": q.get("code_snippet", ""),
                    "image_url": q.get("image_url", ""),
                    "topic_tag": q.get("topic_tag", ""),
                    "q_type": q_type,
                    "difficulty": q.get("difficulty", "medium"),
                    "user_answer": user_ans,
                    "correct_option": expected_correct,
                    "is_correct": is_correct,
                    "explanation": q["explanation"],
                })

            int_correct = int(round(correct_count))
            score = round((correct_count / total_questions * 10), 1) if total_questions > 0 else 0
            res_id = db.save_exam_result(
                subject_id=subject_id,
                total_questions=total_questions,
                correct_answers=int_correct,
                score=score,
                time_spent_seconds=time_spent,
                detail_json=json.dumps(detail_results, ensure_ascii=False),
                exam_type=exam_type,
                user_id=uid,
            )
            draft_cleared = False
            if draft_key:
                draft_cleared = db.delete_study_progress(acc_id, draft_key)
            return {
                "success": True,
                "result_id": res_id,
                "score": score,
                "correct_count": int_correct,
                "total_questions": total_questions,
                "draft_cleared": draft_cleared,
                "details": detail_results,
            }

        result_payload = await asyncio.to_thread(_score_and_persist)
        return json_resp(result_payload)
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


# ==========================================
# Handlers: Lưu & Tiếp Tục Tiến Trình Học (Save & Resume)
# ==========================================
async def list_progress_handler(request):
    try:
        acc = _extract_account_id(request)
        ptype = request.query.get("progress_type")
        sid = request.query.get("subject_id")
        lim = request.query.get("limit", "50")
        drafts = await asyncio.to_thread(
            db.list_study_progress, account_id=acc, progress_type=ptype, subject_id=sid, limit=lim
        )
        return json_resp({"success": True, "account_id": acc, "drafts": drafts})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


async def get_progress_item_handler(request):
    try:
        acc = _extract_account_id(request)
        draft_key = request.match_info.get("draft_key", "").strip()
        if not draft_key:
            return json_resp({"success": False, "error": "draft_key is required"}, 400)
        draft = await asyncio.to_thread(db.get_study_progress, acc, draft_key)
        if not draft:
            return json_resp({"success": False, "error": "Draft not found"}, 404)
        return json_resp({"success": True, "draft": draft})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


async def save_progress_handler(request):
    try:
        data = await safe_get_json(request)
        if not isinstance(data, dict):
            return json_resp({"success": False, "error": "JSON object expected"}, 400)
        acc = _extract_account_id(request, data)
        draft_key = str(data.get("draft_key") or "").strip()
        if not draft_key:
            return json_resp({"success": False, "error": "draft_key is required"}, 400)
        draft = await asyncio.to_thread(
            db.upsert_study_progress,
            account_id=acc,
            draft_key=draft_key,
            progress_type=data.get("progress_type", "exam"),
            subject_id=data.get("subject_id"),
            chapter_tag=data.get("chapter_tag", ""),
            title=data.get("title", ""),
            payload=data.get("payload"),
            payload_json=data.get("payload_json"),
            current_index=data.get("current_index", 0),
            total_items=data.get("total_items", 0),
            answered_count=data.get("answered_count", 0),
        )
        return json_resp({"success": True, "draft": draft})
    except ValueError as ve:
        return json_resp({"success": False, "error": str(ve)}, 400)
    except json.JSONDecodeError:
        return json_resp({"success": False, "error": "Invalid JSON body"}, 400)
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


async def delete_progress_handler(request):
    try:
        data = {}
        if request.method == "POST" or request.can_read_body:
            try:
                raw_data = await safe_get_json(request)
                if isinstance(raw_data, dict):
                    data = raw_data
            except Exception:
                data = {}
        acc = _extract_account_id(request, data)
        draft_key = (
            request.match_info.get("draft_key")
            or data.get("draft_key")
            or request.query.get("draft_key")
            or ""
        ).strip()
        if not draft_key:
            return json_resp({"success": False, "error": "draft_key is required"}, 400)
        deleted = await asyncio.to_thread(db.delete_study_progress, acc, draft_key)
        return json_resp({"success": True, "deleted": deleted, "account_id": acc, "draft_key": draft_key})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


# ==========================================
# Handlers: Bài Tập Lớn & Flashcards
# ==========================================

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


async def get_exercises(request):
    try:
        sid = int(request.match_info["id"])
        exercises = db.get_exercises_by_subject(sid)
        return json_resp({"success": True, "exercises": exercises})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


async def get_exercises_by_query(request):
    """Alias: /api/exercises?subject_id=N (query-param style used by frontend/tests)."""
    try:
        sid = int(request.rel_url.query.get("subject_id", 0))
        exercises = db.get_exercises_by_subject(sid)
        return json_resp({"success": True, "exercises": exercises})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


async def get_flashcards(request):
    try:
        sid = int(request.match_info["id"])
        cards = db.get_flashcards_by_subject(sid)
        return json_resp({"success": True, "flashcards": cards})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


async def get_flashcards_by_query(request):
    """Alias: /api/flashcards?subject_id=N (query-param style used by frontend/tests)."""
    try:
        sid = int(request.rel_url.query.get("subject_id", 0))
        cards = db.get_flashcards_by_subject(sid)
        return json_resp({"success": True, "flashcards": cards})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


async def _build_keys_status_payload() -> dict:
    summary, router_status = await asyncio.gather(
        asyncio.to_thread(ai.get_pool_summary),
        asyncio.to_thread(ai.get_router_public_status),
    )
    return {
        "success": True,
        "secured_on_server": True,
        "has_gemini_key": summary["has_gemini_key"],
        "key_count": summary["total_count"],
        "total_count": summary["total_count"],
        "ready_count": summary["ready_count"],
        "active_count": summary["active_count"],
        "cooldown_count": summary["cooldown_count"],
        "invalid_count": summary["invalid_count"],
        "disabled_count": summary.get("disabled_count", 0),
        "masked_key": summary["masked_key"],
        "keys": summary["keys"],
        "pool": summary["keys"],
        "router": router_status,
        "openai": router_status,
        "gateway_local_hint": ai.get_gateway_local_hint(),
    }


async def api_ai_key_status(request):
    """GET /api/ai/key-status — trả trạng thái pool Gemini (đã che) và 9Router/OpenAI."""
    payload = await _build_keys_status_payload()
    summary_total = payload["total_count"]
    router_info = payload["router"]
    payload.update({
        "gemini_keys": summary_total,
        "openai_configured": bool(router_info.get("has_key")),
        "openai_base": router_info.get("base_url", ""),
    })
    return json_resp(payload)


async def api_ai_keys_handler(request):
    """GET /api/ai/keys — danh sách API Key & 9Router được bảo vệ trên server (chỉ trả bản che masked)."""
    return json_resp(await _build_keys_status_payload())


async def api_ai_keys_add(request):
    """POST /api/ai/keys/add — gắn 1 hoặc nhiều Gemini API Key an toàn, kiểm tra định dạng & deduplicate."""
    auth_err = _require_admin_if_auth(request)
    if auth_err:
        return auth_err
    try:
        data = await safe_get_json(request)
        if not isinstance(data, dict):
            return json_resp({"success": False, "error": "JSON object expected"}, 400)

        auto_test = bool(data.get("auto_test", False))
        if auto_test:
            allowed, retry_after = _check_rate_limit(request, "ai_test", limit=15, window_sec=60)
            if not allowed:
                return json_resp(
                    {"success": False, "error": f"Quá nhiều lượt kiểm tra key. Thử lại sau {retry_after}s.", "retry_after": retry_after},
                    429,
                )

        raw_keys = (
            data.get("keys")
            or data.get("api_keys")
            or data.get("gemini_api_keys")
            or data.get("key")
            or ""
        )
        res = await ai.add_gemini_keys_to_pool(raw_keys, auto_test=auto_test, sync_env=True)
        if not res.get("success"):
            return json_resp(res, 400)
        return json_resp(res)
    except json.JSONDecodeError:
        return json_resp({"success": False, "error": "Invalid JSON body"}, 400)
    except Exception as e:
        return json_resp({"success": False, "error": ai._sanitize_error_text(str(e))}, 500)


async def api_ai_keys_delete(request):
    """POST /api/ai/keys/delete hoặc DELETE /api/ai/keys/{index} — xóa Gemini API Key khỏi pool & .env."""
    auth_err = _require_admin_if_auth(request)
    if auth_err:
        return auth_err
    try:
        data = {}
        if request.method != "DELETE" and request.can_read_body:
            try:
                raw_data = await safe_get_json(request)
                if isinstance(raw_data, dict):
                    data = raw_data
            except Exception:
                data = {}

        idx_param = request.match_info.get("index")
        raw_idx = idx_param if idx_param is not None else data.get("index")
        index_val = int(raw_idx) if raw_idx is not None and str(raw_idx).strip().lstrip("-").isdigit() else None
        key_id = data.get("id") or data.get("key_id")
        if key_id is not None:
            try:
                key_id = int(key_id)
            except (TypeError, ValueError):
                key_id = None
        masked_key = str(data.get("masked_key") or "").strip() or None
        zero_idx = data.get("zero_index")
        if zero_idx is not None:
            try:
                zero_idx = int(zero_idx)
            except (TypeError, ValueError):
                zero_idx = None

        res = await asyncio.to_thread(
            ai.delete_gemini_key_from_pool,
            index=index_val,
            key_id=key_id,
            masked_key=masked_key,
            zero_index=zero_idx,
            sync_env=True,
        )
        if not res.get("deleted"):
            return json_resp(res, 404)
        return json_resp(res)
    except Exception as e:
        return json_resp({"success": False, "error": ai._sanitize_error_text(str(e))}, 500)


async def api_ai_keys_toggle(request):
    """POST /api/ai/keys/toggle — tạm tắt hoặc bật lại 1 Gemini key trong pool."""
    auth_err = _require_admin_if_auth(request)
    if auth_err:
        return auth_err
    try:
        data = await safe_get_json(request)
        if not isinstance(data, dict):
            return json_resp({"success": False, "error": "JSON object expected"}, 400)
        raw_idx = data.get("index")
        index_val = int(raw_idx) if raw_idx is not None and str(raw_idx).strip().lstrip("-").isdigit() else None
        key_id = data.get("id") or data.get("key_id")
        if key_id is not None:
            try:
                key_id = int(key_id)
            except (TypeError, ValueError):
                key_id = None
        masked_key = str(data.get("masked_key") or "").strip() or None
        enabled = data.get("enabled") if "enabled" in data else None
        if enabled is not None:
            enabled = bool(enabled)

        res = await asyncio.to_thread(
            ai.toggle_gemini_key_in_pool,
            index=index_val,
            key_id=key_id,
            masked_key=masked_key,
            enabled=enabled,
        )
        if not res.get("success"):
            return json_resp(res, 404)
        return json_resp(res)
    except Exception as e:
        return json_resp({"success": False, "error": ai._sanitize_error_text(str(e))}, 500)


async def api_ai_9router_config(request):
    """POST /api/ai/9router — lưu cấu hình 9Router / FOSTA / OpenAI-compatible với kiểm tra SSRF & bảo toàn mask."""
    auth_err = _require_admin_if_auth(request)
    if auth_err:
        return auth_err
    try:
        data = await safe_get_json(request)
        if not isinstance(data, dict):
            return json_resp({"success": False, "error": "JSON object expected"}, 400)

        base_url = data.get("base_url") if "base_url" in data else data.get("router_base_url")
        if base_url is None and "openai_base_url" in data:
            base_url = data.get("openai_base_url")

        if "api_key" in data:
            api_key = data.get("api_key")
        elif "key" in data:
            api_key = data.get("key")
        elif "router_api_key" in data:
            api_key = data.get("router_api_key")
        elif "openai_api_key" in data:
            api_key = data.get("openai_api_key")
        else:
            api_key = None

        model = data.get("model") if "model" in data else data.get("router_model")
        if model is None and "openai_model" in data:
            model = data.get("openai_model")

        priority = data.get("priority") if "priority" in data else data.get("ai_provider_priority")
        clear_key = bool(data.get("clear_key") or data.get("clear_openai_key"))

        ok, router_pub, msg = await asyncio.to_thread(
            ai.save_router_config,
            base_url=base_url,
            api_key=api_key,
            model=model,
            priority=priority,
            clear_key=clear_key,
        )
        if not ok:
            return json_resp({"success": False, "error": msg, "router": router_pub, "openai": router_pub}, 400)
        return json_resp({"success": True, "router": router_pub, "openai": router_pub, "message": msg})
    except json.JSONDecodeError:
        return json_resp({"success": False, "error": "Invalid JSON body"}, 400)
    except Exception as e:
        return json_resp({"success": False, "error": ai._sanitize_error_text(str(e))}, 500)


async def api_network_qr_info(request):
    """GET /api/network/qr-info — trả URL LAN và tunnel để hiển thị QR."""
    import ai_service as ai
    info = await get_network_info(request)
    return info


async def api_battle_leaderboard(request):
    """GET /api/battle/leaderboard — stub; ponytail: real-time arena qua WebSocket."""
    return json_resp({"success": True, "leaderboard": []})


async def api_stem_reference(request):
    """GET /api/stem/reference — stub; ponytail: tích hợp STEM reference DB sau."""
    return json_resp({"success": True, "references": []})


async def api_exam_ctump_parts(request):
    """GET /api/exam/ctump-parts — trả danh sách phần thi CTUMP từ DB."""
    try:
        subjects = db.get_all_subjects()
        keywords = ("ctump", "hóa sinh", "hoa sinh", "biochem")
        ctump = [
            s for s in subjects
            if any(kw in str(s.get("name", "")).lower() for kw in keywords)
        ]
        return json_resp({"success": True, "parts": ctump, "total": len(ctump)})
    except Exception as e:
        return json_resp({"success": True, "parts": [], "total": 0, "note": str(e)})


async def create_flashcard(request):
    try:
        sid = int(request.match_info["id"])
        data = await safe_get_json(request)
        cid = db.add_flashcard(
            subject_id=sid,
            front=data["front"],
            back=data["back"],
            hint=data.get("hint", "")
        )
        return json_resp({"success": True, "id": cid})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


async def review_flashcard(request):
    try:
        cid = int(request.match_info["id"])
        data = await safe_get_json(request)
        rating = int(data.get("rating", 2))
        res = db.update_flashcard_review(cid, rating)
        return json_resp({"success": True, "result": res})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


# ==========================================
# Handlers: Universal Document Upload (.pdf, .pptx, .docx, .xlsx, images)
# ==========================================
async def upload_document_handler(request):
    """
    Nhận 1 hoặc nhiều file tài liệu (.pdf, .pptx, .ppt, .docx, .doc, .xlsx, .csv, ảnh đề cương...)
    và trích xuất văn bản sạch (tự động OCR qua Gemini Vision nếu là ảnh hoặc PDF scan).
    """
    try:
        parsed_files = []
        combined_blocks = []
        all_extracted_images = []
        all_direct_questions = []

        if request.content_type and request.content_type.startswith("multipart/"):
            reader = await request.multipart()
            while True:
                part = await reader.next()
                if part is None:
                    break
                filename = part.filename
                if not filename:
                    continue
                raw_bytes = await part.read(decode=False)
                if not raw_bytes:
                    continue
                info = await doc_parser.parse_uploaded_file(filename, raw_bytes, ai_module=ai)
                parsed_files.append({
                    "filename": info["filename"],
                    "summary_badge": info["summary_badge"],
                    "char_count": info["char_count"],
                    "used_vision_ocr": info["used_vision_ocr"],
                    "image_count": len(info.get("extracted_images", [])),
                    "direct_question_count": len(info.get("direct_questions", []))
                })
                all_extracted_images.extend(info.get("extracted_images", []))
                all_direct_questions.extend(info.get("direct_questions", []))
                if info["content"]:
                    combined_blocks.append(f"=== Tài liệu: {info['filename']} ({info['summary_badge']}) ===\n{info['content']}")
        else:
            data = await safe_get_json(request)
            for fitem in data.get("files", []):
                fname = fitem.get("filename", "document.txt")
                b64_str = fitem.get("base64", "")
                if not b64_str:
                    continue
                raw_bytes = base64.b64decode(b64_str)
                info = await doc_parser.parse_uploaded_file(fname, raw_bytes, ai_module=ai)
                parsed_files.append({
                    "filename": info["filename"],
                    "summary_badge": info["summary_badge"],
                    "char_count": info["char_count"],
                    "used_vision_ocr": info["used_vision_ocr"],
                    "image_count": len(info.get("extracted_images", [])),
                    "direct_question_count": len(info.get("direct_questions", []))
                })
                all_extracted_images.extend(info.get("extracted_images", []))
                all_direct_questions.extend(info.get("direct_questions", []))
                if info["content"]:
                    combined_blocks.append(f"=== Tài liệu: {info['filename']} ({info['summary_badge']}) ===\n{info['content']}")

        combined_text = "\n\n".join(combined_blocks).strip()
        if not parsed_files:
            return json_resp({"success": False, "error": "Chưa nhận được tệp tin tải lên."}, 400)

        return json_resp({
            "success": True,
            "files": parsed_files,
            "combined_content": combined_text,
            "total_chars": len(combined_text),
            "extracted_images": all_extracted_images,
            "direct_questions": all_direct_questions,
            "direct_question_count": len(all_direct_questions)
        })
    except Exception as e:
        return json_resp({"success": False, "error": f"Không thể đọc tệp tin: {str(e)}"}, 500)


async def import_direct_questions_handler(request):
    """Lưu trực tiếp toàn bộ danh sách câu hỏi trích xuất nguyên bản từ PDF/DOCX vào môn học đã chọn"""
    try:
        data = await safe_get_json(request)
        subject_id = int(data.get("subject_id") or 5)
        questions = data.get("questions", [])
        saved_count = 0
        for q in questions:
            q_txt = str(q.get("question_text", "")).strip()
            if not q_txt:
                continue
            db.add_question(
                subject_id=subject_id,
                question_text=q_txt,
                code_snippet=q.get("code_snippet", ""),
                option_a=q.get("option_a", ""),
                option_b=q.get("option_b", ""),
                option_c=q.get("option_c", ""),
                option_d=q.get("option_d", ""),
                correct_option=q.get("correct_option", "A"),
                explanation=q.get("explanation", ""),
                difficulty=q.get("difficulty", "medium"),
                q_type=q.get("q_type", "mcq"),
                image_url=q.get("image_url", ""),
                topic_tag=q.get("topic_tag", "")
            )
            saved_count += 1
        return json_resp({
            "success": True,
            "saved_count": saved_count,
            "message": f"Đã nhập nguyên bản {saved_count} câu hỏi vào Ngân hàng đề!"
        })
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


async def ai_generate_image_question_handler(request):
    """Dùng Gemini Vision (hoặc bộ tạo thông minh) để sinh câu hỏi trắc nghiệm từ hình ảnh và lưu vào môn học"""
    try:
        data = await safe_get_json(request)
        subject_id = int(data.get("subject_id") or 5)
        image_url = str(data.get("image_url", "")).strip()
        label = str(data.get("label", "")).strip()
        subs = db.get_all_subjects()
        found = next((s for s in subs if s["id"] == subject_id), None)
        subject_name = data.get("subject_name") or (found["name"] if found else "Đại học")

        if not image_url or not image_url.startswith("/static/"):
            return json_resp({"success": False, "error": "Đường dẫn hình ảnh không hợp lệ."}, 400)

        rel_path = image_url.lstrip("/").replace("/", os.sep)
        abs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), rel_path)
        if not os.path.exists(abs_path):
            return json_resp({"success": False, "error": "Không tìm thấy tệp ảnh trên máy chủ."}, 404)

        with open(abs_path, "rb") as f:
            raw_bytes = f.read()
        ext = os.path.splitext(abs_path)[1].lower()
        mime_map = {".png": "image/png", ".webp": "image/webp", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}
        q_obj = await ai.ai_generate_image_question(subject_name, mime_map.get(ext, "image/jpeg"), raw_bytes, hint_label=label)

        qid = db.add_question(
            subject_id=subject_id,
            question_text=q_obj.get("question", f"[Hình ảnh] Câu hỏi nhận diện ({label})"),
            option_a=q_obj.get("a", "Phương án A"),
            option_b=q_obj.get("b", "Phương án B"),
            option_c=q_obj.get("c", "Phương án C"),
            option_d=q_obj.get("d", "Phương án D"),
            correct_option=q_obj.get("correct", "A"),
            explanation=q_obj.get("explanation", ""),
            difficulty="medium",
            q_type="mcq",
            image_url=image_url,
            topic_tag="Câu hỏi Hình ảnh Minh họa"
        )
        return json_resp({
            "success": True,
            "id": qid,
            "question": {
                "id": qid,
                "subject_id": subject_id,
                "question_text": q_obj.get("question", ""),
                "option_a": q_obj.get("a", ""),
                "option_b": q_obj.get("b", ""),
                "option_c": q_obj.get("c", ""),
                "option_d": q_obj.get("d", ""),
                "correct_option": q_obj.get("correct", "A"),
                "explanation": q_obj.get("explanation", ""),
                "image_url": image_url
            }
        })
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


async def ai_grade_handwritten_handler(request):
    """Chấm bài tự luận viết tay, giấy nháp hoặc phiếu xét nghiệm qua ảnh chụp Camera điện thoại / tải lên"""
    try:
        data = await safe_get_json(request)
        subject_name = str(data.get("subject_name") or "Thực Hành Hóa Sinh & Y Khoa").strip()
        question_text = str(data.get("question_text") or "").strip()
        student_note = str(data.get("student_note") or "").strip()
        image_b64 = str(data.get("image_base64") or "").strip()
        mime_type = str(data.get("mime_type") or "image/jpeg").strip()

        if not image_b64:
            return json_resp({"success": False, "error": "Chưa có ảnh bài làm để chấm."}, 400)

        if "," in image_b64 and image_b64.startswith("data:"):
            header, image_b64 = image_b64.split(",", 1)
            m = re.search(r"data:([^;]+);base64", header)
            if m:
                mime_type = m.group(1)

        import base64
        raw_bytes = base64.b64decode(image_b64)
        grading = await ai.ai_grade_handwritten_image(
            subject_name=subject_name,
            question_text=question_text,
            mime_type=mime_type,
            raw_bytes=raw_bytes,
            student_note=student_note
        )
        return json_resp({"success": True, "grading": grading})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


async def get_question_discussions_handler(request):
    try:
        qid = int(request.match_info["id"])
        comments = db.get_discussions_by_question(qid)
        return json_resp({"success": True, "comments": comments, "discussions": comments})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


async def add_question_discussion_handler(request):
    try:
        qid = int(request.match_info["id"])
        data = await safe_get_json(request)
        author = str(data.get("author_name", "Sinh viên ẩn danh")).strip() or "Sinh viên ẩn danh"
        content = str(data.get("content", "")).strip()
        role = str(data.get("author_role", "student")).strip()
        if not content:
            return json_resp({"success": False, "error": "Nội dung bình luận không được để trống."}, 400)
        is_ver = 1 if role in ("ta", "ai_verified") else 0
        cid = db.add_discussion_comment(qid, author, content, author_role=role, is_verified=is_ver)
        comments = db.get_discussions_by_question(qid)
        return json_resp({"success": True, "id": cid, "comments": comments})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


async def upvote_discussion_handler(request):
    try:
        cid = int(request.match_info["id"])
        upvotes = db.upvote_discussion_comment(cid)
        return json_resp({"success": True, "upvotes": upvotes})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


# ==========================================
# Handlers: AI Features & Multi-Key Gemini Engine
# ==========================================
async def _resolve_subject_name_async(subject_id, subject_name: str = "") -> str:
    sname = str(subject_name or "").strip()
    if sname:
        return sname
    if subject_id is not None and str(subject_id).strip().isdigit():
        sid = int(subject_id)
        subs = await asyncio.to_thread(db.get_all_subjects)
        found = next((s for s in subs if s["id"] == sid), None)
        if found:
            return found["name"]
    return "Đại học tổng hợp"


async def _handle_tutor_assist_common(request, default_mode: str = "explain"):
    data = await safe_get_json(request)
    if not isinstance(data, dict):
        return json_resp({"success": False, "error": "JSON object expected"}, 400)

    subject_name = await _resolve_subject_name_async(data.get("subject_id"), data.get("subject_name", ""))
    message = str(data.get("message") or data.get("query") or "").strip()
    mode = str(data.get("mode") or default_mode).strip()
    persona = str(data.get("persona") or "professor").strip()
    tutor_style_prompt = str(data.get("tutor_style_prompt") or "").strip()
    question_text = str(data.get("question_text") or "").strip()
    options = data.get("options")
    correct_answer = str(data.get("correct_answer") or data.get("correct_option") or "").strip()
    selected_answer = str(data.get("selected_answer") or data.get("user_wrong_answer") or "").strip()
    question_image_hint = str(data.get("question_image_hint") or "").strip()
    code_snippet = str(data.get("code_snippet") or "").strip()
    selected_term = str(data.get("selected_term") or "").strip()
    chat_history = data.get("chat_history") if isinstance(data.get("chat_history"), list) else data.get("history")

    res = await ai.ai_tutor_assist(
        subject_name=subject_name,
        message=message,
        mode=mode,
        persona=persona,
        tutor_style_prompt=tutor_style_prompt,
        question_text=question_text,
        options=options,
        correct_answer=correct_answer,
        selected_answer=selected_answer,
        question_image_hint=question_image_hint,
        code_snippet=code_snippet,
        selected_term=selected_term,
        chat_history=chat_history if isinstance(chat_history, list) else None,
    )

    session_id = str(data.get("session_id") or "").strip()
    save_history = bool(data.get("save_history")) or bool(session_id)
    res["history_saved"] = False
    if save_history:
        acc_id = _extract_account_id(request, data)
        ctx_meta = {
            k: v
            for k, v in {
                "question_id": data.get("question_id"),
                "question_text": question_text[:400] if question_text else "",
                "selected_answer": selected_answer,
                "correct_answer": correct_answer,
                "selected_term": selected_term,
            }.items()
            if v not in (None, "")
        }
        turns_to_save = []
        user_txt = message or question_text or selected_term
        if user_txt:
            turns_to_save.append({"role": "user", "content": user_txt, "mode": res["mode"], "context": ctx_meta})
        if res.get("reply"):
            turns_to_save.append({
                "role": "model",
                "content": res["reply"],
                "mode": res["mode"],
                "context": ctx_meta,
                "provider_used": res.get("provider_used", ""),
                "model_used": res.get("model_used", ""),
                "masked_key": res.get("masked_key", ""),
                "latency_ms": res.get("latency_ms"),
            })
        if turns_to_save:
            try:
                auto_title = str(data.get("title") or "").strip()
                if not auto_title:
                    topic_snippet = re.sub(r"\s+", " ", (question_text or selected_term or message)).strip()
                    if topic_snippet:
                        auto_title = (f"{subject_name} — {topic_snippet}" if subject_name else topic_snippet)[:120]
                saved = await asyncio.to_thread(
                    _append_tutor_turns,
                    acc_id,
                    session_id or None,
                    auto_title,
                    data.get("subject_id"),
                    subject_name,
                    res["mode"],
                    persona,
                    turns_to_save,
                )
                res["session_id"] = saved["session_id"]
                res["history_saved"] = True
            except Exception:
                if session_id:
                    res["session_id"] = session_id

    return res


def _append_tutor_turns(
    account_id: str,
    session_id: str,
    title: str,
    subject_id,
    subject_name: str,
    mode: str,
    persona: str,
    turns: list,
) -> dict:
    last_sess = None
    sid = session_id
    for t in turns:
        last_sess = db.save_tutor_chat_turn(
            account_id=account_id,
            session_id=sid,
            title=title,
            subject_id=subject_id,
            subject_name=subject_name,
            mode=t.get("mode", mode),
            persona=persona,
            role=t.get("role", "user"),
            content=t.get("content", ""),
            context=t.get("context"),
            provider_used=t.get("provider_used", ""),
            model_used=t.get("model_used", ""),
            masked_key=t.get("masked_key", ""),
            latency_ms=t.get("latency_ms"),
        )
        sid = last_sess["session_id"]
    return last_sess or {"session_id": sid or ""}


async def test_key_handler(request):
    auth_err = _require_admin_if_auth(request)
    if auth_err:
        return auth_err
    allowed, retry_after = _check_rate_limit(request, "ai_test", limit=15, window_sec=60)
    if not allowed:
        return json_resp(
            {"success": False, "error": f"Quá nhiều lượt kiểm tra key. Thử lại sau {retry_after}s.", "retry_after": retry_after},
            429,
        )
    try:
        data = await safe_get_json(request)
        key = str(data.get("api_key") or "").strip() if isinstance(data, dict) else ""
        if not key or ai._is_masked_placeholder(key):
            pool = await asyncio.to_thread(ai.get_api_keys_pool)
            idx = None
            if isinstance(data, dict) and data.get("index") is not None:
                try:
                    idx = int(data["index"]) - 1
                except (TypeError, ValueError):
                    idx = None
            if idx is not None and 0 <= idx < len(pool):
                key = pool[idx]["key"]
            else:
                key = await asyncio.to_thread(ai.get_api_key)
        res = await ai.test_api_key(key)
        res["secured_on_server"] = True
        res["pool"] = await asyncio.to_thread(ai.get_pool_status)
        return json_resp(res)
    except Exception as e:
        return json_resp({"success": False, "message": ai._sanitize_error_text(str(e))}, 500)


async def test_all_keys_handler(request):
    auth_err = _require_admin_if_auth(request)
    if auth_err:
        return auth_err
    allowed, retry_after = _check_rate_limit(request, "ai_test", limit=15, window_sec=60)
    if not allowed:
        return json_resp(
            {"success": False, "error": f"Quá nhiều lượt kiểm tra dàn key. Thử lại sau {retry_after}s.", "retry_after": retry_after},
            429,
        )
    try:
        keys_override = None
        if request.can_read_body:
            try:
                data = await safe_get_json(request)
                if isinstance(data, dict):
                    keys_override = data.get("keys") or data.get("gemini_api_keys") or data.get("api_keys")
            except Exception:
                keys_override = None
        res = await ai.test_all_pool_keys(keys_input=keys_override)
        return json_resp(res)
    except Exception as e:
        return json_resp({"success": False, "message": ai._sanitize_error_text(str(e))}, 500)


async def ai_hint_handler(request):
    try:
        out = await _handle_tutor_assist_common(request, default_mode="socratic")
        if isinstance(out, web.Response):
            return out
        if not out.get("success"):
            out["hint"] = (
                "Hãy xác định công thức/định nghĩa trọng tâm của câu hỏi, kiểm tra điều kiện áp dụng "
                "và loại trừ ngay 2 phương án trái bản chất."
            )
            out["reply"] = out.get("reply") or out["hint"]
            out["fallback_used"] = True
            out["success"] = True
        else:
            out["hint"] = out["reply"]
        return json_resp(out)
    except Exception as e:
        return json_resp({"success": False, "error": ai._sanitize_error_text(str(e))}, 500)


async def ai_deep_analysis_handler(request):
    try:
        data = await safe_get_json(request)
        q_text = data.get("question_text", "")
        correct_opt = data.get("correct_option", "")
        explanation = data.get("explanation", "")
        code = data.get("code_snippet", "")
        analysis = await ai.ai_deep_analysis(q_text, correct_opt, explanation, code)
        return json_resp({"success": True, "analysis": analysis})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


async def ai_similar_handler(request):
    try:
        data = await safe_get_json(request)
        q_text = data.get("question_text", "")
        code = data.get("code_snippet", "")
        similar = await ai.ai_generate_similar(q_text, code)
        return json_resp({"success": True, "similar": similar})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


async def ai_custom_qa_handler(request):
    try:
        data = await safe_get_json(request)
        q_text = data.get("question_text", "")
        correct_text = data.get("correct_text", "")
        query = data.get("query", "")
        code = data.get("code_snippet", "")
        answer = await ai.ai_custom_qa(q_text, correct_text, query, code)
        return json_resp({"success": True, "answer": answer})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


async def ai_grade_essay_handler(request):
    try:
        data = await safe_get_json(request)
        q_text = data.get("question_text", "")
        expected = data.get("expected_barem", "")
        student_ans = data.get("student_answer", "")
        grading = await ai.ai_grade_essay(q_text, expected, student_ans)
        return json_resp({"success": True, "grading": grading})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


async def ai_roadmap_handler(request):
    try:
        data = await safe_get_json(request)
        subject_id = int(data.get("subject_id") or 5)
        subject_name = data.get("subject_name", "")
        subs = db.get_all_subjects()
        if not subject_name:
            found = next((s for s in subs if s["id"] == subject_id), None)
            subject_name = found["name"] if found else "Đại học tổng hợp"

        mistake_questions = data.get("mistake_questions", [])
        if not mistake_questions and data.get("mistake_ids"):
            m_ids = {int(x) for x in data.get("mistake_ids", []) if str(x).isdigit()}
            all_qs = db.get_questions_by_subject(subject_id)
            mistake_questions = [q["question_text"] for q in all_qs if q["id"] in m_ids]

        stats_summary = db.get_stats()
        roadmap = await ai.ai_personalized_roadmap(subject_name, stats_summary, mistake_questions)
        return json_resp({"success": True, "roadmap": roadmap})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


async def ai_evaluate_exam_handler(request):
    try:
        data = await safe_get_json(request)
        subject_name = data.get("subject_name", "Môn học")
        total = int(data.get("total", 0))
        correct = int(data.get("correct", 0))
        wrong_qs = data.get("wrong_questions", [])
        topic_tags = data.get("topic_tags", [])
        eval_md = await ai.ai_evaluate_exam(subject_name, total, correct, wrong_qs, topic_tags)
        return json_resp({"success": True, "evaluation": eval_md})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


async def ai_explain_exercise_handler(request):
    try:
        data = await safe_get_json(request)
        title = data.get("title", "")
        problem = data.get("problem", "")
        sample_code = data.get("sample_code", "")
        md = await ai.ai_explain_exercise(title, problem, sample_code)
        return json_resp({"success": True, "explanation": md})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


async def ai_chat(request):
    try:
        out = await _handle_tutor_assist_common(request, default_mode="explain")
        if isinstance(out, web.Response):
            return out
        return json_resp(out)
    except json.JSONDecodeError:
        return json_resp({"success": False, "error": "Invalid JSON body"}, 400)
    except Exception as e:
        return json_resp({"success": False, "error": ai._sanitize_error_text(str(e))}, 500)


async def ai_tutor_assist_handler(request):
    try:
        out = await _handle_tutor_assist_common(request, default_mode="explain")
        if isinstance(out, web.Response):
            return out
        return json_resp(out)
    except json.JSONDecodeError:
        return json_resp({"success": False, "error": "Invalid JSON body"}, 400)
    except Exception as e:
        return json_resp({"success": False, "error": ai._sanitize_error_text(str(e))}, 500)


async def ai_explain_handler(request):
    try:
        out = await _handle_tutor_assist_common(request, default_mode="explain")
        if isinstance(out, web.Response):
            return out
        out["explanation"] = out.get("reply", "")
        return json_resp(out)
    except json.JSONDecodeError:
        return json_resp({"success": False, "error": "Invalid JSON body"}, 400)
    except Exception as e:
        return json_resp({"success": False, "error": ai._sanitize_error_text(str(e))}, 500)


async def api_ai_history_list(request):
    """GET /api/ai/history — lấy các phiên hội thoại AI (đang mở hoặc đã lưu trữ khi xóa màn hình)."""
    try:
        acc = _extract_account_id(request)
        archived = request.query.get("archived", "all")
        q_str = request.query.get("q", "")
        session_id = request.query.get("session_id") or None
        try:
            limit = int(request.query.get("limit", "50"))
        except (TypeError, ValueError):
            limit = 50
        res = await asyncio.to_thread(
            db.list_tutor_chat_sessions,
            account_id=acc,
            archived=archived,
            query=q_str,
            session_id=session_id,
            limit=limit,
        )
        res["success"] = True
        return json_resp(res)
    except Exception as e:
        return json_resp({"success": False, "error": ai._sanitize_error_text(str(e))}, 500)


async def api_ai_history_save(request):
    """POST /api/ai/history — lưu lượt hỏi/đáp hoặc toàn bộ phiên chat gia sư AI."""
    try:
        data = await safe_get_json(request)
        if not isinstance(data, dict):
            return json_resp({"success": False, "error": "JSON object expected"}, 400)
        acc = _extract_account_id(request, data)
        messages = data.get("messages") if isinstance(data.get("messages"), list) else None
        content = str(data.get("content") or "").strip()
        if not messages and not content:
            return json_resp({"success": False, "error": "Cần content hoặc danh sách messages để lưu lịch sử."}, 400)

        sess = await asyncio.to_thread(
            db.save_tutor_chat_turn,
            account_id=acc,
            session_id=data.get("session_id"),
            title=str(data.get("title") or "").strip(),
            subject_id=data.get("subject_id"),
            subject_name=str(data.get("subject_name") or "").strip(),
            mode=str(data.get("mode") or "explain").strip(),
            persona=str(data.get("persona") or "professor").strip(),
            role=str(data.get("role") or "user").strip(),
            content=content,
            context=data.get("context") if isinstance(data.get("context"), dict) else None,
            provider_used=str(data.get("provider_used") or "").strip(),
            model_used=str(data.get("model_used") or "").strip(),
            masked_key=str(data.get("masked_key") or "").strip(),
            latency_ms=data.get("latency_ms"),
            messages=messages,
            replace=bool(data.get("replace", False)),
        )
        return json_resp({"success": True, "account_id": acc, "session_id": sess["session_id"], "session": sess})
    except json.JSONDecodeError:
        return json_resp({"success": False, "error": "Invalid JSON body"}, 400)
    except Exception as e:
        return json_resp({"success": False, "error": ai._sanitize_error_text(str(e))}, 500)


async def api_ai_history_archive(request):
    """POST /api/ai/history/archive — Xóa màn hình (lưu trữ mềm is_archived=1) hoặc khôi phục lại."""
    try:
        data = await safe_get_json(request)
        if not isinstance(data, dict):
            return json_resp({"success": False, "error": "JSON object expected"}, 400)
        acc = _extract_account_id(request, data)
        restore = bool(data.get("restore", False))
        archive_all = bool(data.get("archive_all_active", False))
        sid = data.get("session_id")
        sids = data.get("session_ids") if isinstance(data.get("session_ids"), list) else None
        updated = await asyncio.to_thread(
            db.archive_tutor_chat_sessions,
            account_id=acc,
            session_id=sid,
            session_ids=sids,
            archive_all_active=archive_all,
            restore=restore,
        )
        return json_resp({
            "success": True,
            "account_id": acc,
            "updated_count": updated,
            "restored": restore,
        })
    except json.JSONDecodeError:
        return json_resp({"success": False, "error": "Invalid JSON body"}, 400)
    except Exception as e:
        return json_resp({"success": False, "error": ai._sanitize_error_text(str(e))}, 500)


async def api_ai_history_delete(request):
    """DELETE /api/ai/history/{session_id} hoặc POST /api/ai/history/delete — xóa vĩnh viễn phiên trong kho lưu trữ."""
    try:
        data = {}
        if request.method == "POST" and request.can_read_body:
            try:
                raw_data = await safe_get_json(request)
                if isinstance(raw_data, dict):
                    data = raw_data
            except Exception:
                data = {}
        acc = _extract_account_id(request, data)
        sid = (
            request.match_info.get("session_id")
            or data.get("session_id")
            or request.query.get("session_id")
            or ""
        ).strip()
        if not sid:
            return json_resp({"success": False, "error": "session_id is required"}, 400)
        deleted = await asyncio.to_thread(db.delete_tutor_chat_session, acc, sid)
        if not deleted:
            return json_resp({"success": False, "deleted": False, "error": "Không tìm thấy phiên hội thoại"}, 404)
        return json_resp({"success": True, "deleted": True, "account_id": acc, "session_id": sid})
    except Exception as e:
        return json_resp({"success": False, "error": ai._sanitize_error_text(str(e))}, 500)


async def ai_concept_recall_handler(request):
    try:
        data = await safe_get_json(request)
        subject_name = data.get("subject_name", "Môn học")
        q_text = data.get("question_text", "")
        code = data.get("code_snippet", "")
        concept = await ai.ai_concept_recall(subject_name, q_text, code)
        return json_resp({"success": True, "concept": concept})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


async def ai_explain_mistake_handler(request):
    try:
        data = await safe_get_json(request)
        subject_name = data.get("subject_name", "Môn học")
        q_text = data.get("question_text", "")
        wrong_ans = data.get("user_wrong_answer", "")
        correct_ans = data.get("correct_answer", "")
        expl = data.get("explanation", "")
        code = data.get("code_snippet", "")
        diagnosis = await ai.ai_explain_mistake(subject_name, q_text, wrong_ans, correct_ans, expl, code)
        return json_resp({"success": True, "diagnosis": diagnosis})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


async def ai_mnemonic_handler(request):
    try:
        data = await safe_get_json(request)
        subject_name = data.get("subject_name", "Môn học")
        q_text = data.get("question_text", "")
        correct_ans = data.get("correct_answer", "")
        expl = data.get("explanation", "")
        mnemonic = await ai.ai_mnemonic_trick(subject_name, q_text, correct_ans, expl)
        return json_resp({"success": True, "mnemonic": mnemonic})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


async def ai_make_flashcard_handler(request):
    try:
        data = await safe_get_json(request)
        subject_id = int(data.get("subject_id") or 5)
        subject_name = data.get("subject_name", "")
        if not subject_name:
            subs = db.get_all_subjects()
            found = next((s for s in subs if s["id"] == subject_id), None)
            subject_name = found["name"] if found else "Môn học"
        q_text = data.get("question_text", "")
        correct_ans = data.get("correct_answer", "")
        expl = data.get("explanation", "")
        card = await ai.ai_question_to_flashcard(subject_name, q_text, correct_ans, expl)
        cid = db.add_flashcard(
            subject_id=subject_id,
            front=card.get("front", q_text[:200]),
            back=card.get("back", correct_ans),
            hint=card.get("hint", "")
        )
        return json_resp({"success": True, "id": cid, "flashcard": card})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


async def ai_explain_flashcard_handler(request):
    try:
        data = await safe_get_json(request)
        subject_name = data.get("subject_name", "Môn học")
        front = data.get("front", "")
        back = data.get("back", "")
        explanation = await ai.ai_explain_flashcard(subject_name, front, back)
        return json_resp({"success": True, "explanation": explanation})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


async def ai_expand_bank_handler(request):
    """Sinh nhanh thêm câu hỏi hoặc thẻ Flashcard cho môn học bất kỳ từ chương trình chuẩn (không cần tải file)"""
    try:
        data = await safe_get_json(request)
        subject_id = int(data.get("subject_id") or 5)
        kind = data.get("kind", "questions")
        count = max(1, min(15, int(data.get("count", 5))))
        q_type = data.get("q_type", "mcq")
        cognitive_level = data.get("cognitive_level", "mixed")

        subs = db.get_all_subjects()
        found = next((s for s in subs if s["id"] == subject_id), None)
        subject_name = data.get("subject_name") or (found["name"] if found else "Đại học")

        if kind == "flashcards":
            generated = await ai.ai_generate_flashcards(subject_name, "", count=count)
            saved_cards = []
            for item in generated:
                cid = db.add_flashcard(
                    subject_id=subject_id,
                    front=item.get("front", ""),
                    back=item.get("back", ""),
                    hint=item.get("hint", "")
                )
                saved_cards.append({"id": cid, **item})
            return json_resp({
                "success": True,
                "generated_count": len(saved_cards),
                "cards": saved_cards
            })

        generated = await ai.ai_generate_questions(subject_name, "", count=count, q_type=q_type, cognitive_level=cognitive_level)
        saved_questions = []
        for item in generated:
            q_text = item.get("question", "")
            code_snip = item.get("code_snippet", "")
            opt_a = item.get("a", "")
            opt_b = item.get("b", "")
            opt_c = item.get("c", "")
            opt_d = item.get("d", "")
            corr = item.get("correct", "A")
            expl = item.get("explanation", "")
            diff = item.get("difficulty", "medium")
            qt = item.get("q_type", q_type if q_type != "all" else "mcq")

            qid = db.add_question(
                subject_id=subject_id,
                question_text=q_text,
                code_snippet=code_snip,
                option_a=opt_a,
                option_b=opt_b,
                option_c=opt_c,
                option_d=opt_d,
                correct_option=corr,
                explanation=expl,
                difficulty=diff,
                q_type=qt
            )
            saved_questions.append({
                "id": qid,
                "subject_id": subject_id,
                "q_type": qt,
                "question_text": q_text,
                "code_snippet": code_snip,
                "option_a": opt_a,
                "option_b": opt_b,
                "option_c": opt_c,
                "option_d": opt_d,
                "correct_option": corr,
                "explanation": expl,
                "difficulty": diff
            })

        return json_resp({
            "success": True,
            "generated_count": len(saved_questions),
            "saved_questions": saved_questions
        })
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


async def ai_generate_quiz(request):
    try:
        data = await safe_get_json(request)
        subject_id = int(data.get("subject_id") or 5)
        subject_name = data.get("subject_name", "Môn học")
        content = data.get("content", "")
        count = int(data.get("count", 5))
        q_type = data.get("q_type", "mcq")
        cognitive_level = data.get("cognitive_level", "mixed")

        generated = await ai.ai_generate_questions(subject_name, content, count, q_type, cognitive_level=cognitive_level)
        saved_questions = []
        for item in generated:
            q_text = item.get("question", "")
            code_snip = item.get("code_snippet", "")
            opt_a = item.get("a", "")
            opt_b = item.get("b", "")
            opt_c = item.get("c", "")
            opt_d = item.get("d", "")
            corr = item.get("correct", "A")
            expl = item.get("explanation", "")
            diff = item.get("difficulty", "medium")
            qt = item.get("q_type", q_type if q_type != "all" else "mcq")

            qid = db.add_question(
                subject_id=subject_id,
                question_text=q_text,
                code_snippet=code_snip,
                option_a=opt_a,
                option_b=opt_b,
                option_c=opt_c,
                option_d=opt_d,
                correct_option=corr,
                explanation=expl,
                difficulty=diff,
                q_type=qt
            )
            saved_questions.append({
                "id": qid,
                "subject_id": subject_id,
                "q_type": qt,
                "question_text": q_text,
                "code_snippet": code_snip,
                "option_a": opt_a,
                "option_b": opt_b,
                "option_c": opt_c,
                "option_d": opt_d,
                "correct_option": corr,
                "explanation": expl,
                "difficulty": diff
            })

        return json_resp({
            "success": True,
            "generated_count": len(saved_questions),
            "questions": generated,
            "saved_questions": saved_questions,
            "data": {"questions": generated, "saved_count": len(saved_questions)}
        })
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


async def ai_generate_cards(request):
    try:
        data = await safe_get_json(request)
        subject_id = int(data.get("subject_id") or 5)
        subject_name = data.get("subject_name", "Môn học")
        content = data.get("content", "")
        count = int(data.get("count", 5))

        generated = await ai.ai_generate_flashcards(subject_name, content, count)
        saved_count = 0
        for item in generated:
            db.add_flashcard(
                subject_id=subject_id,
                front=item.get("front", ""),
                back=item.get("back", ""),
                hint=item.get("hint", "")
            )
            saved_count += 1

        return json_resp({
            "success": True,
            "generated_count": saved_count,
            "cards": generated,
            "data": generated
        })
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


async def ai_cheat_sheet(request):
    try:
        data = await safe_get_json(request)
        subject_name = data.get("subject_name", "Môn học")
        content = data.get("content", "")
        sheet = await ai.ai_summarize_cheat_sheet(subject_name, content)
        return json_resp({
            "success": True,
            "cheat_sheet": sheet,
            "data": {"markdown": sheet}
        })
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


# ==========================================
# Handlers: Stats & Multi-Key Pool Settings
# ==========================================

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


async def get_stats(request):
    stats = await asyncio.to_thread(db.get_stats)
    return json_resp({"success": True, "stats": stats})


async def handle_ai_gateway_diag(request):
    """Chẩn đoán đường đi AI: cấu hình hiện tại + khả năng dò Cloudflare Tunnel."""
    info = {
        "code_version": "gateway-diag-v2",
        "discovery_env_set": bool(os.environ.get("AI_GATEWAY_DISCOVERY_URL", "").strip()),
        "discovery_url_used": ai.gateway_discovery_url(),
        "secret_required_by_client": bool(ai.gateway_secret()),
        "is_local_runtime": ai._is_local_runtime(),
    }
    try:
        cfg = await asyncio.to_thread(ai.get_openai_settings)
        info["configured_base_url"] = cfg.get("base_url", "")
        info["configured_model"] = cfg.get("model", "")
        info["provider_type"] = cfg.get("provider_type", "")
        info["has_key"] = bool(cfg.get("key"))
        info["masked_key"] = ai.mask_key(cfg.get("key", "")) if cfg.get("key") else ""
    except Exception as exc:
        info["settings_error"] = ai._sanitize_error_text(str(exc))

    resolved = ""
    try:
        resolved = await ai.resolve_gateway_base_url(info.get("configured_base_url", ""))
        info["resolved_base_url"] = resolved
    except Exception as exc:
        info["resolve_error"] = ai._sanitize_error_text(str(exc))

    if resolved and resolved.startswith("http"):
        ok_u, norm_u, _ = ai.validate_router_base_url(resolved)
        if ok_u:
            root = norm_u[:-3] if norm_u.endswith("/v1") else norm_u.rstrip("/")
            try:
                session = await ai._get_http_session()
                async with session.get(f"{root}/healthz", timeout=aiohttp.ClientTimeout(total=12)) as resp:
                    info["gateway_health_status"] = resp.status
                    info["gateway_reachable"] = resp.status == 200
            except Exception as exc:
                info["gateway_reachable"] = False
                info["gateway_health_error"] = ai._sanitize_error_text(str(exc))

    ok = bool(info.get("gateway_reachable"))
    info["success"] = ok
    info["verdict"] = (
        "Tunnel OK - Gateway phản hồi bình thường."
        if ok
        else "Gateway/Tunnel chưa phản hồi. Kiểm tra dịch vụ 9Router / start_ai_gateway đang chạy hay chưa."
    )
    return json_resp(info)


async def handle_test_openai_key(request):
    """POST /api/ai/test_9router (and /api/ai/test-9router, /api/ai/test-openai)."""
    auth_err = _require_admin_if_auth(request)
    if auth_err:
        return auth_err
    allowed, retry_after = _check_rate_limit(request, "ai_test", limit=15, window_sec=60)
    if not allowed:
        return json_resp(
            {"success": False, "error": f"Quá nhiều lượt kiểm tra 9Router/OpenAI. Thử lại sau {retry_after}s.", "retry_after": retry_after},
            429,
        )
    try:
        data = await safe_get_json(request)
        if not isinstance(data, dict):
            return json_resp({"success": False, "message": "JSON object expected"}, 400)
        key = str(data.get("api_key") or data.get("key") or "").strip()
        base_url = str(data.get("base_url") or data.get("router_base_url") or "").strip()
        model = str(data.get("model") or data.get("router_model") or "").strip()
        res = await ai.test_9router_endpoint(key=key, base_url=base_url, model=model)
        status_code = 400 if res.get("status_code") == 400 else 200
        return json_resp(res, status=status_code)
    except json.JSONDecodeError:
        return json_resp({"success": False, "message": "Invalid JSON body"}, 400)
    except Exception as e:
        return json_resp({"success": False, "message": ai._sanitize_error_text(str(e))}, status=500)


async def get_settings(request):
    return json_resp(await _build_keys_status_payload())


async def save_settings(request):
    auth_err = _require_admin_if_auth(request)
    if auth_err:
        return auth_err
    try:
        data = await safe_get_json(request)
        if not isinstance(data, dict):
            return json_resp({"success": False, "error": "JSON object expected"}, 400)

        def _apply_gemini_updates():
            current_pool = ai.get_api_keys_pool()
            if data.get("clear_all_keys"):
                ai.save_api_keys_pool([])
            elif "remove_key_index" in data:
                rm_idx = int(data["remove_key_index"])
                ai.delete_gemini_key_from_pool(zero_index=rm_idx, sync_env=True)
            elif "add_api_keys" in data:
                raw_new = data["add_api_keys"]
                tokens = ai._parse_key_tokens(raw_new) if isinstance(raw_new, str) else [
                    str(x).strip()
                    for x in (raw_new or [])
                    if str(x).strip() and not ai._is_masked_placeholder(str(x).strip())
                ]
                existing_set = {item["key"] for item in current_pool}
                added_any = False
                for nk in tokens:
                    ok_fmt, _ = ai.validate_gemini_key_format(nk)
                    if ok_fmt and nk not in existing_set:
                        existing_set.add(nk)
                        current_pool.append({"key": nk, "label": f"Key #{len(current_pool) + 1}"})
                        added_any = True
                if added_any:
                    ai.save_api_keys_pool(current_pool)
            elif "gemini_api_keys" in data:
                raw_val = data["gemini_api_keys"]
                parsed_tokens = ai._parse_key_tokens(raw_val) if isinstance(raw_val, str) else [
                    str(x).strip()
                    for x in (raw_val or [])
                    if str(x).strip() and not ai._is_masked_placeholder(str(x).strip())
                ]
                valid_tokens = [t for t in parsed_tokens if ai.validate_gemini_key_format(t)[0]]
                if valid_tokens:
                    ai.save_api_keys_pool(valid_tokens)
            elif "gemini_api_key" in data:
                single_k = str(data["gemini_api_key"] or "").strip()
                if single_k and not ai._is_masked_placeholder(single_k):
                    ok_fmt, _ = ai.validate_gemini_key_format(single_k)
                    if ok_fmt:
                        existing_set = {item["key"] for item in current_pool}
                        if single_k not in existing_set:
                            current_pool.append({"key": single_k, "label": f"Key #{len(current_pool) + 1}"})
                            ai.save_api_keys_pool(current_pool)

        await asyncio.to_thread(_apply_gemini_updates)

        has_router_fields = any(
            k in data
            for k in (
                "clear_openai_key",
                "clear_router_key",
                "openai_api_key",
                "router_api_key",
                "openai_base_url",
                "router_base_url",
                "openai_model",
                "router_model",
                "ai_provider_priority",
                "priority",
            )
        )
        if has_router_fields:
            base_url = data.get("router_base_url") if "router_base_url" in data else data.get("openai_base_url")
            if "router_api_key" in data:
                api_key = data.get("router_api_key")
            elif "openai_api_key" in data:
                api_key = data.get("openai_api_key")
            else:
                api_key = None
            model = data.get("router_model") if "router_model" in data else data.get("openai_model")
            priority = data.get("ai_provider_priority") if "ai_provider_priority" in data else data.get("priority")
            clear_key = bool(data.get("clear_openai_key") or data.get("clear_router_key"))

            ok_r, _, err_r = await asyncio.to_thread(
                ai.save_router_config,
                base_url=base_url,
                api_key=api_key,
                model=model,
                priority=priority,
                clear_key=clear_key,
            )
            if not ok_r:
                return json_resp({"success": False, "error": err_r}, 400)

        payload = await _build_keys_status_payload()
        payload["message"] = (
            f"Đã cập nhật dàn {payload['total_count']} Gemini API Key (được bảo mật trên server) và cấu hình AI Gateway!"
        )
        return json_resp(payload)
    except json.JSONDecodeError:
        return json_resp({"success": False, "error": "Invalid JSON body"}, 400)
    except Exception as e:
        return json_resp({"success": False, "error": ai._sanitize_error_text(str(e))}, 500)


def get_lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return "127.0.0.1"


def _read_active_tunnel_url() -> str:
    tunnel_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "online_tunnel.json")
    if not os.path.exists(tunnel_file):
        return os.environ.get("PUBLIC_URL", "").strip()
    try:
        with open(tunnel_file, encoding="utf-8") as f:
            info = json.load(f)
        # Chỉ dùng nếu được cập nhật trong 12 giờ gần nhất
        if time.time() - float(info.get("updated_at", 0)) < 43200:
            return str(info.get("public_url", "")).strip()
    except Exception:
        pass
    return os.environ.get("PUBLIC_URL", "").strip()


async def get_network_info(request):
    ip = get_lan_ip()
    lan_url = f"http://{ip}:{PORT}"
    # Khi truy cập qua Internet (Cloudflare Tunnel / Render / Railway...), trả về đúng địa chỉ công khai
    host = request.headers.get("X-Forwarded-Host") or request.host or ""
    hostname = host.split(":")[0]
    is_public = bool(hostname) and hostname not in ("localhost", "127.0.0.1", ip) and not re.match(
        r"^(10\.|192\.168\.|172\.(1[6-9]|2\d|3[01])\.)", hostname
    )
    public_url = (
        f"{'https' if _is_https(request) else 'http'}://{host}"
        if is_public
        else _read_active_tunnel_url()
    )
    return json_resp({
        "success": True,
        "lan_ip": ip,
        "port": PORT,
        "lan_url": public_url or lan_url,
        "local_wifi_url": lan_url,
        "public_url": public_url,
        "permanent_gateway_url": "https://ntfy.sh/unimaster_ctump_5292",
        "is_online": bool(public_url),
        "auth_enabled": AUTH_ENABLED
    })


async def get_user_state(request):
    uid = request.get("user", {}).get("id", 1)
    state = db.get_user_sync_state(uid)
    return json_resp({"success": True, "state": state})


async def save_user_state(request):
    try:
        uid = request.get("user", {}).get("id", 1)
        incoming = await safe_get_json(request)
        saved = db.save_user_sync_state(uid, incoming)
        return json_resp({"success": True, "state": saved})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


def _image_url_to_base64(img_url: str, cache: dict) -> str:
    if not img_url or not img_url.startswith("/static/"):
        return img_url
    if img_url in cache:
        return cache[img_url]
    try:
        import base64
        base_dir = os.path.dirname(os.path.abspath(__file__))
        rel = img_url.lstrip("/").replace("/", os.sep)
        abs_p = os.path.join(base_dir, rel)
        if os.path.exists(abs_p):
            ext = os.path.splitext(abs_p)[1].lower()
            mime = {".png": "image/png", ".webp": "image/webp", ".gif": "image/gif"}.get(ext, "image/jpeg")
            with open(abs_p, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("ascii")
            data_uri = f"data:{mime};base64,{b64}"
            cache[img_url] = data_uri
            return data_uri
    except Exception:
        pass
    return img_url


def build_full_snapshot(include_api_key=False, embed_images_base64=False):
    subjects = db.get_all_subjects()
    questions_by_sub = {}
    exercises_by_sub = {}
    flashcards_by_sub = {}
    img_cache = {}
    for s in subjects:
        sid = str(s["id"])
        q_list = db.get_questions_by_subject(s["id"])
        if embed_images_base64:
            enriched = []
            for q in q_list:
                q_copy = dict(q)
                if q_copy.get("image_url"):
                    q_copy["image_url"] = _image_url_to_base64(q_copy["image_url"], img_cache)
                enriched.append(q_copy)
            questions_by_sub[sid] = enriched
        else:
            questions_by_sub[sid] = q_list
        exercises_by_sub[sid] = db.get_exercises_by_subject(s["id"])
        flashcards_by_sub[sid] = db.get_flashcards_by_subject(s["id"])

    raw_state = db.get_setting("user_sync_state", "{}")
    try:
        user_state = json.loads(raw_state) if raw_state else {}
        if isinstance(user_state, dict):
            for secret_k in ("gemini_api_key", "gemini_api_keys", "gemini_api_keys_pool", "openai_api_key"):
                user_state.pop(secret_k, None)
    except Exception:
        user_state = {}

    snap = {
        "version": "10.0",
        "subjects": subjects,
        "questions_by_subject": questions_by_sub,
        "exercises_by_subject": exercises_by_sub,
        "flashcards_by_subject": flashcards_by_sub,
        "stats": db.get_stats(),
        "user_state": user_state,
        "image_base64_map": img_cache,
        "ai_keys_secured_on_server": True,
        "ai_key_count": len(ai.get_api_keys_pool()),
    }
    return snap


async def get_offline_snapshot(request):
    """Trả về gói dữ liệu đầy đủ (kèm ảnh Base64, không bao giờ gắn API key thô) để trình duyệt lưu vào IndexedDB chạy khi tắt PC"""
    snap = await asyncio.to_thread(build_full_snapshot, include_api_key=False, embed_images_base64=True)
    return json_resp({"success": True, "snapshot": snap})


async def export_backup(request):
    def _build():
        snap = build_full_snapshot(include_api_key=False)
        return json.dumps(snap, ensure_ascii=False, indent=2)

    body = await asyncio.to_thread(_build)
    return web.Response(
        text=body,
        content_type="application/json",
        headers={"Content-Disposition": 'attachment; filename="UniMaster_Backup.json"'},
    )


async def import_backup(request):
    auth_err = _require_admin_if_auth(request)
    if auth_err:
        return auth_err
    try:
        data = await safe_get_json(request)

        def _do_import():
            if "user_state" in data and isinstance(data["user_state"], dict):
                db.set_setting("user_sync_state", json.dumps(data["user_state"], ensure_ascii=False))

            existing_codes = {s["code"]: s["id"] for s in db.get_all_subjects()}
            imported_q = 0
            for s in data.get("subjects", []):
                code = s.get("code", "")
                old_sid = str(s.get("id", ""))
                if code and code not in existing_codes:
                    new_sid = db.add_subject(code, s.get("name", code), s.get("icon", "📘"), s.get("category", ""), s.get("description", ""))
                    existing_codes[code] = new_sid
                    for q in data.get("questions_by_subject", {}).get(old_sid, []):
                        db.add_question(
                            new_sid, q.get("question_text", ""), q.get("option_a", ""), q.get("option_b", ""),
                            q.get("option_c", ""), q.get("option_d", ""), q.get("correct_option", "A"),
                            q.get("explanation", ""), q.get("difficulty", "medium"), q.get("q_type", "mcq"),
                            q.get("code_snippet", "")
                        )
                        imported_q += 1
            return imported_q

        imported_q = await asyncio.to_thread(_do_import)
        return json_resp({"success": True, "imported_questions": imported_q, "message": "Đã khôi phục dữ liệu thành công!"})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


async def admin_upload_backup(request):
    """Nhận file .db từ Admin để khôi phục dữ liệu an toàn."""
    user_info = request.get("user", {})
    if user_info.get("role") != "admin":
        return json_resp({"success": False, "error": "Chỉ Quản trị viên mới có quyền tải lên cơ sở dữ liệu."}, 403)

    reader = await request.multipart()
    field = await reader.next()
    if not field or field.name != 'file':
        return json_resp({"success": False, "error": "Không tìm thấy file tải lên."}, 400)

    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp_path = tmp.name
    tmp.close()
    try:
        with open(tmp_path, 'wb') as f:
            while True:
                chunk = await field.read_chunk()
                if not chunk:
                    break
                f.write(chunk)

        def _verify_and_restore():
            conn = sqlite3.connect(tmp_path)
            cur = conn.cursor()
            cur.execute("PRAGMA integrity_check;")
            res = cur.fetchone()
            conn.close()
            if not res or res[0] != "ok":
                return False, f"File SQLite không hợp lệ hoặc bị hỏng ({res[0] if res else 'unknown'})."
            target_conn = sqlite3.connect(db.DB_PATH)
            source_conn = sqlite3.connect(tmp_path)
            source_conn.backup(target_conn)
            target_conn.close()
            source_conn.close()
            db.init_db()
            return True, ""

        ok, err_msg = await asyncio.to_thread(_verify_and_restore)
        if not ok:
            return json_resp({"success": False, "error": err_msg}, 400)
        return json_resp({"success": True, "message": "Đã khôi phục cơ sở dữ liệu thành công!"})
    except Exception as e:
        return json_resp({"success": False, "error": f"Lỗi khi khôi phục: {str(e)}"}, 500)
    finally:
        try:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
        except OSError:
            pass


async def admin_download_backup(request):
    """Cho phép Admin tải về file .db hiện tại với dữ liệu nhất quán."""
    user_info = request.get("user", {})
    if user_info.get("role") != "admin":
        return json_resp({"success": False, "error": "Chỉ Quản trị viên mới có quyền tải về."}, 403)

    if not os.path.exists(db.DB_PATH):
        return json_resp({"success": False, "error": "Không tìm thấy file dữ liệu."}, 404)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    def _snapshot_db_bytes():
        tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        tmp_path = tmp.name
        tmp.close()
        try:
            src = sqlite3.connect(db.DB_PATH)
            dst = sqlite3.connect(tmp_path)
            src.backup(dst)
            src.close()
            dst.close()
            with open(tmp_path, "rb") as f:
                return f.read()
        finally:
            try:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
            except OSError:
                pass

    content = await asyncio.to_thread(_snapshot_db_bytes)
    return web.Response(
        body=content,
        content_type="application/x-sqlite3",
        headers={"Content-Disposition": f'attachment; filename="unimaster-{stamp}.db"'},
    )


def generate_standalone_html_string() -> str:
    with open(os.path.join(STATIC_DIR, "index.html"), encoding="utf-8") as f:
        html = f.read()
    with open(os.path.join(STATIC_DIR, "style.css"), encoding="utf-8") as f:
        css = f.read()
    with open(os.path.join(STATIC_DIR, "app.js"), encoding="utf-8") as f:
        js = f.read()

    snap = build_full_snapshot(include_api_key=False, embed_images_base64=True)
    snap_json = json.dumps(snap, ensure_ascii=False).replace("</script>", "<\\/script>")

    html = re.sub(
        r'<link\s+rel="stylesheet"\s+href="/static/style\.css[^"]*"\s*/?>',
        lambda _: f"<style>\n{css}\n</style>",
        html
    )
    html = re.sub(
        r'<script\s+src="/static/app\.js[^"]*"></script>',
        lambda _: f"<script>window.__UNIMASTER_OFFLINE_DB__ = {snap_json};</script>\n<script>\n{js}\n</script>",
        html
    )
    if re.search(r"(AQ\.Ab[A-Za-z0-9._-]{16,}|AIzaSy[A-Za-z0-9_-]{16,}|sk-[A-Za-z0-9_-]{20,})", html):
        raise ValueError("Security check failed: raw API key detected in standalone HTML output")
    return html


async def export_standalone_html(request):
    """Tạo 1 file HTML siêu độc lập chứa trọn bộ Ngân hàng câu hỏi + Ảnh Base64 + Offline chạy mọi nơi khi TẮT PC"""
    try:
        html = await asyncio.to_thread(generate_standalone_html_string)
        return web.Response(
            text=html,
            content_type="text/html",
            charset="utf-8",
            headers={"Content-Disposition": 'attachment; filename="UniMaster_Chay_Moi_Noi_Khong_Can_PC.html"'},
        )
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


async def pwa_manifest(request):
    manifest = {
        "name": "UniMaster AI Pro v10.0",
        "short_name": "UniMaster",
        "description": "Hệ thống ôn thi Đại học thông minh tích hợp AI — Chạy mọi nơi kể cả khi tắt PC",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#000000",
        "theme_color": "#7c3aed",
        "icons": [
            {"src": "/icon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any maskable"}
        ]
    }
    return json_resp(manifest)


async def pwa_icon_svg(request):
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
      <defs>
        <linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#7c3aed"/>
          <stop offset="100%" stop-color="#ec4899"/>
        </linearGradient>
      </defs>
      <rect width="256" height="256" rx="56" fill="url(#g)"/>
      <text x="128" y="172" font-family="Arial,sans-serif" font-size="136" font-weight="900" text-anchor="middle" fill="#ffffff">U</text>
    </svg>"""
    return web.Response(text=svg, content_type="image/svg+xml")


async def pwa_sw(request):
    sw_code = """
    const CACHE_NAME = 'unimaster-pwa-v25';
    const CORE_ASSETS = [
      '/',
      '/static/index.html',
      '/static/style.css?v=25.0',
      '/static/app.js?v=25.0',
      '/manifest.json',
      '/icon.svg'
    ];
    self.addEventListener('install', (e) => {
      e.waitUntil(
        caches.open(CACHE_NAME).then((cache) => cache.addAll(CORE_ASSETS)).catch(() => {})
      );
      self.skipWaiting();
    });
    self.addEventListener('activate', (e) => {
      e.waitUntil(
        caches.keys().then((keys) => Promise.all(
          keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k))
        )).then(() => self.clients.claim())
      );
    });
    self.addEventListener('fetch', (e) => {
      if (e.request.method !== 'GET') return;
      e.respondWith(
        fetch(e.request)
          .then((resp) => {
            if (resp && resp.status === 200 && (e.request.url.includes('/static/') || e.request.mode === 'navigate')) {
              const clone = resp.clone();
              caches.open(CACHE_NAME).then((c) => c.put(e.request, clone)).catch(() => {});
            }
            return resp;
          })
          .catch(() => caches.match(e.request).then((r) => r || caches.match('/')))
      );
    });
    """
    return web.Response(text=sw_code, content_type="application/javascript")


# ==========================================
# App Factory & Routes
# ==========================================

# =========================================================================
# MODULE 1 & 2 & 3: CODE RUNNER, ESSAY GRADER & TIMED EXAM HANDLERS
# =========================================================================
async def api_code_run(request):
    try:
        data = await safe_get_json(request)
        lang = data.get("language", "cpp")
        code = data.get("code", "")
        inp = data.get("input_data", "")
        res = await code_engine.execute_code(lang, code, inp)
        return json_resp(res)
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)

async def api_code_test(request):
    try:
        data = await safe_get_json(request)
        ex_id = int(data.get("exercise_id", 0))
        lang = data.get("language", "cpp")
        code = data.get("code", "")
        res = await code_engine.test_code_against_cases(ex_id, lang, code)
        return json_resp(res)
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)

async def api_code_ai_review(request):
    try:
        data = await safe_get_json(request)
        title = data.get("title", "")
        problem = data.get("problem", "")
        code = data.get("code", "")
        lang = data.get("language", "cpp")
        res = await code_engine.ai_review_code_advanced(title, problem, code, lang)
        return json_resp({"success": True, "review": res})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)

async def api_get_essay_prompts(request):
    try:
        sid = request.query.get("subject_id")
        subject_id = int(sid) if sid and sid.isdigit() else None
        prompts = db.get_essay_prompts(subject_id)
        return json_resp({"success": True, "prompts": prompts})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)

async def api_grade_essay_advanced(request):
    try:
        data = await safe_get_json(request)
        prompt_id = data.get("prompt_id", "")
        student_answer = data.get("student_answer", "")
        question_text = data.get("question_text", "")
        rubric = data.get("rubric", {})
        res = await code_engine.grade_essay_advanced(prompt_id, student_answer, question_text, json.dumps(rubric) if isinstance(rubric, dict) else str(rubric))
        return json_resp({"success": True, "result": res})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)

async def api_timed_exam_start(request):
    try:
        sid = int(request.query.get("subject_id", 5))
        count = int(request.query.get("count", 40))
        duration = int(request.query.get("duration", 60))
        res = await asyncio.to_thread(code_engine.start_timed_exam, sid, count=count, duration_minutes=duration)
        return json_resp(res)
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


async def api_timed_exam_submit(request):
    try:
        data = await safe_get_json(request)
        sid = int(data.get("subject_id", 5))
        answers = data.get("answers", {})
        time_spent = int(data.get("time_spent_seconds", 0))
        draft_key = str(data.get("draft_key") or "").strip()
        user_info = request.get("user") or {"id": 1}
        user_id = user_info.get("id", 1)
        acc_id = _extract_account_id(request, data)

        def _submit():
            out = code_engine.submit_timed_exam(sid, answers, time_spent, user_id=user_id)
            if draft_key:
                out["draft_cleared"] = db.delete_study_progress(acc_id, draft_key)
            return out

        res = await asyncio.to_thread(_submit)
        return json_resp(res)
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


# =========================================================================
# UNIMASTER v15.0 SPECIAL EXAM HANDLERS
# =========================================================================
async def api_validate_oop_structure(request):
    try:
        data = await safe_get_json(request)
        code = data.get("code", "")
        req = data.get("requirements", {})
        res = await asyncio.to_thread(code_engine.validate_csharp_oop_structure, code, req)
        return json_resp(res)
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


async def api_exam_shuffle(request):
    try:
        sid = int(request.query.get("subject_id", 5))
        count = int(request.query.get("count", 40))

        def _shuffle():
            all_qs = db.get_questions_by_subject(sid)
            selected = random.sample(all_qs, count) if len(all_qs) > count else all_qs
            return code_engine.fisher_yates_shuffle_exam(selected)

        shuffled = await asyncio.to_thread(_shuffle)
        return json_resp({"success": True, "questions": shuffled})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


async def api_sm2_review(request):
    try:
        data = await safe_get_json(request)
        card_id = int(data.get("card_id", 0))
        rating = data.get("rating", "good")
        res = await asyncio.to_thread(code_engine.calculate_sm2, card_id, rating)
        return json_resp(res)
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


async def api_sm2_due_today(request):
    try:
        sid = request.query.get("subject_id")
        subject_id = int(sid) if sid and sid.isdigit() else None

        def _due():
            conn = db.get_connection()
            try:
                c = conn.cursor()
                if subject_id:
                    c.execute(
                        """
                        SELECT * FROM flashcards
                        WHERE subject_id = ? AND (next_review <= datetime('now') OR next_review IS NULL OR next_review = '')
                        ORDER BY interval_days ASC LIMIT 150
                        """,
                        (subject_id,),
                    )
                else:
                    c.execute(
                        """
                        SELECT * FROM flashcards
                        WHERE next_review <= datetime('now') OR next_review IS NULL OR next_review = ''
                        ORDER BY interval_days ASC LIMIT 150
                        """
                    )
                return [dict(r) for r in c.fetchall()]
            finally:
                conn.close()

        rows = await asyncio.to_thread(_due)
        return json_resp({"success": True, "count": len(rows), "cards": rows})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)

async def api_validate_essay_steps(request):
    try:
        data = await safe_get_json(request)
        q_text = data.get("question_text", "")
        proof = data.get("student_proof", "")
        topic = data.get("topic", "Toán Rời Rạc")
        res = await code_engine.validate_essay_step_by_step(q_text, proof, topic)
        return json_resp({"success": True, "validation": res})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)

async def api_rubber_duck(request):
    try:
        data = await safe_get_json(request)
        code = data.get("code", "")
        lang = data.get("language", "csharp")
        err = data.get("error_trace", "")
        reply = await code_engine.rubber_duck_critique(code, lang, err)
        return json_resp({"success": True, "reply": reply})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)

async def _telegram_backup_once():
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_BACKUP_CHAT_ID", "").strip()
    if not token or not chat_id or not os.path.exists(db.DB_PATH):
        return False
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    try:
        source = sqlite3.connect(db.DB_PATH)
        target = sqlite3.connect(tmp.name)
        source.backup(target)
        target.close(); source.close()
        with open(tmp.name, "rb") as backup:
            form = aiohttp.FormData()
            form.add_field("chat_id", chat_id)
            form.add_field("document", backup, filename=f"unimaster-{stamp}.db", content_type="application/octet-stream")
            async with aiohttp.ClientSession() as session:
                async with session.post(f"https://api.telegram.org/bot{token}/sendDocument", data=form, timeout=60) as response:
                    return response.status == 200
    finally:
        try: os.unlink(tmp.name)
        except OSError: pass

async def _telegram_backup_loop():
    hours = max(1, int(os.environ.get("TELEGRAM_BACKUP_INTERVAL_HOURS", "24")))
    while True:
        try:
            await _telegram_backup_once()
        except Exception as exc:
            print(f"⚠️ Telegram backup failed: {exc}")
        await asyncio.sleep(hours * 3600)

def create_app():
    db.init_db()
    # Always repair the catalog first: cloud volumes can start with an empty DB
    # even though the large question-bank seeders below only add 4 newer subjects.
    catalog_seed.ensure_core_subject_catalog()
    db.ensure_admin_user(APP_PASSWORD or "uni-5292")
    stem_seed.ensure_stem_and_math_upgraded()
    seed_hoasinh_ctump.ensure_hoasinh_ctump_seeded()
    # Raise client_max_size to 30 MB for PDF / PowerPoint / Word / Image uploads
    app = web.Application(
        middlewares=[auth_middleware, no_cache_static_middleware],
        client_max_size=30 * 1024 * 1024
    )

    app.router.add_get("/login", login_page)
    app.router.add_post("/api/login", login_api)
    app.router.add_post("/api/logout", auth_logout_api)
    app.router.add_post("/api/auth/login", auth_login_api)
    app.router.add_post("/api/auth/register", auth_register_api)
    app.router.add_post("/api/auth/logout", auth_logout_api)
    app.router.add_get("/api/auth/me", auth_me_api)
    app.router.add_get("/api/auth/login-history", auth_login_history_api)
    app.router.add_get("/api/admin/users", admin_get_users_api)
    app.router.add_get("/api/admin/login-events", admin_login_events_api)
    app.router.add_delete("/api/admin/users/{id}", admin_delete_user_api)
    app.router.add_get("/healthz", healthz)

    app.router.add_get("/api/subjects", get_subjects)
    app.router.add_post("/api/subjects", create_subject)
    app.router.add_delete("/api/subjects/{id}", delete_subject)

    app.router.add_get("/api/subjects/{id}/questions", get_questions)
    app.router.add_post("/api/subjects/{id}/questions", create_question)
    app.router.add_get("/api/subjects/{id}/exercises", get_exercises)
    app.router.add_post("/api/exam/submit", submit_exam)
    app.router.add_post("/api/exams/submit", submit_exam)
    app.router.add_get("/api/exam/detail/{id}", get_exam_detail)

    app.router.add_get("/api/progress", list_progress_handler)
    app.router.add_post("/api/progress", save_progress_handler)
    app.router.add_post("/api/progress/delete", delete_progress_handler)
    app.router.add_get("/api/progress/{draft_key}", get_progress_item_handler)
    app.router.add_delete("/api/progress/{draft_key}", delete_progress_handler)

    app.router.add_get("/api/questions/{id}/discussions", get_question_discussions_handler)
    app.router.add_post("/api/questions/{id}/discussions", add_question_discussion_handler)
    app.router.add_post("/api/discussions/{id}/upvote", upvote_discussion_handler)

    app.router.add_get("/api/subjects/{id}/flashcards", get_flashcards)
    app.router.add_post("/api/subjects/{id}/flashcards", create_flashcard)
    app.router.add_post("/api/flashcards/{id}/review", review_flashcard)

    app.router.add_post("/api/upload-document", upload_document_handler)
    app.router.add_post("/api/import-direct-questions", import_direct_questions_handler)
    app.router.add_post("/api/ai/generate-image-question", ai_generate_image_question_handler)
    app.router.add_post("/api/ai/grade-handwritten", ai_grade_handwritten_handler)

    app.router.add_get("/api/ai/keys", api_ai_keys_handler)
    app.router.add_post("/api/ai/keys/add", api_ai_keys_add)
    app.router.add_post("/api/ai/keys/delete", api_ai_keys_delete)
    app.router.add_delete("/api/ai/keys/{index}", api_ai_keys_delete)
    app.router.add_post("/api/ai/keys/toggle", api_ai_keys_toggle)
    app.router.add_post("/api/ai/9router", api_ai_9router_config)
    app.router.add_post("/api/ai/test_keys", test_all_keys_handler)
    app.router.add_post("/api/ai/test-keys", test_all_keys_handler)
    app.router.add_post("/api/ai/test-key", test_key_handler)
    app.router.add_post("/api/ai/test-all-keys", test_all_keys_handler)
    app.router.add_post("/api/ai/test_9router", handle_test_openai_key)
    app.router.add_post("/api/ai/test-9router", handle_test_openai_key)
    app.router.add_post("/api/ai/test-openai", handle_test_openai_key)
    app.router.add_get("/api/ai/gateway-diag", handle_ai_gateway_diag)
    app.router.add_post("/api/ai/hint", ai_hint_handler)
    app.router.add_post("/api/ai/explain", ai_explain_handler)
    app.router.add_post("/api/ai/tutor-assist", ai_tutor_assist_handler)
    app.router.add_post("/api/ai/concept-recall", ai_concept_recall_handler)
    app.router.add_post("/api/ai/deep-analysis", ai_deep_analysis_handler)
    app.router.add_post("/api/ai/explain-mistake", ai_explain_mistake_handler)
    app.router.add_post("/api/ai/mnemonic", ai_mnemonic_handler)
    app.router.add_post("/api/ai/make-flashcard", ai_make_flashcard_handler)
    app.router.add_post("/api/ai/explain-flashcard", ai_explain_flashcard_handler)
    app.router.add_post("/api/ai/expand-bank", ai_expand_bank_handler)
    app.router.add_post("/api/ai/similar-question", ai_similar_handler)
    app.router.add_post("/api/ai/custom-qa", ai_custom_qa_handler)
    app.router.add_post("/api/ai/grade-essay", ai_grade_essay_handler)
    app.router.add_post("/api/ai/roadmap", ai_roadmap_handler)
    app.router.add_post("/api/ai/evaluate-exam", ai_evaluate_exam_handler)
    app.router.add_post("/api/ai/explain-exercise", ai_explain_exercise_handler)

    app.router.add_post("/api/ai/chat", ai_chat)
    app.router.add_get("/api/ai/history", api_ai_history_list)
    app.router.add_post("/api/ai/history", api_ai_history_save)
    app.router.add_post("/api/ai/history/archive", api_ai_history_archive)
    app.router.add_delete("/api/ai/history/{session_id}", api_ai_history_delete)
    app.router.add_post("/api/ai/history/delete", api_ai_history_delete)
    app.router.add_post("/api/ai/generate-quiz", ai_generate_quiz)
    app.router.add_post("/api/ai/generate-flashcards", ai_generate_cards)
    app.router.add_post("/api/ai/cheat-sheet", ai_cheat_sheet)

    app.router.add_post("/api/history/archive", api_archive_save)
    app.router.add_get("/api/history/archive", api_archive_list)
    app.router.add_get("/api/stats", get_stats)
    app.router.add_get("/api/settings", get_settings)
    app.router.add_post("/api/settings", save_settings)

    app.router.add_get("/api/network-info", get_network_info)
    app.router.add_get("/api/user-state", get_user_state)
    app.router.add_post("/api/user-state", save_user_state)
    app.router.add_get("/api/offline-snapshot", get_offline_snapshot)
    app.router.add_get("/api/backup/export", export_backup)
    app.router.add_post("/api/admin/backup/upload", admin_upload_backup)
    app.router.add_get("/api/admin/backup/download", admin_download_backup)
    app.router.add_post("/api/backup/import", import_backup)
    app.router.add_get("/api/export-standalone", export_standalone_html)

    # UniMaster v11.0 Extended Capabilities
    app.router.add_get("/ws/arena", extensions.websocket_arena_handler)
    app.router.add_get("/api/export/anki", extensions.export_anki_handler)
    app.router.add_get("/api/export/printable-exam", extensions.export_printable_exam_handler)
    app.router.add_get("/api/meds/search", extensions.get_drug_database_handler)
    app.router.add_post("/api/meds/calculate-dosing", extensions.calculate_renal_dose_handler)
    app.router.add_post("/api/biostat/calculate", extensions.biostat_calculate_handler)
    app.router.add_get("/api/virtual-patient/cases", extensions.get_virtual_cases_handler)

    # Exam Prep Special Routes (Code Runner, Essay Grader, Timed Exam)
    app.router.add_post("/api/code/run", api_code_run)
    app.router.add_post("/api/code/test", api_code_test)
    app.router.add_post("/api/code/ai-review", api_code_ai_review)
    app.router.add_get("/api/essay-prompts", api_get_essay_prompts)
    app.router.add_post("/api/ai/grade-essay-advanced", api_grade_essay_advanced)
    app.router.add_get("/api/timed-exam/start", api_timed_exam_start)
    app.router.add_post("/api/timed-exam/submit", api_timed_exam_submit)

    app.router.add_get("/manifest.json", pwa_manifest)
    app.router.add_get("/icon.svg", pwa_icon_svg)
    app.router.add_get("/sw.js", pwa_sw)

    async def index_handler(request):
        return web.FileResponse(os.path.join(STATIC_DIR, "index.html"))

        # Special Exam Routes & Anti-Cheat
    app.router.add_post("/api/code/validate-oop", api_validate_oop_structure)
    app.router.add_get("/api/exam/shuffle", api_exam_shuffle)
    app.router.add_post("/api/flashcards/sm2-review", api_sm2_review)
    app.router.add_get("/api/flashcards/due-today", api_sm2_due_today)
    app.router.add_post("/api/ai/validate-essay-steps", api_validate_essay_steps)
    app.router.add_post("/api/ai/rubber-duck", api_rubber_duck)

    # Alias routes: query-param style (used by frontend & tests)
    app.router.add_get("/api/exercises", get_exercises_by_query)
    app.router.add_get("/api/flashcards", get_flashcards_by_query)

    # Missing endpoints surfaced by test_server_endpoints.py
    app.router.add_get("/api/ai/key-status", api_ai_key_status)
    app.router.add_get("/api/network/qr-info", api_network_qr_info)
    app.router.add_get("/api/battle/leaderboard", api_battle_leaderboard)
    app.router.add_get("/api/stem/reference", api_stem_reference)
    app.router.add_get("/api/exam/ctump-parts", api_exam_ctump_parts)

    # Route URLs (/exam/practical, /exam/essay, etc.)
    app.router.add_get("/exam/practical", index_handler)
    app.router.add_get("/exam/essay", index_handler)
    app.router.add_get("/exam/survival", index_handler)
    app.router.add_get("/exam/cheatsheet", index_handler)

    app.router.add_get("/", index_handler)
    app.router.add_static("/static/", STATIC_DIR)
    app.on_cleanup.append(lambda _app: ai.close_http_session())
    if os.environ.get("TELEGRAM_BOT_TOKEN") and os.environ.get("TELEGRAM_BACKUP_CHAT_ID"):
        app.on_startup.append(lambda _app: _start_backup_task(_app))
        app.on_cleanup.append(lambda _app: _stop_backup_task(_app))

    return app


async def _start_backup_task(app):
    app["telegram_backup_task"] = asyncio.create_task(_telegram_backup_loop())

async def _stop_backup_task(app):
    task = app.pop("telegram_backup_task", None)
    if task:
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)

if __name__ == "__main__":
    app = create_app()
    lan_ip = get_lan_ip()
    print(f"🚀 UniMaster AI v10.0 running on PC: http://localhost:{PORT} | Mobile/iPad Wi-Fi: http://{lan_ip}:{PORT}")
    print(f"🔐 Bảo vệ truy cập: {'BẬT' if AUTH_ENABLED else 'TẮT (chế độ nội bộ)'} | 💾 Dữ liệu: {db.DB_PATH}")
    web.run_app(app, host="0.0.0.0", port=PORT)
