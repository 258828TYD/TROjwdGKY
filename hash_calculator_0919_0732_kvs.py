# 代码生成时间: 2025-09-19 07:32:04
import hashlib
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from typing import Optional

"""
哈希值计算工具
提供基于 HTTP 的哈希值计算服务。
"""

# 哈希计算函数
def calculate_hash(value: str, algorithm: str = 'sha256') -> str:
    """
    计算给定值的哈希值。
    
    参数：
    value: 需要计算哈希值的字符串
    algorithm: 哈希算法名称，默认为 'sha256'
    
    返回：
    计算得到的哈希值字符串
    
    异常：
    ValueError: 如果指定的算法不支持
    """
    try:
        hash_func = getattr(hashlib, algorithm)()
    except AttributeError:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
    hash_func.update(value.encode('utf-8'))
    return hash_func.hexdigest()

# HTTP 路由
routes = [
    Route('/hash', endpoint=hash_handler, methods=['POST']),
]

# HTTP 处理函数
async def hash_handler(request):
    "