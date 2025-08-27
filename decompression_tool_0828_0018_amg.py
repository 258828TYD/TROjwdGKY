# 代码生成时间: 2025-08-28 00:18:36
import asyncio
import shutil
from starlette.applications import Starlette
from starlette.responses import FileResponse, JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from zipfile import ZipFile, BadZipFile
from pathlib import Path

# 压缩文件解压工具的星LETTE应用程序
class DecompressionTool(Starlette):
    """
    使用STARLETTE框架创建的压缩文件解压工具。
    """
    def __init__(self):
        # 定义路由
        routes = [
            Route("/decompress", self.decompress_file, methods=["POST"]),
        ]
        super().__init__(routes=routes)

    async def decompress_file(self, request):
        """
        处理文件上传和解压的请求。
        :param request: Starlette请求对象
        :return: JSON响应，包含解压结果或错误信息。
        """
        try:
            # 获取上传的文件
            file = await request.form()
            uploaded_file = file.get('file')
            if not uploaded_file:
                return JSONResponse(
                    content={"error": "No file uploaded."}, status_code=HTTP_400_BAD_REQUEST
                )

            # 确保文件是ZIP格式
            if not uploaded_file.filename.endswith('.zip'):
                return JSONResponse(
                    content={"error": "Unsupported file type. Only .zip files are accepted."}, status_code=HTTP_400_BAD_REQUEST
                )

            # 创建临时目录和解压目录
            temp_dir = Path('temp')
            temp_dir.mkdir(exist_ok=True)
            extracted_dir = temp_dir / 'extracted'
            extracted_dir.mkdir(exist_ok=True)

            # 保存上传的文件到临时目录
            file_path = temp_dir / uploaded_file.filename
            with open(file_path, 'wb') as f:
                f.write(await uploaded_file.read())

            # 解压ZIP文件
            with ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(extracted_dir)

            # 返回解压成功的消息
            return JSONResponse(
                content={"message": "File decompressed successfully."}, status_code=HTTP_200_OK
            )

        except BadZipFile:
            return JSONResponse(
                content={"error": "Invalid ZIP file."}, status_code=HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            # 捕获任何其他异常并返回500错误
            return JSONResponse(
                content={"error": str(e)}, status_code=HTTP_500_INTERNAL_SERVER_ERROR
            )
        finally:
            # 清理临时文件和目录
            if temp_dir.exists():
                shutil.rmtree(temp_dir)

# 运行应用程序
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(DecompressionTool(), host="0.0.0.0", port=8000)