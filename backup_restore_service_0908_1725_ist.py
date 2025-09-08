# 代码生成时间: 2025-09-08 17:25:58
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
import json
import shutil
import os
import tempfile

"""
A Starlette application for data backup and restore.
This application provides endpoints for backing up and restoring data.
"""


# Constants
BACKUP_DIR = 'backups'
RESTORE_DIR = 'restore'

class BackupRestoreService:
    """
    A service class for handling data backup and restore operations.
    """
    def __init__(self):
        if not os.path.exists(BACKUP_DIR):
            os.makedirs(BACKUP_DIR)
        if not os.path.exists(RESTORE_DIR):
            os.makedirs(RESTORE_DIR)

    def backup_data(self, data_path):
        """
        Creates a backup of the data at the specified path.
        Args:
            data_path (str): The path of the data to backup.
        Returns:
            str: The path of the backup file.
        """
        try:
            # Create a temporary file for backup
            with tempfile.NamedTemporaryFile(suffix='.backup', delete=False) as tmp_file:
                backup_path = tmp_file.name
                # Copy the data to the backup file
                shutil.copytree(data_path, backup_path)
                return backup_path
        except Exception as e:
            raise Exception(f"Failed to backup data: {str(e)}")

    def restore_data(self, backup_path, target_path):
        """
        Restores data from the specified backup path to the target path.
        Args:
            backup_path (str): The path of the backup file.
            target_path (str): The path where the data will be restored.
        Returns:
            bool: True if restoration is successful, False otherwise.
        """
        try:
            # Remove the target directory if it already exists
            if os.path.exists(target_path):
                shutil.rmtree(target_path)
            # Copy the backup data to the target path
            shutil.copytree(backup_path, target_path)
            return True
        except Exception as e:
            raise Exception(f"Failed to restore data: {str(e)}")

# Routes
routes = [
    Route('/api/backup', endpoint=BackupHandler, methods=['POST']),
    Route('/api/restore', endpoint=RestoreHandler, methods=['POST']),
]

# Handlers
class BackupHandler:
    def __init__(self, service):
        self.service = service

    async def __call__(self, request):
        data = await request.json()
        backup_path = self.service.backup_data(data['data_path'])
        return JSONResponse({'message': 'Backup successful', 'backup_path': backup_path})

class RestoreHandler:
    def __init__(self, service):
        self.service = service

    async def __call__(self, request):
        data = await request.json()
        try:
            restore_success = self.service.restore_data(data['backup_path'], data['target_path'])
            if restore_success:
                return JSONResponse({'message': 'Restore successful'})
            else:
                return JSONResponse({'message': 'Restore failed'}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return JSONResponse({'message': str(e)}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

# Create the Starlette application
app = Starlette(routes=routes)

# Service
service = BackupRestoreService()

# Add service instances to the app state
app.add_middleware(lambda app: app.state['backup_restore_service'] = service)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)