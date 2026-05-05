"""
Расширенный контейнер Fleet с методами sort_by, filter_by и apply,
поддерживающими цепочки операций. Наследует базовую коллекцию из ЛР3.
"""

from lab03.models import Fleet as BaseFleet


class Fleet(BaseFleet):
    """
    Расширенная коллекция автобусов с возможностью передачи функций-стратегий.
    """

    def sort_by(self, key_func):
        """
        Сортирует коллекцию по заданной key-функции.
        Возвращает себя для цепочки вызовов.

        Args:
            key_func: функция, принимающая объект Bus и возвращающая ключ сортировки.

        Returns:
            self (Fleet): та же коллекция, но отсортированная.
        """
        self._items.sort(key=key_func)
        return self

    def filter_by(self, predicate):
        """
        Создаёт новую коллекцию из элементов, удовлетворяющих предикату.

        Args:
            predicate: функция-предикат, принимающая Bus и возвращающая bool.

        Returns:
            Fleet: новый экземпляр Fleet с отфильтрованными элементами.
        """
        new_fleet = Fleet()
        for bus in self._items:
            if predicate(bus):
                # Копируем объект без дублирования (используем тот же объект)
                new_fleet._items.append(bus)
        return new_fleet

    def apply(self, func):
        """
        Применяет функцию ко всем элементам коллекции.
        Возвращает себя для цепочки.

        Args:
            func: функция, которая вызывается для каждого элемента коллекции.

        Returns:
            self (Fleet): коллекция после применения функции.
        """
        for bus in self._items:
            func(bus)
        return self