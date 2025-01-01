from abc import abstractmethod, ABC
from typing import Any


class Modifier(ABC):
    name: str

    @abstractmethod
    def modify(self, value: Any, opts: list[Any]) -> Any:
        pass


def modifier_name(name: str):
    def wrapper(cls: type[Modifier]):
        cls.name = name

        return cls

    return wrapper