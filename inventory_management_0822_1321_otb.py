# 代码生成时间: 2025-08-22 13:21:17
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
import json
import uvicorn

# 假设的库存数据存储
inventory = {"items": []}

class InventoryManager:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        """添加物品到库存中"""
        self.items.append(item)
        return {
            "status": "success",
            "message": "Item added successfully"
        }

    def remove_item(self, item_id):
        """根据ID移除库存中的物品"""
        for item in self.items:
            if item.get("id") == item_id:
                self.items.remove(item)
                return {
                    "status": "success",
                    "message": "Item removed successfully"
                }
        return {
            "status": "error",
            "message": "Item not found"
        }

    def get_item(self, item_id):
        """根据ID获取物品信息"""
        for item in self.items:
            if item.get("id") == item_id:
                return {
                    "status": "success",
                    "data": item
                }
        return {
            "status": "error",
            "message": "Item not found"
        }

    def update_item(self, item_id, new_data):
        """根据ID更新物品信息"""
        for item in self.items:
            if item.get("id") == item_id:
                item.update(new_data)
                return {
                    "status": "success",
                    "message": "Item updated successfully"
                }
        return {
            "status": "error",
            "message": "Item not found"
        }

# 创建库存管理器实例
inventory_manager = InventoryManager()

# 星lette路由
routes = [
    Route("/inventory/add", endpoint=lambda request: add_item_endpoint(request, inventory_manager), methods=["POST"]),
    Route("/inventory/remove/{item_id}", endpoint=lambda request: remove_item_endpoint(request, inventory_manager), methods=["DELETE"]),
    Route("/inventory/{item_id}", endpoint=lambda request: get_item_endpoint(request, inventory_manager), methods=["GET"]),
    Route("/inventory/update/{item_id}", endpoint=lambda request: update_item_endpoint(request, inventory_manager), methods=["PUT"]),
]

# 添加物品到库存的端点
async def add_item_endpoint(request, inventory_manager):
    try:
        data = await request.json()
        item = {"id": data.get("id"), "name": data.get("name"), "quantity": data.get("quantity")}
        result = inventory_manager.add_item(item)
        return JSONResponse(result, status_code=HTTP_200_OK)
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

# 根据ID移除物品的端点
async def remove_item_endpoint(request, inventory_manager):
    try:
        item_id = request.path_params.get("item_id")
        result = inventory_manager.remove_item(item_id)
        return JSONResponse(result, status_code=HTTP_200_OK)
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

# 根据ID获取物品信息的端点
async def get_item_endpoint(request, inventory_manager):
    try:
        item_id = request.path_params.get("item_id")
        result = inventory_manager.get_item(item_id)
        if result.get("status") == "error":
            return JSONResponse(result, status_code=HTTP_404_NOT_FOUND)
        return JSONResponse(result, status_code=HTTP_200_OK)
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

# 根据ID更新物品信息的端点
async def update_item_endpoint(request, inventory_manager):
    try:
        item_id = request.path_params.get("item_id")
        data = await request.json()
        result = inventory_manager.update_item(item_id, data)
        return JSONResponse(result, status_code=HTTP_200_OK)
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

# 创建星lette应用
app = Starlette(routes=routes)

# 运行应用
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)