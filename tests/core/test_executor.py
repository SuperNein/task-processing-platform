import pytest

from src.core.task_model import Task
from src.core.executor import AsyncTaskExecutor
from src.core.exceptions.executor_errors import (
    ExecutorNotStartedError,
)


class SampleHandler:
    async def handle(self, task: Task) -> None:
        pass


class RuntimeFailingHandler:
    async def handle(self, task: Task) -> None:
        raise RuntimeError("fail")


@pytest.fixture
def handler():
    return SampleHandler()

@pytest.fixture
def failing_handler():
    return RuntimeFailingHandler()


class TestAsyncTaskExecutor:
    @pytest.mark.asyncio
    async def test_submit_without_start(self, task):
        executor = AsyncTaskExecutor()

        with pytest.raises(ExecutorNotStartedError):
            await executor.submit(task)

    @pytest.mark.asyncio
    async def test_register_handler(self, handler):
        executor = AsyncTaskExecutor()

        executor.register_handler(handler)

        assert executor._handler is handler

    @pytest.mark.asyncio
    async def test_execute_tasks(self, handler, tasks):
        async with AsyncTaskExecutor(workers=2) as executor:
            executor.register_handler(handler)

            for task in tasks:
                await executor.submit(task)

            await executor.wait_all()

        assert executor.errors == []

    @pytest.mark.asyncio
    async def test_handler_not_registered(self, tasks):
        async with AsyncTaskExecutor(workers=1) as executor:
            for task in tasks:
                await executor.submit(task)

            await executor.wait_all()

        assert len(executor.errors) == len(tasks)

    @pytest.mark.asyncio
    async def test_failing_handler(self, failing_handler, tasks):
        async with AsyncTaskExecutor(workers=2) as executor:
            executor.register_handler(failing_handler)

            for task in tasks:
                await executor.submit(task)

            await executor.wait_all()

        assert len(executor.errors) == len(tasks)

    @pytest.mark.asyncio
    async def test_wait_all_completes(self, handler, tasks):
        async with AsyncTaskExecutor(workers=1) as executor:
            executor.register_handler(handler)

            for task in tasks:
                await executor.submit(task)

            await executor.wait_all()

        assert True

    @pytest.mark.asyncio
    async def test_multiple_workers(self, handler, tasks):
        async with AsyncTaskExecutor(workers=3) as executor:
            executor.register_handler(handler)

            for task in tasks:
                await executor.submit(task)

            await executor.wait_all()

        assert executor.errors == []

    @pytest.mark.asyncio
    async def test_context_manager_start_stop(self, handler):
        executor = AsyncTaskExecutor(workers=1)

        async with executor:
            executor.register_handler(handler)
            assert executor._running

        assert not executor._running
