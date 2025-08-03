# 代码生成时间: 2025-08-03 08:38:17
import os
import glob
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from typing import List, Dict

"""
批量文件重命名工具
"""

class RenameTool:
    def __init__(self, directory: str):
        self.directory = directory

    def rename_files(self, pattern: str, replacement: str) -> List[str]:
        """
        重命名指定目录下的所有文件
        :param pattern: 要替换的文本模式
        :param replacement: 新的文件名中替换后的文本
        :return: 重命名成功的文件列表
        """
        renamed_files = []
        for filename in glob.glob(os.path.join(self.directory, "*")):
            if os.path.isfile(filename):
                new_filename = filename.replace(pattern, replacement)
                try:
                    os.rename(filename, new_filename)
                    renamed_files.append(new_filename)
                except OSError as e:
                    print(f"Error renaming {filename} to {new_filename}: {e}")
        return renamed_files

    def get_files(self) -> List[str]:
        """
        获取指定目录下的所有文件
        :return: 文件名列表
        """
        return glob.glob(os.path.join(self.directory, "*"))


def rename_files_endpoint(request):
    directory = request.query_params.get("directory")
    pattern = request.query_params.get("pattern")
    replacement = request.query_params.get("replacement")
    if not directory or not pattern or not replacement:
        return JSONResponse(
            {
                "error": "Missing required query parameters"
            },
            status_code=HTTP_400_BAD_REQUEST,
        )
    rename_tool = RenameTool(directory)
    try:
        renamed_files = rename_tool.rename_files(pattern, replacement)
        return JSONResponse(
            {
                "message": "Files renamed successfully",
                "renamed_files": renamed_files,
            },
            status_code=HTTP_200_OK,
        )
    except Exception as e:
        return JSONResponse(
            {
                "error": str(e),
            },
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )

def list_files_endpoint(request):
    directory = request.query_params.get("directory")
    if not directory:
        return JSONResponse(
            {
                "error": "Missing required query parameters"
            },
            status_code=HTTP_400_BAD_REQUEST,
        )
    rename_tool = RenameTool(directory)
    files = rename_tool.get_files()
    return JSONResponse(
        {
            "files": files,
        },
        status_code=HTTP_200_OK,
    )

app = Starlette(
    routes=[
        Route("/rename", endpoint=rename_files_endpoint),
        Route("/files", endpoint=list_files_endpoint),
    ],
)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)