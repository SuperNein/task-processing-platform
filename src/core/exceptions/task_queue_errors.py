class TaskQueueError(Exception):
    """Base task queue exception"""


class QueueClosedError(TaskQueueError):
    """Cannot put task into a closed queue"""
    def __init__(self, *args):
        if args:
            super().__init__(*args)
        else:
            super().__init__("Cannot put task into a closed queue")


class QueueShutdownError(TaskQueueError):
    """Raise when Task Queue is closed and empty"""
    def __init__(self, *args):
        if args:
            super().__init__(*args)
        else:
            super().__init__("Task Queue is closed and empty")
