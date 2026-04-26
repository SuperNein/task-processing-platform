import pytest

from src.core.task_model import Task
from src.core.enums import TaskStatus

class TestTask:
    @pytest.mark.parametrize(
        "status, is_closed",
        [
            (TaskStatus.new, False),
            (TaskStatus.in_progress, False),
            (TaskStatus.done, True),
            (TaskStatus.cancelled, True)
        ]
    )
    def test_generator_source(self, task, status, is_closed):
        task.status = status
        assert task.is_closed == is_closed


    def test_repr_task(self, task):
        assert repr(task) == (
                f"Task("
                f"description='{task.description}', "
                f"priority={task.priority})"
            )

    def test_tasks_eq(self, task):
        task_id = task.id

        other = Task("new_description")
        other._id = task_id

        assert task == other
        assert not (task != other)

    @pytest.mark.parametrize("other", [
        "42",
        42,
        None
    ])
    def test_radd_type_error(self, task, other):
        assert task != other
        assert not (task == other)


class TestTasksAdd:
    def test_zero_radd(self, task):
        assert 0 + task == task

    def test_tasks_add(self):
        description_1 = "description_1"
        description_2 = "description_2"

        priority_1 = 3
        priority_2 = 4

        task_1 = Task(
            description=description_1,
            priority=priority_1,
        )
        task_2 = Task(
            description=description_2,
            priority=priority_2,
        )

        description = description_1 + "\n" + description_2
        priority = max(priority_1, priority_2)

        task = (task_1 + task_2)

        assert task.description == description
        assert task.priority == priority


    @pytest.mark.parametrize("other", [
        "42",
        42,
        None
    ])
    def test_radd_type_error(self, task, other):
        with pytest.raises(TypeError):
            other + task


    @pytest.mark.parametrize("other", [
        "42",
        42,
        None
    ])
    def test_add_type_error(self, task, other):
        with pytest.raises(TypeError):
            task + other
