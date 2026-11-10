import re

with open('static/app.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

with open('static/index.html', 'r', encoding='utf-8') as f:
    html_text = f.read()

# 1. Check all onclick functions in HTML
onclicks = set(re.findall(r'onclick=["\']([^"\']+)["\']', html_text))
print(f"Total unique onclick handlers in HTML: {len(onclicks)}")
missing_fns = []
for oc in onclicks:
    # Extract function name(s)
    calls = [c.strip() for c in oc.split(';') if c.strip()]
    for call in calls:
        fn_match = re.match(r'([a-zA-Z0-9_$]+)\s*\(', call)
        if fn_match:
            fn_name = fn_match.group(1)
            # check if defined in JS or built-in
            builtins = ['alert', 'confirm', 'prompt', 'print', 'closeModal', 'openModal', 'setVirtualStep', 'nextVirtualStep', 'prevVirtualStep', 'rateFlashcard', 'openImageLightbox']
            if fn_name not in builtins:
                if f"function {fn_name}" not in js_text and f"{fn_name} =" not in js_text and f"window.{fn_name}" not in js_text:
                    missing_fns.append(fn_name)

print("Missing onclick functions in app.js:", set(missing_fns))

# 2. Check for common undefined variables/functions called inside app.js
called_fns = set(re.findall(r'\b([a-zA-Z0-9_$]+)\s*\(', js_text))
print(f"Total function calls in app.js: {len(called_fns)}")

# Check specific suspicious calls
for sus in ['awardXP', 'addXp', 'playSound', 'showToast', 'formatRichText', 'escapeHtml', 'renderMarkdown', 'renderAllMathOnPage', 'renderKatexSafe']:
    defined = f"function {sus}" in js_text or f"{sus} =" in js_text or f"window.{sus}" in js_text
    print(f"  Check '{sus}': {'DEFINED' if defined else 'MISSING'}")
