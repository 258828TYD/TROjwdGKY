# 代码生成时间: 2025-09-15 23:25:09
# system_performance_monitor.py
# A simple system performance monitor using Python and Starlette framework.

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK
import psutil
import platform
import datetime

# Util function to get system information
def get_system_info():
    system_info = {
        "system": platform.system(),
        "node": platform.node(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
    }
    return system_info

# Util function to get CPU information
def get_cpu_info():
    cpu_times = psutil.cpu_times_percent(interval=1)
    cpu_usage = psutil.cpu_percent(interval=1)
    return {
        "cpu_times_percent": cpu_times,
        "cpu_percent": cpu_usage,
    }

# Util function to get memory information
def get_memory_info():
    memory = psutil.virtual_memory()
    return {
        "total": memory.total,
        "available": memory.available,
        "used": memory.used,
        "percent": memory.percent,
    }

# Util function to get disk information
def get_disk_info():
    disk = psutil.disk_usage('/')
    return {
        "total": disk.total,
        "available": disk.free,
        "used": disk.used,
        "percent": disk.percent,
    }

# Util function to get network information
def get_network_info():
    network_io = psutil.net_io_counters()
    return {
        "bytes_sent": network_io.bytes_sent,
        