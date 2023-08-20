from phonebook import Phonebook
from misc import *


class InputHandler:
    def __init__(self):
        self.phonebook = Phonebook()
        self.user_input = None

    @clear_screen
    def run(self):
        while True:
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
                    self.close()
                case _:
                    cls()

    @clear_screen
    def view_records(self):
        pages = chunk(self.phonebook.records, 10)
        current_page_index = 0

        while True:
            cls()
            print(f"Телефонный справочник (c. {current_page_index + 1})\n")

            """TODO: rewrite using some module for pretty tables"""
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
                    pass

    @clear_screen
    def add_record(self):
        input("Adding record...press any key to continue...")
        self.run()

    @clear_screen
    def edit_record(self):
        input("Editing record...press any key to continue...")
        self.run()

    @clear_screen
    def find_records(self):
        input("Finding record...press any key to continue...")
        self.run()

    @clear_screen
    def close(self):
        exit()
