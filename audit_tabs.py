import asyncio, aiohttp, json

async def audit_all_tabs():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://127.0.0.1:9225/json') as resp:
            tabs = await resp.json()
            target = next((t for t in tabs if 'localhost:8080' in t.get('url', '')), None)
            if not target:
                print('Target tab not found')
                return
            ws_url = target['webSocketDebuggerUrl']
            
            async with session.ws_connect(ws_url) as ws:
                await ws.send_json({'id': 1, 'method': 'Runtime.enable'})
                await ws.send_json({'id': 2, 'method': 'Page.enable'})
                await ws.send_json({'id': 3, 'method': 'Page.reload'})
                await asyncio.sleep(2.0)
                
                tab_list = ['dashboard', 'exam', 'exercises', 'essay', 'flashcards', 'search', 'tutor', 'generator', 'arena', 'lab']
                errors = []
                
                async def collect_exceptions():
                    while True:
                        try:
                            msg = await asyncio.wait_for(ws.receive(), timeout=0.3)
                            if msg.type == aiohttp.WSMsgType.TEXT:
                                data = json.loads(msg.data)
                                if data.get('method') == 'Runtime.exceptionThrown':
                                    details = data.get('params', {}).get('exceptionDetails', {})
                                    err_text = details.get('text', '') + ': ' + str(details.get('exception', {}).get('description', ''))
                                    errors.append(err_text)
                        except asyncio.TimeoutError:
                            break

                await collect_exceptions()
                
                for t in tab_list:
                    print(f'Testing switchTab("{t}")...')
                    await ws.send_json({
                        'id': 100,
                        'method': 'Runtime.evaluate',
                        'params': {'expression': f'switchTab("{t}")', 'returnByValue': True}
                    })
                    await asyncio.sleep(0.4)
                    await collect_exceptions()
                
                print('\nTotal exceptions caught across all tabs:', len(errors))
                for e in set(errors):
                    print('ERROR:', e)

asyncio.run(audit_all_tabs())
