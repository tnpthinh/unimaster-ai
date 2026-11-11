r"""Cổng AI: cho phép Render (server cloud) gọi 9Router đang chạy trên máy bạn.

Luồng kết nối:
    Render  ->  Cloudflare Tunnel (HTTPS)  ->  proxy có X-Gateway-Secret  ->  9Router 127.0.0.1:20128

Vì sao cần proxy: 9Router mặc định KHÔNG có xác thực ở tầng mạng, nếu mở thẳng ra
Internet thì ai biết URL cũng dùng được toàn bộ tài khoản AI của bạn. Proxy chỉ cho
request đi qua khi có header X-Gateway-Secret.

Cách dùng:
    python start_ai_gateway.py            # chạy nền, in secret + hướng dẫn
    python start_ai_gateway.py --foreground  # chạy ngay tại cửa sổ này (để xem log)
    python start_ai_gateway.py --stop        # tắt gateway đang chạy nền

Secret lưu tại ai_gateway_secret.txt (đã gitignore). URL tunnel hiện tại lưu tại
ai_gateway_tunnel.json và được công bố lên ntfy để backend tự dò.
"""
import json
import os
import re
import secrets
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.join(ROOT, "tools")
CLOUDFLARED_EXE = os.path.join(TOOLS_DIR, "cloudflared.exe")
ROUTER_BASE_URL = os.environ.get("ROUTER_BASE_URL", "http://127.0.0.1:20128").rstrip("/")
GATEWAY_PORT = int(os.environ.get("AI_GATEWAY_PORT", "20129"))
SECRET_FILE = os.path.join(ROOT, "ai_gateway_secret.txt")
STATE_FILE = os.path.join(ROOT, "ai_gateway_tunnel.json")
PID_FILE = os.path.join(ROOT, "ai_gateway.pid")
LOG_FILE = os.path.join(ROOT, "ai_gateway_cloudflared.log")
APP_LOG_FILE = os.path.join(ROOT, "ai_gateway.log")
GATEWAY_TOPIC = "unimaster_ctump_5292"
PUBLISH_URL = f"https://ntfy.sh/{GATEWAY_TOPIC}"
DISCOVERY_URL = f"https://ntfy.sh/{GATEWAY_TOPIC}/json?poll=1&since=72h"
PYTHONW = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")


# ---------------------------------------------------------------- tiện ích chung
def ensure_secret() -> str:
    """Tạo secret một lần; file local này không bao giờ được commit lên Git."""
    if os.path.exists(SECRET_FILE):
        with open(SECRET_FILE, encoding="utf-8") as file:
            saved = file.read().strip()
        if saved:
            return saved
    value = secrets.token_urlsafe(32)
    with open(SECRET_FILE, "w", encoding="utf-8") as file:
        file.write(value + "\n")
    return value


def http_ok(url: str, timeout: float = 5.0) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            return response.status == 200
    except Exception:
        return False


def router_is_healthy() -> bool:
    return http_ok(f"{ROUTER_BASE_URL}/v1/models")


def gateway_is_healthy() -> bool:
    return http_ok(f"http://127.0.0.1:{GATEWAY_PORT}/healthz", 2.0)


def publish_gateway(public_url: str) -> None:
    """Đăng URL mới lên ntfy; URL không đủ để dùng vì còn cần secret."""
    payload = json.dumps({
        "gateway_url": public_url.rstrip("/") + "/v1",
        "updated_at": int(time.time()),
        "service": "UniMaster 9Router gateway",
    }).encode("utf-8")
    request = urllib.request.Request(
        PUBLISH_URL,
        data=payload,
        headers={"Title": "UniMaster AI Gateway", "Tags": "robot,lock"},
        method="POST",
    )
    try:
        urllib.request.urlopen(request, timeout=10).read()
    except Exception as exc:
        print(f"⚠ Không công bố được URL gateway lên ntfy: {exc}")


# ------------------------------------------------------------------- proxy server
class GatewayHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    gateway_secret = ""

    def log_message(self, fmt, *args):
        print(f"[AI Gateway] {self.client_address[0]} - {fmt % args}")

    def _send_json(self, status: int, payload: dict):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _forward(self):
        if self.headers.get("X-Gateway-Secret", "") != self.gateway_secret:
            self._send_json(403, {"error": "Gateway secret is invalid"})
            return
        try:
            content_length = int(self.headers.get("Content-Length", "0") or "0")
            body = self.rfile.read(content_length) if content_length else None
            skip = {"host", "connection", "x-gateway-secret", "content-length", "transfer-encoding"}
            headers = {key: value for key, value in self.headers.items() if key.lower() not in skip}
            if body is not None:
                headers["Content-Length"] = str(len(body))
            request = urllib.request.Request(
                ROUTER_BASE_URL + self.path,
                data=body,
                headers=headers,
                method=self.command,
            )
            with urllib.request.urlopen(request, timeout=150) as response:
                response_body = response.read()
                self.send_response(response.status)
                for key, value in response.headers.items():
                    if key.lower() not in {"connection", "transfer-encoding", "content-encoding", "content-length"}:
                        self.send_header(key, value)
                self.send_header("Content-Length", str(len(response_body)))
                self.end_headers()
                self.wfile.write(response_body)
        except urllib.error.HTTPError as error:
            response_body = error.read()
            self.send_response(error.code)
            self.send_header("Content-Type", error.headers.get("Content-Type", "application/json"))
            self.send_header("Content-Length", str(len(response_body)))
            self.end_headers()
            self.wfile.write(response_body)
        except Exception as exc:
            self._send_json(502, {"error": f"Local 9Router unavailable: {exc}"})

    def do_GET(self):
        if self.path.startswith("/healthz"):
            self._send_json(200, {"ok": True, "service": "unimaster-ai-gateway"})
            return
        self._forward()

    def do_POST(self):
        self._forward()


def start_proxy(secret: str) -> ThreadingHTTPServer:
    GatewayHandler.gateway_secret = secret
    server = ThreadingHTTPServer(("127.0.0.1", GATEWAY_PORT), GatewayHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


# ------------------------------------------------------------------ cloudflare tunnel
def start_tunnel() -> str:
    if not os.path.exists(CLOUDFLARED_EXE):
        raise RuntimeError(
            f"Không tìm thấy {CLOUDFLARED_EXE}. Hãy chạy start_online.py một lần để tải cloudflared."
        )
    log = open(LOG_FILE, "w", encoding="utf-8", errors="replace")
    creation_flags = 0
    if os.name == "nt":
        creation_flags = (
            getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0x00000200)
            | getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)
        )
    subprocess.Popen(
        [CLOUDFLARED_EXE, "tunnel", "--url", f"http://127.0.0.1:{GATEWAY_PORT}", "--no-autoupdate"],
        cwd=ROOT,
        stdout=log,
        stderr=subprocess.STDOUT,
        stdin=subprocess.DEVNULL,
        creationflags=creation_flags,
        close_fds=True,
    )
    pattern = re.compile(r"https://[a-z0-9-]+\.trycloudflare\.com", re.IGNORECASE)
    deadline = time.time() + 40
    while time.time() < deadline:
        try:
            content = open(LOG_FILE, encoding="utf-8", errors="replace").read()
            found = pattern.search(content)
            if found:
                return found.group(0)
        except FileNotFoundError:
            pass
        time.sleep(0.4)
    raise RuntimeError(f"Không lấy được URL Cloudflare. Xem log: {LOG_FILE}")


# --------------------------------------------------------------------------- chạy nền
def run_child() -> int:
    """Tiến trình nền thật sự: giữ proxy + tunnel sống tới khi bị tắt."""
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if gateway_is_healthy():
        print("Gateway đã chạy sẵn, không khởi động trùng.")
        return 0
    if not router_is_healthy():
        print(f"❌ 9Router chưa chạy tại {ROUTER_BASE_URL}. Hãy mở 9Router trước.")
        return 1
    secret = ensure_secret()
    start_proxy(secret)
    print(f"🔐 Proxy bảo vệ: http://127.0.0.1:{GATEWAY_PORT}")
    public_url = start_tunnel()
    publish_gateway(public_url)
    with open(STATE_FILE, "w", encoding="utf-8") as file:
        json.dump(
            {"public_url": public_url, "discovery_url": DISCOVERY_URL, "updated_at": time.time()},
            file,
            indent=2,
        )
    with open(PID_FILE, "w", encoding="utf-8") as file:
        file.write(str(os.getpid()))
    print(f"✅ Tunnel AI online: {public_url}")
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        return 0


def spawn_detached() -> int:
    """Windows: chạy lại chính script này bằng pythonw để không phụ thuộc cửa sổ terminal."""
    executable = PYTHONW if os.path.exists(PYTHONW) else sys.executable
    creation_flags = 0x00000008 | 0x00000200  # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
    log = open(APP_LOG_FILE, "a", encoding="utf-8", errors="replace")
    subprocess.Popen(
        [executable, os.path.abspath(__file__), "--child"],
        cwd=ROOT,
        stdout=log,
        stderr=subprocess.STDOUT,
        stdin=subprocess.DEVNULL,
        creationflags=creation_flags,
        close_fds=True,
    )
    deadline = time.time() + 45
    while time.time() < deadline:
        if gateway_is_healthy() and os.path.exists(STATE_FILE):
            try:
                state = json.load(open(STATE_FILE, encoding="utf-8"))
                if time.time() - float(state.get("updated_at", 0)) < 120:
                    return 0
            except Exception:
                pass
        time.sleep(0.5)
    print(f"⚠ Chưa xác nhận được gateway. Xem log: {APP_LOG_FILE}")
    return 1


def stop_gateway() -> int:
    stopped = False
    if os.path.exists(PID_FILE):
        try:
            pid = int(open(PID_FILE, encoding="utf-8").read().strip())
            subprocess.run(["taskkill", "/F", "/PID", str(pid)], capture_output=True)
            stopped = True
        except Exception:
            pass
        try:
            os.remove(PID_FILE)
        except OSError:
            pass
    # cloudflared của gateway dùng cổng GATEWAY_PORT: tắt tiến trình nào chứa cổng đó
    result = subprocess.run(
        ["powershell", "-NoProfile", "-Command",
         f"(Get-NetTCPConnection -LocalPort {GATEWAY_PORT} -ErrorAction SilentlyContinue)"
         f".OwningProcess | ForEach-Object {{ Stop-Process -Id $_ -Force }}"],
        capture_output=True,
    )
    if result.returncode == 0:
        stopped = True
    print("Đã tắt gateway." if stopped else "Không tìm thấy gateway đang chạy.")
    return 0


def print_banner(secret: str, state: dict):
    public_url = state.get("public_url", "")
    print("\n" + "=" * 74)
    print("🔗 CỔNG AI 9ROUTER ĐÃ SẴN SÀNG CHO RENDER")
    print("=" * 74)
    print(f"🌍 Tunnel công khai:  {public_url}")
    print(f"🛡  Proxy local:       http://127.0.0.1:{GATEWAY_PORT}  (bắt buộc secret)")
    print(f"🔐 Secret:            {secret}")
    print("-" * 74)
    print("Dán 2 biến này vào Render Dashboard > Environment:")
    print(f"   AI_GATEWAY_DISCOVERY_URL = {DISCOVERY_URL}")
    print(f"   AI_GATEWAY_SECRET        = {secret}")
    print("-" * 74)
    print("Trong UniMaster > Cài đặt AI, chọn:")
    print("   Base URL = http://127.0.0.1:20128/v1")
    print("   Model    = All  hoặc  Coding-Pro")
    print("   Key      = API key trong 9Router > API Keys (dạng sk-...)")
    print("=" * 74 + "\n")


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    args = set(sys.argv[1:])
    if "--stop" in args:
        return stop_gateway()
    if "--child" in args:
        return run_child()
    if not router_is_healthy():
        print(f"❌ 9Router chưa chạy tại {ROUTER_BASE_URL}. Hãy mở 9Router trước rồi chạy lại.")
        return 1

    if "--foreground" in args:
        return run_child()

    if not gateway_is_healthy():
        print("⏳ Đang khởi động gateway chạy nền (proxy + Cloudflare Tunnel)...")
        if spawn_detached() != 0:
            return 1
    else:
        print("ℹ Gateway đang chạy sẵn — bỏ qua bước khởi động.")

    secret = ensure_secret()
    try:
        state = json.load(open(STATE_FILE, encoding="utf-8"))
    except Exception:
        state = {}
    print_banner(secret, state)
    print(f"📄 Log: {APP_LOG_FILE} • {LOG_FILE}")
    print("Tắt khi cần: python start_ai_gateway.py --stop\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
