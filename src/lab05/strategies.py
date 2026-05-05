"""
Модуль стратегий: сортировки, фильтры, фабрики, map-функции и callable-объекты.
Использует классы из collection.py (локальный импорт).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from collection import CityBus, IntercityBus, ElectricBus

"""
Модуль стратегий: сортировки, фильтры, фабрики, map-функции и callable-объекты.
Импортирует классы из локального collection.py.
"""
from .collection import CityBus, IntercityBus, ElectricBus

def by_route_number(bus):
    return bus.route_number

def by_capacity(bus):
    return bus.capacity

def by_speed(bus):
    return bus.average_speed

def by_fill_ratio(bus):
    return bus.current_passengers / bus.capacity if bus.capacity > 0 else 0

def by_driver_name(bus):
    return (bus.driver_name or "").lower()

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

def make_capacity_filter(min_capacity):
    def filter_fn(bus):
        return bus.capacity >= min_capacity
    return filter_fn

def make_route_filter(route_number):
    def filter_fn(bus):
        return bus.route_number == route_number
    return filter_fn

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

class DiscountStrategy:
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
    def __call__(self, bus):
        return bus.capacity