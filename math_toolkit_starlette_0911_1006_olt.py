# 代码生成时间: 2025-09-11 10:06:40
import starlette.applications
import starlette.responses
import starlette.routing
import starlette.requests
from starlette.exceptions import HTTPException as StarletteHTTPException


# 定义数学计算工具集的类
class MathToolKit:
    # 加法运算
    @staticmethod
    def add(x, y):
        try:
            return x + y
        except TypeError:
            raise StarletteHTTPException(status_code=400, detail="Both arguments must be numerical values.")

    # 减法运算
    @staticmethod
    def subtract(x, y):
        try:
            return x - y
        except TypeError:
            raise StarletteHTTPException(status_code=400, detail="Both arguments must be numerical values.")

    # 乘法运算
    @staticmethod
    def multiply(x, y):
        try:
            return x * y
        except TypeError:
            raise StarletteHTTPException(status_code=400, detail="Both arguments must be numerical values.")

    # 除法运算
    @staticmethod
    def divide(x, y):
        if y == 0:
            raise StarletteHTTPException(status_code=400, detail="Cannot divide by zero.")
        try:
            return x / y
        except TypeError:
            raise StarletteHTTPException(status_code=400, detail="Both arguments must be numerical values.")


# 创建Starlette路由和应用
def add(request: starlette.requests.Request):
    x = request.query_params.get("x")
    y = request.query_params.get("y")
    try:
        x, y = float(x), float(y)
        result = MathToolKit.add(x, y)
        return starlette.responses.JSONResponse(content={"result": result})
    except ValueError:
        raise StarletteHTTPException(status_code=400, detail="Invalid numerical input.")


def subtract(request: starlette.requests.Request):
    x = request.query_params.get("x")
    y = request.query_params.get("y")
    try:
        x, y = float(x), float(y)
        result = MathToolKit.subtract(x, y)
        return starlette.responses.JSONResponse(content={"result": result})
    except ValueError:
        raise StarletteHTTPException(status_code=400, detail="Invalid numerical input.")


def multiply(request: starlette.requests.Request):
    x = request.query_params.get("x")
    y = request.query_params.get("y")
    try:
        x, y = float(x), float(y)
        result = MathToolKit.multiply(x, y)
        return starlette.responses.JSONResponse(content={"result": result})
    except ValueError:
        raise StarletteHTTPException(status_code=400, detail="Invalid numerical input.")


def divide(request: starlette.requests.Request):
    x = request.query_params.get("x")
    y = request.query_params.get("y")
    try:
        x, y = float(x), float(y)
        result = MathToolKit.divide(x, y)
        return starlette.responses.JSONResponse(content={"result": result})
    except ValueError:
        raise StarletteHTTPException(status_code=400, detail="Invalid numerical input.")


# 路由列表
routes = [
    starlette.routing.Route("/add", endpoint=add, methods=["GET"]),
    starlette.routing.Route("/subtract", endpoint=subtract, methods=["GET"]),
    starlette.routing.Route("/multiply", endpoint=multiply, methods=["GET"]),
    starlette.routing.Route("/divide", endpoint=divide, methods=["GET"]),
]


# 应用实例
app = starlette.applications StarletteApplication(routes=routes)

"""
Simple Math Toolkit using Starlette framework.

This application provides basic arithmetic operations:
- Addition
- Subtraction
- Multiplication
- Division

All operations are exposed as RESTful API endpoints.
"""