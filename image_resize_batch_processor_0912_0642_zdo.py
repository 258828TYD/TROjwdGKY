# 代码生成时间: 2025-09-12 06:42:11
import os
import shutil
from PIL import Image
from starlette.applications import Starlette
from starlette.responses import FileResponse
from starlette.routing import Route
from starlette.requests import Request

# 常量定义
DEFAULT_OUTPUT_FORMAT = "JPEG"
DEFAULT_QUALITY = 85

# 定义一个函数来调整图片尺寸
def resize_image(input_image_path, output_image_path, new_size, format=DEFAULT_OUTPUT_FORMAT, quality=DEFAULT_QUALITY):
    with Image.open(input_image_path) as img:
        resized_img = img.resize(new_size, Image.ANTIALIAS)
        resized_img.save(output_image_path, format=format, quality=quality)

# 定义一个函数来处理批量调整图片尺寸
def process_batch_resize(input_dir, output_dir, new_size, format=DEFAULT_OUTPUT_FORMAT, quality=DEFAULT_QUALITY):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        try:
            resize_image(input_path, output_path, new_size, format, quality)
            print(f"Resized {filename}")
        except IOError as e:
            print(f"Error resizing {filename}: {e}")

# 创建一个Starlette应用
app = Starlette(debug=True)

# 定义路由
@app.route("/resize", methods=["POST"])
async def resize_endpoint(request: Request):
    # 获取请求数据
    input_dir = request.json().get("input_dir")
    output_dir = request.json().get("output_dir")
    new_size = request.json().get("new_size")

    # 错误处理
    if not input_dir or not output_dir or not new_size:
        return {"error": "Missing input or output directory, or new size"}

    # 执行批量调整尺寸操作
    process_batch_resize(input_dir, output_dir, new_size)
    return {"message": "Batch resize completed successfully"}

# 定义路由以返回静态图片文件
@app.route("/images/{filename:path}")
async def serve_file(request: Request):
    output_dir = request.json().get("output_dir", "./output")  # 默认输出目录
    file_path = os.path.join(output_dir, request.path_params["filename"])
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        return {"error": "File not found"}

# 将路由添加到应用
routes = [
    Route("/resize", resize_endpoint),
    Route("/images/{filename:path}", serve_file)
]
app.routes.extend(routes)

# 以下是__main__区块，用于直接运行应用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)