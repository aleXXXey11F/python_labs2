#!/usr/bin/env python3
"""Демонстрация работы интерфейсов Printable и Comparable."""

from models import PrintableCityBus, ComparableIntercityBus, AdvancedElectricBus, Ticket, ExtendedFleet
from interfaces import Printable, Comparable
from lab03.models import Bus

def print_separator(title):
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)

def scenario_1_interfaces_basics():
    """Сценарий 1: Создание объектов с интерфейсами, вызов методов."""
    print_separator("СЦЕНАРИЙ 1: БАЗОВАЯ РАБОТА ИНТЕРФЕЙСОВ")
    
    city_bus = PrintableCityBus("5", 50, 60.5, "Иванов", low_floor=True, has_air_conditioning=True)
    intercity_bus = ComparableIntercityBus("205", 80, 90.0, "Петров", has_toilet=True, wifi_available=True)
    electric_bus = AdvancedElectricBus("10", 40, 55.0, "Сидоров", battery_capacity=350.0)
    ticket = Ticket("T-100", "5", 35.0, "valid")
    
    objects = [city_bus, intercity_bus, electric_bus, ticket]
    
    print("Объекты, реализующие интерфейсы:")
    for obj in objects:
        if isinstance(obj, Printable):
            print(f"  Printable: {obj.to_string()}")
        if isinstance(obj, Comparable):
            print(f"  Comparable: реализован (compare_to)")

    print("\nСравнение через Comparable:")
    bus1 = ComparableIntercityBus("101", 60, 85.0, "Водитель А")
    bus2 = ComparableIntercityBus("102", 60, 95.0, "Водитель Б")
    res = bus1.compare_to(bus2)
    print(f"  bus1.compare_to(bus2) = {res} (bus1 скорость {bus1.average_speed}, bus2 {bus2.average_speed})")

    t1 = Ticket("T1", "5", 30.0)
    t2 = Ticket("T2", "5", 50.0)
    print(f"  t1.compare_to(t2) = {t1.compare_to(t2)} (цена {t1.price} vs {t2.price})")

def scenario_2_polymorphism():
    """Сценарий 2: Полиморфизм через интерфейсы, функции с типами интерфейсов."""
    print_separator("СЦЕНАРИЙ 2: ПОЛИМОРФИЗМ ЧЕРЕЗ ИНТЕРФЕЙСЫ")
    
    items = [
        PrintableCityBus("1", 40, 50.0, "Водитель1"),
        AdvancedElectricBus("E1", 30, 45.0, "Водитель2", battery_capacity=280.0),
        Ticket("T-200", "1", 25.0),
        Ticket("T-201", "E1", 30.0, "used"),
    ]
    
    def print_all(items: list[Printable]):
        print("Вывод всех Printable объектов:")
        for item in items:
            print(f"  {item.to_string()}")
    
    print_all([item for item in items if isinstance(item, Printable)])
    
    print("\nСортировка списка Comparable объектов:")
    comparable_list = [item for item in items if isinstance(item, Comparable)]
    # Используем cmp_to_key для сортировки по compare_to
    from functools import cmp_to_key
    comparable_list.sort(key=cmp_to_key(lambda a, b: a.compare_to(b)))
    print("После сортировки (по возрастанию ключа compare_to):")
    for item in comparable_list:
        if isinstance(item, Printable):
            print(f"  {item.to_string()}")

def scenario_3_fleet_integration():
    """Сценарий 3: Интеграция с коллекцией Fleet – фильтрация, сортировка, вывод."""
    print_separator("СЦЕНАРИЙ 3: КОЛЛЕКЦИЯ С ИНТЕРФЕЙСАМИ")
    
    fleet = ExtendedFleet()
    
    fleet.add(PrintableCityBus("5", 50, 60.5, "Иванов", low_floor=True, has_air_conditioning=True))
    fleet.add(ComparableIntercityBus("205", 80, 90.0, "Петров", has_toilet=True, wifi_available=True))
    fleet.add(AdvancedElectricBus("10", 40, 55.0, "Сидоров", battery_capacity=350.0))
    fleet.add(Ticket("T-001", "5", 35.0, "valid"))
    fleet.add(Ticket("T-002", "10", 50.0, "used"))
    # Добавим обычный автобус из lab03, не реализующий интерфейсы
    from lab03.models import CityBus
    fleet.add(CityBus("7", 45, 55.0, "СтарыйВодитель", low_floor=False))
    
    print("Коллекция ExtendedFleet (использует to_string для Printable):")
    print(fleet)
    
    print("\nФильтрация по интерфейсу Printable:")
    printables = fleet.get_printable()
    for obj in printables:
        print(f"  {obj.to_string()}")
    
    print("\nФильтрация по интерфейсу Comparable:")
    comparables = fleet.get_comparable()
    for obj in comparables:
        print(f"  {type(obj).__name__} – реализует compare_to")
    
    print("\nСортировка Comparable-объектов в коллекции (по возрастанию):")
    fleet.sort_comparable()
    print(fleet)
    
    print("\nПолиморфный вывод всех Printable через fleet.print_all_printable():")
    fleet.print_all_printable()
    
    print("\nПроверка isinstance:")
    for item in fleet:
        print(f"  {item.route_number if hasattr(item,'route_number') else item.ticket_id}: "
              f"Printable={isinstance(item, Printable)}, Comparable={isinstance(item, Comparable)}")

def main():
    print("="*70)
    print(" ЛАБОРАТОРНАЯ РАБОТА №4: ИНТЕРФЕЙСЫ И АБСТРАКТНЫЕ КЛАССЫ")
    print("="*70)
    scenario_1_interfaces_basics()
    scenario_2_polymorphism()
    scenario_3_fleet_integration()
    print("\nВсе сценарии выполнены.")

if __name__ == "__main__":
    main()