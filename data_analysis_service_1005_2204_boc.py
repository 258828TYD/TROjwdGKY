# 代码生成时间: 2025-10-05 22:04:23
import asyncio
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.exceptions import HTTPException as StarletteHTTPException

# 数据统计器类
class DataAnalyzer:
    def __init__(self):
        self.data = []

    def add_data_point(self, data_point):
        """添加数据点到集合中。"""
        self.data.append(data_point)

    def calculate_mean(self):
        """计算数据集的平均值。"""
        if not self.data:
            raise ValueError("数据集为空，无法计算平均值。")
        return sum(self.data) / len(self.data)

    def calculate_median(self):
        """计算数据集的中位数。"""
        if not self.data:
            raise ValueError("数据集为空，无法计算中位数。")
        sorted_data = sorted(self.data)
        n = len(sorted_data)
        mid = n // 2
        if n % 2 == 0:
            return (sorted_data[mid - 1] + sorted_data[mid]) / 2
        else:
            return sorted_data[mid]

# 创建数据分析师的实例
analyzer = DataAnalyzer()

# Starlette应用
app = Starlette(debug=True)

# 添加路由
app.add_route("/add", endpoint=AddDataEndpoint(analyzer), methods=["POST"])
app.add_route("/mean", endpoint=MeanEndpoint(analyzer), methods=["GET"])
app.add_route("/median", endpoint=MedianEndpoint(analyzer), methods=["GET"])

# 添加数据点的Endpoint
class AddDataEndpoint:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    async def __call__(self, request):
        try:
            data = await request.json()
            if 'data_point' not in data:
                raise ValueError("请求数据中缺少 'data_point'。")
            self.analyzer.add_data_point(data['data_point'])
            return JSONResponse({'message': '数据点添加成功。'})
        except ValueError as ve:
            raise StarletteHTTPException(status_code=400, detail=str(ve))
        except Exception as e:
            raise StarletteHTTPException(status_code=500, detail=str(e))

# 计算平均值的Endpoint
class MeanEndpoint:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    async def __call__(self, request):
        try:
            return JSONResponse({'mean': self.analyzer.calculate_mean()})
        except ValueError as ve:
            raise StarletteHTTPException(status_code=400, detail=str(ve))
        except Exception as e:
            raise StarletteHTTPException(status_code=500, detail=str(e))

# 计算中位数的Endpoint
class MedianEndpoint:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    async def __call__(self, request):
        try:
            return JSONResponse({'median': self.analyzer.calculate_median()})
        except ValueError as ve:
            raise StarletteHTTPException(status_code=400, detail=str(ve))
        except Exception as e:
            raise StarletteHTTPException(status_code=500, detail=str(e))
