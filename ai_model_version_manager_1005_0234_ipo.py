# 代码生成时间: 2025-10-05 02:34:25
# ai_model_version_manager.py
# This module provides a simple AI model version management system using Starlette framework.

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_404_NOT_FOUND
import json
import os

# Define a class to handle AI model version management
class ModelVersionManager:
    def __init__(self, storage_path):
        # Initialize the manager with a storage path
        self.storage_path = storage_path

    def list_versions(self):
        # List all AI model versions stored in the directory
        try:
            versions = os.listdir(self.storage_path)
            return versions
        except FileNotFoundError:
            return []

    def get_model_version(self, version):
        # Get a specific AI model version from storage
        try:
            with open(os.path.join(self.storage_path, version), 'r') as file:
                return file.read()
        except FileNotFoundError:
            return None

    def save_model_version(self, version, model_data):
        # Save a new AI model version to storage
        try:
            with open(os.path.join(self.storage_path, version), 'w') as file:
                file.write(model_data)
            return True
        except Exception as e:
            return False

# Create a Starlette application with routes for model version management
app = Starlette(debug=True)
model_manager = ModelVersionManager(storage_path='./models')

# Route to list all AI model versions
@app.route('/models/versions', methods=['GET'])
async def list_versions(request):
    versions = model_manager.list_versions()
    return JSONResponse(content={'versions': versions})

# Route to get a specific AI model version
@app.route('/models/versions/{version}', methods=['GET'])
async def get_model_version(request):
    version = request.path_params['version']
    model_data = model_manager.get_model_version(version)
    if model_data is not None:
        return JSONResponse(content={'version': version, 'data': model_data})
    else:
        return JSONResponse(status_code=HTTP_404_NOT_FOUND, content={'error': 'Model version not found'})

# Route to save a new AI model version
@app.route('/models/versions', methods=['POST'])
async def save_model_version(request):
    data = await request.json()
    version = data.get('version')
    model_data = data.get('data')
    if version and model_data:
        success = model_manager.save_model_version(version, model_data)
        if success:
            return JSONResponse(status_code=201, content={'message': 'Model version saved successfully'})
        else:
            return JSONResponse(status_code=500, content={'error': 'Failed to save model version'})
    else:
        return JSONResponse(status_code=400, content={'error': 'Missing version or data in request body'})
