#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.lab03.base import Bus


class CityBus(Bus):
    def __init__(self, route_number, capacity, average_speed, driver_name=None,
                 route_type="обычный", has_validator=True):
        super().__init__(route_number, capacity, average_speed, driver_name)
        self._route_type = route_type
        self._has_validator = has_validator
        self.vehicle_type = "Городской автобус"
    
    @property
    def route_type(self):
        return self._route_type
    
    @property
    def has_validator(self):
        return self._has_validator
    
    def get_route_schedule(self):
        return {
            "route": self._route_number,
            "type": self._route_type,
            "interval_minutes": 10 if self._route_type == "обычный" else 20,
            "first_bus": "06:00",
            "last_bus": "23:00"
        }
    
    def calculate_fare(self, distance):
        base_fare = 30.0
        if self._has_validator:
            return base_fare * 0.8
        return base_fare
    
    def get_info(self):
        info = super().get_info()
        info.update({
            "route_type": self._route_type,
            "has_validator": self._has_validator,
            "schedule": self.get_route_schedule()
        })
        return info
    
    def __str__(self):
        base_str = super().__str__()
        validator_str = "✅ валидатор есть" if self._has_validator else "❌ валидатора нет"
        return f"{base_str} | {validator_str} | Тип: {self._route_type}"


class TouristBus(Bus):
    def __init__(self, route_number, capacity, average_speed, driver_name=None,
                 has_wifi=True, has_toilet=True, tour_guide_name=None):
        super().__init__(route_number, capacity, average_speed, driver_name)
        self._has_wifi = has_wifi
        self._has_toilet = has_toilet
        self._tour_guide_name = tour_guide_name
        self.vehicle_type = "Туристический автобус"
    
    @property
    def has_wifi(self):
        return self._has_wifi
    
    @property
    def has_toilet(self):
        return self._has_toilet
    
    @property
    def tour_guide_name(self):
        return self._tour_guide_name
    
    @tour_guide_name.setter
    def tour_guide_name(self, name):
        if name is not None and (not isinstance(name, str) or name.strip() == ""):
            raise ValueError("Имя экскурсовода должно быть непустой строкой")
        self._tour_guide_name = name
    
    def get_comfort_level(self):
        score = 0
        if self._has_wifi:
            score += 1
        if self._has_toilet:
            score += 1
        if self.capacity <= 30:
            score += 1
        if score >= 2:
            return "Люкс"
        elif score == 1:
            return "Стандарт"
        else:
            return "Эконом"
    
    def calculate_fare(self, distance):
        base_fare = 100 + distance * 20
        comfort_multiplier = 1.0
        if self._has_wifi:
            comfort_multiplier += 0.1
        if self._has_toilet:
            comfort_multiplier += 0.1
        if self.capacity <= 30:
            comfort_multiplier += 0.2
        if self._tour_guide_name:
            comfort_multiplier += 0.15
        return base_fare * comfort_multiplier
    
    def get_info(self):
        info = super().get_info()
        info.update({
            "has_wifi": self._has_wifi,
            "has_toilet": self._has_toilet,
            "tour_guide": self._tour_guide_name,
            "comfort_level": self.get_comfort_level()
        })
        return info
    
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
    def __init__(self, route_number, capacity, average_speed, driver_name=None,
                 has_escort=True, school_name="МБОУ СОШ №1"):
        super().__init__(route_number, capacity, average_speed, driver_name)
        self._has_escort = has_escort
        self._school_name = school_name
        self.vehicle_type = "Школьный автобус"
    
    @property
    def has_escort(self):
        return self._has_escort
    
    @property
    def school_name(self):
        return self._school_name
    
    @school_name.setter
    def school_name(self, name):
        if not isinstance(name, str) or name.strip() == "":
            raise ValueError("Название школы должно быть непустой строкой")
        self._school_name = name
    
    def get_safety_rating(self):
        rating = 5
        if self._average_speed > 60:
            rating -= 2
        if self._has_escort:
            rating += 1
        if self._capacity > 40:
            rating -= 1
        return f"{rating}/5" if rating > 0 else "1/5"
    
    def calculate_fare(self, distance):
        return 0.0
    
    def board_passenger(self):
        if not self._is_on_route:
            raise ValueError("Нельзя садить пассажиров - автобус не на маршруте")
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
    
    def get_info(self):
        info = super().get_info()
        info.update({
            "has_escort": self._has_escort,
            "school_name": self._school_name,
            "safety_rating": self.get_safety_rating()
        })
        return info
    
    def __str__(self):
        base_str = super().__str__()
        escort_str = "👨‍🏫 с сопровождающим" if self._has_escort else "⚠️ без сопровождающего"
        return f"{base_str} | {escort_str} | Школа: {self._school_name} | Безопасность: {self.get_safety_rating()}"