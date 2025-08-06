# 代码生成时间: 2025-08-07 00:27:44
import os
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.testclient import TestClient
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from starlette.routing import Route
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import requires

# 示例中间件，用于日志记录
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        print(f"请求方法：{request.method}, 请求路径：{request.url.path}")
        response = await call_next(request)
        print(f"响应状态码：{response.status_code}, 响应路径：{request.url.path}")
        return response

# 示例接口
@requires('authenticated')
async def test_endpoint(request):
    return JSONResponse(content={'message': 'Hello, World!'}, status_code=HTTP_200_OK)

# 示例应用
class AutomationTestApp(Starlette):
    def __init__(self):
        super().__init__(
            debug=True,
            routes=[
                Route('/', test_endpoint)
            ],
            middleware=[
                LoggingMiddleware()
            ]
        )

# 测试客户端
async def test_app_client():
    app = AutomationTestApp()
    client = TestClient(app)

    # 测试成功响应
    response = await client.get('/')
    assert response.status_code == HTTP_200_OK
    assert response.json() == {'message': 'Hello, World!'}

    # 测试未找到响应
    response = await client.get('/non-existent')
    assert response.status_code == HTTP_404_NOT_FOUND

    # 测试认证中间件
    response = await client.get('/')
    assert response.status_code == HTTP_401_UNAUTHORIZED

# 运行测试
if __name__ == '__main__':
    from starlette.config import load_dotenv
    from uvicorn import run

    load_dotenv()  # 从.env文件加载环境变量
    run(AutomationTestApp, host='0.0.0.0', port=8000)

    # 运行异步测试函数
    import asyncio
    asyncio.run(test_app_client())