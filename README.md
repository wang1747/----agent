# 🤖 AI 智能旅行助手

基于 **ReAct（Reasoning + Acting）模式** 的 LLM Agent，能够自动调用工具查询天气和推荐旅游景点。

## ✨ 功能

- 🌤️ **实时天气查询** — 通过 [wttr.in](https://wttr.in) API 获取任意城市的当前天气
- 🏯 **智能景点推荐** — 通过 [Tavily Search](https://tavily.com) 搜索引擎，根据天气条件推荐最合适的景点
- 🔄 **ReAct 推理循环** — 模型自主思考 → 调用工具 → 观察结果 → 继续推理，最多 3 轮迭代
- 🔌 **OpenAI 兼容接口** — 支持任意兼容 OpenAI API 的 LLM 服务（默认使用 DeepSeek）

## 📁 项目结构

```
.
├── main.py                    # 主程序入口，ReAct Agent 循环
├── OpenAICompatibleClient.py  # LLM 客户端封装（OpenAI 兼容接口）
├── tool.py                    # 工具注册表
├── tool1.py                   # get_weather — 天气查询工具
├── tool2.py                   # get_attraction — 景点推荐工具
├── system_prompt              # Agent 系统提示词
├── pyproject.toml             # 项目配置
├── .env.example               # 环境变量模板
└── .gitignore                 # Git 忽略规则
```

## 🚀 快速开始

### 1. 环境要求

- Python >= 3.11
- pip

### 2. 安装依赖

```bash
pip install openai python-dotenv tavily-python requests
```

### 3. 配置 API 密钥

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的 API 密钥：

```env
DEEPSEEK_API_KEY=你的DeepSeek密钥
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL_ID=deepseek-v4-flash
TAVILY_API_KEY=你的Tavily密钥
```

> ⚠️ `.env` 已被 `.gitignore` 忽略，不会被提交到 Git。**请勿将 API 密钥硬编码在代码中。**

### 4. 运行

```bash
python main.py
```

示例输出：

```
用户输入: 你好，请帮我查询一下今天北京的天气，然后根据天气推荐一个合适的旅游景点。
========================================
---循环1---
模型输出:
Thought: 我需要先查询北京的天气。
Action: get_weather(city="北京")

Observation: 北京的当前天气: Sunny, 温度: 32°C
========================================
---循环2---
模型输出:
Thought: 天气晴朗，适合户外活动，让我搜索推荐景点。
Action: get_attraction(city="北京", weather="Sunny")

Observation: 故宫、颐和园、长城...
========================================
---循环3---
模型输出:
Thought: 已获得足够信息，可以给出最终推荐。
Action: Finish[北京今天晴天32°C，推荐去故宫和颐和园...]

任务完成，最终答案: 北京今天晴天32°C，推荐去故宫和颐和园...
```

## 🧠 工作原理

本项目实现了经典的 **ReAct Agent** 架构：

```
用户输入 → [ Thought → Action → Observation ] × N → 最终答案
```

1. **Thought（思考）**：模型分析当前状态，决定下一步做什么
2. **Action（行动）**：调用具体工具或输出最终答案
3. **Observation（观察）**：工具返回结果，反馈给模型

模型会在 Thought 和 Action 之间循环，直到：
- 给出 `Finish[最终答案]` 结束任务
- 达到最大迭代次数（3 轮）

## 🔧 技术栈

| 组件 | 技术 |
|------|------|
| LLM | DeepSeek V4 Flash（可替换为任意 OpenAI 兼容模型） |
| 天气 API | [wttr.in](https://wttr.in) |
| 搜索 API | [Tavily Search](https://tavily.com) |
| LLM SDK | `openai` (OpenAI 兼容模式) |
| 环境变量 | `python-dotenv` |

## 🛠️ 自定义

### 更换 LLM 模型

编辑 `.env` 文件：

```env
DEEPSEEK_API_KEY=你的密钥
DEEPSEEK_BASE_URL=https://api.openai.com/v1      # 换成 OpenAI
DEEPSEEK_MODEL_ID=gpt-4o                          # 换成 GPT-4o
```

### 添加新工具

1. 创建 `tool3.py`，实现工具函数
2. 在 `tool.py` 中注册：`available_tools["新工具名"] = 新函数`
3. 在 `system_prompt` 中描述新工具的用法

### 调整迭代次数

修改 `main.py` 第 29 行 `for i in range(3)` 中的数字。
