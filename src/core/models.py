import uuid
from datetime import datetime

from src.core.enums import TaskPriority, TaskStatus
from src.core.descriptors import (
    TaskIdDescriptor,
    DescriptionDescriptor,
    CreatedAtDescriptor,
    PriorityDescriptor,
    StatusDescriptor,
)


class Task:
    __slots__ = (
        "_id",
        "_description",
        "_priority",
        "_status",
        "_created_at",
    )

    id = TaskIdDescriptor()
    description = DescriptionDescriptor()
    priority = PriorityDescriptor()
    status = StatusDescriptor()
    created_at = CreatedAtDescriptor()

    def __init__(
            self,
            description: str,
            priority: TaskPriority | int = TaskPriority.normal,
    ):
        self._id = uuid.uuid4()
        self._created_at = datetime.now()

        self.description = description
        self.priority = priority
        self.status = TaskStatus.new


    @property
    def is_closed(self) -> bool:
        """True if task is done or cancelled"""
        return self.status in {TaskStatus.done, TaskStatus.cancelled}

    def __str__(self) -> str:
        return (
            f"Task("
            f"id='{self.id}', "
            f"description={self.description!r}, "
            f"priority={self.priority!r})"
        )

    def __repr__(self) -> str:
        return (
            f"Task("
            f"description={self.description!r}, "
            f"priority={self.priority!r})"
        )

    def __radd__(self, other) -> Task:
        if other == 0:
            return self
        raise TypeError(f"Cannot add {type(other)} to Task")

    def __add__(self, other: Task) -> Task:
        if not  isinstance(other, Task):
            raise TypeError(f"Cannot add Task to {type(other)}")

        description = self.description + "\n" + other.description
        priority = max(self.priority, other.priority)

        return Task(
            description=description,
            priority=priority,
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, Task):
            return False

        return self.id == other.id
