# 代码生成时间: 2025-10-04 03:05:22
import starlette.applications
import starlette.routing
import starlette.responses
from starlette.requests import Request
import json
import logging

# 设置日志记录器
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 假设这是我们要远程调用的服务类
class RemoteService:
    def add(self, x, y):
        """远程服务加法操作"""
        return x + y

    def subtract(self, x, y):
        """远程服务减法操作"""
        return x - y

# RPC处理器，处理来自客户端的RPC请求
class RPCHandler:
    def __init__(self, service):
        self.service = service

    async def __call__(self, request: Request):
        try:
            # 获取JSON请求体
            data = await request.json()
            # 获取方法名和参数
            method_name = data.get('method')
            params = data.get('params')
            # 检查方法名
            if not method_name or not callable(getattr(self.service, method_name, None)):
                return starlette.responses.JSONResponse(
                    content={'error': 'Method not found'}, status_code=404
                )
            # 调用方法
            result = getattr(self.service, method_name)(*params)
            return starlette.responses.JSONResponse(content={'result': result})
        except Exception as e:
            logger.error(f'Error processing RPC request: {e}')
            return starlette.responses.JSONResponse(
                content={'error': str(e)}, status_code=500
            )

# 创建Starlette应用
app = starlette.applications Starlette()

# 设置路由
routes = starlette.routing.Routes([
    # 映射RPC处理器到 /rpc 路径
    {'path': '/rpc', 'endpoint': RPCHandler(RemoteService()), 'methods': ['POST']}
])

# 将路由添加到应用
app.add_routes(routes)

# 如果直接运行此文件，则启动Starlette应用
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)