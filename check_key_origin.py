transcript_path = r'C:\Users\PC\.gemini\antigravity\brain\bf908d19-5939-4c23-8975-52dd4241139d\.system_generated\logs\transcript.jsonl'
with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        if '00eab046c62fd5b2' in line:
            import json
            obj = json.loads(line)
            print("Step index:", obj.get('step_index'))
            print("Source:", obj.get('source'))
            print("Type:", obj.get('type'))
            print("Content:", str(obj.get('content'))[:500])
            print("="*50)
