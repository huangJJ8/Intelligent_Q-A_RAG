"""
检索器 — ChromaDB 语义相似搜索
"""

from langchain_core.documents import Document
from typing import List, Optional
from app.config import settings
from app.rag.vector_store import get_vectorstore


def retrieve_similar_chunks(
    query: str,
    top_k: Optional[int] = None,
    score_threshold: Optional[float] = None,
    product_category: Optional[str] = None,
) -> List[Document]:
    """从向量存储中检索与查询最相似的文档片段"""
    vectorstore = get_vectorstore()
    top_k = top_k or settings.RETRIEVAL_TOP_K
    score_threshold = score_threshold or settings.RETRIEVAL_SCORE_THRESHOLD

    # 构建过滤条件
    search_kwargs = {"k": top_k}
    if product_category:
        search_kwargs["filter"] = {"product_category": product_category}

    # 相似度搜索（带分数阈值过滤）
    results_with_scores = vectorstore.similarity_search_with_relevance_scores(
        query, k=top_k, **({"filter": search_kwargs["filter"]} if "filter" in search_kwargs else {})
    )

    # 过滤低于阈值的
    filtered = [
        (doc, score)
        for doc, score in results_with_scores
        if score >= score_threshold
    ]

    return [doc for doc, _ in filtered]


def retrieve_with_scores(
    query: str,
    top_k: Optional[int] = None,
    score_threshold: Optional[float] = None,
) -> List[tuple]:
    """检索并返回 (Document, score) 元组，用于引用展示"""
    vectorstore = get_vectorstore()
    top_k = top_k or settings.RETRIEVAL_TOP_K
    score_threshold = score_threshold or settings.RETRIEVAL_SCORE_THRESHOLD

    results_with_scores = vectorstore.similarity_search_with_relevance_scores(
        query, k=top_k
    )

    return [
        (doc, score)
        for doc, score in results_with_scores
        if score >= score_threshold
    ]
