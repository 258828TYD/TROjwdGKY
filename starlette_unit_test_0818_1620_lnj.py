# 代码生成时间: 2025-08-18 16:20:38
import asyncio
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse
# 扩展功能模块
from starlette.testclient import TestClient
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from unittest import TestCase, main


# 定义一个简单的Starlette应用
class SimpleApp(Starlette):
    def __init__(self):
        routes = [
            Route("/", endpoint=lambda request: JSONResponse({"message": "Hello World"})),
        ]
        super().__init__(routes=routes)


# 实现单元测试
class TestSimpleApp(TestCase):
    def setUp(self):
        # 初始化TestClient
        self.app = TestClient(SimpleApp())

    def test_home_page(self):
# 扩展功能模块
        # 测试主页返回Hello World
# FIXME: 处理边界情况
        response = self.app.get("/")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json(), {"message": "Hello World"})

    def test_not_found(self):
        # 测试返回404 Not Found
        response = self.app.get("/nonexistent")
# NOTE: 重要实现细节
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)


# 运行测试
if __name__ == "__main__":
    main(argv=[''], verbosity=2, exit=False)
