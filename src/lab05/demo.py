"""
Демонстрация лабораторной работы №5.
Три сценария, покрывающих все требования: стратегии, фильтры, map, цепочки, callable-объекты.
"""

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
    """Вспомогательная функция для форматированного вывода."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_collection(fleet, message):
    """Вывод коллекции с заголовком."""
    print(f"\n{message}:")
    for i, bus in enumerate(fleet, 1):
        print(f"  {i}. {bus}")


# ------------------------------------------------------------
# Создание тестовой коллекции (разнотипные автобусы)
# ------------------------------------------------------------
fleet = Fleet()
fleet.add(CityBus("12", 80, 45, "Иванов", low_floor=True, has_air_conditioning=True))
fleet.add(CityBus("24", 60, 40, "Петров", low_floor=False))
fleet.add(IntercityBus("М4", 55, 90, "Сидоров", has_toilet=True, wifi_available=True))
fleet.add(IntercityBus("М8", 50, 85, "Козлов", has_toilet=False))
fleet.add(ElectricBus("7", 70, 35, "Смирнов", battery_capacity=250))

# Запустим некоторые на маршрут для разнообразия (водитель уже есть)
fleet._items[0].start_route()   # CityBus 12 на маршрут
fleet._items[2].start_route()   # IntercityBus М4 на маршрут
fleet._items[4].start_route()   # ElectricBus 7 на маршрут

# Имитация посадки пассажиров для реалистичности
for _ in range(30):
    fleet._items[0].board_passenger()
for _ in range(45):
    fleet._items[2].board_passenger()
for _ in range(20):
    fleet._items[4].board_passenger()

# ------------------------------------------------------------
# Сценарий 1: Полная цепочка filter → sort → apply
# ------------------------------------------------------------
print_section("Сценарий 1. Цепочка filter → sort → apply")

# 1) Исходная коллекция
print_collection(fleet, "Исходный автопарк")

# 2) filter_by – только автобусы на маршруте
on_route = fleet.filter_by(is_on_route)
print_collection(on_route, "После фильтрации (только на маршруте)")

# 3) sort_by – по заполненности (по убыванию эффективности)
#    Для наглядности используем отдельную функцию reversed через лямбду
on_route.sort_by(lambda b: -by_fill_ratio(b))
print_collection(on_route, "После сортировки (по убыванию заполненности)")

# 4) apply – применяем к каждому callable-стратегию (вывод скидки)
discount_10 = DiscountStrategy(10)
print("\nРезультат применения скидки 10% ко всем в отфильтрованной коллекции:")
for bus in on_route:
    info = discount_10(bus)
    print(f"  Маршрут {info['route']}: {info['original_fare']} → {info['discounted_fare']} ({info['discount']})")

# ------------------------------------------------------------
# Сценарий 2: Замена стратегии без изменения кода коллекции
# ------------------------------------------------------------
print_section("Сценарий 2. Взаимозаменяемость стратегий")

# Создадим свежую копию для чистоты эксперимента
fleet2 = Fleet()
for bus in fleet:
    fleet2._items.append(bus)

# Сортировка по разным стратегиям, один и тот же метод sort_by
print("\nСортировка по номеру маршрута:")
fleet2.sort_by(by_route_number)
print_collection(fleet2, "Результат")

print("\nСортировка по вместимости (через lambda):")
fleet2.sort_by(lambda b: b.capacity)
print_collection(fleet2, "Результат")

print("\nСортировка по средней скорости (callable-стратегия):")
speed_sorter = SortByCapacityCallable()  # специально callable, но сортирует по скорости? Исправим на by_speed позже, оставляем как демонстрацию:)
# Здесь по условию мы просто показываем, что можно передать другой callable
# Лучше передать по скорости через функцию:
fleet2.sort_by(by_speed)
print_collection(fleet2, "Результат (по скорости)")

# Фильтрация с заменой предиката
print("\nФильтрация: только городские автобусы:")
city_only = fleet2.filter_by(is_city_bus)
print_collection(city_only, "Результат")

print("\nТа же коллекция, другой фильтр: только электробусы:")
electric_only = fleet2.filter_by(is_electric_bus)
print_collection(electric_only, "Результат")

# ------------------------------------------------------------
# Сценарий 3: map, фабрика, lambda vs именованная функция, callable-объекты
# ------------------------------------------------------------
print_section("Сценарий 3. map, фабрики функций и callable-стратегии")

# 3.1 map() преобразование в словари
dicts = list(map(bus_to_dict, fleet))
print("\nmap bus_to_dict (первые 3 элемента):")
for d in dicts[:3]:
    print(" ", d)

# 3.2 map() с lambda для быстрого извлечения маршрутов
routes = list(map(lambda b: b.route_number, fleet))
print(f"\nНомера маршрутов всех автобусов (lambda): {routes}")

# 3.3 Фабрика функций: создать фильтр по вместимости >= 60
big_filter = make_capacity_filter(60)
big_fleet = fleet.filter_by(big_filter)
print_collection(big_fleet, "Автобусы с вместимостью >= 60 (фабрика make_capacity_filter(60))")

# 3.4 Сравнение lambda и именованной функции
# Именованная функция by_fill_ratio уже существует
print("\nСортировка по заполненности (именованная функция by_fill_ratio):")
fleet.sort_by(by_fill_ratio)
print_collection(fleet, "Результат")

# Тот же результат, но через lambda
fleet.sort_by(lambda b: b.current_passengers / b.capacity if b.capacity else 0)
print("\nСортировка по заполненности (lambda):")
print_collection(fleet, "Результат – идентичен предыдущему")

# 3.5 Callable-объект как стратегия
print("\nПрименение callable-стратегии ActivateAllStrategy ко всей коллекции:")
activator = ActivateAllStrategy()
results = [activator(bus) for bus in fleet]
for res in results:
    print(f"  {res}")

print_collection(fleet, "Состояние после попытки активации всех")