import asyncio

from src.protocols.handler import TaskHandler
from src.services.validation import ProtocolValidator
from src.core.task_model import Task
from src.core.async_task_queue import AsyncTaskQueue
from src.core.exceptions.task_queue_errors import QueueShutdownError
from src.core.exceptions.executor_errors import (
    TaskProcessingError,
    ExecutorNotStartedError,
    HandlerNotRegisteredError,
)


class AsyncTaskExecutor:
    """
    Async Task Executor

    Supports multiple competitive workers.
    Managed as context manager:

    Example:
        async with AsyncTaskExecutor(workers=3) as executor:
            executor.register_handler(MyHandler())
            await executor.submit(task)
            await executor.wait_all()
    """
    validator = ProtocolValidator(protocol=TaskHandler)

    def __init__(self, workers: int = 2) -> None:
        self._workers = workers
        self._running = False

        self._queue: AsyncTaskQueue | None = None
        self._handler: TaskHandler | None = None

        self._worker_tasks: list[asyncio.Task] = []
        self._errors: list[TaskProcessingError] = []


    def register_handler(self, handler: TaskHandler) -> None:
        """
        Register task handler

        Raises:
            TypeError: if handler miss following TaskHandler protocol.
        """
        self.validator.validate(handler)
        self._handler = handler

    async def submit(self, task: Task) -> None:
        """Submit task into queue

        Raises:
            ExecutorNotStartedError: if executor is not started.
        """
        if not self._running or self._queue is None:
            raise ExecutorNotStartedError

        await self._queue.put(task)

    async def wait_all(self) -> None:
        """Wait for all tasks to complete"""
        if self._queue:
            await self._queue.join()

    @property
    def errors(self) -> list[TaskProcessingError]:
        """Task processing errors"""
        return self._errors


    async def __aenter__(self) -> AsyncTaskExecutor:
        self._queue = AsyncTaskQueue()
        self._running = True
        self._worker_tasks = [
            asyncio.create_task(self._worker_loop(f"worker-{i}"))
            for i in range(self._workers)
        ]
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> bool:
        if self._queue:
            self._queue.close(workers=self._workers)

        await asyncio.gather(*self._worker_tasks, return_exceptions=True)

        self._running = False
        return False


    async def _worker_loop(self, name: str) -> None:
        """Takes a task from the queue and processes"""
        async for task in self._queue:
            try:
                if self._handler is None:
                    raise HandlerNotRegisteredError

                await self._handler.handle(task)

            except Exception as e:
                error = TaskProcessingError(task, e)
                self._errors.append(error)
