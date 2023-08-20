from os import system
from sys import platform
from itertools import islice


def clear_screen():
    system("cls" if platform == "win32" else "clear")


def chunk(it, size):
    it = iter(it)
    return list(iter(lambda: tuple(islice(it, size)), ()))
