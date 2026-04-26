import asyncio

from src.core.task_model import Task


class FailingHandler:
    """Handler: raise exception on high priority"""
    async def handle(self, task: Task) -> None:
        if task.priority >= 3:
            raise ValueError(f"Too high priority: {task.priority}")

        await asyncio.sleep(0.05)

        print(f"  > [{task.id}] processed")
