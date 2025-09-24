# 代码生成时间: 2025-09-24 08:41:51
import psutil
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

"""
A Starlette application that provides an endpoint to check the memory usage of the system.
"""

# Define the route for memory usage analysis
routes = [
    Route("/mem_usage", endpoint=mem_usage_endpoint),
]

# Create the Starlette application
app = Starlette(debug=True, routes=routes)

"""
Error handling function to catch exceptions and return them as JSON responses.
"""
async def handle_exceptions(request, exc):
    """
    Handle exceptions and return a JSON response with error details.
    """
    return JSONResponse(
        {
            "error": str(exc),
            "message": "An error occurred while processing your request."
        },
        status_code=500
    )

"""
Endpoint function for memory usage analysis.
"""
async def mem_usage_endpoint(request):
    """
    Return the current memory usage of the system as a JSON response.
    """
    try:
        # Get the current memory usage statistics
        mem = psutil.virtual_memory()
        # Create a dictionary to store the memory usage data
        mem_usage_data = {
            "total": mem.total,
            "available": mem.available,
            "used": mem.used,
            "free": mem.free,
            "percent": mem.percent,
        }
        # Return the memory usage data as a JSON response
        return JSONResponse(mem_usage_data)
    except Exception as e:
        # Log the exception and return an error response
        print(f"Error: {e}")
        return JSONResponse(
            {
                "error": str(e),
                "message": "Failed to retrieve memory usage data."
            },
            status_code=500
        )

# Run the application if this module is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)