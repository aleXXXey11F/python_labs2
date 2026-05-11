# container.py
"""
Модуль lab06: Generic-коллекция TypedCollection, протоколы, аннотированные классы автобусов.
Содержит все необходимые классы и функции без внешних зависимостей.
"""

from typing import (
    TypeVar, Generic, Callable, Optional, List, Protocol,
    Iterable, Union, get_args, get_origin
)


# ============================================================================
# Вспомогательная валидация (скопирована из lab01)
# ============================================================================

def validate_route_number(route: str) -> bool:
    if not isinstance(route, str) or not route.strip():
        raise ValueError("Номер маршрута должен быть непустой строкой")
    return True


def validate_capacity(cap: int) -> bool:
    if not isinstance(cap, int) or cap <= 0 or cap > 100:
        raise ValueError("Вместимость должна быть целым положительным числом ≤ 100")
    return True


def validate_speed(speed: float) -> bool:
    if not isinstance(speed, (int, float)) or speed < 10 or speed > 120:
        raise ValueError("Скорость должна быть от 10 до 120 км/ч")
    return True


def validate_driver_name(name: Optional[str]) -> bool:
    if name is not None:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Имя водителя должно быть непустой строкой или None")
    return True


# ============================================================================
# Классы автобусов (аннотированная версия lab03 + методы для протоколов)
# ============================================================================

class Bus:
    """Базовый класс автобуса."""
    vehicle_type: str = "Автобус"
    total_buses_created: int = 0

    def __init__(self, route_number: str, capacity: int, average_speed: float,
                 driver_name: Optional[str] = None) -> None:
        validate_route_number(route_number)
        validate_capacity(capacity)
        validate_speed(average_speed)
        validate_driver_name(driver_name)

        self._route_number: str = route_number
        self._capacity: int = capacity
        self._average_speed: float = average_speed
        self._driver_name: Optional[str] = driver_name
        self._current_passengers: int = 0
        self._is_on_route: bool = False
        Bus.total_buses_created += 1

    @property
    def route_number(self) -> str:
        return self._route_number

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def average_speed(self) -> float:
        return self._average_speed

    @property
    def driver_name(self) -> Optional[str]:
        return self._driver_name

    @property
    def current_passengers(self) -> int:
        return self._current_passengers

    @property
    def is_on_route(self) -> bool:
        return self._is_on_route

    @property
    def free_seats(self) -> int:
        return self._capacity - self._current_passengers

    @driver_name.setter
    def driver_name(self, name: str) -> None:
        validate_driver_name(name)
        self._driver_name = name

    # Методы для протоколов (добавлены в ЛР-6)
    def display(self) -> str:
        """Возвращает строку с информацией об автобусе (для протокола Displayable)."""
        return self.display_info()

    def score(self) -> float:
        """Возвращает коэффициент заполненности (для протокола Scorable)."""
        return self._current_passengers / self._capacity if self._capacity > 0 else 0.0

    # --------------- бизнес-методы ---------------
    def board_passenger(self) -> bool:
        if not self._is_on_route:
            raise ValueError("Нельзя садить пассажиров - автобус не на маршруте")
        if self._current_passengers < self._capacity:
            self._current_passengers += 1
            return True
        return False

    def alight_passenger(self) -> bool:
        if not self._is_on_route:
            raise ValueError("Нельзя высаживать пассажиров - автобус не на маршруте")
        if self._current_passengers > 0:
            self._current_passengers -= 1
            return True
        return False

    def start_route(self) -> bool:
        if self._driver_name is None:
            raise ValueError("Нельзя отправить автобус без водителя")
        if self._is_on_route:
            raise ValueError("Автобус уже на маршруте")
        self._is_on_route = True
        return True

    def end_route(self) -> bool:
        self._is_on_route = False
        self._current_passengers = 0
        return True

    def calculate_travel_time(self, distance: float) -> float:
        if not isinstance(distance, (int, float)) or distance <= 0:
            raise ValueError("Расстояние должно быть положительным числом")
        return distance / self._average_speed

    def get_efficiency_rating(self) -> str:
        if self._capacity == 0:
            return "Нет данных"
        fill_ratio = self._current_passengers / self._capacity
        if fill_ratio < 0.3:
            return "Низкая загрузка"
        elif fill_ratio < 0.7:
            return "Средняя загрузка"
        else:
            return "Высокая загрузка"

    def display_info(self) -> str:
        return (f"Тип: {self.vehicle_type} | Маршрут: {self._route_number} | "
                f"Вместимость: {self._capacity} | Скорость: {self._average_speed} км/ч")

    def calculate_fare(self, distance: float = 1.0) -> float:
        raise NotImplementedError("Метод calculate_fare() должен быть реализован в дочернем классе")

    def __str__(self) -> str:
        status = "на маршруте" if self._is_on_route else "в парке"
        driver = self._driver_name if self._driver_name else "не назначен"
        return (f"Автобус маршрута {self._route_number} | "
                f"Водитель: {driver} | "
                f"Вместимость: {self._capacity} | "
                f"Пассажиров: {self._current_passengers} | "
                f"Статус: {status}")

    def __repr__(self) -> str:
        return (f"Bus(route_number='{self._route_number}', "
                f"capacity={self._capacity}, "
                f"average_speed={self._average_speed}, "
                f"driver_name='{self._driver_name}')")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Bus):
            return False
        return (self._route_number == other._route_number and
                self._capacity == other._capacity)


class CityBus(Bus):
    """Городской автобус."""
    def __init__(self, route_number: str, capacity: int, average_speed: float,
                 driver_name: Optional[str] = None,
                 low_floor: bool = True, has_air_conditioning: bool = False) -> None:
        super().__init__(route_number, capacity, average_speed, driver_name)
        self.low_floor: bool = low_floor
        self.has_air_conditioning: bool = has_air_conditioning

    def calculate_fare(self, distance: float = 1.0) -> float:
        base_fare = 30.0
        if self.has_air_conditioning:
            base_fare += 5.0
        return base_fare

    def display_info(self) -> str:
        base_info = super().display_info()
        floor_type = "низкопольный" if self.low_floor else "высокопольный"
        ac = "есть" if self.has_air_conditioning else "нет"
        return f"{base_info} | Тип: городской | Пол: {floor_type} | Кондиционер: {ac}"

    def __str__(self) -> str:
        base_str = super().__str__()
        floor = "низкопольный" if self.low_floor else "высокопольный"
        ac = "конд." if self.has_air_conditioning else "без конд."
        return f"[City] {base_str} | {floor} | {ac}"


class IntercityBus(Bus):
    """Междугородний автобус."""
    def __init__(self, route_number: str, capacity: int, average_speed: float,
                 driver_name: Optional[str] = None,
                 has_toilet: bool = True, wifi_available: bool = False) -> None:
        super().__init__(route_number, capacity, average_speed, driver_name)
        self.has_toilet: bool = has_toilet
        self.wifi_available: bool = wifi_available

    def calculate_fare(self, distance: float) -> float:
        rate_per_km = 2.5
        if self.wifi_available:
            rate_per_km += 0.5
        return rate_per_km * distance

    def display_info(self) -> str:
        base_info = super().display_info()
        toilet = "есть" if self.has_toilet else "нет"
        wifi = "есть" if self.wifi_available else "нет"
        return f"{base_info} | Тип: междугородний | Туалет: {toilet} | Wi-Fi: {wifi}"

    def __str__(self) -> str:
        base_str = super().__str__()
        toilet = "туалет" if self.has_toilet else "без туалета"
        wifi = "Wi-Fi" if self.wifi_available else "без Wi-Fi"
        return f"[Intercity] {base_str} | {toilet} | {wifi}"


class ElectricBus(Bus):
    """Электробус."""
    def __init__(self, route_number: str, capacity: int, average_speed: float,
                 driver_name: Optional[str] = None,
                 battery_capacity: float = 300.0, charging_time: float = 4.0) -> None:
        super().__init__(route_number, capacity, average_speed, driver_name)
        self.battery_capacity: float = battery_capacity
        self.charging_time: float = charging_time

    def calculate_fare(self, distance: float = 1.0) -> float:
        return 25.0

    def calculate_range(self) -> float:
        consumption = 1.2  # кВт·ч на км
        return self.battery_capacity / consumption

    def display_info(self) -> str:
        base_info = super().display_info()
        range_km = self.calculate_range()
        return (f"{base_info} | Тип: электробус | "
                f"Батарея: {self.battery_capacity} кВт·ч | "
                f"Запас хода: ~{range_km:.0f} км")

    def __str__(self) -> str:
        base_str = super().__str__()
        return f"[Electric] {base_str} | Батарея: {self.battery_capacity} кВт·ч"


# ============================================================================
# Протоколы (для задания 5)
# ============================================================================

class Displayable(Protocol):
    def display(self) -> str:
        ...


class Scorable(Protocol):
    def score(self) -> float:
        ...


# ============================================================================
# Типовые переменные
# ============================================================================

T = TypeVar('T')                      # произвольный тип
R = TypeVar('R')                      # для map
D = TypeVar('D', bound=Displayable)   # только объекты с display()
S = TypeVar('S', bound=Scorable)     # только объекты со score()


# ============================================================================
# Обобщённая коллекция TypedCollection (повторяет интерфейс Fleet из ЛР-2)
# ============================================================================

class TypedCollection(Generic[T]):
    """Generic-коллекция, хранящая элементы типа T, с проверкой типа при добавлении."""

    def __init__(self) -> None:
        self._items: List[T] = []

    # ---------- базовые операции ----------
    def add(self, item: T) -> bool:
        """
        Добавить элемент. Выполняет проверку типа во время выполнения
        (если класс был конкретизирован, например TypedCollection[Bus]).
        """
        # Проверка типа во время выполнения через __orig_class__
        if hasattr(self, '__orig_class__'):
            base_args = get_args(self.__orig_class__)
            if base_args:
                expected_type = base_args[0]
                # Проверяем только если expected_type — конкретный класс (не TypeVar)
                if isinstance(expected_type, type):
                    if not isinstance(item, expected_type):
                        raise TypeError(
                            f"Ожидается объект типа {expected_type.__name__}, получен {type(item).__name__}"
                        )
        # Проверка дубликатов по __eq__
        for existing in self._items:
            if existing == item:
                raise ValueError("Элемент уже существует в коллекции")
        self._items.append(item)
        return True

    def remove(self, item: T) -> bool:
        """Удалить элемент по значению. Возвращает True при успехе."""
        for i, existing in enumerate(self._items):
            if existing == item:
                del self._items[i]
                return True
        raise ValueError("Элемент не найден в коллекции")

    def remove_at(self, index: int) -> T:
        """Удалить элемент по индексу. Возвращает удалённый элемент."""
        if index < 0 or index >= len(self._items):
            raise IndexError(f"Индекс {index} вне диапазона (0-{len(self._items)-1})")
        return self._items.pop(index)

    def get_all(self) -> List[T]:
        """Вернуть копию списка всех элементов."""
        return self._items.copy()

    # ---------- поиск (методы из ЛР-2, применимы только если T имеет соответствующие атрибуты) ----------
    def find_by_route_number(self, route_number: str) -> List[T]:
        """Найти все элементы с заданным номером маршрута."""
        return [item for item in self._items if getattr(item, 'route_number', None) == route_number]

    def find_by_driver_name(self, driver_name: str) -> List[T]:
        """Поиск по имени водителя (частичное совпадение)."""
        result = []
        for item in self._items:
            name = getattr(item, 'driver_name', None)
            if name and driver_name.lower() in name.lower():
                result.append(item)
        return result

    def find_by_capacity_range(self, min_cap: int, max_cap: int) -> List[T]:
        """Поиск по диапазону вместимости."""
        result = []
        for item in self._items:
            cap = getattr(item, 'capacity', None)
            if cap is not None and min_cap <= cap <= max_cap:
                result.append(item)
        return result

    # ---------- фильтрация состояния (из ЛР-2) ----------
    def get_on_route(self) -> 'TypedCollection[T]':
        """Вернуть новую коллекцию с элементами, находящимися на маршруте."""
        new_coll: TypedCollection[T] = TypedCollection()
        for item in self._items:
            if getattr(item, 'is_on_route', False):
                new_coll._items.append(item)
        return new_coll

    def get_in_depot(self) -> 'TypedCollection[T]':
        """Вернуть новую коллекцию с элементами в парке."""
        new_coll: TypedCollection[T] = TypedCollection()
        for item in self._items:
            if not getattr(item, 'is_on_route', True):
                new_coll._items.append(item)
        return new_coll

    def get_by_efficiency(self, rating: str) -> 'TypedCollection[T]':
        """Вернуть новую коллекцию с элементами заданного рейтинга."""
        new_coll: TypedCollection[T] = TypedCollection()
        for item in self._items:
            if getattr(item, 'get_efficiency_rating', lambda: "")() == rating:
                new_coll._items.append(item)
        return new_coll

    # ---------- сортировка ----------
    def sort_by_route_number(self, reverse: bool = False) -> None:
        self._items.sort(key=lambda x: getattr(x, 'route_number', ''), reverse=reverse)

    def sort_by_capacity(self, reverse: bool = False) -> None:
        self._items.sort(key=lambda x: getattr(x, 'capacity', 0), reverse=reverse)

    def sort_by_speed(self, reverse: bool = False) -> None:
        self._items.sort(key=lambda x: getattr(x, 'average_speed', 0.0), reverse=reverse)

    def sort(self, key: Optional[Callable[[T], Union[str, int, float]]] = None,
             reverse: bool = False) -> None:
        if key is not None:
            self._items.sort(key=key, reverse=reverse)
        else:
            self._items.sort(reverse=reverse)

    # ---------- новые методы (задание 4) ----------
    def find(self, predicate: Callable[[T], bool]) -> Optional[T]:
        """Вернуть первый элемент, удовлетворяющий предикату, или None."""
        for item in self._items:
            if predicate(item):
                return item
        return None

    def filter(self, predicate: Callable[[T], bool]) -> List[T]:
        """Вернуть список всех элементов, удовлетворяющих предикату."""
        return [item for item in self._items if predicate(item)]

    def map(self, transform: Callable[[T], R]) -> List[R]:
        """Применить функцию преобразования ко всем элементам и вернуть список результатов."""
        return [transform(item) for item in self._items]

    # ---------- магические методы ----------
    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterable[T]:
        return iter(self._items)

    def __getitem__(self, index: Union[int, slice]) -> Union[T, List[T]]:
        if isinstance(index, slice):
            return self._items[index]
        if index < 0:
            index = len(self._items) + index
        if index < 0 or index >= len(self._items):
            raise IndexError(f"Индекс {index} вне диапазона")
        return self._items[index]

    def __contains__(self, item: T) -> bool:
        return any(existing == item for existing in self._items)

    def __str__(self) -> str:
        if not self._items:
            return "TypedCollection: пусто"
        items_str = "\n".join(f"  - {item}" for item in self._items)
        return f"TypedCollection[{type(self._items[0]).__name__}...] ({len(self._items)} шт.):\n{items_str}"