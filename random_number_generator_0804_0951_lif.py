# 代码生成时间: 2025-08-04 09:51:54
import random
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

"""
Random Number Generator Service
A simple web service that generates random numbers using the Starlette framework.
"""

class RandomNumberGeneratorService:
    """ Handles random number generation logic. """

    def __init__(self):
        pass

    def generate_random_number(self, lower_bound, upper_bound):
        """
        Generates a random number within a specified range.

        Args:
            lower_bound (int): The lower bound of the range.
            upper_bound (int): The upper bound of the range.

        Returns:
            int: A random number within the specified range.
        """
        if lower_bound > upper_bound:
            raise ValueError("Lower bound cannot be greater than upper bound.")

        return random.randint(lower_bound, upper_bound)

async def random_number_endpoint(request):
    """
    Asynchronous endpoint for generating random numbers.

    Args:
        request: The HTTP request object.

    Returns:
        JSONResponse: A response containing the generated random number.
    """
    try:
        query_params = request.query_params
        lower_bound = int(query_params.get("lower", 1))
        upper_bound = int(query_params.get("upper", 100))
        random_number = RandomNumberGeneratorService().generate_random_number(lower_bound, upper_bound)
        return JSONResponse(content={"random_number": random_number})
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Define the routes for the Starlette application
routes = [
    Route("/random", endpoint=random_number_endpoint),
]

# Create and run the Starlette application
app = Starlette(debug=True, routes=routes)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)