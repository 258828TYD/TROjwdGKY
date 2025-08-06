# 代码生成时间: 2025-08-06 13:45:13
# 引入必要的库
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.exceptions import HTTPException as StarletteHTTPException

# 定义一个异常类，用于处理数学计算中的错误
class MathError(Exception):
    pass

# 定义数学计算工具集
class MathCalculator:
    # 加法
    @staticmethod
    def add(x, y):
        return x + y

    # 减法
    @staticmethod
    def subtract(x, y):
        return x - y

    # 乘法
    @staticmethod
    def multiply(x, y):
        return x * y

    # 除法
    @staticmethod
    def divide(x, y):
        if y == 0:
            raise MathError("Cannot divide by zero")
        return x / y

# 创建一个Starlette应用
app = Starlette(debug=True)

# 定义路由和视图函数
@app.route("/add", methods=["GET"])
async def add(request):
    # 从查询参数中获取数值
    x = float(request.query_params.get("x", 0))
    y = float(request.query_params.get("y", 0))
    try:
        result = MathCalculator.add(x, y)
        return JSONResponse({"result": result})
    except MathError as e:
        raise StarletteHTTPException(status_code=400, detail=str(e))

@app.route="/subtract", methods=["GET"]
async def subtract(request):
    x = float(request.query_params.get("x", 0))
    y = float(request.query_params.get("y", 0))
    try:
        result = MathCalculator.subtract(x, y)
        return JSONResponse({"result": result})
    except MathError as e:
        raise StarletteHTTPException(status_code=400, detail=str(e))

@app.route="/multiply", methods=["GET"]
async def multiply(request):
    x = float(request.query_params.get("x", 0))
    y = float(request.query_params.get("y", 0))
    try:
        result = MathCalculator.multiply(x, y)
        return JSONResponse({"result": result})
    except MathError as e:
        raise StarletteHTTPException(status_code=400, detail=str(e))

@app.route="/divide", methods=["GET"]
async def divide(request):
    x = float(request.query_params.get("x", 0))
    y = float(request.query_params.get("y", 0))
    try:
        result = MathCalculator.divide(x, y)
        return JSONResponse({"result": result})
    except MathError as e:
        raise StarletteHTTPException(status_code=400, detail=str(e))

# 将视图函数添加到路由中
routes = [
    Route("/add", add),
    Route("subtract", subtract),
    Route("multiply", multiply),
    Route("divide", divide),
]
app.routes.routes.extend(routes)