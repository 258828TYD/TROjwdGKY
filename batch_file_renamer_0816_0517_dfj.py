# 代码生成时间: 2025-08-16 05:17:09
import os
import glob
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

# Define the application instance
app = Starlette(debug=True)

# Helper function to rename files in a directory
def rename_files(directory, prefix, suffix):
    """
    Renames files in the specified directory with a new prefix and suffix.
    
    Args:
        directory (str): The directory containing the files to rename.
        prefix (str): The new prefix for the files.
        suffix (str): The new suffix for the files.
    
    Returns:
        A list of tuples containing the old and new filenames.
    """
    renamed_files = []
    for filename in glob.glob(os.path.join(directory, "*")):
        # Extract the file extension
        file_extension = os.path.splitext(filename)[1]
        new_filename = f"{prefix}{os.path.splitext(filename)[0]}{suffix}{file_extension}"
        new_filepath = os.path.join(directory, new_filename)
        try:
            os.rename(filename, new_filepath)
            renamed_files.append((os.path.basename(filename), os.path.basename(new_filepath)))
        except Exception as e:
            return {
                "error": f"Failed to rename file {filename} to {new_filepath}: {str(e)}",
                "status": HTTP_500_INTERNAL_SERVER_ERROR
            }
    return renamed_files

# Endpoint to handle renaming files
@app.route("/rename", methods=["POST"])
async def rename_files_endpoint(request):
    """
    Handles POST requests to rename files.
    
    Args:
        request (Request): The incoming request.
    
    Returns:
        A JSON response indicating the result of the renaming operation.
    """
    try:
        data = await request.json()
        directory = data.get("directory")
        prefix = data.get("prefix")
        suffix = data.get("suffix")
        if not directory or not prefix or not suffix:
            return JSONResponse(
                content={
                    "error": "Missing required parameters: directory, prefix, and suffix."
                },
                status_code=HTTP_400_BAD_REQUEST
            )
        result = rename_files(directory, prefix, suffix)
        if isinstance(result, dict):
            return JSONResponse(content=result, status_code=result["status"])
        return JSONResponse(
            content={
                "renamed_files": result
            },
            status_code=HTTP_200_OK
        )
    except Exception as e:
        return JSONResponse(
            content={
                "error": f"An error occurred: {str(e)}",
            },
            status_code=HTTP_500_INTERNAL_SERVER_ERROR
        )

# Define the routes for the application
routes = [
    Route("/rename", rename_files_endpoint),
]

# Add the routes to the application
app.routes.extend(routes)