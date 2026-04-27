from abc import ABC, abstractmethod

class Printable(ABC):
    """Интерфейс для объектов, которые могут предоставить строковое представление."""
    @abstractmethod
    def to_string(self) -> str:
        ...

class Comparable(ABC):
    """Интерфейс для объектов, которые можно сравнивать друг с другом."""
    @abstractmethod
    def compare_to(self, other: 'Comparable') -> int:
        ...