# 代码生成时间: 2025-08-23 18:12:41
import uvicorn
from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
import plotly.graph_objects as go
import json

# 配置图表生成器类
class ChartGenerator:
    def __init__(self):
        pass

    def generate_chart(self, data):
        # 创建一个新的图表对象
        chart = go.Figure()
        
        # 根据输入的数据类型和结构生成图表
        if 'x' in data and 'y' in data:
            chart.add_trace(go.Scatter(x=data['x'], y=data['y']))
        elif 'x' in data and 'y' in data and 'z' in data:
            chart.add_trace(go.Scatter3d(x=data['x'], y=data['y'], z=data['z']))
        else:
            raise ValueError("Invalid data format for chart generation.")
        
        return chart.to_html(full_html=False)

# 创建一个Starlette应用
app = Starlette(
    debug=True,
)

# 路由和静态文件服务
app.add_middleware(StaticFiles, directory="static")

# 定义图表生成的API端点
@app.route("/generate", methods=["POST"])
async def generate_chart(request):
    # 获取请求体中的数据
    try:
        data = await request.json()
    except json.JSONDecodeError:
        return JSONResponse({"error": "Invalid JSON format"}, status_code=400)
    
    # 实例化图表生成器并生成图表
    chart_generator = ChartGenerator()
    chart_html = chart_generator.generate_chart(data)
    
    # 返回图表的HTML代码
    return HTMLResponse(chart_html)

# 运行应用
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
