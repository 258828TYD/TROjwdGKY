# 代码生成时间: 2025-07-31 05:18:44
# shopping_cart_app.py

"""Shopping Cart Application using Starlette framework."""

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_400_BAD_REQUEST
from starlette.requests import Request
import uuid

# In-memory store for shopping cart items
shopping_cart = {}

# Function to add item to the cart
def add_item_to_cart(cart_id, item):
    """Add an item to the shopping cart."""
    if cart_id not in shopping_cart:
        shopping_cart[cart_id] = []
    shopping_cart[cart_id].append(item)
    return HTTP_200_OK

# Function to remove item from the cart
def remove_item_from_cart(cart_id, item_id):
    """Remove an item from the shopping cart."""
    if cart_id in shopping_cart:
        try:
            shopping_cart[cart_id].remove(item_id)
            return HTTP_200_OK
        except ValueError:
            return HTTP_404_NOT_FOUND
    else:
        return HTTP_404_NOT_FOUND

# Function to get cart items
def get_cart_items(cart_id):
    """Get all items in the shopping cart."""
    return shopping_cart.get(cart_id, [])

# Endpoint to add an item to the cart
async def add_item(request: Request):
    """Add an item to the shopping cart via POST request."""
    data = await request.json()
    item = data.get('item')
    if not item:
        return JSONResponse({'detail': 'Item is required.'}, status_code=HTTP_400_BAD_REQUEST)

    cart_id = data.get('cart_id')
    if not cart_id:
        cart_id = str(uuid.uuid4())  # Generate a new cart ID if not provided

    status = add_item_to_cart(cart_id, item)
    return JSONResponse({'cart_id': cart_id, 'status': status}, status_code=status)

# Endpoint to remove an item from the cart
async def remove_item(request: Request):
    """Remove an item from the shopping cart via POST request."""
    data = await request.json()
    item_id = data.get('item_id')
    if not item_id:
        return JSONResponse({'detail': 'Item ID is required.'}, status_code=HTTP_400_BAD_REQUEST)

    cart_id = data.get('cart_id')
    if not cart_id:
        return JSONResponse({'detail': 'Cart ID is required.'}, status_code=HTTP_400_BAD_REQUEST)

    status = remove_item_from_cart(cart_id, item_id)
    return JSONResponse({'status': status}, status_code=status)

# Endpoint to get cart items
async def get_cart(request: Request):
    """Get all items in the shopping cart via GET request."""
    cart_id = request.path_params.get('cart_id')
    if not cart_id:
        return JSONResponse({'detail': 'Cart ID is required.'}, status_code=HTTP_400_BAD_REQUEST)

    cart_items = get_cart_items(cart_id)
    return JSONResponse({'cart_id': cart_id, 'items': cart_items}, status_code=HTTP_200_OK)

# Routes for the shopping cart application
routes = [
    Route('/cart/{cart_id}/items/', get_cart, methods=['GET']),
    Route('/add_item/', add_item, methods=['POST']),
    Route('/remove_item/', remove_item, methods=['POST']),
]

# Create the Starlette application
app = Starlette(debug=True, routes=routes)
