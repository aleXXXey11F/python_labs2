import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lab03.models import Bus, CityBus, IntercityBus, ElectricBus, Fleet
from interfaces import Printable, Comparable

class PrintableCityBus(CityBus, Printable):
    """Городской автобус, поддерживающий печать через Printable."""
    def to_string(self) -> str:
        return (f"[Printable] Городской автобус №{self.route_number}: "
                f"{self.current_passengers}/{self.capacity} пасс. | "
                f"{'низкопольный' if self.low_floor else 'высокопольный'} | "
                f"кондиционер: {'да' if self.has_air_conditioning else 'нет'}")

class ComparableIntercityBus(IntercityBus, Comparable):
    """Междугородний автобус, умеющий сравниваться по средней скорости."""
    def compare_to(self, other: 'Comparable') -> int:
        if not isinstance(other, ComparableIntercityBus):
            raise TypeError("Сравнивать можно только с ComparableIntercityBus")
        if self.average_speed < other.average_speed:
            return -1
        elif self.average_speed > other.average_speed:
            return 1
        else:
            return 0

class AdvancedElectricBus(ElectricBus, Printable, Comparable):
    """Электробус с поддержкой и печати, и сравнения."""
    def to_string(self) -> str:
        return (f"[Printable] Электробус №{self.route_number}: "
                f"батарея {self.battery_capacity} кВт·ч, "
                f"запас хода ~{self.calculate_range():.0f} км | "
                f"пассажиров: {self.current_passengers}/{self.capacity}")

    def compare_to(self, other: 'Comparable') -> int:
        if not isinstance(other, AdvancedElectricBus):
            raise TypeError("Сравнивать можно только с AdvancedElectricBus")
        if self.battery_capacity < other.battery_capacity:
            return -1
        elif self.battery_capacity > other.battery_capacity:
            return 1
        else:
            return 0

class Ticket(Printable, Comparable):
    """Билет на проезд — новый класс, реализующий оба интерфейса."""
    def __init__(self, ticket_id: str, route_number: str, price: float, status: str = "valid"):
        self.ticket_id = ticket_id
        self.route_number = route_number
        self.price = price
        self.status = status   # "valid", "used", "expired"

    def to_string(self) -> str:
        return (f"[Printable] Билет {self.ticket_id}: "
                f"маршрут {self.route_number}, цена {self.price:.2f} руб., "
                f"статус: {self.status}")

    def compare_to(self, other: 'Comparable') -> int:
        if not isinstance(other, Ticket):
            raise TypeError("Сравнивать можно только с Ticket")
        if self.price < other.price:
            return -1
        elif self.price > other.price:
            return 1
        else:
            return 0

class ExtendedFleet(Fleet):
    """Расширенная коллекция с поддержкой интерфейсов Printable и Comparable."""
    
    def get_printable(self):
        """Возвращает только объекты, реализующие интерфейс Printable."""
        return [item for item in self._items if isinstance(item, Printable)]
    
    def get_comparable(self):
        """Возвращает только объекты, реализующие интерфейс Comparable."""
        return [item for item in self._items if isinstance(item, Comparable)]
    
    def print_all_printable(self):
        """Полиморфный вызов to_string() для всех Printable объектов коллекции."""
        for item in self.get_printable():
            print(item.to_string())
    
    def sort_comparable(self, reverse=False):
        """
        Сортирует Comparable-объекты в коллекции, используя их compare_to.
        Остальные объекты остаются на своих местах (в конце после сортировки Comparable).
        Для демонстрации: сортируем только группу Comparable, остальные добавляем после.
        """
        comparable_items = []
        others = []
        for item in self._items:
            if isinstance(item, Comparable):
                comparable_items.append(item)
            else:
                others.append(item)
        # Сортировка Comparable с помощью compare_to
        # Используем пузырьковую сортировку для наглядности (можно любую)
        n = len(comparable_items)
        for i in range(n):
            for j in range(0, n-i-1):
                if comparable_items[j].compare_to(comparable_items[j+1]) > 0:
                    if reverse:
                        # если reverse, меняем условие? Упростим: сначала по возрастанию,
                        # потом reverse переворачивает список.
                        pass
        # Простая реализация через sorted с ключом, но ключ использует compare_to
        # Создаём функцию, которая возвращает значение, но compare_to возвращает int,
        # для сортировки с ключом нужен абсолютный порядок. Поэтому используем sorted
        # с кастомным компаратором (functools.cmp_to_key).
        from functools import cmp_to_key
        comparable_items.sort(key=cmp_to_key(lambda a, b: a.compare_to(b)), reverse=reverse)
        self._items = comparable_items + others

    # Переопределяем __str__, чтобы использовать to_string для Printable, если доступно
    def __str__(self):
        if len(self._items) == 0:
            return "Автопарк: пуст"
        result = f"Автопарк (всего единиц: {len(self._items)})\n"
        result += "-" * 50 + "\n"
        for i, item in enumerate(self._items):
            if isinstance(item, Printable):
                result += f"{i+1}. {item.to_string()}\n"
            else:
                result += f"{i+1}. {str(item)}\n"
        return result