import requests
from bs4 import BeautifulSoup
from notion_client import Client
import argparse
import sys
from urllib.parse import urlparse
import re
import os
from config import NOTION_CONFIG, HEADERS, EXTRACTION_CONFIG


class XArticleToNotion:
    def __init__(self, notion_token, database_id):
        """
        初始化X文章提取器
        
        :param notion_token: Notion API密钥
        :param database_id: Notion数据库ID
        """
        self.notion = Client(auth=notion_token)
        self.database_id = database_id

    def extract_article_from_x(self, url):
        """
        从X链接提取文章标题和内容
        
        :param url: X文章链接
        :return: 包含标题和内容的字典
        """
        # 获取网页内容
        headers = HEADERS
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except requests.RequestException as e:
            raise Exception(f"无法获取网页内容: {str(e)}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 尝试提取标题
        title = ""
        title_element = soup.find('meta', property='og:title') or soup.find('title')
        if title_element:
            title = title_element.get('content') or title_element.text
        else:
            # 如果找不到标题，则使用URL的一部分作为标题
            title = f"X Post - {urlparse(url).path.split('/')[-1][:50]}"

        # 尝试提取推文内容
        content = ""
        
        # 首先尝试查找X特有的元素
        # 使用配置文件中的选择器列表
        selectors = EXTRACTION_CONFIG['selectors']
        
        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                for element in elements:
                    text = element.get_text().strip()
                    if len(text) > len(content):
                        content = text
                break
        
        # 如果仍然没有找到内容，尝试从meta标签获取描述
        if not content:
            desc_element = soup.find('meta', attrs={'name': 'description'}) or \
                          soup.find('meta', property='og:description')
            if desc_element:
                content = desc_element.get('content', '')
        
        # 如果还是没有内容，尝试直接从body获取文本
        if not content:
            body_text = soup.get_text()
            # 只保留有意义的文本行
            lines = [line.strip() for line in body_text.splitlines() if len(line.strip()) > 10]
            content = '\n'.join(lines[:10])  # 只取前10行有意义的内容
        
        # 清理内容，移除多余的空白字符
        content = re.sub(r'\n\s*\n', '\n\n', content)  # 移除多余的空行
        content = content.strip()
        
        # 如果还是没有足够内容，至少包含URL
        if not content:
            content = f"内容来自: {url}\n\n未能提取到具体内容。"
        
        return {
            'title': title[:EXTRACTION_CONFIG['max_title_length']],  # 使用配置的最大长度
            'content': content
        }

    def save_to_notion(self, title, content):
        """
        将文章保存到Notion数据库
        
        :param title: 文章标题
        :param content: 文章内容
        :return: 创建的页面ID
        """
        # 准备页面内容
        children = []
        
        # 添加内容段落
        # 由于Notion API对单个块的长度有限制，我们需要分割长文本
        paragraphs = content.split('\n\n')
        for paragraph in paragraphs:
            if paragraph.strip():  # 忽略空段落
                # 如果段落太长，进一步分割
                max_chunk_size = EXTRACTION_CONFIG['max_content_chunk']  # 使用配置的最大块大小
                while len(paragraph) > max_chunk_size:  # Notion rich text content限制约为2000字符
                    chunk = paragraph[:max_chunk_size]
                    paragraph = paragraph[max_chunk_size:]
                    
                    children.append({
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": chunk
                                    }
                                }
                            ]
                        }
                    })
                
                # 添加剩余部分（如果有的话）
                if paragraph.strip():
                    children.append({
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": paragraph.strip()
                                    }
                                }
                            ]
                        }
                    })

        # 创建新页面
        new_page = self.notion.pages.create(
            parent={"database_id": self.database_id},
            properties={
                "Title": {
                    "title": [
                        {
                            "text": {
                                "content": title
                            }
                        }
                    ]
                }
            },
            children=children
        )
        
        return new_page['id']

    def process_x_link(self, url):
        """
        处理整个流程：从X链接提取内容并保存到Notion
        
        :param url: X文章链接
        :return: 结果信息
        """
        try:
            print(f"正在提取X链接内容: {url}")
            
            # 提取文章
            article_data = self.extract_article_from_x(url)
            
            print(f"提取完成 - 标题: {article_data['title'][:50]}...")
            
            # 保存到Notion
            page_id = self.save_to_notion(article_data['title'], article_data['content'])
            
            print(f"成功保存到Notion - 页面ID: {page_id}")
            
            return {
                'success': True,
                'title': article_data['title'],
                'notion_page_id': page_id,
                'message': f"成功将文章 '{article_data['title'][:30]}...' 保存到Notion"
            }
            
        except Exception as e:
            print(f"处理过程中出错: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': f"处理失败: {str(e)}"
            }


def main():
    parser = argparse.ArgumentParser(description='将X文章保存到Notion')
    parser.add_argument('url', nargs='?', help='X文章链接')
    parser.add_argument('--token', default=os.getenv('NOTION_TOKEN'), 
                       help='Notion API密钥 (可从环境变量NOTION_TOKEN获取)')
    parser.add_argument('--database-id', default=os.getenv('NOTION_DATABASE_ID'), 
                       help='Notion数据库ID (可从环境变量NOTION_DATABASE_ID获取)')
    
    args = parser.parse_args()
    
    if not args.url:
        print("请提供X文章链接")
        print("用法: python x_extractor.py <X文章链接>")
        sys.exit(1)
    
    # 检查是否提供了必需的API凭据
    if not args.token:
        print("错误: 必须提供Notion API密钥")
        print("方法1: 通过命令行参数 --token")
        print("方法2: 设置环境变量 NOTION_TOKEN")
        sys.exit(1)
    
    if not args.database_id:
        print("错误: 必须提供Notion数据库ID")
        print("方法1: 通过命令行参数 --database-id") 
        print("方法2: 设置环境变量 NOTION_DATABASE_ID")
        sys.exit(1)
    
    extractor = XArticleToNotion(args.token, args.database_id)
    result = extractor.process_x_link(args.url)
    
    print("\n" + "="*50)
    print(result['message'])
    
    if result['success']:
        print(f"页面ID: {result['notion_page_id']}")


if __name__ == "__main__":
    main()