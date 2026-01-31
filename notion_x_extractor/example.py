#!/usr/bin/env python3

"""
示例脚本：展示如何使用X到Notion提取器
"""

from x_extractor import XArticleToNotion
import os


def example_usage():
    # 从环境变量获取API密钥和数据库ID
    NOTION_TOKEN = os.getenv('NOTION_TOKEN')
    DATABASE_ID = os.getenv('NOTION_DATABASE_ID')
    
    if not NOTION_TOKEN:
        print("错误: 未设置环境变量 NOTION_TOKEN")
        print("请先设置环境变量: export NOTION_TOKEN='your_token_here'")
        return
    
    if not DATABASE_ID:
        print("错误: 未设置环境变量 NOTION_DATABASE_ID")
        print("请先设置环境变量: export NOTION_DATABASE_ID='your_database_id_here'")
        return
    
    # 创建提取器实例
    extractor = XArticleToNotion(NOTION_TOKEN, DATABASE_ID)
    
    print("X文章到Notion提取器示例")
    print("="*40)
    
    # 示例链接（您可以用真实的X链接替换）
    sample_url = input("请输入X文章链接: ")
    
    if sample_url:
        result = extractor.process_x_link(sample_url)
        print(f"\n结果: {result['message']}")
    else:
        print("未提供链接")


if __name__ == "__main__":
    example_usage()