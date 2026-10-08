# 企业 RAG 知识库问答系统 · Enterprise RAG Knowledge Base

> 基于 **LangChain** 的企业级 RAG（检索增强生成）知识库问答系统，支持多用户多会话、
> 流式对话、引用溯源与权限隔离。

<p>
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white">
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-backend-009688?logo=fastapi&logoColor=white">
  <img alt="React" src="https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=white">
  <img alt="LangChain" src="https://img.shields.io/badge/LangChain-RAG-1C3C3C">
  <img alt="ChromaDB" src="https://img.shields.io/badge/ChromaDB-vector%20store-FF6F00">
</p>

**English summary** — A multi-user RAG Q&A system on LangChain. FastAPI + React 18 +
TypeScript, ChromaDB as the vector store, SQLite for application data, JWT/bcrypt for auth.
Supports document ingestion (TXT / MD / PDF / DOCX / CSV / XLSX), SSE streaming answers and
**citation tracing** back to the source chunks, with admin-only knowledge-base management.

---

## 技术栈

| 层级 | 技术 |
| --- | --- |
| 大语言模型 | 阿里云百炼 DashScope API (qwen-plus) |
| 嵌入模型 | 阿里云百炼 text-embedding-v2 |
| RAG 框架 | LangChain + LangChain-Community |
| 后端框架 | FastAPI (Python) |
| 前端框架 | React 18 + TypeScript + Vite |
| UI 组件库 | Ant Design 5 |
| 向量数据库 | ChromaDB |
| 关系数据库 | SQLite |
| 认证 | JWT + bcrypt |

---

## 功能特性

- 知识库文档上传与管理（支持 TXT / MD / PDF / DOCX / CSV / XLSX）
- 流式 RAG 问答（SSE 实时推送）
- **引用来源展示**（知识库片段可追溯）
- 多用户多会话管理
- 历史对话持久化与恢复
- 用户注册 / 登录 / 修改密码
- 管理员权限隔离（仅 admin 可管理知识库）
- Markdown 渲染（支持表格产品对比）

---

## 🔐 安全说明（部署前必读）

本项目**不提供任何默认账号或默认密码**。管理员账号必须由你在首次部署时自行创建。

管理员凭据通过环境变量注入，请编辑 `backend/.env`：

```dotenv
# ---- LLM ----
DASHSCOPE_API_KEY=sk-your-api-key-here

# ---- 初始管理员（仅首次初始化时使用）----
ADMIN_USERNAME=admin
ADMIN_PASSWORD=<请设置一个强密码>

# ---- 安全 ----
JWT_SECRET=<请生成一个随机长字符串>
```

> ⚠️ **提醒**
> - `backend/.env` 已被 `.gitignore` 忽略，**不要**提交到仓库。
> - 首次初始化后建议尽快在系统内修改管理员密码。
> - 生产环境请额外配置 HTTPS、访问频率限制与数据库备份。
> - 若你曾在公开场合暴露过 admin 密码，请立即轮换。

---

## 快速启动

### 前置要求

- Python 3.10+
- Node.js 18+
- 阿里云百炼 API Key（[开通地址](https://bailian.console.aliyun.com/)）

### 1. 配置环境变量

复制 `.env.example` 为 `backend/.env`，填入 API Key 与管理员账号（见上方「安全说明」）。

### 2. 一键启动（Windows）

双击运行 `start.bat`，脚本会自动：

1. 创建 Python 虚拟环境并安装依赖
2. 安装前端 npm 依赖
3. 启动后端（http://localhost:8000）和前端（http://localhost:5173）

### 3. 手动启动

**后端：**

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**前端：**

```bash
cd frontend
npm install
npm run dev
```

### 4. 访问系统

- 前端页面：http://localhost:5173
- API 文档：http://localhost:8000/docs

---

## 使用指南

1. 用管理员账号登录 → 进入「知识库管理」→ 上传文档
2. 等待文档处理完成（状态变为「已索引」）
3. 进入「我的会话」→ 新建会话 → 开始提问
4. 回答会引用知识库来源，点击可查看原文片段
5. 普通用户注册后只能进行问答，无法访问知识库管理

---

## 项目结构

```text
├── backend/                 # FastAPI 后端
│   ├── app/
│   │   ├── api/             # API 路由
│   │   ├── models/          # ORM 模型
│   │   ├── schemas/         # Pydantic 模型
│   │   ├── services/        # 业务逻辑
│   │   ├── rag/             # RAG 管道组件
│   │   └── core/            # 安全与依赖
│   └── data/                # 运行时数据
├── frontend/                # React 前端
│   └── src/
│       ├── pages/           # 页面组件
│       ├── components/      # 可复用组件
│       ├── store/           # Zustand 状态
│       └── api/             # API 客户端
├── data/products/           # 示例电商商品数据
└── start.bat                # 一键启动脚本
```

---

## RAG 管道

```text
文档上传 (TXT/MD/PDF/DOCX/CSV/XLSX)
      ↓
文本抽取 → 分片 (chunking) → 向量化 (text-embedding-v2)
      ↓
ChromaDB 持久化
      ↓
用户提问 → 向量检索 Top-K → 拼接上下文 → qwen-plus 生成
      ↓
SSE 流式返回 + 引用片段 (citation tracing)
```

---

## API 概览

| 端点 | 方法 | 说明 | 权限 |
| --- | --- | --- | --- |
| `/api/auth/register` | POST | 用户注册 | 公开 |
| `/api/auth/login` | POST | 用户登录 | 公开 |
| `/api/auth/me` | GET | 当前用户信息 | 登录 |
| `/api/auth/change-password` | PUT | 修改密码 | 登录 |
| `/api/conversations` | GET/POST | 会话列表 / 新建 | 登录 |
| `/api/conversations/{id}` | GET/DELETE/PATCH | 会话操作 | 所有者 |
| `/api/conversations/{id}/messages` | POST | SSE 流式问答 | 所有者 |
| `/api/kb/documents` | GET/POST | 文档列表 / 上传 | admin |
| `/api/kb/documents/{id}` | GET/DELETE | 文档详情 / 删除 | admin |
| `/api/kb/stats` | GET | KB 统计 | admin |
| `/api/kb/reindex` | POST | 重建索引 | admin |
| `/api/health` | GET | 健康检查 | 公开 |

---

## 许可

仅供学习参考。
