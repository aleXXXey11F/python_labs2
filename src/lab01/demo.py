#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Демонстрационный файл для лабораторной работы №1.
Показывает работу класса Bus со всеми возможностями.
"""

from model import Bus


def print_separator(title):
    """Вспомогательная функция для красивого вывода."""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def demonstrate_creation():
    """Демонстрация создания объектов и атрибутов класса."""
    print_separator("1. СОЗДАНИЕ ОБЪЕКТОВ И АТРИБУТЫ КЛАССА")
    
    # Создание автобусов
    bus1 = Bus("5", 50, 60.5, "Иванов И.И.")
    bus2 = Bus("15", 80, 55.0, "Петров П.П.")
    bus3 = Bus("5", 50, 65.0, "Сидоров С.С.")  # Тот же маршрут и вместимость
    
    print("Созданы автобусы:")
    print(f"  {bus1}")
    print(f"  {bus2}")
    print(f"  {bus3}")
    
    # Демонстрация атрибутов класса
    print(f"\nАтрибуты класса:")
    print(f"  vehicle_type (через класс): {Bus.vehicle_type}")
    print(f"  vehicle_type (через экземпляр): {bus1.vehicle_type}")
    print(f"  Всего создано автобусов: {Bus.total_buses_created}")
    
    # Изменение атрибута класса
    Bus.vehicle_type = "Городской автобус"
    print(f"\nПосле изменения атрибута класса:")
    print(f"  vehicle_type: {bus2.vehicle_type}")


def demonstrate_magic_methods():
    """Демонстрация магических методов."""
    print_separator("2. МАГИЧЕСКИЕ МЕТОДЫ")
    
    bus = Bus("25", 90, 50.0, "Михайлов М.М.")
    
    print(f"__str__(): {bus}")
    print(f"__repr__(): {repr(bus)}")
    
    # Демонстрация __eq__
    bus_same = Bus("25", 90, 45.0, "Николаев Н.Н.")  # Другой водитель, скорость
    bus_different = Bus("30", 60, 55.0, "Алексеев А.А.")
    
    print(f"\nСравнение автобусов:")
    print(f"  bus == bus_same: {bus == bus_same} (разные водители, но маршрут/вместимость совпадают)")
    print(f"  bus == bus_different: {bus == bus_different}")


def demonstrate_properties_and_setters():
    """Демонстрация свойств и сеттеров."""
    print_separator("3. СВОЙСТВА И СЕТТЕРЫ")
    
    bus = Bus("10", 60, 55.5, "Сергеев С.С.")
    print(f"Начальное состояние: {bus}")
    
    # Чтение свойств
    print(f"\nСвойства (геттеры):")
    print(f"  Номер маршрута: {bus.route_number}")
    print(f"  Вместимость: {bus.capacity}")
    print(f"  Скорость: {bus.average_speed} км/ч")
    print(f"  Водитель: {bus.driver_name}")
    print(f"  Вычисляемое свойство (свободные места): {bus.free_seats}")
    
    # Изменение через сеттер
    print(f"\nИзменение водителя через setter:")
    bus.driver_name = "Козлов К.К."
    print(f"  Новый водитель: {bus.driver_name}")
    print(f"  Обновленный автобус: {bus}")
    
    # Попытка некорректного изменения
    print(f"\nПопытка установить пустое имя водителя:")
    try:
        bus.driver_name = ""
    except ValueError as e:
        print(f"  Ошибка валидации: {e}")


def demonstrate_business_methods():
    """Демонстрация бизнес-методов и логических состояний."""
    print_separator("4. БИЗНЕС-МЕТОДЫ И ЛОГИЧЕСКИЕ СОСТОЯНИЯ")
    
    bus = Bus("12", 40, 45.0, "Соколов С.С.")
    print(f"Начальное состояние: {bus}")
    
    # Попытка посадить пассажира до выхода на маршрут
    print(f"\nПопытка посадить пассажира до выхода на маршрут:")
    try:
        bus.board_passenger()
    except ValueError as e:
        print(f"  Ошибка: {e}")
    
    # Выход на маршрут
    print(f"\nВыход на маршрут:")
    bus.start_route()
    print(f"  Статус после старта: {'на маршруте' if bus.is_on_route else 'в парке'}")
    
    # Посадка пассажиров
    print(f"\nПосадка пассажиров:")
    for i in range(15):
        bus.board_passenger()
    print(f"  После посадки 15 пассажиров: {bus}")
    print(f"  Свободных мест: {bus.free_seats}")
    print(f"  Рейтинг эффективности: {bus.get_efficiency_rating()}")
    
    # Добавим еще пассажиров
    for i in range(25):
        bus.board_passenger()
    print(f"\nПосле посадки всех пассажиров: {bus}")
    print(f"  Свободных мест: {bus.free_seats}")
    print(f"  Рейтинг эффективности: {bus.get_efficiency_rating()}")
    
    # Попытка посадить лишнего пассажира
    print(f"\nПопытка посадить 41-го пассажира:")
    if not bus.board_passenger():
        print(f"  Мест нет! Пассажир остался на остановке")
    
    # Высадка пассажиров
    print(f"\nВысадка пассажиров:")
    for i in range(10):
        bus.alight_passenger()
    print(f"  После высадки 10 пассажиров: {bus}")
    
    # Расчет времени в пути
    distance = 25.5
    travel_time = bus.calculate_travel_time(distance)
    print(f"\nРасчет времени в пути:")
    print(f"  Расстояние: {distance} км")
    print(f"  Средняя скорость: {bus.average_speed} км/ч")
    print(f"  Время в пути: {travel_time:.2f} ч ({travel_time*60:.0f} мин)")
    
    # Завершение маршрута
    print(f"\nЗавершение маршрута:")
    bus.end_route()
    print(f"  После завершения: {bus}")


def demonstrate_validation():
    """Демонстрация валидации данных."""
    print_separator("5. ВАЛИДАЦИЯ ДАННЫХ")
    
    print("Попытки создания автобусов с некорректными данными:")
    
    test_cases = [
        ("Некорректный номер маршрута", "", 50, 60.0, "Иванов"),
        ("Некорректный тип номера", 123, 50, 60.0, "Иванов"),
        ("Отрицательная вместимость", "5", -10, 60.0, "Иванов"),
        ("Слишком большая вместимость", "5", 150, 60.0, "Иванов"),
        ("Скорость слишком низкая", "5", 50, 5.0, "Иванов"),
        ("Скорость слишком высокая", "5", 50, 150.0, "Иванов"),
        ("Пустое имя водителя", "5", 50, 60.0, "   "),
    ]
    
    for description, route, cap, speed, driver in test_cases:
        print(f"\n  {description}:")
        try:
            bus = Bus(route, cap, speed, driver)
            print(f"    Успешно создан: {bus}")
        except ValueError as e:
            print(f"    Ошибка: {e}")


def main():
    """Главная функция демонстрации."""
    print("=" * 60)
    print(" ЛАБОРАТОРНАЯ РАБОТА №1: КЛАСС И ИНКАПСУЛЯЦИЯ")
    print(" Тема: Транспорт (класс Bus)")
    print("=" * 60)
    
    demonstrate_creation()
    demonstrate_magic_methods()
    demonstrate_properties_and_setters()
    demonstrate_business_methods()
    demonstrate_validation()
    
    print_separator("ИТОГ")
    print("Всего создано автобусов:", Bus.total_buses_created)
    print("Демонстрация завершена!")


if __name__ == "__main__":
    main()