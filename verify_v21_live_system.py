import subprocess, time, json, asyncio, aiohttp, base64

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
proc = subprocess.Popen([chrome_path, '--headless=new', '--remote-debugging-port=9250', '--window-size=1280,850', '--disable-gpu', 'http://localhost:8080'])
time.sleep(3.0)

async def test_live():
    async with aiohttp.ClientSession() as s:
        async with s.get('http://127.0.0.1:9250/json') as r:
            tabs = await r.json()
        target = next((t for t in tabs if 'localhost:8080' in t.get('url', '')), None)
        if not target:
            print("ERROR: localhost:8080 tab not found!")
            return
        ws_url = target['webSocketDebuggerUrl']
        
        async with s.ws_connect(ws_url) as ws:
            await ws.send_json({'id': 1, 'method': 'Runtime.enable'})
            await ws.send_json({'id': 2, 'method': 'Page.enable'})

            async def eval_js(code):
                await ws.send_json({
                    'id': 100,
                    'method': 'Runtime.evaluate',
                    'params': {'expression': code, 'awaitPromise': True, 'returnByValue': True}
                })
                while True:
                    m = await ws.receive_json()
                    if m.get('id') == 100:
                        return m.get('result', {}).get('result', {}).get('value')

            async def capture_screenshot(filename):
                await ws.send_json({
                    'id': 200,
                    'method': 'Page.captureScreenshot',
                    'params': {'format': 'jpeg', 'quality': 90}
                })
                while True:
                    m = await ws.receive_json()
                    if m.get('id') == 200:
                        data = m.get('result', {}).get('data', '')
                        with open(filename, 'wb') as f:
                            f.write(base64.b64decode(data))
                        print(f"📸 Saved screenshot: {filename}")
                        break

            # 1. Check Dashboard Stats on fresh load
            stats = await eval_js("""({
                subjects: document.getElementById('stat-subjects')?.innerText,
                questions: document.getElementById('stat-questions')?.innerText,
                stateSubsLen: STATE?.subjects?.length
            })""")
            print("1. Dashboard Stats Verification:", stats)
            assert int(stats['subjects']) >= 10, f"Subjects stat too low: {stats['subjects']}"
            assert int(stats['questions'].replace(',', '')) >= 500, f"Questions stat too low: {stats['questions']}"

            # 2. Test switching to Light Theme
            await eval_js("setThemeMode('light')")
            await asyncio.sleep(0.5)

            # Check computed styles of deadline countdown card
            card_styles = await eval_js("""(() => {
                const card = document.querySelector('.border-rose-500\\\\/40');
                const title = card?.querySelector('.font-extrabold');
                const countdown = document.getElementById('countdown-15-11');
                const urgentTitle = document.getElementById('survival-urgent-title');
                return {
                    urgentTitleColor: urgentTitle ? window.getComputedStyle(urgentTitle).color : null,
                    cardTitleColor: title ? window.getComputedStyle(title).color : null,
                    countdownColor: countdown ? window.getComputedStyle(countdown).color : null,
                    cardBg: card ? window.getComputedStyle(card).backgroundColor : null
                };
            })()""")
            print("2. Light Mode Deadline Card Styles:", card_styles)

            # 3. Open Settings Modal in Light Mode and test scrollable height
            await eval_js("openModal('modal-settings')")
            await asyncio.sleep(0.5)
            modal_metrics = await eval_js("""(() => {
                const modal = document.getElementById('modal-settings');
                const card = modal?.querySelector('.uni-card');
                const body = modal?.querySelector('.overflow-y-auto');
                return {
                    modalVisible: !modal?.classList.contains('hidden'),
                    cardHeight: card?.offsetHeight,
                    windowHeight: window.innerHeight,
                    bodyScrollHeight: body?.scrollHeight,
                    bodyClientHeight: body?.clientHeight,
                    bodyCanScroll: body?.scrollHeight > body?.clientHeight
                };
            })()""")
            print("3. Modal Settings Metrics:", modal_metrics)
            assert modal_metrics['modalVisible'] is True, "Modal settings did not open"
            assert modal_metrics['bodyCanScroll'] is True, "Modal body is not scrollable"

            # Capture modal screenshot
            await capture_screenshot(r'C:\Users\PC\.gemini\antigravity\brain\bf908d19-5939-4c23-8975-52dd4241139d\modal_v21_verified.jpg')

            # Close modal
            await eval_js("closeModal('modal-settings')")
            await asyncio.sleep(0.3)

            # 4. Test backup handlers
            backup_test = await eval_js("""(() => {
                return {
                    exportFnExists: typeof exportFullBackup === 'function',
                    importFnExists: typeof triggerImportBackupModal === 'function',
                    askCodeFnExists: typeof askAiAboutSelectedCode === 'function'
                };
            })()""")
            print("4. New Functions Verification:", backup_test)
            assert backup_test['exportFnExists'] is True
            assert backup_test['importFnExists'] is True
            assert backup_test['askCodeFnExists'] is True

            # 5. Take dashboard screenshot in light mode
            await capture_screenshot(r'C:\Users\PC\.gemini\antigravity\brain\bf908d19-5939-4c23-8975-52dd4241139d\dashboard_v21_light_verified.jpg')

            # 6. Test tab switching across all tabs
            tabs = ['dashboard', 'exam', 'exercises', 'essay', 'flashcards', 'lab', 'tutor', 'arena']
            for t in tabs:
                await eval_js(f"switchTab('{t}')")
                await asyncio.sleep(0.2)
            await eval_js("switchTab('dashboard')")

            print("\n🎉 ALL TESTS PASSED WITH 100% SUCCESS!")

asyncio.run(test_live())
proc.terminate()
