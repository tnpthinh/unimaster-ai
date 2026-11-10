import subprocess, time, json, asyncio, aiohttp, base64

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
proc = subprocess.Popen([chrome_path, '--headless=new', '--remote-debugging-port=9255', '--window-size=1280,850', '--disable-gpu', 'http://localhost:8080'])
time.sleep(3.0)

async def test_v22():
    async with aiohttp.ClientSession() as s:
        async with s.get('http://127.0.0.1:9255/json') as r:
            tabs = await r.json()
        target = next((t for t in tabs if 'localhost:8080' in t.get('url', '')), None)
        if not target:
            print("ERROR: localhost:8080 tab not found!")
            return
        ws_url = target['webSocketDebuggerUrl']
        
        async with s.ws_connect(ws_url) as ws:
            await ws.send_json({'id': 1, 'method': 'Runtime.enable'})
            await ws.send_json({'id': 2, 'method': 'Page.enable'})
            await ws.send_json({'id': 3, 'method': 'Network.enable'})
            await ws.send_json({'id': 4, 'method': 'Network.clearBrowserCache'})
            await ws.send_json({'id': 5, 'method': 'Page.reload', 'params': {'ignoreCache': True}})
            await asyncio.sleep(2.5)

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

            # 1. Header & Settings Button Check
            header_check = await eval_js("""(() => {
                const settingsBtn = document.querySelector('header button[onclick*="openSettingsModal"]');
                const rect = settingsBtn ? settingsBtn.getBoundingClientRect() : null;
                return {
                    found: !!settingsBtn,
                    rect: rect ? { left: rect.left, right: rect.right, top: rect.top, width: rect.width } : null,
                    windowWidth: window.innerWidth,
                    isFullyVisible: rect ? (rect.right <= window.innerWidth && rect.left >= 0) : false
                };
            })()""")
            print("1. Header Settings Button Visibility Check:", header_check)
            assert header_check['isFullyVisible'] is True, f"Settings button overflows! Rect: {header_check['rect']}"

            # 2. Floating AI Tutor Open & Clean Close Check
            await eval_js("openFloatingTutor()")
            await asyncio.sleep(0.3)
            open_state = await eval_js("!document.getElementById('floating-tutor-window')?.classList.contains('hidden')")
            print("2a. AI Tutor Opened successfully:", open_state)

            await eval_js("closeFloatingTutor()")
            await asyncio.sleep(0.3)
            close_state = await eval_js("""(() => {
                const win = document.getElementById('floating-tutor-window');
                const backdrop = document.getElementById('floating-tutor-backdrop');
                const container = document.getElementById('floating-tutor-container');
                return {
                    winHidden: win?.classList.contains('hidden'),
                    backdropHidden: backdrop?.classList.contains('hidden'),
                    containerExpandedRemoved: !container?.classList.contains('tutor-expanded-parent')
                };
            })()""")
            print("2b. AI Tutor Clean Close Check:", close_state)
            assert close_state['winHidden'] is True
            assert close_state['backdropHidden'] is True
            assert close_state['containerExpandedRemoved'] is True

            # 3. Exam Active Screen Navigation Buttons Check
            # Launch exam with 3 sample questions
            await eval_js("""(() => {
                const qs = [
                    { id: 101, question_text: 'Câu hỏi kiểm thử số 1: Công thức Friedewald là gì?', option_a: 'A. Đúng', option_b: 'B. Sai', option_c: 'C. Khác', option_d: 'D. Không rõ', correct_option: 'A', _effectiveCorrect: 'A', q_type: 'mcq' },
                    { id: 102, question_text: 'Câu hỏi kiểm thử số 2: Phản ứng Biuret đặc trưng cho liên kết nào?', option_a: 'A. Peptid', option_b: 'B. Ester', option_c: 'C. Glucosid', option_d: 'D. Phosphodiester', correct_option: 'A', _effectiveCorrect: 'A', q_type: 'mcq' }
                ];
                switchTab('exam'); launchExamWithQuestions(qs, 'practice');
            })()""")
            await asyncio.sleep(0.5)

            exam_nav_check = await eval_js("""(() => {
                const topNext = document.getElementById('top-btn-next-q');
                const topPrev = document.getElementById('top-btn-prev-q');
                const botNext = document.getElementById('btn-next-q');
                const botPrev = document.getElementById('btn-prev-q');
                return {
                    topNextVisible: !!topNext && !topNext.closest('.hidden'), hiddenAncestor: topNext?.closest('.hidden')?.id || topNext?.closest('.hidden')?.tagName,
                    topPrevDisabled: topPrev?.disabled,
                    botNextVisible: !!botNext && !botNext.closest('.hidden'), botHiddenParent: botNext?.closest('.hidden')?.id || botNext?.closest('.hidden')?.className,
                    qNum: document.getElementById('current-q-num')?.innerText
                };
            })()""")
            print("3a. Exam Navigation Buttons Check on Q1:", exam_nav_check)
            assert exam_nav_check['topNextVisible'] is True
            assert exam_nav_check['botNextVisible'] is True

            # Test option selection
            await eval_js("selectExamOption('A')")
            await asyncio.sleep(0.3)

            # Test Next Question
            await eval_js("nextQuestion()")
            await asyncio.sleep(0.3)
            q2_check = await eval_js("""({
                qNum: document.getElementById('current-q-num')?.innerText,
                topPrevDisabled: document.getElementById('top-btn-prev-q')?.disabled,
                topNextLabel: document.getElementById('top-btn-next-q')?.innerText
            })""")
            print("3b. Advanced to Q2 Check:", q2_check)
            assert q2_check['qNum'] == '2'
            assert q2_check['topPrevDisabled'] is False

            # Capture screenshot of exam screen with navigation
            await capture_screenshot(r'C:\Users\PC\.gemini\antigravity\brain\bf908d19-5939-4c23-8975-52dd4241139d\exam_v22_verified.jpg')

            # 4. Study Break Modal Check
            await eval_js("openModal('modal-study-break')")
            await asyncio.sleep(0.3)
            break_check = await eval_js("!document.getElementById('modal-study-break')?.classList.contains('hidden')")
            print("4. Study Break Modal Open Check:", break_check)
            assert break_check is True

            # Capture screenshot of study break modal
            await capture_screenshot(r'C:\Users\PC\.gemini\antigravity\brain\bf908d19-5939-4c23-8975-52dd4241139d\study_break_v22_verified.jpg')

            await eval_js("closeModal('modal-study-break')")

            print("\n🎉 ALL v22 VERIFICATIONS COMPLETED SUCCESSFULLY WITH 0 ERRORS!")

asyncio.run(test_v22())
proc.terminate()
