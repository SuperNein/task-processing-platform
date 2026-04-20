from typing import Protocol, Iterable, runtime_checkable

from src.core.models import Task


@runtime_checkable
class TaskSource(Protocol):
    def get_tasks(self) -> Iterable[Task]:
        """
        Get all tasks from source.
        :return:   Iterable of models.Task
        """
        ...
