"""
配置文件 - 存储API凭据和其他配置
"""

import os

# Notion API配置
NOTION_CONFIG = {
    'token': os.getenv('NOTION_TOKEN', ''),  # 从环境变量获取
    'database_id': os.getenv('NOTION_DATABASE_ID', '')  # 从环境变量获取
}

# 请求头配置
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 内容提取配置
EXTRACTION_CONFIG = {
    'max_title_length': 100,  # Notion标题最大长度
    'max_content_chunk': 2000,  # 单个内容块最大长度
    'selectors': [  # 用于提取内容的CSS选择器列表
        'article div[data-testid="tweetText"]',
        '[data-testid="tweetText"]',
        '.tweet-text',
        'p',
        'div[lang]',
        'meta[name="description"]',
        'meta[property="og:description"]'
    ]
}