# 代码生成时间: 2025-08-26 01:07:44
# message_notification_system.py

# Import necessary libraries
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
import logging

# Initialize a logger
logger = logging.getLogger(__name__)

# Define a simple in-memory datastore for notifications
notifications = []

# Define the Notification model
class Notification:
    def __init__(self, message, recipient):
        self.message = message
        self.recipient = recipient

# Define the API endpoints
def send_notification(request):
    """
    API endpoint to send a notification.
    It receives a JSON payload containing the message and recipient's email.
    Returns a JSON response with the result of the operation.
    """
    try:
        data = request.json()
        message = data.get('message')
        recipient = data.get('recipient')

        if not message or not recipient:
            return JSONResponse(
                content={'error': 'Missing message or recipient'},
                status_code=HTTP_400_BAD_REQUEST
            )

        new_notification = Notification(message, recipient)
        notifications.append(new_notification)
        return JSONResponse(content={'message': 'Notification sent successfully'})
    except Exception as e:
        logger.error(f'Error sending notification: {e}')
        return JSONResponse(
            content={'error': 'Internal server error'},
            status_code=HTTP_500_INTERNAL_SERVER_ERROR
        )

def get_notifications(request):
    """
    API endpoint to retrieve all notifications.
    Returns a JSON response with the list of notifications.
    """
    return JSONResponse(content={'notifications': [
        {'message': notification.message, 'recipient': notification.recipient}
        for notification in notifications
    ]})

# Define the routes for the application
routes = [
    Route('/send-notification', send_notification, methods=['POST']),
    Route('/get-notifications', get_notifications, methods=['GET'])
]

# Create the application instance
app = Starlette(debug=True, routes=routes)

# Start the application
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
