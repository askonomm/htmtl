from abc import abstractmethod, ABC
from typing import Any


class Modifier(ABC):
    @abstractmethod
    def modify(self, value: Any, opts: list[Any]) -> Any:
        pass
