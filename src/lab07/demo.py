# lab07/demo.py
"""
Автоматическая демонстрация работы приложения (без участия пользователя).
Демонстрирует все четыре сценария, описанные в задании на оценку 5.
Запустите: python demo.py
"""

import os
import sys

# Добавляем родительскую директорию в путь (если нужно)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import App
from models import Bus, CityBus, IntercityBus, ElectricBus
from exceptions import DuplicateItemError, ItemNotFoundError


def print_separator(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_buses(buses, title=None):
    if title:
        print(f"\n{title}:")
    if not buses:
        print("  (пусто)")
    for i, bus in enumerate(buses, 1):
        print(f"  {i}. {bus}")


def scenario_1():
    """Сценарий 1: запуск → автозагрузка → вывод коллекции."""
    print_separator("СЦЕНАРИЙ 1: АВТОЗАГРУЗКА ДАННЫХ")
    
    # Создаём экземпляр App с временным файлом
    app = App("demo_data.json")
    print("Начальное состояние (должно быть пусто):")
    print_buses(app.get_all_buses(), "Автобусы после загрузки")

    # Добавляем несколько автобусов
    print("\nДобавляем автобусы...")
    app.add_bus("CityBus", "5", 50, 60.5, "Иванов",
                low_floor=True, has_air_conditioning=True)
    app.add_bus("IntercityBus", "101", 80, 90.0, "Петров",
                has_toilet=True, wifi_available=True)
    app.add_bus("ElectricBus", "E1", 40, 55.0, "Сидоров",
                battery_capacity=350.0)

    print_buses(app.get_all_buses(), "После добавления трёх автобусов")
    
    # Сохраняем и завершаем сессию
    app.shutdown()
    print("\nДанные сохранены в demo_data.json. Завершаем сессию.")

    # Имитация перезапуска: новый объект App с тем же файлом
    print("\nПерезапуск приложения...")
    app2 = App("demo_data.json")
    print_buses(app2.get_all_buses(), "Автобусы после перезагрузки из файла")

    # Очищаем временный файл в конце сценария (опционально, для демонстрации оставим)
    return app2  # передадим в следующий сценарий


def scenario_2(app: App):
    """Сценарий 2: добавление, удаление с подтверждением, выход → повторный запуск."""
    print_separator("СЦЕНАРИЙ 2: ДОБАВЛЕНИЕ, УДАЛЕНИЕ, СОХРАНЕНИЕ")

    # Добавим новый автобус
    print("\nДобавляем междугородний автобус маршрута '202'")
    app.add_bus("IntercityBus", "202", 65, 85.0, "Кузнецов",
                has_toilet=True, wifi_available=True)
    print_buses(app.get_all_buses(), "После добавления")

    # Удалим автобус '101' (с имитацией подтверждения)
    route_to_delete = "101"
    print(f"\nУдаляем автобус маршрута '{route_to_delete}'...")
    bus = app.find_bus_by_route(route_to_delete)
    if bus:
        print(f"  Найден: {bus}")
        # Имитация подтверждения (в demo просто удаляем)
        removed = app.remove_bus_by_route(route_to_delete)
        print(f"  Удалён: {removed}")
    else:
        print(f"  Автобус маршрута '{route_to_delete}' не найден.")
    
    print_buses(app.get_all_buses(), "После удаления")
    
    # Сохраняем и выходим
    app.shutdown()
    print("\nДанные сохранены. Выход.")

    # Перезапуск
    print("\nПерезапуск приложения...")
    app_new = App("demo_data.json")
    print_buses(app_new.get_all_buses(), "После перезагрузки (автобус 101 должен отсутствовать)")
    return app_new


def scenario_3(app: App):
    """Сценарий 3: сортировка с выбором стратегии."""
    print_separator("СЦЕНАРИЙ 3: СОРТИРОВКА")
    print("Исходный порядок:")
    print_buses(app.get_all_buses())

    # Сортировка по номеру маршрута (возрастание)
    app.sort_buses(App.key_by_route)
    print_buses(app.get_all_buses(), "Сортировка по номеру маршрута (возр.)")

    # Сортировка по вместимости (убывание)
    app.sort_buses(App.key_by_capacity, reverse=True)
    print_buses(app.get_all_buses(), "Сортировка по вместимости (убыв.)")

    # Сортировка по скорости (возрастание)
    app.sort_buses(App.key_by_speed)
    print_buses(app.get_all_buses(), "Сортировка по скорости (возр.)")

    # Сортировка по дате добавления (возрастание)
    app.sort_buses(App.key_by_created)
    print_buses(app.get_all_buses(), "Сортировка по дате добавления (возр.)")


def scenario_4(app: App):
    """Сценарий 4: фильтрация и перехват исключений."""
    print_separator("СЦЕНАРИЙ 4: ФИЛЬТРАЦИЯ И ОБРАБОТКА ОШИБОК")
    print("Исходная коллекция:")
    print_buses(app.get_all_buses())

    # Фильтрация: только городские автобусы
    city = app.filter_buses(lambda b: isinstance(b, CityBus))
    print_buses(city, "Городские автобусы")

    # Фильтрация: вместимость >= 60
    big = app.filter_buses(lambda b: b.capacity >= 60)
    print_buses(big, "Автобусы с вместимостью >= 60")

    # Фильтрация: на маршруте (никого не отправляли, будет пусто)
    on_route = app.filter_buses(lambda b: b.is_on_route)
    print_buses(on_route, "Автобусы на маршруте (должно быть пусто)")

    # Попытка добавить дубликат
    print("\nПопытка добавить дубликат (маршрут '5' вместимость 50)...")
    try:
        app.add_bus("CityBus", "5", 50, 55.0, "Другой водитель")
    except DuplicateItemError as e:
        print(f"  Перехвачено исключение: {e}")

    # Попытка удалить несуществующий автобус
    print("\nПопытка удалить несуществующий автобус (маршрут '999')...")
    try:
        app.remove_bus_by_route("999")
    except ItemNotFoundError as e:
        print(f"  Перехвачено исключение: {e}")


def main():
    print("=" * 70)
    print(" ДЕМОНСТРАЦИЯ ЛАБОРАТОРНОЙ РАБОТЫ №7 (АВТОМАТИЧЕСКАЯ)")
    print("=" * 70)

    # Удалим demo_data.json, если остался с предыдущего запуска
    if os.path.exists("demo_data.json"):
        os.remove("demo_data.json")
        print("Удалён старый demo_data.json")

    app = scenario_1()          # теперь app содержит загруженные данные
    app = scenario_2(app)       # обновлённый app после перезапуска
    scenario_3(app)
    scenario_4(app)

    print("\n" + "=" * 70)
    print(" ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("=" * 70)
    # Оставляем файл demo_data.json для проверки
    print(f"Файл demo_data.json оставлен в папке {os.getcwd()}")


if __name__ == "__main__":
    main()