# 代码生成时间: 2025-08-09 02:08:37
import asyncio
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.datastructures import MutableHeaders

# 缓存中间件
class CacheMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, cache_max_age=3600):
        super().__init__(app)
        self.cache_max_age = cache_max_age
        self.cache = {}

    async def dispatch(self, request, call_next):
        # 检查缓存中是否有数据
        if self.is_cacheable(request):
            cached_response = self.get_from_cache(request.url.path)
            if cached_response:
                return cached_response
        # 如果没有缓存则调用下一个中间件
        response = await call_next(request)
        # 如果响应可以被缓存，则添加到缓存中
        self.add_to_cache(request.url.path, response)
        return response

    def is_cacheable(self, request):
        # 这里可以添加更多的条件判断是否可缓存
        return True

    def get_from_cache(self, path):
        # 从缓存中获取数据
        return self.cache.get(path)

    def add_to_cache(self, path, response):
        # 将响应添加到缓存中
        self.cache[path] = response

# 示例路由
async def homepage(request):
    # 模拟一些逻辑处理
    await asyncio.sleep(1)
    return JSONResponse({'message': 'Hello World!'})

# 创建Starlette应用
app = Starlette(debug=True)
app.add_route('/', homepage, name='homepage')
app.add_middleware(CacheMiddleware, cache_max_age=3600)

# 启动应用
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)