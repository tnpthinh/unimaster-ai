import subprocess, time, json, asyncio, aiohttp

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
proc = subprocess.Popen([chrome_path, '--headless=new', '--remote-debugging-port=9240', '--window-size=1280,850', '--disable-gpu', 'http://localhost:8080'])
time.sleep(2.5)

async def test():
    async with aiohttp.ClientSession() as s:
        async with s.get('http://127.0.0.1:9240/json') as r:
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
            await run_js("quickStartBai4Lipid()", 1)
            await asyncio.sleep(1.0)

            # Select an option
            await run_js("selectExamOption('B')", 2)

            # Await submit
            r = await run_js("""(async function() {
                await submitExamNow(true);
                return {
                    isResultVisible: !document.getElementById('exam-result-screen')?.classList.contains('hidden'),
                    scoreText: document.getElementById('res-score-num')?.innerText,
                    correctText: document.getElementById('res-correct')?.innerText
                };
            })()""", 3)
            print("Submit result:", r)

asyncio.run(test())
proc.terminate()
