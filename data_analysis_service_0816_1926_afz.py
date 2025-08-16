# 代码生成时间: 2025-08-16 19:26:20
import asyncio
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import pandas as pd
import numpy as np
from typing import Any, Dict


# 数据统计分析器服务
class DataAnalysisService:
    def __init__(self, data: pd.DataFrame):
        """
        初始化数据分析服务
        :param data: 待分析的数据
        """
        self.data = data

    def mean(self, column_name: str) -> float:
        """
        计算指定列的平均值
        :param column_name: 列名称
        :return: 平均值
        """
        try:
            return self.data[column_name].mean()
        except KeyError:
            raise ValueError(f"Column '{column_name}' not found in data")

    def std_dev(self, column_name: str) -> float:
        """
        计算指定列的标准差
        :param column_name: 列名称
        :return: 标准差
        """
        try:
            return self.data[column_name].std()
        except KeyError:
            raise ValueError(f"Column '{column_name}' not found in data")


# 数据分析器Starlette应用
class DataAnalysisApp(Starlette):
    def __init__(self, data: pd.DataFrame):
        super().__init__(
            routes=[
                Route("/mean/{column_name}", self.mean_endpoint),
                Route("/std_dev/{column_name}", self.std_dev_endpoint),
            ],
        )
        self.data_analysis_service = DataAnalysisService(data)

    async def mean_endpoint(self, request):
        """
        处理获取平均值的请求
        """
        column_name = request.path_params['column_name']
        try:
            mean_value = self.data_analysis_service.mean(column_name)
            return JSONResponse(content={"mean": mean_value})
        except ValueError as e:
            return JSONResponse(content={"error": str(e)}, status_code=400)

    async def std_dev_endpoint(self, request):
        """
        处理获取标准差的请求
        """
        column_name = request.path_params['column_name']
        try:
            std_dev_value = self.data_analysis_service.std_dev(column_name)
            return JSONResponse(content={"std_dev": std_dev_value})
        except ValueError as e:
            return JSONResponse(content={"error": str(e)}, status_code=400)


# 启动数据分析器应用
async def main():
    """
    启动数据分析器应用
    """
    # 示例数据
    data = pd.DataFrame(
        {
            "A": np.random.randn(100),
            "B": np.random.randn(100),
        }
    )

    app = DataAnalysisApp(data)
    await app.start("0.0.0.0", 8000)
    print("Data Analysis Service is running on http://0.0.0.0:8000")

if __name__ == "__main__":
    asyncio.run(main())