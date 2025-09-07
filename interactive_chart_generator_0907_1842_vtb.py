# 代码生成时间: 2025-09-07 18:42:56
from fastapi import FastAPI, Form, Request
from starlette.responses import HTMLResponse
from pydantic import BaseModel
from typing import List

# 定义 FastAPI 应用
app = FastAPI()

# 定义请求体模型
class ChartRequest(BaseModel):
    title: str = Form(...)
    x_label: str = Form(...)
    y_label: str = Form(...)
    data: List[List[float]] = Form(...)

# 定义交互式图表生成器的 HTML 模板
CHART_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <canvas id="myChart" width="400" height="400"></canvas>
    <script>
        var ctx = document.getElementById('myChart').getContext('2d');
        var myChart = new Chart(ctx, {{
            type: 'line',
            data: {{
                labels: [],
                datasets: [{{
                    label: 'Data',
                    data: {data},
                    borderWidth: 1
                }}]
            }},
            options: {{
                scales: {{
                    x: {{
                        display: true,
                        title: {{
                            display: true,
                            text: '{x_label}'
                        }}
                    }},
                    y: {{
                        display: true,
                        title: {{
                            display: true,
                            text: '{y_label}'
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""

# 创建交互式图表生成器的端点
@app.post("/generate_chart/")
async def generate_chart(request: Request, chart_request: ChartRequest):
    # 从请求体中获取图表数据
    title = chart_request.title
    x_label = chart_request.x_label
    y_label = chart_request.y_label
    data = chart_request.data

    # 检查数据是否有效
    if not data or len(data[0]) == 0:
        return {
            "error": "Invalid data provided."
        }

    # 将数据转换为字符串格式，以便在 HTML 中使用
    data_str = ",".join(["[{}]".format(",".join(map(str, x))) for x in data])

    # 将图表数据插入 HTML 模板中
    chart_html = CHART_TEMPLATE.format(
        title=title,
        x_label=x_label,
        y_label=y_label,
        data=data_str
    )

    # 返回 HTML 响应
    return HTMLResponse(chart_html)

# 定义测试端点
@app.get("/")
async def read_root():
    return "Hello, visit /docs for interactive chart generator documentation!"
