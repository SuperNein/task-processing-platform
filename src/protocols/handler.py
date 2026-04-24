from typing import Protocol, runtime_checkable

from src.core.task_model import Task


@runtime_checkable
class TaskHandler(Protocol):
    """
    Task handler protocol class
    Every object realising handle() method realising this protocol
    """
    async def handle(self, task: Task) -> None:
        """Handle one task"""
        ...
