# 代码生成时间: 2025-08-24 20:42:45
import starlette.testclient
import pytest
# 扩展功能模块
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse, PlainTextResponse

# 定义一个简单的Starlette应用
def app():
    async def homepage(request):
        return PlainTextResponse('Hello, World!')

    return Starlette(debug=True, routes=[
        Route('/', homepage),
    ])

# 创建一个测试客户端
test_client = starlette.testclient.TestClient(app())

# 测试首页返回值
def test_homepage():
    response = test_client.get('/')
    assert response.status_code == 200
    assert response.text == 'Hello, World!'
# 扩展功能模块

# 测试错误的路由
def test_not_found():
    response = test_client.get('/nonexistent')
    assert response.status_code == 404

# 使用pytest的fixture来创建测试客户端
@pytest.fixture
def client():
# 增强安全性
    with starlette.testclient.TestClient(app()) as client:
        yield client

# 使用fixture测试首页
def test_homepage_with_fixture(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.text == 'Hello, World!'
# 扩展功能模块

# 使用fixture测试JSON响应
def test_json_response(client):
    async def json_route(request):
        return JSONResponse({'message': 'Hello, World!'})
# TODO: 优化性能

    # 添加新的路由
    app().add_route('/', json_route)

    response = client.get('/')
# NOTE: 重要实现细节
    assert response.status_code == 200
    assert response.json() == {'message': 'Hello, World!'}

# 清理路由
def teardown_module(module):
# NOTE: 重要实现细节
    app().routes.clear()  # 清除添加的路由以避免影响其他测试
# 扩展功能模块