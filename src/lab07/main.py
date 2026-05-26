# lab07/main.py
"""Точка входа в консольное приложение."""

from cli import CLI

if __name__ == "__main__":
    cli = CLI("data.json")
    cli.run()