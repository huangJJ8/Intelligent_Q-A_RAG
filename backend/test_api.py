"""Standalone DashScope MaaS API test — run with: venv\Scripts\python.exe test_api.py"""
import os, sys
sys.path.insert(0, ".")

from app.config import settings

API_KEY = settings.DASHSCOPE_API_KEY
BASE_URL = settings.DASHSCOPE_API_BASE

# ====== Test 1: raw openai SDK ======
print("=== Test 1: openai SDK raw call ===")
try:
    from openai import OpenAI
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    resp = client.chat.completions.create(
        model="qwen-plus",
        messages=[{"role": "user", "content": "回复两个字：你好"}],
        max_tokens=50,
        stream=False,
    )
    print(f"SUCCESS: {resp.choices[0].message.content}")
except Exception as e:
    print(f"FAIL: {e}")
print()

# ====== Test 2: openai SDK streaming ======
print("=== Test 2: openai SDK streaming ===")
try:
    from openai import OpenAI
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    stream = client.chat.completions.create(
        model="qwen-plus",
        messages=[{"role": "user", "content": "回复两个字：你好"}],
        max_tokens=50,
        stream=True,
    )
    print("Streaming: ", end="", flush=True)
    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    print()
    print("SUCCESS")
except Exception as e:
    print(f"\nFAIL: {e}")
print()

# ====== Test 3: ChatOpenAI from langchain_openai ======
print("=== Test 3: ChatOpenAI invoke ===")
try:
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage
    llm = ChatOpenAI(model="qwen-plus", api_key=API_KEY, base_url=BASE_URL, temperature=0.3)
    resp = llm.invoke([HumanMessage(content="回复两个字：你好")])
    print(f"SUCCESS: {resp.content}")
except Exception as e:
    print(f"FAIL: {e}")
print()

# ====== Test 4: ChatOpenAI streaming ======
print("=== Test 4: ChatOpenAI streaming ===")
try:
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage, SystemMessage
    llm = ChatOpenAI(model="qwen-plus", api_key=API_KEY, base_url=BASE_URL, temperature=0.3, streaming=True)
    print("Streaming: ", end="", flush=True)
    full = ""
    for chunk in llm.stream([SystemMessage(content="你是助手"), HumanMessage(content="回复：你好")]):
        if chunk.content:
            full += chunk.content
            print(chunk.content, end="", flush=True)
    print()
    print("SUCCESS" if full else "FAIL: empty response")
except Exception as e:
    print(f"\nFAIL: {e}")
print()

# ====== Test 5: With SystemMessage only ======
print("=== Test 5: HumanMessage only (no SystemMessage) ===")
try:
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage
    llm = ChatOpenAI(model="qwen-plus", api_key=API_KEY, base_url=BASE_URL, temperature=0.3)
    resp = llm.invoke([HumanMessage(content="你好")])
    print(f"SUCCESS: {resp.content}")
except Exception as e:
    print(f"FAIL: {e}")
print()

# ====== Test 6: Embedding ======
print("=== Test 6: OpenAIEmbeddings ===")
try:
    from langchain_openai import OpenAIEmbeddings
    emb = OpenAIEmbeddings(model="text-embedding-v2", api_key=API_KEY, base_url=BASE_URL, dimensions=1024)
    vec = emb.embed_query("测试文本")
    print(f"SUCCESS: vector dim={len(vec)}")
except Exception as e:
    print(f"FAIL: {e}")

print("\n=== ALL DONE ===")
