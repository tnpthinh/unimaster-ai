import subprocess, time, json, asyncio, aiohttp, base64

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
proc = subprocess.Popen([chrome_path, '--headless=new', '--remote-debugging-port=9225', '--window-size=1200,800', '--disable-gpu', 'http://localhost:8080'])
time.sleep(2)

async def take_shot():
    async with aiohttp.ClientSession() as s:
        async with s.get('http://127.0.0.1:9225/json') as r:
            tabs = await r.json()
        target = next((t for t in tabs if 'localhost:8080' in t.get('url', '')), tabs[0])
        ws_url = target['webSocketDebuggerUrl']
        async with s.ws_connect(ws_url) as ws:
            await ws.send_json({'id': 1, 'method': 'Runtime.enable'})
            await ws.send_json({'id': 2, 'method': 'Page.enable'})
            
            # Open modal
            await ws.send_json({
                'id': 10,
                'method': 'Runtime.evaluate',
                'params': {
                    'expression': 'openModal("modal-settings")',
                    'returnByValue': True
                }
            })
            await asyncio.sleep(0.5)
            
            # Capture screenshot
            await ws.send_json({
                'id': 20,
                'method': 'Page.captureScreenshot',
                'params': {'format': 'jpeg', 'quality': 90}
            })
            
            while True:
                resp = await ws.receive_json()
                if resp.get('id') == 20:
                    b64_data = resp['result']['data']
                    out_path = r'C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai\modal_verified.jpg'
                    with open(out_path, 'wb') as f:
                        f.write(base64.b64decode(b64_data))
                    print(f'Saved screenshot to {out_path} ({len(b64_data)} bytes)')
                    break

try:
    asyncio.run(take_shot())
finally:
    proc.terminate()
