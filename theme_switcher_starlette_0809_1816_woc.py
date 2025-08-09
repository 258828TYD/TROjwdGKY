# 代码生成时间: 2025-08-09 18:16:31
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
# FIXME: 处理边界情况
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

# Theme switcher middleware to manage theme
class ThemeMiddleware(SessionMiddleware):
    def __init__(self, secret_key):
# 扩展功能模块
        super().__init__(secret_key)
# NOTE: 重要实现细节

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
# 优化算法效率
        theme = request.session.get("theme")
        if theme is not None:
            response.headers["X-Theme"] = theme
        return response

# Route to switch themes
async def switch_theme(request: Request):
    theme = request.query_params.get("theme", "light")
    if theme not in ["light", "dark"]:
# 增强安全性
        return JSONResponse(
            content={"error": "Invalid theme provided"}, status_code=HTTP_400_BAD_REQUEST
        )
    request.session["theme"] = theme
    return JSONResponse(content={"theme": theme}, status_code=HTTP_200_OK)

# Main application
app = Starlette(
    middleware=[
        Middleware(ThemeMiddleware, secret_key="a_secret_key")
# 扩展功能模块
    ],
    routes=[
        Route("/switch-theme", endpoint=switch_theme),
    ]
)

# Documentation for the switch_theme function
"""
This function handles theme switching requests.
It expects a GET request to /switch-theme with a query parameter 'theme'.
# 改进用户体验
The theme can be either 'light' or 'dark'. If the theme is not provided,
# FIXME: 处理边界情况
it defaults to 'light'. If an invalid theme is provided, it returns a 400 error.

:param request: The Starlette request object containing query parameters.
:return: A JSON response with the selected theme or an error message.
"""
# 优化算法效率

# Application documentation
"""
This Starlette application provides a simple theme switcher service.
It uses session middleware to store the theme preference and returns the selected theme.
The middleware also adds an 'X-Theme' header to the response to indicate the current theme.
# TODO: 优化性能

Usage:
- Send a GET request to /switch-theme with the desired theme as a query parameter.
- The application will store the theme preference and return the selected theme in the response.
- The 'X-Theme' header will be set in the response to indicate the current theme.

Example:
- GET /switch-theme?theme=dark - Switches the theme to dark and returns the response with theme set to dark.
"""