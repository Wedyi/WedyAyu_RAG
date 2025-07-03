# 低代码RAG平台后端开发技术方案



本技术方案将根据提供的后端项目结构，详细规划开发步骤、完成先后顺序、采用的框架和实现方法。我们将遵循敏捷开发原则，分阶段迭代，确保核心功能的稳定性和可扩展性。

**Python 版本选择：** 推荐使用 **Python 3.10 或 3.11**。这些版本与主流的AI/ML库（如PyTorch、TensorFlow、Hugging Face Transformers）以及向量数据库客户端（如Pinecone、Weaviate、Milvus、Qdrant）具有良好的兼容性，能提供稳定的开发环境 [1, 2, 3, 4, 5, 6, 7, 8]。



## 1. 阶段划分与优先级



我们将开发过程划分为以下几个主要阶段，并标注其优先级和依赖关系：

- **阶段0：环境搭建与基础骨架 (高优先级，无前置依赖)**
- **阶段1：核心基础设施 (高优先级，依赖阶段0)**
- **阶段2：知识库管理与数据处理 (高优先级，依赖阶段1)**
- **阶段3：RAG核心引擎 (高优先级，依赖阶段2)**
- **阶段4：项目与工作流管理 (中优先级，依赖阶段1、3)**
- **阶段5：应用执行与调试 (中优先级，依赖阶段3、4)**
- **阶段6：用户认证与授权 (中优先级，可并行或在阶段1后开始)**
- **阶段7：测试与部署 (贯穿始终，并在各阶段完成后进行)**



## 2. 详细开发技术方案





### 阶段0：环境搭建与基础骨架



**目标：** 搭建开发环境，初始化项目结构，并确保 FastAPI 应用能够启动。

**完成顺序：** 1

**涉及模块：**

- `main.py`
- `requirements.txt`
- `.env`
- `backend/` 目录结构

**框架与方法：**

- **FastAPI：** 作为高性能的Web框架，用于构建API服务 [3]。
- **Docker/Docker Compose：** 用于容器化开发环境，确保环境一致性 [11, 14]。
- **Poetry/Pipenv (可选)：** 用于依赖管理，替代 `pip` 提高效率。

**实现内容：**

1. **创建项目目录结构：** 按照提供的结构创建所有空目录和文件。
2. **初始化 `requirements.txt`：** 添加 `fastapi`, `uvicorn[standard]`, `python-dotenv` 等基础依赖。
3. **配置 `.env`：** 放置基础环境变量，如 `DATABASE_URL` (暂定为本地PostgreSQL)。
4. **`main.py` 初始化：** 编写 FastAPI 应用的最小启动代码，包含一个简单的根路由。
5. **Docker Compose 配置：** 编写 `docker-compose.yml` 文件，包含 FastAPI 服务和 PostgreSQL 数据库服务。
6. **基础测试：** 确保 FastAPI 应用能在 Docker 环境中成功启动并响应。



### 阶段1：核心基础设施



**目标：** 建立数据库连接、配置管理和基础安全组件。

**完成顺序：** 2 (依赖阶段0)

**涉及模块：**

- `app/core/config.py`
- `app/core/security.py`
- `app/db/session.py`
- `app/models/user.py`, `project.py`, `knowledge_base.py` (仅模型定义)
- `app/schemas/user.py`, `project.py`, `token.py` (仅Schema定义)
- `app/crud/` (基础CRUD接口)

**框架与方法：**

- **SQLAlchemy：** 作为ORM，用于数据库交互 [3]。
- **Pydantic：** 用于数据校验和序列化/反序列化 [3]。
- **Passlib：** 用于密码哈希（如 `bcrypt`）[8]。
- **PyJWT：** 用于JWT令牌的生成和校验。

**实现内容：**

1. **`app/core/config.py`：** 定义 `Settings` 类，使用 `Pydantic BaseSettings` 从环境变量加载配置，如数据库URL、JWT密钥等。
2. **`app/db/session.py`：** 配置 SQLAlchemy 引擎和会话，实现数据库连接池管理。
3. **`app/models/`：** 定义 `User`, `Project`, `KnowledgeBase` 的 SQLAlchemy 模型，包含基本字段和关系。
4. **`app/schemas/`：** 定义 `UserCreate`, `UserResponse`, `ProjectCreate`, `ProjectResponse`, `KnowledgeBaseCreate`, `KnowledgeBaseResponse`, `Token` 等 Pydantic Schema，用于请求体校验和响应数据格式化。
5. **`app/core/security.py`：** 实现密码哈希（`hash_password`, `verify_password`）和JWT令牌的生成与解码（`create_access_token`, `decode_token`）。
6. **`app/crud/`：** 编写基础的 CRUD 操作接口，如 `create_user`, `get_user_by_email`, `create_project` 等，与 SQLAlchemy 模型交互。
7. **数据库迁移工具：** 引入 `Alembic` 进行数据库模式管理。



### 阶段2：知识库管理与数据处理



**目标：** 实现知识库的创建、文件上传、文档解析、分块和向量化，并与向量数据库集成。

**完成顺序：** 3 (依赖阶段1)

**涉及模块：**

- `app/models/knowledge_base.py` (完善)
- `app/schemas/knowledge_base.py` (完善)
- `app/services/knowledge_base_service.py`
- `app/services/rag_engine/data_loaders/`
- `app/services/rag_engine/vector_stores/`
- `app/api/v1/endpoints/knowledge_bases.py`
- `app/crud/` (知识库相关CRUD)

**框架与方法：**

- **LangChain/LlamaIndex (可选，作为内部工具)：** 用于简化文档加载、分块和向量化流程 [4]。
- **PyPDF2/python-docx/Pillow (图像处理) 等：** 用于文档解析。
- **Sentence Transformers/OpenAI Embeddings API：** 用于生成文本嵌入 [16, 17]。
- **选定的向量数据库客户端：** 如 `pinecone-client`, `weaviate-client`, `pymilvus`, `qdrant-client` [1, 6, 7, 8]。
- **Celery/Redis：** 用于异步处理耗时的文档解析和向量化任务 [3]。

**实现内容：**

1. **`app/services/knowledge_base_service.py`：**
   - **文件上传与存储：** 实现文件上传接口，将原始文件存储到本地文件系统或对象存储（如S3）。
   - **文档解析：** 根据文件类型调用 `data_loaders` 中的相应解析器（如PDF解析器、TXT解析器），提取文本内容。考虑集成OCR能力处理图像和扫描件 [10, 13]。
   - **智能分块：** 实现文本分块逻辑，支持可配置的分块策略（如固定大小、递归字符分割、基于语义的分块）。预留可视化预览和人工干预的接口（虽然前端实现，但后端需支持相关数据结构）[9, 10, 14]。
   - **向量化：** 调用选定的嵌入模型（如`all-MiniLM-L6-v2`或OpenAI Embeddings API）将分块后的文本转换为向量。
   - **向量数据库写入：** 调用 `vector_stores` 中的接口，将向量和元数据写入选定的向量数据库。
   - **异步处理：** 将文档解析和向量化等耗时操作放入Celery任务队列，避免API阻塞 [3]。
2. **`app/services/rag_engine/data_loaders/`：** 实现 `PDFLoader`, `TextLoader`, `URLLoader` 等具体加载器。
3. **`app/services/rag_engine/vector_stores/`：** 定义 `VectorStore` 接口，并实现具体向量数据库的客户端封装（如 `PineconeVectorStore`, `WeaviateVectorStore`），包含 `add_vectors`, `search_vectors` 等方法。
4. **`app/api/v1/endpoints/knowledge_bases.py`：** 实现知识库的创建、更新、删除、文件上传、文件解析状态查询等API端点。
5. **`app/crud/`：** 完善知识库及其关联文件的CRUD操作。



### 阶段3：RAG核心引擎



**目标：** 构建RAG工作流的执行器和可插拔的节点系统，实现LLM调用和检索逻辑。

**完成顺序：** 4 (依赖阶段2)

**涉及模块：**

- `app/services/rag_engine/graph_executor.py`
- `app/services/rag_engine/nodes/`
- `app/services/rag_engine/vector_stores/` (检索部分)
- `app/core/config.py` (LLM配置)

**框架与方法：**

- **FastAPI/Pydantic：** 用于定义节点输入输出Schema。
- **Python标准库：** 用于图遍历和执行逻辑。
- **Hugging Face Transformers/OpenAI API/Ollama客户端：** 用于LLM调用 [4, 5, 21]。

**实现内容：**

1. **`app/services/rag_engine/nodes/base_node.py`：** 定义 `BaseNode` 抽象基类，包含 `execute` 抽象方法，以及 `input_schema`, `output_schema` 等属性。
2. **`app/services/rag_engine/nodes/input_node.py`：** 实现 `InputNode`，作为工作流的入口，接收用户查询。
3. **`app/services/rag_engine/nodes/retrieval_node.py`：**
   - 实现 `RetrievalNode`，接收用户查询和知识库ID。
   - 调用 `vector_stores` 中的 `search_vectors` 方法进行向量检索。
   - 实现混合搜索（关键词+向量）和重排序逻辑 [1, 8, 13]。
   - 返回检索到的相关文档片段和元数据（用于引用）。
4. **`app/services/rag_engine/nodes/llm_node.py`：**
   - 实现 `LLMNode`，接收提示模板和上下文（来自检索节点）。
   - 封装对不同LLM（OpenAI、Hugging Face本地模型等）的调用逻辑。
   - 支持LLM参数配置（温度、最大令牌数等）。
   - 处理LLM响应，包括流式输出。
5. **`app/services/rag_engine/nodes/parser_node.py`：** 实现 `ParserNode`，用于在RAG工作流中对特定文本进行二次解析或格式化。
6. **`app/services/rag_engine/graph_executor.py`：**
   - 实现 `GraphExecutor` 类，负责解析工作流的JSON定义（图结构）。
   - 实现图遍历算法（如拓扑排序），按顺序执行节点。
   - 管理节点之间的数据传递和状态。
   - 处理错误和异常。
7. **LLM配置：** 在 `app/core/config.py` 中添加LLM相关的API密钥和默认模型配置。



### 阶段4：项目与工作流管理



**目标：** 实现项目（应用）的创建、保存、加载和版本控制，以及工作流（Chatflow）的定义和存储。

**完成顺序：** 5 (依赖阶段1、3)

**涉及模块：**

- `app/models/project.py` (完善)
- `app/schemas/project.py` (完善)
- `app/services/project_service.py`
- `app/api/v1/endpoints/projects.py`
- `app/crud/` (项目相关CRUD)

**框架与方法：**

- **JSON：** 用于存储工作流的图结构定义。
- **SQLAlchemy：** 用于存储项目元数据和工作流JSON。

**实现内容：**

1. **`app/models/project.py`：** 完善 `Project` 模型，添加字段用于存储工作流的JSON定义（例如 `workflow_definition: JSONB`）。
2. **`app/schemas/project.py`：** 完善 `ProjectCreate`, `ProjectResponse` Schema，包含工作流定义字段。
3. **`app/services/project_service.py`：**
   - 实现 `create_project`, `get_project`, `update_project`, `delete_project` 等业务逻辑。
   - 处理工作流JSON定义的保存和加载。
   - 考虑版本控制机制（例如，每次保存都创建一个新版本或记录历史更改）。
4. **`app/api/v1/endpoints/projects.py`：** 实现项目的创建、列表、获取、更新、删除等API端点。
5. **`app/crud/`：** 完善项目相关的CRUD操作。



### 阶段5：应用执行与调试



**目标：** 提供API接口用于执行已定义的工作流，并支持调试功能。

**完成顺序：** 6 (依赖阶段3、4)

**涉及模块：**

- `app/api/v1/endpoints/app_execution.py`
- `app/services/rag_engine/graph_executor.py` (执行入口)

**框架与方法：**

- **FastAPI：** 用于定义执行API。
- **Python标准库：** 用于日志记录和调试信息收集。

**实现内容：**

1. **`app/api/v1/endpoints/app_execution.py`：**
   - **执行API：** 实现一个API端点（例如 `/execute_app/{project_id}`），接收用户输入和项目ID。
   - 从数据库加载指定项目的 `workflow_definition`。
   - 实例化 `GraphExecutor` 并传入工作流定义。
   - 调用 `GraphExecutor` 的执行方法，传入用户输入。
   - 返回RAG工作流的最终输出（LLM生成的响应，包含引用）。
   - **调试API (可选，但推荐)：** 实现一个API端点，允许用户在执行工作流时获取每个节点的中间输出和状态，便于调试。
2. **`app/services/rag_engine/graph_executor.py`：** 增强执行器，使其能够记录每个节点的输入、输出和执行时间，并在调试模式下返回这些信息。



### 阶段6：用户认证与授权



**目标：** 实现用户注册、登录、JWT令牌管理以及API路由的权限控制。

**完成顺序：** 7 (可并行于阶段1后开始，但API路由保护需等待相关API开发完成)

**涉及模块：**

- `app/models/user.py` (完善)
- `app/schemas/user.py`, `token.py` (完善)
- `app/core/security.py` (完善)
- `app/api/v1/endpoints/auth.py`
- `app/api/deps.py`
- `app/crud/` (用户相关CRUD)

**框架与方法：**

- **FastAPI Security：** 用于API密钥、OAuth2等认证方案 [3]。
- **JWT (JSON Web Tokens)：** 用于无状态认证。

**实现内容：**

1. **`app/models/user.py`：** 确保 `User` 模型包含 `hashed_password` 字段。
2. **`app/schemas/user.py`：** 定义 `UserCreate`, `UserLogin`, `UserResponse` 等Schema。
3. **`app/core/security.py`：** 完善 `create_access_token`, `verify_password` 等函数。
4. **`app/api/v1/endpoints/auth.py`：**
   - 实现用户注册 (`/register`)：接收用户名、邮箱、密码，哈希密码后保存用户。
   - 实现用户登录 (`/login`)：验证用户凭据，生成并返回JWT令牌。
   - 实现获取当前用户 (`/me`)：通过JWT令牌获取当前用户信息。
5. **`app/api/deps.py`：**
   - 实现 `get_current_user` 依赖函数，用于从请求头中解析JWT令牌，验证并获取当前认证用户。
   - 实现 `get_current_active_user` 等更细粒度的权限依赖。
6. **API路由保护：** 在所有需要认证的API路由上应用 `Depends(get_current_user)` 或 `Depends(get_current_active_user)`。



### 阶段7：测试与部署



**目标：** 编写全面的测试用例，并建立持续集成/持续部署（CI/CD）流程。

**完成顺序：** 贯穿始终，并在各阶段完成后进行

**涉及模块：**

- `tests/`
- `main.py` (生产配置)
- `.env` (生产配置)
- `requirements.txt` (生产依赖)
- CI/CD 配置文件 (如 `.github/workflows/main.yml` 或 `gitlab-ci.yml`)

**框架与方法：**

- **Pytest：** Python 单元测试和集成测试框架。
- **FastAPI TestClient：** 用于测试FastAPI应用。
- **Mocking库：** 如 `unittest.mock`，用于模拟外部服务（LLM API、向量数据库）。
- **Docker/Docker Compose：** 用于本地部署和测试环境。
- **CI/CD工具：** GitHub Actions, GitLab CI, Jenkins 等。

**实现内容：**

1. **单元测试：** 为 `core/`, `crud/`, `services/` 中的每个函数和类编写单元测试，确保其独立功能的正确性。
2. **集成测试：** 测试API端点、数据库交互、RAG工作流的端到端流程，确保各模块协同工作。
3. **性能测试 (可选，但推荐)：** 使用 `locust` 或 `JMeter` 对关键API和RAG执行进行负载测试，评估系统在并发请求下的性能 [7, 28]。
4. **安全测试 (可选，但推荐)：** 进行渗透测试、漏洞扫描，并测试认证授权机制的健壮性 [29, 7, 33]。
5. **AI模型评估：** 编写脚本评估RAG输出的质量（准确性、相关性、幻觉率），并集成到测试流程中 [24, 32]。
6. **CI/CD 管道：**
   - 配置 CI/CD 流程，在代码提交时自动运行测试。
   - 实现自动化部署脚本，将应用部署到开发、测试和生产环境。
   - 考虑蓝绿部署或金丝雀发布策略，确保平滑升级。
7. **监控与日志：** 集成日志库（如 `logging` 模块），并配置日志收集系统（如ELK Stack或Prometheus/Grafana），以便在生产环境中监控应用性能和错误 [7]。



## 3. 关键技术选型与考量



- **数据库：**
  - **关系型数据库：** PostgreSQL 是一个功能强大、稳定可靠的选择，适合存储用户、项目、知识库元数据和工作流定义（JSONB字段）[3]。
  - **向量数据库：** 初始阶段可选择易于本地部署和测试的开源方案如 **ChromaDB** 或 **Qdrant** [18]。随着项目发展和规模扩大，可考虑切换到更具扩展性的托管服务如 **Pinecone** 或 **Weaviate** [1, 6, 25]。
- **LLM集成：** 优先使用OpenAI API进行快速原型开发和测试。同时，预留接口支持Hugging Face Transformers库加载本地开源模型（如Llama系列）或通过Ollama进行本地推理，以提供灵活性和成本控制 [4, 5, 21]。
- **嵌入模型：** 初始可选择`all-MiniLM-L6-v2`等高性能、小尺寸的开源模型进行本地测试，或直接使用OpenAI的`text-embedding-3-small/large` API [16, 17]。
- **文档解析：** 对于PDF，可使用`PyPDF2`或`pypdf`。对于DOCX，可使用`python-docx`。对于图像，可考虑集成`Pillow`进行基础处理，或调用云服务（如Azure AI Vision API）进行OCR [10, 13]。
- **分块策略：** 初始实现基于字符或令牌的简单分块。后续迭代可引入更复杂的策略，如递归字符分割、基于语义的分块，并考虑RAGFlow的模板化分块思想 [9, 10, 14]。
- **RAG框架：** 尽管我们正在构建自己的RAG引擎，但可以参考或有限地使用LangChain/LlamaIndex等框架中的某些组件（如文档加载器、文本分割器），以加速开发，但核心逻辑仍由自定义节点实现 [4]。



## 4. 持续改进与迭代



- **用户反馈：** 建立机制收集用户反馈，并将其纳入产品待办事项列表，驱动后续迭代 [24, 20, 11]。
- **性能优化：** 持续监控系统性能，识别瓶颈并进行优化，例如引入缓存、优化数据库查询、并行处理等 [7, 28]。
- **功能扩展：** 根据用户需求和市场趋势，逐步增加新的节点类型、集成更多LLM/嵌入模型、支持更多数据源和高级RAG策略 [9, 10, 13]。
- **安全性：** 定期进行安全审计和漏洞扫描，及时修复安全问题 [29, 7, 33]。

通过以上详细的开发技术方案，我们可以有条不