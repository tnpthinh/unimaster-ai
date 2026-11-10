import asyncio, aiohttp, json

key = "sk-00eab046c62fd5b2-1xm2wbqqkfylmmti-083b2119"

async def test_direct():
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }

    # Test 1: Standard api.openai.com
    print("=== TEST 1: https://api.openai.com/v1/chat/completions ===")
    async with aiohttp.ClientSession() as session:
        for model in ["gpt-4o-mini", "gpt-3.5-turbo"]:
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": "Hi"}],
                "max_tokens": 10
            }
            try:
                async with session.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                    text = await resp.text()
                    print(f"Status: {resp.status}")
                    print(f"Response: {text}")
            except Exception as e:
                print("Error:", e)

    # Test 2: List models to see what this key has access to or if it's invalid
    print("\n=== TEST 2: https://api.openai.com/v1/models ===")
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get("https://api.openai.com/v1/models", headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                text = await resp.text()
                print(f"Status: {resp.status}")
                print(f"Response: {text[:300]}")
        except Exception as e:
            print("Error:", e)

asyncio.run(test_direct())
