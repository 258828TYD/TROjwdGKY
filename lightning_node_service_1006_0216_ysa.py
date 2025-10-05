# 代码生成时间: 2025-10-06 02:16:27
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request
from starlette.status import HTTP_404_NOT_FOUND
import logging


# 设置日志记录器
logger = logging.getLogger(__name__)


class LightningNodeService:
    """
    服务类，用于处理与闪电网络节点相关的请求。
    """
    def __init__(self):
        self.nodes = []  # 存储节点信息的列表

    def add_node(self, node_info):
        "