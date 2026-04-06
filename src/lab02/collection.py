#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль с классом Fleet для лабораторной работы №2.
Реализует контейнер для хранения объектов Bus.
"""

from model import Bus


class Fleet:
    """
    Класс-контейнер для управления коллекцией автобусов.
    
    Атрибуты:
        _items (list): Внутренний список для хранения объектов Bus
    
    Методы:
        add(item) - добавить автобус
        remove(item) - удалить автобус
        remove_at(index) - удалить по индексу
        get_all() - получить список всех автобусов
        find_by_route_number(route_number) - поиск по номеру маршрута
        find_by_driver_name(driver_name) - поиск по имени водителя
        find_by_capacity_range(min_cap, max_cap) - поиск по диапазону вместимости
        get_on_route() - получить автобусы на маршруте
        get_in_depot() - получить автобусы в парке
        sort_by_route_number() - сортировка по номеру маршрута
        sort_by_capacity() - сортировка по вместимости
        sort_by_speed() - сортировка по скорости
        sort(key) - универсальная сортировка
        __len__() - получение количества автобусов
        __iter__() - итерация по автобусам
        __getitem__(index) - доступ по индексу
        __contains__(item) - проверка наличия автобуса
    """
    
    def __init__(self):
        """Конструктор класса Fleet. Создает пустую коллекцию."""
        self._items = []
    
    def add(self, item):
        """
        Добавить автобус в коллекцию.
        
        Args:
            item (Bus): Объект автобуса для добавления
            
        Raises:
            TypeError: Если добавляемый объект не является экземпляром Bus
            ValueError: Если автобус с таким маршрутом и вместимостью уже существует
            
        Returns:
            bool: True если добавление успешно
        """
        # Проверка типа
        if not isinstance(item, Bus):
            raise TypeError(f"Можно добавлять только объекты Bus, получен {type(item).__name__}")
        
        # Проверка на дубликат (по маршруту и вместимости, как в __eq__ класса Bus)
        for existing in self._items:
            if existing == item:
                raise ValueError(f"Автобус маршрута {item.route_number} с вместимостью {item.capacity} уже существует в коллекции")
        
        self._items.append(item)
        return True
    
    def remove(self, item):
        """
        Удалить автобус из коллекции.
        
        Args:
            item (Bus): Объект автобуса для удаления
            
        Raises:
            ValueError: Если автобус не найден в коллекции
            
        Returns:
            bool: True если удаление успешно
        """
        for i, existing in enumerate(self._items):
            if existing == item:
                del self._items[i]
                return True
        
        raise ValueError("Автобус не найден в коллекции")
    
    def remove_at(self, index):
        """
        Удалить автобус по индексу.
        
        Args:
            index (int): Индекс удаляемого автобуса
            
        Raises:
            IndexError: Если индекс выходит за пределы коллекции
            
        Returns:
            Bus: Удаленный автобус
        """
        if index < 0 or index >= len(self._items):
            raise IndexError(f"Индекс {index} вне диапазона (0-{len(self._items)-1})")
        
        return self._items.pop(index)
    
    def get_all(self):
        """
        Получить список всех автобусов в коллекции.
        
        Returns:
            list: Копия внутреннего списка автобусов
        """
        return self._items.copy()
    
    def find_by_route_number(self, route_number):
        """
        Найти автобусы по номеру маршрута.
        
        Args:
            route_number (str): Номер маршрута для поиска
            
        Returns:
            list: Список автобусов с указанным номером маршрута
        """
        return [bus for bus in self._items if bus.route_number == route_number]
    
    def find_by_driver_name(self, driver_name):
        """
        Найти автобусы по имени водителя (частичное совпадение).
        
        Args:
            driver_name (str): Имя водителя для поиска
            
        Returns:
            list: Список автобусов с указанным водителем
        """
        return [bus for bus in self._items if bus.driver_name and driver_name.lower() in bus.driver_name.lower()]
    
    def find_by_capacity_range(self, min_cap, max_cap):
        """
        Найти автобусы в заданном диапазоне вместимости.
        
        Args:
            min_cap (int): Минимальная вместимость
            max_cap (int): Максимальная вместимость
            
        Returns:
            list: Список автобусов в указанном диапазоне
        """
        return [bus for bus in self._items if min_cap <= bus.capacity <= max_cap]
    
    def get_on_route(self):
        """
        Получить автобусы, находящиеся на маршруте.
        
        Returns:
            Fleet: Новая коллекция с автобусами на маршруте
        """
        new_fleet = Fleet()
        for bus in self._items:
            if bus.is_on_route:
                new_fleet.add(bus)
        return new_fleet
    
    def get_in_depot(self):
        """
        Получить автобусы, находящиеся в парке.
        
        Returns:
            Fleet: Новая коллекция с автобусами в парке
        """
        new_fleet = Fleet()
        for bus in self._items:
            if not bus.is_on_route:
                new_fleet.add(bus)
        return new_fleet
    
    def get_by_efficiency(self, rating):
        """
        Получить автобусы с заданным рейтингом эффективности.
        
        Args:
            rating (str): Рейтинг ("Низкая загрузка", "Средняя загрузка", "Высокая загрузка")
            
        Returns:
            Fleet: Новая коллекция с автобусами указанного рейтинга
        """
        new_fleet = Fleet()
        for bus in self._items:
            if bus.is_on_route and bus.get_efficiency_rating() == rating:
                new_fleet.add(bus)
        return new_fleet
    
    def sort_by_route_number(self, reverse=False):
        """
        Сортировка коллекции по номеру маршрута.
        
        Args:
            reverse (bool): Если True, сортировка в обратном порядке
        """
        self._items.sort(key=lambda bus: bus.route_number, reverse=reverse)
    
    def sort_by_capacity(self, reverse=False):
        """
        Сортировка коллекции по вместимости.
        
        Args:
            reverse (bool): Если True, сортировка в обратном порядке
        """
        self._items.sort(key=lambda bus: bus.capacity, reverse=reverse)
    
    def sort_by_speed(self, reverse=False):
        """
        Сортировка коллекции по средней скорости.
        
        Args:
            reverse (bool): Если True, сортировка в обратном порядке
        """
        self._items.sort(key=lambda bus: bus.average_speed, reverse=reverse)
    
    def sort(self, key=None, reverse=False):
        """
        Универсальная сортировка коллекции.
        
        Args:
            key: Функция для получения ключа сортировки
            reverse (bool): Если True, сортировка в обратном порядке
        """
        if key is None:
            self._items.sort(reverse=reverse)
        else:
            self._items.sort(key=key, reverse=reverse)
    
    # Магические методы
    def __len__(self):
        """
        Возвращает количество автобусов в коллекции.
        
        Returns:
            int: Количество автобусов
        """
        return len(self._items)
    
    def __iter__(self):
        """
        Возвращает итератор для обхода коллекции.
        
        Returns:
            iterator: Итератор по автобусам
        """
        return iter(self._items)
    
    def __getitem__(self, index):
        """
        Доступ к автобусу по индексу.
        
        Args:
            index (int): Индекс автобуса (поддерживает отрицательные индексы)
            
        Returns:
            Bus: Автобус по указанному индексу
            
        Raises:
            IndexError: Если индекс выходит за пределы
        """
        if isinstance(index, slice):
            return self._items[index]
        
        # Преобразуем отрицательный индекс в положительный
        if index < 0:
            index = len(self._items) + index
        
        if index < 0 or index >= len(self._items):
            raise IndexError(f"Индекс {index} вне диапазона (0-{len(self._items)-1})")
        
        return self._items[index]
    
    def __contains__(self, item):
        """
        Проверка наличия автобуса в коллекции.
        
        Args:
            item (Bus): Автобус для проверки
            
        Returns:
            bool: True если автобус есть в коллекции
        """
        for existing in self._items:
            if existing == item:
                return True
        return False
    
    def __str__(self):
        """
        Строковое представление коллекции.
        
        Returns:
            str: Информация о коллекции
        """
        if len(self._items) == 0:
            return "🚌 Автопарк: пуст"
        
        result = f"🚌 Автопарк (всего автобусов: {len(self._items)})\n"
        result += "-" * 50 + "\n"
        for i, bus in enumerate(self._items):
            result += f"{i+1}. {bus}\n"
        return result