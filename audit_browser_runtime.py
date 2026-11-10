import subprocess, time, json, asyncio, aiohttp

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
proc = subprocess.Popen([chrome_path, '--headless=new', '--remote-debugging-port=9238', '--window-size=1280,850', '--disable-gpu', 'http://localhost:8080'])
time.sleep(2.5)

async def audit_browser():
    async with aiohttp.ClientSession() as s:
        async with s.get('http://127.0.0.1:9238/json') as r:
            tabs = await r.json()
        target = next((t for t in tabs if 'localhost:8080' in t.get('url', '')), tabs[0])
        ws_url = target['webSocketDebuggerUrl']
        
        async with s.ws_connect(ws_url) as ws:
            await ws.send_json({'id': 1, 'method': 'Runtime.enable'})
            await ws.send_json({'id': 2, 'method': 'Page.enable'})
            await ws.send_json({'id': 3, 'method': 'Console.enable'})

            errors = []

            async def handle_msg():
                while True:
                    m = await ws.receive_json()
                    if m.get('method') == 'Runtime.exceptionThrown':
                        details = m.get('params', {}).get('exceptionDetails', {})
                        text = details.get('text', '')
                        exc = details.get('exception', {}).get('description', '')
                        errors.append(f"EXCEPTION: {text} - {exc}")
                    elif m.get('method') == 'Console.messageAdded':
                        msg = m.get('params', {}).get('message', {})
                        if msg.get('level') == 'error':
                            errors.append(f"CONSOLE ERROR: {msg.get('text')}")
                    elif 'id' in m and m['id'] > 100:
                        return m.get('result', {}).get('result', {}).get('value')

            async def run_js(code, mid):
                await ws.send_json({
                    'id': mid,
                    'method': 'Runtime.evaluate',
                    'params': {'expression': code, 'awaitPromise': True, 'returnByValue': True}
                })
                return await handle_msg()

            await asyncio.sleep(2.0)

            # Test tab switching across ALL tabs
            tabs_to_test = ['dashboard', 'exam', 'exercises', 'essay', 'flashcards', 'lab', 'tutor', 'arena']
            for i, tab in enumerate(tabs_to_test):
                print(f"Testing tab: {tab}...")
                await run_js(f"switchTab('{tab}')", 200 + i)
                await asyncio.sleep(0.3)

            # Test opening all modals
            modals_to_test = [
                'modal-settings',
                'modal-account-profile',
                'modal-account-subjects',
                'modal-exam-history',
                'modal-tutor-chat-history',
                'modal-stem-reference',
                'modal-subject-picker',
                'modal-offline-qr'
            ]
            for j, modal in enumerate(modals_to_test):
                print(f"Testing modal: {modal}...")
                await run_js(f"openModal('{modal}')", 300 + j)
                await asyncio.sleep(0.2)
                await run_js(f"closeModal('{modal}')", 400 + j)
                await asyncio.sleep(0.1)

            print("\n=== RUNTIME ERRORS CAPTURED ===")
            for err in errors:
                print("❌", err)
            print(f"Total runtime errors: {len(errors)}")

asyncio.run(audit_browser())
proc.terminate()
