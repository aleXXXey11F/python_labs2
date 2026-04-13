#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Демонстрационный файл для лабораторной работы №3.
Показывает наследование, полиморфизм, работу с коллекцией Fleet.
"""

import sys
import os

# Добавляем пути для импорта Fleet из ЛР-2
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lab02.collection import Fleet

from base import Bus
from models import CityBus, TouristBus


def print_separator(title):
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)


def scenario_1_create_hierarchy():
    """Сценарий 1: Создание объектов разных типов."""
    print_separator("СЦЕНАРИЙ 1: СОЗДАНИЕ ОБЪЕКТОВ ИЕРАРХИИ")

    # Базовый класс
    bus1 = Bus("10", 50, 60.0, "Иванов И.И.")
    # Городской автобус
    city_bus = CityBus("5", 80, 45.0, "Петров П.П.",
                       number_of_stops=15, has_air_conditioning=True)
    # Туристический автобус
    tourist_bus = TouristBus("101", 40, 80.0, "Сидоров С.С.",
                             has_toilet=True, luggage_capacity=120)

    print("Созданы объекты:")
    print(f"  Базовый: {bus1}")
    print(f"  CityBus: {city_bus}")
    print(f"  TouristBus: {tourist_bus}")

    # Демонстрация новых методов
    print("\nНовые методы дочерних классов:")
    print(f"  CityBus плотность остановок: {city_bus.calculate_stop_density():.1f} остановок на 10 км")
    print(f"  TouristBus уровень комфорта: {tourist_bus.calculate_comfort_level()}/10")


def scenario_2_polymorphism():
    """Сценарий 2: Полиморфное поведение (переопределённый метод calculate_travel_time)."""
    print_separator("СЦЕНАРИЙ 2: ПОЛИМОРФИЗМ — РАСЧЁТ ВРЕМЕНИ В ПУТИ")

    distance = 50.0  # км

    # Создаём экземпляры разных типов
    ordinary = Bus("20", 60, 60.0, "Водитель1")
    city = CityBus("21", 80, 60.0, "Водитель2", number_of_stops=20, has_air_conditioning=True)
    tourist = TouristBus("22", 40, 60.0, "Водитель3", has_toilet=True, luggage_capacity=100)

    print(f"Дистанция: {distance} км, базовая скорость у всех 60 км/ч")
    print()

    # Единый вызов метода для разных объектов — разное поведение
    for obj in (ordinary, city, tourist):
        time = obj.calculate_travel_time(distance)
        print(f"{type(obj).__name__}: {time:.2f} ч → {time*60:.1f} мин")
        if isinstance(obj, CityBus):
            print(f"  (добавлено время на {city.number_of_stops} остановок)")
        elif isinstance(obj, TouristBus):
            print(f"  (добавлено 10% к времени из-за комфортного стиля)")


def scenario_3_fleet_with_mixed_types():
    """Сценарий 3: Коллекция Fleet хранит объекты разных типов."""
    print_separator("СЦЕНАРИЙ 3: КОЛЛЕКЦИЯ FLEET С РАЗНЫМИ ТИПАМИ АВТОБУСОВ")

    fleet = Fleet()

    # Создаём разные автобусы
    bus_a = Bus("1", 50, 65.0, "Алексеев")
    bus_b = CityBus("2", 80, 50.0, "Борисов", number_of_stops=12, has_air_conditioning=False)
    bus_c = TouristBus("3", 35, 90.0, "Владимиров", has_toilet=True, luggage_capacity=150)
    bus_d = CityBus("4", 60, 55.0, "Григорьев", number_of_stops=8, has_air_conditioning=True)

    # Добавляем в коллекцию
    for b in (bus_a, bus_b, bus_c, bus_d):
        fleet.add(b)

    print("В коллекцию добавлены 4 автобуса разных типов:")
    print(fleet)

    # Демонстрация полиморфизма через коллекцию
    print("\nВызов calculate_travel_time для каждого автобуса в коллекции (расстояние 30 км):")
    for i, bus in enumerate(fleet):
        time = bus.calculate_travel_time(30)
        print(f"  {i+1}. {type(bus).__name__}: {time:.2f} ч")


def scenario_4_filtering_by_type():
    """Сценарий 4: Фильтрация коллекции по типу с использованием isinstance."""
    print_separator("СЦЕНАРИЙ 4: ФИЛЬТРАЦИЯ ПО ТИПУ")

    fleet = Fleet()
    # Наполняем разными автобусами
    fleet.add(CityBus("10", 70, 52.0, "Вод1", 10, True))
    fleet.add(TouristBus("20", 45, 85.0, "Вод2", True, 200))
    fleet.add(CityBus("11", 90, 48.0, "Вод3", 14, False))
    fleet.add(Bus("30", 55, 65.0, "Вод4"))
    fleet.add(TouristBus("21", 50, 80.0, "Вод5", False, 80))

    print("Исходная коллекция (всего 5 автобусов):")
    print(fleet)

    # Фильтрация по типу CityBus
    city_buses = [b for b in fleet if isinstance(b, CityBus)]
    print(f"\nГородские автобусы (CityBus): {len(city_buses)}")
    for b in city_buses:
        print(f"  {b.route_number} | кондиционер: {'да' if b.has_air_conditioning else 'нет'}")

    # Фильтрация по типу TouristBus
    tourist_buses = [b for b in fleet if isinstance(b, TouristBus)]
    print(f"\nТуристические автобусы (TouristBus): {len(tourist_buses)}")
    for b in tourist_buses:
        print(f"  {b.route_number} | туалет: {'да' if b.has_toilet else 'нет'}")

    # Фильтрация только базового класса (не производных)
    pure_buses = [b for b in fleet if type(b) is Bus]
    print(f"\nЧистые базовые автобусы (не CityBus и не TouristBus): {len(pure_buses)}")


def scenario_5_polymorphic_interface():
    """Сценарий 5: Единый интерфейс без условий (полиморфизм)."""
    print_separator("СЦЕНАРИЙ 5: ПОЛИМОРФНЫЙ ИНТЕРФЕЙС")

    fleet = Fleet()
    fleet.add(CityBus("A", 70, 50.0, "Д1", 10, True))
    fleet.add(TouristBus("B", 40, 80.0, "Д2", True, 130))
    fleet.add(Bus("C", 55, 60.0, "Д3"))

    print("Для каждого автобуса вызываем метод get_efficiency_rating()")
    print("(результат зависит только от загрузки, но все объекты его поддерживают):\n")

    # Имитируем отправку на маршрут и посадку пассажиров
    for bus in fleet:
        bus.start_route()
    # Разная загрузка
    city_bus = fleet[0]
    for _ in range(60):
        city_bus.board_passenger()
    tourist_bus = fleet[1]
    for _ in range(10):
        tourist_bus.board_passenger()
    ordinary_bus = fleet[2]
    for _ in range(40):
        ordinary_bus.board_passenger()

    for bus in fleet:
        print(f"{type(bus).__name__} маршрут {bus.route_number}: "
              f"{bus.current_passengers}/{bus.capacity} пасс. → {bus.get_efficiency_rating()}")

    print("\nВызов общего метода calculate_travel_time (разное поведение без if/elif):")
    dist = 40
    for bus in fleet:
        print(f"{type(bus).__name__}: {bus.calculate_travel_time(dist):.2f} ч")


def main():
    print("=" * 70)
    print(" ЛАБОРАТОРНАЯ РАБОТА №3: НАСЛЕДОВАНИЕ И ИЕРАРХИЯ КЛАССОВ")
    print(" Тема: Транспорт (Bus → CityBus, TouristBus)")
    print("=" * 70)

    scenario_1_create_hierarchy()
    scenario_2_polymorphism()
    scenario_3_fleet_with_mixed_types()
    scenario_4_filtering_by_type()
    scenario_5_polymorphic_interface()

    print_separator("ИТОГ")
    print(f"Всего создано автобусов всех типов: {Bus.total_buses_created}")
    print("Демонстрация завершена!")


if __name__ == "__main__":
    main()