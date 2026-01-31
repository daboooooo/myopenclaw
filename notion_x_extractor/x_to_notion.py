#!/usr/bin/env python3
"""
便捷脚本：将X文章保存到Notion
使用环境变量中的API密钥和数据库ID
"""

import sys
import os
from x_extractor import XArticleToNotion


def main():
    if len(sys.argv) != 2:
        print("用法: python x_to_notion.py <X文章链接>")
        sys.exit(1)
    
    url = sys.argv[1]
    
    # 从环境变量获取API凭据
    token = os.getenv('NOTION_TOKEN')
    database_id = os.getenv('NOTION_DATABASE_ID')
    
    if not token:
        print("错误: 未设置环境变量 NOTION_TOKEN")
        print("请先设置环境变量: export NOTION_TOKEN='your_token_here'")
        sys.exit(1)
    
    if not database_id:
        print("错误: 未设置环境变量 NOTION_DATABASE_ID")
        print("请先设置环境变量: export NOTION_DATABASE_ID='your_database_id_here'")
        sys.exit(1)
    
    # 创建提取器实例
    extractor = XArticleToNotion(token, database_id)
    
    result = extractor.process_x_link(url)
    
    print("\n" + "="*50)
    print(result['message'])
    
    if result['success']:
        print(f"页面ID: {result['notion_page_id']}")


if __name__ == "__main__":
    main()