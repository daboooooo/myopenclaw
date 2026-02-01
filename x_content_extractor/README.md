# X内容提取器 (X Content Extractor)

一个成功绕过X（Twitter）反爬虫保护的内容提取工具，能够获取真实的推文内容并保存到Notion等平台。

## 背景问题

X（Twitter）实施了严格的反爬虫机制，当通过自动化工具访问时，会检测到JavaScript被禁用，并返回提示："我们检测到此浏览器中禁用了JavaScript。请启用JavaScript或切换到受支持的浏览器以继续使用x.com。"

## 解决方案

我们采用浏览器自动化技术成功绕过了这些保护措施：

### 1. 使用Playwright浏览器自动化
- 模拟真实浏览器环境
- 设置合适的用户代理和浏览器指纹
- 处理反自动化检测

### 2. 浏览器配置技巧
- 使用无头模式运行（适合服务器环境）
- 添加多个Chrome启动参数来模拟真实环境
- 隐藏自动化特征

### 3. 关键技术要点
- 使用 `addInitScript` 注入脚本来隐藏自动化特征
- 设置真实的用户代理、时区、语言等信息
- 使用 `waitForSelector` 等待页面元素加载
- 合理的超时设置

## 文件说明

- `x_content_scraper.js`: 核心JavaScript脚本，使用Playwright绕过反爬虫保护
- `x_to_notion_with_real_content.py`: Python脚本，整合内容提取和Notion保存功能
- `package.json`: Node.js依赖配置

## 安装依赖

```bash
npm install @playwright/test
npx playwright install chromium
```

## 使用方法

### 提取X内容
```bash
node x_content_scraper.js "https://x.com/username/status/xxxxx"
```

### 提取并保存到Notion
```bash
# 设置环境变量
export NOTION_TOKEN="your_notion_token"
export NOTION_DATABASE_ID="your_database_id"

# 运行提取和保存脚本
python x_to_notion_with_real_content.py "https://x.com/username/status/xxxxx" "Title_Property_Name"
```

## 技术细节

### JavaScript/Playwright配置要点
1. 启动参数设置：包含多个参数来模拟真实浏览器
2. 页面加载策略：使用 `domcontentloaded` 并设置适当超时
3. 元素选择器：使用X平台特有的选择器来定位内容
4. 反检测措施：通过 `addInitScript` 隐藏自动化特征

### 成功案例
我们成功提取了如下内容：
- 标题: "X 上的 宝玉：“当每个人都能指挥一支 AI 大军，什么能力最重要？” / X"
- 内容: "当每个人都能指挥一支 AI 大军，什么能力最重要？"

## 环境要求

- Node.js v14+
- Python 3.7+
- Playwright浏览器依赖
- 系统图形库（如libatk1.0-0等）

## 注意事项

1. 请遵守X的使用条款和robots.txt
2. 不要过于频繁地请求，避免被封IP
3. 个人使用，请勿用于大规模商业抓取
4. 代码仅供学习和技术研究使用

## 许可证

仅供个人学习和研究使用。