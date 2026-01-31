# X文章到Notion提取器

这个工具可以从X（原Twitter）链接中提取文章内容并自动保存到您的Notion数据库中。

## 使用方法

### 基本用法
```bash
export NOTION_TOKEN="your_notion_token"
export NOTION_DATABASE_ID="your_database_id"
python x_to_notion.py <X文章链接>
```

### 自定义API密钥和数据库ID
```bash
python x_extractor.py <X文章链接> --token <您的Notion API密钥> --database-id <您的数据库ID>
```

## 依赖项

- `requests`
- `beautifulsoup4`
- `notion-client`

## 注意事项

- 请确保您的Notion数据库中有名为"Title"的属性，因为这是脚本用来存储文章标题的
- 脚本会自动将提取的文章内容分成适当的段落保存到Notion中
- 如果遇到反爬虫机制，可能需要使用代理或等待一段时间再试

## 如何设置Notion数据库

1. 在Notion中创建一个新的数据库
2. 确保数据库有一个名为"Title"的标题属性
3. 共享数据库并启用API访问权限
4. 记下数据库ID（URL中的部分）和Integration Token