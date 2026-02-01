# Renaiss Scout Bot (Python 版)

一个功能强大、有趣的 Telegram 机器人，专为 Renaiss 卡牌平台打造。

## 主要功能

1.  **智能聊天 (无限大脑)**: 使用免费的 `gemini-2.5-flash` 模型，你可以用自然语言和"小R"聊天，查询任何卡牌信息、评级知识等。
2.  **套利监控**: 自动扫描 Renaiss 市场，发现 FMV 套利机会，并通过 `/arbitrage` 命令展示给你。
3.  **有趣的人设**: "小R"是一个沉迷卡牌的"卡痴"，性格风趣，会像朋友一样和你聊天。

## 项目结构

```
renaiss-bot-py/
├── main.py             # 主程序入口
├── config.py           # 配置加载
├── requirements.txt    # Python 依赖
├── .env.example        # 环境变量模板
├── adapters/           # 外部服务适配器
│   ├── llm_adapter.py  # LLM (Gemini) 接口
│   └── renaiss_adapter.py # Renaiss API 接口
├── core/               # 核心处理逻辑
│   ├── chat_handler.py # 自然语言聊天处理
│   └── command_handler.py # 命令处理
├── jobs/               # 后台任务
│   └── scheduler.py    # 定时任务调度
├── models/             # 数据模型
│   └── database.py     # SQLAlchemy 数据库模型
├── services/           # 业务逻辑服务
│   ├── arbitrage_service.py # 套利计算
│   └── card_info_service.py # 卡牌信息查询
└── utils/              # 工具类
    └── logger.py       # 日志工具
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env`，并填入你的 Telegram Bot Token。

```bash
cp .env.example .env
# 编辑 .env 文件，填入 TELEGRAM_TOKEN
```

### 3. 运行 Bot

```bash
python main.py
```

## 重要链接

-   **作者推特**: [https://x.com/chen1904o](https://x.com/chen1904o?s=21)
-   **官方推特**: [https://x.com/renaissxyz](https://x.com/renaissxyz?s=21)
-   **官方 Discord**: [https://discord.gg/renaiss](https://discord.gg/renaiss)

## 技术栈

-   **语言**: Python 3.11+
-   **Telegram 库**: `python-telegram-bot`
-   **LLM**: `gemini-2.5-flash` (通过 OpenAI 兼容接口)
-   **数据库**: SQLite (异步, via `aiosqlite` & `SQLAlchemy`)
-   **任务调度**: `APScheduler`

---

Made with ❤️ by Manus AI
