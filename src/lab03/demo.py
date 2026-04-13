#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Демонстрационный файл для лабораторной работы №3.
Показывает работу иерархии классов Bus, CityBus, TouristBus, SchoolBus.
"""

from .base import Bus
from .models import CityBus, TouristBus, SchoolBus
from ..lab02.collection import Fleet


def print_separator(title):
    """Вспомогательная функция для красивого вывода."""
    print("\n" + "=" * 80)
    print(f" {title}")
    print("=" * 80)


def print_bus_info(bus, title=None):
    """Вывод информации об автобусе."""
    if title:
        print(f"\n{title}:")
    print(f"  {bus}")
    print(f"  Тип: {type(bus).__name__}")
    print(f"  Стоимость проезда (10 км): {bus.calculate_fare(10):.2f} руб")


def scenario_1_inheritance_demo():
    """Сценарий 1: Демонстрация наследования."""
    print_separator("СЦЕНАРИЙ 1: НАСЛЕДОВАНИЕ КЛАССОВ")
    
    # Создание объектов разных типов
    city_bus = CityBus("5", 50, 60.5, "Иванов И.И.", "обычный", True)
    tourist_bus = TouristBus("ТУР-1", 30, 80.0, "Петров П.П.", True, True, "Сидорова А.А.")
    school_bus = SchoolBus("ШК-1", 40, 55.0, "Сергеев С.С.", True, "МБОУ Гимназия №1")
    
    print("\nСозданы объекты разных типов:")
    print_bus_info(city_bus, "🏙️ Городской автобус")
    print_bus_info(tourist_bus, "🏖️ Туристический автобус")
    print_bus_info(school_bus, "🏫 Школьный автобус")
    
    # Демонстрация использования super()
    print("\n--- Демонстрация super() ---")
    print("Все дочерние классы используют super() для вызова конструктора базового класса")
    print("Базовый код не дублируется, все общие атрибуты инициализируются в Bus.__init__")


def scenario_2_new_attributes_and_methods():
    """Сценарий 2: Новые атрибуты и методы."""
    print_separator("СЦЕНАРИЙ 2: НОВЫЕ АТРИБУТЫ И МЕТОДЫ")
    
    city_bus = CityBus("10", 60, 65.0, "Козлов К.К.", "экспресс", True)
    tourist_bus = TouristBus("ТУР-2", 25, 90.0, "Михайлов М.М.", True, False, None)
    school_bus = SchoolBus("ШК-2", 35, 50.0, "Федоров Ф.Ф.", False, "МБОУ СОШ №5")
    
    # Новые атрибуты CityBus
    print("\n--- CityBus: новые атрибуты ---")
    print(f"  Тип маршрута: {city_bus.route_type}")
    print(f"  Наличие валидатора: {city_bus.has_validator}")
    print(f"  Расписание: {city_bus.get_route_schedule()}")
    
    # Новые атрибуты TouristBus
    print("\n--- TouristBus: новые атрибуты ---")
    print(f"  Наличие WiFi: {tourist_bus.has_wifi}")
    print(f"  Наличие туалета: {tourist_bus.has_toilet}")
    print(f"  Экскурсовод: {tourist_bus.tour_guide_name}")
    print(f"  Уровень комфорта: {tourist_bus.get_comfort_level()}")
    
    # Новые атрибуты SchoolBus
    print("\n--- SchoolBus: новые атрибуты ---")
    print(f"  Наличие сопровождающего: {school_bus.has_escort}")
    print(f"  Школа: {school_bus.school_name}")
    print(f"  Рейтинг безопасности: {school_bus.get_safety_rating()}")


def scenario_3_polymorphism():
    """Сценарий 3: Полиморфизм и переопределение методов."""
    print_separator("СЦЕНАРИЙ 3: ПОЛИМОРФИЗМ")
    
    # Создание списка объектов разных типов
    buses = [
        CityBus("5", 50, 60.5, "Иванов И.И.", "обычный", True),
        TouristBus("ТУР-1", 30, 80.0, "Петров П.П.", True, True, "Сидорова А.А."),
        SchoolBus("ШК-1", 40, 55.0, "Сергеев С.С.", True, "МБОУ Гимназия №1"),
        CityBus("15", 80, 55.0, "Алексеев А.А.", "экспресс", False),
    ]
    
    print("\nПолиморфизм метода calculate_fare():")
    print("-" * 60)
    print(f"{'Тип автобуса':<25} {'Расстояние 5 км':<20} {'Расстояние 10 км':<20} {'Расстояние 20 км':<20}")
    print("-" * 60)
    
    for bus in buses:
        bus_type = type(bus).__name__
        fare_5 = bus.calculate_fare(5)
        fare_10 = bus.calculate_fare(10)
        fare_20 = bus.calculate_fare(20)
        print(f"{bus_type:<25} {fare_5:>15.2f} руб {fare_10:>15.2f} руб {fare_20:>15.2f} руб")
    
    print("\n--- Разное поведение одного метода для разных объектов ---")
    for bus in buses:
        print(f"\n{type(bus).__name__}:")
        print(f"  {bus}")
        print(f"  Стоимость проезда (15 км): {bus.calculate_fare(15):.2f} руб")


def scenario_4_isinstance_and_override():
    """Сценарий 4: isinstance() и переопределение __str__."""
    print_separator("СЦЕНАРИЙ 4: ISINSTANCE() И ПЕРЕОПРЕДЕЛЕНИЕ __STR__")
    
    city_bus = CityBus("5", 50, 60.5, "Иванов И.И.")
    tourist_bus = TouristBus("ТУР-1", 30, 80.0, "Петров П.П.")
    school_bus = SchoolBus("ШК-1", 40, 55.0, "Сергеев С.С.")
    
    # Проверка типов
    print("\n--- Проверка типов через isinstance() ---")
    print(f"city_bus является Bus: {isinstance(city_bus, Bus)}")
    print(f"city_bus является CityBus: {isinstance(city_bus, CityBus)}")
    print(f"city_bus является TouristBus: {isinstance(city_bus, TouristBus)}")
    
    print(f"\ntourist_bus является Bus: {isinstance(tourist_bus, Bus)}")
    print(f"tourist_bus является TouristBus: {isinstance(tourist_bus, TouristBus)}")
    
    # Переопределение __str__
    print("\n--- Переопределение __str__ в дочерних классах ---")
    print("Базовый класс Bus:")
    base_bus = Bus("100", 60, 65.0, "Тестовый")
    print(f"  {base_bus}")
    
    print("\nДочерние классы (расширенное строковое представление):")
    print(f"  {city_bus}")
    print(f"  {tourist_bus}")
    print(f"  {school_bus}")


def scenario_5_collection_integration():
    """Сценарий 5: Интеграция с коллекцией из ЛР-2."""
    print_separator("СЦЕНАРИЙ 5: КОЛЛЕКЦИЯ РАЗНЫХ ТИПОВ ОБЪЕКТОВ")
    
    # Создание коллекции
    fleet = Fleet()
    
    # Добавление объектов разных типов
    city_bus1 = CityBus("5", 50, 60.5, "Иванов И.И.", "обычный", True)
    city_bus2 = CityBus("15", 80, 55.0, "Петров П.П.", "экспресс", False)
    tourist_bus1 = TouristBus("ТУР-1", 30, 80.0, "Сидоров С.С.", True, True, "Козлова А.А.")
    tourist_bus2 = TouristBus("ТУР-2", 25, 90.0, "Михайлов М.М.", True, False, None)
    school_bus1 = SchoolBus("ШК-1", 40, 55.0, "Сергеев С.С.", True, "МБОУ Гимназия №1")
    school_bus2 = SchoolBus("ШК-2", 35, 50.0, "Федоров Ф.Ф.", False, "МБОУ СОШ №5")
    
    # Отправляем на маршруты
    for bus in [city_bus1, city_bus2, tourist_bus1, school_bus1]:
        bus.start_route()
    
    # Посадка пассажиров
    for _ in range(30):
        city_bus1.board_passenger()
    for _ in range(60):
        city_bus2.board_passenger()
    for _ in range(20):
        tourist_bus1.board_passenger()
    for _ in range(25):
        school_bus1.board_passenger()
    
    # Добавление в коллекцию
    for bus in [city_bus1, city_bus2, tourist_bus1, tourist_bus2, school_bus1, school_bus2]:
        fleet.add(bus)
    
    print(f"\nКоллекция содержит {len(fleet)} автобусов разных типов:")
    for i, bus in enumerate(fleet):
        print(f"  {i+1}. {type(bus).__name__}: {bus.route_number}")
    
    # Фильтрация по типу
    print("\n--- Фильтрация по типу (ручная) ---")
    
    city_buses = [bus for bus in fleet if isinstance(bus, CityBus)]
    tourist_buses = [bus for bus in fleet if isinstance(bus, TouristBus)]
    school_buses = [bus for bus in fleet if isinstance(bus, SchoolBus)]
    
    print(f"  Городских автобусов: {len(city_buses)}")
    print(f"  Туристических автобусов: {len(tourist_buses)}")
    print(f"  Школьных автобусов: {len(school_buses)}")
    
    # Полиморфный вызов для всей коллекции
    print("\n--- Полиморфный вызов calculate_fare(10 км) для всех автобусов ---")
    for bus in fleet:
        fare = bus.calculate_fare(10)
        print(f"  {type(bus).__name__} маршрута {bus.route_number}: {fare:.2f} руб")
    
    # Вызов get_info() для всех
    print("\n--- Информация о каждом автобусе (метод get_info) ---")
    for bus in fleet[:3]:  # Первые 3 для краткости
        info = bus.get_info()
        print(f"\n  {type(bus).__name__}:")
        for key, value in info.items():
            print(f"    {key}: {value}")


def scenario_6_polymorphism_without_conditions():
    """Сценарий 6: Полиморфизм без условий (анти-паттерн if type == ...)."""
    print_separator("СЦЕНАРИЙ 6: ПОЛИМОРФИЗМ БЕЗ УСЛОВИЙ")
    
    # Пример анти-паттерна (плохо)
    print("\n❌ Анти-паттерн (не делайте так!):")
    print("def calculate_any_fare(bus, distance):")
    print("    if type(bus) == CityBus:")
    print("        return bus.calculate_fare(distance)")
    print("    elif type(bus) == TouristBus:")
    print("        return bus.calculate_fare(distance)")
    print("    ...")
    
    # ✅ Правильный подход - полиморфизм
    print("\n✅ Правильный подход (полиморфизм):")
    print("def calculate_any_fare(bus, distance):")
    print("    return bus.calculate_fare(distance)  # Общий интерфейс")
    
    buses = [
        CityBus("1", 50, 60.0, "В1"),
        TouristBus("2", 30, 80.0, "В2"),
        SchoolBus("3", 40, 55.0, "В3"),
    ]
    
    # Отправляем на маршрут
    for bus in buses:
        bus.start_route()
    
    print("\n--- Полиморфный вызов без проверки типов ---")
    print("Единый интерфейс calculate_fare() работает по-разному для разных типов:")
    
    for bus in buses:
        # Никаких if type == ... !
        fare = bus.calculate_fare(10)
        rating = bus.get_efficiency_rating()
        print(f"\n  {type(bus).__name__}:")
        print(f"    Автобус: {bus}")
        print(f"    Стоимость проезда (10 км): {fare:.2f} руб")
        print(f"    Эффективность: {rating}")


def scenario_7_filtering_by_type():
    """Сценарий 7: Фильтрация коллекции по типу."""
    print_separator("СЦЕНАРИЙ 7: ФИЛЬТРАЦИЯ ПО ТИПУ")
    
    fleet = Fleet()
    
    # Создание разных автобусов
    buses_data = [
        ("Городской", CityBus, "5", 50, 60.5, "Иванов И.И."),
        ("Городской", CityBus, "15", 80, 55.0, "Петров П.П."),
        ("Туристический", TouristBus, "ТУР-1", 30, 80.0, "Сидоров С.С."),
        ("Туристический", TouristBus, "ТУР-2", 25, 90.0, "Козлов К.К."),
        ("Школьный", SchoolBus, "ШК-1", 40, 55.0, "Сергеев С.С."),
        ("Школьный", SchoolBus, "ШК-2", 35, 50.0, "Федоров Ф.Ф."),
        ("Городской", CityBus, "22", 60, 65.0, "Алексеев А.А."),
    ]
    
    for _, bus_class, route, cap, speed, driver in buses_data:
        bus = bus_class(route, cap, speed, driver)
        bus.start_route()
        # Случайное количество пассажиров
        import random
        for _ in range(random.randint(10, cap - 5)):
            try:
                bus.board_passenger()
            except:
                pass
        fleet.add(bus)
    
    print(f"\nВсего автобусов в парке: {len(fleet)}")
    
    # Функции фильтрации по типу
    def get_only_city_buses(collection):
        """Получить только городские автобусы."""
        result = Fleet()
        for bus in collection:
            if isinstance(bus, CityBus):
                result.add(bus)
        return result
    
    def get_only_tourist_buses(collection):
        """Получить только туристические автобусы."""
        result = Fleet()
        for bus in collection:
            if isinstance(bus, TouristBus):
                result.add(bus)
        return result
    
    def get_only_school_buses(collection):
        """Получить только школьные автобусы."""
        result = Fleet()
        for bus in collection:
            if isinstance(bus, SchoolBus):
                result.add(bus)
        return result
    
    # Применение фильтрации
    city_fleet = get_only_city_buses(fleet)
    tourist_fleet = get_only_tourist_buses(fleet)
    school_fleet = get_only_school_buses(fleet)
    
    print(f"\n--- Фильтрация по типу ---")
    print(f"  Городские автобусы: {len(city_fleet)}")
    for bus in city_fleet:
        print(f"    - Маршрут {bus.route_number}, вместимость {bus.capacity}, пассажиров: {bus.current_passengers}")
    
    print(f"\n  Туристические автобусы: {len(tourist_fleet)}")
    for bus in tourist_fleet:
        print(f"    - Маршрут {bus.route_number}, вместимость {bus.capacity}, комфорт: {bus.get_comfort_level()}")
    
    print(f"\n  Школьные автобусы: {len(school_fleet)}")
    for bus in school_fleet:
        print(f"    - Маршрут {bus.route_number}, школа: {bus.school_name}, безопасность: {bus.get_safety_rating()}")
    
    # Статистика по типам
    print("\n--- Статистика по типам ---")
    total_capacity_city = sum(bus.capacity for bus in city_fleet)
    total_capacity_tourist = sum(bus.capacity for bus in tourist_fleet)
    total_capacity_school = sum(bus.capacity for bus in school_fleet)
    
    print(f"  Городские: общая вместимость {total_capacity_city}, средняя загрузка: {sum(bus.current_passengers for bus in city_fleet)/total_capacity_city*100:.1f}%")
    print(f"  Туристические: общая вместимость {total_capacity_tourist}, средняя загрузка: {sum(bus.current_passengers for bus in tourist_fleet)/total_capacity_tourist*100:.1f}%")
    print(f"  Школьные: общая вместимость {total_capacity_school}, средняя загрузка: {sum(bus.current_passengers for bus in school_fleet)/total_capacity_school*100:.1f}%")


def main():
    """Главная функция демонстрации."""
    print("=" * 80)
    print(" ЛАБОРАТОРНАЯ РАБОТА №3: НАСЛЕДОВАНИЕ И ИЕРАРХИЯ КЛАССОВ")
    print(" Тема: Транспорт (Bus и его наследники)")
    print("=" * 80)
    
    scenario_1_inheritance_demo()
    scenario_2_new_attributes_and_methods()
    scenario_3_polymorphism()
    scenario_4_isinstance_and_override()
    scenario_5_collection_integration()
    scenario_6_polymorphism_without_conditions()
    scenario_7_filtering_by_type()
    
    print_separator("ИТОГ")
    print(f"Всего создано автобусов за время работы программы: {Bus.total_buses_created}")
    print("✅ Демонстрация всех возможностей наследования и полиморфизма завершена!")
    print("\nКлючевые моменты:")
    print("  • Базовый класс Bus (из ЛР-1)")
    print("  • 3 дочерних класса: CityBus, TouristBus, SchoolBus")
    print("  • Использование super() для вызова конструктора базового класса")
    print("  • Новые атрибуты и методы в каждом дочернем классе")
    print("  • Переопределение метода calculate_fare() (полиморфизм)")
    print("  • Переопределение __str__() и get_info()")
    print("  • Использование isinstance() для проверки типов")
    print("  • Интеграция с коллекцией Fleet из ЛР-2")
    print("  • Фильтрация коллекции по типу объектов")


if __name__ == "__main__":
    main()