with open('ai_service.py', 'r', encoding='utf-8') as f:
    code = f.read()

pos = code.find('async def _call_openai_chatgpt')
print(code[pos:pos+2500])
