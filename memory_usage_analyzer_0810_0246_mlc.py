# 代码生成时间: 2025-08-10 02:46:55
import psutil
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import platform

# 获取系统内存使用情况
def get_memory_usage():
    """
    Function to retrieve memory usage statistics.
    
    Returns:
        dict: A dictionary containing memory usage data.
    """
    try:
        memory = psutil.virtual_memory()
        return {
            'total': memory.total,
            'available': memory.available,
            'used': memory.used,
            'free': memory.free,
            'percent': memory.percent,
        }
    except Exception as e:
        return {'error': str(e)}

# Create the Starlette application
app = Starlette(debug=True)

# Define a route for memory usage endpoint
@app.route("/memory")
async def memory_usage(request):
    """
    Endpoint to get the memory usage of the system.
    
    Args:
        request (Request): The incoming request object.
    
    Returns:
        JSONResponse: A JSON response containing memory usage statistics.
    """
    memory_data = get_memory_usage()
    return JSONResponse(content=memory_data)

# Define the routes
routes = [
    Route("/memory", endpoint=memory_usage),
]

# Mount the routes on the application
app.add_routes(routes)

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
