# 代码生成时间: 2025-09-13 18:37:49
import starlette.applications
import starlette.responses
import starlette.routing
import starlette.exceptions
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.requests import Request
import aiohttp
import aiofiles
import json

# Middleware to handle CORS
class SimpleMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, allow_origins: list = ['*'], allow_methods: list = ['*'], allow_headers: list = ['*'], allow_credentials: bool = False):
        super().__init__(app)
        self.allow_origins = allow_origins
        self.allow_methods = allow_methods
        self.allow_headers = allow_headers
        self.allow_credentials = allow_credentials

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Set CORS headers
        response.headers['Access-Control-Allow-Origin'] = ', '.join(self.allow_origins)
        response.headers['Access-Control-Allow-Methods'] = ', '.join(self.allow_methods)
        response.headers['Access-Control-Allow-Headers'] = ', '.join(self.allow_headers)
        response.headers['Access-Control-Allow-Credentials'] = str(self.allow_credentials).lower()

        return response

# Create a Starlette application
app = starlette.applications Starlette(app=starlette.types.ASGIApp)

# Define routes
routes = [
    starlette.routing.Route('/', endpoint=starlette.responses.JSONResponse({'message': 'Hello, World!'}), methods=['GET']),
    starlette.routing.Route('/api/data', endpoint=starlette.responses.JSONResponse({'data': 'API data response'})),
]

# Add routes to the application
app.add_routes(routes)

# Add middleware to handle CORS
app.add_middleware(SimpleMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'], allow_credentials=False)

# Add static files
app.add_middleware(StaticFiles, directory='static')

# Add templates
templates = Jinja2Templates(directory='templates')

# Define an error handler
async def http_exception_handler(request: Request, exc: starlette.exceptions.HTTPException):
    return starlette.responses.JSONResponse({'detail': str(exc)}, status_code=exc.status_code)

# Add error handler to the application
app.add_exception_handler(starlette.exceptions.HTTPException, http_exception_handler)

# Define an endpoint for the responsive layout
@app.route('/layout', methods=['GET'])
async def responsive_layout(request: Request):
    # Render the responsive layout template
    return templates.TemplateResponse('layout.html', {'request': request})

# Define an endpoint for the API data
@app.route('/api/data', methods=['GET'])
async def api_data(request: Request):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://api.example.com/data') as response:
                data = await response.json()
                return starlette.responses.JSONResponse(data)
    except Exception as e:
        raise starlette.exceptions.HTTPException(status_code=500, detail=str(e))

# Define an endpoint for uploading files
@app.route('/upload', methods=['POST'])
async def upload_file(request: Request):
    try:
        form = await request.form()
        file = form['file'].file
        filename = form['file'].filename
        async with aiofiles.open(f'./uploads/{filename}', mode='wb') as f:
            await f.write(await file.read())
        return starlette.responses.JSONResponse({'message': 'File uploaded successfully'})
    except Exception as e:
        raise starlette.exceptions.HTTPException(status_code=500, detail=str(e))

# Run the application
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)