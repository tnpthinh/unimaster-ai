with open(r'C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai\code_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = """"actual": act if not is_hidden or not is_passed else "[Khớp đáp án]","""
replacement = """"actual": act if not is_hidden else ("[Passed]" if is_passed else "[Failed - Sai Kết Quả]"),"""

if target in text:
    text = text.replace(target, replacement)
    with open(r'C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai\code_engine.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("code_engine.py hidden testcase privacy hardened.")
else:
    print("Target not found in code_engine.py")
