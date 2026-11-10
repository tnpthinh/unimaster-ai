import subprocess, time, json, asyncio, aiohttp, base64

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
proc = subprocess.Popen([chrome_path, '--headless=new', '--remote-debugging-port=9227', '--window-size=1280,800', '--disable-gpu', 'http://localhost:8080'])
time.sleep(2.5)

async def check():
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get('http://127.0.0.1:9227/json') as r:
                tabs = await r.json()
            target = tabs[0]
            ws_url = target['webSocketDebuggerUrl']
            async with s.ws_connect(ws_url) as ws:
                await ws.send_json({'id': 1, 'method': 'Runtime.enable'})
                await ws.send_json({'id': 2, 'method': 'Page.enable'})
                
                async def run_js(code):
                    msg_id = int(time.time() * 1000) % 100000
                    await ws.send_json({'id': msg_id, 'method': 'Runtime.evaluate', 'params': {'expression': code, 'awaitPromise': True, 'returnByValue': True}})
                    while True:
                        m = await ws.receive()
                        d = json.loads(m.data)
                        if d.get('id') == msg_id:
                            return d.get('result', {}).get('result', {}).get('value')

                await asyncio.sleep(2.0)
                await run_js('switchTab("exam")')
                await asyncio.sleep(0.5)
                await run_js('quickStartBai4Lipid()')
                await asyncio.sleep(1.0)
                
                js_code = """
                (function() {
                    const el = document.getElementById('q-prompt-text');
                    const area = document.getElementById('q-answer-area');
                    return {
                        promptText: el ? el.innerText : null,
                        promptRect: el ? {width: el.offsetWidth, height: el.offsetHeight} : null,
                        areaChildCount: area ? area.children.length : 0,
                        areaText: area ? area.innerText.substring(0, 100) : null,
                        qTitle: document.getElementById('active-exam-title') ? document.getElementById('active-exam-title').innerText : null,
                        curQ: document.getElementById('current-q-num') ? document.getElementById('current-q-num').innerText : null,
                        totQ: document.getElementById('total-q-num') ? document.getElementById('total-q-num').innerText : null
                    };
                })()
                """
                prompt_info = await run_js(js_code)
                print('EXAM INFO:', json.dumps(prompt_info, ensure_ascii=False, indent=2))
                
                await ws.send_json({'id': 99, 'method': 'Page.captureScreenshot', 'params': {'format': 'jpeg', 'quality': 85}})
                while True:
                    m = await ws.receive()
                    d = json.loads(m.data)
                    if d.get('id') == 99:
                        img_data = base64.b64decode(d['result']['data'])
                        out_path = r'C:\Users\PC\.gemini\antigravity\brain\bf908d19-5939-4c23-8975-52dd4241139d\exam_screen_check.jpg'
                        with open(out_path, 'wb') as f:
                            f.write(img_data)
                        print('Screenshot saved to:', out_path)
                        break
    except Exception as e:
        print('Exception:', e)

try:
    asyncio.run(check())
finally:
    proc.terminate()
