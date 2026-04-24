from src.core.task_model import Task


class ExecutorError(Exception):
    """Base executor exception"""


class TaskProcessingError(ExecutorError):
    """Processing a specific task error"""
    def __init__(self, task: Task, cause: Exception):
        self.task = task
        self.cause = cause
        super().__init__(f"[{task.id}] {cause}")


class ExecutorNotStartedError(ExecutorError):
    """Using executor before starting"""
    def __init__(self, *args):
        if args:
            super().__init__(*args)
        else:
            super().__init__("Cannot use executor before starting")


class HandlerNotRegisteredError(ExecutorError):
    """Handler not registered"""
    def __init__(self, *args):
        if args:
            super().__init__(*args)
        else:
            super().__init__("Handler not registered")
