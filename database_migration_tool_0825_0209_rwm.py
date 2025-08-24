# 代码生成时间: 2025-08-25 02:09:08
import asyncio
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
import uvicorn
from alembic.command import upgrade, downgrade
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# DatabaseMigrationTool class that handles database migrations
class DatabaseMigrationTool:
    def __init__(self, alembic_cfg_path, db_url):
        self.alembic_cfg_path = alembic_cfg_path
        self.db_url = db_url
        self.engine = create_engine(db_url)
        self.alembic_cfg = Config(self.alembic_cfg_path)
        self.alembic_cfg.set_main_option('sqlalchemy.url', db_url)

    # Perform database upgrade
    async def upgrade_db(self):
        try:
            upgrade(self.alembic_cfg, 'head')
            return {'status': 'success', 'message': 'Database upgraded successfully'}
        except SQLAlchemyError as e:
            return {'status': 'error', 'message': str(e)}

    # Perform database downgrade
    async def downgrade_db(self):
        try:
            downgrade(self.alembic_cfg, '-1')
            return {'status': 'success', 'message': 'Database downgraded successfully'}
        except SQLAlchemyError as e:
            return {'status': 'error', 'message': str(e)}

# Create a Starlette application with routes for database migration
app = Starlette(
    routes=[
        Route('/api/upgrade', endpoint=lambda request: JSONResponse(
            await DatabaseMigrationTool('alembic.ini', request.query_params['db_url']).upgrade_db()),
            methods=['POST']),
        Route('/api/downgrade', endpoint=lambda request: JSONResponse(
            await DatabaseMigrationTool('alembic.ini', request.query_params['db_url']).downgrade_db()),
            methods=['POST']),
    ]
)

# Entry point for the application
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
