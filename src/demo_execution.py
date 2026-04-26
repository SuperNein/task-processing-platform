import time

from src.protocols.source import TaskSource
from src.services.loader import TaskSourceLoader
from src.core.executor import AsyncTaskExecutor
from src.handlers.print_handler import PrintHandler
from src.handlers.failing_handler import FailingHandler


async def demo_execution(source: TaskSource) -> None:
    """Demonstrate execution of tasks from source"""
    print(f"=== Start tasks from {source.__class__.__name__} execution ===")
    loader = TaskSourceLoader(source)
    tasks_to_run = [task for task in loader.load()]
    print(f"  > All tasks loaded\n")


    print("\n=== PrintHandler ===")
    start = time.perf_counter()

    async with AsyncTaskExecutor(workers=3) as executor:
        executor.register_handler(PrintHandler())

        for task in tasks_to_run[:]:
            await executor.submit(task)

        await executor.wait_all()

    print(f"\n  Total time: {time.perf_counter() - start:.2f}s\n")


    print("\n=== FailingHandler ===")
    async with AsyncTaskExecutor(workers=2) as executor:
        executor.register_handler(FailingHandler())

        for task in tasks_to_run[:]:
            await executor.submit(task)

        await executor.wait_all()

    if executor.errors:
        print(f"\n  Errors: {len(executor.errors)}")
        for err in executor.errors:
            print(f"  > {err}")

    print("\n=== End of the execution ===\n")
