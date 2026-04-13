"""
Модуль с базовым классом Bus для лабораторной работы №3.
Является основой для иерархии классов транспортных средств.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lab01.validate as validate


class Bus:
    """
    Базовый класс, представляющий автобус на маршруте.
    
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
        validate.validate_route_number(route_number)
        validate.validate_capacity(capacity)
        validate.validate_speed(average_speed)
        validate.validate_driver_name(driver_name)
        
        self._route_number = route_number
        self._capacity = capacity
        self._average_speed = average_speed
        self._driver_name = driver_name
        self._current_passengers = 0
        self._is_on_route = False
        
        Bus.total_buses_created += 1
    
    @property
    def route_number(self):
        return self._route_number
    
    @property
    def capacity(self):
        return self._capacity
    
    @property
    def average_speed(self):
        return self._average_speed
    
    @property
    def driver_name(self):
        return self._driver_name
    
    @property
    def current_passengers(self):
        return self._current_passengers
    
    @property
    def is_on_route(self):
        return self._is_on_route
    
    @property
    def free_seats(self):
        return self._capacity - self._current_passengers
    
    @driver_name.setter
    def driver_name(self, new_name):
        validate.validate_driver_name(new_name)
        self._driver_name = new_name
    
    def board_passenger(self):
        if not self._is_on_route:
            raise ValueError("Нельзя садить пассажиров - автобус не на маршруте")
        if self._current_passengers < self._capacity:
            self._current_passengers += 1
            return True
        return False
    
    def alight_passenger(self):
        if not self._is_on_route:
            raise ValueError("Нельзя высаживать пассажиров - автобус не на маршруте")
        if self._current_passengers > 0:
            self._current_passengers -= 1
            return True
        return False
    
    def start_route(self):
        if self._driver_name is None:
            raise ValueError("Нельзя отправить автобус без водителя")
        if self._is_on_route:
            raise ValueError("Автобус уже на маршруте")
        self._is_on_route = True
        return True
    
    def end_route(self):
        self._is_on_route = False
        self._current_passengers = 0
        return True
    
    def calculate_travel_time(self, distance):
        if not isinstance(distance, (int, float)) or distance <= 0:
            raise ValueError("Расстояние должно быть положительным числом")
        return distance / self._average_speed
    
    def get_efficiency_rating(self):
        fill_ratio = self._current_passengers / self._capacity if self._capacity > 0 else 0
        if fill_ratio < 0.3:
            return "Низкая загрузка"
        elif fill_ratio < 0.7:
            return "Средняя загрузка"
        else:
            return "Высокая загрузка"
    
    def display_info(self):
        """
        Полиморфный метод для отображения информации об автобусе.
        Будет переопределён в дочерних классах.
        """
        return (f"Тип: {self.vehicle_type} | Маршрут: {self._route_number} | "
                f"Вместимость: {self._capacity} | Скорость: {self._average_speed} км/ч")
    
    def calculate_fare(self, distance=1.0):
        """
        Расчёт стоимости проезда. Базовый метод выбрасывает исключение,
        так как должен быть реализован в дочерних классах.
        """
        raise NotImplementedError("Метод calculate_fare() должен быть реализован в дочернем классе")
    
    def __str__(self):
        status = "на маршруте" if self._is_on_route else "в парке"
        driver = self._driver_name if self._driver_name else "не назначен"
        return (f"Автобус маршрута {self._route_number} | "
                f"Водитель: {driver} | "
                f"Вместимость: {self._capacity} | "
                f"Пассажиров: {self._current_passengers} | "
                f"Статус: {status}")
    
    def __repr__(self):
        return (f"Bus(route_number='{self._route_number}', "
                f"capacity={self._capacity}, "
                f"average_speed={self._average_speed}, "
                f"driver_name='{self._driver_name}')")
    
    def __eq__(self, other):
        if not isinstance(other, Bus):
            return False
        return (self._route_number == other._route_number and 
                self._capacity == other._capacity)