import subprocess, time, json, asyncio, aiohttp

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
proc = subprocess.Popen([chrome_path, '--headless=new', '--remote-debugging-port=9225', '--disable-gpu', 'http://localhost:8080'])
time.sleep(2)

async def inspect():
    async with aiohttp.ClientSession() as s:
        async with s.get('http://127.0.0.1:9225/json') as r:
            tabs = await r.json()
        target = next((t for t in tabs if 'localhost:8080' in t.get('url', '')), tabs[0])
        ws_url = target['webSocketDebuggerUrl']
        async with s.ws_connect(ws_url) as ws:
            await ws.send_json({'id': 1, 'method': 'Runtime.enable'})
            await ws.send_json({
                'id': 10,
                'method': 'Runtime.evaluate',
                'params': {
                    'expression': '''(() => {
                        openModal('modal-settings');
                        const modal = document.getElementById('modal-settings');
                        const card = modal.querySelector('.uni-card');
                        const header = card.children[0];
                        const tabsBar = card.children[1];
                        const body = card.children[2];
                        const firstTabBtn = tabsBar.querySelector('button');
                        return JSON.stringify({
                            cardRect: card.getBoundingClientRect(),
                            headerRect: header.getBoundingClientRect(),
                            tabsBarRect: tabsBar.getBoundingClientRect(),
                            tabsBarScrollHeight: tabsBar.scrollHeight,
                            tabsBarClientHeight: tabsBar.clientHeight,
                            firstTabBtnRect: firstTabBtn.getBoundingClientRect(),
                            bodyRect: body.getBoundingClientRect()
                        });
                    })()''',
                    'returnByValue': True
                }
            })
            while True:
                resp = await ws.receive_json()
                if resp.get('id') == 10:
                    val = resp['result']['result']['value']
                    print('MODAL RECTS:\n', json.dumps(json.loads(val), indent=2))
                    break

try:
    asyncio.run(inspect())
finally:
    proc.terminate()
