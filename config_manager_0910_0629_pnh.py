# 代码生成时间: 2025-09-10 06:29:04
# config_manager.py
# 使用STARLETTE框架实现的配置文件管理器

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.config import Config


# 定义配置文件管理器类
class ConfigManager:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.config = Config(self.config_file)
        
    # 获取配置项
    def get_item(self, key):
        try:
            return self.config(key)
        except KeyError:
            raise KeyError(f"Key {key} not found in config file.")
        
    # 设置配置项
    def set_item(self, key, value):
        try:
            self.config[key] = value
            self.config.save()
        except Exception as e:
            raise Exception(f"Failed to set config item: {str(e)}")
        
    # 删除配置项
    def delete_item(self, key):
        try:
            if key in self.config:
                del self.config[key]
                self.config.save()
            else:
                raise KeyError(f"Key {key} not found in config file.")
        except Exception as e:
            raise Exception(f"Failed to delete config item: {str(e)}")


# 创建Starlette应用
app = Starlette(debug=True)

# 定义路由
@app.route("/config/{key}", methods=["GET", "POST", "DELETE"])
async def config_route(request):
    config_manager = ConfigManager()
    key = request.path_params.get("key")
    
    if request.method == "GET":
        value = config_manager.get_item(key)
        return JSONResponse({key: value})
    elif request.method == "POST":
        value = request.json().get(key)
        config_manager.set_item(key, value)
        return JSONResponse({key: value})
    elif request.method == "DELETE":
        config_manager.delete_item(key)
        return JSONResponse({})
    else:
        return JSONResponse({}, status_code=405)


# 启动应用
if __name__ == "__main__":
    app.run()
