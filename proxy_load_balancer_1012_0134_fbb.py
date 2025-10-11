# 代码生成时间: 2025-10-12 01:34:21
import asyncio
from starlette.applications import Starlette
from starlette.responses import Response
from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.types import ASGIApp
import aiohttp
import urllib.parse
import random

# 定义后端服务器列表
BACKENDS = [
    {'url': 'http://backend1.com'},
    {'url': 'http://backend2.com'},
    {'url': 'http://backend3.com'},
]

# 负载均衡中间件
class LoadBalancerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 选择一个后端服务器
        backend = random.choice(BACKENDS)
        backend_url = backend['url']

        # 构造代理请求
        proxy_url = urllib.parse.urljoin(backend_url, request.url.path)
        headers = request.headers.copy()
        # 移除Host头部，防止后端服务器解析错误
        headers.pop('host', None)
        headers['Host'] = backend_url

        # 发送代理请求
        async with aiohttp.ClientSession() as session:
            async with session.request(request.method, proxy_url, headers=headers,
                                    data=request.body) as response:
                new_response = Response(
                    response.status, response.text(), media_type=response.headers['Content-Type'])
                for key, value in response.headers.items():
                    if key.lower() not in ['content-length', 'content-type', 'transfer-encoding', 'host']:
                        new_response.headers[key] = value
                return new_response

# 创建Starlette应用
app = Starlette(middleware=[Middleware(LoadBalancerMiddleware)], routes=[
    Route('/', endpoint=lambda request: Response('Hello, World!')),
])

# 运行应用
if __name__ == '__main__':
    asyncio.run(app.run())