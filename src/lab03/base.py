#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль с базовым классом Bus для лабораторной работы №3.
Наследуется от класса из ЛР-1.
"""

import sys
import os

# Добавляем корневую папку проекта в sys.path для корректного импорта
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.lab01.validate import (
    validate_route_number,
    validate_capacity,
    validate_speed,
    validate_driver_name
)


class Bus:
    """
    Базовый класс, представляющий автобус на маршруте.
    """
    vehicle_type = "Автобус"
    total_buses_created = 0
    
    def __init__(self, route_number, capacity, average_speed, driver_name=None):
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
        validate_driver_name(new_name)
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
        fill_ratio = self._current_passengers / self._capacity
        if fill_ratio < 0.3:
            return "Низкая загрузка"
        elif fill_ratio < 0.7:
            return "Средняя загрузка"
        else:
            return "Высокая загрузка"
    
    def calculate_fare(self, distance):
        # Базовый метод (может быть переопределён)
        return 20 + distance * 10
    
    def get_info(self):
        status = "на маршруте" if self._is_on_route else "в парке"
        return {
            "type": self.vehicle_type,
            "route": self._route_number,
            "capacity": self._capacity,
            "driver": self._driver_name,
            "passengers": self._current_passengers,
            "status": status
        }
    
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