with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('static/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

for term in ['osce', 'chạy trạm', 'station', 'tram', 'phòng thí nghiệm', 'virtualstep']:
    count_html = html.lower().count(term)
    count_js = js.lower().count(term)
    print(f"Term '{term}': HTML={count_html}, JS={count_js}")
