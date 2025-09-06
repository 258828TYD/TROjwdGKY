# 代码生成时间: 2025-09-06 15:36:21
import os
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
import shutil

# 错误处理异常
class RenameError(Exception):
    pass

class BatchRenameTool:
    def __init__(self, directory):
        self.directory = directory
        # 检查目录是否存在
        if not os.path.isdir(directory):
            raise ValueError(f"The directory {directory} does not exist.")

    def rename_files(self, rename_pattern):
        # 检查rename_pattern是否为函数
        if not callable(rename_pattern):
            raise RenameError("rename_pattern must be a callable function.")

        for filename in os.listdir(self.directory):
            file_path = os.path.join(self.directory, filename)
            if os.path.isfile(file_path):
                try:
                    new_filename = rename_pattern(filename)
                    new_file_path = os.path.join(self.directory, new_filename)
                    # 重命名文件
                    shutil.move(file_path, new_file_path)
                except Exception as e:
                    raise RenameError(f"Error renaming file {filename}: {str(e)}")

# Starlette应用
app = Starlette(debug=True)

# 路由：批量重命名文件
@app.route("/rename", methods=["POST"])
async def rename(request):
    # 获取请求体
    body = await request.json()
    # 获取目录和重命名模式
    directory = body.get("directory")
    rename_pattern = body.get("rename_pattern")

    if not directory or not rename_pattern:
        return JSONResponse(
            content={"error": "Missing directory or rename_pattern in request body."},
            status_code=HTTP_400_BAD_REQUEST,
        )

    # 将rename_pattern字符串转换为函数
    try:
        rename_pattern = eval(rename_pattern)
    except Exception as e:
        return JSONResponse(
            content={"error": f"Invalid rename_pattern: {str(e)}"},
            status_code=HTTP_400_BAD_REQUEST,
        )

    try:
        # 实例化工具并重命名文件
        rename_tool = BatchRenameTool(directory)
        rename_tool.rename_files(rename_pattern)
    except (RenameError, ValueError) as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        return JSONResponse(
            content={"error": f"An unexpected error occurred: {str(e)}"},
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return JSONResponse(content={"message": "Files renamed successfully."}, status_code=HTTP_200_OK)

# 定义路由
routes = [
    Route("/rename", rename),
]

# 应用路由
app.add_routes(routes)