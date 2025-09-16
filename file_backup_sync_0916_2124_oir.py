# 代码生成时间: 2025-09-16 21:24:27
import os
import shutil
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.exceptions import HTTPException as StarletteHTTPException


class FileBackupSyncException(Exception):
    """Custom exception for file backup and sync operations."""
    pass


class FileBackupSync:
    def __init__(self, source, destination):
        """Initialize the FileBackupSync instance with source and destination paths."""
        self.source = source
        self.destination = destination

    def backup(self):
        """Backup files from the source directory to the destination directory."""
        try:
            if not os.path.exists(self.destination):
                os.makedirs(self.destination)
            for filename in os.listdir(self.source):
                src_file = os.path.join(self.source, filename)
                dst_file = os.path.join(self.destination, filename)
                if os.path.isfile(src_file):
                    shutil.copy2(src_file, dst_file)
            return {"status": "success", "message": "Backup completed successfully."}
        except Exception as e:
            raise FileBackupSyncException(f"Backup failed: {e}")

    def sync(self):
        """Sync files between the source and destination directories."""
        try:
            for filename in os.listdir(self.source):
                src_file = os.path.join(self.source, filename)
                dst_file = os.path.join(self.destination, filename)
                if os.path.isfile(src_file):
                    if not os.path.exists(dst_file) or os.stat(src_file).st_mtime > os.stat(dst_file).st_mtime:
                        shutil.copy2(src_file, dst_file)
            return {"status": "success", "message": "Sync completed successfully."}
        except Exception as e:
            raise FileBackupSyncException(f"Sync failed: {e}")


async def backup_files(request):
    """Endpoint to trigger file backup operation."""
    backup_sync = FileBackupSync(request.query_params['source'], request.query_params['destination'])
    try:
        result = backup_sync.backup()
        return JSONResponse(result)
    except FileBackupSyncException as e:
        return JSONResponse({'status': 'error', 'message': str(e)}, status_code=500)

async def sync_files(request):
    """Endpoint to trigger file sync operation."""
    backup_sync = FileBackupSync(request.query_params['source'], request.query_params['destination'])
    try:
        result = backup_sync.sync()
        return JSONResponse(result)
    except FileBackupSyncException as e:
        return JSONResponse({'status': 'error', 'message': str(e)}, status_code=500)


routes = [
    Route("/backup", endpoint=backup_files, methods=["GET"]),
    Route("/sync", endpoint=sync_files, methods=["GET"]),
]


app = Starlette(debug=True, routes=routes)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)