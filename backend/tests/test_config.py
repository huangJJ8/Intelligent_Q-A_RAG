"""测试配置模块 — 验证所有配置项正确加载"""

import pytest
import os
from app.config import Settings, settings


class TestSettings:
    """配置管理 — 环境变量和默认值"""

    def test_默认值_正确设置(self):
        """场景：检查关键默认配置项"""
        assert settings.APP_NAME == "E-Commerce RAG Knowledge Base"
        assert settings.LLM_MODEL == "qwen-plus"
        assert settings.EMBEDDING_MODEL == "text-embedding-v2"
        assert settings.LLM_TEMPERATURE == 0.3
        assert settings.CHUNK_SIZE == 800
        assert settings.CHUNK_OVERLAP == 100
        assert settings.RETRIEVAL_TOP_K == 5
        assert settings.RETRIEVAL_SCORE_THRESHOLD == 0.4
        assert settings.CHAT_HISTORY_WINDOW == 10
        assert settings.MAX_UPLOAD_SIZE_MB == 50
        assert settings.JWT_ALGORITHM == "HS256"
        assert settings.JWT_EXPIRE_MINUTES == 1440

    def test_管理员种子数据_配置正确(self):
        """场景：管理员用户名和密码已配置"""
        assert settings.ADMIN_USERNAME == "admin"
        assert settings.ADMIN_PASSWORD == "123456"

    def test_DashScope_API_Key_已配置(self):
        """场景：百炼 API Key 不为空"""
        assert settings.DASHSCOPE_API_KEY != ""
        assert len(settings.DASHSCOPE_API_KEY) > 10
        assert settings.DASHSCOPE_API_KEY.startswith("sk-")

    def test_允许的文件扩展名_解析正确(self):
        """场景：ALLOWED_EXTENSIONS 正确解析为列表"""
        extensions = settings.allowed_extensions_list
        assert "txt" in extensions
        assert "md" in extensions
        assert "pdf" in extensions
        assert "docx" in extensions
        assert "csv" in extensions
        assert "xlsx" in extensions
        assert len(extensions) == 6

    def test_CORS_来源_解析正确(self):
        """场景：CORS_ORIGINS 正确解析为列表"""
        origins = settings.cors_origins_list
        assert "http://localhost:5173" in origins
        assert len(origins) >= 1

    def test_数据库URL_配置正确(self):
        """场景：DATABASE_URL 指向 SQLite"""
        assert "sqlite" in settings.DATABASE_URL
        assert "aiosqlite" in settings.DATABASE_URL

    def test_ChromaDB_配置正确(self):
        """场景：ChromaDB 持久化目录和集合名配置正确"""
        assert settings.CHROMA_PERSIST_DIR == "./data/chromadb"
        assert settings.CHROMA_COLLECTION_NAME == "ecommerce_kb"
