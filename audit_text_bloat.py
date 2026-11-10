# audit_text_bloat.py
import re

with open('static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

sections = re.findall(r'<section\s+id=[\'"]([^\'"]+)[\'"]', text)
print("Sections found:", sections)

modals = re.findall(r'<div\s+id=[\'"](modal-[^\'"]+)[\'"]', text)
print("\nModals found:", len(modals), modals[:15])

# Find all paragraphs <p> with > 40 chars
long_p = re.findall(r'<p[^>]*>([^<]{40,})</p>', text)
print(f"\nLong <p> elements ({len(long_p)} found):")
for i, p in enumerate(long_p[:20]):
    clean = ' '.join(p.split())
    print(f"{i+1}. {clean[:100]}...")

# Find all subtitle/heading pairs with wordy text
long_h = re.findall(r'<h[1-4][^>]*>([^<]{40,})</h[1-4]>', text)
print(f"\nLong headings ({len(long_h)} found):")
for i, h in enumerate(long_h[:15]):
    clean = ' '.join(h.split())
    print(f"{i+1}. {clean[:100]}...")
