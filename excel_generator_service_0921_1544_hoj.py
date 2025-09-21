# 代码生成时间: 2025-09-21 15:44:25
# excel_generator_service.py

"""
Excel表格自动生成器服务，使用STARLETTE框架创建API。
该服务能够接受HTTP请求，并生成指定格式的Excel文件。
"""

import asyncio
from starlette.applications import Starlette
from starlette.responses import FileResponse
from starlette.routing import Route
from starlette.exceptions import HTTPException as StarletteHTTPException
from openpyxl import Workbook
from openpyxl.styles import Alignment

# 定义生成Excel文件的函数
async def generate_excel(request):
    """
    根据请求参数生成Excel文件。
    :param request: Starlette请求对象
    :return: FileResponse对象，返回生成的Excel文件
    """
    try:
        # 创建工作簿
        wb = Workbook()
        # 选择默认的工作表
        ws = wb.active
        # 设置工作表标题
        ws.title = "Generated Excel"
        # 设置单元格文本对齐方式
        ws['A1'].alignment = Alignment(horizontal='center')
        # 添加一些示例数据
        ws.append(["Header 1", "Header 2", "Header 3"])
        ws.append(["Data 1", "Data 2", "Data 3"])
        # 将工作簿保存到临时文件
        temp_file = 'temp_excel.xlsx'
        wb.save(temp_file)
        # 返回文件响应
        return FileResponse(temp_file, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    except Exception as e:
        # 处理异常
        raise StarletteHTTPException(status_code=500, detail=str(e))

# 创建Starlette应用
app = Starlette(debug=True)

# 定义路由
app.add_route("/generate_excel", generate_excel, methods=["GET"])

# 启动服务
if __name__ == "__main__":
    asyncio.run(app.run(host="0.0.0.0", port=8000))
