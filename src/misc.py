from os import system
from sys import platform
from typing import Iterable
from itertools import islice


def clear_screen() -> None:
    system("cls" if platform == "win32" else "clear")


def chunk(it: Iterable, size: int = 10) -> list[tuple]:
    it = iter(it)
    return list(iter(lambda: tuple(islice(it, size)), ()))
