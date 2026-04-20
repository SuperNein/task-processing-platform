import time

from src.core.enums import TaskStatus
from src.core.task_queue import TaskQueue
from src.protocols.source import TaskSource
from src.services.loader import TasksLoader


def process_tasks(source: TaskSource) -> TaskQueue:
    """
    Processing tasks from source simulation.
    :return:    list of closed tasks
    """
    print(f"Start tasks from {source.__class__.__name__} processing...")
    loader = TasksLoader(source)
    tasks = TaskQueue(loader.load())

    for task in tasks:
        task.status = TaskStatus.in_progress

        time.sleep(0.5)

        task.status = TaskStatus.done

        print(f"Processed {task}")

    closed_tasks = [task for task in tasks.filter.status(TaskStatus.done)]
    print(f"Processed {len(closed_tasks)} tasks\n")

    return tasks
