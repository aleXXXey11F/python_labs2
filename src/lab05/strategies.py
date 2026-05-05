"""
Модуль стратегий и функций высшего порядка для коллекции транспортных средств.
Включает именованные стратегии сортировки, фильтрации, фабрики функций,
callable-объекты и вспомогательные обработчики.
"""

from lab03.models import CityBus, IntercityBus, ElectricBus


# --------------------------------------------------------------
# Стратегии сортировки (key-функции)
# --------------------------------------------------------------

def by_route_number(bus):
    """Сортировка по номеру маршрута (строковое сравнение)."""
    return bus.route_number


def by_capacity(bus):
    """Сортировка по вместимости автобуса."""
    return bus.capacity


def by_speed(bus):
    """Сортировка по средней скорости."""
    return bus.average_speed


def by_fill_ratio(bus):
    """Сортировка по доле занятых мест (чем выше, тем эффективнее)."""
    return bus.current_passengers / bus.capacity if bus.capacity > 0 else 0


def by_driver_name(bus):
    """Сортировка по имени водителя (None идут в конец)."""
    return (bus.driver_name or "").lower()


# --------------------------------------------------------------
# Функции-фильтры (предикаты)
# --------------------------------------------------------------

def is_city_bus(bus):
    """Предикат: объект является городским автобусом."""
    return isinstance(bus, CityBus)


def is_intercity_bus(bus):
    """Предикат: объект является междугородним автобусом."""
    return isinstance(bus, IntercityBus)


def is_electric_bus(bus):
    """Предикат: объект является электробусом."""
    return isinstance(bus, ElectricBus)


def is_on_route(bus):
    """Предикат: автобус находится на маршруте."""
    return bus.is_on_route


def has_free_seats(bus):
    """Предикат: в автобусе есть свободные места."""
    return bus.free_seats > 0


# --------------------------------------------------------------
# Фабрики функций (замыкания)
# --------------------------------------------------------------

def make_capacity_filter(min_capacity):
    """
    Фабрика предиката: возвращает функцию, проверяющую вместимость >= min_capacity.

    Пример:
        big_buses = filter(make_capacity_filter(50), fleet)
    """
    def filter_fn(bus):
        return bus.capacity >= min_capacity
    return filter_fn


def make_route_filter(route_number):
    """
    Фабрика предиката: возвращает функцию, проверяющую совпадение номера маршрута.

    Пример:
        route_42 = filter(make_route_filter("42"), fleet)
    """
    def filter_fn(bus):
        return bus.route_number == route_number
    return filter_fn


# --------------------------------------------------------------
# Функции для map (преобразование объектов)
# --------------------------------------------------------------

def bus_to_dict(bus):
    """Преобразует объект автобуса в словарь с основными полями."""
    return {
        "type": bus.vehicle_type,
        "route": bus.route_number,
        "capacity": bus.capacity,
        "passengers": bus.current_passengers,
        "status": "on route" if bus.is_on_route else "depot"
    }


def bus_to_summary_string(bus):
    """Возвращает краткое строковое представление автобуса."""
    return f"{bus.vehicle_type} #{bus.route_number} (мест: {bus.capacity}, скорость: {bus.average_speed} км/ч)"


# --------------------------------------------------------------
# Callable-стратегии (паттерн «Стратегия»)
# --------------------------------------------------------------

class DiscountStrategy:
    """
    Стратегия расчёта цены билета со скидкой.
    Не изменяет сам объект, а возвращает пару (старая цена, новая цена).
    """

    def __init__(self, discount_percent):
        """
        Args:
            discount_percent (float): процент скидки (0-100).
        """
        self.discount = discount_percent / 100.0

    def __call__(self, bus):
        """
        Применяет скидку к стоимости проезда (результат calculate_fare).

        Returns:
            dict: информация об автобусе и изменении цены.
        """
        try:
            original = bus.calculate_fare(1.0)   # стандартное расстояние 1 км
        except NotImplementedError:
            original = 0.0
        discounted = original * (1 - self.discount)
        return {
            "route": bus.route_number,
            "original_fare": round(original, 2),
            "discounted_fare": round(discounted, 2),
            "discount": f"{self.discount*100:.0f}%"
        }


class ActivateAllStrategy:
    """
    Стратегия перевода всех автобусов (не на маршруте) в активное состояние.
    При вызове запускает маршрут, если автобус ещё не на маршруте и имеет водителя.
    """

    def __call__(self, bus):
        if not bus.is_on_route and bus.driver_name is not None:
            try:
                bus.start_route()
                return f"{bus.route_number}: отправлен на маршрут"
            except ValueError as e:
                return f"{bus.route_number}: ошибка – {e}"
        else:
            return f"{bus.route_number}: уже на маршруте или нет водителя"


class SortByCapacityCallable:
    """
    Callable-объект, который можно использовать как key-функцию для сортировки по вместимости.
    Демонстрирует, что стратегия может быть callable-объектом, а не только функцией.
    """
    def __call__(self, bus):
        return bus.capacity