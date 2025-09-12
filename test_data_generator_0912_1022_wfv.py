# 代码生成时间: 2025-09-12 10:22:36
# test_data_generator.py

import starlette.status as status
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.applications import Starlette

# 生成测试数据的函数
def generate_test_data(data_size: int) -> list:
    """Generates a list of test data entries.

    Args:
        data_size (int): The number of test data entries to generate.

    Returns:
        list: A list of test data entries.
    """
    test_data = []
    for i in range(data_size):
        test_data.append({"id": i, "name": f"TestName{i}", "value": 100 + i})
    return test_data

# API端点，用于获取测试数据
async def get_test_data(request):
    """Handles GET requests to retrieve test data.

    Args:
        request: The incoming HTTP request.

    Returns:
        JSONResponse: A JSON response containing the test data.
    """
    try:
        query_params = request.query_params
        data_size = int(query_params.get("size", 10))  # Default to 10 if size is not provided
        test_data = generate_test_data(data_size)
        return JSONResponse(status_code=status.HTTP_200_OK, content=test_data)
    except ValueError:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Invalid size parameter. It must be an integer."}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)}
        )

# 创建Starlette应用
app = Starlette(
    debug=True,
    routes=[
        Route("/test-data", endpoint=get_test_data),
    ],
)

# 运行应用时的入口点
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)