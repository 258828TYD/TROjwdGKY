# 代码生成时间: 2025-09-17 18:17:13
from starlette.applications import Starlette
from starlette.responses import JSONResponse, Response
from starlette.routing import Route
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK
from uuid import uuid4
import json

# 库存管理系统数据存储
inventory_data = {
    "items": []
}

class InventoryItem:
    """库存项类"""
    def __init__(self, item_id, product_name, quantity):
        self.item_id = item_id
        self.product_name = product_name
        self.quantity = quantity

    def to_dict(self):
        """将库存项转换为字典"""
        return {
            "item_id": self.item_id,
            "product_name": self.product_name,
            "quantity": self.quantity
        }

# 添加库存项的路由
async def add_inventory(request):
    """添加新的库存项"""
    try:
        data = await request.json()
        if not all(key in data for key in ("product_name", "quantity")):
            return JSONResponse(
                content="{'error': 'Missing product_name or quantity'}",
                status_code=HTTP_400_BAD_REQUEST
            )
        item = InventoryItem(str(uuid4()), data["product_name"], data["quantity"])
        inventory_data["items"].append(item.to_dict())
        return JSONResponse(content=item.to_dict(), status_code=HTTP_200_OK)
    except json.JSONDecodeError:
        return JSONResponse(
            content="{'error': 'Invalid JSON'}",
            status_code=HTTP_400_BAD_REQUEST
        )

# 获取所有库存项的路由
async def get_inventory(request):
    """获取所有库存项"""
    return JSONResponse(content=inventory_data, status_code=HTTP_200_OK)

# 获取单个库存项的路由
async def get_inventory_item(request):
    """通过ID获取单个库存项"""
    item_id = request.path_params.get("item_id")
    if item_id is None:
        return JSONResponse(
            content="{'error': 'Missing item_id'}",
            status_code=HTTP_400_BAD_REQUEST
        )
    item = next(
        (item for item in inventory_data["items"] if item["item_id"] == item_id),
        None
    )
    if item is None:
        return JSONResponse(
            content="{'error': 'Item not found'}",
            status_code=HTTP_404_NOT_FOUND
        )
    return JSONResponse(content=item, status_code=HTTP_200_OK)

# 更新库存项的路由
async def update_inventory(request):
    """更新库存项"""
    data = await request.json()
    item_id = request.path_params.get("item_id")
    if item_id is None:
        return JSONResponse(
            content="{'error': 'Missing item_id'}",
            status_code=HTTP_400_BAD_REQUEST
        )
    item = next(
        (item for item in inventory_data["items"] if item["item_id"] == item_id),
        None
    )
    if item is None:
        return JSONResponse(
            content="{'error': 'Item not found'}",
            status_code=HTTP_404_NOT_FOUND
        )
    if "product_name" in data:
        item["product_name"] = data["product_name"]
    if "quantity" in data:
        item["quantity"] = data["quantity"]
    return JSONResponse(content=item, status_code=HTTP_200_OK)

# 删除库存项的路由
async def delete_inventory_item(request):
    """删除库存项"""
    item_id = request.path_params.get("item_id")
    if item_id is None:
        return JSONResponse(
            content="{'error': 'Missing item_id'}",
            status_code=HTTP_400_BAD_REQUEST
        )
    item = next(
        (item for item in inventory_data["items"] if item["item_id"] == item_id),
        None
    )
    if item is None:
        return JSONResponse(
            content="{'error': 'Item not found'}",
            status_code=HTTP_404_NOT_FOUND
        )
    inventory_data["items"].remove(item)
    return JSONResponse(
        content="{'message': 'Item deleted successfully'}",
        status_code=HTTP_200_OK
    )

# 路由列表
routes = [
    Route("/inventory", endpoint=get_inventory, methods=["GET"]),
    Route("/inventory", endpoint=add_inventory, methods=["POST"]),
    Route("/inventory/{item_id}", endpoint=get_inventory_item, methods=["GET"]),
    Route("/inventory/{item_id}", endpoint=update_inventory, methods=["PUT"]),
    Route("/inventory/{item_id}", endpoint=delete_inventory_item, methods=["DELETE"]),
]

# 创建Starlette应用
app = Starlette(routes=routes, debug=True)