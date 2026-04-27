from abc import ABC, abstractmethod

class Printable(ABC):
    """Интерфейс для объектов, которые могут предоставить строковое представление."""
    @abstractmethod
    def to_string(self) -> str:
        """Возвращает строковое представление объекта."""
        ...

class Comparable(ABC):
    """Интерфейс для объектов, которые можно сравнивать друг с другом."""
    @abstractmethod
    def compare_to(self, other: 'Comparable') -> int:
        """
        Сравнивает текущий объект с другим.
        Возвращает отрицательное число, если self < other,
        0, если равны, положительное, если self > other.
        """
        ...