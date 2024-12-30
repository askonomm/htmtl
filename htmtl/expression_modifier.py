from abc import abstractmethod, ABC
from typing import Any


class ExpressionModifier(ABC):
    name: str

    @abstractmethod
    def modify(self, value: Any, opts: list[Any]) -> Any:
        pass


def modifier(name: str):
    def wrapper(cls: type[ExpressionModifier]):
        cls.name = name

        return cls

    return wrapper