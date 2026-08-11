"""
嵌入模型 — dashscope SDK 原生 TextEmbedding
"""

from langchain_core.embeddings import Embeddings
from app.config import settings
from typing import List
import dashscope


class DashScopeEmbeddings(Embeddings):
    """Custom Embeddings using dashscope SDK directly (MaaS workspace endpoint)"""

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        results = []
        for text in texts:
            resp = dashscope.TextEmbedding.call(
                model=settings.EMBEDDING_MODEL,
                api_key=settings.DASHSCOPE_API_KEY,
                input=text,
            )
            if resp.status_code == 200:
                results.append(resp.output["embeddings"][0]["embedding"])
            else:
                raise RuntimeError(f"Embedding failed: {resp.message}")
        return results

    def embed_query(self, text: str) -> List[float]:
        resp = dashscope.TextEmbedding.call(
            model=settings.EMBEDDING_MODEL,
            api_key=settings.DASHSCOPE_API_KEY,
            input=text,
        )
        if resp.status_code == 200:
            return resp.output["embeddings"][0]["embedding"]
        else:
            raise RuntimeError(f"Embedding failed: {resp.message}")


def get_embeddings() -> DashScopeEmbeddings:
    return DashScopeEmbeddings()
