import subprocess, time, json, asyncio, aiohttp

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
proc = subprocess.Popen([chrome_path, '--headless=new', '--remote-debugging-port=9225', '--disable-gpu', 'http://localhost:8080'])
time.sleep(2.5)

async def check():
    async with aiohttp.ClientSession() as s:
        async with s.get('http://127.0.0.1:9225/json') as r:
            tabs = await r.json()
        print('Available tabs:', [(t.get('title'), t.get('url')) for t in tabs])
        target = next((t for t in tabs if 'localhost:8080' in t.get('url', '')), tabs[0])
        print('Selected target:', target.get('title'), target.get('url'))
        ws_url = target['webSocketDebuggerUrl']
        async with s.ws_connect(ws_url) as ws:
            await ws.send_json({'id': 1, 'method': 'Runtime.enable'})
            await ws.send_json({'id': 2, 'method': 'Log.enable'})
            await ws.send_json({'id': 3, 'method': 'Page.enable'})
            await ws.send_json({'id': 4, 'method': 'Network.enable'})
            
            # Print page title and URL
            await ws.send_json({'id': 5, 'method': 'Runtime.evaluate', 'params': {'expression': 'window.location.href + " | " + document.title + " | scripts: " + Array.from(document.querySelectorAll("script")).map(s => s.src).join(", ")', 'returnByValue': True}})
            loc_resp = await ws.receive_json()
            print('=== PAGE INFO ===', loc_resp)
            
            exceptions = []
            console_logs = []
            
            async def drain_events():
                while True:
                    try:
                        msg = await asyncio.wait_for(ws.receive(), timeout=0.2)
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            data = json.loads(msg.data)
                            if data.get('method') == 'Runtime.exceptionThrown':
                                exceptions.append(data['params']['exceptionDetails'])
                            elif data.get('method') == 'Runtime.consoleAPICalled':
                                console_logs.append(data['params'])
                    except asyncio.TimeoutError:
                        break

            await asyncio.sleep(1.5)
            await drain_events()

            print('=== INITIAL EXCEPTIONS ===')
            for ex in exceptions:
                print(ex.get('text'), ex.get('exception', {}).get('description'))
            
            # Check dashboard stats
            await ws.send_json({
                'id': 10,
                'method': 'Runtime.evaluate',
                'params': {
                    'expression': 'JSON.stringify({subjectsLen: STATE ? STATE.subjects ? STATE.subjects.length : null : null, statSubjects: document.getElementById("stat-subjects") ? document.getElementById("stat-subjects").textContent : null, statQuestions: document.getElementById("stat-questions") ? document.getElementById("stat-questions").textContent : null})',
                    'returnByValue': True
                }
            })
            resp = await ws.receive_json()
            print('=== DASHBOARD STATS RAW ===', json.dumps(resp))

            # Trigger quickStartBai4Lipid
            await ws.send_json({
                'id': 20,
                'method': 'Runtime.evaluate',
                'params': {
                    'expression': 'quickStartBai4Lipid()',
                    'awaitPromise': True,
                    'returnByValue': True
                }
            })
            resp2 = await ws.receive_json()
            await asyncio.sleep(1.5)
            await drain_events()

            print('=== quickStartBai4Lipid EXCEPTIONS ===')
            for ex in exceptions:
                print(ex.get('text'), ex.get('exception', {}).get('description'))

            # Check exam elements
            await ws.send_json({
                'id': 30,
                'method': 'Runtime.evaluate',
                'params': {
                    'expression': 'JSON.stringify({prompt: document.getElementById("q-prompt-text") ? document.getElementById("q-prompt-text").innerHTML : null, answerArea: document.getElementById("q-answer-area") ? document.getElementById("q-answer-area").innerHTML.substring(0, 300) : null, examTitle: document.getElementById("active-exam-title") ? document.getElementById("active-exam-title").textContent : null, totalQ: STATE && STATE.exam && STATE.exam.questions ? STATE.exam.questions.length : null, currentQ: STATE && STATE.exam ? STATE.exam.currentIndex : null, qObj: STATE && STATE.exam && STATE.exam.questions ? STATE.exam.questions[0] : null})',
                    'returnByValue': True
                }
            })
            resp3 = await ws.receive_json()
            print('=== EXAM ELEMENTS RAW ===', json.dumps(resp3))

try:
    asyncio.run(check())
finally:
    proc.terminate()
