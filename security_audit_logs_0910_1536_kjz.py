# 代码生成时间: 2025-09-10 15:36:38
import asyncio
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import logging
import json
import datetime

# 配置日志记录器
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)


# 安全审计日志中间件
class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            # 在请求之前记录日志
            LOGGER.info(f"Request {request.method} {request.url.path} started")
            
            response = await call_next(request)
            
            # 在请求之后记录日志
            LOGGER.info(f"Request {request.method} {request.url.path} completed with status {response.status_code}")
            
            return response
        except Exception as e:
            # 记录异常日志
            LOGGER.error(f"An error occurred: {str(e)}")
            raise

# 审计日志记录函数
async def log_audit(request: Request):
    try:
        # 获取请求信息
        request_info = {
            "method": request.method,
            "path": request.url.path,
            "query_params": dict(request.query_params),
            "headers": dict(request.headers),
            "body": await request.body(),
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        # 记录到日志
        LOGGER.info(f"Audit Log: {json.dumps(request_info)}")
        
        # 响应客户端
        return JSONResponse(content={"message": "Audit log recorded"}, status_code=200)
    except Exception as e:
        # 处理记录过程中的异常
        LOGGER.error(f"Error recording audit log: {str(e)}")
        return JSONResponse(content={"error": "Failed to record audit log"}, status_code=500)

# 创建Starlette应用
app = Starlette(middleware=[AuditMiddleware()], routes=[
    Route("/audit", endpoint=log_audit, methods=["POST"]),
])

# 运行应用（在实际部署时，这部分代码通常放在独立的脚本文件中）
if __name__ == "__main__":
    asyncio.run(app.run(host="0.0.0.0", port=8000))
