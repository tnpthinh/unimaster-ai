import subprocess, time, json, asyncio, aiohttp

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
proc = subprocess.Popen([chrome_path, '--headless=new', '--remote-debugging-port=9225', '--disable-gpu', 'http://localhost:8080'])
time.sleep(2.5)

async def audit():
    async with aiohttp.ClientSession() as s:
        async with s.get('http://127.0.0.1:9225/json') as r:
            tabs = await r.json()
        target = next((t for t in tabs if 'localhost:8080' in t.get('url', '')), tabs[0])
        ws_url = target['webSocketDebuggerUrl']
        
        async with s.ws_connect(ws_url) as ws:
            await ws.send_json({'id': 1, 'method': 'Runtime.enable'})
            await ws.send_json({'id': 2, 'method': 'Log.enable'})
            await ws.send_json({'id': 3, 'method': 'Page.enable'})
            
            all_errors = []
            
            async def collect():
                while True:
                    try:
                        msg = await asyncio.wait_for(ws.receive(), timeout=0.25)
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            data = json.loads(msg.data)
                            if data.get('method') == 'Runtime.exceptionThrown':
                                details = data['params']['exceptionDetails']
                                err_desc = details.get('text', '') + ' | ' + details.get('exception', {}).get('description', '')
                                all_errors.append(err_desc)
                            elif data.get('method') == 'Log.entryAdded':
                                entry = data['params']['entry']
                                if entry.get('level') == 'error':
                                    all_errors.append(f"ConsoleError: {entry.get('text')}")
                    except asyncio.TimeoutError:
                        break

            await asyncio.sleep(1.5)
            await collect()
            
            async def run_js(code, desc):
                await ws.send_json({
                    'id': int(time.time() * 1000) % 100000,
                    'method': 'Runtime.evaluate',
                    'params': {'expression': code, 'awaitPromise': True, 'returnByValue': True}
                })
                await asyncio.sleep(0.3)
                await collect()

            # Test all tabs
            tabs = ['dashboard', 'exam', 'exercises', 'essay', 'flashcards', 'search', 'tutor', 'generator', 'arena', 'lab']
            for t in tabs:
                await run_js(f'switchTab("{t}")', f'Switch to {t}')

            # Switch back to exam and test operations
            await run_js('switchTab("exam")', 'Switch to exam')
            await run_js('quickStartBai4Lipid()', 'quickStartBai4Lipid')
            await run_js('toggleZenMode()', 'toggleZenMode ON')
            await run_js('toggleZenMode()', 'toggleZenMode OFF')
            await run_js('selectExamOption("A")', 'selectExamOption A')
            await run_js('nextQuestion()', 'nextQuestion')
            await run_js('prevQuestion()', 'prevQuestion')
            await run_js('toggleNoteBox()', 'toggleNoteBox')
            await run_js('toggleFloatingTutor()', 'toggleFloatingTutor')
            await run_js('toggleFloatingTutorSize()', 'toggleFloatingTutorSize')
            await run_js('toggleFloatingTutor()', 'close floating tutor')
            
            # Test switch back to dashboard
            await run_js('switchTab("dashboard")', 'Switch back to dashboard')
            
            # Test other features
            await run_js('openModal("modal-settings")', 'open modal-settings')
            await run_js('switchSettingsTab("ai")', 'switchSettingsTab ai')
            await run_js('closeModal("modal-settings")', 'close modal-settings')
            
            # Test exercises
            await run_js('switchTab("exercises")', 'switchTab exercises')
            await run_js('if (STATE.exercises && STATE.exercises.length) openExerciseDetail(STATE.exercises[0].id)', 'openExerciseDetail')

            # Test essay
            await run_js('switchTab("essay")', 'switchTab essay')
            await run_js('if (STATE.essayPrompts && STATE.essayPrompts.length) selectEssayPrompt(STATE.essayPrompts[0].id)', 'selectEssayPrompt')

            print('=== AUDIT FINISHED ===')
            print(f'Total errors caught: {len(all_errors)}')
            for err in set(all_errors):
                print('ERR:', err)

try:
    asyncio.run(audit())
finally:
    proc.terminate()
