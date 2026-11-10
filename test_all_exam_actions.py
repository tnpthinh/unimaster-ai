import subprocess, time, json, asyncio, aiohttp

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
proc = subprocess.Popen([chrome_path, '--headless=new', '--remote-debugging-port=9239', '--window-size=1280,850', '--disable-gpu', 'http://localhost:8080'])
time.sleep(2.5)

async def test_exam_suite():
    async with aiohttp.ClientSession() as s:
        async with s.get('http://127.0.0.1:9239/json') as r:
            tabs = await r.json()
        target = next((t for t in tabs if 'localhost:8080' in t.get('url', '')), tabs[0])
        ws_url = target['webSocketDebuggerUrl']
        
        async with s.ws_connect(ws_url) as ws:
            await ws.send_json({'id': 1, 'method': 'Runtime.enable'})
            await ws.send_json({'id': 2, 'method': 'Page.enable'})

            async def run_js(code, mid):
                await ws.send_json({
                    'id': mid,
                    'method': 'Runtime.evaluate',
                    'params': {'expression': code, 'awaitPromise': True, 'returnByValue': True}
                })
                while True:
                    m = await ws.receive_json()
                    if m.get('id') == mid:
                        res = m.get('result', {}).get('result', {})
                        if 'value' in res:
                            return res['value']
                        return res

            await asyncio.sleep(2.0)

            # Start Exam
            await run_js("quickStartBai4Lipid()", 101)
            await asyncio.sleep(1.0)

            # Test 1: Option Select
            r1 = await run_js("""(function() {
                selectExamOption('B');
                return {
                    selectedAns: STATE.exam.answers[STATE.exam.questions[0].id],
                    isOptBSelected: document.getElementById('opt-row-B')?.classList.contains('selected')
                };
            })()""", 102)
            print("1. Select Option B:", r1)

            # Test 2: 50/50 Lifeline
            r2 = await run_js("""(function() {
                useLifeline5050();
                const qid = STATE.exam.questions[0].id;
                return { eliminated: STATE.exam.eliminated[qid] };
            })()""", 103)
            print("2. 50/50 Lifeline:", r2)

            # Test 3: Bookmark
            r3 = await run_js("""(function() {
                toggleBookmarkCurrent();
                const qid = STATE.exam.questions[0].id;
                return { isBookmarked: STATE.bookmarks.includes(qid) };
            })()""", 104)
            print("3. Bookmark Current:", r3)

            # Test 4: Note Box
            r4 = await run_js("""(function() {
                toggleNoteBox();
                const isHidden = document.getElementById('q-note-box')?.classList.contains('hidden');
                const inp = document.getElementById('q-note-input');
                if (inp) inp.value = 'Mẹo test note';
                saveCurrentNote();
                const qid = STATE.exam.questions[0].id;
                return { isNoteBoxOpen: !isHidden, savedNote: STATE.notes[qid] };
            })()""", 105)
            print("4. Note Box:", r4)

            # Test 5: Next & Prev Question
            r5 = await run_js("""(function() {
                nextQuestion();
                const idxAfterNext = STATE.exam.currentIndex;
                prevQuestion();
                const idxAfterPrev = STATE.exam.currentIndex;
                return { idxAfterNext, idxAfterPrev };
            })()""", 106)
            print("5. Next / Prev Nav:", r5)

            # Test 6: Submit Exam and Check Result Screen
            r6 = await run_js("""(function() {
                submitExamNow(true);
                const isResultVisible = !document.getElementById('exam-result-screen')?.classList.contains('hidden');
                const scoreText = document.getElementById('res-score')?.innerText;
                return { isResultVisible, scoreText };
            })()""", 107)
            print("6. Submit Exam:", r6)

asyncio.run(test_exam_suite())
proc.terminate()
