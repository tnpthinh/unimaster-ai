import subprocess, time, json, asyncio, aiohttp

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
proc = subprocess.Popen([chrome_path, '--headless=new', '--remote-debugging-port=9229', '--disable-gpu', 'http://localhost:8080'])
time.sleep(2)

async def run():
    async with aiohttp.ClientSession() as s:
        async with s.get('http://127.0.0.1:9229/json') as r:
            tabs = await r.json()
        target = tabs[0]
        async with s.ws_connect(target['webSocketDebuggerUrl']) as ws:
            await ws.send_json({'id': 1, 'method': 'Runtime.enable'})
            await asyncio.sleep(2.0)
            await ws.send_json({'id': 10, 'method': 'Runtime.evaluate', 'params': {'expression': 'document.getElementById("stat-subjects") ? document.getElementById("stat-subjects").innerText : "none"', 'returnByValue': True}})
            while True:
                resp = await ws.receive_json()
                if resp.get('id') == 10:
                    print('RESP 10:', resp)
                    break

try:
    asyncio.run(run())
finally:
    proc.terminate()
