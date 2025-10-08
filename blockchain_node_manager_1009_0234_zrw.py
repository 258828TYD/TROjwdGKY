# 代码生成时间: 2025-10-09 02:34:28
# blockchain_node_manager.py
# This module provides a basic blockchain node manager using Starlette framework.
# NOTE: 重要实现细节

from starlette.applications import Starlette
from starlette.responses import JSONResponse, Response
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
import json

# Define a simple blockchain node structure
class BlockchainNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.peers = []
    
    def add_peer(self, peer_id):
        if peer_id not in self.peers:
# TODO: 优化性能
            self.peers.append(peer_id)
            return True
# 增强安全性
        return False
    
    def remove_peer(self, peer_id):
        if peer_id in self.peers:
            self.peers.remove(peer_id)
            return True
        return False

    def get_peers(self):
        return self.peers
# TODO: 优化性能

# Define the BlockchainNodeManager class
class BlockchainNodeManager:
    def __init__(self):
        self.nodes = {}
    
    def create_node(self, node_id):
        if node_id in self.nodes:
            return False
        self.nodes[node_id] = BlockchainNode(node_id)
        return True
    
    def delete_node(self, node_id):
        if node_id not in self.nodes:
            return False
# FIXME: 处理边界情况
        del self.nodes[node_id]
        return True
    
    def add_peer_to_node(self, node_id, peer_id):
        if node_id not in self.nodes:
            return False
        return self.nodes[node_id].add_peer(peer_id)
    
    def remove_peer_from_node(self, node_id, peer_id):
        if node_id not in self.nodes:
            return False
        return self.nodes[node_id].remove_peer(peer_id)
    
    def get_peers_of_node(self, node_id):
        if node_id not in self.nodes:
            return []
        return self.nodes[node_id].get_peers()

# Define the Starlette application
app = Starlette(
    routes=[
        # Route to create a new blockchain node
        Route("/nodes", endpoint=lambda request: JSONResponse(
            status_code=HTTP_200_OK, content=json.dumps(
                BlockchainNodeManager().create_node(request.query_params.get("node_id", None))))),
        # Route to delete a blockchain node
        Route("/nodes/{node_id}", endpoint=lambda request: JSONResponse(
            status_code=HTTP_200_OK, content=json.dumps(
                BlockchainNodeManager().delete_node(request.path_params["node_id\])))),
        # Route to add a peer to a node
        Route("/nodes/{node_id}/peers", endpoint=lambda request: JSONResponse(
            status_code=HTTP_200_OK, content=json.dumps(
                BlockchainNodeManager().add_peer_to_node(request.path_params["node_id"], request.query_params.get("peer_id", None))))),
# TODO: 优化性能
        # Route to remove a peer from a node
# 添加错误处理
        Route("/nodes/{node_id}/peers/{peer_id}", endpoint=lambda request: JSONResponse(
            status_code=HTTP_200_OK, content=json.dumps(
                BlockchainNodeManager().remove_peer_from_node(request.path_params["node_id"], request.path_params["peer_id\])))),
        # Route to get peers of a node
# FIXME: 处理边界情况
        Route("/nodes/{node_id}/peers", endpoint=lambda request: JSONResponse(
# 增强安全性
            status_code=HTTP_200_OK, content=json.dumps(
                BlockchainNodeManager().get_peers_of_node(request.path_params["node_id\])))),
    ]
)

# Error handler for 404 requests
async def not_found(request):
    return Response("Not Found", status_code=HTTP_404_NOT_FOUND)

# Add error handler to the application
app.add_exception_handler(404, not_found)

# Error handler for 400 requests
async def bad_request(request, exc):
    return Response(f"Bad Request: {str(exc)}", status_code=HTTP_400_BAD_REQUEST)
# NOTE: 重要实现细节

# Add error handler to the application
app.add_exception_handler(TypeError, bad_request)

# Run the application with uvicorn
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host='0.0.0.0', port=8000)