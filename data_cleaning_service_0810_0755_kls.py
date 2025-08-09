# 代码生成时间: 2025-08-10 07:55:24
import json
from typing import Any, Dict
from starlette.responses import JSONResponse
from starlette.requests import Request
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

# Constants for the API endpoints
API_ENDPOINT_CLEAN = "/clean"

# Data cleaning and preprocessing functions
def clean_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Cleans the input data by removing empty strings, None values and
    converts all keys to lowercase.
    
    :param data: Dictionary containing the data to be cleaned
    :return: Dictionary with cleaned data
    """
    if not isinstance(data, dict):
        raise ValueError("Input data must be a dictionary.")
    
    cleaned_data = {key.lower(): value for key, value in data.items() if value not in (None, '')}
    return cleaned_data

# Starlette route handlers
async def clean_data_handler(request: Request) -> JSONResponse:
    """
    Handles requests to the clean data endpoint.
    
    :param request: Starlette Request object
    :return: Starlette JSONResponse with cleaned data or an error message
    """
    try:
        # Parse the JSON body of the request
        data = await request.json()
        # Clean the data
        cleaned_data = clean_data(data)
        # Return the cleaned data in the response
        return JSONResponse(content={"cleaned_data": cleaned_data}, status_code=HTTP_200_OK)
    except json.JSONDecodeError:
        return JSONResponse(content={"error": "Invalid JSON format"}, status_code=HTTP_400_BAD_REQUEST)
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=HTTP_400_BAD_REQUEST)

# Define the route
def register_routes(app):
    """
    Registers the data cleaning endpoint to the Starlette application.
    
    :param app: Starlette application instance
    """
    app.add_route(API_ENDPOINT_CLEAN, clean_data_handler)

# Example of how to use the service
if __name__ == "__main__":
    from starlette.applications import Starlette
    from starlette.middleware import Middleware
    from starlette.middleware.cors import CORSMiddleware
    
    # Create a new Starlette application instance
    app = Starlette(middleware=[
        Middleware(CORSMiddleware, allow_origins="*", allow_methods="*", allow_headers="*")
    ])
    
    # Register the routes
    register_routes(app)
    
    # Run the app
    app.run(debug=True)