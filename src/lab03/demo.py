#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Демонстрационный файл для лабораторной работы №3.
Показывает иерархию классов, наследование, полиморфизм и работу с коллекцией.
"""

from models import CityBus, IntercityBus, ElectricBus, Fleet, Bus


def print_separator(title):
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)


def scenario_1_inheritance_and_super():
    """Сценарий 1: Создание объектов, демонстрация наследования и super()."""
    print_separator("СЦЕНАРИЙ 1: НАСЛЕДОВАНИЕ И ВЫЗОВ КОНСТРУКТОРА БАЗОВОГО КЛАССА")
    
    city_bus = CityBus("5", 50, 60.5, "Иванов И.И.", low_floor=True, has_air_conditioning=True)
    intercity_bus = IntercityBus("205", 80, 90.0, "Петров П.П.", has_toilet=True, wifi_available=True)
    electric_bus = ElectricBus("10", 40, 55.0, "Сидоров С.С.", battery_capacity=350.0, charging_time=3.5)
    
    print("Созданы объекты разных типов (конструкторы используют super()):")
    print(f"  {city_bus}")
    print(f"  {intercity_bus}")
    print(f"  {electric_bus}")
    
    print("\nАтрибуты, унаследованные от базового класса:")
    print(f"  CityBus: маршрут={city_bus.route_number}, вместимость={city_bus.capacity}")
    print(f"  IntercityBus: водитель={intercity_bus.driver_name}, скорость={intercity_bus.average_speed}")
    print(f"  ElectricBus: статус={electric_bus.is_on_route}, пассажиров={electric_bus.current_passengers}")
    
    print("\nНовые атрибуты производных классов:")
    print(f"  CityBus: low_floor={city_bus.low_floor}, air_conditioning={city_bus.has_air_conditioning}")
    print(f"  IntercityBus: has_toilet={intercity_bus.has_toilet}, wifi={intercity_bus.wifi_available}")
    print(f"  ElectricBus: battery_capacity={electric_bus.battery_capacity} кВт·ч")


def scenario_2_polymorphism_and_overriding():
    """Сценарий 2: Полиморфизм, переопределение методов, проверка типов."""
    print_separator("СЦЕНАРИЙ 2: ПОЛИМОРФИЗМ И ПЕРЕОПРЕДЕЛЕНИЕ МЕТОДОВ")
    
    city_bus = CityBus("7", 45, 55.0, "Алексеев А.А.", low_floor=True, has_air_conditioning=False)
    intercity_bus = IntercityBus("315", 70, 95.0, "Смирнов С.С.", has_toilet=True, wifi_available=True)
    electric_bus = ElectricBus("12", 35, 50.0, "Козлов К.К.", battery_capacity=280.0)
    
    # Отправляем на маршрут
    city_bus.start_route()
    intercity_bus.start_route()
    electric_bus.start_route()
    
    # Посадка пассажиров
    for _ in range(30):
        city_bus.board_passenger()
    for _ in range(50):
        intercity_bus.board_passenger()
    for _ in range(20):
        electric_bus.board_passenger()
    
    buses = [city_bus, intercity_bus, electric_bus]
    
    print("Переопределённый __str__() для разных типов:")
    for bus in buses:
        print(f"  {bus}")
    
    print("\nПереопределённый метод display_info():")
    for bus in buses:
        print(f"  {bus.display_info()}")
    
    print("\nПолиморфный метод calculate_fare():")
    print(f"  Городской (без расстояния): {city_bus.calculate_fare()} руб.")
    print(f"  Междугородний (150 км): {intercity_bus.calculate_fare(150):.2f} руб.")
    print(f"  Электробус: {electric_bus.calculate_fare()} руб.")
    
    print("\nПроверка типов с помощью isinstance():")
    for bus in buses:
        if isinstance(bus, CityBus):
            print(f"  {bus.route_number} — это городской автобус")
        elif isinstance(bus, IntercityBus):
            print(f"  {bus.route_number} — это междугородний автобус")
        elif isinstance(bus, ElectricBus):
            print(f"  {bus.route_number} — это электробус")
    
    print("\nСпецифический метод электробуса calculate_range():")
    print(f"  Запас хода электробуса: {electric_bus.calculate_range():.0f} км")


def scenario_3_fleet_with_types():
    """Сценарий 3: Коллекция, фильтрация по типам, полиморфизм."""
    print_separator("СЦЕНАРИЙ 3: КОЛЛЕКЦИЯ С ФИЛЬТРАЦИЕЙ ПО ТИПАМ")
    
    fleet = Fleet()
    
    fleet.add(CityBus("1", 40, 55.0, "Водитель1", low_floor=True, has_air_conditioning=True))
    fleet.add(CityBus("2", 50, 50.0, "Водитель2", low_floor=False, has_air_conditioning=False))
    fleet.add(IntercityBus("101", 60, 85.0, "Водитель3", has_toilet=True, wifi_available=True))
    fleet.add(IntercityBus("102", 55, 90.0, "Водитель4", has_toilet=False, wifi_available=False))
    fleet.add(ElectricBus("3", 35, 45.0, "Водитель5", battery_capacity=300.0))
    fleet.add(ElectricBus("4", 30, 40.0, "Водитель6", battery_capacity=250.0))
    
    print("Сформирован автопарк из 6 автобусов разных типов:")
    print(fleet)
    
    print("\n--- Фильтрация по типу (isinstance) ---")
    city_list = fleet.get_city_buses()
    print(f"Городских автобусов: {len(city_list)}")
    for bus in city_list:
        print(f"  {bus}")
    
    intercity_list = fleet.get_intercity_buses()
    print(f"\nМеждугородних автобусов: {len(intercity_list)}")
    for bus in intercity_list:
        print(f"  {bus}")
    
    electric_list = fleet.get_electric_buses()
    print(f"\nЭлектробусов: {len(electric_list)}")
    for bus in electric_list:
        print(f"  {bus}")
    
    print("\n--- Полиморфный вызов display_info() для всей коллекции ---")
    fleet.process_all()


def scenario_4_uniform_interface():
    """Сценарий 4: Единый интерфейс, полиморфизм без условий."""
    print_separator("СЦЕНАРИЙ 4: ЕДИНЫЙ ИНТЕРФЕЙС И ПОЛИМОРФНОЕ ПОВЕДЕНИЕ")
    
    fleet = Fleet()
    fleet.add(CityBus("8", 45, 60.0, "Михайлов М.М.", low_floor=True, has_air_conditioning=True))
    fleet.add(IntercityBus("220", 70, 95.0, "Николаев Н.Н.", has_toilet=True, wifi_available=True))
    fleet.add(ElectricBus("15", 40, 50.0, "Сергеев С.С.", battery_capacity=320.0))
    
    # Отправляем на маршрут и добавляем пассажиров
    for bus in fleet:
        bus.start_route()
        # Разное количество пассажиров для наглядности
        if isinstance(bus, CityBus):
            for _ in range(35):
                bus.board_passenger()
        elif isinstance(bus, IntercityBus):
            for _ in range(55):
                bus.board_passenger()
        elif isinstance(bus, ElectricBus):
            for _ in range(25):
                bus.board_passenger()
    
    print("Единый список объектов разных типов. Вызов одного метода — разное поведение.")
    print("\nВызов calculate_fare() для разных типов:")
    distance = 100.0
    for bus in fleet:
        if isinstance(bus, IntercityBus):
            fare = bus.calculate_fare(distance)
            print(f"  {bus.route_number} (междугородний, {distance} км): {fare:.2f} руб.")
        else:
            fare = bus.calculate_fare()
            print(f"  {bus.route_number} ({type(bus).__name__}): {fare:.2f} руб.")
    
    print("\nВызов get_efficiency_rating() (унаследован без изменений):")
    for bus in fleet:
        print(f"  {bus.route_number}: загрузка {bus.current_passengers}/{bus.capacity} → {bus.get_efficiency_rating()}")
    
    print("\nДемонстрация анти-паттерна vs гуд-паттерн:")
    print("  (гуд-паттерн: прямой вызов полиморфного метода, без проверок типа)")


def scenario_5_business_case():
    """Сценарий 5: Бизнес-сценарий с отчётом."""
    print_separator("СЦЕНАРИЙ 5: БИЗНЕС-СЦЕНАРИЙ (РАСЧЁТ СТОИМОСТИ ПРОЕЗДА ДЛЯ ВСЕГО ПАРКА)")
    
    fleet = Fleet()
    fleet.add(CityBus("C1", 45, 55.0, "Иванов", low_floor=True, has_air_conditioning=True))
    fleet.add(CityBus("C2", 50, 50.0, "Петров", low_floor=False, has_air_conditioning=False))
    fleet.add(IntercityBus("M1", 65, 85.0, "Сидоров", has_toilet=True, wifi_available=True))
    fleet.add(IntercityBus("M2", 60, 90.0, "Смирнов", has_toilet=False, wifi_available=False))
    fleet.add(ElectricBus("E1", 35, 45.0, "Кузнецов", battery_capacity=300.0))
    fleet.add(ElectricBus("E2", 30, 40.0, "Васильев", battery_capacity=250.0))
    
    # Отправляем на маршрут и имитируем загрузку
    for bus in fleet:
        bus.start_route()
        import random
        passengers = random.randint(10, bus.capacity)
        for _ in range(passengers):
            bus.board_passenger()
    
    print("Состояние автопарка после выхода на маршруты:")
    print(fleet)
    
    print("\n--- Расчёт стоимости проезда для пассажиров каждого рейса ---")
    total_revenue = 0.0
    distance_intercity = 120  # средняя дальность междугороднего рейса
    
    for bus in fleet:
        if bus.current_passengers > 0:
            if isinstance(bus, IntercityBus):
                fare_per_passenger = bus.calculate_fare(distance_intercity)
            else:
                fare_per_passenger = bus.calculate_fare()
            revenue = fare_per_passenger * bus.current_passengers
            total_revenue += revenue
            print(f"Маршрут {bus.route_number} ({type(bus).__name__}): "
                  f"пассажиров {bus.current_passengers}, тариф {fare_per_passenger:.2f} руб., "
                  f"выручка {revenue:.2f} руб.")
    
    print(f"\nОбщая выручка парка: {total_revenue:.2f} руб.")
    
    print("\n--- Фильтрация по типу для технического обслуживания ---")
    electric_buses = fleet.get_electric_buses()
    print(f"Электробусы, требующие проверки батареи ({len(electric_buses)} ед.):")
    for eb in electric_buses:
        print(f"  Маршрут {eb.route_number}: батарея {eb.battery_capacity} кВт·ч, "
              f"время зарядки {eb.charging_time} ч")


def main():
    print("=" * 70)
    print(" ЛАБОРАТОРНАЯ РАБОТА №3: НАСЛЕДОВАНИЕ И ИЕРАРХИЯ КЛАССОВ")
    print(" Тема: Транспорт (иерархия автобусов)")
    print("=" * 70)
    
    scenario_1_inheritance_and_super()
    scenario_2_polymorphism_and_overriding()
    scenario_3_fleet_with_types()
    scenario_4_uniform_interface()
    scenario_5_business_case()
    
    print_separator("ИТОГ")
    print(f"Всего создано автобусов за время работы программы: {Bus.total_buses_created}")
    print("Демонстрация завершена!")


if __name__ == "__main__":
    main()