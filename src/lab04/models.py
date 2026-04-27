"""
Все классы, необходимые для ЛР-4, собраны в одном файле для независимости.
"""

from interfaces import Printable, Comparable

# ====================== Базовая валидация (упрощённая) ======================
class ValidationError(ValueError):
    pass

def validate_route_number(route):
    if not isinstance(route, str) or not route.strip():
        raise ValidationError("Некорректный номер маршрута")

def validate_capacity(capacity):
    if not isinstance(capacity, int) or capacity <= 0 or capacity > 100:
        raise ValidationError("Вместимость должна быть целым положительным числом ≤ 100")

def validate_speed(speed):
    if not isinstance(speed, (int, float)) or speed < 10 or speed > 120:
        raise ValidationError("Скорость должна быть от 10 до 120 км/ч")

def validate_driver_name(name):
    if name is not None:
        if not isinstance(name, str) or not name.strip():
            raise ValidationError("Имя водителя не может быть пустым")

# ====================== Базовый класс Bus (из ЛР-1) ========================
class Bus:
    vehicle_type = "Автобус"
    total_buses_created = 0

    def __init__(self, route_number, capacity, average_speed, driver_name=None):
        validate_route_number(route_number)
        validate_capacity(capacity)
        validate_speed(average_speed)
        validate_driver_name(driver_name)

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
    def driver_name(self, name):
        validate_driver_name(name)
        self._driver_name = name

    def board_passenger(self):
        if not self._is_on_route:
            raise ValueError("Автобус не на маршруте")
        if self._current_passengers < self._capacity:
            self._current_passengers += 1
            return True
        return False

    def alight_passenger(self):
        if not self._is_on_route:
            raise ValueError("Автобус не на маршруте")
        if self._current_passengers > 0:
            self._current_passengers -= 1
            return True
        return False

    def start_route(self):
        if self._driver_name is None:
            raise ValueError("Нет водителя")
        if self._is_on_route:
            raise ValueError("Уже на маршруте")
        self._is_on_route = True
        return True

    def end_route(self):
        self._is_on_route = False
        self._current_passengers = 0
        return True

    def get_efficiency_rating(self):
        ratio = self._current_passengers / self._capacity if self._capacity else 0
        if ratio < 0.3: return "Низкая загрузка"
        elif ratio < 0.7: return "Средняя загрузка"
        else: return "Высокая загрузка"

    def display_info(self):
        return (f"Тип: {self.vehicle_type} | Маршрут: {self._route_number} | "
                f"Вместимость: {self._capacity} | Скорость: {self._average_speed} км/ч")

    def calculate_fare(self, distance=1.0):
        raise NotImplementedError("Метод calculate_fare() должен быть реализован в подклассе")

    def __str__(self):
        status = "на маршруте" if self._is_on_route else "в парке"
        driver = self._driver_name or "не назначен"
        return (f"Автобус маршрута {self._route_number} | "
                f"Водитель: {driver} | "
                f"Вместимость: {self._capacity} | "
                f"Пассажиров: {self._current_passengers} | "
                f"Статус: {status}")

    def __repr__(self):
        return f"Bus('{self._route_number}', {self._capacity}, {self._average_speed}, '{self._driver_name}')"

    def __eq__(self, other):
        if not isinstance(other, Bus):
            return False
        return self._route_number == other._route_number and self._capacity == other._capacity

# ====================== Производные классы (из ЛР-3) ========================
class CityBus(Bus):
    def __init__(self, route_number, capacity, average_speed, driver_name=None,
                 low_floor=True, has_air_conditioning=False):
        super().__init__(route_number, capacity, average_speed, driver_name)
        self.low_floor = low_floor
        self.has_air_conditioning = has_air_conditioning

    def calculate_fare(self, distance=1.0):
        fare = 30.0
        if self.has_air_conditioning:
            fare += 5.0
        return fare

    def display_info(self):
        base = super().display_info()
        floor = "низкопольный" if self.low_floor else "высокопольный"
        ac = "есть" if self.has_air_conditioning else "нет"
        return f"{base} | Тип: городской | Пол: {floor} | Кондиционер: {ac}"

    def __str__(self):
        base = super().__str__()
        floor = "низкоп." if self.low_floor else "высокоп."
        ac = "конд." if self.has_air_conditioning else "без конд."
        return f"[City] {base} | {floor} | {ac}"

class IntercityBus(Bus):
    def __init__(self, route_number, capacity, average_speed, driver_name=None,
                 has_toilet=True, wifi_available=False):
        super().__init__(route_number, capacity, average_speed, driver_name)
        self.has_toilet = has_toilet
        self.wifi_available = wifi_available

    def calculate_fare(self, distance):
        rate = 2.5
        if self.wifi_available:
            rate += 0.5
        return rate * distance

    def display_info(self):
        base = super().display_info()
        toilet = "есть" if self.has_toilet else "нет"
        wifi = "есть" if self.wifi_available else "нет"
        return f"{base} | Тип: междугородний | Туалет: {toilet} | Wi-Fi: {wifi}"

    def __str__(self):
        base = super().__str__()
        toilet = "туалет" if self.has_toilet else "без туалета"
        wifi = "Wi-Fi" if self.wifi_available else "без Wi-Fi"
        return f"[Intercity] {base} | {toilet} | {wifi}"

class ElectricBus(Bus):
    def __init__(self, route_number, capacity, average_speed, driver_name=None,
                 battery_capacity=300.0, charging_time=4.0):
        super().__init__(route_number, capacity, average_speed, driver_name)
        self.battery_capacity = battery_capacity
        self.charging_time = charging_time

    def calculate_fare(self, distance=1.0):
        return 25.0

    def calculate_range(self):
        consumption = 1.2  # кВт·ч на км
        return self.battery_capacity / consumption

    def display_info(self):
        base = super().display_info()
        rng = self.calculate_range()
        return f"{base} | Тип: электробус | Батарея: {self.battery_capacity} кВт·ч | Запас хода: ~{rng:.0f} км"

    def __str__(self):
        base = super().__str__()
        return f"[Electric] {base} | Батарея: {self.battery_capacity} кВт·ч"

# ====================== Классы, реализующие интерфейсы ======================
class PrintableCityBus(CityBus, Printable):
    def to_string(self) -> str:
        return (f"[Printable] Городской автобус №{self.route_number}: "
                f"{self.current_passengers}/{self.capacity} пасс. | "
                f"{'низкопольный' if self.low_floor else 'высокопольный'} | "
                f"кондиционер: {'да' if self.has_air_conditioning else 'нет'}")

class ComparableIntercityBus(IntercityBus, Comparable):
    def compare_to(self, other: 'Comparable') -> int:
        if not isinstance(other, ComparableIntercityBus):
            raise TypeError("Сравнивать можно только с ComparableIntercityBus")
        if self.average_speed < other.average_speed:
            return -1
        elif self.average_speed > other.average_speed:
            return 1
        return 0

class AdvancedElectricBus(ElectricBus, Printable, Comparable):
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
        return 0

class Ticket(Printable, Comparable):
    def __init__(self, ticket_id, route_number, price, status="valid"):
        self.ticket_id = ticket_id
        self.route_number = route_number
        self.price = price
        self.status = status

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
        return 0

# ====================== Коллекция Fleet с интерфейсными методами ============
from functools import cmp_to_key

class Fleet:
    def __init__(self):
        self._items = []

    def add(self, item):
        if not isinstance(item, Bus) and not isinstance(item, Ticket):
            raise TypeError("Можно добавлять только объекты Bus или Ticket")
        for existing in self._items:
            if type(existing) == type(item) and existing == item:
                raise ValueError("Элемент уже существует в коллекции")
        self._items.append(item)
        return True

    def remove(self, item):
        for i, existing in enumerate(self._items):
            if type(existing) == type(item) and existing == item:
                del self._items[i]
                return True
        raise ValueError("Элемент не найден")

    def get_all(self):
        return self._items.copy()

    def get_printable(self):
        return [item for item in self._items if isinstance(item, Printable)]

    def get_comparable(self):
        return [item for item in self._items if isinstance(item, Comparable)]

    def print_all_printable(self):
        for item in self.get_printable():
            print(item.to_string())

    def sort_comparable(self, reverse=False):
        comparables = [item for item in self._items if isinstance(item, Comparable)]
        others = [item for item in self._items if not isinstance(item, Comparable)]
        comparables.sort(key=cmp_to_key(lambda a, b: a.compare_to(b)), reverse=reverse)
        self._items = comparables + others

    def __iter__(self):
        return iter(self._items)

    def __len__(self):
        return len(self._items)

    def __getitem__(self, index):
        return self._items[index]

    def __str__(self):
        if not self._items:
            return "Автопарк: пуст"
        lines = [f"Автопарк (всего единиц: {len(self._items)})", "-"*50]
        for i, item in enumerate(self._items, 1):
            if isinstance(item, Printable):
                lines.append(f"{i}. {item.to_string()}")
            else:
                lines.append(f"{i}. {str(item)}")
        return "\n".join(lines)