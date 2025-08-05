# 代码生成时间: 2025-08-05 17:18:33
import os
import datetime
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from starlette.requests import Request
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.routing import Route
from starlette.app import Starlette

# 日志文件的存储路径
LOG_FILE_PATH = "./error_logs/"

# 确保日志文件路径存在
os.makedirs(LOG_FILE_PATH, exist_ok=True)

class ErrorLoggerMiddleware:
    """
    错误日志收集中间件
    """
    async def __call__(self, request: Request, call_next):
        response = await call_next(request)
        return response

    async def dispatch_exception(self, request: Request, exc: BaseException):
        """
        异常处理
        """
        # 记录错误信息到日志文件
        error_message = f"{request.client.host} - {request.url.path} - {str(exc)}"
        error_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_log = f"{error_timestamp} - {error_message}
"
        with open(os.path.join(LOG_FILE_PATH, "error_log.txt"), "a") as log_file:
            log_file.write(error_log)

        # 可以选择是否返回错误信息给客户端，这里为了安全起见返回HTTP 500
        return JSONResponse(
            content={"detail": "Internal Server Error"},
            status_code=HTTP_500_INTERNAL_SERVER_ERROR
        )

# 创建Starlette应用
app = Starlette(debug=True, middleware=[ErrorLoggerMiddleware()])

# 定义一个测试路由
@app.route("/error")
async def raise_error(request: Request) -> JSONResponse:
    """
    故意抛出一个异常，用于测试错误日志收集功能
    """
    raise ValueError("故意抛出的错误")

# 定义一个健康检查路由
@app.route("/health")
async def health_check(request: Request) -> JSONResponse:
    """
    健康检查接口
    """
    return JSONResponse(content={"status": "ok"}, status_code=HTTP_200_OK)

# 定义路由
routes = [
    Route("/error", endpoint=raise_error),
    Route("/health", endpoint=health_check),
]

# 应用路由
app.routes.extend(routes)

# 启动应用
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)