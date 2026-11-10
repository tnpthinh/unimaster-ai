with open('verify_v22_fixes.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
    "botNextVisible: !!botNext && !botNext.closest('.hidden'),",
    "botNextVisible: !!botNext && !botNext.closest('.hidden'), botHiddenParent: botNext?.closest('.hidden')?.id || botNext?.closest('.hidden')?.className,"
)
with open('verify_v22_fixes.py', 'w', encoding='utf-8') as f:
    f.write(text)
