from enum import Enum, IntEnum

class TaskPriority(IntEnum):
    low = 1
    normal = 2
    high = 3
    critical = 4


class TaskStatus(str, Enum):
    new = "new"
    in_progress = "in_progress"
    done = "done"
    cancelled = "cancelled"
