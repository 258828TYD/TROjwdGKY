# 代码生成时间: 2025-09-04 19:49:31
# document_converter.py
# A simple document converter using Starlette framework.

import os
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from starlette.requests import Request

# The supported document formats
SUPPORTED_FORMATS = {'txt', 'pdf', 'docx', 'xlsx'}

# The root directory for the documents
DOCUMENT_ROOT = 'documents'

# Ensure the document root directory exists
os.makedirs(DOCUMENT_ROOT, exist_ok=True)

def convert_document(file_path, target_format):
    # Placeholder function for document conversion logic
    # This should be replaced with actual conversion logic
    return f"{os.path.basename(file_path)}.{target_format}"

async def convert(request: Request):
    # Extract the document name and target format from the query parameters
    document_name = request.query_params.get('document')
    target_format = request.query_params.get('format')
    
    # Check if the document name and target format are provided
    if not document_name or not target_format:
        return JSONResponse(
            content={'error': 'Missing document name or target format'},
            status_code=HTTP_400_BAD_REQUEST
        )
    
    # Check if the target format is supported
    if target_format not in SUPPORTED_FORMATS:
        return JSONResponse(
            content={'error': 'Unsupported document format'},
            status_code=HTTP_400_BAD_REQUEST
        )
    
    # Construct the full path to the document
    document_path = os.path.join(DOCUMENT_ROOT, document_name)
    
    # Check if the document exists
    if not os.path.exists(document_path):
        return JSONResponse(
            content={'error': 'Document not found'},
            status_code=HTTP_400_BAD_REQUEST
        )
    
    # Perform the document conversion
    try:
        converted_document_path = convert_document(document_path, target_format)
        return JSONResponse(
            content={'message': 'Document converted successfully', 'path': converted_document_path},
            status_code=HTTP_200_OK
        )
    except Exception as e:
        return JSONResponse(
            content={'error': str(e)},
            status_code=HTTP_500_INTERNAL_SERVER_ERROR
        )

# Define the routes for the application
routes = [
    Route('/document/convert', convert, methods=['GET']),
]

# Create the Starlette application
app = Starlette(debug=True, routes=routes)

# Run the application with 'uvicorn document_converter:app --reload'
