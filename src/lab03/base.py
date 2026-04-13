#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль с базовым классом Bus для лабораторной работы №3.
Наследуется от класса из ЛР-1.
"""

import sys
import os

# Добавляем пути для импорта модулей из ЛР-1
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from lab01.validate import (
    validate_route_number,
    validate_capacity,
    validate_speed,
    validate_driver_name
)


class Bus:
    """
    Базовый класс, представляющий автобус на маршруте.
    
    Атрибуты класса:
        vehicle_type (str): Тип транспортного средства
        total_buses_created (int): Счетчик созданных экземпляров
    
    Атрибуты экземпляра:
        _route_number (str): Номер маршрута
        _capacity (int): Вместимость автобуса
        _average_speed (float): Средняя скорость
        _driver_name (str): Имя водителя
        _current_passengers (int): Текущее количество пассажиров
        _is_on_route (bool): Статус нахождения на маршруте
    """
    
    vehicle_type = "Автобус"
    total_buses_created = 0
    
    def __init__(self, route_number, capacity, average_speed, driver_name=None):
        """Конструктор базового класса Bus."""
        validate_route_number(route_number)
        validate_capacity(capacity)
        validate_speed(average_speed)
        validate_driver_name(driver_name)
        
        self._route_number = route_number
        self._capacity = capacity
        self._average_speed = average_speed
        self._driver_name = driver_name
        self._current_passengers = 0
        self._is_on_route = False
        
        Bus.total_buses_created += 1
    
    # Свойства (геттеры)
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
    
    # Сеттер с валидацией
    @driver_name.setter
    def driver_name(self, new_name):
        validate_driver_name(new_name)
        self._driver_name = new_name
    
    # Бизнес-методы
    def board_passenger(self):
        """Посадка одного пассажира."""
        if not self._is_on_route:
            raise ValueError("Нельзя садить пассажиров - автобус не на маршруте")
        
        if self._current_passengers < self._capacity:
            self._current_passengers += 1
            return True
        return False
    
    def alight_passenger(self):
        """Высадка одного пассажира."""
        if not self._is_on_route:
            raise ValueError("Нельзя высаживать пассажиров - автобус не на маршруте")
        
        if self._current_passengers > 0:
            self._current_passengers -= 1
            return True
        return False
    
    def start_route(self):
        """Отправление автобуса на маршрут."""
        if self._driver_name is None:
            raise ValueError("Нельзя отправить автобус без водителя")
        
        if self._is_on_route:
            raise ValueError("Автобус уже на маршруте")
        
        self._is_on_route = True
        return True
    
    def end_route(self):
        """Завершение маршрута."""
        self._is_on_route = False
        self._current_passengers = 0
        return True
    
    def calculate_travel_time(self, distance):
        """Рассчитать время в пути."""
        if not isinstance(distance, (int, float)) or distance <= 0:
            raise ValueError("Расстояние должно быть положительным числом")
        return distance / self._average_speed
    
    def get_efficiency_rating(self):
        """Получить рейтинг эффективности."""
        fill_ratio = self._current_passengers / self._capacity
        
        if fill_ratio < 0.3:
            return "Низкая загрузка"
        elif fill_ratio < 0.7:
            return "Средняя загрузка"
        else:
            return "Высокая загрузка"
    
    # Полиморфный метод (будет переопределен в дочерних классах)
    def calculate_fare(self, distance):
        """
        Расчет стоимости проезда.
        Базовый метод - будет переопределен в дочерних классах.
        
        Args:
            distance (float): Расстояние в километрах
            
        Returns:
            float: Стоимость проезда
        """
        # Базовая формула: 20 руб + 10 руб/км
        return 20 + distance * 10
    
    # Общий интерфейс для полиморфизма
    def get_info(self):
        """
        Получить информацию об автобусе.
        Базовый метод - может быть переопределен.
        """
        status = "на маршруте" if self._is_on_route else "в парке"
        return {
            "type": self.vehicle_type,
            "route": self._route_number,
            "capacity": self._capacity,
            "driver": self._driver_name,
            "passengers": self._current_passengers,
            "status": status
        }
    
    # Магические методы
    def __str__(self):
        status = "на маршруте" if self._is_on_route else "в парке"
        driver = self._driver_name if self._driver_name else "не назначен"
        
        return (f"🚌 {self.vehicle_type} маршрута {self._route_number} | "
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