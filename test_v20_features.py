import subprocess, time, json, asyncio, aiohttp, base64

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
proc = subprocess.Popen([chrome_path, '--headless=new', '--remote-debugging-port=9237', '--window-size=1280,850', '--disable-gpu', 'http://localhost:8080'])
time.sleep(2.5)

async def test_v20():
    async with aiohttp.ClientSession() as s:
        async with s.get('http://127.0.0.1:9237/json') as r:
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

            # TEST 1: Fullscreen Button on Header and Home Banner
            t1 = await run_js("""(function() {
                const headerBtn = document.getElementById('header-fullscreen-btn');
                const heroBtn = document.querySelector('button[onclick="toggleAppFullscreen()"]');
                const headerText = headerBtn ? headerBtn.innerText : '';
                toggleAppFullscreen();
                const isFsMode = document.body.classList.contains('app-fullscreen-mode');
                toggleAppFullscreen(); // Toggle back
                return { hasHeaderBtn: Boolean(headerBtn), hasHeroBtn: Boolean(heroBtn), headerText, isFsMode };
            })()""")
            print("TEST 1 - FULLSCREEN BUTTONS:", json.dumps(t1, ensure_ascii=False, indent=2))
            assert t1['hasHeaderBtn'], "Header fullscreen button must exist!"
            assert t1['hasHeroBtn'], "Hero banner fullscreen button must exist!"
            assert t1['isFsMode'], "Body should have app-fullscreen-mode on toggle!"

            # TEST 2: Multi-Account System & Switching
            t2 = await run_js("""(function() {
                const accounts = getAllLocalAccounts();
                switchActiveAccount('acc_cntt');
                const active1 = getActiveAccount();
                const avatar1 = document.getElementById('header-user-avatar')?.innerText;
                const name1 = document.getElementById('header-user-name')?.innerText;

                switchActiveAccount('acc_y_khoa');
                const active2 = getActiveAccount();
                const avatar2 = document.getElementById('header-user-avatar')?.innerText;
                const name2 = document.getElementById('header-user-name')?.innerText;

                return {
                    totalAccounts: accounts.length,
                    cntt: { name: active1.name, avatar: avatar1, headerName: name1 },
                    ykhoa: { name: active2.name, avatar: avatar2, headerName: name2 }
                };
            })()""")
            print("TEST 2 - MULTI-ACCOUNT SWITCHING:", json.dumps(t2, ensure_ascii=False, indent=2))
            assert t2['totalAccounts'] >= 3, "Must have at least 3 starter accounts!"
            assert t2['cntt']['avatar'] == '💻', "CNTT account avatar should be 💻"
            assert t2['ykhoa']['avatar'] == '🩺', "Y Khoa account avatar should be 🩺"

            # TEST 3: Account Subject Picker & Enrollment
            t3 = await run_js("""(function() {
                openAccountSubjectPickerModal('acc_y_khoa');
                const modalVisible = !document.getElementById('modal-account-subjects')?.classList.contains('hidden');
                selectSubjectPreset('medical');
                const selectedCount = tempSelectedSubjectIds.size;
                saveAccountEnrolledSubjects();
                const updatedAcc = getActiveAccount();
                return { modalVisible, selectedCount, savedSubjects: updatedAcc.enrolled_subjects };
            })()""")
            print("TEST 3 - SUBJECT PICKER ENROLLMENT:", json.dumps(t3, ensure_ascii=False, indent=2))
            assert t3['modalVisible'], "Subject picker modal must be visible when opened!"
            assert t3['selectedCount'] >= 1, "Medical preset should select medical subject(s)!"
            assert 10 in t3['savedSubjects'], "Hóa Sinh CTUMP (10) must be in saved subjects!"

            # TEST 4: Deep Color Studio Customization
            t4 = await run_js("""(function() {
                setCustomStageBg('#181824');
                const bgSurface = getComputedStyle(document.documentElement).getPropertyValue('--bg-surface').trim();

                setOptionColorMode('rainbow');
                const optA = getComputedStyle(document.documentElement).getPropertyValue('--opt-a-accent').trim();
                const optB = getComputedStyle(document.documentElement).getPropertyValue('--opt-b-accent').trim();

                setGlobalZoomScale(120);
                const baseFont = getComputedStyle(document.documentElement).getPropertyValue('--base-font-size').trim();

                setQuestionTextColor('#ffffff');
                const qColor = getComputedStyle(document.documentElement).getPropertyValue('--custom-q-text-color').trim();

                return { bgSurface, optA, optB, baseFont, qColor };
            })()""")
            print("TEST 4 - DEEP COLOR STUDIO:", json.dumps(t4, ensure_ascii=False, indent=2))
            assert t4['bgSurface'] == '#181824', "Custom stage background should be #181824!"
            assert t4['optA'] == '#8b5cf6', "Option A rainbow accent should be #8b5cf6!"
            assert t4['baseFont'] == '19.2px', "120% zoom should set base font to 19.2px!"
            assert t4['qColor'] == '#ffffff', "Question text color should be #ffffff!"

            # TEST 5: iPad & iPhone Responsive Verification
            # Set to iPad viewport
            await ws.send_json({
                'id': 501,
                'method': 'Emulation.setDeviceMetricsOverride',
                'params': {'width': 820, 'height': 1180, 'deviceScaleFactor': 2, 'mobile': True}
            })
            await asyncio.sleep(0.5)
            t5_ipad = await run_js("""(function() {
                const bottomNavVisible = getComputedStyle(document.querySelector('.mobile-bottom-nav')).display !== 'none';
                return { ipadBottomNavVisible: bottomNavVisible };
            })()""")
            print("TEST 5 - IPAD PORTRAIT NAV:", t5_ipad)
            assert t5_ipad['ipadBottomNavVisible'], "Bottom nav must be visible on iPad portrait!"

            # Set to iPad landscape
            await ws.send_json({
                'id': 502,
                'method': 'Emulation.setDeviceMetricsOverride',
                'params': {'width': 1180, 'height': 820, 'deviceScaleFactor': 2, 'mobile': False}
            })
            await asyncio.sleep(0.5)
            t5_ipad_ls = await run_js("""(function() {
                const topNavVisible = getComputedStyle(document.querySelector('header nav')).display !== 'none';
                return { ipadLandscapeTopNavVisible: topNavVisible };
            })()""")
            print("TEST 5 - IPAD LANDSCAPE NAV:", t5_ipad_ls)
            assert t5_ipad_ls['ipadLandscapeTopNavVisible'], "Top nav must be visible on iPad landscape!"

            # Reset back to standard desktop for verified screenshot
            await ws.send_json({
                'id': 503,
                'method': 'Emulation.setDeviceMetricsOverride',
                'params': {'width': 1280, 'height': 850, 'deviceScaleFactor': 1, 'mobile': False}
            })
            await asyncio.sleep(0.5)

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
                    with open(r'C:\Users\PC\.gemini\antigravity\brain\bf908d19-5939-4c23-8975-52dd4241139d\exam_v20_verified.jpg', 'wb') as img_f:
                        img_f.write(base64.b64decode(data))
                    print("Saved verified screenshot to exam_v20_verified.jpg")
                    break

            print("\n=============================================")
            print("ALL 5 V20 INTEGRATION TESTS PASSED 100% PERFECTLY!")
            print("=============================================")

asyncio.run(test_v20())
proc.terminate()
