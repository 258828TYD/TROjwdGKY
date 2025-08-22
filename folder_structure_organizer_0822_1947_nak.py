# 代码生成时间: 2025-08-22 19:47:48
import os
import shutil
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.requests import Request
from typing import Dict, Any

# 文件夹结构整理器服务类
class FolderStructureOrganizerService:
    def __init__(self, root_path: str):
        self.root_path = root_path

    def organize(self) -> Dict[str, Any]:
        """
        整理文件夹结构，将所有文件移动到相应的子文件夹中。
        返回一个字典，包含整理的结果和错误信息。
        """
        try:
            files = os.listdir(self.root_path)
            organized = True
            message = "Files organized successfully."
            for file in files:
                file_path = os.path.join(self.root_path, file)
                if os.path.isfile(file_path):
                    file_extension = os.path.splitext(file)[1]
                    if not os.path.exists(os.path.join(self.root_path, file_extension[1:])):
                        os.makedirs(os.path.join(self.root_path, file_extension[1:]))
                    shutil.move(file_path, os.path.join(self.root_path, file_extension[1:], file))
            return {"success": organized, "message": message}
        except Exception as e:
            return {"success": False, "message": str(e)}

# Starlette 应用
app = Starlette(
    routes=[
        Route("/organize", endpoint=organize_folder_structure, methods=["POST"]),
    ],
)

# 处理整理文件夹结构的请求
async def organize_folder_structure(request: Request):
    root_path = "./"  # 设置根目录路径，可以根据需要修改
    service = FolderStructureOrganizerService(root_path)
    result = service.organize()
    return JSONResponse(result)
