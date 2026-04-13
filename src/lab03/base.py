#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Базовый класс Bus для лабораторной работы №3.
Содержит общие атрибуты и методы для всех типов автобусов.
"""

# Функции валидации (вынесены для независимости)
def validate_route_number(route_number):
    if not isinstance(route_number, str):
        raise ValueError("Номер маршрута должен быть строкой")
    if not route_number or route_number.strip() == "":
        raise ValueError("Номер маршрута не может быть пустым")
    return True

def validate_capacity(capacity):
    if not isinstance(capacity, int):
        raise ValueError("Вместимость должна быть целым числом")
    if capacity <= 0:
        raise ValueError("Вместимость должна быть положительным числом")
    if capacity > 100:
        raise ValueError("Вместимость не может превышать 100 пассажиров")
    return True

def validate_speed(speed):
    if not isinstance(speed, (int, float)):
        raise ValueError("Скорость должна быть числом")
    if speed < 10:
        raise ValueError("Скорость не может быть меньше 10 км/ч")
    if speed > 120:
        raise ValueError("Скорость не может превышать 120 км/ч")
    return True

def validate_driver_name(driver_name):
    if driver_name is not None:
        if not isinstance(driver_name, str):
            raise ValueError("Имя водителя должно быть строкой")
        if driver_name.strip() == "":
            raise ValueError("Имя водителя не может быть пустым")
    return True


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

    # Геттеры
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

    # Бизнес-методы
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
        """
        Рассчитать время в пути (в часах) без учёта дополнительных факторов.
        """
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

    # Магические методы
    def __str__(self):
        status = "на маршруте" if self._is_on_route else "в парке"
        driver = self._driver_name if self._driver_name else "не назначен"
        return (f"🚌 {self.vehicle_type} маршрута {self._route_number} | "
                f"Водитель: {driver} | Вместимость: {self._capacity} | "
                f"Пассажиров: {self._current_passengers} | Статус: {status}")

    def __repr__(self):
        return (f"Bus(route_number='{self._route_number}', capacity={self._capacity}, "
                f"average_speed={self._average_speed}, driver_name='{self._driver_name}')")

    def __eq__(self, other):
        if not isinstance(other, Bus):
            return False
        return (self._route_number == other._route_number and
                self._capacity == other._capacity)