# 代码生成时间: 2025-08-22 03:31:39
import logging
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.exceptions import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.exceptions import ExceptionMiddleware


# 设置日志配置
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class ErrorLogMiddleware(BaseHTTPMiddleware):
    """
    中间件用于捕获和记录异常
    """
    async def dispatch(self, request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            logger.error(f"Unhandled exception: {exc}")
            if isinstance(exc, HTTPException):
                return JSONResponse(
                    content={"detail": exc.detail},
                    status_code=exc.status_code,
                )
            return JSONResponse(
                content={"detail": "Internal Server Error"},
                status_code=500,
            )


app = Starlette(
    debug=True,
    routes=[
        Route("/error", lambda request: "This will raise an error"),
        # 可以添加更多路由
    ],
    middleware=[
        ExceptionMiddleware(),
        ErrorLogMiddleware(),
    ],
)

# 程序入口点
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)