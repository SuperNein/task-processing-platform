import logging
import asyncio

from src.protocols.handler import TaskHandler
from src.services.validation import ProtocolValidator
from src.core.task_model import Task
from src.core.async_task_queue import AsyncTaskQueue
from src.core.exceptions.executor_errors import (
    TaskProcessingError,
    ExecutorNotStartedError,
    HandlerNotRegisteredError,
)


logger = logging.getLogger(__name__)


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

        logger.info(f"Handler registered: {handler.__class__.__name__}", )


    async def submit(self, task: Task) -> None:
        """Submit task into queue

        Raises:
            ExecutorNotStartedError: if executor is not started.
        """
        if not self._running or self._queue is None:
            logger.error("Submit called before executor start")
            raise ExecutorNotStartedError

        await self._queue.put(task)

        logger.debug(f"Task submitted id={task.id}", )


    async def wait_all(self) -> None:
        """Wait for all tasks to complete"""
        if self._queue:
            logger.info("Waiting for all tasks to complete...")
            await self._queue.join()
            logger.info("All tasks completed")


    @property
    def errors(self) -> list[TaskProcessingError]:
        """Task processing errors"""
        return self._errors


    async def __aenter__(self) -> AsyncTaskExecutor:
        self._queue = AsyncTaskQueue()
        self._running = True

        logger.info(f"Executor started (workers={self._workers})")

        self._worker_tasks = [
            asyncio.create_task(self._worker_loop(f"worker-{i}"))
            for i in range(self._workers)
        ]
        return self


    async def __aexit__(self, exc_type, exc_val, exc_tb) -> bool:
        if self._queue:
            logger.info("Shutting down executor...")
            self._queue.close(workers=self._workers)

        await asyncio.gather(*self._worker_tasks, return_exceptions=True)

        self._running = False
        logger.info("Executor stopped")

        return False


    async def _worker_loop(self, name: str) -> None:
        """Takes a task from the queue and processes"""
        logger.debug(f"{name} started", )

        async for task in self._queue:

            logger.debug(f"{name} processing task id={task.id}")

            try:
                if self._handler is None:
                    raise HandlerNotRegisteredError

                await self._handler.handle(task)

                logger.info(f"{name} completed task id={task.id}")

            except Exception as e:
                error = TaskProcessingError(task, e)
                self._errors.append(error)

                logger.error(f"{name} failed task id={task.id} error={e}",)

        logger.debug(f"{name} stopped")
