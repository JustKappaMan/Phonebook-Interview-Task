import os
import sys
from pathlib import Path
from itertools import islice
from configparser import ConfigParser

from phonebook import Phonebook


def chunk(it: list, size: int) -> list[tuple]:
    """Split a list into tuples of equal size (except the last one)"""
    it = iter(it)
    return list(iter(lambda: tuple(islice(it, size)), ()))


class Program:
    """Basically, the UI class. It uses Phonebook to manipulate all the records."""

    def __init__(self, config_file_path: Path = Path("..", "settings.ini")) -> None:
        # Config that preserves case
        config = ConfigParser()
        config.optionxform = str

        if config_file_path.exists():
            with open(config_file_path, "r", encoding="utf-8") as f:
                config.read_file(f, source=config_file_path.name)
        else:
            config.add_section("Appearance")
            config.set("Appearance", "ColumnWidth", "16")
            config.set("Appearance", "RecordsPerPage", "10")
            config.add_section("Search")
            config.set("Search", "Strict", "False")
            config.set("Search", "CaseSensitive", "False")

            with open(config_file_path, "w", encoding="utf-8") as f:
                config.write(f)

            Program.clear_screen()
            input(
                f"Файл настроек '{config_file_path}' не найден! "
                "Создан файл со стандартными настройками."
                "\n\nНажмите Enter чтобы продолжить..."
            )

        # Table column width and max table cell value length at the same time.
        # Can't be less than 16 to be displayed properly.
        self.column_width = config.getint("Appearance", "ColumnWidth", fallback=16)
        self.column_width = max(self.column_width, 16)

        # Number of table rows per page when viewing records.
        # The recommended (and default) value is 10. The min value is 1.
        self.records_per_page = config.getint("Appearance", "RecordsPerPage", fallback=10)
        self.records_per_page = 10 if self.records_per_page < 1 else self.records_per_page

        # If True, the `==` operator is used when searching, otherwise `in` is used.
        # The default value is False.
        self.search_is_strict = config.getboolean("Search", "Strict", fallback=False)

        # If True, the search is case-sensitive, otherwise it's not.
        # The default value is False.
        self.search_is_case_sensitive = config.getboolean("Search", "CaseSensitive", fallback=False)

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
        pages = chunk(self.phonebook.records, self.records_per_page)
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
                            is_strict=self.search_is_strict,
                            is_case_sensitive=self.search_is_case_sensitive,
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
                        pages = chunk(found_records, self.records_per_page)
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
        print("=" * len(self.phonebook.fieldnames) * (self.column_width + 1))
        print(*(field.center(self.column_width) for field in self.phonebook.fieldnames), sep="|")
        print("=" * len(self.phonebook.fieldnames) * (self.column_width + 1))
        for record in records:
            print(*(value.ljust(self.column_width) for value in record.values()), sep="|")

    def __guarded_input(self, prompt: str, clear_screen: bool = False) -> str:
        """To accept data that fits into a table column"""
        while True:
            if clear_screen:
                Program.clear_screen()

            input_data = input(prompt).strip()

            if len(input_data) <= self.column_width:
                return input_data

    @staticmethod
    def clear_screen() -> None:
        """Clear the command line on any platform"""
        os.system("cls" if sys.platform == "win32" else "clear")

    @staticmethod
    def close() -> None:
        """Clear the command line and exit the program"""
        Program.clear_screen()
        sys.exit()
