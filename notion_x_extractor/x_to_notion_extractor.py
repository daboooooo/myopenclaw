import requests
from bs4 import BeautifulSoup
from notion_client import Client
import re
from urllib.parse import urlparse
import os


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
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 尝试提取标题 - X可能有不同的结构
        title = ""
        title_element = soup.find('meta', property='og:title') or soup.find('title')
        if title_element:
            title = title_element.get('content') or title_element.text
        else:
            # 如果找不到标题，则使用第一个文本块作为标题
            title = f"X Post - {urlparse(url).path.split('/')[-1]}"
        
        # 提取文章内容 - 对于X，通常是推文文本
        content = ""
        # 尝试查找主要文本内容
        text_elements = soup.find_all(['p', 'div', 'span'])
        
        for element in text_elements:
            text = element.get_text().strip()
            if len(text) > len(content) and not element.find('script'):
                content = text
        
        # 如果没有找到内容，尝试其他方式
        if not content:
            content_element = soup.find('meta', property='og:description')
            if content_element:
                content = content_element.get('content', '')
        
        # 如果仍然没有内容，尝试从页面直接提取文本
        if not content:
            body_text = soup.get_text()
            # 清理文本
            lines = [line.strip() for line in body_text.splitlines()]
            content = '\n'.join([line for line in lines if len(line) > 20])
            
        # 如果还是没有足够内容，至少包含URL
        if not content:
            content = f"Content extracted from: {url}"
        
        return {
            'title': title[:100],  # Notion标题有长度限制
            'content': content
        }

    def save_to_notion(self, title, content):
        """
        将文章保存到Notion数据库
        
        :param title: 文章标题
        :param content: 文章内容
        :return: 创建的页面ID
        """
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
            children=[
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": content
                                }
                            }
                        ]
                    }
                },
                {
                    "object": "block",
                    "type": "divider",
                    "divider": {}
                }
            ]
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
            
            print(f"提取完成 - 标题: {article_data['title']}")
            
            # 保存到Notion
            page_id = self.save_to_notion(article_data['title'], article_data['content'])
            
            print(f"成功保存到Notion - 页面ID: {page_id}")
            
            return {
                'success': True,
                'title': article_data['title'],
                'notion_page_id': page_id,
                'message': f"成功将文章 '{article_data['title']}' 保存到Notion"
            }
            
        except Exception as e:
            print(f"处理过程中出错: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': f"处理失败: {str(e)}"
            }


def main():
    """
    主函数 - 示例用法
    """
    import os
    
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
    
    extractor = XArticleToNotion(NOTION_TOKEN, DATABASE_ID)
    
    # 示例调用（替换为实际的X链接）
    x_url = input("请输入X文章链接: ")
    result = extractor.process_x_link(x_url)
    
    print(result['message'])


if __name__ == "__main__":
    main()