# 代码生成时间: 2025-08-27 15:34:05
# system_performance_monitor.py
# A simple system performance monitoring tool using Starlette.

import psutil
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

# Define a function to get CPU usage
def cpu_usage() -> float:
    return psutil.cpu_percent(interval=1)

# Define a function to get memory usage
def memory_usage() -> dict:
    memory = psutil.virtual_memory()
    return {
        'total': memory.total,
        'available': memory.available,
        'used': memory.used,
        'percentage': memory.percent
    }

# Define a function to get disk usage
def disk_usage() -> dict:
    disk = psutil.disk_usage('/')
    return {
        'total': disk.total,
        'used': disk.used,
        'free': disk.free,
        'percentage': disk.percent
    }

# Define a function to get network usage
def network_usage() -> dict:
    network_io = psutil.net_io_counters()
    return {
        'bytes_sent': network_io.bytes_sent,
        'bytes_recv': network_io.bytes_recv
    }

# Define an endpoint to retrieve performance metrics
async def get_performance_metrics(request):
    try:
        cpu = cpu_usage()
        memory = memory_usage()
        disk = disk_usage()
        network = network_usage()
        response = {
            'cpu': cpu,
            'memory': memory,
            'disk': disk,
            'network': network
        }
        return JSONResponse(response)
    except Exception as e:
        return JSONResponse({'error': str(e)}, status_code=500)

# Create a Starlette application
app = Starlette(debug=True, routes=[
    Route('/', get_performance_metrics),
])

# Documentation for the / route
"""
GET /
Returns a JSON object containing system performance metrics.

Example response:
{
    "cpu": 5.0,
    "memory": {
        "total": 16777216,
        "available": 8192512,
        "used": 8587168,
        "percentage": 51.1
    },
    "disk": {
        "total": 250000000000,
        "used": 150000000000,
        "free": 100000000000,
        "percentage": 60.0
    },
    "network": {
        "bytes_sent": 1500000,
        "bytes_recv": 1000000
    }
}
"""
