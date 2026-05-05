"""
Демонстрация лабораторной работы №5.
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from lab03.models import CityBus, IntercityBus, ElectricBus
from lab05.collection import Fleet
from lab05.strategies import (
    by_route_number, by_capacity, by_speed, by_fill_ratio,
    is_city_bus, is_electric_bus, is_on_route,
    make_capacity_filter,
    bus_to_dict, bus_to_summary_string,
    DiscountStrategy, ActivateAllStrategy, SortByCapacityCallable
)


def print_section(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def print_collection(fleet, message):
    print(f"\n{message}:")
    for i, bus in enumerate(fleet, 1):
        print(f"  {i}. {bus}")


# ----- Создание тестовой коллекции -----
fleet = Fleet()
fleet.add(CityBus("12", 80, 45, "Иванов", low_floor=True, has_air_conditioning=True))
fleet.add(CityBus("24", 60, 40, "Петров", low_floor=False))
fleet.add(IntercityBus("М4", 55, 90, "Сидоров", has_toilet=True, wifi_available=True))
fleet.add(IntercityBus("М8", 50, 85, "Козлов", has_toilet=False))
fleet.add(ElectricBus("7", 70, 35, "Смирнов", battery_capacity=250))

# Имитация работы
fleet._items[0].start_route()
fleet._items[2].start_route()
fleet._items[4].start_route()
for _ in range(30): fleet._items[0].board_passenger()
for _ in range(45): fleet._items[2].board_passenger()
for _ in range(20): fleet._items[4].board_passenger()


# ----- Сценарий 1: цепочка filter → sort → apply -----
print_section("Сценарий 1. Цепочка filter → sort → apply")
print_collection(fleet, "Исходный автопарк")
on_route = fleet.filter_by(is_on_route)
print_collection(on_route, "Только на маршруте")
on_route.sort_by(lambda b: -by_fill_ratio(b))
print_collection(on_route, "Отсортированы по убыванию загрузки")
discount_10 = DiscountStrategy(10)
print("\nПрименение скидки 10% (DiscountStrategy):")
for bus in on_route:
    info = discount_10(bus)
    print(f"  Маршрут {info['route']}: {info['original_fare']} → {info['discounted_fare']} ({info['discount']})")


# ----- Сценарий 2: взаимозаменяемость стратегий -----
print_section("Сценарий 2. Взаимозаменяемость стратегий")
fleet2 = Fleet()
for bus in fleet: fleet2._items.append(bus)

print("\nСортировка по номеру маршрута:")
fleet2.sort_by(by_route_number)
print_collection(fleet2, "")

print("\nСортировка по вместимости:")
fleet2.sort_by(by_capacity)
print_collection(fleet2, "")

print("\nСортировка по скорости:")
fleet2.sort_by(by_speed)
print_collection(fleet2, "")

print("\nФильтрация: только городские автобусы:")
print_collection(fleet2.filter_by(is_city_bus), "")

print("\nФильтрация: только электробусы:")
print_collection(fleet2.filter_by(is_electric_bus), "")


# ----- Сценарий 3: map, фабрики, lambda и callable-объекты -----
print_section("Сценарий 3. map, фабрики, lambda и callable-стратегии")

# map
dicts = list(map(bus_to_dict, fleet))
print("\nmap bus_to_dict (первые 3):")
for d in dicts[:3]: print(" ", d)

routes = list(map(lambda b: b.route_number, fleet))
print(f"\nНомера маршрутов (lambda): {routes}")

# фабрика
big_filter = make_capacity_filter(60)
big_fleet = fleet.filter_by(big_filter)
print_collection(big_fleet, "Автобусы вместимостью >= 60 (фабрика make_capacity_filter(60))")

# lambda vs именованная функция
print("\nСортировка по заполненности (именованная функция by_fill_ratio):")
fleet.sort_by(by_fill_ratio)
print_collection(fleet, "")

fleet.sort_by(lambda b: b.current_passengers / b.capacity if b.capacity else 0)
print("\nСортировка по заполненности (lambda) – идентичный результат:")
print_collection(fleet, "")

# callable-объект
print("\nПрименение ActivateAllStrategy:")
activator = ActivateAllStrategy()
for bus in fleet:
    print(f"  {activator(bus)}")
print_collection(fleet, "Состояние после активации")