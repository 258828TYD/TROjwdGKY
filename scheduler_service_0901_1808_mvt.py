# 代码生成时间: 2025-09-01 18:08:19
import asyncio
import logging
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.executors.asyncio import AsyncIOExecutor


# 设置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 定时任务调度器服务
class SchedulerService:
    def __init__(self, scheduler):
        self.scheduler = scheduler

    async def start(self):
        """启动定时任务调度器"""
        self.scheduler.start()
        logger.info("Scheduler started")

    async def add_job(self, job_func, trigger):
        "