# 代码生成时间: 2025-08-17 09:24:02
import starlette.responses
from starlette.routing import Route
from starlette.templating import Jinja2Templates
from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.requests import Request
from starlette.status import HTTP_400_BAD_REQUEST
import html


# Initialize templates
templates = Jinja2Templates(directory="./templates")


async def xss_protection_middleware(request: Request, next: ASGIApp) -> starlette.responses.Response:
    # Check for potential XSS attacks in the body of the request
    if request.method == "POST":
        body = await request.body()
        unsafe_chars = b'>"'  # Characters that can be used in XSS attacks
        if any(char in body for char in unsafe_chars):
            return starlette.responses.Response(
                "Potential XSS attack detected.",
                status_code=HTTP_400_BAD_REQUEST
            )
    return await next(request)


async def home(request: Request):
    # Escape user input to prevent XSS attacks
    user_input = html.escape(request.query_params.get("input", ""))
    return templates.render("home.html", request=request, user_input=user_input)


# Define routes
routes = [
    Route("/", endpoint=home, methods=["GET", "POST"]),
    # Middleware to protect against XSS attacks
    Route("/", endpoint=xss_protection_middleware, methods=["POST"])
]


# Define the application
app = starlette.applications.Application(routes=routes)


# Document the middleware
"""
Middleware to protect against XSS attacks in Starlette application.

This middleware will check for the presence of potentially dangerous
characters in the request body and return a 400 Bad Request error
if any are found.
"""

# Document the home route
"""
Home route that escapes user input to prevent XSS attacks.

This route takes a query parameter 'input' and escapes it to prevent
XSS attacks when rendered in the HTML template.
"""

# Document the templates
"""
Templates directory containing HTML files for rendering.

The 'home.html' template will render the escaped user input to display on the page.
"""
