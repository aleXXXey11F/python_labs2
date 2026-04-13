#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль с производными классами для лабораторной работы №3.
Содержит дочерние классы от Bus.
"""

from .base import Bus


class CityBus(Bus):
    """
    Городской автобус.
    Дочерний класс от Bus.
    
    Дополнительные атрибуты:
        _route_type (str): Тип маршрута (обычный/экспресс)
        _has_validator (bool): Наличие валидатора/кондуктора
    
    Дополнительные методы:
        get_route_schedule(): Получить расписание маршрута
    """
    
    def __init__(self, route_number, capacity, average_speed, driver_name=None,
                 route_type="обычный", has_validator=True):
        """
        Конструктор класса CityBus.
        
        Args:
            route_number: Номер маршрута
            capacity: Вместимость
            average_speed: Средняя скорость
            driver_name: Имя водителя
            route_type: Тип маршрута (обычный/экспресс)
            has_validator: Наличие валидатора/кондуктора
        """
        # Вызов конструктора базового класса через super()
        super().__init__(route_number, capacity, average_speed, driver_name)
        
        # Новые атрибуты
        self._route_type = route_type
        self._has_validator = has_validator
        
        # Переопределяем атрибут класса для конкретного экземпляра
        self.vehicle_type = "Городской автобус"
    
    # Геттеры для новых атрибутов
    @property
    def route_type(self):
        """Тип маршрута."""
        return self._route_type
    
    @property
    def has_validator(self):
        """Наличие валидатора."""
        return self._has_validator
    
    # Новый метод
    def get_route_schedule(self):
        """
        Получить расписание маршрута.
        
        Returns:
            dict: Словарь с расписанием
        """
        # Симуляция расписания
        return {
            "route": self._route_number,
            "type": self._route_type,
            "interval_minutes": 10 if self._route_type == "обычный" else 20,
            "first_bus": "06:00",
            "last_bus": "23:00"
        }
    
    # Переопределение метода calculate_fare (полиморфизм)
    def calculate_fare(self, distance):
        """
        Расчет стоимости проезда для городского автобуса.
        Городской тариф: фиксированная стоимость + льготы.
        
        Args:
            distance (float): Расстояние в километрах
            
        Returns:
            float: Стоимость проезда
        """
        # Городской тариф: 30 руб фиксированно, не зависит от расстояния
        # Если есть валидатор - можно использовать транспортную карту со скидкой
        base_fare = 30.0
        
        if self._has_validator:
            # Скидка при использовании карты
            return base_fare * 0.8  # 20% скидка
        return base_fare
    
    # Переопределение метода get_info
    def get_info(self):
        """Расширенная информация о городском автобусе."""
        info = super().get_info()
        info.update({
            "route_type": self._route_type,
            "has_validator": self._has_validator,
            "schedule": self.get_route_schedule()
        })
        return info
    
    # Переопределение __str__
    def __str__(self):
        base_str = super().__str__()
        validator_str = "✅ валидатор есть" if self._has_validator else "❌ валидатора нет"
        return f"{base_str} | {validator_str} | Тип: {self._route_type}"


class TouristBus(Bus):
    """
    Туристический автобус.
    Дочерний класс от Bus.
    
    Дополнительные атрибуты:
        _has_wifi (bool): Наличие Wi-Fi
        _has_toilet (bool): Наличие туалета
        _tour_guide_name (str): Имя экскурсовода
    
    Дополнительные методы:
        get_comfort_level(): Получить уровень комфорта
    """
    
    def __init__(self, route_number, capacity, average_speed, driver_name=None,
                 has_wifi=True, has_toilet=True, tour_guide_name=None):
        """
        Конструктор класса TouristBus.
        """
        super().__init__(route_number, capacity, average_speed, driver_name)
        
        # Новые атрибуты
        self._has_wifi = has_wifi
        self._has_toilet = has_toilet
        self._tour_guide_name = tour_guide_name
        
        # Переопределяем атрибут класса
        self.vehicle_type = "Туристический автобус"
    
    # Геттеры
    @property
    def has_wifi(self):
        return self._has_wifi
    
    @property
    def has_toilet(self):
        return self._has_toilet
    
    @property
    def tour_guide_name(self):
        return self._tour_guide_name
    
    # Сеттер для экскурсовода
    @tour_guide_name.setter
    def tour_guide_name(self, name):
        if name is not None and (not isinstance(name, str) or name.strip() == ""):
            raise ValueError("Имя экскурсовода должно быть непустой строкой")
        self._tour_guide_name = name
    
    # Новый метод
    def get_comfort_level(self):
        """
        Получить уровень комфорта туристического автобуса.
        
        Returns:
            str: Уровень комфорта (Люкс/Стандарт/Эконом)
        """
        score = 0
        if self._has_wifi:
            score += 1
        if self._has_toilet:
            score += 1
        if self.capacity <= 30:  # Меньше мест - больше комфорта
            score += 1
        
        if score >= 2:
            return "Люкс"
        elif score == 1:
            return "Стандарт"
        else:
            return "Эконом"
    
    # Переопределение метода calculate_fare (полиморфизм)
    def calculate_fare(self, distance):
        """
        Расчет стоимости проезда для туристического автобуса.
        Туристический тариф: высокая стоимость + доплата за комфорт.
        """
        # Базовая стоимость: 100 руб + 20 руб/км
        base_fare = 100 + distance * 20
        
        # Доплата за комфорт
        comfort_multiplier = 1.0
        if self._has_wifi:
            comfort_multiplier += 0.1
        if self._has_toilet:
            comfort_multiplier += 0.1
        if self.capacity <= 30:
            comfort_multiplier += 0.2
        
        # Если есть экскурсовод - доплата
        if self._tour_guide_name:
            comfort_multiplier += 0.15
        
        return base_fare * comfort_multiplier
    
    # Переопределение метода get_info
    def get_info(self):
        info = super().get_info()
        info.update({
            "has_wifi": self._has_wifi,
            "has_toilet": self._has_toilet,
            "tour_guide": self._tour_guide_name,
            "comfort_level": self.get_comfort_level()
        })
        return info
    
    # Переопределение __str__
    def __str__(self):
        base_str = super().__str__()
        features = []
        if self._has_wifi:
            features.append("WiFi")
        if self._has_toilet:
            features.append("Туалет")
        features_str = ", ".join(features) if features else "нет удобств"
        guide_str = f" | Экскурсовод: {self._tour_guide_name}" if self._tour_guide_name else ""
        return f"{base_str} | Удобства: {features_str}{guide_str} | Комфорт: {self.get_comfort_level()}"


class SchoolBus(Bus):
    """
    Школьный автобус.
    Дочерний класс от Bus.
    
    Дополнительные атрибуты:
        _has_escort (bool): Наличие сопровождающего
        _school_name (str): Название школы
    
    Дополнительные методы:
        get_safety_rating(): Получить рейтинг безопасности
    """
    
    def __init__(self, route_number, capacity, average_speed, driver_name=None,
                 has_escort=True, school_name="МБОУ СОШ №1"):
        """
        Конструктор класса SchoolBus.
        """
        super().__init__(route_number, capacity, average_speed, driver_name)
        
        # Новые атрибуты
        self._has_escort = has_escort
        self._school_name = school_name
        
        # Переопределяем атрибут класса
        self.vehicle_type = "Школьный автобус"
    
    # Геттеры
    @property
    def has_escort(self):
        return self._has_escort
    
    @property
    def school_name(self):
        return self._school_name
    
    # Сеттер
    @school_name.setter
    def school_name(self, name):
        if not isinstance(name, str) or name.strip() == "":
            raise ValueError("Название школы должно быть непустой строкой")
        self._school_name = name
    
    # Новый метод
    def get_safety_rating(self):
        """
        Получить рейтинг безопасности школьного автобуса.
        
        Returns:
            str: Рейтинг безопасности
        """
        rating = 5  # Базовый рейтинг
        
        # Скорость ограничена для безопасности
        if self._average_speed > 60:
            rating -= 2
        
        # Наличие сопровождающего повышает безопасность
        if self._has_escort:
            rating += 1
        
        # Вместительность (чем меньше, тем безопаснее)
        if self._capacity > 40:
            rating -= 1
        
        return f"{rating}/5" if rating > 0 else "1/5"
    
    # Переопределение метода calculate_fare (полиморфизм)
    def calculate_fare(self, distance):
        """
        Расчет стоимости проезда для школьного автобуса.
        Школьный тариф: бесплатно или льготный.
        """
        # Школьные автобусы обычно бесплатные
        return 0.0
    
    # Переопределение метода board_passenger (дополнительная логика)
    def board_passenger(self):
        """
        Посадка пассажира в школьный автобус.
        С дополнительной проверкой безопасности.
        """
        if not self._is_on_route:
            raise ValueError("Нельзя садить пассажиров - автобус не на маршруте")
        
        # Проверка безопасности перед посадкой
        if not self._has_escort and self._current_passengers >= self._capacity * 0.8:
            print("⚠️ Внимание! Нет сопровождающего, посадка ограничена до 80% вместимости")
            if self._current_passengers < self._capacity * 0.8:
                self._current_passengers += 1
                return True
            return False
        
        if self._current_passengers < self._capacity:
            self._current_passengers += 1
            return True
        return False
    
    # Переопределение метода get_info
    def get_info(self):
        info = super().get_info()
        info.update({
            "has_escort": self._has_escort,
            "school_name": self._school_name,
            "safety_rating": self.get_safety_rating()
        })
        return info
    
    # Переопределение __str__
    def __str__(self):
        base_str = super().__str__()
        escort_str = "👨‍🏫 с сопровождающим" if self._has_escort else "⚠️ без сопровождающего"
        return f"{base_str} | {escort_str} | Школа: {self._school_name} | Безопасность: {self.get_safety_rating()}"