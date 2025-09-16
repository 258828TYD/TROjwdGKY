# 代码生成时间: 2025-09-17 07:40:29
import starlette.status as status
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.applications import Starlette
from starlette.requests import Request
import heapq

# 排序算法实现
def bubble_sort(arr):
    """冒泡排序算法实现"""
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr


def quick_sort(arr):
    """快速排序算法实现"""
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        less_than_pivot = [x for x in arr[1:] if x <= pivot]
        greater_than_pivot = [x for x in arr[1:] if x > pivot]
        return quick_sort(less_than_pivot) + [pivot] + quick_sort(greater_than_pivot)

# 创建Starlette应用
app = Starlette(debug=True)

# 排序接口实现
@app.route("/sort/{algorithm}", methods=["GET"])
def sort(request: Request, algorithm: str):
    """
    根据算法对数组进行排序
    :param request: 请求对象
    :param algorithm: 排序算法名称
    :return: 排序结果
    """
    query_params = request.query_params
    array = query_params.get(