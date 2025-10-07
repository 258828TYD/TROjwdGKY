# 代码生成时间: 2025-10-08 00:00:24
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
import json
import logging


# Initialize logger
logger = logging.getLogger(__name__)


class BlockchainNodeManager:
    def __init__(self):
        # Initialize an empty list to store nodes
        self.nodes = []

    def add_node(self, node):
        """Add a new node to the blockchain network."""
        try:
            if node not in self.nodes:
                self.nodes.append(node)
                return True
            else:
                return False
        except Exception as e:
            logger.error(f"Error adding node: {e}")
            return False

    def remove_node(self, node):
        """Remove a node from the blockchain network."""
        try:
            if node in self.nodes:
                self.nodes.remove(node)
                return True
            else:
                return False
        except Exception as e:
            logger.error(f"Error removing node: {e}")
            return False

    def get_nodes(self):
        """Return a list of all nodes in the blockchain network."""
        return self.nodes


# API endpoint for adding a node
async def add_node_endpoint(request):
    body = await request.json()
    node_manager = request.state.node_manager
    success = node_manager.add_node(body['node'])
    if success:
        return JSONResponse({'message': 'Node added successfully'}, status_code=200)
    else:
        return JSONResponse({'message': 'Node already exists'}, status_code=400)

# API endpoint for removing a node
async def remove_node_endpoint(request):
    body = await request.json()
    node_manager = request.state.node_manager
    success = node_manager.remove_node(body['node'])
    if success:
        return JSONResponse({'message': 'Node removed successfully'}, status_code=200)
    else:
        return JSONResponse({'message': 'Node not found'}, status_code=404)

# API endpoint for getting all nodes
async def get_nodes_endpoint(request):
    node_manager = request.state.node_manager
    nodes = node_manager.get_nodes()
    return JSONResponse({'nodes': nodes}, status_code=200)

# Exception handler for 404 errors
async def not_found(request, exc):
    return JSONResponse({'detail': 'Not found'}, status_code=HTTP_404_NOT_FOUND)

# Exception handler for 500 errors
async def server_error(request, exc):
    return JSONResponse({'detail': 'Server error'}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

# Initialize the BlockchainNodeManager instance
node_manager = BlockchainNodeManager()

# Create a Starlette application with routes
app = Starlette(
    routes=[
        Route('/add_node', add_node_endpoint),
        Route('/remove_node', remove_node_endpoint),
        Route('/get_nodes', get_nodes_endpoint)
    ],
    on_startup=[node_manager.add_node],
    exception_handlers={404: not_found, 500: server_error},
    debug=True
)

# Set the node manager as a state on the application
app.state.node_manager = node_manager

# Run the application with Uvicorn
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)