from typing import Iterable, Any

from src.core.task_model import Task


class GeneratorTaskSource:
    def __init__(self, count: int = 10, description: Any = None):
        self._count = count
        self.description = description or ""

    def get_tasks(self) -> Iterable[Task]:
        for i in range(self._count):
            yield Task(
                description=self.description,
                priority=(i % 4) + 1
            )
