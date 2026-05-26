# lab07/cli.py
"""Консольный интерфейс приложения (CLI)."""

from typing import List
from app import App
from models import Bus, ValidationError
from exceptions import DuplicateItemError, ItemNotFoundError


class CLI:
    """Интерактивный интерфейс командной строки."""

    def __init__(self, storage_path: str = "data.json") -> None:
        """Инициализация CLI с созданием объекта App.
        
        Args:
            storage_path: путь к файлу данных.
        """
        self.app: App = App(storage_path)

    # --------------------------------------------------------- вывод меню
    def print_menu(self) -> None:
        """Вывести главное меню."""
        print("\n" + "=" * 40)
        print("  УПРАВЛЕНИЕ АВТОПАРКОМ")
        print("=" * 40)
        print("1. Добавить автобус")
        print("2. Показать все автобусы")
        print("3. Найти автобус по маршруту")
        print("4. Удалить автобус")
        print("5. Фильтрация автобусов")
        print("6. Сортировка автобусов")
        print("0. Выход")
        print("=" * 40)

    # --------------------------------------------------------- ввод с обработкой
    def safe_input_int(self, prompt: str, min_val: int = None, max_val: int = None) -> int:
        """Безопасный ввод целого числа с проверкой диапазона."""
        while True:
            try:
                value = int(input(prompt))
                if (min_val is not None and value < min_val) or (max_val is not None and value > max_val):
                    print(f"Введите число в диапазоне {min_val}–{max_val}")
                    continue
                return value
            except ValueError:
                print("Ошибка: введите целое число")

    def safe_input_float(self, prompt: str, min_val: float = None, max_val: float = None) -> float:
        """Безопасный ввод числа с плавающей точкой."""
        while True:
            try:
                value = float(input(prompt))
                if (min_val is not None and value < min_val) or (max_val is not None and value > max_val):
                    print(f"Введите число в диапазоне {min_val}–{max_val}")
                    continue
                return value
            except ValueError:
                print("Ошибка: введите число")

    def confirm(self, msg: str) -> bool:
        """Запросить подтверждение y/n."""
        while True:
            ans = input(f"{msg} (y/n): ").strip().lower()
            if ans in ('y', 'yes', 'да'):
                return True
            elif ans in ('n', 'no', 'нет'):
                return False
            print("Пожалуйста, ответьте 'y' или 'n'")

    # --------------------------------------------------------- команды меню
    def do_add_bus(self) -> None:
        """Добавление нового автобуса."""
        print("\n--- Добавление автобуса ---")
        print("Типы автобусов: 1 - городской (CityBus)")
        print("                2 - междугородний (IntercityBus)")
        print("                3 - электробус (ElectricBus)")
        type_choice = self.safe_input_int("Выберите тип (1-3): ", 1, 3)
        bus_type = {1: "CityBus", 2: "IntercityBus", 3: "ElectricBus"}[type_choice]

        route = input("Номер маршрута: ").strip()
        capacity = self.safe_input_int("Вместимость (1-100): ", 1, 100)
        speed = self.safe_input_float("Средняя скорость (10-120 км/ч): ", 10.0, 120.0)
        driver = input("Имя водителя (Enter, если нет): ").strip()
        driver = driver if driver else None

        kwargs = {}
        if bus_type == "CityBus":
            low = input("Низкопольный? (y/n, по умолчанию y): ").strip().lower()
            kwargs["low_floor"] = low != 'n'
            ac = input("Кондиционер? (y/n, по умолчанию n): ").strip().lower()
            kwargs["has_air_conditioning"] = ac == 'y'
        elif bus_type == "IntercityBus":
            toilet = input("Туалет? (y/n, по умолчанию y): ").strip().lower()
            kwargs["has_toilet"] = toilet != 'n'
            wifi = input("Wi-Fi? (y/n, по умолчанию n): ").strip().lower()
            kwargs["wifi_available"] = wifi == 'y'
        elif bus_type == "ElectricBus":
            batt = self.safe_input_float("Ёмкость батареи, кВт·ч (по умолчанию 300): ", 10.0, 1000.0)
            kwargs["battery_capacity"] = batt
            charge = self.safe_input_float("Время зарядки, ч (по умолчанию 4): ", 0.5, 24.0)
            kwargs["charging_time"] = charge

        try:
            bus = self.app.add_bus(bus_type, route, capacity, speed, driver, **kwargs)
            print(f"✅ Автобус добавлен: {bus}")
        except DuplicateItemError as e:
            print(f"❌ Ошибка: {e}")
        except ValidationError as e:
            print(f"❌ Ошибка валидации: {e}")

    def do_show_all(self) -> None:
        """Вывод всех автобусов."""
        buses = self.app.get_all_buses()
        if not buses:
            print("\n📭 Автопарк пуст.")
            return
        print("\n--- Список автобусов ---")
        for i, bus in enumerate(buses, 1):
            print(f"{i:2d}. {bus}")

    def do_find(self) -> None:
        """Поиск автобуса по номеру маршрута."""
        route = input("\nВведите номер маршрута для поиска: ").strip()
        bus = self.app.find_bus_by_route(route)
        if bus:
            print(f"🔍 Найден: {bus}")
        else:
            print(f"❌ Автобус маршрута '{route}' не найден.")

    def do_delete(self) -> None:
        """Удаление автобуса."""
        route = input("\nВведите номер маршрута для удаления: ").strip()
        bus = self.app.find_bus_by_route(route)
        if not bus:
            print(f"❌ Автобус маршрута '{route}' не найден.")
            return
        print(f"Найден: {bus}")
        if not self.confirm("Удалить этот автобус?"):
            print("Удаление отменено.")
            return
        try:
            self.app.remove_bus_by_route(route)
            print("✅ Автобус удалён.")
        except ItemNotFoundError:
            print("❌ Автобус не найден (возможно, уже удалён).")

    def do_filter(self) -> None:
        """Фильтрация автобусов."""
        print("\n--- Фильтрация ---")
        print("1. По типу (городской/междугородний/электробус)")
        print("2. По диапазону вместимости")
        print("3. По статусу (на маршруте / в парке)")
        choice = self.safe_input_int("Выберите фильтр: ", 1, 3)

        if choice == 1:
            print("  1 - Городской, 2 - Междугородний, 3 - Электробус")
            t = self.safe_input_int("Тип: ", 1, 3)
            if t == 1:
                buses = self.app.filter_buses(lambda b: isinstance(b, __import__('models', fromlist=['CityBus']).CityBus))
            elif t == 2:
                buses = self.app.filter_buses(lambda b: isinstance(b, __import__('models', fromlist=['IntercityBus']).IntercityBus))
            else:
                buses = self.app.filter_buses(lambda b: isinstance(b, __import__('models', fromlist=['ElectricBus']).ElectricBus))
            self._print_buses(buses, "Результат фильтрации по типу")
        elif choice == 2:
            min_c = self.safe_input_int("Минимальная вместимость: ", 1, 100)
            max_c = self.safe_input_int("Максимальная вместимость: ", min_c, 100)
            buses = self.app.filter_buses(lambda b: min_c <= b.capacity <= max_c)
            self._print_buses(buses, f"Автобусы с вместимостью {min_c}–{max_c}")
        elif choice == 3:
            print("  1 - На маршруте, 2 - В парке")
            s = self.safe_input_int("Статус: ", 1, 2)
            if s == 1:
                buses = self.app.filter_buses(lambda b: b.is_on_route)
            else:
                buses = self.app.filter_buses(lambda b: not b.is_on_route)
            self._print_buses(buses, "Результат фильтрации по статусу")

    def do_sort(self) -> None:
        """Сортировка коллекции."""
        print("\n--- Сортировка ---")
        print("1. По номеру маршрута")
        print("2. По вместимости")
        print("3. По средней скорости")
        print("4. По дате добавления")
        choice = self.safe_input_int("Выберите поле сортировки: ", 1, 4)
        print("Порядок: 1 - по возрастанию, 2 - по убыванию")
        order = self.safe_input_int("Выберите порядок: ", 1, 2)
        reverse = order == 2

        from app import App  # уже импортирован
        if choice == 1:
            key = App.key_by_route
        elif choice == 2:
            key = App.key_by_capacity
        elif choice == 3:
            key = App.key_by_speed
        else:
            key = App.key_by_created

        self.app.sort_buses(key, reverse=reverse)
        print("✅ Коллекция отсортирована.")
        self.do_show_all()

    def _print_buses(self, buses: List[Bus], title: str = "") -> None:
        """Вывести список автобусов с заголовком."""
        if title:
            print(f"\n{title}:")
        if not buses:
            print("  (нет результатов)")
            return
        for i, bus in enumerate(buses, 1):
            print(f"  {i}. {bus}")

    # --------------------------------------------------------- главный цикл
    def run(self) -> None:
        """Запуск основного цикла меню."""
        print("=" * 40)
        print("  ДОБРО ПОЖАЛОВАТЬ В СИСТЕМУ УПРАВЛЕНИЯ АВТОПАРКОМ")
        print("=" * 40)
        while True:
            self.print_menu()
            choice = self.safe_input_int("Выберите пункт меню: ", 0, 6)

            if choice == 0:
                print("Сохраняем данные и выходим...")
                self.app.shutdown()
                print("До свидания!")
                break
            elif choice == 1:
                self.do_add_bus()
            elif choice == 2:
                self.do_show_all()
            elif choice == 3:
                self.do_find()
            elif choice == 4:
                self.do_delete()
            elif choice == 5:
                self.do_filter()
            elif choice == 6:
                self.do_sort()