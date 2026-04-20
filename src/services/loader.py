from typing import Iterable, Optional

from src.core.task_model import Task
from src.protocols.source import TaskSource
from src.services.validation import SourceValidator


class TasksLoader:
    def __init__(self, source: TaskSource, validator: Optional[SourceValidator] = None):
        if validator is None:
            validator = SourceValidator()

        validator.validate(source)
        self._source = source

    def load(self) -> Iterable[Task]:
        """
        Get tasks from source.
        :return:   Iterable of models.Task
        """
        return self._source.get_tasks()
