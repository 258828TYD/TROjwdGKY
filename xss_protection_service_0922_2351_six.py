# 代码生成时间: 2025-09-22 23:51:06
import starlette.requests
import starlette.responses
from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint
from starlette.status import HTTP_400_BAD_REQUEST
import html

class XSSProtectionService(HTTPEndpoint):
    async def get(self, request: starlette.requests.Request):
        """
        Handle GET requests to demonstrate XSS protection.
        This method will sanitise user input to prevent XSS attacks.
        """
        # Extract user input from request query parameters
        user_input = request.query_params.get('user_input')

        # Sanitize input to prevent XSS attacks
        sanitized_input = html.escape(user_input) if user_input else ''

        # Return a response with the sanitized input
        return starlette.responses.Response(f"Received sanitized input: {sanitized_input}")

    async def post(self, request: starlette.requests.Request):
        """
        Handle POST requests to demonstrate XSS protection.
        This method will sanitize user input from the request body to prevent XSS attacks.
        """
        try:
            # Extract user input from the request body
            data = await request.json()
            user_input = data.get('user_input')

            # Sanitize input to prevent XSS attacks
            sanitized_input = html.escape(user_input) if user_input else ''

            # Return a response with the sanitized input
            return starlette.responses.Response(f"Received sanitized input: {sanitized_input}")
        except ValueError:
            # Handle JSON decoding error
            return starlette.responses.Response(
                "Invalid JSON provided in the request body.",
                status_code=HTTP_400_BAD_REQUEST
            )

# Define a route for the XSS protection service
routes = [
    Route("/xss", endpoint=XSSProtectionService, methods=["GET", "POST"])
]
