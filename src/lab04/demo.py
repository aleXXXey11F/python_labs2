#!/usr/bin/env python3
"""Демонстрация работы интерфейсов Printable и Comparable (автономная версия)."""

from models import (
    PrintableCityBus, ComparableIntercityBus, AdvancedElectricBus,
    Ticket, Fleet
)
from interfaces import Printable, Comparable

def print_separator(title):
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)

def scenario_1():
    print_separator("СЦЕНАРИЙ 1: БАЗОВАЯ РАБОТА ИНТЕРФЕЙСОВ")
    city = PrintableCityBus("5", 50, 60.5, "Иванов", low_floor=True, has_air_conditioning=True)
    inter = ComparableIntercityBus("205", 80, 90.0, "Петров", has_toilet=True, wifi_available=True)
    electro = AdvancedElectricBus("10", 40, 55.0, "Сидоров", battery_capacity=350.0)
    ticket = Ticket("T-100", "5", 35.0, "valid")

    for obj in [city, inter, electro, ticket]:
        if isinstance(obj, Printable):
            print(f"  Printable: {obj.to_string()}")
        if isinstance(obj, Comparable):
            print(f"  Comparable: реализован")

    bus1 = ComparableIntercityBus("101", 60, 85.0, "Водитель А")
    bus2 = ComparableIntercityBus("102", 60, 95.0, "Водитель Б")
    print(f"\n  bus1.compare_to(bus2) = {bus1.compare_to(bus2)}")

    t1 = Ticket("T1", "5", 30.0)
    t2 = Ticket("T2", "5", 50.0)
    print(f"  t1.compare_to(t2) = {t1.compare_to(t2)}")

def scenario_2():
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

    printables = [item for item in items if isinstance(item, Printable)]
    print_all(printables)

    print("\nСортировка билетов по цене:")
    tickets = [Ticket("A", "1", 50), Ticket("B", "1", 30), Ticket("C", "1", 40)]
    from functools import cmp_to_key
    tickets.sort(key=cmp_to_key(lambda a, b: a.compare_to(b)))
    for t in tickets:
        print(f"  {t.to_string()}")

    print("\nСортировка междугородних автобусов по скорости:")
    buses = [
        ComparableIntercityBus("10", 60, 85.0, "A"),
        ComparableIntercityBus("11", 60, 95.0, "B"),
        ComparableIntercityBus("12", 60, 75.0, "C"),
    ]
    buses.sort(key=cmp_to_key(lambda a, b: a.compare_to(b)))
    for b in buses:
        print(f"  [Comparable] {b}")

def scenario_3():
    print_separator("СЦЕНАРИЙ 3: КОЛЛЕКЦИЯ С ИНТЕРФЕЙСАМИ")
    fleet = Fleet()
    fleet.add(PrintableCityBus("5", 50, 60.5, "Иванов", low_floor=True, has_air_conditioning=True))
    fleet.add(ComparableIntercityBus("101", 80, 90.0, "Петров", has_toilet=True, wifi_available=True))
    fleet.add(ComparableIntercityBus("102", 75, 85.0, "Сидоров", has_toilet=False, wifi_available=True))
    fleet.add(ComparableIntercityBus("103", 85, 95.0, "Смирнов", has_toilet=True, wifi_available=False))
    fleet.add(AdvancedElectricBus("10", 40, 55.0, "Электроводитель", battery_capacity=350.0))
    fleet.add(Ticket("T-001", "5", 35.0, "valid"))
    fleet.add(Ticket("T-002", "10", 50.0, "used"))
    from models import CityBus as PlainCityBus
    fleet.add(PlainCityBus("7", 45, 55.0, "СтарыйВодитель", low_floor=False))

    print("Коллекция (Printable используют to_string):")
    print(fleet)

    print("\nФильтрация по Printable:")
    for obj in fleet.get_printable():
        print(f"  {obj.to_string()}")

    print("\nФильтрация по Comparable:")
    for obj in fleet.get_comparable():
        print(f"  {type(obj).__name__} – реализует compare_to")

    print("\nСортировка Comparable (группировка по типам, по возрастанию):")
    fleet.sort_comparable()
    print(fleet)

    print("\nПолиморфный вызов fleet.print_all_printable():")
    fleet.print_all_printable()

    print("\nПроверка isinstance:")
    for item in fleet:
        mid = getattr(item, 'route_number', getattr(item, 'ticket_id', '?'))
        print(f"  {mid}: Printable={isinstance(item, Printable)}, Comparable={isinstance(item, Comparable)}")

if __name__ == "__main__":
    print("=" * 70)
    print(" ЛАБОРАТОРНАЯ РАБОТА №4: ИНТЕРФЕЙСЫ И АБСТРАКТНЫЕ КЛАССЫ")
    print("=" * 70)
    scenario_1()
    scenario_2()
    scenario_3()
    print("\nДемонстрация завершена.")