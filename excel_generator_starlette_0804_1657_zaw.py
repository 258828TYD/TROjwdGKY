# 代码生成时间: 2025-08-04 16:57:25
import os
import tempfile
from starlette.applications import Starlette
from starlette.responses import FileResponse, JSONResponse
from starlette.routing import Route
from openpyxl import Workbook
from starlette.status import HTTP_500InternalServerError

# 定义一个简单的Excel生成器
class ExcelGenerator:
    def __init__(self, title):
        self.title = title
# NOTE: 重要实现细节
        self.workbook = Workbook()
        self.sheet = self.workbook.active
        self.sheet.title = title
# 添加错误处理

    def add_row(self, row_data):
        """
        向当前工作表添加一行数据
# 添加错误处理
        :param row_data: 一个列表，包含行中的数据
        """
        self.sheet.append(row_data)

    def save_to_file(self, file_path):
        """
        将Excel文档保存到指定路径
        :param file_path: 文件保存的路径
# 改进用户体验
        """
        self.workbook.save(file_path)
# TODO: 优化性能

    def generate_excel(self, data):
        """
        生成Excel文件
        :param data: 一个二维列表，包含所有行的数据
        """
        for row in data:
            self.add_row(row)
        return self

# 定义API路由
def get_excel(request):
    """
    提供一个GET API来生成Excel文件
    """
# NOTE: 重要实现细节
    try:
# 添加错误处理
        # 使用临时文件路径
        file_path = tempfile.mkstemp()[1]
# 增强安全性
        generator = ExcelGenerator("Sample Excel").generate_excel([["Name", "Age"], ["Alice", 30], ["Bob", 25]])
        generator.save_to_file(file_path)
        return FileResponse(file_path, filename="sample.xlsx", media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=HTTP_500InternalServerError)

# 创建Starlette应用并添加路由
app = Starlette(debug=True)
app.add_route("/excel", get_excel, methods=["GET"])
# 增强安全性

if __name__ == "__main__":
    # 运行应用
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)