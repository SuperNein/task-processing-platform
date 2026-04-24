from typing import Iterable

from src.core.task_model import Task
from src.protocols.source import TaskSource
from src.services.validation import ProtocolValidator


class TaskSourceLoader:
    _validator = ProtocolValidator(protocol=TaskSource)

    def __init__(self, source: TaskSource):
        self._validator.validate(source)
        self._source = source

    def load(self) -> Iterable[Task]:
        """
        Get tasks from source.
        :return:   Iterable of models.Task
        """
        return self._source.get_tasks()
