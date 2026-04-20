import pytest

from src.core.models import Task
from src.core.task_queue import TaskQueue, _TaskQueueFilter
from src.core.enums import TaskPriority, TaskStatus


@pytest.fixture
def sample_tasks_list() -> list[Task]:
    return [
        Task(
            description="description_1",
            priority=1
        ),
        Task(
            description="description_2",
            priority=2
        ),
        Task(
            description="description_3",
            priority=3
        ),
    ]

@pytest.fixture
def empty_queue() -> TaskQueue:
    return TaskQueue()

@pytest.fixture
def queue(sample_tasks_list: list[Task]) -> TaskQueue:
    return TaskQueue(sample_tasks_list)

@pytest.fixture
def queue_filter(queue: TaskQueue) -> _TaskQueueFilter:
    return queue.filter


class TestTaskQueue:
    def test_empty_queue_len(self, empty_queue):
        assert len(empty_queue) == 0

    def test_queue_len(self, queue):
        assert len(queue) == 3

    def test_queue_bool(self, empty_queue, queue):
        assert not empty_queue
        assert queue

    def test_push_queue(self, queue, task):
        queue_len = len(queue)

        queue.push(task)
        assert len(queue) == queue_len + 1

    @pytest.mark.parametrize("data", [
        "42",
        42,
        None
    ])
    def test_push_queue_with_invalid_data(self, queue, data):
        with pytest.raises(TypeError):
            queue.push(data)

    def test_extend_queue(self, queue, sample_tasks_list):
        queue_len = len(queue)
        sample_tasks_len = len(sample_tasks_list)

        queue.extend(sample_tasks_list)
        assert len(queue) == queue_len + sample_tasks_len

    @pytest.mark.parametrize("data", [
        "42",
        42,
        None
    ])
    def test_extend_queue_with_invalid_data(self, queue, data):
        with pytest.raises(TypeError):
            queue.extend(data)

    def test_peek_queue(self, queue, sample_tasks_list):
        first_task = sample_tasks_list[0]
        assert queue.peek() == first_task

    def test_peek_empty_queue(self, empty_queue):
        with pytest.raises(IndexError):
            empty_queue.peek()

    def test_pop_queue(self, queue, sample_tasks_list):
        queue_len = len(queue)
        first_task = sample_tasks_list[0]

        assert queue.pop().id == first_task.id
        assert len(queue) == queue_len - 1

    def test_pop_empty_queue(self, empty_queue):
        with pytest.raises(IndexError):
            empty_queue.pop()

    def test_copy_queue(self, queue, sample_tasks_list):
        new_queue = queue.copy()
        new_tasks = [task for task in new_queue]

        assert sample_tasks_list == new_tasks

    def test_queue_repr(self, queue, sample_tasks_list):
        assert repr(queue) == f"TaskQueue(tasks={sample_tasks_list!r})"

    def test_add_queue(self, queue, sample_tasks_list):
        new_queue = queue + sample_tasks_list
        assert len(new_queue) == len(queue) + len(sample_tasks_list)

    def test_iadd_queue(self, queue, sample_tasks_list):
        queue_len = len(queue)
        queue += sample_tasks_list
        assert len(queue) == queue_len + len(sample_tasks_list)

    def test_set_queue_filter(self, empty_queue):
        with pytest.raises(AttributeError):
            empty_queue.filter = None


class TestTaskQueueFilter:
    @pytest.mark.parametrize(
        "status",
        [s for s in TaskStatus]
    )
    def test_filter_by_status(self, queue_filter, sample_tasks_list, status):
        filtered_queue = [
            task for task in queue_filter.status(status)
        ]
        filtered_tasks = [
            task for task in sample_tasks_list if task.status == status
        ]

        assert filtered_tasks == filtered_queue

    @pytest.mark.parametrize(
        "priority",
        [s for s in TaskPriority]
    )
    def test_filter_by_priority(self, queue_filter, sample_tasks_list, priority):
        filtered_queue = [
            task for task in queue_filter.priority(priority)
        ]
        filtered_tasks = [
            task for task in sample_tasks_list if task.priority == priority
        ]

        assert filtered_tasks == filtered_queue

    @pytest.mark.parametrize("predicate", [
        lambda task: task.description == "description_1",
        lambda task: task.priority <= 1,
    ])
    def test_filter_by_predicate(self, queue_filter, sample_tasks_list, predicate):
        filtered_queue = [
            task for task in queue_filter(predicate)
        ]
        filtered_tasks = [
            task for task in sample_tasks_list if predicate(task)
        ]

        assert filtered_tasks == filtered_queue

    @pytest.mark.parametrize("predicate", [
        "42",
        42,
        None
    ])
    def test_filter_by_no_callable_predicate(self, queue_filter, predicate):
        with pytest.raises(TypeError):
            list(queue_filter(predicate))
