from os import system
from sys import platform
from functools import wraps

screens = {
    "start_screen": (
        "Телефонный справочник\n\n"
        "1. Просмотреть записи\n"
        "2. Добавить запись\n"
        "3. Редактировать запись\n"
        "4. Поиск по записям\n"
        "5. Завершить программу\n"
    )
}


def clear_screen(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        system("cls" if platform == "win32" else "clear")
        return method(self, *args, **kwargs)

    return wrapper
