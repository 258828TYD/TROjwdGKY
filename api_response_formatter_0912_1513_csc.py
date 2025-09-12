# 代码生成时间: 2025-09-12 15:13:09
import json
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request


# 定义一个函数用于创建格式化的API响应
def format_api_response(request: Request, data: dict, status_code: int = 200) -> JSONResponse:
    """
    创建一个格式化的API响应。
    
    :param request: Starlette请求对象
    :param data: 响应数据
    :param status_code: HTTP状态码，默认为200
    :return: 格式化的JSON响应
    """
    response_data = {
        "status": status_code,
        "data": data
    }
    return JSONResponse(response_data, status_code=status_code)


# 定义一个中间件用于异常处理
async def exception_middleware(request: Request, call_next):
    """
    异常处理中间件。
    
    :param request: Starlette请求对象
    :param call_next: 调用下一个中间件或路由处理器的函数
    :return: 响应对象
    """
    try:
        response = await call_next(request)
    except StarletteHTTPException as exc:
        # 将Starlette异常转换为格式化的API响应
        return format_api_response(request, {"error": exc.detail}, exc.status_code)
    except Exception as exc:
        # 处理非Starlette异常
        return format_api_response(request, {"error": "Internal Server Error"}, 500)
    return response


# 示例路由
async def example_route(request: Request):
    """示例路由。
    
    :param request: Starlette请求对象
    :return: 格式化的API响应
    """
    # 这里可以添加业务逻辑
    data = {"message": "Hello, World!"}
    return format_api_response(request, data)