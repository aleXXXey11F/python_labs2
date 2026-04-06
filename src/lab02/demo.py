#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Демонстрационный файл для лабораторной работы №2.
Показывает работу класса Fleet (коллекция автобусов) со всеми возможностями.
"""

from model import Bus
from collection import Fleet


def print_separator(title):
    """Вспомогательная функция для красивого вывода."""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)


def print_fleet(fleet, title="Текущее состояние автопарка"):
    """Вспомогательная функция для вывода коллекции."""
    print(f"\n{title}:")
    print("-" * 60)
    if len(fleet) == 0:
        print("  (пусто)")
    else:
        for i, bus in enumerate(fleet):
            print(f"  {i+1}. {bus}")


def scenario_1_basic_operations():
    """Сценарий 1: Базовые операции (добавление, удаление, проверка типа)."""
    print_separator("СЦЕНАРИЙ 1: БАЗОВЫЕ ОПЕРАЦИИ")
    
    # Создание пустой коллекции
    fleet = Fleet()
    print("Создана пустая коллекция автобусов")
    print_fleet(fleet, "Коллекция после создания")
    
    # Создание автобусов
    bus1 = Bus("5", 50, 60.5, "Иванов И.И.")
    bus2 = Bus("15", 80, 55.0, "Петров П.П.")
    bus3 = Bus("22", 40, 65.0, "Сидоров С.С.")
    
    print("\nСозданы автобусы:")
    print(f"  {bus1}")
    print(f"  {bus2}")
    print(f"  {bus3}")
    
    # Добавление в коллекцию
    print("\n--- Добавление автобусов в коллекцию ---")
    fleet.add(bus1)
    print("Добавлен: Автобус маршрута 5")
    fleet.add(bus2)
    print("Добавлен: Автобус маршрута 15")
    fleet.add(bus3)
    print("Добавлен: Автобус маршрута 22")
    
    print_fleet(fleet, "Коллекция после добавления")
    
    # Проверка типа при добавлении
    print("\n--- Проверка типа при добавлении ---")
    try:
        fleet.add("Это строка, а не автобус")
    except TypeError as e:
        print(f"  Ошибка (ожидаемо): {e}")
    
    # Удаление автобуса
    print("\n--- Удаление автобуса ---")
    fleet.remove(bus2)
    print("Удален: Автобус маршрута 15")
    print_fleet(fleet, "Коллекция после удаления")


def scenario_2_search_and_duplicates():
    """Сценарий 2: Поиск и проверка дубликатов."""
    print_separator("СЦЕНАРИЙ 2: ПОИСК И ПРОВЕРКА ДУБЛИКАТОВ")
    
    fleet = Fleet()
    
    # Создание автобусов
    bus1 = Bus("5", 50, 60.5, "Иванов И.И.")
    bus2 = Bus("15", 80, 55.0, "Петров П.П.")
    bus3 = Bus("5", 50, 65.0, "Сидоров С.С.")  # Тот же маршрут и вместимость, что у bus1
    
    fleet.add(bus1)
    fleet.add(bus2)
    
    print("В коллекции:")
    print_fleet(fleet, "")
    
    # Проверка дубликатов
    print("\n--- Проверка на дубликаты ---")
    try:
        fleet.add(bus3)
    except ValueError as e:
        print(f"  Ошибка (ожидаемо): {e}")
    print("  Дубликат не был добавлен")
    
    # Поиск по номеру маршрута
    print("\n--- Поиск по номеру маршрута '5' ---")
    found = fleet.find_by_route_number("5")
    print(f"  Найдено автобусов: {len(found)}")
    for bus in found:
        print(f"    {bus}")
    
    # Поиск по имени водителя
    print("\n--- Поиск по имени водителя (частичное совпадение) ---")
    found = fleet.find_by_driver_name("Петров")
    print(f"  Найдено автобусов: {len(found)}")
    for bus in found:
        print(f"    {bus}")
    
    # Поиск по диапазону вместимости
    print("\n--- Поиск по диапазону вместимости (50-100) ---")
    found = fleet.find_by_capacity_range(50, 100)
    print(f"  Найдено автобусов: {len(found)}")
    for bus in found:
        print(f"    {bus}")
    
    # Использование len()
    print(f"\n--- Использование len() ---")
    print(f"  Всего автобусов в коллекции: {len(fleet)}")
    
    # Использование итерации
    print("\n--- Итерация по коллекции (for item in fleet) ---")
    for i, bus in enumerate(fleet):
        print(f"  {i+1}. {bus.route_number} - {bus.driver_name}")


def scenario_3_indexing_and_sorting():
    """Сценарий 3: Индексация и сортировка."""
    print_separator("СЦЕНАРИЙ 3: ИНДЕКСАЦИЯ И СОРТИРОВКА")
    
    fleet = Fleet()
    
    # Создание автобусов с разными характеристиками
    buses = [
        Bus("22", 40, 65.0, "Алексеев А.А."),
        Bus("5", 50, 60.5, "Иванов И.И."),
        Bus("15", 80, 55.0, "Петров П.П."),
        Bus("9", 60, 70.0, "Смирнов С.С."),
        Bus("3", 30, 50.0, "Козлов К.К."),
    ]
    
    for bus in buses:
        fleet.add(bus)
    
    print("Исходная коллекция (в порядке добавления):")
    print_fleet(fleet, "")
    
    # Доступ по индексу (__getitem__)
    print("\n--- Доступ по индексу ---")
    print(f"  fleet[0]: {fleet[0]}")
    print(f"  fleet[2]: {fleet[2]}")
    print(f"  fleet[-1]: {fleet[-1]}")
    
    try:
        print(f"  fleet[10]: {fleet[10]}")
    except IndexError as e:
        print(f"  Ошибка при доступе к несуществующему индексу: {e}")
    
    # Срез (также через __getitem__)
    print("\n--- Срез коллекции ---")
    slice_result = fleet[1:4]
    print(f"  fleet[1:4]: {len(slice_result)} автобусов")
    for bus in slice_result:
        print(f"    {bus.route_number} - {bus.driver_name}")
    
    # Удаление по индексу
    print("\n--- Удаление по индексу (remove_at) ---")
    removed = fleet.remove_at(2)
    print(f"  Удален автобус: {removed.route_number} - {removed.driver_name}")
    print_fleet(fleet, "Коллекция после удаления")
    
    # Сортировка по номеру маршрута
    print("\n--- Сортировка по номеру маршрута ---")
    fleet.sort_by_route_number()
    print_fleet(fleet, "После сортировки по номеру маршрута")
    
    # Сортировка по вместимости
    print("\n--- Сортировка по вместимости (по убыванию) ---")
    fleet.sort_by_capacity(reverse=True)
    print_fleet(fleet, "После сортировки по вместимости (от большей к меньшей)")
    
    # Сортировка по скорости
    print("\n--- Сортировка по средней скорости ---")
    fleet.sort_by_speed()
    print_fleet(fleet, "После сортировки по скорости (от меньшей к большей)")


def scenario_4_filtering():
    """Сценарий 4: Фильтрация коллекций."""
    print_separator("СЦЕНАРИЙ 4: ФИЛЬТРАЦИЯ КОЛЛЕКЦИЙ")
    
    fleet = Fleet()
    
    # Создание автобусов
    bus1 = Bus("5", 50, 60.5, "Иванов И.И.")
    bus2 = Bus("15", 80, 55.0, "Петров П.П.")
    bus3 = Bus("22", 40, 65.0, "Сидоров С.С.")
    bus4 = Bus("9", 60, 70.0, "Смирнов С.С.")
    
    fleet.add(bus1)
    fleet.add(bus2)
    fleet.add(bus3)
    fleet.add(bus4)
    
    # Отправляем некоторые автобусы на маршрут
    print("Отправляем автобусы на маршруты:")
    bus1.start_route()
    bus1.board_passenger()
    bus1.board_passenger()
    print(f"  {bus1.route_number} - на маршруте")
    
    bus2.start_route()
    for _ in range(60):
        bus2.board_passenger()
    print(f"  {bus2.route_number} - на маршруте (высокая загрузка)")
    
    bus3.start_route()
    for _ in range(10):
        bus3.board_passenger()
    print(f"  {bus3.route_number} - на маршруте (низкая загрузка)")
    
    # bus4 остается в парке
    print(f"  {bus4.route_number} - в парке")
    
    print_fleet(fleet, "Все автобусы")
    
    # Фильтрация: автобусы на маршруте
    print("\n--- Фильтрация: автобусы на маршруте (get_on_route) ---")
    on_route = fleet.get_on_route()
    print_fleet(on_route, "Автобусы на маршруте")
    
    # Фильтрация: автобусы в парке
    print("\n--- Фильтрация: автобусы в парке (get_in_depot) ---")
    in_depot = fleet.get_in_depot()
    print_fleet(in_depot, "Автобусы в парке")
    
    # Фильтрация по рейтингу эффективности
    print("\n--- Фильтрация: автобусы с высокой загрузкой ---")
    high_efficiency = fleet.get_by_efficiency("Высокая загрузка")
    print_fleet(high_efficiency, "Автобусы с высокой загрузкой")
    
    # Проверка, что фильтрация возвращает новую коллекцию
    print("\n--- Проверка: фильтрация не изменяет исходную коллекцию ---")
    print(f"  Исходная коллекция (get_in_depot): {len(in_depot)} автобусов")
    print(f"  Исходная коллекция (оригинал): {len(fleet)} автобусов")


def scenario_5_business_scenarios():
    """Сценарий 5: Бизнес-сценарии использования."""
    print_separator("СЦЕНАРИЙ 5: БИЗНЕС-СЦЕНАРИИ")
    
    # Сценарий 5.1: Управление парком автобусов
    print("\n--- Сценарий 5.1: Управление парком автобусов ---")
    
    fleet = Fleet()
    
    # Добавление новых автобусов
    print("1. Прием новых автобусов в парк:")
    new_buses = [
        Bus("101", 90, 60.0, "Водитель1"),
        Bus("102", 70, 55.0, "Водитель2"),
        Bus("103", 50, 65.0, "Водитель3"),
        Bus("104", 80, 58.0, "Водитель4"),
    ]
    
    for bus in new_buses:
        fleet.add(bus)
        print(f"   Принят: маршрут {bus.route_number}, вместимость {bus.capacity}")
    
    print(f"\n   Итого в парке: {len(fleet)} автобусов")
    
    # Отправка на маршруты
    print("\n2. Отправка автобусов на маршруты:")
    for bus in fleet:
        bus.start_route()
        # Случайное количество пассажиров
        import random
        passengers = random.randint(20, bus.capacity)
        for _ in range(passengers):
            bus.board_passenger()
        print(f"   Маршрут {bus.route_number}: {bus.current_passengers}/{bus.capacity} пассажиров")
    
    # Анализ загрузки
    print("\n3. Анализ загрузки парка:")
    high_load = fleet.get_by_efficiency("Высокая загрузка")
    medium_load = fleet.get_by_efficiency("Средняя загрузка")
    low_load = fleet.get_by_efficiency("Низкая загрузка")
    
    print(f"   Высокая загрузка: {len(high_load)} автобусов")
    print(f"   Средняя загрузка: {len(medium_load)} автобусов")
    print(f"   Низкая загрузка: {len(low_load)} автобусов")
    
    # Сценарий 5.2: Поиск и замена водителя
    print("\n--- Сценарий 5.2: Поиск и замена водителя ---")
    
    # Поиск автобуса по маршруту
    route_to_fix = "102"
    found_buses = fleet.find_by_route_number(route_to_fix)
    
    if found_buses:
        bus_to_fix = found_buses[0]
        print(f"  Найден автобус маршрута {route_to_fix}")
        print(f"  Текущий водитель: {bus_to_fix.driver_name}")
        
        # Замена водителя
        bus_to_fix.driver_name = "НовыйВодитель"
        print(f"  Новый водитель: {bus_to_fix.driver_name}")
    
    # Сценарий 5.3: Сортировка и отчет
    print("\n--- Сценарий 5.3: Формирование отчета по парку ---")
    
    print("\n  Отчет о автобусах (отсортировано по вместимости):")
    fleet.sort_by_capacity(reverse=True)
    print("-" * 65)
    print(f"  {'№':<3} {'Маршрут':<8} {'Вместимость':<12} {'Водитель':<15} {'Пассажиров':<10}")
    print("-" * 65)
    for i, bus in enumerate(fleet, 1):
        print(f"  {i:<3} {bus.route_number:<8} {bus.capacity:<12} {bus.driver_name:<15} {bus.current_passengers:<10}")
    print("-" * 65)
    
    total_capacity = sum(bus.capacity for bus in fleet)
    total_passengers = sum(bus.current_passengers for bus in fleet)
    print(f"\n  ИТОГО: вместимость парка: {total_capacity}, пассажиров: {total_passengers}")
    print(f"  Общая загрузка парка: {total_passengers/total_capacity*100:.1f}%")


def main():
    """Главная функция демонстрации."""
    print("=" * 70)
    print(" ЛАБОРАТОРНАЯ РАБОТА №2: КОЛЛЕКЦИЯ ОБЪЕКТОВ")
    print(" Тема: Транспорт (класс Fleet - коллекция автобусов)")
    print("=" * 70)
    
    scenario_1_basic_operations()
    scenario_2_search_and_duplicates()
    scenario_3_indexing_and_sorting()
    scenario_4_filtering()
    scenario_5_business_scenarios()
    
    print_separator("ИТОГ")
    print("Всего создано автобусов за время работы программы:", Bus.total_buses_created)
    print("Демонстрация завершена!")


if __name__ == "__main__":
    main()