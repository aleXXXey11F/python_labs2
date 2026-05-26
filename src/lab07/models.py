# lab07/models.py
"""Модели предметной области: автобусы (Bus, CityBus, IntercityBus, ElectricBus)."""

from datetime import datetime
from typing import Any, Dict, Optional

class ValidationError(ValueError):
    """Ошибка валидации данных."""
    pass

# ------------------------------------------------------------------ валидация
def _validate_route_number(route: str) -> bool:
    if not isinstance(route, str) or not route.strip():
        raise ValidationError("Номер маршрута должен быть непустой строкой")
    return True

def _validate_capacity(cap: int) -> bool:
    if not isinstance(cap, int) or cap <= 0 or cap > 100:
        raise ValidationError("Вместимость должна быть целым положительным числом ≤ 100")
    return True

def _validate_speed(speed: float) -> bool:
    if not isinstance(speed, (int, float)) or speed < 10 or speed > 120:
        raise ValidationError("Средняя скорость должна быть от 10 до 120 км/ч")
    return True

def _validate_driver_name(name: Optional[str]) -> bool:
    if name is not None:
        if not isinstance(name, str) or not name.strip():
            raise ValidationError("Имя водителя должно быть непустой строкой или None")
    return True


class Bus:
    """Базовый класс автобуса."""
    vehicle_type: str = "Автобус"
    total_buses_created: int = 0

    def __init__(self, route_number: str, capacity: int, average_speed: float,
                 driver_name: Optional[str] = None,
                 created_at: Optional[datetime] = None) -> None:
        _validate_route_number(route_number)
        _validate_capacity(capacity)
        _validate_speed(average_speed)
        _validate_driver_name(driver_name)

        self._route_number: str = route_number
        self._capacity: int = capacity
        self._average_speed: float = average_speed
        self._driver_name: Optional[str] = driver_name
        self._current_passengers: int = 0
        self._is_on_route: bool = False
        self.created_at: datetime = created_at or datetime.now()
        Bus.total_buses_created += 1

    # ---------------------------------------------------------------- свойства
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
        _validate_driver_name(name)
        self._driver_name = name

    # --------------------------------------------------------- бизнес-методы
    def board_passenger(self) -> bool:
        if not self._is_on_route:
            raise ValueError("Нельзя садить пассажиров – автобус не на маршруте")
        if self._current_passengers < self._capacity:
            self._current_passengers += 1
            return True
        return False

    def alight_passenger(self) -> bool:
        if not self._is_on_route:
            raise ValueError("Нельзя высаживать пассажиров – автобус не на маршруте")
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

    def get_efficiency_rating(self) -> str:
        if self._capacity == 0:
            return "Нет данных"
        ratio = self._current_passengers / self._capacity
        if ratio < 0.3:
            return "Низкая загрузка"
        elif ratio < 0.7:
            return "Средняя загрузка"
        else:
            return "Высокая загрузка"

    def display_info(self) -> str:
        return (f"Тип: {self.vehicle_type} | Маршрут: {self._route_number} | "
                f"Вместимость: {self._capacity} | Скорость: {self._average_speed} км/ч")

    def calculate_fare(self, distance: float = 1.0) -> float:
        raise NotImplementedError("Метод calculate_fare() должен быть реализован в подклассе")

    # ------------------------------------------------- сериализация
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.__class__.__name__,
            "route_number": self._route_number,
            "capacity": self._capacity,
            "average_speed": self._average_speed,
            "driver_name": self._driver_name,
            "current_passengers": self._current_passengers,
            "is_on_route": self._is_on_route,
            "created_at": self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Bus':
        if data["type"] == "CityBus":
            return CityBus(
                data["route_number"], data["capacity"], data["average_speed"],
                data.get("driver_name"),
                low_floor=data.get("low_floor", True),
                has_air_conditioning=data.get("has_air_conditioning", False),
                created_at=datetime.fromisoformat(data["created_at"])
            )
        elif data["type"] == "IntercityBus":
            return IntercityBus(
                data["route_number"], data["capacity"], data["average_speed"],
                data.get("driver_name"),
                has_toilet=data.get("has_toilet", True),
                wifi_available=data.get("wifi_available", False),
                created_at=datetime.fromisoformat(data["created_at"])
            )
        elif data["type"] == "ElectricBus":
            return ElectricBus(
                data["route_number"], data["capacity"], data["average_speed"],
                data.get("driver_name"),
                battery_capacity=data.get("battery_capacity", 300.0),
                charging_time=data.get("charging_time", 4.0),
                created_at=datetime.fromisoformat(data["created_at"])
            )
        else:
            raise ValueError(f"Неизвестный тип автобуса: {data['type']}")

    # --------------------------------------------------- магические методы
    def __str__(self) -> str:
        status = "на маршруте" if self._is_on_route else "в парке"
        driver = self._driver_name or "не назначен"
        return (f"Автобус маршрута {self._route_number} | "
                f"Водитель: {driver} | "
                f"Вместимость: {self._capacity} | "
                f"Пассажиров: {self._current_passengers} | "
                f"Статус: {status} | "
                f"Добавлен: {self.created_at.strftime('%Y-%m-%d %H:%M')}")

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}('{self._route_number}', "
                f"{self._capacity}, {self._average_speed}, '{self._driver_name}')")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Bus):
            return False
        return (self._route_number == other._route_number and
                self._capacity == other._capacity)


class CityBus(Bus):
    """Городской автобус."""
    def __init__(self, route_number: str, capacity: int, average_speed: float,
                 driver_name: Optional[str] = None,
                 low_floor: bool = True, has_air_conditioning: bool = False,
                 created_at: Optional[datetime] = None) -> None:
        super().__init__(route_number, capacity, average_speed, driver_name, created_at)
        self.low_floor: bool = low_floor
        self.has_air_conditioning: bool = has_air_conditioning

    def calculate_fare(self, distance: float = 1.0) -> float:
        base_fare = 30.0
        if self.has_air_conditioning:
            base_fare += 5.0
        return base_fare

    def display_info(self) -> str:
        base = super().display_info()
        floor = "низкопольный" if self.low_floor else "высокопольный"
        ac = "есть" if self.has_air_conditioning else "нет"
        return f"{base} | Городской | {floor} | Кондиционер: {ac}"

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d.update({
            "low_floor": self.low_floor,
            "has_air_conditioning": self.has_air_conditioning
        })
        return d

    def __str__(self) -> str:
        base = super().__str__()
        floor = "низкоп." if self.low_floor else "высокоп."
        ac = "конд." if self.has_air_conditioning else "без конд."
        return f"[City] {base} | {floor} | {ac}"


class IntercityBus(Bus):
    """Междугородний автобус."""
    def __init__(self, route_number: str, capacity: int, average_speed: float,
                 driver_name: Optional[str] = None,
                 has_toilet: bool = True, wifi_available: bool = False,
                 created_at: Optional[datetime] = None) -> None:
        super().__init__(route_number, capacity, average_speed, driver_name, created_at)
        self.has_toilet: bool = has_toilet
        self.wifi_available: bool = wifi_available

    def calculate_fare(self, distance: float) -> float:
        rate = 2.5
        if self.wifi_available:
            rate += 0.5
        return rate * distance

    def display_info(self) -> str:
        base = super().display_info()
        toilet = "есть" if self.has_toilet else "нет"
        wifi = "есть" if self.wifi_available else "нет"
        return f"{base} | Междугородний | Туалет: {toilet} | Wi-Fi: {wifi}"

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d.update({
            "has_toilet": self.has_toilet,
            "wifi_available": self.wifi_available
        })
        return d

    def __str__(self) -> str:
        base = super().__str__()
        toilet = "туалет" if self.has_toilet else "без туалета"
        wifi = "Wi-Fi" if self.wifi_available else "без Wi-Fi"
        return f"[Intercity] {base} | {toilet} | {wifi}"


class ElectricBus(Bus):
    """Электробус."""
    def __init__(self, route_number: str, capacity: int, average_speed: float,
                 driver_name: Optional[str] = None,
                 battery_capacity: float = 300.0, charging_time: float = 4.0,
                 created_at: Optional[datetime] = None) -> None:
        super().__init__(route_number, capacity, average_speed, driver_name, created_at)
        self.battery_capacity: float = battery_capacity
        self.charging_time: float = charging_time

    def calculate_fare(self, distance: float = 1.0) -> float:
        return 25.0

    def calculate_range(self) -> float:
        consumption = 1.2  # кВт·ч/км
        return self.battery_capacity / consumption

    def display_info(self) -> str:
        base = super().display_info()
        rng = self.calculate_range()
        return f"{base} | Электробус | Батарея: {self.battery_capacity} кВт·ч | Запас хода: ~{rng:.0f} км"

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d.update({
            "battery_capacity": self.battery_capacity,
            "charging_time": self.charging_time
        })
        return d

    def __str__(self) -> str:
        base = super().__str__()
        return f"[Electric] {base} | Батарея: {self.battery_capacity} кВт·ч"