# ApplicationResearchAgent

多Agent协作的应用研究系统，使用GLM API（OpenAI兼容），集成Tavily网络搜索，输出Markdown研究报告。

## 项目结构

```
ApplicationResearchAgent/
├── main.py                      # 入口文件，协调Agent工作流
├── agents/
│   ├── research_agent.py        # 研究Agent（Tavily搜索）
│   ├── writer_agent.py          # 写作Agent（生成报告）
│   └── judger_agent.py          # 判断Agent（评估质量）
├── utils/
│   ├── llm_client.py            # GLM API客户端（单例）
│   ├── output_manager.py        # Markdown输出管理器
│   └── response_parser.py       # LLM响应解析器
├── prompts/
│   ├── research_prompt.py       # 研究提示词模板
│   ├── writer_prompt.py         # 写作提示词模板
│   └── judger_prompt.py         # 判断提示词模板
├── config.py                    # 配置文件
├── requirements.txt             # 依赖列表
└── .env.example                 # 环境变量示例
```

## 工作流程

```
用户输入研究主题
    ↓
ResearchAgent (Tavily搜索) → 收集信息
    ↓
JudgerAgent (评估) → 信息是否充足?
    ↓ 否          ↓ 是
(继续搜索)    WriterAgent → 生成Markdown报告
                                    ↓
                            OutputManager → 保存文件
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

```bash
python main.py --topic "你的研究主题"
```

示例：
```bash
python main.py --topic "人工智能在医疗领域的应用"
```

### 4. 查看输出

生成的Markdown报告会保存在 `output/markdown/` 目录下，文件名格式为：
```
{研究主题}_{时间戳}.md
```

## 配置说明

在 `config.py` 中可以调整：
- `MAX_SEARCH_ROUNDS`: 最大搜索轮次（默认3轮）
- `MARKDOWN_DIR`: Markdown输出目录
- GLM和Tavily的API配置

## 依赖说明

- `openai`: GLM API兼容客户端
- `tavily-python`: 网络搜索
- `python-dotenv`: 环境变量管理

## 特性

- 多Agent协作架构
- 智能搜索循环（自动判断信息是否充足）
- 结构化Markdown报告输出
- 可复用的LLM客户端（单例模式）
- 完整的错误处理和重试机制
