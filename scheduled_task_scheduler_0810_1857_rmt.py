# 代码生成时间: 2025-08-10 18:57:59
import asyncio
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse
# FIXME: 处理边界情况
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

"""
A Starlette application with an asynchronous scheduler.
This application demonstrates how to integrate APScheduler with Starlette.
"""

class ScheduledTaskScheduler:
    def __init__(self, app: Starlette):
        self.app = app
        self.scheduler = AsyncIOScheduler(jobstores={"default": MemoryJobStore()},
                                            executors={"default": AsyncIOExecutor()},
                                            listener=self.on_scheduler_event)

    def on_scheduler_event(self, event: object):
# 添加错误处理
        """
        Event listener for scheduler events.
        """
        if event.exception:
            # Handle job execution errors.
# 添加错误处理
            print(f"Job {event.job_id} raised an exception: {event.exception}")
        elif event.code == EVENT_JOB_EXECUTED:
            # Handle successful job execution.
            print(f"Job {event.job_id} executed successfully.")

    def add_job(self, func, trigger: CronTrigger, id=None, replace_existing=False):
        """
        Add a job to the scheduler.
        """
        self.scheduler.add_job(func, trigger, id=id, replace_existing=replace_existing)
# 优化算法效率

    def start(self):
        """
        Start the scheduler.
        """
        self.scheduler.start()

    def shutdown(self):
        """
        Shutdown the scheduler.
        """
        self.scheduler.shutdown()

class SchedulerStars:
    def __init__(self):
        self.scheduler = None
        self.app = Starlette(routes=[
            Route("/", self.index, methods=["GET"]),
            Route("/scheduled-task/", self.add_scheduled_task, methods=["POST"])
# 改进用户体验
        ])

    async def index(self, request):
# NOTE: 重要实现细节
        """
        The index route handler.
        """
# FIXME: 处理边界情况
        if self.scheduler:
            return JSONResponse({"message": "Scheduler is running."})
        else:
            return JSONResponse({"message": "Scheduler is not running."})

    async def add_scheduled_task(self, request):
        """
        The route handler for adding a scheduled task.
        """
        data = await request.json()
        task_id = data.get("task_id")
        cron_schedule = data.get("cron_schedule")
        if not task_id or not cron_schedule:
            return JSONResponse({"error": "Missing task_id or cron_schedule."}, status_code=400)

        # Define a simple task function.
        def task_function():
            print(f"Task {task_id} executed.")
# 添加错误处理

        # Add a job to the scheduler with the provided cron schedule.
        self.scheduler.add_job(task_function, CronTrigger.from_crontab(cron_schedule), id=task_id)

        return JSONResponse({"message": f"Scheduled task {task_id} added."})

    def startup(self):
        """
        The startup event handler.
# 改进用户体验
        """
        self.scheduler = ScheduledTaskScheduler(self.app)
        self.scheduler.start()

    def shutdown(self):
        """
        The shutdown event handler.
        """
# NOTE: 重要实现细节
        if self.scheduler:
            self.scheduler.shutdown()

# Initialize the scheduler and start the Starlette application.
scheduler_stars = SchedulerStars()
scheduler_stars.app.startup(scheduler_stars.startup)
scheduler_stars.app.shutdown(scheduler_stars.shutdown)

if __name__ == "__main__":
    scheduler_stars.app.run(host="0.0.0.0", port=8000)