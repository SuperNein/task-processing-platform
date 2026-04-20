from src.core.enums import TaskStatus


API_STUB_TASKS = 15

VALID_STATUS_CHANGES = {
    TaskStatus.new: [
        TaskStatus.new,
        TaskStatus.in_progress,
        TaskStatus.done,
        TaskStatus.cancelled,
    ],
    TaskStatus.in_progress: [
        TaskStatus.in_progress,
        TaskStatus.done,
        TaskStatus.cancelled,
    ],
    TaskStatus.done: [
        TaskStatus.done,
    ],
    TaskStatus.cancelled: [
        TaskStatus.cancelled,
        TaskStatus.new,
    ],
}
