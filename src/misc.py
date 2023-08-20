from os import system
from sys import platform
from functools import wraps
from itertools import islice


def cls():
    system("cls" if platform == "win32" else "clear")


def clear_screen(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        cls()
        return method(self, *args, **kwargs)

    return wrapper


def chunk(it, size):
    it = iter(it)
    return list(iter(lambda: tuple(islice(it, size)), ()))
