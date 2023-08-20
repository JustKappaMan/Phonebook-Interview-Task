from sys import exit

from phonebook import Phonebook
from misc import *


class InputHandler:
    """The UI class that uses Phonebook to manipulate all the records"""

    def __init__(self) -> None:
        self.phonebook = Phonebook()
        self.user_input = None

    def run(self) -> None:
        """Main menu"""
        while True:
            clear_screen()
            self.user_input = input(
                "Телефонный справочник\n\n"
                "1. Просмотреть записи\n"
                "2. Добавить запись\n"
                "3. Редактировать запись\n"
                "4. Поиск по записям\n"
                "5. Завершить программу\n\n"
                "Введите номер пункта меню: "
            )

            match self.user_input:
                case "1":
                    self.view_records()
                case "2":
                    self.add_record()
                case "3":
                    self.edit_record()
                case "4":
                    self.find_records()
                case "5":
                    InputHandler.close()
                case _:
                    continue

    def view_records(self) -> None:
        """Menu section to view DB page by page"""
        pages = chunk(self.phonebook.records)
        current_page_index = 0

        while True:
            clear_screen()
            print(f"Телефонный справочник (c. {current_page_index + 1})\n")

            # TODO: rewrite using some module for pretty tables
            print(*(f"{field:<16}" for field in self.phonebook.fieldnames), sep="|")
            for record in pages[current_page_index]:
                print(*(f"{value:<16}" for value in record.values()), sep="|")

            self.user_input = input(
                "\n1. Следующая страница\n"
                "2. Предыдущая страница\n"
                "3. Главное меню\n\n"
                "Введите номер пункта меню: "
            )

            # Can't turn the first/last page? Redisplay the current one.
            match self.user_input:
                case "1":
                    if current_page_index < len(pages) - 1:
                        current_page_index += 1
                case "2":
                    if current_page_index > 0:
                        current_page_index -= 1
                case "3":
                    self.run()
                case _:
                    continue

    def add_record(self) -> None:
        clear_screen()
        input("Adding record...press any key to continue...")
        self.run()

    def edit_record(self) -> None:
        clear_screen()
        input("Editing record...press any key to continue...")
        self.run()

    def find_records(self) -> None:
        clear_screen()
        input("Finding record...press any key to continue...")
        self.run()

    @staticmethod
    def close() -> None:
        clear_screen()
        exit()
