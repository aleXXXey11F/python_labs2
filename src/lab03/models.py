#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Производные классы для лабораторной работы №3.
CityBus и TouristBus наследуются от базового класса Bus.
"""

from base import Bus


class CityBus(Bus):
    """
    Городской автобус.
    Дополнительные атрибуты: количество остановок, наличие кондиционера.
    """

    def __init__(self, route_number, capacity, average_speed, driver_name,
                 number_of_stops, has_air_conditioning):
        # Вызов конструктора базового класса
        super().__init__(route_number, capacity, average_speed, driver_name)

        # Новые атрибуты
        self._number_of_stops = number_of_stops
        self._has_air_conditioning = has_air_conditioning

    # Геттеры для новых атрибутов
    @property
    def number_of_stops(self):
        return self._number_of_stops

    @property
    def has_air_conditioning(self):
        return self._has_air_conditioning

    # Новый метод
    def calculate_stop_density(self):
        """Плотность остановок (количество остановок на 10 км маршрута)."""
        # Для демонстрации используем фиктивную длину маршрута 20 км
        route_length_km = 20.0
        return (self._number_of_stops / route_length_km) * 10

    # Переопределённый метод базового класса (полиморфизм)
    def calculate_travel_time(self, distance):
        """
        Время в пути с учётом остановок (каждая остановка добавляет 0.5 минуты).
        """
        base_time = super().calculate_travel_time(distance)
        stop_time = self._number_of_stops * 0.5 / 60.0  # минуты → часы
        return base_time + stop_time

    # Переопределение __str__ для демонстрации
    def __str__(self):
        base_str = super().__str__()
        ac_status = "есть кондиционер" if self._has_air_conditioning else "нет кондиционера"
        return f"{base_str} | Остановок: {self._number_of_stops} | {ac_status}"


class TouristBus(Bus):
    """
    Туристический автобус.
    Дополнительные атрибуты: наличие туалета, вместимость багажа.
    """

    def __init__(self, route_number, capacity, average_speed, driver_name,
                 has_toilet, luggage_capacity):
        super().__init__(route_number, capacity, average_speed, driver_name)

        self._has_toilet = has_toilet
        self._luggage_capacity = luggage_capacity

    @property
    def has_toilet(self):
        return self._has_toilet

    @property
    def luggage_capacity(self):
        return self._luggage_capacity

    # Новый метод
    def calculate_comfort_level(self):
        """Уровень комфорта (0-10) на основе наличия туалета и вместимости багажа."""
        level = 5  # базовый уровень
        if self._has_toilet:
            level += 3
        if self._luggage_capacity > 50:
            level += 2
        return min(level, 10)

    # Переопределённый метод базового класса
    def calculate_travel_time(self, distance):
        """
        Для туристического автобуса время увеличивается на 10% из-за более
        спокойного стиля вождения (комфорт важнее скорости).
        """
        base_time = super().calculate_travel_time(distance)
        return base_time * 1.1

    def __str__(self):
        base_str = super().__str__()
        toilet_status = "есть туалет" if self._has_toilet else "нет туалета"
        return f"{base_str} | {toilet_status} | Багаж: {self._luggage_capacity} кг"