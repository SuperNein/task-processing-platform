from typing import Optional, Any

from src.common.constants import VALID_STATUS_CHANGES
from src.core.enums import TaskPriority, TaskStatus
from src.core.exceptions import (
    InvalidPriorityError,
    InvalidStatusError,
    InvalidStatusChangeError
)


class BaseDescriptor:
    """Base descriptor class."""
    def __set_name__(self, owner: type, name: str):
        self.public_name = name
        self.private_name = f"_{name}"

    def __get__(self, instance: Optional[object], owner: type) -> Any:
        if instance is None:
            return self
        return getattr(instance, self.private_name)


class TaskIdDescriptor(BaseDescriptor):
    """Read-only descriptor for task id."""
    def __set__(self, instance: object, value: Any):
        raise AttributeError(f"Attribute '{self.public_name}' is read-only")


class DescriptionDescriptor(BaseDescriptor):
    """Validate task description"""
    def __set__(self, instance: object, value: Any):
        if not isinstance(value, str):
            raise TypeError(
                f"Task description must be 'str', got '{type(value)}'"
            )

        setattr(instance, self.private_name, value)


class CreatedAtDescriptor(BaseDescriptor):
    """Format datetime value to 'Y-m-d H:M:S'"""
    def __get__(self, instance: Optional[object], owner: type) -> Any:
        if instance is None:
            return self

        return getattr(instance, self.private_name).strftime("%Y-%m-%d %H:%M:%S")


class PriorityDescriptor(BaseDescriptor):
    """Validate value with enums.TaskPriority"""
    def __set__(self, instance: object, value: Any):
        if isinstance(value, TaskPriority):
            validated_value = value.value

        elif isinstance(value, int) and value in TaskPriority:
            validated_value = value

        else:
            raise InvalidPriorityError(value=value)

        setattr(instance, self.private_name, validated_value)


class StatusDescriptor(BaseDescriptor):
    """Validate value with enums.TaskStatus"""
    def __set__(self, instance: object, value: Any):
        if isinstance(value, TaskStatus):
            validated_value = value.value

        elif isinstance(value, str) and value in TaskStatus:
            validated_value = value

        else:
            raise InvalidStatusError(value=value)

        previous_value = getattr(instance, self.private_name, None)

        if previous_value is None:
            if validated_value != TaskStatus.new:
                raise InvalidStatusChangeError(
                    f"Initial status must be 'new', got '{value!r}'"
                )

        elif validated_value not in VALID_STATUS_CHANGES[previous_value]:
            raise InvalidStatusChangeError(
                f"Status '{previous_value!r}' cannot be changed by '{validated_value!r}'"
            )

        setattr(instance, self.private_name, validated_value)
