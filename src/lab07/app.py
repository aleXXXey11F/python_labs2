# lab07/app.py
"""Бизнес-логика приложения: управление коллекцией автобусов."""

from datetime import datetime
from typing import Any, Callable, Dict, List, Optional
from models import Bus, CityBus, IntercityBus, ElectricBus, ValidationError
from exceptions import DuplicateItemError, ItemNotFoundError
from storage import load, save


class App:
    """Основной класс приложения, управляющий коллекцией автобусов."""

    def __init__(self, storage_path: str = "data.json") -> None:
        """Инициализация приложения с загрузкой данных из файла.
        
        Args:
            storage_path: путь к JSON-файлу с данными.
        """
        self._buses: List[Bus] = []
        self._storage_path: str = storage_path
        self.load_data()

    # ------------------------------------------------------ загрузка / сохранение
    def load_data(self) -> None:
        """Загрузить автобусы из JSON-файла."""
        data = load(self._storage_path)
        self._buses = [Bus.from_dict(item) for item in data]

    def save_data(self) -> None:
        """Сохранить текущие автобусы в JSON-файл."""
        save([bus.to_dict() for bus in self._buses], self._storage_path)

    def shutdown(self) -> None:
        """Корректное завершение работы с сохранением данных."""
        self.save_data()

    # ------------------------------------------------------ операции с коллекцией
    def add_bus(self, bus_type: str, route: str, capacity: int, speed: float,
                driver: Optional[str] = None, **kwargs: Any) -> Bus:
        """Добавить новый автобус в коллекцию.
        
        Args:
            bus_type: тип автобуса ('CityBus', 'IntercityBus', 'ElectricBus').
            route: номер маршрута.
            capacity: вместимость.
            speed: средняя скорость.
            driver: имя водителя (может быть None).
            **kwargs: дополнительные параметры, зависящие от типа.
        
        Returns:
            Созданный объект автобуса.
        
        Raises:
            DuplicateItemError: если автобус с такими маршрутом и вместимостью уже есть.
            ValidationError: при некорректных параметрах.
        """
        if bus_type == "CityBus":
            bus: Bus = CityBus(route, capacity, speed, driver,
                               low_floor=kwargs.get("low_floor", True),
                               has_air_conditioning=kwargs.get("has_air_conditioning", False))
        elif bus_type == "IntercityBus":
            bus = IntercityBus(route, capacity, speed, driver,
                               has_toilet=kwargs.get("has_toilet", True),
                               wifi_available=kwargs.get("wifi_available", False))
        elif bus_type == "ElectricBus":
            bus = ElectricBus(route, capacity, speed, driver,
                              battery_capacity=kwargs.get("battery_capacity", 300.0),
                              charging_time=kwargs.get("charging_time", 4.0))
        else:
            raise ValueError(f"Неизвестный тип автобуса: {bus_type}")

        # проверка дубликата (по __eq__)
        for existing in self._buses:
            if existing == bus:
                raise DuplicateItemError(
                    f"Автобус маршрута {route} вместимостью {capacity} уже существует"
                )
        self._buses.append(bus)
        return bus

    def get_all_buses(self) -> List[Bus]:
        """Получить список всех автобусов."""
        return self._buses.copy()

    def find_bus_by_route(self, route: str) -> Optional[Bus]:
        """Найти первый автобус с заданным номером маршрута.
        
        Args:
            route: номер маршрута.
        
        Returns:
            Найденный автобус или None.
        """
        for bus in self._buses:
            if bus.route_number == route:
                return bus
        return None

    def remove_bus_by_route(self, route: str) -> Bus:
        """Удалить первый автобус с заданным номером маршрута.
        
        Args:
            route: номер маршрута.
        
        Returns:
            Удалённый автобус.
        
        Raises:
            ItemNotFoundError: если автобус не найден.
        """
        for i, bus in enumerate(self._buses):
            if bus.route_number == route:
                return self._buses.pop(i)
        raise ItemNotFoundError(f"Автобус маршрута {route} не найден")

    def filter_buses(self, predicate: Callable[[Bus], bool]) -> List[Bus]:
        """Отфильтровать автобусы по предикату.
        
        Args:
            predicate: функция, принимающая Bus и возвращающая bool.
        
        Returns:
            Список автобусов, удовлетворяющих условию.
        """
        return [bus for bus in self._buses if predicate(bus)]

    def sort_buses(self, key_func: Callable[[Bus], Any], reverse: bool = False) -> None:
        """Отсортировать коллекцию на месте по заданному ключу.
        
        Args:
            key_func: функция ключа сортировки.
            reverse: если True – по убыванию.
        """
        self._buses.sort(key=key_func, reverse=reverse)

    # ------------------------------------------------------ полезные предикаты / ключи
    @staticmethod
    def key_by_route(bus: Bus) -> str:
        return bus.route_number

    @staticmethod
    def key_by_capacity(bus: Bus) -> int:
        return bus.capacity

    @staticmethod
    def key_by_speed(bus: Bus) -> float:
        return bus.average_speed

    @staticmethod
    def key_by_created(bus: Bus) -> datetime:
        return bus.created_at