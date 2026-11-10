with open('static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Check where view-dashboard starts
idx = text.find('<section id="view-dashboard"')
print("view-dashboard index:", idx)
if idx != -1:
    print(text[idx:idx+300])

# Check where the last modal is
idx2 = text.rfind('id="modal-')
print("\nLast modal index:", idx2)
if idx2 != -1:
    print(text[idx2:idx2+200])
