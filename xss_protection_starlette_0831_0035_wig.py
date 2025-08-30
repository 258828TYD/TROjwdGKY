# 代码生成时间: 2025-08-31 00:35:46
import re
from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

"""
XSS Protection Middleware for Starlette applications.

This middleware sanitizes input to prevent Cross-Site Scripting (XSS) attacks.
"""

# Regular expression patterns to match potential XSS attacks
XSS_PATTERNS = [
    r'<[^>]*script[^>]*>',  # Matches script tags
    r'javascript:',  # Matches JavaScript URIs
    r'on[a-z]+\s*=',  # Matches JavaScript event handlers
    r'<[^>]*iframe[^>]*>',  # Matches iframe tags
    r'<[^>]*object[^>]*>',  # Matches object tags
    r'<[^>]*embed[^>]*>',  # Matches embed tags
    r'<[^>]*applet[^>]*>',  # Matches applet tags
]

class XSSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """
        Dispatches the request and sanitizes the input to prevent XSS attacks.
        """
        try:
            # Check if the request method is a POST
            if request.method == 'POST':
                # Sanitize the request body
                request._data = await self._sanitize_request_body(request)

            # Continue processing the request
            response = await call_next(request)
            return response
        except Exception as e:
            # Handle any errors that occur during the sanitization process
            return HTMLResponse("<h1>Internal Server Error</h1>", status_code=500)

    async def _sanitize_request_body(self, request: Request):
        """
        Sanitization function to remove XSS patterns from the request body.
        """
        if not request.body:
            return request._data

        # Initialize an empty list to store sanitized data
        sanitized_data = []

        # Iterate over each pattern and remove matches from the request body
        for pattern in XSS_PATTERNS:
            sanitized_body = re.sub(pattern, '', request.body.decode(), flags=re.IGNORECASE)
            sanitized_data.append(sanitized_body)

        # Return the sanitized body as bytes
        return ''.join(sanitized_data).encode()

# Create a Starlette application with the XSS protection middleware
app = Starlette(middleware=[
    XSSMiddleware(),
])

# Define a simple route to demonstrate the middleware
@app.route('/', methods=['GET', 'POST'])
async def homepage(request: Request):
    """
    Homepage route to demonstrate the XSS protection middleware.
    """
    # Check if the request method is a POST
    if request.method == 'POST':
        # Get the sanitized request body
        body = await request.body()
    else:
        # Return a simple HTML page for GET requests
        return HTMLResponse("""
        <html>
            <head><title>XSS Protection Middleware</title></head>
            <body>
                <h1>Welcome to the XSS Protection Middleware Demo</h1>
                <form method="post" action="/">
                    <label for="input">Enter some text:</label><br>
                    <input type="text" id="input" name="input" required><br>
                    <input type="submit" value="Submit">
                </form>
            </body>
        </html>
        """)

    # Return the sanitized input
    return HTMLResponse(f"<h1>You entered: {body.decode()}</h1>")
