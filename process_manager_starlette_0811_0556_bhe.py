# 代码生成时间: 2025-08-11 05:56:26
import subprocess
import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

"""
进程管理器 Starlette 应用程序
提供启动、停止和列出进程的服务
"""

class ProcessManager:
    def __init__(self):
        self.processes = {}

    def start_process(self, command):
        """
        启动一个新的进程
        :param command: 要执行的命令
        :return: 启动成功的进程ID
        """
        try:
            process = subprocess.Popen(command, shell=True)
            self.processes[process.pid] = process
            return process.pid
        except Exception as e:
            raise Exception(f"Failed to start process: {str(e)}")

    def stop_process(self, process_id):
        """
        停止一个进程
        :param process_id: 要停止的进程ID
        """
        if process_id in self.processes:
            process = self.processes.pop(process_id)
            process.terminate()
            process.wait()
        else:
            raise Exception(f"Process with ID {process_id} not found.")

    def list_processes(self):
        """
        列出所有进程
        :return: 进程列表
        """
        return {pid: p.pid for pid, p in self.processes.items()}

# 创建 ProcessManager 实例
process_manager = ProcessManager()

# 路由和视图函数
routes = [
    Route("/start", endpoint=lambda request: JSONResponse(
        content={"pid": process_manager.start_process(request.query_params.get("command"))},
        status_code=HTTP_200_OK)),
    Route("/stop", endpoint=lambda request: JSONResponse(
        content={"message": "Process stopped"},
        status_code=HTTP_200_OK)),
    Route("/list", endpoint=lambda request: JSONResponse(
        content=process_manager.list_processes(),
        status_code=HTTP_200_OK)),
]

# 启动 Starlette 应用程序
if __name__ == "__main__":
    uvicorn.run(Starlette(routes=routes), host="0.0.0.0", port=8000)