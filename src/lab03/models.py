"""
Модуль с производными классами автобусов и расширенной коллекцией Fleet.
Реализует иерархию наследования от базового класса Bus.
"""

from .base import Bus


class CityBus(Bus):
    """
    Городской автобус.
    
    Дополнительные атрибуты:
        low_floor (bool): Низкопольный ли автобус
        has_air_conditioning (bool): Наличие кондиционера
    """
    
    def __init__(self, route_number, capacity, average_speed, driver_name=None,
                 low_floor=True, has_air_conditioning=False):
        super().__init__(route_number, capacity, average_speed, driver_name)
        self.low_floor = low_floor
        self.has_air_conditioning = has_air_conditioning
    
    def calculate_fare(self, distance=1.0):
        """Стоимость проезда в городском автобусе фиксированная."""
        base_fare = 30.0
        if self.has_air_conditioning:
            base_fare += 5.0
        return base_fare
    
    def display_info(self):
        base_info = super().display_info()
        floor_type = "низкопольный" if self.low_floor else "высокопольный"
        ac = "есть" if self.has_air_conditioning else "нет"
        return f"{base_info} | Тип: городской | Пол: {floor_type} | Кондиционер: {ac}"
    
    def __str__(self):
        base_str = super().__str__()
        floor = "низкопольный" if self.low_floor else "высокопольный"
        ac = "конд." if self.has_air_conditioning else "без конд."
        return f"[City] {base_str} | {floor} | {ac}"


class IntercityBus(Bus):
    """
    Междугородний автобус.
    
    Дополнительные атрибуты:
        has_toilet (bool): Наличие туалета
        wifi_available (bool): Доступен ли Wi-Fi
    """
    
    def __init__(self, route_number, capacity, average_speed, driver_name=None,
                 has_toilet=True, wifi_available=False):
        super().__init__(route_number, capacity, average_speed, driver_name)
        self.has_toilet = has_toilet
        self.wifi_available = wifi_available
    
    def calculate_fare(self, distance):
        """Стоимость проезда зависит от расстояния (руб/км)."""
        rate_per_km = 2.5
        if self.wifi_available:
            rate_per_km += 0.5
        return rate_per_km * distance
    
    def display_info(self):
        base_info = super().display_info()
        toilet = "есть" if self.has_toilet else "нет"
        wifi = "есть" if self.wifi_available else "нет"
        return f"{base_info} | Тип: междугородний | Туалет: {toilet} | Wi-Fi: {wifi}"
    
    def __str__(self):
        base_str = super().__str__()
        toilet = "туалет" if self.has_toilet else "без туалета"
        wifi = "Wi-Fi" if self.wifi_available else "без Wi-Fi"
        return f"[Intercity] {base_str} | {toilet} | {wifi}"


class ElectricBus(Bus):
    """
    Электробус.
    
    Дополнительные атрибуты:
        battery_capacity (float): Ёмкость батареи, кВт·ч
        charging_time (float): Время полной зарядки, часов
    """
    
    def __init__(self, route_number, capacity, average_speed, driver_name=None,
                 battery_capacity=300.0, charging_time=4.0):
        super().__init__(route_number, capacity, average_speed, driver_name)
        self.battery_capacity = battery_capacity
        self.charging_time = charging_time
    
    def calculate_fare(self, distance=1.0):
        """Стоимость проезда в электробусе снижена (экологический тариф)."""
        return 25.0
    
    def calculate_range(self):
        """Примерный запас хода на полной зарядке (км)."""
        # Допустим, расход 1.2 кВт·ч/км
        consumption = 1.2
        return self.battery_capacity / consumption
    
    def display_info(self):
        base_info = super().display_info()
        range_km = self.calculate_range()
        return (f"{base_info} | Тип: электробус | "
                f"Батарея: {self.battery_capacity} кВт·ч | "
                f"Запас хода: ~{range_km:.0f} км")
    
    def __str__(self):
        base_str = super().__str__()
        return f"[Electric] {base_str} | Батарея: {self.battery_capacity} кВт·ч"


class Fleet:
    """
    Расширенный класс-контейнер для управления коллекцией автобусов
    с поддержкой полиморфизма и фильтрации по типам.
    """
    
    def __init__(self):
        self._items = []
    
    def add(self, item):
        if not isinstance(item, Bus):
            raise TypeError(f"Можно добавлять только объекты Bus, получен {type(item).__name__}")
        for existing in self._items:
            if existing == item:
                raise ValueError(f"Автобус маршрута {item.route_number} с вместимостью {item.capacity} уже существует в коллекции")
        self._items.append(item)
        return True
    
    def remove(self, item):
        for i, existing in enumerate(self._items):
            if existing == item:
                del self._items[i]
                return True
        raise ValueError("Автобус не найден в коллекции")
    
    def remove_at(self, index):
        if index < 0 or index >= len(self._items):
            raise IndexError(f"Индекс {index} вне диапазона")
        return self._items.pop(index)
    
    def get_all(self):
        return self._items.copy()
    
    def find_by_route_number(self, route_number):
        return [bus for bus in self._items if bus.route_number == route_number]
    
    def find_by_driver_name(self, driver_name):
        return [bus for bus in self._items if bus.driver_name and driver_name.lower() in bus.driver_name.lower()]
    
    def find_by_capacity_range(self, min_cap, max_cap):
        return [bus for bus in self._items if min_cap <= bus.capacity <= max_cap]
    
    def get_on_route(self):
        new_fleet = Fleet()
        for bus in self._items:
            if bus.is_on_route:
                new_fleet.add(bus)
        return new_fleet
    
    def get_in_depot(self):
        new_fleet = Fleet()
        for bus in self._items:
            if not bus.is_on_route:
                new_fleet.add(bus)
        return new_fleet
    
    def get_by_efficiency(self, rating):
        new_fleet = Fleet()
        for bus in self._items:
            if bus.is_on_route and bus.get_efficiency_rating() == rating:
                new_fleet.add(bus)
        return new_fleet
    
    # Фильтрация по типам (задание на 5)
    def get_city_buses(self):
        """Возвращает список только городских автобусов."""
        return [bus for bus in self._items if isinstance(bus, CityBus)]
    
    def get_intercity_buses(self):
        """Возвращает список только междугородних автобусов."""
        return [bus for bus in self._items if isinstance(bus, IntercityBus)]
    
    def get_electric_buses(self):
        """Возвращает список только электробусов."""
        return [bus for bus in self._items if isinstance(bus, ElectricBus)]
    
    def process_all(self):
        """
        Демонстрация полиморфного поведения: вызов display_info() для всех автобусов.
        """
        for bus in self._items:
            print(bus.display_info())
    
    def sort_by_route_number(self, reverse=False):
        self._items.sort(key=lambda bus: bus.route_number, reverse=reverse)
    
    def sort_by_capacity(self, reverse=False):
        self._items.sort(key=lambda bus: bus.capacity, reverse=reverse)
    
    def sort_by_speed(self, reverse=False):
        self._items.sort(key=lambda bus: bus.average_speed, reverse=reverse)
    
    def sort(self, key=None, reverse=False):
        if key is None:
            self._items.sort(reverse=reverse)
        else:
            self._items.sort(key=key, reverse=reverse)
    
    def __len__(self):
        return len(self._items)
    
    def __iter__(self):
        return iter(self._items)
    
    def __getitem__(self, index):
        if isinstance(index, slice):
            return self._items[index]
        if index < 0:
            index = len(self._items) + index
        if index < 0 or index >= len(self._items):
            raise IndexError(f"Индекс {index} вне диапазона")
        return self._items[index]
    
    def __contains__(self, item):
        for existing in self._items:
            if existing == item:
                return True
        return False
    
    def __str__(self):
        if len(self._items) == 0:
            return "Автопарк: пуст"
        result = f"Автопарк (всего автобусов: {len(self._items)})\n"
        result += "-" * 50 + "\n"
        for i, bus in enumerate(self._items):
            result += f"{i+1}. {bus}\n"
        return result