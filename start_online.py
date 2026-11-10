r"""
UniMaster AI Pro v9.0 — Trình Khởi Chạy Online Cố Định & Bền Vững (Persistent Tunnel + Fixed Gateway)
- GIỮ NGUYÊN ĐỊA CHỈ WEBSITE: Nếu đường truyền Cloudflare đang chạy khỏe, tuyệt đối KHÔNG khởi động lại hay đổi link mới!
- Chạy nền độc lập (Detached Background Service trên Windows): Không bị tắt khi đóng cửa sổ Terminal hay khởi động lại phiên làm việc.
- Tự động đồng bộ địa chỉ lên Cổng Truy Cập Cố Định Vĩnh Viễn: https://ntfy.sh/unimaster_ctump_5292
- Hỗ trợ Cloudflare Named Tunnel cố định (nếu có mã trong cloudflare_token.txt).
"""
import json
import os
import re
import secrets
import subprocess
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.join(ROOT, "tools")
CLOUDFLARED_EXE = os.path.join(TOOLS_DIR, "cloudflared.exe")
CLOUDFLARED_URL = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
PASSWORD_FILE = os.path.join(ROOT, "online_password.txt")
TUNNEL_JSON = os.path.join(ROOT, "online_tunnel.json")
PIDS_JSON = os.path.join(ROOT, "online_pids.json")
CF_TOKEN_FILE = os.path.join(ROOT, "cloudflare_token.txt")
CF_LOG_FILE = os.path.join(ROOT, "cloudflared.log")
SRV_LOG_FILE = os.path.join(ROOT, "server.log")
PERMANENT_GATEWAY_TOPIC = "unimaster_ctump_5292"
PERMANENT_GATEWAY_URL = f"https://ntfy.sh/{PERMANENT_GATEWAY_TOPIC}"
PORT = int(os.environ.get("PORT", "8080"))


def ensure_password() -> str:
    env_pw = os.environ.get("APP_PASSWORD", "").strip()
    if env_pw:
        return env_pw
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, encoding="utf-8") as f:
            pw = f.read().strip()
        if pw:
            return pw
    pw = f"uni-{secrets.randbelow(9000) + 1000}"
    with open(PASSWORD_FILE, "w", encoding="utf-8") as f:
        f.write(pw + "\n")
    return pw


def ensure_cloudflared():
    if os.path.exists(CLOUDFLARED_EXE) and os.path.getsize(CLOUDFLARED_EXE) > 5_000_000:
        return
    os.makedirs(TOOLS_DIR, exist_ok=True)
    print("⏳ Đang tải công cụ kết nối HTTPS Cloudflare chính thức (~35MB)...")
    tmp_path = CLOUDFLARED_EXE + ".part"
    req = urllib.request.Request(CLOUDFLARED_URL, headers={"User-Agent": "UniMaster-AI/9.0"})
    with urllib.request.urlopen(req, timeout=120) as resp, open(tmp_path, "wb") as out:
        while True:
            chunk = resp.read(256 * 1024)
            if not chunk:
                break
            out.write(chunk)
    if os.path.exists(CLOUDFLARED_EXE):
        os.remove(CLOUDFLARED_EXE)
    os.replace(tmp_path, CLOUDFLARED_EXE)


def is_url_healthy(url: str, timeout_sec: float = 4.0) -> bool:
    if not url:
        return False
    try:
        check_url = url.rstrip("/") + "/healthz"
        req = urllib.request.Request(check_url, headers={"User-Agent": "UniMaster-HealthCheck/9.0"})
        with urllib.request.urlopen(req, timeout=timeout_sec) as r:
            return r.status == 200
    except Exception:
        return False


def get_existing_live_tunnel() -> str:
    """Return existing public_url if both local server and public tunnel are healthy."""
    if not os.path.exists(TUNNEL_JSON):
        return ""
    try:
        with open(TUNNEL_JSON, encoding="utf-8") as f:
            data = json.load(f)
        pub_url = (data.get("public_url") or "").strip()
        if pub_url and is_url_healthy(f"http://127.0.0.1:{PORT}", 2.0) and is_url_healthy(pub_url, 5.0):
            return pub_url
    except Exception:
        pass
    return ""


def publish_to_permanent_gateway(pub_url: str, pw: str):
    """Publish the live tunnel URL to the permanent fixed ntfy.sh channel so bookmarks never break."""
    try:
        payload = json.dumps({
            "url": pub_url,
            "password": pw,
            "updated_at": int(time.time()),
            "app": "UniMaster AI Pro v9.0"
        })
        req = urllib.request.Request(
            PERMANENT_GATEWAY_URL,
            data=payload.encode("utf-8"),
            headers={
                "Title": "UniMaster AI Pro Online (Bam de mo ngay)",
                "Click": pub_url,
                "Actions": f"view, Mo UniMaster AI Pro ({pw}), {pub_url}, clear=true",
                "Tags": "mortar_board,rocket",
            },
            method="POST",
        )
        urllib.request.urlopen(req, timeout=6).read()
    except Exception:
        pass


def write_permanent_html_launcher(pub_url: str, pw: str):
    """Generate Vao_UniMaster_Co_Dinh.html which always auto-redirects to the latest live tunnel."""
    launcher_path = os.path.join(ROOT, "Vao_UniMaster_Co_Dinh.html")
    html = f"""<!DOCTYPE html>
<html lang="vi" class="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Cổng Truy Cập Cố Định • UniMaster AI Pro</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      min-height: 100vh; display: flex; align-items: center; justify-content: center;
      padding: 20px; background: #000000; color: #f4f4f5;
      font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
      background-image: radial-gradient(circle at 20% 20%, rgba(124,58,237,0.28), transparent 45%),
                        radial-gradient(circle at 80% 80%, rgba(16,185,129,0.22), transparent 45%);
    }}
    .card {{
      width: 100%; max-width: 440px; background: #0b0b10; border: 1px solid #27272a;
      border-radius: 24px; padding: 32px 26px; text-align: center;
      box-shadow: 0 28px 70px rgba(0,0,0,0.65);
    }}
    .logo {{
      width: 60px; height: 60px; border-radius: 18px; margin: 0 auto 16px;
      display: flex; align-items: center; justify-content: center; font-size: 28px;
      background: linear-gradient(135deg, #7c3aed, #ec4899); color: #fff; font-weight: 900;
    }}
    h1 {{ font-size: 20px; font-weight: 800; margin-bottom: 8px; }}
    p {{ font-size: 13px; color: #a1a1aa; line-height: 1.55; margin-bottom: 20px; }}
    .btn {{
      display: block; width: 100%; padding: 14px; border-radius: 14px;
      background: linear-gradient(135deg, #7c3aed, #ec4899); color: #fff;
      font-weight: 800; font-size: 14px; text-decoration: none; margin-bottom: 12px;
    }}
    .pw-box {{
      padding: 10px 14px; border-radius: 12px; background: #18181b;
      border: 1px solid #3f3f46; font-size: 12px; color: #d4d4d8;
    }}
    code {{ color: #34d399; font-weight: 800; font-size: 14px; }}
  </style>
</head>
<body>
  <div class="card">
    <div class="logo">U</div>
    <h1>Đang Kết Nối UniMaster AI Pro...</h1>
    <p id="status-txt">Đang tự động tìm máy chủ HTTPS đang hoạt động và chuyển hướng tức thì...</p>
    <a id="direct-link" href="{pub_url}" class="btn">🚀 Bấm Vào Đây Nếu Chưa Tự Chuyển Trang</a>
    <div class="pw-box">Mật khẩu truy cập: <code>{pw}</code></div>
  </div>
  <script>
    const FALLBACK_URL = {json.dumps(pub_url)};
    const GATEWAY_JSON = "https://ntfy.sh/{PERMANENT_GATEWAY_TOPIC}/json?poll=1&since=72h";
    async function resolveAndRedirect() {{
      try {{
        const resp = await fetch(GATEWAY_JSON, {{ cache: "no-store" }});
        const text = await resp.text();
        const lines = text.trim().split("\\n").filter(Boolean);
        for (let i = lines.length - 1; i >= 0; i--) {{
          try {{
            const item = JSON.parse(lines[i]);
            if (item.Click && item.Click.startsWith("https://")) {{
              document.getElementById("direct-link").href = item.Click;
              window.location.replace(item.Click);
              return;
            }}
            const msg = JSON.parse(item.message || "{{}}");
            if (msg.url && msg.url.startsWith("https://")) {{
              document.getElementById("direct-link").href = msg.url;
              window.location.replace(msg.url);
              return;
            }}
          }} catch (_) {{}}
        }}
      }} catch (_) {{}}
      window.location.replace(FALLBACK_URL);
    }}
    resolveAndRedirect();
  </script>
</body>
</html>
"""
    with open(launcher_path, "w", encoding="utf-8") as f:
        f.write(html)


def start_detached_services(pw: str) -> str:
    """Start server.py and cloudflared.exe as detached background processes on Windows so they never die when shell exits."""
    creation_flags = 0
    if os.name == "nt":
        creation_flags = (
            getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0x00000200)
            | getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)
        )

    env = os.environ.copy()
    env["APP_PASSWORD"] = pw
    env["PORT"] = str(PORT)
    env["PYTHONIOENCODING"] = "utf-8"

    # 1. Start local server if not already healthy
    srv_pid = None
    if not is_url_healthy(f"http://127.0.0.1:{PORT}", 2.0):
        print(f"🚀 Đang khởi động máy chủ UniMaster AI Pro chạy nền tại cổng {PORT}...")
        srv_log = open(SRV_LOG_FILE, "a", encoding="utf-8", errors="replace")
        srv_proc = subprocess.Popen(
            [sys.executable, os.path.join(ROOT, "server.py")],
            cwd=ROOT,
            env=env,
            stdout=srv_log,
            stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL,
            creationflags=creation_flags,
            close_fds=True,
        )
        srv_pid = srv_proc.pid

        deadline = time.time() + 20.0
        while time.time() < deadline:
            if is_url_healthy(f"http://127.0.0.1:{PORT}", 1.5):
                break
            time.sleep(0.35)

    if not is_url_healthy(f"http://127.0.0.1:{PORT}", 2.0):
        print("❌ Không thể khởi động máy chủ tại cổng 8080.")
        sys.exit(1)

    # Nếu đường hầm cloudflared cũ vẫn đang sống, giữ nguyên URL cũ sau khi khởi động lại server.py!
    existing_after_srv = get_existing_live_tunnel()
    if existing_after_srv:
        write_permanent_html_launcher(existing_after_srv, pw)
        publish_to_permanent_gateway(existing_after_srv, pw)
        return existing_after_srv

    # 2. Start cloudflared tunnel in background and capture its URL from cloudflared.log
    print("🌐 Đang thiết lập đường truyền HTTPS cố định suốt phiên chạy máy...")
    if os.path.exists(CF_LOG_FILE):
        try:
            os.remove(CF_LOG_FILE)
        except OSError:
            pass

    cf_log = open(CF_LOG_FILE, "w", encoding="utf-8", errors="replace")
    cf_cmd = [CLOUDFLARED_EXE, "tunnel", "--url", f"http://127.0.0.1:{PORT}", "--no-autoupdate"]
    if os.path.exists(CF_TOKEN_FILE):
        token = open(CF_TOKEN_FILE, encoding="utf-8").read().strip()
        if token:
            cf_cmd = [CLOUDFLARED_EXE, "tunnel", "--no-autoupdate", "run", "--token", token]

    cf_proc = subprocess.Popen(
        cf_cmd,
        cwd=ROOT,
        stdout=cf_log,
        stderr=subprocess.STDOUT,
        stdin=subprocess.DEVNULL,
        creationflags=creation_flags,
        close_fds=True,
    )

    url_pattern = re.compile(r"https://[a-z0-9-]+\.trycloudflare\.com", re.IGNORECASE)
    pub_url = ""
    deadline = time.time() + 25.0
    while time.time() < deadline:
        if os.path.exists(CF_LOG_FILE):
            try:
                content = open(CF_LOG_FILE, encoding="utf-8", errors="replace").read()
                m = url_pattern.search(content)
                if m:
                    pub_url = m.group(0)
                    break
            except Exception:
                pass
        time.sleep(0.4)

    if pub_url:
        with open(TUNNEL_JSON, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "public_url": pub_url,
                    "permanent_gateway_url": PERMANENT_GATEWAY_URL,
                    "updated_at": time.time(),
                },
                f,
                indent=2,
            )
        with open(PIDS_JSON, "w", encoding="utf-8") as f:
            json.dump({"server_pid": srv_pid, "cloudflared_pid": cf_proc.pid, "updated_at": time.time()}, f, indent=2)
        publish_to_permanent_gateway(pub_url, pw)
        write_permanent_html_launcher(pub_url, pw)

    return pub_url


def print_banner(pub_url: str, pw: str, reused: bool):
    print("\n" + "=" * 72)
    if reused:
        print("🔒 ĐỊA CHỈ WEBSITE ĐANG ĐƯỢC GIỮ NGUYÊN (KHÔNG ĐỔI LINK MỚI)!")
    else:
        print("🎉 HỆ THỐNG UNIMASTER AI PRO v9.0 ĐÃ ONLINE & CHẠY NỀN BỀN VỮNG!")
    print("=" * 72)
    print(f"🌍 1. Link HTTPS Trực Tiếp (Đã khóa cố định): {pub_url}")
    print(f"📌 2. Cổng Truy Cập Cố Định Vĩnh Viễn:        {PERMANENT_GATEWAY_URL}")
    print(f"      (Lưu link số 2 này vào dấu trang ĐT/iPad — không bao giờ đổi!)")
    print(f"🔐 3. Mật khẩu đăng nhập:                     {pw}")
    print(f"💻 4. Truy cập trên máy tính này:             http://localhost:{PORT}")
    print("=" * 72 + "\n")


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    pw = ensure_password()
    ensure_cloudflared()

    # Check if existing tunnel is already alive -> DO NOT CHANGE THE URL!
    existing_url = get_existing_live_tunnel()
    if existing_url:
        publish_to_permanent_gateway(existing_url, pw)
        write_permanent_html_launcher(existing_url, pw)
        print_banner(existing_url, pw, reused=True)
        return

    pub_url = start_detached_services(pw)
    if not pub_url:
        print("❌ Không lấy được địa chỉ Cloudflare Tunnel. Hãy kiểm tra kết nối mạng.")
        sys.exit(1)

    print_banner(pub_url, pw, reused=False)


if __name__ == "__main__":
    main()
