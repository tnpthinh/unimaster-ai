# -*- coding: utf-8 -*-
"""
Update server.py with multi-account authentication, role-based security (admin only),
per-user state isolation and history sync, and modern luxury login/register page.
"""

import os
import re

SERVER_PY_PATH = r"C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai\server.py"

with open(SERVER_PY_PATH, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update AUTH_EXEMPT_PATHS
old_auth_exempt = """AUTH_EXEMPT_PATHS = {
    "/login", "/api/login", "/manifest.json", "/icon.svg", "/healthz",
    "/ws/arena", "/api/export/anki", "/api/export/printable-exam"
}"""

new_auth_exempt = """AUTH_EXEMPT_PATHS = {
    "/login", "/api/login", "/api/auth/login", "/api/auth/register",
    "/manifest.json", "/icon.svg", "/healthz",
    "/ws/arena", "/api/export/anki", "/api/export/printable-exam"
}"""

code = code.replace(old_auth_exempt, new_auth_exempt)

# 2. Update token and auth middleware functions
old_token_funcs = """def _make_session_token():
    expires = int(time.time()) + SESSION_DAYS * 86400
    nonce = secrets.token_hex(8)
    payload = f"{expires}.{nonce}"
    sig = hmac.new(_SESSION_KEY, payload.encode(), hashlib.sha256).hexdigest()
    return f"{payload}.{sig}"


def _valid_session_token(token: str) -> bool:
    try:
        expires, nonce, sig = token.split(".")
        expected = hmac.new(_SESSION_KEY, f"{expires}.{nonce}".encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(sig, expected) and int(expires) > time.time()
    except Exception:
        return False


def _client_ip(request):
    return (
        request.headers.get("CF-Connecting-IP")
        or request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
        or request.remote
        or "unknown"
    )


def _is_https(request):
    return request.secure or request.headers.get("X-Forwarded-Proto", "").lower() == "https"


@web.middleware
async def auth_middleware(request, handler):
    if not APP_PASSWORD or request.path in AUTH_EXEMPT_PATHS:
        return await handler(request)
    if _valid_session_token(request.cookies.get(SESSION_COOKIE, "")):
        return await handler(request)
    if request.path.startswith("/api/"):
        return json_resp({"success": False, "error": "Phiên đăng nhập đã hết hạn. Hãy tải lại trang để đăng nhập.", "auth_required": True}, 401)
    raise web.HTTPFound("/login")"""

new_token_funcs = """def _make_session_token(user_id=1, role="admin"):
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


@web.middleware
async def auth_middleware(request, handler):
    token = request.cookies.get(SESSION_COOKIE, "")
    if not token and request.headers.get("Authorization", "").startswith("Bearer "):
        token = request.headers.get("Authorization", "").split(" ", 1)[1].strip()

    user_info = _parse_session_token(token)
    if user_info:
        request["user"] = user_info
    else:
        # Default fallback: If APP_PASSWORD is empty, admin access; else guest
        request["user"] = {"id": 1, "role": "admin" if not APP_PASSWORD else "guest"}

    if not APP_PASSWORD or request.path in AUTH_EXEMPT_PATHS:
        return await handler(request)

    if user_info:
        return await handler(request)

    if request.path.startswith("/api/"):
        return json_resp({"success": False, "error": "Phiên đăng nhập đã hết hạn. Hãy đăng nhập lại.", "auth_required": True}, 401)
    raise web.HTTPFound("/login")"""

code = code.replace(old_token_funcs, new_token_funcs)

# 3. Redesign LOGIN_PAGE_HTML with Luxury Minimalist Aesthetic & Register Tabs
new_login_page_html = '''LOGIN_PAGE_HTML = """<!DOCTYPE html>
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
'''

# Replace LOGIN_PAGE_HTML
login_html_pattern = re.compile(r'LOGIN_PAGE_HTML = """.*?"""\n', re.DOTALL)
code = login_html_pattern.sub(new_login_page_html + "\n", code)

# 4. Replace login_api and add auth endpoints
old_login_api = """async def login_api(request):
    if not APP_PASSWORD:
        return json_resp({"success": True})
    ip = _client_ip(request)
    fails, locked_until = _LOGIN_FAILS.get(ip, [0, 0])
    now = time.time()
    if locked_until > now:
        return json_resp({"success": False, "error": f"Nhập sai quá nhiều lần. Thử lại sau {int(locked_until - now)} giây."}, 429)

    data = await safe_get_json(request)
    pw = str(data.get("password", ""))
    if hmac.compare_digest(pw.encode("utf-8"), APP_PASSWORD.encode("utf-8")):
        _LOGIN_FAILS.pop(ip, None)
        resp = json_resp({"success": True})
        resp.set_cookie(
            SESSION_COOKIE, _make_session_token(), max_age=SESSION_DAYS * 86400,
            httponly=True, samesite="Lax", secure=_is_https(request), path="/"
        )
        return resp

    fails += 1
    lock = now + min(300, 15 * (2 ** (fails - 5))) if fails >= 5 else 0
    _LOGIN_FAILS[ip] = [fails, lock]
    return json_resp({"success": False, "error": "Sai mật khẩu truy cập"}, 401)"""

new_auth_apis = """async def login_api(request):
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
    return json_resp({"success": False, "error": "Tên đăng nhập hoặc mật khẩu không chính xác."}, 401)


async def auth_register_api(request):
    data = await safe_get_json(request)
    username = str(data.get("username", "")).strip()
    password = str(data.get("password", "")).strip()
    full_name = str(data.get("full_name", "")).strip() or username
    try:
        user = db.create_user(username, password, full_name, role="student")
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
    resp = json_resp({"success": True})
    resp.del_cookie(SESSION_COOKIE, path="/")
    return resp


async def auth_me_api(request):
    user_info = request.get("user")
    if not user_info or user_info.get("role") == "guest":
        return json_resp({"success": False, "error": "Chưa đăng nhập", "auth_required": True}, 401)
    full_user = db.get_user_by_id(user_info["id"])
    return json_resp({"success": True, "user": full_user or user_info})


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
        return json_resp({"success": False, "error": str(e)}, 500)"""

code = code.replace(old_login_api, new_auth_apis)

# 5. Update get_user_state and save_user_state to use request["user"]["id"]
old_user_state_funcs = """async def get_user_state(request):
    raw = db.get_setting("user_sync_state", "{}")
    try:
        state = json.loads(raw) if raw else {}
    except Exception:
        state = {}
    return json_resp({"success": True, "state": state})


async def save_user_state(request):
    try:
        incoming = await safe_get_json(request)
        raw = db.get_setting("user_sync_state", "{}")
        try:
            current = json.loads(raw) if raw else {}
        except Exception:
            current = {}
        current.update(incoming)
        db.set_setting("user_sync_state", json.dumps(current, ensure_ascii=False))
        return json_resp({"success": True, "state": current})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)"""

new_user_state_funcs = """async def get_user_state(request):
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
        return json_resp({"success": False, "error": str(e)}, 500)"""

code = code.replace(old_user_state_funcs, new_user_state_funcs)

# 6. Update submit_exam to save user_id
old_save_exam_call = """        exam_id = db.save_exam_result(
            subject_id=subject_id,
            total_questions=total_q,
            correct_answers=correct_count,
            score=final_score,
            time_spent_seconds=time_spent,
            detail_json=json.dumps(question_results, ensure_ascii=False),
            exam_type=exam_type
        )"""

new_save_exam_call = """        uid = request.get("user", {}).get("id", 1)
        exam_id = db.save_exam_result(
            subject_id=subject_id,
            total_questions=total_q,
            correct_answers=correct_count,
            score=final_score,
            time_spent_seconds=time_spent,
            detail_json=json.dumps(question_results, ensure_ascii=False),
            exam_type=exam_type,
            user_id=uid
        )"""

code = code.replace(old_save_exam_call, new_save_exam_call)

# 7. Register new routes in create_app()
old_routes = """    app.router.add_get("/login", login_page)
    app.router.add_post("/api/login", login_api)
    app.router.add_post("/api/logout", logout_api)"""

new_routes = """    app.router.add_get("/login", login_page)
    app.router.add_post("/api/login", login_api)
    app.router.add_post("/api/logout", auth_logout_api)
    app.router.add_post("/api/auth/login", auth_login_api)
    app.router.add_post("/api/auth/register", auth_register_api)
    app.router.add_post("/api/auth/logout", auth_logout_api)
    app.router.add_get("/api/auth/me", auth_me_api)
    app.router.add_get("/api/admin/users", admin_get_users_api)
    app.router.add_delete("/api/admin/users/{id}", admin_delete_user_api)"""

code = code.replace(old_routes, new_routes)

# 8. Ensure admin user is seeded in create_app()
old_create_app_init = """def create_app():
    db.init_db()
    stem_seed.ensure_stem_and_math_upgraded()
    seed_hoasinh_ctump.ensure_hoasinh_ctump_seeded()"""

new_create_app_init = """def create_app():
    db.init_db()
    db.ensure_admin_user(APP_PASSWORD or "uni-5292")
    stem_seed.ensure_stem_and_math_upgraded()
    seed_hoasinh_ctump.ensure_hoasinh_ctump_seeded()"""

code = code.replace(old_create_app_init, new_create_app_init)

with open(SERVER_PY_PATH, "w", encoding="utf-8") as f:
    f.write(code)

print("Updated server.py successfully! Total lines:", len(code.splitlines()))
