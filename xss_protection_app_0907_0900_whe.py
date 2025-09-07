# 代码生成时间: 2025-09-07 09:00:26
from starlette.applications import Starlette
# NOTE: 重要实现细节
from starlette.responses import JSONResponse, HTMLResponse
from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
# FIXME: 处理边界情况
from starlette.status import HTTP_400_BAD_REQUEST
# 优化算法效率
import html

# Middleware to protect against XSS attacks
class XSSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        # Sanitize the response content to prevent XSS
        if response.body:
            response.body = self.sanitize(response.body)
        return response
    
    @staticmethod
    def sanitize(body):
# 扩展功能模块
        # Sanitizes the response body by escaping HTML
        sanitized_body = html.escape(body.decode('utf-8', 'replace')).encode('utf-8')
        return sanitized_body

# Route for testing XSS protection
async def xss_test(request: Request):
    try:
        # Simulate receiving user input
        user_input = request.query_params.get('input', '')
        # The middleware will sanitize this input before sending it in the response
        return HTMLResponse(f"Received input: {html.escape(user_input)}")
    except Exception as e:
        # Handle any errors that may occur
        return JSONResponse({'error': str(e)}, status_code=HTTP_400_BAD_REQUEST)
# 添加错误处理

# Create a Starlette application with the XSSMiddleware
app = Starlette(
    middleware=[
        Middleware(XSSMiddleware)
    ],
    routes=[
# NOTE: 重要实现细节
        Route("/test", endpoint=xss_test)
    ]
)

# Documentation for the application
"""
XSS Protection Application
This application demonstrates a simple middleware-based approach to prevent XSS attacks in a Starlette application.
# FIXME: 处理边界情况
It sanitizes all response bodies to escape HTML entities, thereby neutralizing potential XSS payloads.
"""