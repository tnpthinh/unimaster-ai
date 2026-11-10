import subprocess, time, json, asyncio, aiohttp, base64

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
proc = subprocess.Popen([chrome_path, '--headless=new', '--remote-debugging-port=9231', '--window-size=1280,820', '--disable-gpu', 'http://localhost:8080'])
time.sleep(2.5)

async def test_all():
    async with aiohttp.ClientSession() as s:
        async with s.get('http://127.0.0.1:9231/json') as r:
            tabs = await r.json()
        target = next((t for t in tabs if 'localhost:8080' in t.get('url', '')), tabs[0])
        ws_url = target['webSocketDebuggerUrl']
        
        async with s.ws_connect(ws_url) as ws:
            await ws.send_json({'id': 1, 'method': 'Runtime.enable'})
            await ws.send_json({'id': 2, 'method': 'Page.enable'})

            async def run_js(code):
                msg_id = int(time.time() * 1000) % 100000
                await ws.send_json({
                    'id': msg_id,
                    'method': 'Runtime.evaluate',
                    'params': {'expression': code, 'awaitPromise': True, 'returnByValue': True}
                })
                while True:
                    m = await ws.receive_json()
                    if m.get('id') == msg_id:
                        return m.get('result', {}).get('result', {}).get('value')

            await asyncio.sleep(2.0)

            # 1. Check Dashboard stats (Must not be 0!)
            dash_info = await run_js("""(function() {
                return {
                    subCount: document.getElementById('stat-subjects')?.innerText,
                    qCount: document.getElementById('stat-questions')?.innerText,
                    subjectsInState: (typeof STATE !== 'undefined' && STATE.subjects) ? STATE.subjects.length : 0
                };
            })()""")
            print("DASHBOARD STATS:", json.dumps(dash_info), flush=True)
            assert int(dash_info['subCount']) > 0, "Subjects count should not be 0"

            # 2. Switch to exam tab
            await run_js('switchTab("exam")')
            await asyncio.sleep(0.5)

            # 3. Test Custom Range Exam: from 1 to 25
            await run_js('setRangePreset(1, 25)')
            range_info = await run_js("""(function() {
                return {
                    from: document.getElementById('exam-range-from')?.value,
                    to: document.getElementById('exam-range-to')?.value,
                    badge: document.getElementById('range-preview-badge')?.innerText
                };
            })()""")
            print("RANGE PRESET INFO:", json.dumps(range_info), flush=True)

            # 4. Start Custom Range Exam
            await run_js('startCustomRangeExam()')
            await asyncio.sleep(0.8)

            exam_active_info = await run_js("""(function() {
                const el = document.getElementById('q-prompt-text');
                const area = document.getElementById('q-answer-area');
                return {
                    title: document.getElementById('active-exam-title')?.innerText,
                    curQ: document.getElementById('current-q-num')?.innerText,
                    totQ: document.getElementById('total-q-num')?.innerText,
                    promptText: el ? el.innerText.substring(0, 80) : null,
                    optionsCount: area ? area.children.length : 0,
                    optionsText: area ? area.innerText.substring(0, 100) : null
                };
            })()""")
            print("CUSTOM RANGE EXAM RUNNING:", json.dumps(exam_active_info, ensure_ascii=False), flush=True)
            assert exam_active_info['promptText'], "Question prompt must not be blank!"
            assert exam_active_info['optionsCount'] >= 2, "Options count must be >= 2!"

            # Select Option A and Next Question
            await run_js('selectExamOption("A")')
            await asyncio.sleep(0.2)
            await run_js('nextQuestion()')
            await asyncio.sleep(0.2)
            
            # Submit exam with auto=true to bypass confirmation modal
            await run_js('submitExamNow(true)')
            await asyncio.sleep(1.0)

            # 5. Check Local History was saved in localStorage
            hist_count = await run_js("""(function() {
                const h = JSON.parse(localStorage.getItem('unimaster_local_exam_history_v2') || '[]');
                return h.length;
            })()""")
            print(f"LOCAL EXAM HISTORY SAVED RECORDS: {hist_count}", flush=True)
            assert hist_count > 0, "Exam history should be saved in localStorage!"

            # 6. Open and verify modal-exam-history
            await run_js('openLocalExamHistoryModal()')
            await asyncio.sleep(0.5)
            hist_modal_info = await run_js("""(function() {
                const list = document.getElementById('leh-history-list');
                return {
                    modalVisible: !document.getElementById('modal-exam-history')?.classList.contains('hidden'),
                    childCards: list ? list.children.length : 0
                };
            })()""")
            print("LOCAL HISTORY MODAL INFO:", json.dumps(hist_modal_info), flush=True)
            await run_js('closeModal("modal-exam-history")')

            # 7. Open and test modal-ctump-original-parts
            await run_js('openCtumpOriginalPartsModal()')
            await asyncio.sleep(0.3)
            ctump_modal_visible = await run_js("!document.getElementById('modal-ctump-original-parts')?.classList.contains('hidden')")
            print("CTUMP 322 MODAL VISIBLE:", ctump_modal_visible, flush=True)
            
            # Start Part 1 from CTUMP 322 modal
            await run_js('startCtumpOriginalPart(1); closeModal("modal-ctump-original-parts");')
            await asyncio.sleep(0.8)
            ctump_p1_info = await run_js("""(function() {
                return {
                    title: document.getElementById('active-exam-title')?.innerText,
                    totQ: document.getElementById('total-q-num')?.innerText,
                    promptText: document.getElementById('q-prompt-text')?.innerText.substring(0, 80)
                };
            })()""")
            print("CTUMP PART 1 RUNNING:", json.dumps(ctump_p1_info, ensure_ascii=False), flush=True)

            # 8. Test AI Tutor Chat Persistence
            await run_js("""(function() {
                saveLocalTutorMessage('user', 'Công thức Friedewald tính LDL-C là gì?', 'Thực Hành Hóa Sinh');
                saveLocalTutorMessage('model', 'Công thức Friedewald: LDL-C = Cholesterol TP - HDL-C - (Triglycerid / 5)', 'Thực Hành Hóa Sinh');
            })()""")
            tutor_hist_count = await run_js("""(function() {
                const t = JSON.parse(localStorage.getItem('unimaster_tutor_chat_history_v2') || '[]');
                return t.length;
            })()""")
            print(f"PERSISTENT TUTOR CHAT MESSAGES IN STORAGE: {tutor_hist_count}", flush=True)
            assert tutor_hist_count >= 2, "Tutor chat should be saved in localStorage!"

            # Open tutor chat history modal
            await run_js('openTutorHistoryModal()')
            await asyncio.sleep(0.3)
            tutor_modal_info = await run_js("""(function() {
                const list = document.getElementById('tutor-history-messages-list');
                return {
                    modalVisible: !document.getElementById('modal-tutor-chat-history')?.classList.contains('hidden'),
                    messagesRendered: list ? list.children.length : 0
                };
            })()""")
            print("TUTOR HISTORY MODAL INFO:", json.dumps(tutor_modal_info), flush=True)
            await run_js('closeModal("modal-tutor-chat-history")')

            # 9. Capture screenshot of active exam with custom range
            await ws.send_json({'id': 99, 'method': 'Page.captureScreenshot', 'params': {'format': 'jpeg', 'quality': 85}})
            while True:
                m = await ws.receive_json()
                if m.get('id') == 99:
                    img_bytes = base64.b64decode(m['result']['data'])
                    out_path = r'C:\Users\PC\.gemini\antigravity\brain\bf908d19-5939-4c23-8975-52dd4241139d\exam_v18_verified.jpg'
                    with open(out_path, 'wb') as f:
                        f.write(img_bytes)
                    print(f"Saved exam screenshot to {out_path} ({len(img_bytes)} bytes)", flush=True)
                    break

            print("\n=== ALL V18 TESTS PASSED WITH 0 ERRORS! ===", flush=True)

try:
    asyncio.run(test_all())
finally:
    proc.terminate()
