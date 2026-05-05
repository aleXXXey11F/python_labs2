"""
Расширенный контейнер Fleet с методами sort_by, filter_by и apply,
поддерживающими цепочки операций.
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from lab03.models import Fleet as BaseFleet


class Fleet(BaseFleet):
    def sort_by(self, key_func):
        self._items.sort(key=key_func)
        return self

    def filter_by(self, predicate):
        new_fleet = Fleet()
        for bus in self._items:
            if predicate(bus):
                new_fleet._items.append(bus)
        return new_fleet

    def apply(self, func):
        for bus in self._items:
            func(bus)
        return self