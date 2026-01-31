# X文章到Notion提取器使用指南

这个工具可以从X（原Twitter）链接中提取文章内容并自动保存到您的Notion数据库中。

## 设置步骤

1. 确保您已在系统中安装Python 3.x
2. 安装依赖包：
   ```bash
   pip install -r requirements.txt
   ```

## 配置说明

本工具使用环境变量存储API配置：
- `NOTION_TOKEN`: 您的Notion Integration Token
- `NOTION_DATABASE_ID`: 您的Notion数据库ID
- `HEADERS`: HTTP请求头配置（在config.py中定义）
- `EXTRACTION_CONFIG`: 内容提取配置（在config.py中定义）

## 使用方法

### 方法1：使用环境变量（推荐）
```bash
export NOTION_TOKEN="your_token_here"
export NOTION_DATABASE_ID="your_database_id_here"
python x_to_notion.py <X文章链接>
```

### 方法2：使用便捷脚本配合 .env 文件
1. 复制示例配置文件：
   ```bash
   cp .env.example .env
   ```
2. 编辑 `.env` 文件，填入您的API凭据
3. 加载环境变量并运行：
   ```bash
   source .env
   python x_to_notion.py <X文章链接>
   ```

### 方法3：使用主提取脚本
```bash
python x_extractor.py <X文章链接> --token <您的Notion API密钥> --database-id <您的数据库ID>
```

### 方法4：使用环境变量运行主脚本
```bash
NOTION_TOKEN="your_token" NOTION_DATABASE_ID="your_db_id" python x_extractor.py <X文章链接>
```

## 如何获取Notion API密钥和数据库ID

### 获取Notion Integration Token
1. 访问 https://www.notion.so/my-integrations
2. 点击 "New integration"
3. 填写集成名称和描述
4. 选择您的工作区
5. 复制生成的 "Internal Integration Token"

### 获取Database ID
1. 在Notion中打开您的数据库
2. 点击右上角的 "Share" 按钮
3. 点击 "Copy link"
4. 从链接中提取数据库ID（链接格式为：https://www.notion.so/your-workspace-name/DATABASE-ID?p=...）

### 授权Integration访问数据库
1. 在您的Notion数据库页面点击 "Share" 按钮
2. 输入您的Integration名称
3. 添加Integration并授予读写权限

## 数据库要求

您的Notion数据库必须包含名为 "Title" 的属性，因为脚本使用此属性存储文章标题。

## 错误处理

- 如果遇到 "无法获取网页内容" 错误，可能是网络连接问题或X的反爬虫机制
- 如果遇到Notion API错误，请检查API密钥和数据库ID是否正确
- 如果内容提取不完整，可能是X页面结构变化导致，需要调整CSS选择器

## 安全注意事项

- 请妥善保管您的Notion API密钥
- 不要在公共场合分享您的API密钥
- 建议定期轮换API密钥