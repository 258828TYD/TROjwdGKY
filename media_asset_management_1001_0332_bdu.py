# 代码生成时间: 2025-10-01 03:32:25
# media_asset_management.py
# 一个使用Starlette框架的媒体资产管理系统

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_400_BAD_REQUEST
import uvicorn
import os
import shutil

class MediaAssetManagement:
    """
    媒体资产管理类
    提供基本的CRUD操作：创建、读取、更新、删除媒体资产
    """
    def __init__(self, storage_path):
        self.storage_path = storage_path
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)

    def create_asset(self, filename, file_stream):
        try:
            file_path = os.path.join(self.storage_path, filename)
            with open(file_path, 'wb') as file:
                shutil.copyfileobj(file_stream, file)
            return {"message": "Asset created successfully"}
        except Exception as e:
            return {"error": f"Failed to create asset: {str(e)}"}

    def read_asset(self, filename):
        try:
            file_path = os.path.join(self.storage_path, filename)
            with open(file_path, 'rb') as file:
                return JSONResponse(content=file.read(), media_type='application/octet-stream')
        except FileNotFoundError:
            return {"error": "Asset not found"}, HTTP_404_NOT_FOUND
        except Exception as e:
            return {"error": f"Failed to read asset: {str(e)}"}

    def update_asset(self, filename, file_stream):
        try:
            file_path = os.path.join(self.storage_path, filename)
            with open(file_path, 'wb') as file:
                shutil.copyfileobj(file_stream, file)
            return {"message": "Asset updated successfully"}
        except Exception as e:
            return {"error": f"Failed to update asset: {str(e)}"}

    def delete_asset(self, filename):
        try:
            file_path = os.path.join(self.storage_path, filename)
            os.remove(file_path)
            return {"message": "Asset deleted successfully"}
        except FileNotFoundError:
            return {"error": "Asset not found"}, HTTP_404_NOT_FOUND
        except Exception as e:
            return {"error": f"Failed to delete asset: {str(e)}"}


# 路由和端点
routes = [
    Route("/asset/", endpoint=MediaAssetManagement("./assets"), methods=["GET", "POST"]),
    Route("/asset/{filename}", endpoint=MediaAssetManagement("./assets"), methods=["GET", "PUT", "DELETE"]),
]

# 创建Starlette应用程序
app = Starlette(debug=True, routes=routes)

# 启动服务器
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
