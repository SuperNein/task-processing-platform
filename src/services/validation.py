from typing import Type, Any, Protocol


class ProtocolValidator:
    """Validate objects as protocol"""
    def __init__(self, protocol: Type[Protocol]):
        self._protocol = protocol

    def is_valid(self, obj: Any) -> bool:
        return isinstance(obj, self._protocol)

    def validate(self, obj: Any) -> None:
        if not self.is_valid(obj):
            raise TypeError(
                f"'{type(obj).__name__}' is missing "
                f"following '{self._protocol.__name__}' protocol member."
            )
