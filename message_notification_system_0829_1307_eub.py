# 代码生成时间: 2025-08-29 13:07:50
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
import logging
import json

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 消息队列，用于存储待发送的消息
message_queue = []

class MessageNotificationSystem:
    def __init__(self):
        self.app = Starlette(debug=True)
        self.routes = [
            Route("/send", self.send_message, methods=["POST"]),
            Route("/receive", self.receive_message, methods=["GET"]),
        ]
        self.app.add_routes(routes=self.routes)

    def send_message(self, request):
        """
        发送消息到队列
        :param request: Starlette请求对象
        :return: JSON响应
        """
        try:
            message = request.json()
            if not message:
                return JSONResponse(
                    content={"error": "No message provided"}, status_code=HTTP_400_BAD_REQUEST
                )
            message_queue.append(message)
            logger.info("Message added to queue: %s", message)
            return JSONResponse(content={"message": "Message sent successfully"}, status_code=HTTP_200_OK)
        except json.JSONDecodeError:
            return JSONResponse(
                content={"error": "Invalid JSON format"}, status_code=HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error("Error sending message: %s", str(e))
            return JSONResponse(content={"error": "Failed to send message"}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

    def receive_message(self, request):
        """
        从队列中获取消息
        :param request: Starlette请求对象
        :return: JSON响应
        """
        try:
            if not message_queue:
                return JSONResponse(
                    content={"error": "No messages in queue"}, status_code=HTTP_400_BAD_REQUEST
                )
            message = message_queue.pop(0)
            logger.info("Message received from queue: %s", message)
            return JSONResponse(content={"message": message}, status_code=HTTP_200_OK)
        except Exception as e:
            logger.error("Error receiving message: %s", str(e))
            return JSONResponse(content={"error": "Failed to receive message"}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

# 创建消息通知系统实例并运行
if __name__ == "__main__":
    notification_system = MessageNotificationSystem()
    uvicorn.run(notification_system.app, host="0.0.0.0", port=8000)