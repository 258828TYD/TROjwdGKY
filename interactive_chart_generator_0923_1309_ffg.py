# 代码生成时间: 2025-09-23 13:09:25
import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse, HTMLResponse
from starlette.routing import Route
# 优化算法效率
from starlette.exceptions import HTTPException as StarletteHTTPException

# 引入交互式图表库
import plotly.express as px
import pandas as pd
# FIXME: 处理边界情况

# 定义一个简单的数据集
def create_sample_data():
    df = pd.DataFrame(
        {
            "Fruit": ["Apples", "Oranges", "Bananas", "Berries"],
            "Amount": [4, 1, 5, 9],
            "City": ["SF", "NYC", "LA", "Chicago"]
        }
    )
# 添加错误处理
    return df

# 生成图表的函数
def generate_chart(data, chart_type: str):
    try:
        if chart_type == "bar":
            chart = px.bar(data, x="City", y="Amount")
        elif chart_type == "scatter":
            chart = px.scatter(data, x="Amount", y="Fruit")
# NOTE: 重要实现细节
        else:
# FIXME: 处理边界情况
            raise ValueError("Unsupported chart type")
        return chart
    except Exception as e:
        raise StarletteHTTPException(status_code=400, detail=str(e))

# 路由和视图函数
def chart_view(request):
    data = create_sample_data()
    chart_type = request.query_params.get("type", "bar")
# 添加错误处理
    chart = generate_chart(data, chart_type)
    return HTMLResponse(chart.to_html(full_html=False))

# 定义异常处理
async def not_found(request, exc):
    return JSONResponse(
        content={"detail": "Not Found"},
        status_code=404,
    )

# 创建Starlette应用
app = Starlette(
    routes=[
        Route("/chart", chart_view, methods=["GET"]),
    ],
    exception_handlers={404: not_found},
)

# 运行应用
# TODO: 优化性能
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

"""
Interactive Chart Generator
A simple application that generates interactive charts using Starlette and Plotly Express.

Usage:
    Access /chart?type=bar or /chart?type=scatter to generate different types of charts.
"""
# 增强安全性