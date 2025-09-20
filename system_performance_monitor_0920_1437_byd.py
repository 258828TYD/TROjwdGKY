# 代码生成时间: 2025-09-20 14:37:34
import psutil
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR

"""
这是一个简单的系统性能监控工具，使用STARLETTE框架。
它提供了接口来获取系统的CPU、内存、磁盘和网络使用情况。
"""

# 定义一个类来封装性能监控功能
class SystemPerformanceMonitor:
    def __init__(self):
        pass

    def get_cpu_usage(self):
        """获取CPU使用率"""
        try:
            cpu_usage = psutil.cpu_percent()
            return cpu_usage
        except Exception as e:
            # 处理可能的异常
            return {"error": str(e)}

    def get_memory_usage(self):
        """获取内存使用情况"""
        try:
            memory = psutil.virtual_memory()
            memory_usage = memory.percent
            return memory_usage
        except Exception as e:
            # 处理可能的异常
            return {"error": str(e)}

    def get_disk_usage(self):
        """获取磁盘使用情况"""
        try:
            disk_usage = psutil.disk_usage('/')
            disk_usage_percent = disk_usage.percent
            return disk_usage_percent
        except Exception as e:
            # 处理可能的异常
            return {"error": str(e)}

    def get_network_usage(self):
        """获取网络使用情况"""
        try:
            network_io = psutil.net_io_counters()
            return {"sent": network_io.bytes_sent, "received": network_io.bytes_recv}
        except Exception as e:
            # 处理可能的异常
            return {"error": str(e)}

# 定义一个函数来处理CPU使用率的请求
async def cpu_usage(request):
    """获取CPU使用率的接口"""
    monitor = SystemPerformanceMonitor()
    result = monitor.get_cpu_usage()
    if isinstance(result, dict) and "error" in result:
        return JSONResponse(result, status_code=HTTP_500_INTERNAL_SERVER_ERROR)
    return JSONResponse(result, status_code=HTTP_200_OK)

# 定义一个函数来处理内存使用情况的请求
async def memory_usage(request):
    """获取内存使用情况的接口"""
    monitor = SystemPerformanceMonitor()
    result = monitor.get_memory_usage()
    if isinstance(result, dict) and "error" in result:
        return JSONResponse(result, status_code=HTTP_500_INTERNAL_SERVER_ERROR)
    return JSONResponse(result, status_code=HTTP_200_OK)

# 定义一个函数来处理磁盘使用情况的请求
async def disk_usage(request):
    """获取磁盘使用情况的接口"""
    monitor = SystemPerformanceMonitor()
    result = monitor.get_disk_usage()
    if isinstance(result, dict) and "error" in result:
        return JSONResponse(result, status_code=HTTP_500_INTERNAL_SERVER_ERROR)
    return JSONResponse(result, status_code=HTTP_200_OK)

# 定义一个函数来处理网络使用情况的请求
async def network_usage(request):
    """获取网络使用情况的接口"""
    monitor = SystemPerformanceMonitor()
    result = monitor.get_network_usage()
    if isinstance(result, dict) and "error" in result:
        return JSONResponse(result, status_code=HTTP_500_INTERNAL_SERVER_ERROR)
    return JSONResponse(result, status_code=HTTP_200_OK)

# 创建一个Starlette应用
app = Starlette(
    routes=[
        Route("/cpu", cpu_usage, methods=["GET"]),
        Route("/memory", memory_usage, methods=["GET"]),
        Route("/disk", disk_usage, methods=["GET"]),
        Route("/network", network_usage, methods=["GET"]),
    ],
)
