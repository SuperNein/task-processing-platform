from typing import List, Optional, Iterable, Dict

from src.core.task_model import Task
from src.common.constants import API_STUB_TASKS


class APIStubTasksSource:
    def __init__(self, url: str):
        self._url = url
        self._data: Optional[List[Dict]] = None

    def _request(self) -> None:
        self._data = [
            {"description": f"api_task_{i}"}
            for i in range(API_STUB_TASKS)
        ]

    def get_tasks(self) -> Iterable[Task]:
        if self._data is None:
            self._request()

        return [
            Task(description=task["description"])
            for task in self._data
        ]
