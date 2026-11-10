with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix broken rubber duck tag
broken_tag = """<!-- Rubber Duck Toxic AI Assistant Sticky Callout -->
          <div id="rubber-duck-sidebar" class="hidden uni-card p-4 border border</div>
    -amber-500/40 bg-gradient-to-r from-amber-950/40 to-slate-900/60 space-y-2 shadow-lg animate-fade-in">"""

fixed_tag = """<!-- Rubber Duck Toxic AI Assistant Sticky Callout -->
          <div id="rubber-duck-sidebar" class="hidden uni-card p-4 border border-amber-500/40 bg-gradient-to-r from-amber-950/40 to-slate-900/60 space-y-2 shadow-lg animate-fade-in">"""

if broken_tag in html:
    html = html.replace(broken_tag, fixed_tag)
    print("Fixed broken rubber duck HTML tag!")
else:
    # regex fallback
    import re
    html = re.sub(
        r'<div id="rubber-duck-sidebar"\s+class="hidden uni-card p-4 border border</div>\s*-amber-500/40[^"]*"',
        '<div id="rubber-duck-sidebar" class="hidden uni-card p-4 border border-amber-500/40 bg-gradient-to-r from-amber-950/40 to-slate-900/60 space-y-2 shadow-lg animate-fade-in"',
        html
    )
    print("Fixed broken rubber duck HTML tag via regex!")

with open('static/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated static/index.html!")
