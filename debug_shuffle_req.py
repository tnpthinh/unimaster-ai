import urllib.request
import urllib.error
import json

with open(r'C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai\online_password.txt', 'r', encoding='utf-8') as f:
    APP_PASSWORD = f.read().strip()

# Login first
req = urllib.request.Request("http://127.0.0.1:8080/api/auth/login",
                             data=json.dumps({'username': 'admin', 'password': APP_PASSWORD}).encode('utf-8'),
                             headers={'Content-Type': 'application/json'})
with urllib.request.urlopen(req) as resp:
    token = json.loads(resp.read().decode('utf-8'))['token']

req2 = urllib.request.Request("http://127.0.0.1:8080/api/exam/shuffle?subject_id=5&count=10",
                              headers={'Authorization': f'Bearer {token}'})
try:
    with urllib.request.urlopen(req2) as resp:
        print("Success:", resp.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print(f"HTTPError {e.code}:")
    print(e.read().decode('utf-8'))
