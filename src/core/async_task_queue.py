import logging
import asyncio

from src.core.task_model import Task
from src.core.exceptions.task_queue_errors import (
    QueueClosedError,
    QueueShutdownError,
)


logger = logging.getLogger(__name__)


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
        logger.info(f"Queue closed (workers={workers})")

        for _ in range(workers):
            self._queue.put_nowait(self._sentinel)


    async def put(self, task: Task) -> None:
        """Put a task into the queue."""
        if self._closed:
            logger.warning("Attempt to put task into closed queue")
            raise QueueClosedError

        if not isinstance(task, Task):
            raise TypeError(
                f"AsyncTaskQueue accepts only Task instances, got {type(task)}"
            )

        await self._queue.put(task)
        logger.debug(f"Task enqueued id={task.id}")


    async def get(self) -> Task:
        """Remove and return task from the queue."""
        task = await self._queue.get()

        if task is self._sentinel:
            logger.debug("Queue shutdown signal received")
            self._queue.task_done()
            raise QueueShutdownError

        logger.debug(f"Task dequeued id={task.id}")
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

    def __aiter__(self):
        return self._iter()

    async def _iter(self):
        """Async generator for __aiter__"""
        while True:
            try:
                task = await self.get()
            except QueueShutdownError:
                break

            try:
                yield task
            finally:
                self.task_done()
