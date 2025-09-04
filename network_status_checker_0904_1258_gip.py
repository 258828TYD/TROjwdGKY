# 代码生成时间: 2025-09-04 12:58:56
import asyncio
import aiohttp
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

"""
Network Status Checker API using Starlette and Aiohttp.
This API provides a simple endpoint to check network connectivity to a specified URL.
"""

async def check_network_status(url: str):
    """
    Asynchronously checks the network connectivity to a given URL.
    :param url: The URL to check network connectivity against.
    :return: A JSON response indicating the status of the network connection.
# TODO: 优化性能
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return {"status": "connected"}
                else:
                    return {"status": "disconnected", "reason": response.status}
    except aiohttp.ClientError as e:
        return {"status": "disconnected", "reason": str(e)}

app = Starlette(debug=True)

@app.route("/check", methods=["GET"])
async def check(request):
    """
    Handle the network status check request.
    :param request: The Starlette request object.
    :return: A JSON response with the network status.
# 增强安全性
    """
    url = request.query_params.get("url")
    if not url:
        return JSONResponse(
            {
                "error": "Missing 'url' query parameter."
            },
# 改进用户体验
            status_code=400,
# 改进用户体验
        )
    result = await check_network_status(url)
    return JSONResponse(result)

if __name__ == "__main__":
# 改进用户体验
    """
    Run the application if this script is executed directly.
# TODO: 优化性能
    """
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)