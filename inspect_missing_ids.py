with open('static/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

missing_ids = [
   'ft-spinner',
   'essay-ans-input',
   'exercise-ai-box',
   'lightbox-caption-el',
   'mistake-bank-modal-list',
   'osce-ai-explanation-box',
   'osce-live-countdown',
   'planner-countdown-badge',
   'code-editor-textarea',
   'header-pomo-pill'
]

for mid in missing_ids:
    idx = js.find(f"'{mid}'")
    if idx == -1:
        idx = js.find(f'"{mid}"')
    print(f"=== {mid} (found: {idx != -1}) ===")
    if idx != -1:
        print(js[max(0, idx-100):min(len(js), idx+200)])
