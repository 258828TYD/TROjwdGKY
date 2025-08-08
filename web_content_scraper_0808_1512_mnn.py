# 代码生成时间: 2025-08-08 15:12:07
import httpx
from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.routing import Route
from bs4 import BeautifulSoup
import logging


# 配置日志
logging.basicConfig(level=logging.INFO)


class WebContentScraper:
    def __init__(self, url):
        """初始化网页内容抓取工具
        
        Args:
        url (str): 要抓取的网页地址
        """
        self.url = url
        self.session = httpx.Client()

    def fetch_content(self):
        """抓取网页内容
        
        Returns:
        str: 网页的HTML内容
        Raises:
        Exception: 网络请求失败或其他错误
        """
        try:
            response = self.session.get(self.url)
            response.raise_for_status()  # 检查响应状态码
            return response.text
        except Exception as e:
            logging.error(f"Failed to fetch content: {e}")
            raise

    def parse_content(self, html):
        """解析网页内容
        
        Args:
        html (str): 网页的HTML内容
        
        Returns:
        dict: 包含网页主要内容的字典
        """
        soup = BeautifulSoup(html, 'html.parser')
        # 假设我们要抓取网页的标题和段落
        title = soup.title.string if soup.title else ''
        paragraphs = [p.get_text() for p in soup.find_all('p')]
        return {'title': title, 'paragraphs': paragraphs}


# 创建Starlette应用程序
app = Starlette(debug=True)

# 定义路由和处理函数
@app.route("/scrape", methods=["GET"])
async def scrape(request):
    url = request.query_params.get('scraper_url')
    if not url:
        return HTMLResponse("Please provide a URL to scrape", status_code=400)
    try:
        scraper = WebContentScraper(url)
        html = scraper.fetch_content()
        content = scraper.parse_content(html)
        return HTMLResponse(f"<h1>Scraped Content:</h1><p>Title: {content['title']}</p>" + \
                             "<p>Paragraphs:</p>" + \
                             "".join([f"<p>{p}</p>" for p in content['paragraphs']]))
    except Exception as e:
        return HTMLResponse(f"Error: {str(e)}", status_code=500)


# 运行应用程序
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)