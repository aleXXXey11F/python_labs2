"""
Модуль с классом Bus для лабораторной работы №1.
Демонстрирует принципы ООП: инкапсуляцию, свойства, магические методы.
"""

from . import validate


class Bus:
    """
    Класс, представляющий автобус на маршруте.
    
    Атрибуты класса:
        vehicle_type (str): Тип транспортного средства (общий для всех автобусов)
        total_buses_created (int): Счетчик созданных экземпляров автобусов
    
    Атрибуты экземпляра:
        _route_number (str): Номер маршрута (закрытый)
        _capacity (int): Вместимость автобуса (закрытый)
        _average_speed (float): Средняя скорость (закрытый)
        _driver_name (str): Имя водителя (закрытый)
        _current_passengers (int): Текущее количество пассажиров (закрытый)
        _is_on_route (bool): Статус нахождения на маршруте (закрытый)
    """
    
    # Атрибуты класса
    vehicle_type = "Автобус"
    total_buses_created = 0
    
    def __init__(self, route_number, capacity, average_speed, driver_name=None):
        """
        Конструктор класса Bus.
        
        Args:
            route_number (str): Номер маршрута
            capacity (int): Вместимость автобуса
            average_speed (float): Средняя скорость
            driver_name (str, optional): Имя водителя
            
        Raises:
            ValueError: Если какой-либо параметр не проходит валидацию
        """
        # Валидация входных данных с использованием отдельных методов
        validate.validate_route_number(route_number)
        validate.validate_capacity(capacity)
        validate.validate_speed(average_speed)
        validate.validate_driver_name(driver_name)
        
        # Инициализация закрытых атрибутов
        self._route_number = route_number
        self._capacity = capacity
        self._average_speed = average_speed
        self._driver_name = driver_name
        self._current_passengers = 0  # Изначально пассажиров нет
        self._is_on_route = False  # Автобус не на маршруте
        
        # Увеличиваем счетчик созданных автобусов
        Bus.total_buses_created += 1
    
    # Свойства (геттеры)
    @property
    def route_number(self):
        """Получить номер маршрута."""
        return self._route_number
    
    @property
    def capacity(self):
        """Получить вместимость автобуса."""
        return self._capacity
    
    @property
    def average_speed(self):
        """Получить среднюю скорость."""
        return self._average_speed
    
    @property
    def driver_name(self):
        """Получить имя водителя."""
        return self._driver_name
    
    @property
    def current_passengers(self):
        """Получить текущее количество пассажиров."""
        return self._current_passengers
    
    @property
    def is_on_route(self):
        """Получить статус нахождения на маршруте."""
        return self._is_on_route
    
    @property
    def free_seats(self):
        """Вычисляемое свойство - количество свободных мест."""
        return self._capacity - self._current_passengers
    
    # Сеттер с валидацией
    @driver_name.setter
    def driver_name(self, new_name):
        """
        Сеттер для имени водителя с валидацией.
        
        Args:
            new_name (str): Новое имя водителя
            
        Raises:
            ValueError: Если имя не проходит валидацию
        """
        validate.validate_driver_name(new_name)
        self._driver_name = new_name
    
    # Бизнес-методы
    def board_passenger(self):
        """
        Посадка одного пассажира в автобус.
        
        Returns:
            bool: True если посадка успешна, False если нет мест
            
        Raises:
            ValueError: Если автобус не на маршруте
        """
        if not self._is_on_route:
            raise ValueError("Нельзя садить пассажиров - автобус не на маршруте")
        
        if self._current_passengers < self._capacity:
            self._current_passengers += 1
            return True
        return False
    
    def alight_passenger(self):
        """
        Высадка одного пассажира из автобуса.
        
        Returns:
            bool: True если высадка успешна, False если пассажиров нет
            
        Raises:
            ValueError: Если автобус не на маршруте
        """
        if not self._is_on_route:
            raise ValueError("Нельзя высаживать пассажиров - автобус не на маршруте")
        
        if self._current_passengers > 0:
            self._current_passengers -= 1
            return True
        return False
    
    def start_route(self):
        """
        Отправление автобуса на маршрут.
        
        Returns:
            bool: True если успешно отправлен
            
        Raises:
            ValueError: Если нет водителя или автобус уже на маршруте
        """
        if self._driver_name is None:
            raise ValueError("Нельзя отправить автобус без водителя")
        
        if self._is_on_route:
            raise ValueError("Автобус уже на маршруте")
        
        self._is_on_route = True
        return True
    
    def end_route(self):
        """
        Завершение маршрута.
        
        Returns:
            bool: True если успешно завершен
        """
        self._is_on_route = False
        self._current_passengers = 0  # Все пассажиры выходят
        return True
    
    def calculate_travel_time(self, distance):
        """
        Рассчитать время в пути на заданное расстояние.
        
        Args:
            distance (float): Расстояние в километрах
            
        Returns:
            float: Время в часах
            
        Raises:
            ValueError: Если расстояние некорректно
        """
        if not isinstance(distance, (int, float)) or distance <= 0:
            raise ValueError("Расстояние должно быть положительным числом")
        
        return distance / self._average_speed
    
    def get_efficiency_rating(self):
        """
        Получить рейтинг эффективности автобуса.
        Поведение зависит от состояния объекта.
        
        Returns:
            str: Рейтинг эффективности
        """
        fill_ratio = self._current_passengers / self._capacity
        
        if fill_ratio < 0.3:
            return "Низкая загрузка"
        elif fill_ratio < 0.7:
            return "Средняя загрузка"
        else:
            return "Высокая загрузка"
    
    # Магические методы
    def __str__(self):
        """
        Строковое представление для пользователей.
        """
        status = "на маршруте" if self._is_on_route else "в парке"
        driver = self._driver_name if self._driver_name else "не назначен"
        
        return (f"🚌 Автобус маршрута {self._route_number} | "
                f"Водитель: {driver} | "
                f"Вместимость: {self._capacity} | "
                f"Пассажиров: {self._current_passengers} | "
                f"Статус: {status}")
    
    def __repr__(self):
        """
        Официальное строковое представление для разработчиков.
        """
        return (f"Bus(route_number='{self._route_number}', "
                f"capacity={self._capacity}, "
                f"average_speed={self._average_speed}, "
                f"driver_name='{self._driver_name}')")
    
    def __eq__(self, other):
        """
        Сравнение двух автобусов.
        Автобусы считаются равными, если у них совпадают номер маршрута
        и вместимость (основные характеристики).
        
        Args:
            other: Другой объект для сравнения
            
        Returns:
            bool: True если объекты равны
        """
        if not isinstance(other, Bus):
            return False
        
        return (self._route_number == other._route_number and 
                self._capacity == other._capacity)