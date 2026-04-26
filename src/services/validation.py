import logging

from typing import Type, Any, Protocol


logger = logging.getLogger(__name__)


class ProtocolValidator:
    """Validate objects as protocol"""
    def __init__(self, protocol: Type[Protocol]):
        self._protocol = protocol

    def is_valid(self, obj: Any) -> bool:
        return isinstance(obj, self._protocol)

    def validate(self, obj: Any) -> None:
        if not self.is_valid(obj):
            logger.error(f"Validation failed: {obj} not {self._protocol.__name__}")
            raise TypeError(
                f"'{type(obj).__name__}' is missing "
                f"following '{self._protocol.__name__}' protocol member."
            )
