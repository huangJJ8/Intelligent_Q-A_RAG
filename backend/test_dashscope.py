"""
Test script — verify DashScope API connectivity
Run: venv\Scripts\python.exe test_dashscope.py
"""
import os
import sys
sys.path.insert(0, ".")

from app.config import settings

print("=== Config ===")
print(f"Model: {settings.LLM_MODEL}")
print(f"Embedding: {settings.EMBEDDING_MODEL}")
print(f"API Base: {settings.DASHSCOPE_API_BASE}")
print()

# ====== Test 1: Direct dashscope SDK ======
print("=== Test 1: dashscope SDK direct ===")
try:
    import dashscope
    from dashscope import Generation

    resp = Generation.call(
        model=settings.LLM_MODEL,
        api_key=settings.DASHSCOPE_API_KEY,
        messages=[{"role": "user", "content": "回复：你好"}],
        result_format="message",
        max_tokens=50,
    )
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        print(f"Output: {resp.output.choices[0].message.content[:100]}")
    else:
        print(f"Error: {resp.message}")
except Exception as e:
    print(f"Exception: {e}")
print()

# ====== Test 2: ChatTongyi from langchain_community ======
print("=== Test 2: ChatTongyi ===")
try:
    from langchain_community.chat_models.tongyi import ChatTongyi
    from langchain_core.messages import HumanMessage

    llm = ChatTongyi(
        model=settings.LLM_MODEL,
        api_key=settings.DASHSCOPE_API_KEY,
        temperature=0.3,
    )
    msg = [HumanMessage(content="回复：你好")]
    resp = llm.invoke(msg)
    print(f"Output: {resp.content[:100]}")
except Exception as e:
    print(f"Exception: {e}")
print()

# ====== Test 3: ChatOpenAI with standard endpoint ======
print("=== Test 3: ChatOpenAI -> dashscope.aliyuncs.com ===")
try:
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage

    llm = ChatOpenAI(
        model=settings.LLM_MODEL,
        api_key=settings.DASHSCOPE_API_KEY,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        temperature=0.3,
    )
    msg = [HumanMessage(content="回复：你好")]
    resp = llm.invoke(msg)
    print(f"Output: {resp.content[:100]}")
except Exception as e:
    print(f"Exception: {e}")
print()

# ====== Test 4: ChatOpenAI with MaaS endpoint ======
print("=== Test 4: ChatOpenAI -> MaaS endpoint ===")
try:
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage

    llm = ChatOpenAI(
        model=settings.LLM_MODEL,
        api_key=settings.DASHSCOPE_API_KEY,
        base_url=settings.DASHSCOPE_API_BASE,
        temperature=0.3,
    )
    msg = [HumanMessage(content="回复：你好")]
    resp = llm.invoke(msg)
    print(f"Output: {resp.content[:100]}")
except Exception as e:
    print(f"Exception: {e}")

print("\n=== DONE ===")
