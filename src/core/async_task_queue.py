import asyncio

from src.core.task_model import Task
from src.core.exceptions.task_queue_errors import (
    QueueClosedError,
    QueueShutdownError,
)


class _Sentinel:
    """Sentinel object for closing async queue"""
    pass


class AsyncTaskQueue:
    """asyncio.Queue composition for Task model"""
    _sentinel = _Sentinel()

    __slots__ = ("_queue", "_closed")

    def __init__(self) -> None:
        self._queue: asyncio.Queue[Task | object] = asyncio.Queue()
        self._closed: bool = False


    @property
    def is_closed(self) -> bool:
        return self._closed

    def close(self, workers: int) -> None:
        """
        Close queue from putting new tasks
        Queue shutdown signal
        """
        if self.is_closed:
            return

        self._closed = True

        for _ in range(workers):
            self._queue.put_nowait(self._sentinel)


    async def put(self, task: Task) -> None:
        """Put a task into the queue."""
        if self._closed:
            raise QueueClosedError

        if not isinstance(task, Task):
            raise TypeError(
                f"AsyncTaskQueue accepts only Task instances, got {type(task)}"
            )

        await self._queue.put(task)


    async def get(self) -> Task:
        """Remove and return task from the queue."""
        task = await self._queue.get()

        if task is self._sentinel:
            raise QueueShutdownError

        return task


    def task_done(self) -> None:
        """Indicate that a formerly enqueued task is complete"""
        self._queue.task_done()

    async def join(self) -> None:
        """Block until all tasks in the queue have been gotten and processed."""
        await self._queue.join()

    def qsize(self) -> int:
        """Number of tasks in the queue."""
        return self._queue.qsize()

    def empty(self) -> bool:
        """Return True if the queue is empty, False otherwise."""
        return self._queue.empty()