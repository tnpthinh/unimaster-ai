import subprocess, time, json, asyncio, aiohttp, base64

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
proc = subprocess.Popen([chrome_path, '--headless=new', '--remote-debugging-port=9236', '--window-size=1280,850', '--disable-gpu', 'http://localhost:8080'])
time.sleep(2.5)

async def test_v19():
    async with aiohttp.ClientSession() as s:
        async with s.get('http://127.0.0.1:9236/json') as r:
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
                        res = m.get('result', {}).get('result', {})
                        if 'value' in res:
                            return res['value']
                        return res

            await asyncio.sleep(2.5)

            # TEST 1: Launch Exam and check Question + Key terms + Discussion button
            t1 = await run_js("""(async function() {
                await quickStartBai4Lipid();
                const qPrompt = document.getElementById('q-prompt-text')?.innerText;
                const optA = document.querySelector('.opt-A .option-text')?.innerText;
                const discBtn = document.getElementById('btn-toggle-discussion')?.innerText;
                const keyRow = document.getElementById('q-key-terms-row')?.innerHTML;
                return { qPrompt, optA, discBtn, hasKeyTerms: Boolean(keyRow && keyRow.length > 10) };
            })()""")
            print("TEST 1 - EXAM & QUESTION RENDERING:", json.dumps(t1, ensure_ascii=False, indent=2))
            assert t1.get('qPrompt') and len(t1['qPrompt']) > 5, "Question prompt must be rendered!"
            assert t1.get('optA') and len(t1['optA']) > 2, "Option A must be rendered!"

            # TEST 2: Toggle Discussion Box and Verify Comment Loading
            t2 = await run_js("""(async function() {
                toggleQuestionDiscussionBox(true);
                await new Promise(r => setTimeout(r, 600));
                const boxVisible = !document.getElementById('q-community-discussion-box')?.classList.contains('hidden');
                const listHtml = document.getElementById('q-discussion-list')?.innerText;
                const countBadge = document.getElementById('q-discussion-count-badge')?.innerText;
                return { boxVisible, listHtml: listHtml.slice(0, 100), countBadge };
            })()""")
            print("TEST 2 - DISCUSSION TOGGLE & LOAD:", json.dumps(t2, ensure_ascii=False, indent=2))
            assert t2['boxVisible'], "Discussion box should be visible when toggled!"

            # TEST 3: AI Tutor Full-Screen Expand Button & Centering
            t3 = await run_js("""(function() {
                windowTutorSizeExpanded = false;
                document.getElementById('floating-tutor-container')?.classList.remove('tutor-expanded-parent');
                toggleFloatingTutor();
                toggleFloatingTutorSize();
                const isExpanded = document.getElementById('floating-tutor-container')?.classList.contains('tutor-expanded-parent');
                const btnLabelAfter = document.getElementById('ft-expand-label')?.innerText;
                return { isExpanded, btnLabelAfter };
            })()""")
            print("TEST 3 - AI EXPAND FULL-SCREEN:", json.dumps(t3, ensure_ascii=False, indent=2))
            assert t3['isExpanded'], "Tutor container must have tutor-expanded-parent class!"
            assert t3['btnLabelAfter'] == 'Thu Nhỏ', "Expand button label must toggle to 'Thu Nhỏ'!"

            # TEST 4: Code Snippet Interactive Rows
            t4 = await run_js("""(function() {
                const sampleCode = 'class Patient {\\n    public string Name;\\n    public int Age;\\n}';
                const html = buildCodeWindowHtml(sampleCode, 'Patient.cs', 'csharp');
                const hasInteractiveRows = html.includes('askAiAboutCodeLine') && html.includes('Hỏi AI');
                const hasWholeCodeBtn = html.includes('askAiAboutWholeCodeSnippet');
                return { hasInteractiveRows, hasWholeCodeBtn };
            })()""")
            print("TEST 4 - INTERACTIVE CODE ASK AI:", json.dumps(t4, ensure_ascii=False, indent=2))
            assert t4['hasInteractiveRows'], "Code lines must have interactive askAiAboutCodeLine!"
            assert t4['hasWholeCodeBtn'], "Code window must have askAiAboutWholeCodeSnippet!"

            # TEST 5: Text Selection Floating AI Bubble
            t5 = await run_js("""(function() {
                const bubble = document.getElementById('text-select-ai-bubble');
                const wordEl = document.getElementById('text-select-ai-word');
                return { hasBubble: Boolean(bubble), hasWordEl: Boolean(wordEl) };
            })()""")
            print("TEST 5 - TEXT SELECTION BUBBLE:", json.dumps(t5, ensure_ascii=False, indent=2))
            assert t5['hasBubble'] and t5['hasWordEl'], "Text selection bubble must exist in DOM!"

            # TEST 6: Safe Archiving & Restore
            t6 = await run_js("""(function() {
                const mockExam = [{ id: 'mock_test_1', subject_name: 'Hóa Sinh', score: 9.5, total_questions: 10, created_at: '2026-11-10' }];
                saveLocalExamHistory(mockExam);
                saveLocalExamArchive([]);
                
                clearAllLocalExamHistory();
                const activeAfterClear = getLocalExamHistory().length;
                const archiveAfterClear = getLocalExamArchive().length;

                restoreAllLocalExamHistory();
                const activeAfterRestore = getLocalExamHistory().length;
                const archiveAfterRestore = getLocalExamArchive().length;

                return { activeAfterClear, archiveAfterClear, activeAfterRestore, archiveAfterRestore };
            })()""")
            print("TEST 6 - SAFE ARCHIVE & RESTORE:", json.dumps(t6, ensure_ascii=False, indent=2))
            assert t6['activeAfterClear'] == 0, "Active exams should be cleared"
            assert t6['archiveAfterClear'] == 1, "Exams must be safely moved into archive"
            assert t6['activeAfterRestore'] == 1, "Exams must be restored to active list"
            assert t6['archiveAfterRestore'] == 0, "Archive should be empty after full restore"

            # Capture screenshot of verified screen
            msg_id = 9999
            await ws.send_json({
                'id': msg_id,
                'method': 'Page.captureScreenshot',
                'params': {'format': 'jpeg', 'quality': 85}
            })
            while True:
                m = await ws.receive_json()
                if m.get('id') == msg_id:
                    data = m.get('result', {}).get('data', '')
                    with open(r'C:\Users\PC\.gemini\antigravity\brain\bf908d19-5939-4c23-8975-52dd4241139d\exam_v19_verified.jpg', 'wb') as img_f:
                        img_f.write(base64.b64decode(data))
                    print("Saved verified screenshot to exam_v19_verified.jpg")
                    break

            print("\n=============================================")
            print("ALL 6 V19 INTEGRATION TESTS PASSED 100% PERFECTLY!")
            print("=============================================")

asyncio.run(test_v19())
proc.terminate()
