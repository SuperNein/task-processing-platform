from typing import Optional, Iterator, Iterable, Callable

from src.core.task_model import Task
from src.core.enums import TaskPriority, TaskStatus


class _TaskQueueFilter:
    """TaskQueue filter proxy"""
    def __init__(self, queue: TaskQueue):
        self._queue = queue

    def status(self, status: TaskStatus) -> Iterator[Task]:
        """Return iterator of tasks with given status"""
        for task in self._queue:
            if task.status == status:
                yield task

    def priority(
            self,
            min_priority: TaskPriority | int,
            max_priority: Optional[TaskPriority | int] = None,
    ) -> Iterator[Task]:
        """
        Return iterator of tasks with priority between min_priority and max_priority
        """
        if max_priority is None:
            max_priority = min_priority

        for task in self._queue:
            if min_priority <= task.priority <= max_priority:
                yield task

    def __call__(self, predicate: Callable[[Task], bool]) -> Iterator[Task]:
        """Filter tasks based on predicate function"""
        if not callable(predicate):
            raise TypeError('TaskQueue filter predicate must be callable')

        for task in self._queue:
            if predicate(task):
                yield task


class TaskQueue:
    """Task iterable collection"""
    __slots__ = ("_tasks", "_filter")

    def __init__(self, tasks: Optional[Iterable[Task]] = None):
        self._filter = _TaskQueueFilter(self)
        self._tasks = []
        if tasks is not None:
            self.extend(tasks)

    @property
    def filter(self) -> _TaskQueueFilter:
        """
        Access to queue filters
        Use filter methods or call with predicate to filter tasks
        Read-only

        Examples: TaskQueue.filter(lambda task: task.status == TaskStatus.new)
                 TaskQueue.filter.status(TaskStatus.new)
                 TaskQueue.filter.priority(TaskPriority.normal)
        """
        return self._filter

    @filter.setter
    def filter(self, value: _TaskQueueFilter):
        raise AttributeError("'TaskQueue.filter' is read-only")


    def __iter__(self) -> Iterator[Task]:
        return iter(self._tasks)

    def __len__(self) -> int:
        return len(self._tasks)

    def __bool__(self) -> bool:
        return bool(self._tasks)

    def __add__(self, other: Iterable[Task]) -> TaskQueue:
        new_queue = self.copy()
        new_queue.extend(other)
        return new_queue

    def __iadd__(self, other: Iterable[Task]) -> TaskQueue:
        self.extend(other)
        return self

    def extend(self, tasks: Iterable[Task]) -> None:
        """Extend queue with iterable of tasks"""
        if not isinstance(tasks, Iterable):
            raise TypeError(
                f"Can only extend TaskQueue with Iterable, not {type(tasks)}"
            )
        for task in tasks:
            self.push(task)

    def push(self, task: Task) -> None:
        """Push task to the end of queue"""
        if not isinstance(task, Task):
            raise TypeError(f"TaskQueue must store Task, not {type(task)}")
        self._tasks.append(task)

    def pop(self) -> Task:
        """Return and remove task from start of queue"""
        if not self._tasks:
            raise IndexError("TaskQueue is empty")
        return self._tasks.pop(0)

    def peek(self) -> Task:
        """Return task from start of queue"""
        if not self._tasks:
            raise IndexError("TaskQueue is empty")
        return self._tasks[0]

    def copy(self) -> TaskQueue:
        """Return copy of queue"""
        return TaskQueue(self._tasks.copy())

    def __repr__(self) -> str:
        return f"TaskQueue(tasks={self._tasks!r})"
