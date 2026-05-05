"""
Модуль с полной иерархией автобусов, базовой коллекцией Fleet (ЛР1-ЛР3)
и расширенным Fleet с методами sort_by, filter_by, apply.
"""

# ------------------- Блок валидации (из lab01) -------------------
def _validate_route_number(route_number):
    if not isinstance(route_number, str) or not route_number.strip():
        raise ValueError("Номер маршрута должен быть непустой строкой")
    return True

def _validate_capacity(capacity):
    if not isinstance(capacity, int) or capacity <= 0:
        raise ValueError("Вместимость должна быть положительным целым числом")
    return True

def _validate_speed(speed):
    if not isinstance(speed, (int, float)) or speed <= 0:
        raise ValueError("Средняя скорость должна быть положительным числом")
    return True

def _validate_driver_name(driver_name):
    if driver_name is not None:
        if not isinstance(driver_name, str) or not driver_name.strip():
            raise ValueError("Имя водителя должно быть непустой строкой или None")
    return True

# ------------------- Классы автобусов (ЛР1, ЛР3) -------------------
class Bus:
    """Базовый класс автобуса."""
    vehicle_type = "Автобус"
    total_buses_created = 0

    def __init__(self, route_number, capacity, average_speed, driver_name=None):
        _validate_route_number(route_number)
        _validate_capacity(capacity)
        _validate_speed(average_speed)
        _validate_driver_name(driver_name)

        self._route_number = route_number
        self._capacity = capacity
        self._average_speed = average_speed
        self._driver_name = driver_name
        self._current_passengers = 0
        self._is_on_route = False
        Bus.total_buses_created += 1

    @property
    def route_number(self): return self._route_number
    @property
    def capacity(self): return self._capacity
    @property
    def average_speed(self): return self._average_speed
    @property
    def driver_name(self): return self._driver_name
    @property
    def current_passengers(self): return self._current_passengers
    @property
    def is_on_route(self): return self._is_on_route
    @property
    def free_seats(self): return self._capacity - self._current_passengers

    @driver_name.setter
    def driver_name(self, new_name):
        _validate_driver_name(new_name)
        self._driver_name = new_name

    def board_passenger(self):
        if not self._is_on_route:
            raise ValueError("Нельзя садить пассажиров - автобус не на маршруте")
        if self._current_passengers < self._capacity:
            self._current_passengers += 1
            return True
        return False

    def alight_passenger(self):
        if not self._is_on_route:
            raise ValueError("Нельзя высаживать пассажиров - автобус не на маршруте")
        if self._current_passengers > 0:
            self._current_passengers -= 1
            return True
        return False

    def start_route(self):
        if self._driver_name is None:
            raise ValueError("Нельзя отправить автобус без водителя")
        if self._is_on_route:
            raise ValueError("Автобус уже на маршруте")
        self._is_on_route = True
        return True

    def end_route(self):
        self._is_on_route = False
        self._current_passengers = 0
        return True

    def calculate_travel_time(self, distance):
        if not isinstance(distance, (int, float)) or distance <= 0:
            raise ValueError("Расстояние должно быть положительным числом")
        return distance / self._average_speed

    def get_efficiency_rating(self):
        fill_ratio = self._current_passengers / self._capacity if self._capacity > 0 else 0
        if fill_ratio < 0.3: return "Низкая загрузка"
        elif fill_ratio < 0.7: return "Средняя загрузка"
        else: return "Высокая загрузка"

    def display_info(self):
        return (f"Тип: {self.vehicle_type} | Маршрут: {self._route_number} | "
                f"Вместимость: {self._capacity} | Скорость: {self._average_speed} км/ч")

    def calculate_fare(self, distance=1.0):
        raise NotImplementedError("Метод calculate_fare() должен быть реализован в дочернем классе")

    def __str__(self):
        status = "на маршруте" if self._is_on_route else "в парке"
        driver = self._driver_name if self._driver_name else "не назначен"
        return (f"Автобус маршрута {self._route_number} | "
                f"Водитель: {driver} | "
                f"Вместимость: {self._capacity} | "
                f"Пассажиров: {self._current_passengers} | "
                f"Статус: {status}")

    def __repr__(self):
        return (f"Bus(route_number='{self._route_number}', "
                f"capacity={self._capacity}, "
                f"average_speed={self._average_speed}, "
                f"driver_name='{self._driver_name}')")

    def __eq__(self, other):
        if not isinstance(other, Bus): return False
        return (self._route_number == other._route_number and 
                self._capacity == other._capacity)


class CityBus(Bus):
    """Городской автобус."""
    def __init__(self, route_number, capacity, average_speed, driver_name=None,
                 low_floor=True, has_air_conditioning=False):
        super().__init__(route_number, capacity, average_speed, driver_name)
        self.low_floor = low_floor
        self.has_air_conditioning = has_air_conditioning

    def calculate_fare(self, distance=1.0):
        base_fare = 30.0
        if self.has_air_conditioning:
            base_fare += 5.0
        return base_fare

    def display_info(self):
        base_info = super().display_info()
        floor_type = "низкопольный" if self.low_floor else "высокопольный"
        ac = "есть" if self.has_air_conditioning else "нет"
        return f"{base_info} | Тип: городской | Пол: {floor_type} | Кондиционер: {ac}"

    def __str__(self):
        base_str = super().__str__()
        floor = "низкопольный" if self.low_floor else "высокопольный"
        ac = "конд." if self.has_air_conditioning else "без конд."
        return f"[City] {base_str} | {floor} | {ac}"


class IntercityBus(Bus):
    """Междугородний автобус."""
    def __init__(self, route_number, capacity, average_speed, driver_name=None,
                 has_toilet=True, wifi_available=False):
        super().__init__(route_number, capacity, average_speed, driver_name)
        self.has_toilet = has_toilet
        self.wifi_available = wifi_available

    def calculate_fare(self, distance):
        rate_per_km = 2.5
        if self.wifi_available:
            rate_per_km += 0.5
        return rate_per_km * distance

    def display_info(self):
        base_info = super().display_info()
        toilet = "есть" if self.has_toilet else "нет"
        wifi = "есть" if self.wifi_available else "нет"
        return f"{base_info} | Тип: междугородний | Туалет: {toilet} | Wi-Fi: {wifi}"

    def __str__(self):
        base_str = super().__str__()
        toilet = "туалет" if self.has_toilet else "без туалета"
        wifi = "Wi-Fi" if self.wifi_available else "без Wi-Fi"
        return f"[Intercity] {base_str} | {toilet} | {wifi}"


class ElectricBus(Bus):
    """Электробус."""
    def __init__(self, route_number, capacity, average_speed, driver_name=None,
                 battery_capacity=300.0, charging_time=4.0):
        super().__init__(route_number, capacity, average_speed, driver_name)
        self.battery_capacity = battery_capacity
        self.charging_time = charging_time

    def calculate_fare(self, distance=1.0):
        return 25.0

    def calculate_range(self):
        consumption = 1.2
        return self.battery_capacity / consumption

    def display_info(self):
        base_info = super().display_info()
        range_km = self.calculate_range()
        return (f"{base_info} | Тип: электробус | "
                f"Батарея: {self.battery_capacity} кВт·ч | "
                f"Запас хода: ~{range_km:.0f} км")

    def __str__(self):
        base_str = super().__str__()
        return f"[Electric] {base_str} | Батарея: {self.battery_capacity} кВт·ч"


# ------------------- Базовая коллекция (ЛР2, ЛР3) -------------------
class BaseFleet:
    """Исходная коллекция автобусов (без методов sort_by/filter_by/apply)."""
    def __init__(self):
        self._items = []

    def add(self, item):
        if not isinstance(item, Bus):
            raise TypeError(f"Можно добавлять только объекты Bus, получен {type(item).__name__}")
        for existing in self._items:
            if existing == item:
                raise ValueError(f"Автобус маршрута {item.route_number} с вместимостью {item.capacity} уже существует")
        self._items.append(item)
        return True

    def remove(self, item):
        for i, existing in enumerate(self._items):
            if existing == item:
                del self._items[i]
                return True
        raise ValueError("Автобус не найден")

    def remove_at(self, index):
        if index < 0 or index >= len(self._items):
            raise IndexError(f"Индекс {index} вне диапазона")
        return self._items.pop(index)

    def get_all(self):
        return self._items.copy()

    def find_by_route_number(self, route_number):
        return [bus for bus in self._items if bus.route_number == route_number]

    def find_by_driver_name(self, driver_name):
        return [bus for bus in self._items if bus.driver_name and driver_name.lower() in bus.driver_name.lower()]

    def find_by_capacity_range(self, min_cap, max_cap):
        return [bus for bus in self._items if min_cap <= bus.capacity <= max_cap]

    def get_on_route(self):
        new_fleet = BaseFleet()
        for bus in self._items:
            if bus.is_on_route:
                new_fleet.add(bus)
        return new_fleet

    def get_in_depot(self):
        new_fleet = BaseFleet()
        for bus in self._items:
            if not bus.is_on_route:
                new_fleet.add(bus)
        return new_fleet

    def get_by_efficiency(self, rating):
        new_fleet = BaseFleet()
        for bus in self._items:
            if bus.is_on_route and bus.get_efficiency_rating() == rating:
                new_fleet.add(bus)
        return new_fleet

    def get_city_buses(self):
        return [bus for bus in self._items if isinstance(bus, CityBus)]

    def get_intercity_buses(self):
        return [bus for bus in self._items if isinstance(bus, IntercityBus)]

    def get_electric_buses(self):
        return [bus for bus in self._items if isinstance(bus, ElectricBus)]

    def process_all(self):
        for bus in self._items:
            print(bus.display_info())

    def sort_by_route_number(self, reverse=False):
        self._items.sort(key=lambda bus: bus.route_number, reverse=reverse)

    def sort_by_capacity(self, reverse=False):
        self._items.sort(key=lambda bus: bus.capacity, reverse=reverse)

    def sort_by_speed(self, reverse=False):
        self._items.sort(key=lambda bus: bus.average_speed, reverse=reverse)

    def sort(self, key=None, reverse=False):
        if key is None:
            self._items.sort(reverse=reverse)
        else:
            self._items.sort(key=key, reverse=reverse)

    def __len__(self): return len(self._items)
    def __iter__(self): return iter(self._items)
    def __getitem__(self, index):
        if isinstance(index, slice):
            return self._items[index]
        if index < 0: index = len(self._items) + index
        if index < 0 or index >= len(self._items):
            raise IndexError(f"Индекс {index} вне диапазона")
        return self._items[index]
    def __contains__(self, item):
        for existing in self._items:
            if existing == item: return True
        return False
    def __str__(self):
        if not self._items: return "Автопарк: пуст"
        result = f"Автопарк (всего автобусов: {len(self._items)})\n" + "-" * 50 + "\n"
        for i, bus in enumerate(self._items):
            result += f"{i+1}. {bus}\n"
        return result


# ------------------- Расширенный Fleet (ЛР5) -------------------
class Fleet(BaseFleet):
    """Расширенная коллекция с методами sort_by, filter_by, apply (паттерн Стратегия)."""
    def sort_by(self, key_func):
        self._items.sort(key=key_func)
        return self

    def filter_by(self, predicate):
        new_fleet = Fleet()
        for bus in self._items:
            if predicate(bus):
                new_fleet._items.append(bus)
        return new_fleet

    def apply(self, func):
        for bus in self._items:
            func(bus)
        return self