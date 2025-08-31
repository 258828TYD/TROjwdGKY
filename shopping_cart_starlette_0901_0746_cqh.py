# 代码生成时间: 2025-09-01 07:46:08
import json
from starlette.applications import Starlette
from starlette.responses import JSONResponse, Response
from starlette.routing import Route

# 模拟数据库中的购物车数据
class Cart:
    def __init__(self):
        self.items = {}

    def add_item(self, product_id, quantity):
        if product_id in self.items:
            self.items[product_id] += quantity
        else:
            self.items[product_id] = quantity
        return True

    def remove_item(self, product_id):
        if product_id in self.items:
            del self.items[product_id]
            return True
        return False

    def update_item(self, product_id, quantity):
        if product_id in self.items:
            if quantity <= 0:
                self.remove_item(product_id)
            else:
                self.items[product_id] = quantity
            return True
        return False

    def get_cart(self):
        return self.items

# 购物车API处理类
class ShoppingCartAPI:
    def __init__(self):
        self.cart = Cart()

    async def add_to_cart(self, request):
        try:
            data = await request.json()
            product_id = data.get('product_id')
            quantity = data.get('quantity')
            if not product_id or not quantity:
                return JSONResponse(
                    status_code=400, content="{"error": "Product ID and quantity are required."}"
                )
            success = self.cart.add_item(product_id, quantity)
            if success:
                return JSONResponse(content=self.cart.get_cart())
            else:
                return JSONResponse(
                    status_code=500, content="{"error": "Failed to add item to cart."}"
                )
        except json.JSONDecodeError:
            return JSONResponse(
                status_code=400, content="{"error": "Invalid JSON data."}"
            )

    async def remove_from_cart(self, request):
        try:
            data = await request.json()
            product_id = data.get('product_id')
            if not product_id:
                return JSONResponse(
                    status_code=400, content="{"error": "Product ID is required."}"
                )
            success = self.cart.remove_item(product_id)
            if success:
                return JSONResponse(content=self.cart.get_cart())
            else:
                return JSONResponse(
                    status_code=404, content="{"error": "Item not found in cart."}"
                )
        except json.JSONDecodeError:
            return JSONResponse(
                status_code=400, content="{"error": "Invalid JSON data."}"
            )

    async def update_cart(self, request):
        try:
            data = await request.json()
            product_id = data.get('product_id')
            quantity = data.get('quantity')
            if not product_id or not quantity:
                return JSONResponse(
                    status_code=400, content="{"error": "Product ID and quantity are required."}"
                )
            success = self.cart.update_item(product_id, quantity)
            if success:
                return JSONResponse(content=self.cart.get_cart())
            else:
                return JSONResponse(
                    status_code=404, content="{"error": "Item not found in cart."}"
                )
        except json.JSONDecodeError:
            return JSONResponse(
                status_code=400, content="{"error": "Invalid JSON data."}"
            )

# 创建Starlette应用
app = Starlette(
    routes=[
        Route('/add_to_cart', endpoint=ShoppingCartAPI().add_to_cart, methods=['POST']),
        Route('/remove_from_cart', endpoint=ShoppingCartAPI().remove_from_cart, methods=['POST']),
        Route('/update_cart', endpoint=ShoppingCartAPI().update_cart, methods=['POST']),
    ]
)

# 启动服务器时运行的代码
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
