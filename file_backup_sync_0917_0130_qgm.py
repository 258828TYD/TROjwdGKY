# 代码生成时间: 2025-09-17 01:30:58
import os
import shutil
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

"""
文件备份和同步工具
使用STARLETTE框架提供RESTful API
"""

class BackupSyncApp(Starlette):
    def __init__(self, config):
        super().__init__(routes=[
            Route("/backup", endpoint=self.backup),
            Route("/sync", endpoint=self.sync),
        ])
        self.config = config

    def backup(self, request):
        """
        备份文件接口
        :param request: 请求对象
        :return: JSON响应
        """
        try:
            src = request.query_params.get("src")
            dst = request.query_params.get("dst")
            if not src or not dst:
                return JSONResponse({"error": "源文件和目标文件不能为空"}, status_code=400)
            shutil.copy(src, dst)
            return JSONResponse({"message": "文件备份成功"})
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)

    def sync(self, request):
        """
        同步文件接口
        :param request: 请求对象
        :return: JSON响应
        """
        try:
            src = request.query_params.get("src")
            dst = request.query_params.get("dst")
            if not src or not dst:
                return JSONResponse({"error": "源目录和目标目录不能为空"}, status_code=400)
            for root, dirs, files in os.walk(src):
                for file in files:
                    src_file = os.path.join(root, file)
                    dst_file = src_file.replace(src, dst)
                    os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                    shutil.copy2(src_file, dst_file)
            return JSONResponse({"message": "文件同步成功"})
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)

if __name__ == "__main__":
    config = {
        "debug": True,
    }
    app = BackupSyncApp(config)
    app.run(host="0.0.0.0", port=8000)