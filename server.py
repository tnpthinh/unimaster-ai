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
    "/manifest.json", "/icon.svg", "/sw.js", "/healthz",
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

    if not AUTH_ENABLED or request.path in AUTH_EXEMPT_PATHS or request.path.startswith("/static/"):
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
    pw = str(data.get("password") or data.get("code") or "").strip()

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


def _inject_playground_exercise(exercises, sid):
    """Them bai Playground ao (id=9999) vao danh sach bai tap.

    LUU Y: chi them cho 2 mon co ho tro chay code that su:
      - Mon 5  : Lap trinh huong doi tuong (C#)
      - Mon 22 : Nhap mon lap trinh (Python)
    Truoc day ham nay them Playground Python vao BAT KY mon nao khac 5
    (vi du mon 21, mon 50...), khien sinh vien thay bai "Playground" khong lien quan.
    """
    if sid not in (5, 22):
        return exercises

    has_play = any(e.get("id") == 9999 or "[TỰ DO]" in str(e.get("title", "")) for e in exercises)
    if not has_play:
        lang = "csharp" if sid == 5 else "python"
        sample = (
"""using System;
using System.Collections.Generic;
using System.Linq;

// 🚀 PLAYGROUND C# (.NET) - TỰ DO SÁNG TẠO & THỰC THI CODE
public class Program {
    public static void Main(string[] args) {
        Console.WriteLine("=== UniMaster C# Sandbox ===");
        string input = Console.ReadLine();
        string user = string.IsNullOrWhiteSpace(input) ? "Kỹ Sư Phần Mềm C#" : input.Trim();
        Console.WriteLine($"Xin chào, {user}! Môi trường C# .NET đang thực thi hoàn hảo.");
    }
}"""
            if sid == 5
            else
"""# 🚀 PLAYGROUND PYTHON 3 - TỰ DO SÁNG TẠO & XỬ LÝ DỮ LIỆU
import sys
import math
from collections import Counter

def main():
    print("=== UniMaster Python Sandbox ===")
    line = sys.stdin.readline().strip()
    user = line if line else "Python Developer"
    print(f"Xin chào, {user}! Môi trường Python 3 sẵn sàng thực thi.")

if __name__ == '__main__':
    main()
"""
        )
        play_ex = {
            "id": 9999,
            "subject_id": sid,
            "title": "🚀 [TỰ DO] Playground Lập Trình C# & Python (Code Tùy Thích)",
            "difficulty": "easy",
            "language": lang,
            "problem": "Không gian thực hành tự do không giới hạn: Bạn có thể viết bất kỳ thuật toán, bài toán thực tế, cấu trúc dữ liệu hoặc class OOP nào bằng C# (.NET) hoặc Python 3. Bạn có thể tự do nhập STDIN, bấm Chạy Thử, xem kết quả console, hoặc dùng AI để tự động sửa lỗi và nâng cấp code theo chuẩn kiến trúc.",
            "specs": [
                "Tự do chọn ngôn ngữ: C# (.NET) hoặc Python 3 (Native).",
                "Tự do nhập dữ liệu đầu vào (STDIN) bất kỳ trong tab Console.",
                "Sử dụng nút 'AI Sửa Lỗi & Nâng Cấp' để AI chẩn đoán lỗi, giải thích bài học và refactor tối ưu."
            ],
            "starter_code": sample,
            "sample_code": sample,
            "solution_code": sample,
            "test_cases": [
                {"input": "UniMaster", "expected_output": f"=== UniMaster {'C# Sandbox' if sid == 5 else 'Python Sandbox'} ===\nXin chào, UniMaster! {'Môi trường C# .NET đang thực thi hoàn hảo.' if sid == 5 else 'Môi trường Python 3 sẵn sàng thực thi.'}", "is_hidden": False}
            ]
        }
        return [play_ex] + list(exercises)
    return exercises


async def get_exercises(request):
    try:
        sid = int(request.match_info["id"])
        exercises = db.get_exercises_by_subject(sid)
        exercises = _inject_playground_exercise(exercises, sid)
        return json_resp({"success": True, "exercises": exercises})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


async def get_exercises_by_query(request):
    """Alias: /api/exercises?subject_id=N (query-param style used by frontend/tests)."""
    try:
        sid = int(request.rel_url.query.get("subject_id", 0))
        exercises = db.get_exercises_by_subject(sid)
        exercises = _inject_playground_exercise(exercises, sid)
        return json_resp({"success": True, "exercises": exercises})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


async def get_exercise_detail(request):
    """GET /api/exercises/{id} — trả chi tiết 1 bài tập (hỗ trợ cả Playground 9999)."""
    try:
        ex_id = int(request.match_info["id"])
        raw_sid = request.rel_url.query.get("subject_id")
        sid = int(raw_sid) if raw_sid and str(raw_sid).isdigit() else 5
        if ex_id == 9999:
            injected = _inject_playground_exercise([], sid if sid in (5, 22) else 5)
            if injected:
                return json_resp({"success": True, "exercise": injected[0]})
        ex = db.get_exercise_by_id(ex_id)
        if ex:
            return json_resp({"success": True, "exercise": ex})
        return json_resp({"success": False, "error": f"Không tìm thấy bài tập #{ex_id}"}, 404)
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
    """GET /api/battle/leaderboard — bảng xếp hạng đấu trường từ lịch sử thi & người dùng."""
    try:
        conn = db.get_connection()
        rows = conn.execute(
            """
            SELECT u.username, u.full_name, u.avatar_emoji,
                   COUNT(e.id) AS exams_count,
                   ROUND(AVG(e.score), 2) AS avg_score,
                   SUM(e.correct_count) AS total_correct
            FROM users u
            LEFT JOIN exam_history e ON e.user_id = u.id
            GROUP BY u.id
            ORDER BY total_correct DESC, avg_score DESC
            LIMIT 20
            """
        ).fetchall()
        conn.close()
        leaderboard = [
            {
                "rank": idx + 1,
                "username": r["username"],
                "name": r["full_name"] or r["username"],
                "avatar": r["avatar_emoji"] or "🎓",
                "exams_count": int(r["exams_count"] or 0),
                "avg_score": float(r["avg_score"] or 0.0),
                "score": int(r["total_correct"] or 0) * 100,
            }
            for idx, r in enumerate(rows)
        ]
        return json_resp({"success": True, "leaderboard": leaderboard})
    except Exception:
        return json_resp({"success": True, "leaderboard": []})


async def api_stem_reference(request):
    """GET /api/stem/reference — bảng giá trị tham chiếu Y khoa & STEM chuẩn."""
    items = [
        {"category": "Hóa sinh máu", "name": "Glucose máu lúc đói", "normal_range": "3.9 – 5.6 mmol/L (70 – 100 mg/dL)", "clinical_note": "≥ 7.0 mmol/L (126 mg/dL) gợi ý Đái tháo đường"},
        {"category": "Hóa sinh máu", "name": "HbA1c", "normal_range": "4.0 – 5.6 %", "clinical_note": "≥ 6.5% chẩn đoán Đái tháo đường; 5.7 – 6.4% tiền ĐTĐ"},
        {"category": "Chức năng thận", "name": "Creatinin huyết thanh", "normal_range": "Nam: 62 – 115 µmol/L | Nữ: 53 – 97 µmol/L", "clinical_note": "Tăng trong suy thận cấp/mạn; dùng tính eGFR / CrCl"},
        {"category": "Chức năng thận", "name": "Ure huyết (BUN)", "normal_range": "2.5 – 7.5 mmol/L", "clinical_note": "Tăng trước thận (mất nước, XHTH), tại thận, sau thận"},
        {"category": "Chức năng thận", "name": "Acid Uric máu", "normal_range": "Nam: 210 – 420 µmol/L | Nữ: 150 – 350 µmol/L", "clinical_note": "Tăng trong bệnh Gout, suy thận, hội chứng ly giải u"},
        {"category": "Gan mật", "name": "AST (GOT) & ALT (GPT)", "normal_range": "< 35 – 40 U/L (ở 37°C)", "clinical_note": "Tăng cao trong hoại tử tế bào gan cấp; De Ritis (AST/ALT) > 2 gợi ý viêm gan rượu"},
        {"category": "Gan mật", "name": "Bilirubin toàn phần", "normal_range": "3.4 – 17.1 µmol/L (0.2 – 1.0 mg/dL)", "clinical_note": "> 34 µmol/L (2 mg/dL) biểu hiện vàng da trên lâm sàng"},
        {"category": "Mỡ máu (Lipid)", "name": "Cholesterol toàn phần", "normal_range": "< 5.2 mmol/L (< 200 mg/dL)", "clinical_note": "Công thức Friedewald: LDL-C = TC - HDL-C - (TG / 2.2) mmol/L (khi TG < 4.5 mmol/L)"},
        {"category": "Lập trình C# OOP", "name": "4 Tính chất OOP", "normal_range": "Đóng gói, Kế thừa, Đa hình, Trừu tượng", "clinical_note": "virtual/override dùng cho đa hình động (Runtime Polymorphism)"},
        {"category": "Lập trình Python", "name": "Độ phức tạp cấu trúc dữ liệu", "normal_range": "dict/set lookup: O(1) | list sort: O(n log n)", "clinical_note": "Sử dụng list comprehension và generator để tối ưu bộ nhớ"}
    ]
    return json_resp({"success": True, "references": items, "items": items})


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
    const CACHE_NAME = 'unimaster-pwa-v40';
    const CORE_ASSETS = [
      '/static/style.css?v=40.0',
      '/static/minimal.css?v=3.0',
      '/static/app.js?v=40.0',
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
      const url = new URL(e.request.url);
      if (url.pathname.startsWith('/api/') || url.pathname.startsWith('/ws/') || url.pathname === '/login' || url.pathname === '/logout') {
        return;
      }
      e.respondWith(
        fetch(e.request)
          .then((resp) => {
            if (resp && resp.status === 200 && !resp.redirected && url.pathname.startsWith('/static/')) {
              const clone = resp.clone();
              caches.open(CACHE_NAME).then((c) => c.put(e.request, clone)).catch(() => {});
            }
            return resp;
          })
          .catch(() => caches.match(e.request))
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
        inp = data.get("input_data")
        if inp is None:
            inp = data.get("input", data.get("stdin", ""))
        res = await code_engine.execute_code(lang, code, str(inp or ""))
        return json_resp(res)
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)

async def api_code_test(request):
    try:
        data = await safe_get_json(request)
        ex_id = int(data.get("exercise_id", 0))
        lang = data.get("language", "cpp")
        code = data.get("code", "")
        raw_sid = data.get("subject_id")
        try:
            sid = int(raw_sid) if raw_sid is not None else None
        except (TypeError, ValueError):
            sid = None
        res = await code_engine.test_code_against_cases(ex_id, lang, code, subject_id=sid)
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

async def api_code_fix_and_upgrade(request):
    try:
        data = await safe_get_json(request)
        code = data.get("code", "")
        lang = data.get("language", "csharp")
        # Frontend gui "problem_title" (khong phai "title") -> phai doc ca 2 key.
        title = data.get("problem_title") or data.get("title", "")
        # Frontend gui "current_error" -> truoc day server chi doc "error",
        # nen AI KHONG BAO GIO nhan duoc loi compile/test can sua.
        error = data.get("current_error") or data.get("error", "")
        res = await code_engine.fix_and_upgrade_code(code, lang, problem_title=title, current_error=error)
        return json_resp(res)
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)


async def api_code_suggest(request):
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
        raw_line_num = data.get("line_number")
        raw_line = data.get("line")
        line = 1
        if raw_line_num is not None and str(raw_line_num).strip().lstrip("-").isdigit():
            line = max(1, int(str(raw_line_num).strip()))
            if isinstance(raw_line, str) and not raw_line.strip().isdigit() and not code.strip():
                code = raw_line
        elif raw_line is not None and str(raw_line).strip().lstrip("-").isdigit():
            line = max(1, int(str(raw_line).strip()))
        elif isinstance(raw_line, str) and raw_line.strip() and not code.strip():
            code = raw_line
            line = 1
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
        return json_resp({"ok": False, "success": False, "error": str(e)}, 500)

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


# ------------------------------------------------------------------------------
# UNIMASTER AI v41.0 — VIVA VOCE, FEYNMAN STUDIO, MINDMAP & UML/MEMORY ANALYZER
# ------------------------------------------------------------------------------

VIVA_QUESTION_BANK = {
    "biochem": [
        {
            "id": "viva_bio_1",
            "topic": "Chu trình Krebs & Chuỗi hô hấp tế bào",
            "question": "Tại sao chu trình Krebs được gọi là con đường chuyển hóa lưỡng dụng (amphibolic pathway)? Nếu thiếu hụt vitamin B1 (Thiamin), những enzyme nào bị đình trệ và hậu quả lâm sàng là gì?",
            "keywords": ["dị hóa", "đồng hóa", "pyruvate dehydrogenase", "alpha-ketoglutarate dehydrogenase", "TPP", "nhiễm toan lactic", "ATP"],
            "model_answer": "Chu trình Krebs là con đường lưỡng dụng vì vừa đóng vai trò DỊ HÓA (oxy hóa Acetyl-CoA tạo NADH, FADH2, GTP để sinh năng lượng) vừa đóng vai trò ĐỒNG HÓA (cung cấp các chất trung gian như Citrate tổng hợp acid béo, alpha-Ketoglutarate và Oxaloacetate tổng hợp acid amin, Succinyl-CoA tổng hợp Heme). Khi thiếu Vitamin B1 (tiền chất của coenzyme TPP - Thiamin pyrophosphate), hai phức hợp enzyme khử carboxyl oxy hóa là Pyruvate dehydrogenase và alpha-Ketoglutarate dehydrogenase bị ức chế, dẫn đến ứ đọng Pyruvate chuyển thành Lactate gây nhiễm toan lactic và thiếu hụt ATP nghiêm trọng ở mô thần kinh, cơ tim (bệnh Beri-beri).",
            "follow_up": "Nếu tế bào lấy quá nhiều Oxaloacetate ra khỏi chu trình Krebs để tân tạo đường (Gluconeogenesis), phản ứng bù (anaplerotic reaction) quan trọng nhất để nạp lại Oxaloacetate là phản ứng nào và do enzyme gì xúc tác?"
        },
        {
            "id": "viva_bio_2",
            "topic": "Động học Enzyme & Chất ức chế",
            "question": "Hãy phân biệt cơ chế của chất ức chế cạnh tranh (Competitive) và ức chế không cạnh tranh (Non-competitive) dựa trên giá trị Km, Vmax và đồ thị nghịch đảo kép Lineweaver-Burk.",
            "keywords": ["Km", "Vmax", "trung tâm hoạt động", "dị lập thể", "Lineweaver-Burk", "tăng Km", "giảm Vmax"],
            "model_answer": "1) Ức chế cạnh tranh: Chất ức chế có cấu trúc giống cơ chất, gắn thuận nghịch vào trung tâm hoạt động của enzyme tự do (E). Khi tăng nồng độ cơ chất [S] thật cao có thể đẩy chất ức chế ra, nên Vmax KHÔNG ĐỔI nhưng Km biểu kiến TĂNG (giảm ái lực). Trên đồ thị Lineweaver-Burk, các đường thẳng cắt nhau trên trục tung (1/Vmax). 2) Ức chế không cạnh tranh: Chất ức chế gắn vào vị trí dị lập thể trên cả E và phức hợp ES, làm bất hoạt xúc tác mà không cản cơ chất gắn vào, do đó Km KHÔNG ĐỔI nhưng Vmax biểu kiến GIẢM. Trên đồ thị Lineweaver-Burk, các đường thẳng cắt nhau trên trục hoành (-1/Km).",
            "follow_up": "Ứng dụng lâm sàng: Khi bệnh nhân ngộ độc Methanol, tại sao truyền Ethanol tĩnh mạch lại cứu sống được bệnh nhân khỏi mù lòa và toan chuyển hóa?"
        },
        {
            "id": "viva_bio_3",
            "topic": "Chuyển hóa Bilirubin & Vàng da",
            "question": "Trên lâm sàng, làm thế nào để phân biệt vàng da trước gan (tan máu), vàng da tại gan và vàng da sau gan (tắc mật) dựa vào Bilirubin tự do, Bilirubin liên hợp, Urobilinogen nước tiểu và Stercobilin phân?",
            "keywords": ["tự do", "gián tiếp", "liên hợp", "trực tiếp", "UDP-glucuronyl transferase", "urobilinogen", "phân bạc màu"],
            "model_answer": "- Trước gan (Tan máu): Tăng mạnh Bilirubin tự do (gián tiếp) trong máu (không qua được cầu thận nên nước tiểu không có bilirubin), tăng Urobilinogen nước tiểu và tăng Stercobilin làm phân sẫm màu.\n- Tại gan (Viêm gan): Tăng cả Bilirubin tự do (do giảm bắt giữ/liên hợp) và Bilirubin liên hợp (do tổn thương tiểu quản mật tràn vào máu), nước tiểu sậm màu (có Bilirubin liên hợp).\n- Sau gan (Tắc mật hoàn toàn): Tăng cao Bilirubin liên hợp (trực tiếp) tràn vào máu và ra nước tiểu (nước tiểu vàng sậm như nước trà đặc), nhưng mật không xuống ruột được nên Urobilinogen âm tính và phân bạc màu như đất sét.",
            "follow_up": "Tại sao trẻ sơ sinh thiếu tháng rất dễ bị vàng da nhân não (Kernicterus) và liệu pháp chiếu đèn xanh hoạt động theo cơ chế hóa sinh nào?"
        }
    ],
    "csharp_oop": [
        {
            "id": "viva_cs_1",
            "topic": "4 Trụ cột OOP & Đa hình (Polymorphism) trong C#",
            "question": "Sự khác biệt bản chất giữa cơ chế nạp chồng (Method Overloading) và ghi đè (Method Overriding - từ khóa virtual/override) trong C# là gì? Khi nào trình biên dịch quyết định hàm được gọi ở Compile-time và khi nào ở Runtime (V-Table)?",
            "keywords": ["Overloading", "Overriding", "virtual", "override", "Compile-time", "Runtime", "V-Table", "new"],
            "model_answer": "- Overloading (Đa hình tĩnh / Compile-time): Các phương thức cùng tên trong cùng một lớp nhưng khác danh sách tham số (số lượng hoặc kiểu dữ liệu). Trình biên dịch xác định chính xác hàm nào được gọi ngay lúc biên dịch.\n- Overriding (Đa hình động / Runtime): Lớp cha khai báo phương thức với `virtual` hoặc `abstract`, lớp con định nghĩa lại với `override`. Khi gọi qua biến tham chiếu kiểu lớp cha trỏ tới đối tượng lớp con (`HinhHoc h = new HinhTron()`), CLR tra bảng phương thức ảo (Virtual Method Table - V-Table) tại thời điểm chạy (Runtime) để gọi đúng hàm của `HinhTron`.",
            "follow_up": "Nếu ở lớp con ta dùng từ khóa `new` thay vì `override` (Method Hiding), điều gì xảy ra khi gọi phương thức thông qua biến tham chiếu kiểu lớp cha?"
        },
        {
            "id": "viva_cs_2",
            "topic": "Abstract Class vs Interface trong .NET",
            "question": "Trong thiết kế hướng đối tượng C#, khi nào bạn chọn `abstract class` và khi nào chọn `interface`? Một lớp trong C# có thể kế thừa nhiều `abstract class` cùng lúc không và tại sao?",
            "keywords": ["abstract class", "interface", "IS-A", "CAN-DO", "đa kế thừa", "Diamond Problem", "constructor", "field"],
            "model_answer": "- `abstract class` thể hiện quan hệ bản chất 'IS-A' (là một), có thể chứa thuộc tính dữ liệu (fields), hàm khởi tạo (constructor), access modifiers và code dùng chung. C# chỉ cho phép ĐƠN KẾ THỪA lớp (`class`) để tránh bài toán Kim cương (Diamond Problem).\n- `interface` thể hiện bản hợp đồng hành vi 'CAN-DO' (có khả năng làm gì), một lớp có thể thực thi ĐA INTERFACE cùng lúc (VD: `class SinhVien : Nguoi, IComparable, IDisposable`), giúp tách biệt giao diện khỏi cài đặt (Loose Coupling & Dependency Injection).",
            "follow_up": "Nếu một lớp thực thi 2 interface có cùng chữ ký phương thức `void Draw()`, làm thế nào để cài đặt tách biệt hành vi cho từng interface trong C#?"
        },
        {
            "id": "viva_cs_3",
            "topic": "Quản lý bộ nhớ Stack vs Heap & Garbage Collector",
            "question": "Hãy giải thích sự khác biệt giữa Value Type (`struct`, `int`, `double`) và Reference Type (`class`, `string`, `List<T>`) trên bộ nhớ Stack và Managed Heap. Hiện tượng Boxing và Unboxing gây ảnh hưởng hiệu năng như thế nào?",
            "keywords": ["Stack", "Heap", "Value Type", "Reference Type", "Boxing", "Unboxing", "Garbage Collector", "con trỏ"],
            "model_answer": "- Value Type lưu trực tiếp giá trị tại chỗ (thường trên Stack Frame nếu là biến cục bộ), khi gán biến sẽ sao chép toàn bộ giá trị độc lập.\n- Reference Type lưu đối tượng thực sự trên Managed Heap (do Garbage Collector quản lý), còn biến trên Stack chỉ giữ địa chỉ tham chiếu (con trỏ) trỏ tới vùng nhớ Heap.\n- Boxing là quá trình đóng gói một Value Type trên Stack thành một đối tượng `object` cấp phát mới trên Heap (tốn thời gian cấp phát + tăng tải cho GC). Unboxing là ép kiểu ngược từ `object` trên Heap về Value Type trên Stack.",
            "follow_up": "Tại sao kiểu `string` trong C# là Reference Type nhưng lại mang tính bất biến (Immutable), và tại sao nối chuỗi trong vòng lặp lớn nên dùng `StringBuilder`?"
        }
    ],
    "discrete_math": [
        {
            "id": "viva_dm_1",
            "topic": "Thuật toán tìm đường đi ngắn nhất Dijkstra & Bellman-Ford",
            "question": "Tại sao thuật toán Dijkstra (sử dụng chiến lược Tham lam - Greedy) lại chạy sai khi đồ thị có cạnh trọng số âm, và thuật toán nào giải quyết được bài toán này?",
            "keywords": ["Dijkstra", "trọng số âm", "Greedy", "Bellman-Ford", "chu trình âm", "độ phức tạp"],
            "model_answer": "Thuật toán Dijkstra giả định rằng một khi đỉnh u có khoảng cách d[u] nhỏ nhất được lấy ra khỏi hàng đợi ưu tiên và đánh dấu cố định (visited), sẽ không thể có đường đi nào khác qua các đỉnh chưa xét làm giảm d[u] thêm nữa (vì mọi cạnh đều >= 0). Khi có cạnh trọng số âm, một đường đi dài hơn ở bước sau đi qua cạnh âm có thể làm tổng trọng số nhỏ hơn cả đỉnh đã chốt, khiến giả định tham lam bị phá vỡ. Để xử lý cạnh âm (và phát hiện chu trình âm), ta dùng thuật toán Bellman-Ford với độ phức tạp O(V * E).",
            "follow_up": "Trong đồ thị không có trọng số (hoặc mọi cạnh đều bằng 1), thuật toán nào tìm đường đi ngắn nhất tối ưu hơn cả Dijkstra và có độ phức tạp bao nhiêu?"
        },
        {
            "id": "viva_dm_2",
            "topic": "Đồ thị Euler, Đồ thị Hamilton & Cây khung nhỏ nhất",
            "question": "Phân biệt điều kiện cần và đủ để một đa đồ thị vô hướng liên thông có Chu trình Euler và Đường đi Euler. Tại sao bài toán kiểm tra Chu trình Euler thuộc lớp P còn Chu trình Hamilton thuộc lớp NP-Complete?",
            "keywords": ["bậc chẵn", "bậc lẻ", "Euler", "Hamilton", "NP-Complete", "Hierholzer", "Kruskal", "Prim"],
            "model_answer": "Theo định lý Euler: Đồ thị vô hướng liên thông có Chu trình Euler khi và chỉ khi MỌI ĐỈNH đều có bậc chẵn; có Đường đi Euler (không khép kín) khi và chỉ khi có ĐÚNG 2 ĐỈNH bậc lẻ. Vì chỉ cần đếm bậc của các đỉnh trong thời gian tuyến tính O(V + E), bài toán Euler thuộc lớp P. Ngược lại, Chu trình Hamilton yêu cầu đi qua mỗi ĐỈNH đúng một lần, không có điều kiện cục bộ đơn giản theo bậc đỉnh mà phải duyệt không gian trạng thái tổ hợp, nên thuộc lớp NP-Complete.",
            "follow_up": "So sánh thuật toán Prim và Kruskal khi tìm Cây khung nhỏ nhất (Minimum Spanning Tree): Khi nào nên chọn Prim và khi nào nên chọn Kruskal?"
        }
    ],
    "python": [
        {
            "id": "viva_py_1",
            "topic": "Cấu trúc dữ liệu & Độ phức tạp Big-O trong Python",
            "question": "Tại sao thao tác kiểm tra phần tử `x in my_collection` trên `set` hoặc `dict` trong Python có độ phức tạp trung bình O(1), trong khi trên `list` lại là O(n)? Điều kiện để một đối tượng làm được khóa (key) của `dict` là gì?",
            "keywords": ["Hash Table", "O(1)", "O(n)", "hashable", "immutable", "__hash__", "__eq__", "tuple", "list"],
            "model_answer": "`set` và `dict` trong Python được cài đặt bên dưới bằng Bảng băm (Hash Table). Khi tìm `x`, Python tính hàm băm `hash(x)` để nhảy trực tiếp tới ô nhớ (bucket) trong thời gian O(1), còn `list` là mảng động phải duyệt tuần tự từng phần tử từ đầu đến cuối mất O(n). Để làm key trong `dict` hoặc phần tử trong `set`, đối tượng phải là Hashable (bất biến - Immutable, cài đặt `__hash__()` và `__eq__()`), ví dụ `int`, `str`, `tuple` (chứa các phần tử bất biến), còn `list` hay `dict` là Mutable nên không thể làm key.",
            "follow_up": "Sự khác biệt giữa tham chiếu nông `copy.copy()` (Shallow Copy) và sao chép sâu `copy.deepcopy()` (Deep Copy) với danh sách lồng nhau `[[1, 2], [3, 4]]` là gì?"
        }
    ]
}


async def api_viva_simulator_handler(request):
    try:
        data = await request.json()
    except Exception:
        data = {}

    action = data.get("action", "start")
    domain = data.get("domain", "biochem")
    persona = data.get("persona", "strict_prof")
    difficulty = data.get("difficulty", "medium")
    question_id = data.get("question_id", "")

    bank = VIVA_QUESTION_BANK.get(domain, VIVA_QUESTION_BANK["biochem"])

    if action in ("start", "next_question"):
        import random
        candidates = [q for q in bank if q["id"] != question_id] or bank
        chosen = random.choice(candidates)
        persona_intro = {
            "strict_prof": "👨‍🏫 [Giáo sư Hội đồng]: Trình bày ngắn gọn, đi thẳng vào bản chất cơ chế và thuật ngữ chuẩn!",
            "socratic_mentor": "🧙‍♂️ [Giảng viên Socratic]: Hãy suy luận từng bước từ nguyên lý gốc nhé, thầy sẽ gợi mở cùng em.",
            "tech_lead": "💻 [Tech Lead / Bác sĩ Nội trú]: Tập trung vào hiệu năng thực tế, xử lý tình huống và các góc khuất (edge cases)!"
        }.get(persona, "👨‍🏫 [Giám khảo AI]: Hãy trả lời câu hỏi vấn đáp dưới đây:")

        return web.json_response({
            "ok": True,
            "question_id": chosen["id"],
            "topic": chosen["topic"],
            "question": chosen["question"],
            "persona_intro": persona_intro,
            "keywords_hint_count": len(chosen["keywords"]),
            "difficulty": difficulty
        })

    user_answer = (data.get("answer") or "").strip()
    question_text = (data.get("question") or "").strip()
    matched_item = next((q for q in bank if q["id"] == question_id or q["question"] == question_text), bank[0])

    if not user_answer:
        return web.json_response({"ok": False, "error": "Vui lòng nhập hoặc nói câu trả lời của bạn trước khi nộp chấm!"}, status=400)

    ans_lower = user_answer.lower()
    keywords = matched_item.get("keywords", [])
    hit_keywords = [kw for kw in keywords if kw.lower() in ans_lower]
    missing_keywords = [kw for kw in keywords if kw.lower() not in ans_lower]

    kw_ratio = len(hit_keywords) / max(1, len(keywords))
    word_count = len(user_answer.split())
    length_factor = min(1.0, word_count / 35.0)

    accuracy_score = min(100, int(round((kw_ratio * 0.75 + length_factor * 0.25) * 100)))
    depth_score = min(100, int(round((length_factor * 0.6 + kw_ratio * 0.4) * 100)))
    terminology_score = min(100, int(round(kw_ratio * 100)))
    clarity_score = min(100, max(55, int(round((0.5 + length_factor * 0.5) * 95))))
    total_score = int(round(accuracy_score * 0.35 + depth_score * 0.25 + terminology_score * 0.25 + clarity_score * 0.15))

    grade_rank = "Xuất sắc (A+)" if total_score >= 85 else ("Khá Giỏi (B+)" if total_score >= 70 else ("Đạt yêu cầu (C)" if total_score >= 50 else "Cần củng cố gấp (D)"))

    feedback = (
        f"Bạn đã nêu trúng {len(hit_keywords)}/{len(keywords)} từ khóa cốt lõi ({', '.join(hit_keywords) if hit_keywords else 'chưa dùng đúng thuật ngữ chuyên ngành'}). "
        f"Độ dài lập luận: {word_count} từ."
    )
    if missing_keywords:
        feedback += f" Để đạt điểm tối đa 10/10 trước hội đồng, bạn cần bổ sung phân tích về: {', '.join(missing_keywords)}."

    try:
        if ai.has_active_key():
            prompt = (
                f"Đóng vai giám khảo thi vấn đáp đại học ({persona}).\n"
                f"Câu hỏi: {question_text}\n"
                f"Câu trả lời của sinh viên: {user_answer}\n"
                f"Đáp án chuẩn tham khảo: {matched_item.get('model_answer', '')}\n"
                f"Hãy nhận xét ngắn gọn, sắc bén (3-4 câu tiếng Việt) về ưu điểm và điểm cần sửa trong câu trả lời của sinh viên."
            )
            ai_comment = await asyncio.wait_for(ai._call_gemini_text(prompt, temperature=0.3), timeout=8.0)
            if ai_comment and len(ai_comment.strip()) > 20:
                feedback = ai_comment.strip()
    except Exception:
        pass

    return web.json_response({
        "ok": True,
        "total_score": total_score,
        "grade_rank": grade_rank,
        "rubric": {
            "accuracy": accuracy_score,
            "depth": depth_score,
            "terminology": terminology_score,
            "clarity": clarity_score
        },
        "hit_keywords": hit_keywords,
        "missing_keywords": missing_keywords,
        "feedback": feedback,
        "model_answer": matched_item.get("model_answer", ""),
        "follow_up_question": matched_item.get("follow_up", "")
    })


async def api_feynman_evaluate_handler(request):
    try:
        data = await request.json()
    except Exception:
        data = {}

    concept = (data.get("concept") or "").strip()
    explanation = (data.get("explanation") or "").strip()
    subject = (data.get("subject") or "Tổng hợp").strip()

    if not concept or not explanation:
        return web.json_response({"ok": False, "error": "Vui lòng nhập tên khái niệm và lời giải thích của bạn!"}, status=400)

    words = explanation.split()
    word_count = len(words)
    has_analogy = any(w in explanation.lower() for w in ["giống như", "tưởng tượng", "ví dụ", "như là", "ví như", "analogy", "nhà máy", "chìa khóa", "ổ khóa", "bản thiết kế"])
    has_structure = any(w in explanation.lower() for w in ["bởi vì", "do đó", "kết quả là", "bước 1", "đầu tiên", "tiếp theo", "tóm lại"])

    simplicity_score = min(100, max(45, 65 + (20 if has_analogy else 0) + (15 if 20 <= word_count <= 180 else 5)))
    accuracy_score = min(100, max(50, 60 + min(30, word_count // 3) + (10 if has_structure else 0)))
    clarity_score = int(round(simplicity_score * 0.55 + accuracy_score * 0.45))

    gaps = []
    if not has_analogy:
        gaps.append("Chưa sử dụng hình ảnh ẩn dụ đời thường (Analogy) — trái tim của phương pháp Feynman để người mới nghe hiểu ngay.")
    if word_count < 25:
        gaps.append("Lời giải thích còn quá ngắn, chưa làm rõ mối quan hệ Nhân - Quả (Tại sao cơ chế này diễn ra?).")
    if not has_structure:
        gaps.append("Nên chia luồng giải thích theo trình tự: Định nghĩa cực ngắn -> Ẩn dụ đời sống -> Ví dụ thực tế.")
    if not gaps:
        gaps.append("Cách diễn đạt rất mạch lạc! Hãy thử thách bản thân bằng cách giải thích thêm các trường hợp ngoại lệ (Edge Cases).")

    feynman_rewrite = (
        f"💡 [Bản chuẩn Feynman cho '{concept}']: Hãy tưởng tượng '{concept}' giống như một quy trình điều phối thông minh trong đời sống. "
        f"Thay vì học thuộc lòng định nghĩa khô khan, bản chất của nó gồm 3 ý: (1) Nó giải quyết bài toán gì? "
        f"(2) Cơ chế cốt lõi hoạt động ra sao khi có tác nhân kích thích? và (3) Nếu thành phần này bị lỗi/thiếu hụt thì hệ thống sẽ sụp đổ ở khâu nào?"
    )
    child_question = f"Nếu em là một học sinh 12 tuổi và hỏi: 'Tại sao ta không thể bỏ qua {concept} mà lại bắt buộc phải dùng nó?', bạn sẽ trả lời thế nào trong 2 câu?"

    try:
        if ai.has_active_key():
            prompt = (
                f"Sinh viên đang luyện phương pháp Feynman cho khái niệm: '{concept}' (Môn: {subject}).\n"
                f"Lời giải thích của sinh viên: '{explanation}'\n"
                f"Hãy viết lại 1 đoạn giải thích chuẩn Feynman cực kỳ dễ hiểu kèm hình ảnh ẩn dụ thú vị (tối đa 4 câu tiếng Việt)."
            )
            ai_rewrite = await asyncio.wait_for(ai._call_gemini_text(prompt, temperature=0.4), timeout=8.0)
            if ai_rewrite and len(ai_rewrite.strip()) > 25:
                feynman_rewrite = ai_rewrite.strip()
    except Exception:
        pass

    return web.json_response({
        "ok": True,
        "concept": concept,
        "clarity_score": clarity_score,
        "simplicity_score": simplicity_score,
        "accuracy_score": accuracy_score,
        "has_analogy": has_analogy,
        "word_count": word_count,
        "knowledge_gaps": gaps,
        "feynman_rewrite": feynman_rewrite,
        "child_question": child_question
    })


MINDMAP_PRESETS = {
    "krebs": {
        "root": "Chu trình Krebs & Hô hấp Tế bào",
        "subtitle": "Trung tâm chuyển hóa năng lượng tại Chất nền Ty thể (Mitochondrial Matrix)",
        "branches": [
            {
                "id": "b1",
                "title": "1. Khởi phát: Pyruvate -> Acetyl-CoA",
                "color": "#ec4899",
                "summary": "Xúc tác bởi phức hợp Pyruvate Dehydrogenase (PDH) cần 5 coenzyme: TPP (B1), FAD (B2), NAD+ (B3), CoA-SH (B5), Acid Lipoic.",
                "formula": "Pyruvate + NAD+ + CoA-SH -> Acetyl-CoA + NADH + CO2",
                "exam_trap": "Bẫy thi: Phản ứng PDH là bước cầu nối, KHÔNG nằm trong 8 phản ứng chính thức của chu trình Krebs nhưng quyết định đầu vào!",
                "subnodes": ["5 Coenzyme (B1, B2, B3, B5, Lipoic)", "Ức chế bởi Acetyl-CoA & NADH cao", "Sinh 1 NADH (2.5 ATP)"]
            },
            {
                "id": "b2",
                "title": "2. 3 Điểm Điều Hòa Không Thuận Nghịch",
                "color": "#8b5cf6",
                "summary": "3 enzyme điều hòa tốc độ chu trình Krebs: Citrate Synthase, Isocitrate Dehydrogenase (quan trọng nhất), và alpha-Ketoglutarate Dehydrogenase.",
                "formula": "Isocitrate + NAD+ -> alpha-Ketoglutarate + CO2 + NADH",
                "exam_trap": "Bẫy thi: ADP và Ca2+ KÍCH THÍCH mạnh Isocitrate dehydrogenase; còn ATP và NADH ỨC CHẾ nó.",
                "subnodes": ["Citrate Synthase (Mở đầu)", "Isocitrate Dehydrogenase (Rate-limiting)", "a-KG Dehydrogenase (Cần B1)"]
            },
            {
                "id": "b3",
                "title": "3. Bảng Cân Bằng Năng Lượng (1 vòng)",
                "color": "#10b981",
                "summary": "Mỗi phân tử Acetyl-CoA đi qua 1 vòng Krebs tạo ra: 3 NADH, 1 FADH2, 1 GTP (ATP) và giải phóng 2 phân tử CO2.",
                "formula": "3 NADH (7.5 ATP) + 1 FADH2 (1.5 ATP) + 1 GTP (1 ATP) = 10 ATP",
                "exam_trap": "Bẫy thi: Quy ước mới tính 1 NADH = 2.5 ATP (cũ là 3), 1 FADH2 = 1.5 ATP (cũ là 2) -> Tổng 10 ATP (hoặc 12 ATP theo quy ước cũ).",
                "subnodes": ["3 NADH tại bước 3, 4, 8", "1 FADH2 tại Succinate DH (Phức hợp II)", "1 GTP tại Succinyl-CoA Synthetase"]
            },
            {
                "id": "b4",
                "title": "4. Vai Trò Lưỡng Dụng (Amphibolic)",
                "color": "#f59e0b",
                "summary": "Cung cấp tiền chất cho tổng hợp Lipid, Acid amin, Porphyrin (Heme) và Tân tạo đường.",
                "formula": "Pyruvate + CO2 + ATP -> Oxaloacetate + ADP + Pi (Pyruvate Carboxylase)",
                "exam_trap": "Bẫy thi: Succinate Dehydrogenase là enzyme DUY NHẤT của chu trình Krebs gắn trên màng trong ty thể!",
                "subnodes": ["Citrate -> Tổng hợp Acid béo", "Succinyl-CoA + Glycine -> Heme", "Oxaloacetate -> Tân tạo Glucose"]
            }
        ]
    },
    "csharp_oop": {
        "root": "4 Trụ Cột OOP & Kiến Trúc C# (.NET)",
        "subtitle": "Nền tảng thiết kế Hướng đối tượng & Quản lý bộ nhớ CLR",
        "branches": [
            {
                "id": "c1",
                "title": "1. Đóng Gói (Encapsulation)",
                "color": "#06b6d4",
                "summary": "Che giấu dữ liệu nội bộ (`private` fields) và kiểm soát truy cập thông qua Properties (`get`/`set`).",
                "formula": "public int Tuoi { get => _tuoi; set => _tuoi = value >= 0 ? value : 0; }",
                "exam_trap": "Bẫy thi: `protected` cho phép lớp con truy cập kể cả khác assembly, còn `internal` chỉ trong cùng một project/assembly.",
                "subnodes": ["Access Modifiers (private/protected/public)", "Auto-Implemented Properties", "Data Validation trong Setter"]
            },
            {
                "id": "c2",
                "title": "2. Kế Thừa (Inheritance)",
                "color": "#8b5cf6",
                "summary": "Tái sử dụng mã nguồn từ lớp cha (`base`), gọi constructor lớp cha bằng `: base(...)`.",
                "formula": "public class BacSi : NhanVienYTe { public BacSi(string ten) : base(ten) {} }",
                "exam_trap": "Bẫy thi: Constructor lớp cha LUÔN chạy trước Constructor lớp con! Từ khóa `sealed` ngăn không cho kế thừa tiếp.",
                "subnodes": ["Đơn kế thừa Class (: BaseClass)", "Từ khóa base() & this()", "Sealed Class chống kế thừa"]
            },
            {
                "id": "c3",
                "title": "3. Đa Hình (Polymorphism)",
                "color": "#ec4899",
                "summary": "Cùng một lời gọi phương thức nhưng hành vi khác nhau tùy thuộc vào kiểu đối tượng thực tế lúc chạy (Runtime V-Table).",
                "formula": "virtual (Lớp cha) ---> override (Lớp con) vs new (Che khuất hàm)",
                "exam_trap": "Bẫy thi: Nếu lớp con dùng `new` thay vì `override`, biến tham chiếu kiểu lớp cha sẽ gọi hàm của LỚP CHA chứ không phải lớp con!",
                "subnodes": ["Overloading (Compile-time)", "Overriding (virtual / override)", "Method Hiding (từ khóa new)"]
            },
            {
                "id": "c4",
                "title": "4. Trừu Tượng (Abstraction)",
                "color": "#10b981",
                "summary": "Tách biệt bản thiết kế (What) khỏi cách thực thi (How) thông qua `abstract class` và `interface`.",
                "formula": "public abstract double TinhLuong(); // Bắt buộc lớp con override",
                "exam_trap": "Bẫy thi: Không thể khởi tạo trực tiếp `new AbstractClass()` hay `new IInterface()`, nhưng có thể khai báo biến tham chiếu của chúng!",
                "subnodes": ["Abstract Class (Quan hệ IS-A)", "Interface (Hợp đồng CAN-DO)", "Đa thực thi Interface"]
            }
        ]
    },
    "graph_theory": {
        "root": "Lý Thuyết Đồ Thị & Thuật Toán Cốt Lõi",
        "subtitle": "Toán Rời Rạc: Duyệt đồ thị, Đường đi ngắn nhất & Cây khung",
        "branches": [
            {
                "id": "g1",
                "title": "1. Biểu Diễn & Duyệt Đồ Thị (BFS / DFS)",
                "color": "#3b82f6",
                "summary": "BFS dùng Hàng đợi (Queue - FIFO) tìm đường ngắn nhất theo số cạnh; DFS dùng Ngăn xếp (Stack / Đệ quy) xét tính liên thông, chu trình.",
                "formula": "Độ phức tạp: O(V + E) với Danh sách kề | O(V^2) với Ma trận kề",
                "exam_trap": "Bẫy thi: Khi liệt kê thứ tự đỉnh thăm, phải tuân thủ thứ tự từ điển (A->Z hoặc 1->N) của đề bài!",
                "subnodes": ["BFS -> Queue (Lan truyền theo lớp)", "DFS -> Stack / Đệ quy (Đi sâu)", "Đếm thành phần liên thông"]
            },
            {
                "id": "g2",
                "title": "2. Đường Đi Ngắn Nhất (Dijkstra & Bellman-Ford)",
                "color": "#f59e0b",
                "summary": "Dijkstra dùng chiến lược tham lam cho trọng số không âm; Bellman-Ford nới lỏng cạnh V-1 lần xử lý được trọng số âm.",
                "formula": "Relax: d[v] = min(d[v], d[u] + w(u, v))",
                "exam_trap": "Bẫy thi: Dijkstra SAI khi có cạnh âm! Nếu bước thứ V của Bellman-Ford vẫn giảm được d[v] thì đồ thị có chu trình âm.",
                "subnodes": ["Dijkstra: O((V+E) log V)", "Bellman-Ford: O(V * E)", "Floyd-Warshall mọi cặp đỉnh: O(V^3)"]
            },
            {
                "id": "g3",
                "title": "3. Cây Khung Nhỏ Nhất (Prim & Kruskal)",
                "color": "#10b981",
                "summary": "Cây khung của đồ thị liên thông N đỉnh luôn có đúng N-1 cạnh và không có chu trình.",
                "formula": "Số cạnh cây khung = |V| - 1 | Định lý Cayley: K_n có n^(n-2) cây khung",
                "exam_trap": "Bẫy thi: Kruskal chọn cạnh nhỏ nhất toàn cục (dùng Union-Find chống chu trình); Prim phát triển từ 1 cây liên thông duy nhất.",
                "subnodes": ["Kruskal (Sắp xếp cạnh tăng dần)", "Prim (Mở rộng đỉnh kề gần nhất)", "Union-Find (Disjoint Set)"]
            },
            {
                "id": "g4",
                "title": "4. Chu Trình Euler & Hamilton",
                "color": "#ec4899",
                "summary": "Euler đi qua MỌI CẠNH đúng 1 lần; Hamilton đi qua MỌI ĐỈNH đúng 1 lần.",
                "formula": "Euler: Mọi đỉnh bậc chẵn | Đường đi Euler: Đúng 2 đỉnh bậc lẻ",
                "exam_trap": "Bẫy thi: Định lý Dirac (mọi đỉnh bậc >= n/2 thì có Hamilton) chỉ là điều kiện ĐỦ, không phải điều kiện cần!",
                "subnodes": ["Chu trình Euler (Bậc chẵn)", "Đường đi Euler (2 đỉnh bậc lẻ)", "Chu trình Hamilton (Định lý Dirac/Ore)"]
            }
        ]
    }
}


async def api_mindmap_generate_handler(request):
    try:
        data = await request.json()
    except Exception:
        data = {}

    topic_key = (data.get("preset") or "krebs").strip().lower()
    custom_topic = (data.get("topic") or "").strip()

    if not custom_topic and topic_key in MINDMAP_PRESETS:
        return web.json_response({"ok": True, "mindmap": MINDMAP_PRESETS[topic_key]})

    title = custom_topic or "Chủ đề Học thuật Đại học"
    generated = {
        "root": title,
        "subtitle": "Sơ đồ tư duy phân nhánh thông minh — Bấm vào từng nhánh để xem chi tiết & bẫy thi cử",
        "branches": [
            {
                "id": "m1",
                "title": f"1. Bản chất & Định nghĩa của {title}",
                "color": "#8b5cf6",
                "summary": f"Khái niệm nền tảng, vai trò sinh lý/kỹ thuật và vị trí của {title} trong chương trình học.",
                "formula": "Nguyên lý gốc: Đầu vào (Input/Cơ chất) ---> Cơ chế xử lý ---> Đầu ra (Output/Sản phẩm)",
                "exam_trap": "Bẫy thi: Thường hỏi phân biệt khái niệm này với các cơ chế có tên gọi tương tự.",
                "subnodes": ["Khái niệm cốt lõi", "Điều kiện hoạt động", "Ý nghĩa thực tiễn"]
            },
            {
                "id": "m2",
                "title": "2. Cơ chế & Các bước thực hiện",
                "color": "#06b6d4",
                "summary": f"Trình tự các bước biến đổi hoặc thuật toán xử lý của {title}.",
                "formula": "Bước 1 (Khởi tạo) -> Bước 2 (Điều hòa giới hạn tốc độ) -> Bước 3 (Hoàn tất)",
                "exam_trap": "Bẫy thi: Chú ý bước giới hạn tốc độ (Rate-limiting step) hoặc trường hợp biên (Edge case).",
                "subnodes": ["Giai đoạn khởi phát", "Bước quyết định tốc độ", "Kết quả thu được"]
            },
            {
                "id": "m3",
                "title": "3. Điều hòa & Các yếu tố ảnh hưởng",
                "color": "#10b981",
                "summary": "Các tác nhân kích thích (Activators), chất ức chế (Inhibitors) hoặc độ phức tạp tài nguyên.",
                "formula": "Tối ưu hóa hiệu suất & Cơ chế phản hồi ngược (Feedback Inhibition)",
                "exam_trap": "Bẫy thi: Nhầm lẫn chiều tác động (tăng hay giảm) khi thay đổi nồng độ/tham số đầu vào.",
                "subnodes": ["Yếu tố kích thích / Tối ưu", "Yếu tố ức chế / Giới hạn", "Cơ chế tự điều chỉnh"]
            },
            {
                "id": "m4",
                "title": "4. Ứng dụng Lâm sàng / Thực chiến Code",
                "color": "#f59e0b",
                "summary": f"Vận dụng {title} vào giải quyết ca lâm sàng hoặc bài tập lập trình thực tế.",
                "formula": "Lý thuyết chuẩn + Phân tích dữ kiện đề bài => Đáp án chính xác 100%",
                "exam_trap": "Bẫy thi: Đề bài thường cài dữ kiện nhiễu, hãy gạch chân từ khóa quyết định!",
                "subnodes": ["Ca bệnh / Bài toán điển hình", "Dấu hiệu nhận biết nhanh", "Tổng kết công thức nhớ nhanh"]
            }
        ]
    }
    return web.json_response({"ok": True, "mindmap": generated})


async def api_code_uml_memory_analyzer(request):
    try:
        data = await request.json()
    except Exception:
        data = {}

    code = data.get("code") or ""
    language = (data.get("language") or "csharp").lower()

    classes = []
    stack_frames = []
    heap_objects = []

    if language in ("csharp", "cs", "c#"):
        class_pattern = re.compile(
            r"(?:public|internal|private|protected)?\s*(abstract|sealed|static)?\s*(class|interface|struct)\s+(\w+)(?:\s*:\s*([^{]+))?",
            re.MULTILINE
        )
        for match in class_pattern.finditer(code):
            modifier, kind, cname, inherits_raw = match.groups()
            parents = [p.strip() for p in (inherits_raw or "").split(",") if p.strip()]
            start_pos = match.end()
            brace_depth = 0
            body_chars = []
            started = False
            for ch in code[start_pos:]:
                if ch == "{":
                    brace_depth += 1
                    started = True
                    if brace_depth == 1:
                        continue
                elif ch == "}":
                    brace_depth -= 1
                    if brace_depth == 0 and started:
                        break
                if started and brace_depth >= 1:
                    body_chars.append(ch)
            body = "".join(body_chars)

            fields = []
            methods = []
            for line in body.splitlines():
                s = line.strip()
                if not s or s.startswith("//"):
                    continue
                vis = "+" if "public" in s else ("-" if "private" in s else ("#" if "protected" in s else "~"))
                prop_m = re.match(r"(?:public|private|protected|internal)\s+(?:virtual|override|abstract|static\s+)?([\w<>[\]]+)\s+(\w+)\s*\{\s*get", s)
                if prop_m:
                    fields.append(f"{vis} {prop_m.group(2)} : {prop_m.group(1)} {{get; set;}}")
                    continue
                meth_m = re.match(r"(?:public|private|protected|internal)?\s*(?:virtual|override|abstract|static\s+)?([\w<>[\]]+)\s+(\w+)\s*\(([^)]*)\)", s)
                if meth_m and meth_m.group(2) not in ("if", "for", "while", "switch", "catch"):
                    ret_type, mname, params = meth_m.groups()
                    tag = " «ctor»" if mname == cname else ""
                    methods.append(f"{vis} {mname}({params.strip()}) : {ret_type}{tag}")
                    continue
                field_m = re.match(r"(?:public|private|protected|internal)\s+(?:readonly\s+|static\s+)?([\w<>[\]]+)\s+(\w+)\s*(?:=|;)", s)
                if field_m:
                    fields.append(f"{vis} {field_m.group(2)} : {field_m.group(1)}")

            stereotype = "«interface»" if kind == "interface" else ("«abstract»" if modifier == "abstract" else ("«struct»" if kind == "struct" else "«class»"))
            classes.append({
                "name": cname,
                "stereotype": stereotype,
                "parents": parents,
                "fields": fields[:8],
                "methods": methods[:8]
            })

        alloc_pattern = re.compile(r"([\w<>[\]]+)\s+(\w+)\s*=\s*new\s+([\w<>[\]]+)\s*\(([^)]*)\)")
        addr_counter = 0x7F8A10
        for m in alloc_pattern.finditer(code):
            decl_type, var_name, obj_type, args = m.groups()
            addr = f"0x{addr_counter:06X}"
            addr_counter += 0x48
            stack_frames.append({
                "name": var_name,
                "declared_type": decl_type,
                "kind": "Reference (Con trỏ Stack -> Heap)",
                "value": f"Ref -> {addr}",
                "target_addr": addr
            })
            heap_objects.append({
                "address": addr,
                "type": obj_type,
                "args": args.strip(),
                "polymorphic": decl_type != obj_type,
                "note": f"Đa hình: Biến `{decl_type}` trỏ tới đối tượng `{obj_type}` trên Heap" if decl_type != obj_type else f"Đối tượng `{obj_type}` cấp phát trên Managed Heap"
            })

        val_pattern = re.compile(r"\b(int|double|float|bool|char|decimal|long)\s+(\w+)\s*=\s*([^;]+);")
        for m in val_pattern.finditer(code):
            vtype, vname, vval = m.groups()
            if "new " not in vval:
                stack_frames.append({
                    "name": vname,
                    "declared_type": vtype,
                    "kind": "Value Type (Lưu trực tiếp trên Stack)",
                    "value": vval.strip()[:28],
                    "target_addr": None
                })
    else:
        for m in re.finditer(r"class\s+(\w+)(?:\(([^)]*)\))?:", code):
            cname, parents_raw = m.groups()
            parents = [p.strip() for p in (parents_raw or "").split(",") if p.strip()]
            classes.append({
                "name": cname,
                "stereotype": "«python class»",
                "parents": parents,
                "fields": ["+ self.* (Dynamic Attributes)"],
                "methods": [f"+ {fn}()" for fn in re.findall(r"def\s+(\w+)\s*\(", code)[:6]]
            })
        addr_counter = 0x10A400
        for m in re.finditer(r"^\s*(\w+)\s*=\s*([^\n#]+)", code, re.MULTILINE):
            vname, expr = m.group(1), m.group(2).strip()
            if vname in ("self", "return", "if", "for", "while"):
                continue
            addr = f"0x{addr_counter:06X}"
            addr_counter += 0x30
            stack_frames.append({
                "name": vname,
                "declared_type": "PyObject*",
                "kind": "Name Binding (Tham chiếu Python)",
                "value": f"Ref -> {addr}",
                "target_addr": addr
            })
            heap_objects.append({
                "address": addr,
                "type": "PyObject",
                "args": expr[:36],
                "polymorphic": False,
                "note": f"Đối tượng Python trên Private Heap: `{expr[:36]}`"
            })

    if not classes:
        classes.append({
            "name": "Program",
            "stereotype": "«entry»",
            "parents": [],
            "fields": [],
            "methods": ["+ Main() : void"]
        })

    return web.json_response({
        "ok": True,
        "language": language,
        "classes": classes,
        "stack_frames": stack_frames[:12],
        "heap_objects": heap_objects[:12]
    })


async def api_gamification_quests_handler(request):
    exam_count = 0
    card_count = 0
    mistake_count = 0
    try:
        conn = db.get_connection()
        c = conn.cursor()
        try:
            exam_count = c.execute("SELECT COUNT(*) FROM exam_results").fetchone()[0]
        except Exception:
            try:
                exam_count = c.execute("SELECT COUNT(*) FROM exam_history").fetchone()[0]
            except Exception:
                exam_count = 0
        try:
            card_count = c.execute("SELECT COUNT(*) FROM flashcards").fetchone()[0]
        except Exception:
            card_count = 0
        conn.close()
    except Exception:
        pass

    quests = [
        {
            "id": "q_exam",
            "title": "Chiến thần Phòng Thi",
            "desc": "Hoàn thành ít nhất 1 đề luyện tập hoặc thi thực chiến",
            "progress": min(1, exam_count),
            "target": 1,
            "xp": 150,
            "icon": "🎯",
            "action_view": "exam"
        },
        {
            "id": "q_code",
            "title": "Kiến trúc sư OOP & Thuật toán",
            "desc": "Chạy thử hoặc chấm Test Case 1 bài tập C# / Python + xem sơ đồ UML/Heap",
            "progress": 1 if exam_count > 0 else 0,
            "target": 1,
            "xp": 200,
            "icon": "💻",
            "action_view": "exercises"
        },
        {
            "id": "q_viva",
            "title": "Bản lĩnh Vấn đáp & Feynman",
            "desc": "Thực hành 1 câu hỏi tại Phòng Vấn Đáp AI hoặc Feynman Studio",
            "progress": 0,
            "target": 1,
            "xp": 250,
            "icon": "🎙️",
            "action_view": "viva"
        },
        {
            "id": "q_lab",
            "title": "Nhà nghiên cứu Phòng Lab",
            "desc": "Mô phỏng Động học Enzyme Michaelis-Menten hoặc Thuật toán Đồ thị",
            "progress": 0,
            "target": 1,
            "xp": 180,
            "icon": "🧬",
            "action_view": "lab"
        }
    ]
    total_xp = exam_count * 120 + card_count * 10
    level = max(1, total_xp // 500 + 1)
    return web.json_response({
        "ok": True,
        "level": level,
        "total_xp": total_xp,
        "next_level_xp": level * 500,
        "unresolved_mistakes": mistake_count,
        "quests": quests
    })


# ----------------------------------------------------------------------------
# UNIMASTER AI v42.0: DEVIL'S ADVOCATE ARENA, EBBINGHAUS CURVE & POLYGLOT CODE
# ----------------------------------------------------------------------------

DEVILS_ADVOCATE_BANK = {
    "biochem": [
        {
            "id": "da_bio_1",
            "topic": "Đái tháo đường Tuýp 1 & Tân tạo đường (Gluconeogenesis)",
            "fallacy_claim": "Ở bệnh nhân Đái tháo đường tuýp 1 không điều trị, nồng độ Glucose trong máu đang cực kỳ cao (hyperglycemia), nên tế bào gan nhận thấy cơ thể đã dư thừa đường và sẽ Tắt hoàn toàn quá trình Tân tạo đường (Gluconeogenesis) cũng như Phân giải Glycogen.",
            "trap_type": "Ngụy biện Ngoại suy Trực giác (Nồng độ ngoại bào vs Tín hiệu nội bào)",
            "keywords": ["insulin", "glucagon", "nội bào", "tăng tân tạo đường", "cơ chất", "Fructose-2,6-bisphosphate", "nhiễm toan ceton"],
            "truth_explanation": "NHẬN ĐỊNH TRÊN HOÀN TOÀN SAI! Dù Glucose trong máu (ngoại bào) rất cao, nhưng do thiếu hụt tuyệt đối Insulin và tăng cao tỷ lệ Glucagon/Insulin, các mô phụ thuộc GLUT4 (cơ vân, mô mỡ) không đưa được glucose vào trong tế bào ('đói giữa biển đường'). Tại gan, tỷ lệ Glucagon/Insulin cao làm giảm Fructose-2,6-bisphosphate, kích hoạt mạnh mẽ các enzyme tân tạo đường (PEPCK, Fructose-1,6-bisphosphatase, Glucose-6-phosphatase) và phân giải glycogen, khiến gan tiếp tục bơm thêm Glucose vào máu làm đường huyết càng tăng kịch trần kèm sinh thể ceton.",
            "challenge_followup": "Tại sao ở bệnh nhân này, nồng độ Malonyl-CoA trong tế bào chất của gan lại giảm mạnh và điều đó ảnh hưởng thế nào đến enzyme CPT-I (Carnitine Palmitoyltransferase I)?"
        },
        {
            "id": "da_bio_2",
            "topic": "Ngộ độc Cyanide (CN-) / CO và Thuốc giải ghép cặp DNP",
            "fallacy_claim": "Khi bệnh nhân bị ngộ độc Cyanide (CN-) làm khóa chặt Phức hợp IV (Cytochrome c oxidase) khiến chuỗi hô hấp ngừng tạo ATP, ta có thể truyền chất giải ghép cặp 2,4-Dinitrophenol (DNP) để mở đường vòng cho proton H+ đi qua màng trong ty thể nhằm khôi phục lại quá trình tổng hợp ATP!",
            "trap_type": "Ngụy biện Cơ chế Hóa thẩm (Chemiosmotic Coupling Fallacy)",
            "keywords": ["gradient proton", "F0F1-ATP synthase", "tỏa nhiệt", "ức chế phức hợp IV", "NADH", "giải ghép cặp"],
            "truth_explanation": "SAI LẦM CHẾT NGƯỜI! Thứ nhất, DNP là chất giải ghép cặp (uncoupler) làm rò rỉ H+ qua màng trong ty thể, làm TRIỆT TIÊU chênh lệch điện hóa proton (proton-motive force) nên năng lượng chỉ giải phóng dưới dạng NHIỆT chứ hoàn toàn KHÔNG đi qua F0F1-ATP synthase để tạo ATP. Thứ hai, khi Phức hợp IV đã bị CN- khóa chặt, dòng vận chuyển điện tử bị tắc nghẽn ở cuối nguồn nên các phức hợp I, III cũng không thể bơm H+ ra khoảng gian màng.",
            "challenge_followup": "Phác đồ hóa sinh đúng đắn để cấp cứu ngộ độc Cyanide bằng Amyl nitrite / Sodium nitrite + Sodium thiosulfate hoạt động dựa trên sự chuyển dạng nào của Hemoglobin?"
        }
    ],
    "csharp_oop": [
        {
            "id": "da_cs_1",
            "topic": "Struct (Value Type) & Thực thi Interface trong C#",
            "fallacy_claim": "Trong C# (.NET), vì `struct` là kiểu giá trị (Value Type) nằm trên vùng nhớ Stack chứ không phải trên Managed Heap như `class`, nên `struct` tuyệt đối KHÔNG BAO GIỜ có thể thực thi (implement) một `interface` như `IComparable` hay `IDisposable`.",
            "trap_type": "Ngụy biện Đồng nhất Kế thừa Lớp với Thực thi Hợp đồng Interface",
            "keywords": ["implement interface", "boxing", "IComparable", "IDisposable", "không kế thừa class", "ValueType"],
            "truth_explanation": "SAI HOÀN TOÀN! Trong C#, `struct` không thể kế thừa từ một `class` hay `struct` khác (vì bản thân nó đã ngầm kế thừa `System.ValueType`), nhưng `struct` HOÀN TOÀN CÓ THỂ thực thi bất kỳ số lượng `interface` nào (ví dụ `int` là `System.Int32` struct thực thi `IComparable<int>`, `IEquatable<int>`). Tuy nhiên cần lưu ý: khi ép kiểu một biến `struct` sang kiểu tham chiếu `interface` (như `IComparable c = myStruct;`), CLR sẽ thực hiện **Boxing** (đóng gói bản sao của struct lên Managed Heap) trừ khi dùng Generic có ràng buộc `where T : IComparable<T>`!",
            "challenge_followup": "Tại sao sử dụng phương thức Generic `void Sort<T>(T item) where T : IComparable<T>` với `struct` lại giúp tránh hoàn toàn hiện tượng Boxing?"
        },
        {
            "id": "da_cs_2",
            "topic": "Từ khóa `readonly` với Kiểu Tham Chiếu (Reference Type)",
            "fallacy_claim": "Khi khai báo `public readonly List<string> DanhSach = new List<string>();` trong một lớp C#, từ khóa `readonly` biến danh sách này thành bất biến tuyệt đối (Immutable), nên mọi lệnh gọi `DanhSach.Add(\"SV01\")` bên ngoài constructor đều sẽ báo lỗi biên dịch!",
            "trap_type": "Ngụy biện Bất biến Tham chiếu (Reference Immutability) vs Bất biến Trạng thái Đối tượng (Object Mutability)",
            "keywords": ["con trỏ", "tham chiếu", "Add", "mutate", "new List", "IReadOnlyList", "bất biến"],
            "truth_explanation": "SAI! Với kiểu tham chiếu (Reference Type), từ khóa `readonly` chỉ khóa chặt **địa chỉ con trỏ trên biến trường** (nghĩa là ngoài constructor bạn không thể gán lại `DanhSach = new List<string>();` sang vùng nhớ mới), nhưng đối tượng `List<string>` nằm trên Heap mà nó trỏ tới vẫn hoàn toàn CÓ THỂ bị thay đổi nội dung bên trong bằng `DanhSach.Add(...)` hoặc `DanhSach.Clear()`! Để bảo vệ dữ liệu thực sự, phải trả về `IReadOnlyList<string>` hoặc `AsReadOnly()`.",
            "challenge_followup": "Sự khác biệt cốt lõi giữa hằng số biên dịch `const` và trường chỉ đọc `readonly` trong C# là gì?"
        }
    ],
    "discrete_math": [
        {
            "id": "da_dm_1",
            "topic": "Thuật toán Dijkstra với Trọng số Âm bằng Phép Cộng Hằng Số",
            "fallacy_claim": "Nếu đồ thị có cạnh trọng số âm (nhưng không có chu trình âm), ví dụ cạnh nhỏ nhất là -5, ta chỉ cần cộng thêm +6 vào TẤT CẢ các cạnh của đồ thị để mọi cạnh đều dương (> 0), sau đó chạy thuật toán Dijkstra thì chắc chắn tìm được đúng đường đi ngắn nhất của đồ thị ban đầu!",
            "trap_type": "Ngụy biện Bảo toàn Thứ tự Đường đi khi Dịch chuyển Trọng số Cạnh",
            "keywords": ["số cạnh", "đường đi nhiều cạnh", "Bellman-Ford", "cộng thêm k*C", "không bảo toàn"],
            "truth_explanation": r"BẪY KINH ĐIỂN TRONG ĐỀ THI GIẢI THUẬT! Khi cộng hằng số dương $C$ vào mỗi cạnh, một đường đi gồm $k$ cạnh sẽ bị cộng thêm $k \cdot C$ chứ không phải một hằng số cố định! Do đó, đường đi $P_1$ có ít cạnh hơn (ví dụ 1 cạnh trọng số 5 $\to 5 + 6 = 11$) sẽ được thiên vị bất công so với đường đi $P_2$ có nhiều cạnh hơn nhưng tổng ban đầu nhỏ hơn (ví dụ 3 cạnh tổng $2 + 2 + (-5) = -1$, sau khi cộng $+6$ mỗi cạnh lại biến thành $8 + 8 + 1 = 17 > 11$). Để xử lý cạnh âm đúng chuẩn phải dùng **Bellman-Ford** hoặc **Thuật toán Johnson** (trọng số lại bằng hàm thế vị $w'(u,v) = w(u,v) + h(u) - h(v)$).",
            "challenge_followup": "Tại sao phép biến đổi trọng số của thuật toán Johnson $w'(u,v) = w(u,v) + h(u) - h(v)$ lại bảo toàn chính xác thứ tự mọi đường đi ngắn nhất giữa hai đỉnh $s$ và $t$?"
        }
    ],
    "python": [
        {
            "id": "da_py_1",
            "topic": "Tham số Mặc định Khả biến (Mutable Default Arguments) trong Python",
            "fallacy_claim": "Trong Python, khi định nghĩa hàm `def them_sinh_vien(ten, ds=[]): ds.append(ten); return ds`, mỗi lần ta gọi `them_sinh_vien('An')` rồi `them_sinh_vien('Bình')` mà không truyền tham số thứ hai, Python sẽ tự động tạo mới một danh sách rỗng `[]` cho từng lần gọi hàm.",
            "trap_type": "Ngụy biện Thời điểm Khởi tạo Tham số Mặc định (Definition-time vs Call-time Evaluation)",
            "keywords": ["def", "một lần duy nhất", "None", "__defaults__", "chia sẻ cùng đối tượng", "mutable"],
            "truth_explanation": "SAI! Trong Python, giá trị mặc định của tham số hàm (`ds=[]`) chỉ được khởi tạo **ĐÚNG MỘT LẦN DUY NHẤT** tại thời điểm câu lệnh `def` được biên dịch (lưu trong thuộc tính `them_sinh_vien.__defaults__`), chứ KHÔNG tạo lại mỗi khi gọi hàm! Vì vậy lần gọi thứ hai `them_sinh_vien('Bình')` sẽ nối tiếp vào chính danh sách cũ và trả về `['An', 'Bình']`. Cách viết chuẩn Pythonic bắt buộc là `def them_sinh_vien(ten, ds=None): if ds is None: ds = []`.",
            "challenge_followup": "Tương tự, điều gì xảy ra khi bạn khởi tạo ma trận 2 chiều bằng cú pháp `matrix = [[0] * 3] * 3` rồi gán `matrix[0][0] = 99`?"
        }
    ]
}


async def api_devils_advocate_handler(request):
    try:
        data = await request.json()
    except Exception:
        data = {}

    action = data.get("action", "challenge")
    domain = data.get("domain", "biochem")
    challenge_id = data.get("challenge_id", "")

    domain_alias = {"csharp": "csharp_oop", "discrete": "discrete_math"}.get(domain, domain)
    bank = DEVILS_ADVOCATE_BANK.get(domain_alias, DEVILS_ADVOCATE_BANK["biochem"])

    if action in ("challenge", "next", "next_challenge"):
        import random
        candidates = [item for item in bank if item["id"] != challenge_id] or bank
        chosen = random.choice(candidates)
        return web.json_response({
            "ok": True,
            "challenge_id": chosen["id"],
            "topic": chosen["topic"],
            "ai_claim": chosen["fallacy_claim"],
            "fallacy_claim": chosen["fallacy_claim"],
            "trap_type": chosen["trap_type"],
            "hint": f"Loại bẫy: {chosen['trap_type']}. Hãy chú ý các từ khóa: {', '.join(chosen['keywords'][:3])}...",
            "hint_keywords_count": len(chosen["keywords"])
        })

    rebuttal = (data.get("rebuttal") or "").strip()
    if not rebuttal:
        return web.json_response({"ok": False, "error": "Hãy nhập lập luận phản biện của bạn để bóc trần lỗi sai của AI!"}, status=400)

    matched = next((item for item in bank if item["id"] == challenge_id), bank[0])
    reb_lower = rebuttal.lower()
    keywords = matched.get("keywords", [])
    hit_kw = [kw for kw in keywords if kw.lower() in reb_lower]
    missed_kw = [kw for kw in keywords if kw.lower() not in reb_lower]

    has_refutation_tone = any(w in reb_lower for w in ["sai", "không đúng", "ngược lại", "bởi vì", "thực tế", "tuy nhiên", "nhầm", "vì"])
    word_count = len(rebuttal.split())
    kw_ratio = len(hit_kw) / max(1, len(keywords))
    len_ratio = min(1.0, word_count / 30.0)

    critical_score = min(100, int(round((kw_ratio * 0.65 + len_ratio * 0.25 + (0.10 if has_refutation_tone else 0)) * 100)))
    critical_score = max(45 if has_refutation_tone else 30, critical_score)

    badge = (
        "🏆 Đại Kiện Tướng Phản Biện (S-Rank)" if critical_score >= 85
        else ("⚔️ Thợ Săn Ngụy Biện (A-Rank)" if critical_score >= 70
        else ("🛡️ Người Gác Đền Tư Duy (B-Rank)" if critical_score >= 55
        else "🔍 Cần Sắc Bén Hơn (C-Rank)"))
    )

    ai_verdict = (
        f"Bạn đã bóc tách trúng {len(hit_kw)}/{len(keywords)} luận điểm cốt lõi ({', '.join(hit_kw) if hit_kw else 'chưa điểm trúng tử huyệt cơ chế'}). "
        f"Loại bẫy ngụy biện của câu này là: {matched['trap_type']}."
    )

    try:
        if ai.has_active_key():
            prompt = (
                f"Trong trò chơi Phản biện Học thuật (Devil's Advocate), AI đưa ra nhận định sai có chủ đích:\n'{matched['fallacy_claim']}'\n"
                f"Sinh viên phản biện lại:\n'{rebuttal}'\n"
                f"Sự thật khoa học: '{matched['truth_explanation']}'\n"
                f"Hãy nhận xét ngắn gọn, hào hứng (3 câu tiếng Việt) xem sinh viên đã bắt trúng chỗ sai chưa và khen/góp ý điểm nào."
            )
            ai_text = await asyncio.wait_for(ai._call_gemini_text(prompt, temperature=0.35), timeout=8.0)
            if ai_text and len(ai_text.strip()) > 20:
                ai_verdict = ai_text.strip()
    except Exception:
        pass

    return web.json_response({
        "ok": True,
        "score": critical_score,
        "critical_score": critical_score,
        "rank": badge,
        "badge": badge,
        "trap_type": matched["trap_type"],
        "hit_keywords": hit_kw,
        "missed_keywords": missed_kw,
        "missing_keywords": missed_kw,
        "ai_response": ai_verdict,
        "ai_verdict": ai_verdict,
        "fallacy_exposed": f"[{matched['trap_type']}] Câu hỏi mở rộng: {matched['challenge_followup']}",
        "scientific_truth": matched["truth_explanation"],
        "truth_explanation": matched["truth_explanation"],
        "challenge_followup": matched["challenge_followup"]
    })


async def api_forgetting_curve_handler(request):
    import math
    exam_count = 0
    avg_score = 7.2
    card_count = 0
    reviewed_cards = 0
    try:
        conn = db.get_connection()
        c = conn.cursor()
        try:
            row = c.execute("SELECT COUNT(*), AVG(score) FROM exam_results").fetchone()
            exam_count = int(row[0] or 0)
            if row[1] is not None:
                avg_score = float(row[1])
        except Exception:
            pass
        try:
            card_count = int(c.execute("SELECT COUNT(*) FROM flashcards").fetchone()[0] or 0)
            reviewed_cards = int(c.execute("SELECT COUNT(*) FROM flashcards WHERE repetitions > 0").fetchone()[0] or 0)
        except Exception:
            pass
        conn.close()
    except Exception:
        pass

    base_stability = 2.6 + min(4.5, exam_count * 0.25 + reviewed_cards * 0.05)
    days = list(range(0, 15))
    unreviewed_curve = []
    spaced_curve = []

    current_s = base_stability
    last_review_day = 0
    review_checkpoints = {1, 3, 7, 14}

    for d in days:
        r_unrev = round(100.0 * math.exp(-d / 2.5), 1)
        unreviewed_curve.append({"day": d, "retention": r_unrev})

        if d == 0:
            spaced_curve.append({"day": 0, "retention": 100.0, "is_review": True})
        elif d in review_checkpoints:
            current_s *= 1.85
            last_review_day = d
            spaced_curve.append({"day": d, "retention": 98.0, "is_review": True})
        else:
            dt = d - last_review_day
            r_sp = round(98.0 * math.exp(-dt / current_s), 1)
            spaced_curve.append({"day": d, "retention": max(45.0, r_sp), "is_review": False})

    predicted_score = round(min(9.8, max(5.5, avg_score * 0.7 + min(3.0, (exam_count * 0.15 + 1.8)))), 1)
    ci_margin = round(max(0.2, 0.85 - min(0.55, exam_count * 0.04)), 1)
    readiness_pct = min(98, max(42, int(round(predicted_score * 10))))

    combined_curve = []
    for idx, d in enumerate(days):
        combined_curve.append({
            "day": d,
            "label": f"D{d}",
            "natural_retention": unreviewed_curve[idx]["retention"],
            "spaced_retention": spaced_curve[idx]["retention"],
            "is_review_checkpoint": spaced_curve[idx]["is_review"]
        })

    advice_text = (
        f"Với độ bền trí nhớ S = {round(base_stability, 2)}, nếu không ôn ngắt quãng, sau 7 ngày bạn sẽ quên {round(100 - unreviewed_curve[7]['retention'], 1)}% kiến thức. "
        f"Hãy kích hoạt 4 mốc ôn tập Vàng (Ngày 1 - Ngày 3 - Ngày 7 - Ngày 14) để giữ tỷ lệ nhớ trên 91% vào ngày thi!"
    )

    return web.json_response({
        "ok": True,
        "exam_count": exam_count,
        "exam_attempts": exam_count,
        "avg_exam_pct": round(avg_score * 10, 1),
        "card_count": card_count,
        "total_flashcards": card_count,
        "reviewed_cards": reviewed_cards,
        "due_flashcards": max(0, card_count - reviewed_cards),
        "stability_index": round(base_stability, 2),
        "memory_strength_s": round(base_stability, 2),
        "predicted_score": predicted_score,
        "predicted_exam_score_10": predicted_score,
        "confidence_interval": f"{predicted_score} ± {ci_margin}",
        "confidence_interval_95": [round(max(0.0, predicted_score - ci_margin), 1), round(min(10.0, predicted_score + ci_margin), 1)],
        "readiness_pct": readiness_pct,
        "current_retention_pct": readiness_pct,
        "curve": combined_curve,
        "unreviewed_curve": unreviewed_curve,
        "spaced_curve": spaced_curve,
        "review_days": sorted(list(review_checkpoints)),
        "recommendation": advice_text,
        "strategy_advice": advice_text
    })


POLYGLOT_PRESETS = {
    "linq_filter": {
        "title": "Lọc, Sắp xếp & Ánh xạ Dữ liệu (LINQ vs List Comprehension vs SQL)",
        "time_complexity": "O(N log N)",
        "space_complexity": "O(N)",
        "active_curve": "nlogn",
        "csharp": (
            "// C# (.NET LINQ Method & Query Syntax)\n"
            "var topStudents = students\n"
            "    .Where(s => s.Gpa >= 8.0 && s.IsActive)\n"
            "    .OrderByDescending(s => s.Gpa)\n"
            "    .Select(s => new { s.Id, s.FullName, Rank = \"Giỏi\" })\n"
            "    .ToList();"
        ),
        "python": (
            "# Python 3 (List Comprehension + sorted key lambda)\n"
            "filtered = [s for s in students if s.gpa >= 8.0 and s.is_active]\n"
            "filtered.sort(key=lambda s: s.gpa, reverse=True)\n"
            "top_students = [\n"
            "    {\"id\": s.id, \"full_name\": s.full_name, \"rank\": \"Giỏi\"}\n"
            "    for s in filtered\n"
            "]"
        ),
        "sql_pseudo": (
            "-- SQL Tương đương & Bản chất Giải thuật\n"
            "SELECT id, full_name, 'Giỏi' AS rank\n"
            "FROM students\n"
            "WHERE gpa >= 8.0 AND is_active = 1\n"
            "ORDER BY gpa DESC;\n"
            "-- Độ phức tạp: Lọc tuyến tính O(N) + TimSort/QuickSort O(N log N)"
        ),
        "notes": "Trong C#, LINQ sử dụng cơ chế **Deferred Execution** (trì hoãn thực thi) cho đến khi gọi `.ToList()` hoặc duyệt `foreach`. Trong Python, List Comprehension thực thi tức thời (Eager), còn nếu dùng `(s for s in ...)` sẽ tạo Generator tương đương với `IEnumerable<T>` của C#!"
    },
    "hash_lookup": {
        "title": "Đếm Tần Suất & Tra cứu Bảng Băm O(1) (Dictionary vs dict/Counter)",
        "time_complexity": "O(N)",
        "space_complexity": "O(U) (U là số phần tử phân biệt)",
        "active_curve": "n",
        "csharp": (
            "// C# (Dictionary<TKey, TValue> - Hash Table O(1) Lookup)\n"
            "var freq = new Dictionary<string, int>();\n"
            "foreach (string word in words)\n"
            "{\n"
            "    freq[word] = freq.GetValueOrDefault(word, 0) + 1;\n"
            "}"
        ),
        "python": (
            "# Python 3 (collections.Counter hoặc dict.get)\n"
            "from collections import Counter\n"
            "freq = Counter(words)\n"
            "# Hoặc thủ công:\n"
            "# freq = {}\n"
            "# for w in words: freq[w] = freq.get(w, 0) + 1"
        ),
        "sql_pseudo": (
            "-- SQL Aggregation / Mã giả Bảng băm\n"
            "SELECT word, COUNT(*) AS freq\n"
            "FROM word_list\n"
            "GROUP BY word;\n"
            "-- Thay vì 2 vòng lặp lồng nhau O(N^2), Bảng băm giảm thời gian xuống O(N)!"
        ),
        "notes": "Nếu dùng 2 vòng lặp `for` lồng nhau để đếm tần suất hoặc tìm cặp tổng bằng $K$ (Two-Sum), độ phức tạp là $O(N^2)$. Khi thay bằng `Dictionary<K,V>` (C#) hoặc `dict`/`set` (Python), mỗi phép tra cứu `ContainsKey` / `in` chỉ tốn $O(1)$ trung bình nên toàn bộ thuật toán giảm xuống $O(N)$!"
    },
    "binary_search": {
        "title": "Tìm Kiếm Nhị Phân Chia Để Trị (Binary Search O(log N))",
        "time_complexity": "O(log N)",
        "space_complexity": "O(1)",
        "active_curve": "logn",
        "csharp": (
            "// C# (Chống tràn số nguyên với left + (right - left) / 2)\n"
            "int BinarySearch(int[] arr, int target)\n"
            "{\n"
            "    int left = 0, right = arr.Length - 1;\n"
            "    while (left <= right)\n"
            "    {\n"
            "        int mid = left + (right - left) / 2;\n"
            "        if (arr[mid] == target) return mid;\n"
            "        if (arr[mid] < target) left = mid + 1;\n"
            "        else right = mid - 1;\n"
            "    }\n"
            "    return -1;\n"
            "}"
        ),
        "python": (
            "# Python 3 (Module chuẩn bisect hoặc cài đặt 2 con trỏ)\n"
            "def binary_search(arr: list[int], target: int) -> int:\n"
            "    left, right = 0, len(arr) - 1\n"
            "    while left <= right:\n"
            "        mid = (left + right) // 2\n"
            "        if arr[mid] == target:\n"
            "            return mid\n"
            "        elif arr[mid] < target:\n"
            "            left = mid + 1\n"
            "        else:\n"
            "            right = mid - 1\n"
            "    return -1"
        ),
        "sql_pseudo": (
            "-- Hệ thức truy hồi Master Theorem:\n"
            "T(N) = T(N / 2) + O(1)  ===>  T(N) = O(log2(N))\n"
            "-- Với N = 1,000,000 phần tử đã sắp xếp:\n"
            "-- Duyệt tuần tự O(N) mất tối đa 1,000,000 bước.\n"
            "-- Tìm kiếm nhị phân O(log N) chỉ mất tối đa 20 bước!"
        ),
        "notes": "Trong C#/Java/C++, công thức `(left + right) / 2` có thể gây **tràn số nguyên 32-bit (Integer Overflow)** nếu `left + right > 2,147,483,647`. Công thức an toàn tuyệt đối là `left + (right - left) / 2`. Trong Python, kiểu `int` có độ lớn tùy ý (Arbitrary-precision) nên không bao giờ tràn số!"
    },
    "oop_polymorphism": {
        "title": "Kế Thừa, Lớp Trừu Tượng & Đa Hình (C# OOP vs Python ABC)",
        "time_complexity": "O(1) (Tra cứu V-Table)",
        "space_complexity": "O(1)",
        "active_curve": "const",
        "csharp": (
            "// C# (abstract class + virtual/override)\n"
            "public abstract class NhanVien\n"
            "{\n"
            "    public string HoTen { get; set; }\n"
            "    protected NhanVien(string ten) => HoTen = ten;\n"
            "    public abstract double TinhLuong();\n"
            "}\n"
            "public class BacSi : NhanVien\n"
            "{\n"
            "    public int SoCaTruc { get; set; }\n"
            "    public BacSi(string ten, int ca) : base(ten) => SoCaTruc = ca;\n"
            "    public override double TinhLuong() => 15000000 + SoCaTruc * 500000;\n"
            "}"
        ),
        "python": (
            "# Python 3 (abc.ABC + @abstractmethod + super())\n"
            "from abc import ABC, abstractmethod\n\n"
            "class NhanVien(ABC):\n"
            "    def __init__(self, ho_ten: str):\n"
            "        self.ho_ten = ho_ten\n"
            "    @abstractmethod\n"
            "    def tinh_luong(self) -> float:\n"
            "        pass\n\n"
            "class BacSi(NhanVien):\n"
            "    def __init__(self, ten: str, so_ca_truc: int):\n"
            "        super().__init__(ten)\n"
            "        self.so_ca_truc = so_ca_truc\n"
            "    def tinh_luong(self) -> float:\n"
            "        return 15_000_000 + self.so_ca_truc * 500_000"
        ),
        "sql_pseudo": (
            "-- So sánh Cơ chế Liên kết Động (Dynamic Dispatch):\n"
            "C# (.NET): Mặc định phương thức là NON-VIRTUAL. Muốn đa hình phải khai báo\n"
            "           rõ từ khóa `virtual`/`abstract` ở lớp cha và `override` ở lớp con.\n"
            "Python:    MỌI phương thức đều là `virtual` (Duck Typing & Dynamic Lookup)."
        ),
        "notes": "Điểm khác biệt hay hỏi thi nhất giữa C# và Python/Java: Trong C#, nếu không có từ khóa `virtual`/`override`, lời gọi hàm được gắn cứng lúc biên dịch (**Early Binding**). Trong Python, mọi lời gọi phương thức đều được phân giải động lúc chạy theo thứ tự **MRO (Method Resolution Order)**."
    },
    "dijkstra_pq": {
        "title": "Thuật toán Dijkstra với Hàng Đợi Ưu Tiên (PriorityQueue / heapq)",
        "time_complexity": "O((V + E) log V)",
        "space_complexity": "O(V + E)",
        "active_curve": "O(N log N)",
        "csharp": (
            "// C# (.NET 6+ PriorityQueue<TElement, TPriority>)\n"
            "var dist = Enumerable.Repeat(int.MaxValue, n).ToArray();\n"
            "var pq = new PriorityQueue<int, int>();\n"
            "dist[src] = 0;\n"
            "pq.Enqueue(src, 0);\n"
            "while (pq.TryDequeue(out int u, out int d))\n"
            "{\n"
            "    if (d > dist[u]) continue;\n"
            "    foreach (var (v, w) in adj[u])\n"
            "        if (dist[u] + w < dist[v])\n"
            "            pq.Enqueue(v, dist[v] = dist[u] + w);\n"
            "}"
        ),
        "python": (
            "# Python 3 (heapq Min-Heap Priority Queue)\n"
            "import heapq\n"
            "dist = [float('inf')] * n\n"
            "dist[src] = 0\n"
            "pq = [(0, src)]\n"
            "while pq:\n"
            "    d, u = heapq.heappop(pq)\n"
            "    if d > dist[u]: continue\n"
            "    for v, w in adj[u]:\n"
            "        if dist[u] + w < dist[v]:\n"
            "            dist[v] = dist[u] + w\n"
            "            heapq.heappush(pq, (dist[v], v))"
        ),
        "sql_pseudo": (
            "-- Mã giả Chuẩn Giáo trình Lý thuyết Đồ thị:\n"
            "1. Khởi tạo d[s] = 0, d[v] = ∞ (v ≠ s), Min-Heap Q = {(0, s)}\n"
            "2. Lặp khi Q ≠ Ø: Lấy đỉnh u có d[u] nhỏ nhất (O(log V))\n"
            "3. Nới lỏng (Relax) mọi cạnh kề (u, v): nếu d[u] + w(u,v) < d[v]\n"
            "   thì cập nhật d[v] và đẩy vào Min-Heap."
        ),
        "notes": "Sử dụng Binary Min-Heap (`PriorityQueue` trong C# hoặc `heapq` trong Python) giúp giảm thời gian tìm đỉnh có khoảng cách nhỏ nhất từ $O(V^2)$ xuống $O((V + E) \\log V)$!"
    },
    "dp_knapsack": {
        "title": "Quy Hoạch Động: Bài Toán Balo 0/1 (0/1 Knapsack DP)",
        "time_complexity": "O(N * W)",
        "space_complexity": "O(W)",
        "active_curve": "O(N^2)",
        "csharp": (
            "// C# (Quy hoạch động mảng 1 chiều tối ưu bộ nhớ O(W))\n"
            "int[] dp = new int[W + 1];\n"
            "for (int i = 0; i < n; i++)\n"
            "    for (int w = W; w >= weights[i]; w--)\n"
            "        dp[w] = Math.Max(dp[w], dp[w - weights[i]] + values[i]);\n"
            "return dp[W];"
        ),
        "python": (
            "# Python 3 (1D Dynamic Programming duyệt ngược trọng lượng)\n"
            "dp = [0] * (W + 1)\n"
            "for w_i, v_i in zip(weights, values):\n"
            "    for w in range(W, w_i - 1, -1):\n"
            "        dp[w] = max(dp[w], dp[w - w_i] + v_i)\n"
            "return dp[W]"
        ),
        "sql_pseudo": (
            "-- Công thức Truy hồi Bellman:\n"
            "dp[i][w] = max( dp[i-1][w], dp[i-1][w - weight[i]] + value[i] )\n"
            "-- Mẹo tối ưu không gian từ O(N*W) xuống O(W):\n"
            "Duyệt w giảm dần từ W về weight[i] để không ghi đè trạng thái hàng i-1!"
        ),
        "notes": "Tại sao phải duyệt `w` lùi từ `W` về `weights[i]`? Vì nếu duyệt tiến từ nhỏ đến lớn, cùng một đồ vật thứ `i` sẽ bị chọn nhiều lần (biến thành bài toán **Unbounded Knapsack**)."
    },
    "two_sum_hash": {
        "title": "Truy Vấn Cặp Phần Tử & Bảng Băm O(N) (C# Dictionary / LINQ vs Python Dict)",
        "time_complexity": "O(N)",
        "space_complexity": "O(N)",
        "active_curve": "O(N)",
        "csharp": (
            "// C# (Dictionary<int, int> tra cứu phần bù O(1))\n"
            "var seen = new Dictionary<int, int>();\n"
            "for (int i = 0; i < nums.Length; i++)\n"
            "{\n"
            "    int comp = target - nums[i];\n"
            "    if (seen.TryGetValue(comp, out int idx)) return new[] { idx, i };\n"
            "    seen[nums[i]] = i;\n"
            "}"
        ),
        "python": (
            "# Python 3 (dict hash table O(1) average lookup)\n"
            "seen: dict[int, int] = {}\n"
            "for i, x in enumerate(nums):\n"
            "    if (target - x) in seen:\n"
            "        return [seen[target - x], i]\n"
            "    seen[x] = i"
        ),
        "sql_pseudo": (
            "-- SQL Self-Join vs Hash Join:\n"
            "SELECT a.idx, b.idx\n"
            "FROM nums a JOIN nums b ON a.val + b.val = :target AND a.idx < b.idx;\n"
            "-- Hash Table giảm từ O(N^2) vét cạn xuống O(N) duyệt 1 lần!"
        ),
        "notes": "Sử dụng `TryGetValue` trong C# chỉ băm khóa (hash key) **đúng 1 lần**, nhanh gấp đôi so với việc gọi `ContainsKey(k)` rồi lại truy cập `seen[k]`."
    }
}


async def api_polyglot_transpile_handler(request):
    try:
        data = await request.json()
    except Exception:
        data = {}

    preset_key = (data.get("preset") or "binary_search").strip()
    custom_code = (data.get("custom_code") or "").strip()

    item = POLYGLOT_PRESETS.get(preset_key) or POLYGLOT_PRESETS["binary_search"]
    custom_analysis = None

    if custom_code:
        for_count = len(re.findall(r"\b(for|foreach|while)\b", custom_code))
        has_sort = any(w in custom_code.lower() for w in [".sort", "orderby", "sorted("])
        if for_count >= 2:
            est_comp = "O(N^2)"
        elif has_sort:
            est_comp = "O(N log N)"
        elif for_count == 1:
            est_comp = "O(N)"
        else:
            est_comp = "O(1)"
        custom_analysis = {
            "detected_loops": for_count,
            "estimated_complexity": est_comp
        }

    return web.json_response({
        "ok": True,
        "title": item["title"],
        "time_complexity": item["time_complexity"],
        "space_complexity": item["space_complexity"],
        "active_curve": item["active_curve"],
        "csharp": item["csharp"],
        "python": item["python"],
        "sql_or_pseudo": item["sql_pseudo"],
        "complexity_note": item["notes"],
        "custom_analysis": custom_analysis,
        "result": item
    })


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
    app.router.add_post("/api/code/fix-and-upgrade", api_code_fix_and_upgrade)
    app.router.add_post("/api/code/suggest", api_code_suggest)
    app.router.add_post("/api/code/inspect-line", api_code_inspect_line)
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
    app.router.add_get("/api/exercises/{id}", get_exercise_detail)
    app.router.add_get("/api/flashcards", get_flashcards_by_query)

    # Missing endpoints surfaced by test_server_endpoints.py
    app.router.add_get("/api/ai/key-status", api_ai_key_status)
    app.router.add_get("/api/network/qr-info", api_network_qr_info)
    app.router.add_get("/api/battle/leaderboard", api_battle_leaderboard)
    app.router.add_get("/api/stem/reference", api_stem_reference)
    app.router.add_get("/api/exam/ctump-parts", api_exam_ctump_parts)

    # UniMaster AI v41.0 & v42.0 Super-Suite Routes
    app.router.add_post("/api/ai/viva-simulator", api_viva_simulator_handler)
    app.router.add_post("/api/ai/feynman-evaluate", api_feynman_evaluate_handler)
    app.router.add_post("/api/ai/mindmap-generate", api_mindmap_generate_handler)
    app.router.add_post("/api/code/uml-memory-analyzer", api_code_uml_memory_analyzer)
    app.router.add_get("/api/gamification/quests", api_gamification_quests_handler)
    app.router.add_post("/api/ai/devils-advocate", api_devils_advocate_handler)
    app.router.add_get("/api/analytics/forgetting-curve", api_forgetting_curve_handler)
    app.router.add_post("/api/code/polyglot-transpile", api_polyglot_transpile_handler)

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
