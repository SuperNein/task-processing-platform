import pytest
import asyncio

from src.core.task_model import Task
from src.core.async_task_queue import AsyncTaskQueue
from src.core.exceptions.task_queue_errors import (
    QueueClosedError,
    QueueShutdownError,
)


@pytest.fixture
def task():
    return Task(description="test", priority=1)

@pytest.fixture
def tasks():
    return [
        Task(description=f"task_{i}", priority=1)
        for i in range(3)
    ]

@pytest.fixture
def queue():
    return AsyncTaskQueue()


class TestAsyncTaskQueue:
    @pytest.mark.asyncio
    async def test_put_and_get(self, queue, task):
        await queue.put(task)

        result = await queue.get()

        assert result.id == task.id

    @pytest.mark.asyncio
    async def test_put_closed_queue(self, queue, task):
        queue.close(workers=1)

        with pytest.raises(QueueClosedError):
            await queue.put(task)

    @pytest.mark.asyncio
    async def test_shutdown_raises(self, queue):
        queue.close(workers=1)

        with pytest.raises(QueueShutdownError):
            await queue.get()

    @pytest.mark.asyncio
    async def test_shutdown_multiple_workers(self, queue):
        queue.close(workers=3)

        results = []

        for _ in range(3):
            try:
                await queue.get()
            except QueueShutdownError:
                results.append(True)

        assert len(results) == 3

    @pytest.mark.asyncio
    async def test_async_iter(self, queue, tasks):
        for task in tasks:
            await queue.put(task)

        queue.close(workers=1)

        results = []

        async for task in queue:
            results.append(task)

        assert [t.id for t in results] == [t.id for t in tasks]

    @pytest.mark.asyncio
    async def test_async_iter_empty(self, queue):
        queue.close(workers=1)

        results = []

        async for task in queue:
            results.append(task)

        assert results == []

    @pytest.mark.asyncio
    @pytest.mark.parametrize("data", ["42", 42, None])
    async def test_put_invalid_data(self, queue, data):
        with pytest.raises(TypeError):
            await queue.put(data)

    @pytest.mark.asyncio
    async def test_join(self, queue, tasks):
        for task in tasks:
            await queue.put(task)

        async def worker():
            async for _ in queue:
                pass

        worker_task = asyncio.create_task(worker())

        queue.close(workers=1)

        await queue.join()
        await worker_task

        assert True
