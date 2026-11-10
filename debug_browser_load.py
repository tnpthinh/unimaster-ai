import subprocess, time, json, asyncio, aiohttp

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
proc = subprocess.Popen([chrome_path, '--headless=new', '--remote-debugging-port=9232', '--window-size=1280,820', '--disable-gpu', 'http://localhost:8080'])
time.sleep(2.5)

async def test():
    async with aiohttp.ClientSession() as s:
        async with s.get('http://127.0.0.1:9232/json') as r:
            tabs = await r.json()
        target = next((t for t in tabs if 'localhost:8080' in t.get('url', '')), tabs[0])
        ws_url = target['webSocketDebuggerUrl']
        
        async with s.ws_connect(ws_url) as ws:
            await ws.send_json({'id': 1, 'method': 'Runtime.enable'})
            await ws.send_json({'id': 2, 'method': 'Page.enable'})
            await ws.send_json({'id': 3, 'method': 'Console.enable'})

            console_msgs = []
            
            async def run_js(code):
                msg_id = int(time.time() * 1000) % 100000
                await ws.send_json({
                    'id': msg_id,
                    'method': 'Runtime.evaluate',
                    'params': {'expression': code, 'awaitPromise': True, 'returnByValue': True}
                })
                while True:
                    m = await ws.receive_json()
                    if m.get('method') == 'Console.messageAdded':
                        console_msgs.append(m.get('params', {}).get('message', {}).get('text'))
                    elif m.get('method') == 'Runtime.consoleAPICalled':
                        args = m.get('params', {}).get('args', [])
                        console_msgs.append(' '.join(str(a.get('value', '')) for a in args))
                    elif m.get('id') == msg_id:
                        return m.get('result', {}).get('result', {}).get('value')

            await asyncio.sleep(2.0)

            stats = await run_js("""({
                subText: document.getElementById('stat-subjects')?.innerText,
                qText: document.getElementById('stat-questions')?.innerText,
                examText: document.getElementById('stat-exams')?.innerText,
                avgText: document.getElementById('stat-avg-score')?.innerText,
                subjectsLen: (window.STATE && window.STATE.subjects) ? window.STATE.subjects.length : 'no STATE'
            })""")
            print("BROWSER STATS:", stats)
            
            # Now let's trigger "Làm Bài Thi Ngay" or start exam
            exam_res = await run_js("""(async function() {
                try {
                    // Click start quick exam or switch to exam
                    await quickStartBai4Lipid();
                    return {
                        examActive: STATE.exam?.active,
                        totalQuestions: STATE.exam?.questions?.length,
                        promptText: document.getElementById('q-prompt-text')?.innerHTML,
                        answerHtml: document.getElementById('q-answer-area')?.innerHTML,
                        qNum: document.getElementById('current-q-num')?.innerText
                    };
                } catch (e) {
                    return { error: e.toString(), stack: e.stack };
                }
            })()""")
            print("EXAM LAUNCH RESULT:", json.dumps(exam_res, ensure_ascii=False, indent=2))
            print("CONSOLE MSGS:", console_msgs)

asyncio.run(test())
proc.terminate()
