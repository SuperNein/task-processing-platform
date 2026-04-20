from typing import Type, Any

from src.protocols.source import TaskSource


class SourceValidator:
    def __init__(self, protocol: Type[TaskSource] = TaskSource):
        self._protocol = protocol

    def is_valid(self, source: Any) -> bool:
        return isinstance(source, self._protocol)

    def validate(self, source: Any) -> None:
        if not self.is_valid(source):
            raise TypeError(
                f"'{type(source).__name__}' is missing "
                f"following '{self._protocol.__name__}' protocol member."
            )
