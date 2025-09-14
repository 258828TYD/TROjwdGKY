# 代码生成时间: 2025-09-15 01:11:03
import asyncio
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from tortoise import Tortoise
from tortoise.exceptions import OperationalError
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel
from typing import Any, Dict

# 数据库迁移配置类
class DatabaseMigrationConfig(BaseModel):
    database_url: str
    generate_models: bool = False

# 数据库迁移工具类
class DatabaseMigrationTool:
    def __init__(self, config: DatabaseMigrationConfig):
        self.config = config
        self.models = []

    async def init_app(self):
        """初始化数据库连接和模型。"""
        await Tortoise.init(
            db_url=self.config.database_url,
            modules={'models': ['your_app.models']}  # 你的模型模块路径
        )
        await Tortoise.generate_schemas()
        if self.config.generate_models:
            self.models = await self.generate_models_from_schemas()

    async def generate_models_from_schemas(self) -> list:
        """从数据库生成模型。"""
        try:
            schema_description = await Tortoise.get_connection('default').get_schema_description()
            return pydantic_model_creator(schema_description)
        except OperationalError as e:
            raise StarletteHTTPException(status_code=500, detail=str(e))

    async def run_migration(self):
        """运行数据库迁移。"""
        try:
            await Tortoise._run_migrations()
            return {"message": "Migration successful"}
        except OperationalError as e:
            raise StarletteHTTPException(status_code=500, detail=str(e))

# RESTful API 端点
async def migrate_db(request):
    """RESTful API 端点，用于触发数据库迁移。"""
    config = DatabaseMigrationConfig(**request.query_params)
    migration_tool = DatabaseMigrationTool(config)
    await migration_tool.init_app()
    result = await migration_tool.run_migration()
    return JSONResponse(result)

# 路由配置
routes = [
    Route("/migrate", migrate_db, methods=["GET"]),
]

# Starlette 应用
app = Starlette(routes=routes)

# 确保异步函数在同步环境中正常运行
if __name__ == "__main__":
    from uvicorn import run
    run(app, host="0.0.0.0", port=8000)
