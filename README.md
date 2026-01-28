# Multi-Agent Starter

> 多Agent协作系统的快速入门参考项目

这是一个用于学习和参考的多Agent协作系统示例项目，展示了如何使用GLM API（OpenAI兼容）和Tavily网络搜索构建一个完整的应用研究系统。

## 项目结构

```
multi-agent-starter/
├── main.py                      # CLI入口文件
├── app.py                       # FastAPI Web入口
├── agents/
│   ├── orchestrator_agent.py    # 编排Agent（协调其他Agent）
│   ├── research_agent.py        # 研究Agent（Tavily搜索）
│   ├── writer_agent.py          # 写作Agent（生成报告）
│   └── judger_agent.py          # 判断Agent（评估质量）
├── utils/
│   ├── llm_client.py            # GLM API客户端（单例）
│   ├── output_manager.py        # Markdown输出管理器
│   ├── response_parser.py       # LLM响应解析器
│   └── temp_storage.py          # 临时存储管理器
├── prompts/
│   ├── research_prompt.py       # 研究提示词模板
│   ├── writer_prompt.py         # 写作提示词模板
│   └── judger_prompt.py         # 判断提示词模板
├── templates/
│   └── index.html               # Web界面模板
├── temp/                        # 临时存储目录（按任务ID组织）
├── output/                      # 输出目录
│   └── markdown/                # 最终Markdown报告
├── config.py                    # 配置文件
├── requirements.txt             # 依赖列表
└── .env.example                 # 环境变量示例
```

## 工作流程

```
用户输入研究主题
    ↓
OrchestratorAgent（编排Agent）
    ↓
ResearchAgent (Tavily搜索) → 收集信息
    ↓
JudgerAgent (评估) → 信息是否充足?
    ↓ 否          ↓ 是
(继续搜索)    WriterAgent → 生成Markdown报告
                                    ↓
                            OutputManager → 保存文件
                                    ↓
                            TempStorage → 保存中间步骤
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置API密钥

复制 `.env.example` 为 `.env` 并填入你的API密钥：

```bash
cp .env.example .env
```

编辑 `.env` 文件：
```env
GLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4/
GLM_API_KEY=your_glm_api_key_here
GLM_MODEL=glm-4-flash

TAVILY_API_KEY=your_tavily_api_key_here
```

### 3. 运行程序

#### 方式一：CLI命令行

```bash
python main.py --topic "你的研究主题"
```

示例：
```bash
python main.py --topic "人工智能在医疗领域的应用"
```

#### 方式二：Web界面

```bash
python app.py
```

然后访问 http://localhost:8000

### 4. 查看输出

#### 最终报告
生成的Markdown报告会保存在 `output/markdown/` 目录下，文件名格式为：
```
{研究主题}_{时间戳}.md
```

#### 临时文件
每个研究任务的中间步骤会保存在 `temp/{任务ID}/` 目录下，文件命名规范：
```
temp/
└── {任务ID}/
    ├── 00_initial_request.json
    ├── 01_research_request.json
    ├── 01_research_response.json
    ├── 02_judger_request.json
    ├── 02_judger_response.json
    ├── 03_research_request.json
    ├── 03_research_response.json
    ├── ...
    └── final_report.md
```

## 配置说明

在 `config.py` 中可以调整：
- `MAX_SEARCH_ROUNDS`: 最大搜索轮次（默认3轮）
- `MARKDOWN_DIR`: Markdown输出目录
- `TEMP_DIR`: 临时存储目录
- GLM和Tavily的API配置

## 依赖说明

- `openai`: GLM API兼容客户端
- `tavily-python`: 网络搜索
- `python-dotenv`: 环境变量管理
- `fastapi`: Web框架
- `uvicorn`: ASGI服务器
- `jinja2`: 模板引擎

## 特性

- 多Agent协作架构
- 智能搜索循环（自动判断信息是否充足）
- 结构化Markdown报告输出
- 可复用的LLM客户端（单例模式）
- 完整的错误处理和重试机制
- Web界面支持
- 临时存储管理（保存所有中间步骤）
- 编排Agent统一管理研究流程

## API说明

### POST /research

执行研究任务

**请求参数：**
- `topic`: 研究主题（form表单）

**响应示例：**
```json
{
  "success": true,
  "task_id": "AI医疗_20240101_120000",
  "topic": "人工智能在医疗领域的应用",
  "markdown_report": "# 研究报告\n...",
  "report_path": "output/markdown/AI医疗_20240101_120000.md",
  "temp_dir": "temp/AI医疗_20240101_120000",
  "steps": [...]
}
```

### GET /

返回Web界面
