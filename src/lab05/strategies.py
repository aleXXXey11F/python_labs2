"""
Модуль стратегий и функций высшего порядка для коллекции транспортных средств.
Использует модели из lab03.
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from lab03.models import CityBus, IntercityBus, ElectricBus


# --- Стратегии сортировки ---
def by_route_number(bus):
    """Сортировка по номеру маршрута."""
    return bus.route_number

def by_capacity(bus):
    """Сортировка по вместимости."""
    return bus.capacity

def by_speed(bus):
    """Сортировка по средней скорости."""
    return bus.average_speed

def by_fill_ratio(bus):
    """Сортировка по доле занятых мест."""
    return bus.current_passengers / bus.capacity if bus.capacity > 0 else 0

def by_driver_name(bus):
    """Сортировка по имени водителя (без учёта регистра)."""
    return (bus.driver_name or "").lower()


# --- Функции-фильтры ---
def is_city_bus(bus):
    return isinstance(bus, CityBus)

def is_intercity_bus(bus):
    return isinstance(bus, IntercityBus)

def is_electric_bus(bus):
    return isinstance(bus, ElectricBus)

def is_on_route(bus):
    return bus.is_on_route

def has_free_seats(bus):
    return bus.free_seats > 0


# --- Фабрики функций ---
def make_capacity_filter(min_capacity):
    """Создаёт фильтр по минимальной вместимости."""
    def filter_fn(bus):
        return bus.capacity >= min_capacity
    return filter_fn

def make_route_filter(route_number):
    """Создаёт фильтр по точному номеру маршрута."""
    def filter_fn(bus):
        return bus.route_number == route_number
    return filter_fn


# --- Функции для map ---
def bus_to_dict(bus):
    return {
        "type": bus.vehicle_type,
        "route": bus.route_number,
        "capacity": bus.capacity,
        "passengers": bus.current_passengers,
        "status": "on route" if bus.is_on_route else "depot"
    }

def bus_to_summary_string(bus):
    return f"{bus.vehicle_type} #{bus.route_number} (мест: {bus.capacity}, скорость: {bus.average_speed} км/ч)"


# --- Callable-стратегии (паттерн «Стратегия») ---
class DiscountStrategy:
    """При вызове возвращает информацию о цене со скидкой."""
    def __init__(self, discount_percent):
        self.discount = discount_percent / 100.0

    def __call__(self, bus):
        try:
            original = bus.calculate_fare(1.0)
        except NotImplementedError:
            original = 0.0
        discounted = original * (1 - self.discount)
        return {
            "route": bus.route_number,
            "original_fare": round(original, 2),
            "discounted_fare": round(discounted, 2),
            "discount": f"{self.discount*100:.0f}%"
        }

class ActivateAllStrategy:
    """Пытается отправить все доступные автобусы на маршрут."""
    def __call__(self, bus):
        if not bus.is_on_route and bus.driver_name is not None:
            try:
                bus.start_route()
                return f"{bus.route_number}: отправлен на маршрут"
            except ValueError as e:
                return f"{bus.route_number}: ошибка – {e}"
        else:
            return f"{bus.route_number}: уже на маршруте или нет водителя"

class SortByCapacityCallable:
    """Callable-объект для сортировки по вместимости."""
    def __call__(self, bus):
        return bus.capacity