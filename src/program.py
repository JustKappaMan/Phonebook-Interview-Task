import os
import sys
from itertools import islice

from config import Config
from phonebook import Phonebook


class Program:
    """Basically, the UI class. It uses Phonebook to manipulate all the records."""

    def __init__(self) -> None:
        self.config = Config()

        if not self.config.file.exists():
            Program.clear_screen()
            input(
                f"Файл настроек '{self.config.file}' не найден! "
                "Создан файл со стандартными настройками."
                "\n\nНажмите Enter чтобы продолжить..."
            )

        self.phonebook = Phonebook()

    def run(self) -> None:
        """Start the program"""
        self.__render_main_menu()

    def __render_main_menu(self) -> None:
        """Main menu"""
        while True:
            Program.clear_screen()
            user_input = input(
                "Телефонный справочник\n\n"
                "1. Просмотреть записи\n"
                "2. Добавить запись\n"
                "3. Редактировать запись\n"
                "4. Поиск по записям\n"
                "5. Завершить программу\n\n"
                "Введите номер пункта меню: "
            ).strip()

            match user_input:
                case "1":
                    self.__render_viewing_section()
                case "2":
                    self.__render_adding_section()
                case "3":
                    self.__render_editing_section()
                case "4":
                    self.__render_search_section()
                case "5":
                    Program.close()
                case _:
                    continue

    def __render_viewing_section(self) -> None:
        """Menu section for viewing records page by page"""
        pages = self.__chunk_records(self.phonebook.records)
        current_page_index = 0

        while True:
            Program.clear_screen()
            print(f"Телефонный справочник (c. {current_page_index + 1})\n")
            self.__print_table(pages[current_page_index])

            user_input = input(
                "\n1. Следующая страница\n"
                "2. Предыдущая страница\n"
                "3. Главное меню\n\n"
                "Введите номер пункта меню: "
            ).strip()

            match user_input:
                case "1":
                    if current_page_index < len(pages) - 1:
                        current_page_index += 1
                case "2":
                    if current_page_index > 0:
                        current_page_index -= 1
                case "3":
                    self.__render_main_menu()
                case _:
                    continue

    def __render_adding_section(self) -> None:
        """Menu section for adding a new record"""

        # ID is just like "INTEGER AUTO_INCREMENT" column in SQL table.
        # It's generated automatically, not received from user input.
        new_record = {"ID": f"{len(self.phonebook.records) + 1}"}
        for name in self.phonebook.fieldnames[1:]:
            new_record[name] = self.__guarded_input(
                f"Телефонный справочник (новая запись)\n\n{name}: ", clear_screen=True
            )

        self.phonebook.add(new_record)

        while True:
            Program.clear_screen()
            user_input = input(
                "Телефонный справочник (новая запись)\n\n"
                "Запись успешно добавлена!\n\n"
                "1. Добавить еще одну\n"
                "2. Главное меню\n\n"
                "Введите номер пункта меню: "
            ).strip()

            match user_input:
                case "1":
                    self.__render_adding_section()
                case "2":
                    self.__render_main_menu()
                case _:
                    continue

    def __render_editing_section(self) -> None:
        """Menu section for editing an existing record"""
        while True:
            user_input = self.__guarded_input(
                "Телефонный справочник (редактирование записи)\n\nВведите ID записи, подлежащей редактированию: ",
                clear_screen=True,
            )

            # Check if record ID is a positive integer in valid range
            if user_input.isdigit():
                if 0 < (record_id := int(user_input)) <= len(self.phonebook.records):
                    break

        while True:
            Program.clear_screen()
            print("Телефонный справочник (редактирование записи)\n")
            self.__print_table([self.phonebook.records[record_id - 1]])

            user_input = input(
                "\n1. Отредактировать данную запись\n2. Главное меню\n\nВведите номер пункта меню: "
            ).strip()

            match user_input:
                case "1":
                    new_record = {"ID": f"{record_id}"}
                    for name in self.phonebook.fieldnames[1:]:
                        new_record[name] = self.__guarded_input(
                            f"Телефонный справочник (редактирование записи)\n\n{name}: ", clear_screen=True
                        )

                    self.phonebook.edit(record_id, new_record)

                    while True:
                        Program.clear_screen()
                        user_input = input(
                            "Телефонный справочник (редактирование записи)\n\n"
                            "Запись успешно отредактирована!\n\n"
                            "1. Отредактировать еще одну\n"
                            "2. Главное меню\n\n"
                            "Введите номер пункта меню: "
                        ).strip()

                        match user_input:
                            case "1":
                                self.__render_editing_section()
                            case "2":
                                self.__render_main_menu()
                            case _:
                                continue

                case "2":
                    self.__render_main_menu()
                case _:
                    continue

    def __render_search_section(self) -> None:
        search_criteria = dict.fromkeys(self.phonebook.fieldnames)

        while True:
            Program.clear_screen()
            user_input = input(
                "Телефонный справочник (поиск по записям)\n\n"
                "Пожалуйста, задайте критерии для поиска\n\n"
                f"1. ID - {search_criteria['ID'] or 'не задан'}\n"
                f"2. Имя - {search_criteria['Имя'] or 'не задано'}\n"
                f"3. Отчество - {search_criteria['Отчество'] or 'не задано'}\n"
                f"4. Фамилия - {search_criteria['Фамилия'] or 'не задана'}\n"
                f"5. Организация - {search_criteria['Организация'] or 'не задана'}\n"
                f"6. Рабочий телефон - {search_criteria['Рабочий телефон'] or 'не задан'}\n"
                f"7. Личный телефон - {search_criteria['Личный телефон'] or 'не задан'}\n"
                "8. Начать поиск\n"
                "9. Главное меню\n\n"
                "Введите номер пункта меню: "
            ).strip()

            Program.clear_screen()
            match user_input:
                case "1":
                    search_criteria["ID"] = self.__guarded_input(
                        "Телефонный справочник (поиск по записям)\n\nВведите ID: ", clear_screen=True
                    )
                case "2":
                    search_criteria["Имя"] = self.__guarded_input(
                        "Телефонный справочник (поиск по записям)\n\nВведите имя: ", clear_screen=True
                    )
                case "3":
                    search_criteria["Отчество"] = self.__guarded_input(
                        "Телефонный справочник (поиск по записям)\n\nВведите отчество: ", clear_screen=True
                    )
                case "4":
                    search_criteria["Фамилия"] = self.__guarded_input(
                        "Телефонный справочник (поиск по записям)\n\nВведите фамилию: ", clear_screen=True
                    )
                case "5":
                    search_criteria["Организация"] = self.__guarded_input(
                        "Телефонный справочник (поиск по записям)\n\nВведите организацию: ", clear_screen=True
                    )
                case "6":
                    search_criteria["Рабочий телефон"] = self.__guarded_input(
                        "Телефонный справочник (поиск по записям)\n\nВведите рабочий телефон: ", clear_screen=True
                    )
                case "7":
                    search_criteria["Личный телефон"] = self.__guarded_input(
                        "Телефонный справочник (поиск по записям)\n\nВведите личный телефон: ", clear_screen=True
                    )
                case "8":
                    if not (
                        found_records := self.phonebook.search(
                            search_criteria,
                            is_strict=self.config.search_is_strict,
                            is_case_sensitive=self.config.search_is_case_sensitive,
                        )
                    ):
                        # "Nothing was found" menu section
                        while True:
                            Program.clear_screen()
                            user_input = input(
                                "Телефонный справочник (результаты поиска)\n\n"
                                "Поиск с заданными критериями не дал результата\n\n"
                                "1. Изменить критерии\n"
                                "2. Главное меню\n\n"
                                "Введите номер пункта меню: "
                            ).strip()

                            match user_input:
                                case "1":
                                    break
                                case "2":
                                    self.__render_main_menu()
                                case _:
                                    continue
                    else:
                        # "Successful search results" menu section
                        pages = self.__chunk_records(found_records)
                        current_page_index = 0

                        while True:
                            Program.clear_screen()
                            print(f"Телефонный справочник (результаты поиска c. {current_page_index + 1})\n")
                            self.__print_table(pages[current_page_index])

                            user_input = input(
                                "\n1. Следующая страница\n"
                                "2. Предыдущая страница\n"
                                "3. Главное меню\n\n"
                                "Введите номер пункта меню: "
                            ).strip()

                            match user_input:
                                case "1":
                                    if current_page_index < len(pages) - 1:
                                        current_page_index += 1
                                case "2":
                                    if current_page_index > 0:
                                        current_page_index -= 1
                                case "3":
                                    self.__render_main_menu()
                                case _:
                                    continue
                case "9":
                    self.__render_main_menu()
                case _:
                    continue

    def __print_table(self, records: list[dict] | tuple[dict]) -> None:
        """Print given records in a pretty table. To some extent."""
        print("=" * len(self.phonebook.fieldnames) * (self.config.column_width + 1))
        print(*(field.center(self.config.column_width) for field in self.phonebook.fieldnames), sep="|")
        print("=" * len(self.phonebook.fieldnames) * (self.config.column_width + 1))
        for record in records:
            print(*(value.ljust(self.config.column_width) for value in record.values()), sep="|")

    def __guarded_input(self, prompt: str, clear_screen: bool = False) -> str:
        """To accept data that fits into a table column"""
        while True:
            if clear_screen:
                Program.clear_screen()

            input_data = input(prompt).strip()

            if len(input_data) <= self.config.column_width:
                return input_data

    def __chunk_records(self, records: list[dict]) -> list[tuple]:
        """Split list of records into equally sized tuples (the last one may vary)"""
        it = iter(records)
        return list(iter(lambda: tuple(islice(it, self.config.records_per_page)), ()))

    @staticmethod
    def clear_screen() -> None:
        """Clear the command line on any platform"""
        os.system("cls" if sys.platform == "win32" else "clear")

    @staticmethod
    def close() -> None:
        """Clear the command line and exit the program"""
        Program.clear_screen()
        sys.exit()
