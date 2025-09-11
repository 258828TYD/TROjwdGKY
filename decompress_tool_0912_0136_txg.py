# 代码生成时间: 2025-09-12 01:36:38
import zipfile
import tarfile
# 增强安全性
import os
from starlette.applications import Starlette
# 改进用户体验
from starlette.responses import FileResponse, JSONResponse
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

# 启动文件解压工具的 Starlette 应用
class DecompressorApp(Starlette):
    def __init__(self):
        # 定义路由
        routes = [
            Route("/decompress", endpoint=DecompressEndpoint, methods=["POST"]),
# 改进用户体验
            Mount("/static", app=StaticFiles(directory="static")),
        ]
        super().__init__(routes=routes)

# 文件解压端点
# 改进用户体验
class DecompressEndpoint:
# 增强安全性
    async def post(self, request):
        # 获取上传的文件数据
        contents = await request.form()
# 增强安全性
        file = contents.get("file")
        if not file:
            return JSONResponse(content={"error": "No file provided."}, status_code=400)

        # 确保文件存在
        if not file.file:
            return JSONResponse(content={"error": "No file attached."}, status_code=400)

        # 保存文件到临时目录
        file_location = await file.save("tempfile.zip")

        try:
# 添加错误处理
            # 检查文件类型并解压
            with open(file_location, "rb") as f:
                filename = f.name
                if zipfile.is_zipfile(f):
# 添加错误处理
                    with zipfile.ZipFile(f, "r") as zip_ref:
                        zip_ref.extractall(".")
                elif tarfile.is_tarfile(f):
                    with tarfile.TarFile(f, "r") as tar_ref:
                        tar_ref.extractall(".")
                else:
                    return JSONResponse(content={"error": "Unsupported file type."}, status_code=415)
        except zipfile.BadZipFile:
# 扩展功能模块
            return JSONResponse(content={"error": "Invalid zip file."}, status_code=400)
        except tarfile.TarError:
            return JSONResponse(content={"error": "Invalid tar file."}, status_code=400)
        except Exception as e:
            return JSONResponse(content={"error": str(e)}, status_code=500)
        finally:
            # 删除临时文件
            os.remove(file_location)

        return JSONResponse(content={"message": "File decompressed successfully."})

# 运行应用
if __name__ == "__main__":
# 添加错误处理
    import uvicorn
# 增强安全性
    uvicorn.run(DecompressorApp, host="0.0.0.0", port=8000)