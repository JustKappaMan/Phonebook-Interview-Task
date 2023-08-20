from os import system
from sys import platform
from itertools import islice


def clear_screen() -> None:
    """Clear command line on any platform"""
    system("cls" if platform == "win32" else "clear")


def chunk(it: list, size: int = 10) -> list[tuple]:
    """Split a list into equally-sized (except the last one) tuples"""
    it = iter(it)
    return list(iter(lambda: tuple(islice(it, size)), ()))
