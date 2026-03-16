"""
Модуль для валидации данных автобуса.
Содержит отдельные методы проверки для каждого атрибута.
"""

def validate_route_number(route_number):
    """
    Проверяет корректность номера маршрута.
    Номер маршрута должен быть непустой строкой.
    
    Args:
        route_number: Проверяемое значение
        
    Returns:
        bool: True если валидация пройдена
        
    Raises:
        ValueError: Если значение не проходит валидацию
    """
    if not isinstance(route_number, str):
        raise ValueError("Номер маршрута должен быть строкой")
    if not route_number or route_number.strip() == "":
        raise ValueError("Номер маршрута не может быть пустым")
    return True


def validate_capacity(capacity):
    """
    Проверяет корректность вместимости автобуса.
    Вместимость должна быть целым положительным числом до 100.
    
    Args:
        capacity: Проверяемое значение
        
    Returns:
        bool: True если валидация пройдена
        
    Raises:
        ValueError: Если значение не проходит валидацию
    """
    if not isinstance(capacity, int):
        raise ValueError("Вместимость должна быть целым числом")
    if capacity <= 0:
        raise ValueError("Вместимость должна быть положительным числом")
    if capacity > 100:
        raise ValueError("Вместимость не может превышать 100 пассажиров")
    return True


def validate_speed(speed):
    """
    Проверяет корректность средней скорости автобуса.
    Скорость должна быть числом от 10 до 120 км/ч.
    
    Args:
        speed: Проверяемое значение
        
    Returns:
        bool: True если валидация пройдена
        
    Raises:
        ValueError: Если значение не проходит валидацию
    """
    if not isinstance(speed, (int, float)):
        raise ValueError("Скорость должна быть числом")
    if speed < 10:
        raise ValueError("Скорость не может быть меньше 10 км/ч")
    if speed > 120:
        raise ValueError("Скорость не может превышать 120 км/ч")
    return True


def validate_driver_name(driver_name):
    """
    Проверяет корректность имени водителя.
    Имя должно быть непустой строкой.
    
    Args:
        driver_name: Проверяемое значение
        
    Returns:
        bool: True если валидация пройдена
        
    Raises:
        ValueError: Если значение не проходит валидацию
    """
    if driver_name is not None:
        if not isinstance(driver_name, str):
            raise ValueError("Имя водителя должно быть строкой")
        if driver_name.strip() == "":
            raise ValueError("Имя водителя не может быть пустым")
    return True


def validate_current_passengers(current_passengers, capacity):
    """
    Проверяет корректность количества текущих пассажиров.
    Количество должно быть неотрицательным и не превышать вместимость.
    
    Args:
        current_passengers: Проверяемое значение
        capacity: Вместимость автобуса
        
    Returns:
        bool: True если валидация пройдена
        
    Raises:
        ValueError: Если значение не проходит валидацию
    """
    if not isinstance(current_passengers, int):
        raise ValueError("Количество пассажиров должно быть целым числом")
    if current_passengers < 0:
        raise ValueError("Количество пассажиров не может быть отрицательным")
    if current_passengers > capacity:
        raise ValueError(f"Количество пассажиров не может превышать вместимость ({capacity})")
    return True