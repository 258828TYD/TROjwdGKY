# 代码生成时间: 2025-08-17 03:53:34
import os
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.encoders import jsonable_encoder

# 定义批量文件重命名工具的API
app = FastAPI(title="Bulk File Renamer")

# 定义批量重命名文件的路由
@app.post("/rename")
async def rename_files(files: list[UploadFile] = File(...), new_names: list[str] = File(...)) -> JSONResponse:
    """
    批量重命名文件。

    参数:
        files (list[UploadFile]): 要重命名的文件列表。
        new_names (list[str]): 新的文件名列表。

    返回:
        JSONResponse: 包含重命名结果的JSON响应。
    """
    try:
        # 确保文件数量和新文件名数量一致
        if len(files) != len(new_names):
            raise ValueError("文件数量和新文件名数量不一致。")

        # 存储重命名结果
        results = []

        # 遍历文件和新文件名，执行重命名操作
        for file, new_name in zip(files, new_names):
            # 获取文件存储路径
            file_location = os.path.join("./files", file.filename)
            # 获取新文件存储路径
            new_file_location = os.path.join("./files", new_name)

            # 将上传的文件保存到服务器
            with open(file_location, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            # 重命名文件
            os.rename(file_location, new_file_location)

            # 记录重命名结果
            results.append({"old_name": file.filename, "new_name": new_name})

        # 返回重命名结果
        return JSONResponse(content=jsonable_encoder(results))
    except Exception as e:
        # 处理异常
        raise StarletteHTTPException(status_code=400, detail=str(e))

# 定义一个路由以提供文件下载功能
@app.get("/files/{filename}")
async def download_file(filename: str):
    """
    下载文件。

    参数:
        filename (str): 文件名。
    """
    file_location = os.path.join("./files", filename)
    return FileResponse(path=file_location, media_type="application/octet-stream")

# 运行服务器
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
