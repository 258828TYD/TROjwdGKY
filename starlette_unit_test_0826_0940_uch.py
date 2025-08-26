# 代码生成时间: 2025-08-26 09:40:16
import asyncio
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.testclient import TestClient
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND
import pytest

# 示例路由和应用
async def homepage(request):  # type: ignore
    return JSONResponse({'message': 'Hello World'})

app = Starlette(debug=True, routes=[
    Route('/', homepage),
])

# 测试客户端
client = TestClient(app)

# 单元测试类
class TestStarletteApp:
    def test_homepage(self):  # type: ignore
        """测试主页返回状态码200和预期消息"""
        response = client.get('/')
        assert response.status_code == HTTP_200_OK
        assert response.json() == {'message': 'Hello World'}

    def test_nonexistent_page(self):  # type: ignore
        """测试不存在的页面返回状态码404"""
        response = client.get('/nonexistent')
        assert response.status_code == HTTP_404_NOT_FOUND

# 异步测试函数
@pytest.mark.asyncio
async def test_async_homepage():  # type: ignore
    """异步测试主页返回状态码200和预期消息"""
    async with client:  # type: ignore
        response = await client.get('/')
        assert response.status_code == HTTP_200_OK
        assert response.json() == {'message': 'Hello World'}

# 运行测试
if __name__ == '__main__':
    pytest.main(["-v", __file__])
