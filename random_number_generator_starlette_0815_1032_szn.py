# 代码生成时间: 2025-08-15 10:32:56
# random_number_generator_starlette.py
# This program creates a Starlette application to generate random numbers.

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import random
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the routes
routes = [
    Route("/random/{min}-{max}", endpoint=generate_random_number),
]

# Define the Starlette application
app = Starlette(debug=True, routes=routes)

# Function to generate a random number
async def generate_random_number(request):
    # Extract the minimum and maximum values from the URL path parameters
    min_max = request.path_params.get("").split("")
    min_val = int(min_max[0])
    max_val = int(min_max[1])

    # Check if the minimum and maximum values are valid
    if min_val > max_val:
        raise ValueError("Minimum value must be less than or equal to maximum value.")

    # Generate a random number within the specified range
    random_num = random.randint(min_val, max_val)

    # Return the generated random number as a JSON response
    return JSONResponse(content={"random_number": random_num})

# Run the application if this script is executed directly
if __name__ == "__main__":
    logger.info("Starting the random number generator...")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)