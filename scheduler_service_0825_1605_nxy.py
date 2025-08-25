# 代码生成时间: 2025-08-25 16:05:13
import asyncio
import schedule
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from http import HTTPStatus
import logging

# 设置日志记录器
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 定义定时任务类
class SchedulerService:
    def __init__(self):
        self.jobs = []

    async def add_job(self, job_func, trigger, *args, **kwargs):
        """添加定时任务到调度器"""
        job = schedule.every(trigger).do(job_func, *args, **kwargs)
        self.jobs.append(job)
        logger.info(f'Job added: {job_func.__name__} with trigger {trigger}')

    async def run_pending(self):
        """运行所有待处理的定时任务"""
        schedule.run_pending()
        logger.info('Running pending jobs...')

# 定时任务路由
async def job_route(request):
    try:
        scheduler = request.state.scheduler
        await scheduler.run_pending()
        return JSONResponse({"message": "Jobs executed"})
    except Exception as e:
        logger.error(f'Error executing jobs: {e}')
        raise StarletteHTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))

# 创建Starlette应用
async def app(scope, receive, send):
    if scope['type'] == 'http':
        scheduler = SchedulerService()
        # 添加定时任务
        await scheduler.add_job(print, '10s', 'Hello, World!')
        # 这里可以添加更多定时任务

        # 定义路由
        routes = [
            Route('/', job_route, methods=['POST'], endpoint=scheduler),
        ]

        return Starlette(routes=routes, lifespan={'scheduler': scheduler})
    else:
        raise ValueError('Unsupported scope')

# 运行定时任务调度器
if __name__ == '__main__':
    asyncio.run(app({'type': 'http'}, None, None))
