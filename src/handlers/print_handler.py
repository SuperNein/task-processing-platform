import asyncio

from src.core.task_model import Task


class PrintHandler:
    """Handler: print task info with delay"""
    async def handle(self, task: Task) -> None:
        await asyncio.sleep(task.priority * 0.05)
        print(f"  > {task}")
