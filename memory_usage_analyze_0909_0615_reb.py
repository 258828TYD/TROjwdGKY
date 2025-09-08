# 代码生成时间: 2025-09-09 06:15:25
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import psutil
import os

"""
Memory Usage Analysis API using Starlette framework.
This application provides an endpoint to analyze and return the memory usage of the system.
"""

def get_memory_usage() -> dict:
    """
    Retrieves the memory usage statistics of the system.
    :return: A dictionary containing memory usage metrics.
    """
    try:
        # Get the memory usage statistics
        mem = psutil.virtual_memory()
        # Create a dictionary with memory usage metrics
        memory_usage = {
            "bytes": mem.total,
            "available_bytes": mem.available,
            "used_bytes": mem.used,
            "free_bytes": mem.free,
            "used_percent": mem.percent,
            "available_percent": 100 - mem.percent
        }
        return memory_usage
    except Exception as e:
        # Handle any exceptions that occur and return an error message
        return {"error": str(e)}

# Define the routes for the application
routes = [
    Route("/memory", endpoint=get_memory_usage, methods=["GET"])
]

# Create the Starlette application
app = Starlette(debug=True, routes=routes)

# Define the command line interface to run the application
if __name__ == "__main__":
    # Run the application on http://127.0.0.1:8000/ by default
    os.system("uvicorn memory_usage_analyze:app --reload")