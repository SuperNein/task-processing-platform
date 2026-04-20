import pytest
import uuid
from datetime import datetime

from src.common.constants import VALID_STATUS_CHANGES
from src.core.models import Task
from src.core.enums import TaskPriority, TaskStatus
from src.core.exceptions.task_errors import (
    InvalidPriorityError,
    InvalidStatusError,
    InvalidStatusChangeError,
)
from src.core.descriptors import (
    BaseDescriptor,
    TaskIdDescriptor,
    CreatedAtDescriptor,
)


class TestBaseDescriptor:
    def test_priority_descriptor_set_name(self):
        descriptor = BaseDescriptor()
        descriptor.__set_name__(Task, "test_attr")

        assert descriptor.public_name == "test_attr"
        assert descriptor.private_name == "_test_attr"

    def test_get_with_none_instance(self):
        descriptor = BaseDescriptor()
        result = descriptor.__get__(None, Task)

        assert result is descriptor


class TestTaskIdDescriptor:
    def test_get_with_none_instance(self):
        descriptor = TaskIdDescriptor()
        result = descriptor.__get__(None, Task)

        assert result is descriptor

    def test_generate_uuid(self, task):
        assert isinstance(task.id, uuid.UUID)
        assert task.id.version == 4

    def test_set_id_attribute_error(self, task):
        with pytest.raises(AttributeError):
            task.id = uuid.uuid4()


class TestDescriptionDescriptor:
    @pytest.mark.parametrize("description", [
        "",
        "abc",
        "42"
    ])
    def test_description_get(self, task, description):
        task._description = description
        assert task.description == description

    @pytest.mark.parametrize("invalid_description", [
        10,
        -1,
        0,
        None,
    ])
    def test_set_with_invalid_values(self, task, invalid_description):
        with pytest.raises(TypeError):
            task.description = invalid_description


class TestCreatedAtDescriptor:
    def test_get_with_none_instance(self):
        descriptor = CreatedAtDescriptor()
        result = descriptor.__get__(None, Task)

        assert result is descriptor

    def test_format_date_type(self, task):
        assert isinstance(task._created_at, datetime)
        assert isinstance(task.created_at, str)

    def test_created_at_with_value(self, task):
        task._created_at = datetime(2000, 1, 1, 00, 00, 00)
        assert task.created_at == "2000-01-01 00:00:00"


class TestPriorityDescriptor:
    @pytest.mark.parametrize(
        "priority",
        [p for p in TaskPriority]
    )
    def test_get_with_enums(self, task, priority):
        task._priority = priority
        assert task.priority == priority.value

    @pytest.mark.parametrize(
        "priority_value",
        [p.value for p in TaskPriority]
    )
    def test_get_with_enum_values(self, task, priority_value):
        task.priority = priority_value
        assert task.priority == priority_value

    @pytest.mark.parametrize("invalid_value", [
        "high",
        "normal",
        10,
        -1,
        0,
        None,
    ])
    def test_get_with_invalid_values(self, task, invalid_value):
        with pytest.raises(InvalidPriorityError):
            task.priority = invalid_value


class TestStatusDescriptor:
    @pytest.mark.parametrize(
        "status",
        [s for s in TaskStatus]
    )
    def test_get_with_enums(self, task, status):
        task._status = status
        assert task.status == status

    @pytest.mark.parametrize(
        "status_value",
        [s.value for s in TaskStatus]
    )
    def test_get_with_str(self, task, status_value):
        task.status = status_value
        assert task.status == status_value

    @pytest.mark.parametrize("invalid_status", [
        "finished",
        "",
        10,
        -1,
        0,
        None,
    ])
    def test_get_with_invalid_values(self, task, invalid_status):
        with pytest.raises(InvalidStatusError):
            task.status = invalid_status

    @pytest.mark.parametrize(
        "status_value",
        [s.value for s in TaskStatus]
    )
    def test_invalid_status_change(self, task, status_value):
        task.status = status_value

        for new_status in [
            s for s in TaskStatus
            if s not in VALID_STATUS_CHANGES[status_value]
        ]:

            with pytest.raises(InvalidStatusChangeError):
                task.status = new_status

    def test_invalid_initial_status_change(self, task):
        delattr(task, '_status')

        with pytest.raises(InvalidStatusChangeError):
            task.status = TaskStatus.done
