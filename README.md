# myopenclaw

这是一个 OpenClaw AI 助手的工作空间，包含各种自动化工具和项目。

## 项目概述

### 1. 现代化 Todo List 应用
- 基于 Python + FastAPI + SQLite + 现代 HTML/CSS/JS
- 已部署至: https://upgraded-space-guide-55xj55q7wxfvp6p-18789.app.github.dev
- 功能包括: CRUD操作、任务状态管理、优先级分类、截止日期跟踪

### 2. X文章到Notion提取器 (notion_x_extractor)
一个可以从X（原Twitter）链接提取文章内容并自动保存到Notion数据库的工具。

#### 特性
- 自动提取X文章标题和内容
- 保存到指定的Notion数据库
- 支持自定义API配置
- 智能内容分割以适应Notion API限制

#### 使用方法
```bash
cd notion_x_extractor
python x_to_notion.py <X文章链接>
```

#### 更多信息
详见 `notion_x_extractor/HOW_TO_USE.md`

## 环境信息

- Python 3.12
- 已安装依赖: notion-client, requests, beautifulsoup4
- 工作目录: `/home/codespace/.openclaw/workspace`

## 许可证

此工作空间由 OpenClaw AI 助手维护。