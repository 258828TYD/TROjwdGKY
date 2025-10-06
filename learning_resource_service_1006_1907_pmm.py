# 代码生成时间: 2025-10-06 19:07:48
# learning_resource_service.py

# Import necessary libraries
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from typing import Any, List, Dict
import uvicorn


# Define the LearningResource model
class LearningResource:
    def __init__(self, id: int, title: str, description: str, link: str):
        self.id = id
        self.title = title
        self.description = description
        self.link = link

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "link": self.link
        }


# Create an in-memory database for learning resources
LEARNING_RESOURCES = [
    LearningResource(1, "Python Basics", "Learn the basics of Python", "https://example.com/python-basics"),
    LearningResource(2, "Advanced Python", "Learn advanced Python techniques", "https://example.com/advanced-python"),
]

# Define the route handlers
async def get_all_resources(request):
    """Returns a list of all learning resources."""
    return JSONResponse([resource.to_dict() for resource in LEARNING_RESOURCES])

async def get_resource(request, resource_id: int):
    """Returns a single learning resource by ID."""
    resource = next((resource for resource in LEARNING_RESOURCES if resource.id == resource_id), None)
    if not resource:
        return JSONResponse({"error": "Resource not found."}, status_code=HTTP_404_NOT_FOUND)
    return JSONResponse(resource.to_dict())

# Define the routes
routes = [
    Route("/resources", get_all_resources, methods=["GET"]),
    Route("/resources/{resource_id:int}", get_resource, methods=["GET"]),
]

# Create the Starlette application
app = Starlette(routes=routes)

# Run the application using Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
