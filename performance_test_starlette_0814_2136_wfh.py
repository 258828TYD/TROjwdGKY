# 代码生成时间: 2025-08-14 21:36:26
import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.testclient import TestClient
import time
import requests
from concurrent.futures import ThreadPoolExecutor

"""
性能测试脚本，使用STARLETTE框架来创建一个简单的测试服务，
并通过多线程并发请求模拟性能测试。
"""

# 定义一个简单的测试服务
class TestService(Starlette):
    def __init__(self):
        super().__init__(routes=[
            Route('/', self.home),
        ])

    # 首页路由
    async def home(self, request):
        return JSONResponse({"message": "Hello, world!"})

# 定义性能测试函数
def performance_test(url, num_requests, max_concurrency):
    """
    性能测试函数
    :param url: 测试服务的URL
    :param num_requests: 总请求数
    :param max_concurrency: 最大并发数
    """
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=max_concurrency) as executor:
        futures = []
        for _ in range(num_requests):
            futures.append(executor.submit(requests.get, url))
        for future in futures:
            future.result()  # 等待每个请求完成
    end_time = time.time()
    print(f"Total requests: {num_requests}, Total time: {end_time - start_time} seconds")

# 主函数
def main():
    # 启动测试服务
    app = TestService()
    uvicorn.run(app, host="0.0.0.0", port=8000)
    try:
        # 运行性能测试
        url = "http://0.0.0.0:8000/"
        num_requests = 100  # 总请求数
        max_concurrency = 10  # 最大并发数
        performance_test(url, num_requests, max_concurrency)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()