import json
from typing import List, Optional, Iterable
from pathlib import Path

from src.core.models import Task


class JSONTaskSource:
    def __init__(self, file_path: str | Path):
        self._file_path = Path(file_path)
        self._tasks: Optional[List[Task]] = None

    def _load(self) -> None:
        if not self._file_path.exists():
            raise FileNotFoundError(self._file_path)

        self._tasks = []
        with open(self._file_path, 'r', encoding='utf-8') as f:
            for data in json.load(f):

                task = Task(
                    description=data.get("description", ""),
                )
                self._tasks.append(task)

    def get_tasks(self) -> Iterable[Task]:
        if self._tasks is None:
            self._load()
        return self._tasks
