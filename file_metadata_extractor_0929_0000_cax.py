# 代码生成时间: 2025-09-29 00:00:31
import os
from datetime import datetime
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

# 文档字符串：文件元数据提取器
class FileMetadataExtractor:
    def __init__(self):
        """
        文件元数据提取器初始化
        """
        self.supported_extensions = {'txt', 'pdf', 'docx', 'xlsx', 'jpg', 'png'}

    def extract_metadata(self, file_path):
        """
        提取文件的元数据
        
        :param file_path: 文件的路径
        :return: 包含文件元数据的字典
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            if os.path.splitext(file_path)[1][1:] not in self.supported_extensions:
                raise ValueError(f"Unsupported file extension: {os.path.splitext(file_path)[1][1:]}")

            file_metadata = {
                'filename': os.path.basename(file_path),
                'file_path': file_path,
                'file_size': os.path.getsize(file_path),
                'creation_time': datetime.fromtimestamp(os.path.getctime(file_path)).strftime("%Y-%m-%d %H:%M:%S"),
                'modification_time': datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d %H:%M:%S"),
                'extension': os.path.splitext(file_path)[1][1:],
            }
            return file_metadata
        except Exception as e:
            return {'error': str(e)}

# Starlette 应用
app = Starlette(debug=True)

@app.route("/extract", methods=["GET"])
async def extract_metadata_route(request):
    """
    提取给定文件的元数据
    
    :param request: Starlette 请求对象
    :return: JSON 响应包含文件元数据
    """
    file_path = request.query_params.get("file_path")
    if not file_path:
        return JSONResponse({'error': 'Missing file_path parameter'})

    extractor = FileMetadataExtractor()
    metadata = extractor.extract_metadata(file_path)
    return JSONResponse(metadata)

# 定义路由
routes = [
    Route("/extract", extract_metadata_route),
]

app.add_routes(routes)