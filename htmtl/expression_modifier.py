from abc import abstractmethod, ABC


class ExpressionModifier(ABC):
    @abstractmethod
    def modify(self, expression):
        pass