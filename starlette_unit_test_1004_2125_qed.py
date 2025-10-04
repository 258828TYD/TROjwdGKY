# 代码生成时间: 2025-10-04 21:25:40
import os
from starlette.testclient import TestClient
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.exceptions import HTTPException
from unittest import TestCase, main
from starlette.status import HTTP_404_NOT_FOUND


# Define the main application for testing
class App:
    def __init__(self):
        self.routes = [
            Route("/test", self.test_endpoint, methods=["GET"]),
        ]

    async def test_endpoint(self, request):
        return JSONResponse({"message": "Hello, World!"})

    def create(self):
        return Starlette(debug=True, routes=self.routes)


# Unit test class for the application
class MyAppTestCase(TestCase):
    def setUp(self):
        # Create a test client for the application
        self.app = TestClient(self.app_instance.create())

    def test_get_test_endpoint(self):
        # Test the GET request to the test endpoint
        response = self.app.get("/test")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Hello, World!"})

    def test_get_non_existent_endpoint(self):
        # Test the GET request to a non-existent endpoint
        with self.assertRaises(HTTPException) as context:
            self.app.get("/non-existent")
        self.assertEqual(context.exception.status_code, HTTP_404_NOT_FOUND)

# Main function to run the tests
if __name__ == "__main__":
    main()
