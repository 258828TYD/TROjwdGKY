# 代码生成时间: 2025-09-29 16:26:01
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import json
# TODO: 优化性能

# Define a BlockchainNode class to manage blockchain nodes
class BlockchainNode:
    def __init__(self, node_id, data):
        self.node_id = node_id
        self.data = data

    def to_dict(self):
        return {"node_id": self.node_id, "data": self.data}

# Define a BlockchainNodeManager class to manage the nodes
class BlockchainNodeManager:
    def __init__(self):
# TODO: 优化性能
        self.nodes = []

    def add_node(self, node_id, data):
        if any(node.node_id == node_id for node in self.nodes):
            return False, "Node ID already exists."
        new_node = BlockchainNode(node_id, data)
        self.nodes.append(new_node)
        return True, new_node.to_dict()

    def get_node(self, node_id):
        for node in self.nodes:
# NOTE: 重要实现细节
            if node.node_id == node_id:
                return node.to_dict()
        return None
# 增强安全性

    def remove_node(self, node_id):
        for node in self.nodes:
# 优化算法效率
            if node.node_id == node_id:
# 添加错误处理
                self.nodes.remove(node)
                return True, "Node removed."
        return False, "Node not found."

# Define the Starlette application
app = Starlette(debug=True)

# Instantiate the BlockchainNodeManager
node_manager = BlockchainNodeManager()

# Define routes for the application
@app.route("/add_node", methods=["POST"])
async def add_node(request):
# NOTE: 重要实现细节
    data = await request.json()
    node_id = data.get("node_id")
    node_data = data.get("data\)
    if not node_id or not node_data:
        return JSONResponse(
# FIXME: 处理边界情况
            content="{"error": "Missing node ID or data."}",
            status_code=HTTP_400_BAD_REQUEST
        )
    success, result = node_manager.add_node(node_id, node_data)
    if success:
        return JSONResponse(content=json.dumps(result), status_code=HTTP_200_OK)
    return JSONResponse(content=json.dumps({"error": result}), status_code=HTTP_400_BAD_REQUEST)
# 增强安全性

@app.route("/get_node/{node_id}", methods=["GET"])
# FIXME: 处理边界情况
async def get_node(request):
    node_id = request.path_params["node_id"]
    node = node_manager.get_node(node_id)
    if node:
        return JSONResponse(content=json.dumps(node), status_code=HTTP_200_OK)
    return JSONResponse(content="{"error": "Node not found."}", status_code=HTTP_400_BAD_REQUEST)

@app.route("/remove_node/{node_id}", methods=["DELETE"])
async def remove_node(request):
    node_id = request.path_params["node_id"]
    success, message = node_manager.remove_node(node_id)
# NOTE: 重要实现细节
    if success:
# 改进用户体验
        return JSONResponse(content=json.dumps({"message": message}), status_code=HTTP_200_OK)
    return JSONResponse(content=json.dumps({"error": message}), status_code=HTTP_400_BAD_REQUEST)

# Run the application
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)