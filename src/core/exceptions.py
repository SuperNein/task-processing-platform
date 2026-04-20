from src.core.enums import TaskPriority, TaskStatus


class TaskError(Exception):
    """Base exception for Task models"""
    pass


class InvalidPriorityError(TaskError):
    """Raised when an invalid priority is given"""
    PRIORITIES = {p for p in TaskPriority}

    def __init__(self, *args, value=None):
        if args:
            super().__init__(*args)

        elif value is not None:
            message = f"Priority must be one of {self.PRIORITIES}, got {value!r}"
            super().__init__(message)

        else:
            super().__init__("Invalid task priority value")


class InvalidStatusError(TaskError):
    """Raised when an invalid status is given"""
    STATUSES = {s for s in TaskStatus}

    def __init__(self, *args, value=None):
        if args:
            super().__init__(*args)

        elif value is not None:
            message = f"Status must be one of {self.STATUSES}, got {value!r}"
            super().__init__(message)

        else:
            super().__init__("Invalid task status value")


class InvalidStatusChangeError(TaskError):
    """Raised when status change is invalid"""
    def __init__(self, *args):
        if args:
            super().__init__(*args)
        else:
            super().__init__("Invalid task status change")
