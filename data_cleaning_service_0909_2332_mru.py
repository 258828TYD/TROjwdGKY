# 代码生成时间: 2025-09-09 23:32:39
import pandas as pd
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.exceptions import HTTPException as StarletteHTTPException


# 数据清洗服务类
class DataCleaningService:
    def __init__(self, data):
        self.data = data  # pandas DataFrame

    def remove_null_values(self, columns=None):  # 去除空值
        """
        移除指定列的数据中的空值
        :param columns: 需要移除空值的列名列表，如果为None，则移除所有列的空值
        """
        if columns:
            return self.data.dropna(subset=columns)
        else:
            return self.data.dropna()

    def fill_null_values(self, value):  # 填充空值
        """
        填充所有列的空值为指定值
        :param value: 用于填充的值
        """
        return self.data.fillna(value)

    def normalize_data(self):  # 归一化数据
        """
        对所有数值型数据进行归一化处理
        """
        return (self.data - self.data.mean()) / self.data.std()

    def encode_categorical_data(self):  # 编码分类数据
        """
        对分类数据进行编码
        """
        return pd.get_dummies(self.data)


# API 路由和异常处理
async def clean_data(request):
    """
    清洗数据的API接口
    """
    try:
        data = await request.json()
        df = pd.DataFrame(data)
        cleaning_service = DataCleaningService(df)
        cleaned_data = cleaning_service.remove_null_values()
        return JSONResponse(content=cleaned_data.to_dict('records'))
    except pd.errors.EmptyDataError:
        raise StarletteHTTPException(status_code=400, detail="Empty data provided")
    except Exception as e:
        raise StarletteHTTPException(status_code=500, detail=str(e))

# 创建 Starlette 应用
app = Starlette(debug=True, routes=[
    Route("/clean", endpoint=clean_data, methods=["POST"])
])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)