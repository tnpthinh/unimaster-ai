with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos_fb = html.find('id="q-feedback-panel"')
pos_btn = html.find('<!-- Sticky Bottom Navigation Bar')
print("HTML between feedback panel and bottom nav:")
print(html[pos_btn-400:pos_btn+200])
