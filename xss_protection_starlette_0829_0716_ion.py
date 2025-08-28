# 代码生成时间: 2025-08-29 07:16:24
import starlette.responses
from starlette.routing import Route
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from html import escape


# 中间件类，用于处理XSS攻击防护
class XSSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # 调用下一个请求处理器
        response = await call_next(request)
        # 检查响应类型是否为HTML
        if 'text/html' in response.headers.get('Content-Type', ''):
            # 转义HTML标签
            response.body = escape(response.body).encode('utf-8')
        return response


# 示例路由和视图函数
async def homepage(request):
    # 模拟用户输入，可能包含XSS攻击代码
    user_input = "<script>alert('XSS')</script>"
    # 此处在实际应用中应该使用模板引擎或其他方式来避免XSS
    return starlette.responses.HTMLResponse(f"<html><body>Hello, {escape(user_input)}!</body></html>")


# 创建Starlette应用
app = Starlette(
    routes=[
        Route('/', homepage),
    ],
    middleware=[
        Middleware(XSSMiddleware),
    ],
)


# 运行应用的代码（在实际部署时使用ASGI服务器运行）
# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app, host='0.0.0.0', port=8000)
