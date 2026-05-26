# lab07/exceptions.py
"""Собственные исключения предметной области."""

class ItemNotFoundError(Exception):
    """Объект не найден в коллекции."""
    pass

class DuplicateItemError(Exception):
    """Объект с таким идентификатором уже существует."""
    pass