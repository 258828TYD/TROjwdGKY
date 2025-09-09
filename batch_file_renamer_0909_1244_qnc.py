# 代码生成时间: 2025-09-09 12:44:10
import os
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import asyncio

"""
批量文件重命名工具 - Starlette API服务
"""

class FileRenamer:
    def __init__(self, directory):
        self.directory = directory

    async def rename_files(self, new_names):
        """
        批量重命名文件
        :param new_names: 一个列表，包含新文件名
        :return: None
        """
        for old_name, new_name in new_names.items():
            try:
                old_path = os.path.join(self.directory, old_name)
                new_path = os.path.join(self.directory, new_name)
                if not os.path.exists(old_path):
                    raise FileNotFoundError(f"File {old_name} not found in {self.directory}")
                os.rename(old_path, new_path)
            except Exception as e:
                return JSONResponse(content={"error": str(e)}, status_code=HTTP_400_BAD_REQUEST)
        return JSONResponse(content={"message": "Files renamed successfully"}, status_code=HTTP_200_OK)

async def rename_files_endpoint(request):
    """
    处理文件重命名请求
    """
    data = await request.json()
    directory = data.get("directory")
    new_names = data.get("new_names")

    if directory is None or new_names is None:
        return JSONResponse(content={"error": "Missing required parameters"}, status_code=HTTP_400_BAD_REQUEST)

    renamer = FileRenamer(directory)
    return await renamer.rename_files(new_names)

# 设置路由和创建Starlette应用
routes = [
    Route("/rename", rename_files_endpoint, methods=["POST"]),
]

app = Starlette(debug=True, routes=routes)

# 运行应用
if __name__ == "__main__":
    asyncio.run(app.start("0.0.0.0", 8000))
