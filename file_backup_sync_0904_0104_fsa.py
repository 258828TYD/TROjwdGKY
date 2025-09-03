# 代码生成时间: 2025-09-04 01:04:31
# file_backup_sync.py - A simple file backup and sync tool using Python and Starlette.

import os
import shutil
import asyncio
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR

# Define a basic error handler for exceptions
async def error_handler(request, exc):
    return JSONResponse(
        {
            "detail": str(exc)
        },
        status_code=HTTP_500_INTERNAL_SERVER_ERROR
    )

# The main application class
class FileBackupSyncApp(Starlette):
    def __init__(self):
        super().__init__(
            routes=[
                Route("/sync", endpoint=SyncEndpoint, methods=["POST"]),
            ],
            exception_handlers={
                500: error_handler,
            },
        )

# SyncEndpoint class to handle file synchronization
class SyncEndpoint:
    async def __init__(self):
        pass

    async def __call__(self, request):
        # Extract the source and destination paths from the request
        data = await request.json()
        source_path = data.get("source")
        destination_path = data.get("destination\)

        try:
            # Check if the source path exists
            if not os.path.exists(source_path):
                return JSONResponse(
                    {
                        "error": f"Source path '{source_path}' does not exist."
                    },
                    status_code=HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Perform the synchronization operation
            await sync_folders(source_path, destination_path)

            # Return a success response
            return JSONResponse(
                {
                    "message": "Files synchronized successfully."
                },
                status_code=HTTP_200_OK
            )
        except Exception as e:
            return JSONResponse(
                {
                    "error": str(e)
                },
                status_code=HTTP_500_INTERNAL_SERVER_ERROR
            )

# Function to synchronize two folders
async def sync_folders(source, destination):
    # Ensure the destination directory exists
    os.makedirs(destination, exist_ok=True)

    for item in os.listdir(source):
        source_item_path = os.path.join(source, item)
        destination_item_path = os.path.join(destination, item)

        # Check if it's a directory or a file
        if os.path.isdir(source_item_path):
            # Recursively sync directories
            await sync_folders(source_item_path, destination_item_path)
        elif os.path.isfile(source_item_path):
            # Copy files to the destination
            shutil.copy2(source_item_path, destination_item_path)

# Main function to run the application
async def main():
    await FileBackupSyncApp().run(host="0.0.0.0", port=8000)

if __name__ == "__main__":
    asyncio.run(main())
