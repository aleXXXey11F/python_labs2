# demo.py
"""
Демонстрация лабораторной работы №6.
Показывает работу TypedCollection с аннотациями типов, протоколы Displayable/Scorable.
"""

from container import (
    Bus, CityBus, IntercityBus, ElectricBus,
    TypedCollection,
    Displayable, Scorable, D, S
)


def print_section(title: str) -> None:
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def demo_3() -> None:
    """Задание на 3: базовая типизация и TypedCollection[Bus]."""
    print_section("ЗАДАНИЕ 3: TYPEDCOLLECTION С АННОТАЦИЯМИ ТИПОВ")

    # Создаём типизированную коллекцию с явным указанием параметра типа
    fleet: TypedCollection[Bus] = TypedCollection[Bus]()

    bus1 = CityBus("12", 80, 45, "Иванов", low_floor=True, has_air_conditioning=True)
    bus2 = IntercityBus("М4", 55, 90, "Петров", has_toilet=True, wifi_available=True)
    bus3 = ElectricBus("7", 70, 35, "Сидоров", battery_capacity=250)

    print("Добавляем автобусы:")
    fleet.add(bus1)
    fleet.add(bus2)
    fleet.add(bus3)

    print(f"\nКоличество добавленных: {len(fleet)}")
    print("Содержимое коллекции:")
    print(fleet)

    # Попытка добавить объект не того типа (демонстрация проверки типов)
    print("\nПопытка добавить строку 'NotABus':")
    try:
        fleet.add("NotABus")  # type: ignore
    except (AttributeError, TypeError, ValueError) as e:
        print(f"  Ошибка (ожидаемо): {e}")

    print("\nВывод всех элементов по одному:")
    for bus in fleet.get_all():
        print(f"  {bus}")


def demo_4() -> None:
    """Задание на 4: find, filter, map с разными типами результата."""
    print_section("ЗАДАНИЕ 4: FIND, FILTER, MAP")

    fleet: TypedCollection[Bus] = TypedCollection()
    # Подготовим несколько автобусов
    fleet.add(CityBus("5", 60, 50, "Иванов", low_floor=True))
    fleet.add(CityBus("22", 40, 55, "Петров"))
    fleet.add(IntercityBus("101", 80, 90, "Сидоров", wifi_available=True))
    fleet.add(IntercityBus("202", 65, 85, "Козлов"))
    fleet.add(ElectricBus("10", 50, 40, "Смирнов", battery_capacity=300))

    # ------------------- find -------------------
    print("\n--- find ---")
    # Ищем первый автобус с вместимостью >= 70
    found = fleet.find(lambda b: b.capacity >= 70)
    if found:
        print(f"Найден автобус с вместимостью >=70: {found}")
    else:
        print("Ничего не найдено (не ожидалось)")

    # Ищем несуществующий
    missing = fleet.find(lambda b: b.route_number == "999")
    print(f"Поиск маршрута '999': {missing}")

    # ------------------- filter -------------------
    print("\n--- filter ---")
    big_capacity = fleet.filter(lambda b: b.capacity > 50)
    print("Автобусы с вместимостью > 50:")
    for b in big_capacity:
        print(f"  {b}")

    # ------------------- map (меняет тип) -------------------
    print("\n--- map (изменение типа результата) ---")
    # Преобразуем в список названий маршрутов (list[str])
    route_names: list[str] = fleet.map(lambda b: b.route_number)
    print(f"Номера маршрутов (list[str]): {route_names}")

    # Преобразуем в список средней скорости (list[float])
    speeds: list[float] = fleet.map(lambda b: b.average_speed)
    print(f"Скорости (list[float]): {speeds}")

    # Преобразуем в список словарей с информацией
    info: list[dict] = fleet.map(lambda b: {
        "route": b.route_number,
        "capacity": b.capacity,
        "free": b.free_seats
    })
    print("Словари с информацией:")
    for entry in info:
        print(f"  {entry}")


def demo_5() -> None:
    """Задание на 5: протоколы Displayable и Scorable."""
    print_section("ЗАДАНИЕ 5: ПРОТОКОЛЫ DISPLAYABLE / SCORABLE")

    # Сценарий 1: TypedCollection[D] с объектами разных типов, реализующими display()
    print("\n--- Сценарий 1: коллекция Displayable ---")
    coll_d: TypedCollection[D] = TypedCollection()

    # CityBus и ElectricBus не наследуются от Displayable, но метод display() у них есть
    cb = CityBus("5", 60, 50, "Иванов", low_floor=True, has_air_conditioning=True)
    eb = ElectricBus("10", 50, 40, "Петров", battery_capacity=320)
    # Также можно добавить IntercityBus, у него тоже есть display()
    ib = IntercityBus("М8", 55, 85, "Сидоров")

    coll_d.add(cb)
    coll_d.add(eb)
    coll_d.add(ib)

    print("Содержимое TypedCollection[Displayable]:")
    for item in coll_d.get_all():
        # IDE знает, что у item есть метод display()
        print(f"  {item.display()}")

    # Сценарий 2: TypedCollection[S] с объектами, имеющими score()
    print("\n--- Сценарий 2: коллекция Scorable ---")
    coll_s: TypedCollection[S] = TypedCollection()

    # Добавим пассажиров для демонстрации score
    cb2 = CityBus("22", 40, 55, "Иванов")
    eb2 = ElectricBus("15", 45, 38, "Смирнов", battery_capacity=280)

    # Вручную посадим пассажиров (имитация)
    cb2.start_route()
    for _ in range(15):
        cb2.board_passenger()
    eb2.start_route()
    for _ in range(35):
        eb2.board_passenger()

    coll_s.add(cb2)
    coll_s.add(eb2)

    print("Элементы TypedCollection[Scorable] и их score:")
    for item in coll_s.get_all():
        # Безопасный вызов score() благодаря bound=Scorable
        print(f"  {item}: score = {item.score():.2f}")

    # Дополнительно: демонстрация, что один и тот же TypedCollection работает с разными ограничениями
    print("\n--- Демонстрация: один и тот же класс TypedCollection с разными ограничениями ---")
    print(f"coll_d type: {type(coll_d)}")
    print(f"coll_s type: {type(coll_s)}")
    print("Оба раза использовали TypedCollection, но с разными TypeVar (D и S)")


def main() -> None:
    print("=" * 70)
    print(" ЛАБОРАТОРНАЯ РАБОТА №6: GENERICS И TYPING")
    print(" Тема: Транспорт — аннотации типов, обобщённая коллекция, протоколы")
    print("=" * 70)

    demo_3()
    demo_4()
    demo_5()

    print("\nДемонстрация завершена.")


if __name__ == "__main__":
    main()