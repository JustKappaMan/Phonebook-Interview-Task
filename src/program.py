import os
import sys
import itertools

from phonebook import Phonebook


def chunk(it: list, size: int = 10) -> list[tuple]:
    """Split a list into equally-sized (except the last one) tuples"""
    it = iter(it)
    return list(iter(lambda: tuple(itertools.islice(it, size)), ()))


class Program:
    """Basically, the UI class that uses Phonebook to manipulate all the records"""

    def __init__(self) -> None:
        self.phonebook = Phonebook()
        self.max_field_length = 16
        self.search_is_strict = False

    def run(self) -> None:
        self.__render_main_menu()

    def __render_main_menu(self) -> None:
        """Main menu"""
        while True:
            Program.__clear_screen()
            user_input = input(
                "Телефонный справочник\n\n"
                "1. Просмотреть записи\n"
                "2. Добавить запись\n"
                "3. Редактировать запись\n"
                "4. Поиск по записям\n"
                "5. Завершить программу\n\n"
                "Введите номер пункта меню: "
            )

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
        """Menu section to view DB page by page"""
        pages = chunk(self.phonebook.records)
        current_page_index = 0

        while True:
            Program.__clear_screen()
            print(f"Телефонный справочник (c. {current_page_index + 1})\n")
            self.__print_table(pages[current_page_index])

            user_input = input(
                "\n1. Следующая страница\n"
                "2. Предыдущая страница\n"
                "3. Главное меню\n\n"
                "Введите номер пункта меню: "
            )

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
        """Menu section to add a new record into DB"""
        # ID is just like "INTEGER AUTO_INCREMENT" column in SQL table
        # It's generated automatically, not received from user input
        new_record = {"ID": len(self.phonebook.records) + 1}
        for name in self.phonebook.fieldnames[1:]:
            new_record[name] = self.__guarded_input(
                f"Телефонный справочник (новая запись)\n\n{name}: ", clear_screen=True
            )

        self.phonebook.add(new_record)

        while True:
            Program.__clear_screen()
            user_input = input(
                "Телефонный справочник (новая запись)\n\n"
                "Запись успешно добавлена!\n\n"
                "1. Добавить еще одну\n"
                "2. Главное меню\n\n"
                "Введите номер пункта меню: "
            )

            match user_input:
                case "1":
                    self.__render_adding_section()
                case "2":
                    self.__render_main_menu()
                case _:
                    continue

    def __render_editing_section(self) -> None:
        """Menu section to edit an existing record in DB"""
        while True:
            user_input = self.__guarded_input(
                "Телефонный справочник (редактирование записи)\n\nВведите ID записи, подлежащей редактированию: ",
                clear_screen=True,
            )

            # Check record ID to be positive integer in valid range
            if not user_input.startswith("-") and user_input.isdigit():
                if 0 < (record_id := int(user_input)) <= len(self.phonebook.records):
                    break

        while True:
            Program.__clear_screen()
            print("Телефонный справочник (редактирование записи)\n")
            self.__print_table([self.phonebook.records[record_id - 1]])

            user_input = input("\n1. Отредактировать данную запись\n2. Главное меню\n\nВведите номер пункта меню: ")
            match user_input:
                case "1":
                    new_record = {"ID": record_id}
                    for name in self.phonebook.fieldnames[1:]:
                        new_record[name] = self.__guarded_input(
                            f"Телефонный справочник (редактирование записи)\n\n{name}: ", clear_screen=True
                        )

                    self.phonebook.edit(record_id, new_record)

                    while True:
                        Program.__clear_screen()
                        user_input = input(
                            "Телефонный справочник (редактирование записи)\n\n"
                            "Запись успешно отредактирована!\n\n"
                            "1. Отредактировать еще одну\n"
                            "2. Главное меню\n\n"
                            "Введите номер пункта меню: "
                        )

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
            Program.__clear_screen()
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
            )

            Program.__clear_screen()
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
                    if not (found_records := self.phonebook.search(search_criteria, is_strict=self.search_is_strict)):
                        # "Nothing was found" menu section
                        while True:
                            Program.__clear_screen()
                            user_input = input(
                                "Телефонный справочник (результаты поиска)\n\n"
                                "Поиск с заданными критериями не дал результата\n\n"
                                "1. Изменить критерии\n"
                                "2. Главное меню\n\n"
                                "Введите номер пункта меню: "
                            )

                            match user_input:
                                case "1":
                                    break
                                case "2":
                                    self.__render_main_menu()
                                case _:
                                    continue
                    else:
                        # "Successful search results" menu section
                        pages = chunk(found_records)
                        current_page_index = 0

                        while True:
                            Program.__clear_screen()
                            print(f"Телефонный справочник (результаты поиска c. {current_page_index + 1})\n")
                            self.__print_table(pages[current_page_index])

                            user_input = input(
                                "\n1. Следующая страница\n"
                                "2. Предыдущая страница\n"
                                "3. Главное меню\n\n"
                                "Введите номер пункта меню: "
                            )

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
        """Print given records in pretty table. To some extent."""
        # TODO: rewrite using some module for pretty tables
        print(*(field.center(self.max_field_length) for field in self.phonebook.fieldnames), sep="|")
        print("=" * len(self.phonebook.fieldnames) * (self.max_field_length + 1))
        for record in records:
            print(*(value.ljust(self.max_field_length) for value in record.values()), sep="|")

    def __guarded_input(self, prompt: str, clear_screen: bool = False) -> str:
        """To accept data that will fit in table column"""
        while True:
            if clear_screen:
                Program.__clear_screen()

            input_data = input(prompt)

            if len(input_data) <= self.max_field_length:
                return input_data

    @staticmethod
    def __clear_screen() -> None:
        """Clear command line on any platform"""
        os.system("cls" if sys.platform == "win32" else "clear")

    @staticmethod
    def close() -> None:
        Program.__clear_screen()
        sys.exit()
