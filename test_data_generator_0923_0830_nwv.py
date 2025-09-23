# 代码生成时间: 2025-09-23 08:30:53
# test_data_generator.py
# A simple test data generator using Starlette framework.

import random
import string
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

# Define a function to generate random test data
def generate_test_data():
    # Generate a random string of letters and digits
    random_string = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
    # Create a dictionary with random test data
    test_data = {
        'id': random.randint(1, 100),
        'name': f"TestUser{random_string}",
        'email': f"{random_string}@example.com",
        'is_active': random.choice([True, False])
    }
    return test_data

# Define a route for generating test data
async def get_test_data(request):
    try:
        # Generate test data
        test_data = generate_test_data()
        # Return the test data as a JSON response
        return JSONResponse(test_data)
    except Exception as e:
        # Handle any exceptions that occur during data generation
        error_message = {'error': str(e)}
        return JSONResponse(error_message, status_code=500)

# Define the application routes
routes = [
    Route('/', get_test_data),
]

# Create a Starlette application
app = Starlette(debug=True, routes=routes)

# If this script is run directly, start the development server
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)