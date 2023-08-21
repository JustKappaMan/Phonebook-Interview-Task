from pathlib import Path
from csv import DictReader, DictWriter


class Phonebook:
    """The class that contains and manipulates all the records"""

    def __init__(self) -> None:
        self.file = Path("..", "phonebook.csv")
        self.fieldnames = ("ID", "Имя", "Отчество", "Фамилия", "Организация", "Рабочий телефон", "Личный телефон")
        self.records: list[dict] = []

        if not self.file.exists():
            with open(self.file, "w", encoding="utf-8", newline="") as f:
                writer = DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()
        else:
            self.__update_records()

    def __update_records(self) -> None:
        """Save all records from DB to `self.records`.
        MUST be called at the end of every method that modifies DB.
        """
        with open(self.file, "r", encoding="utf-8", newline="") as f:
            reader = DictReader(f)
            self.records = list(reader)

    def add(self, record: dict) -> None:
        """Add new record into DB"""
        with open(self.file, "a", encoding="utf-8", newline="") as f:
            writer = DictWriter(f, fieldnames=self.fieldnames)
            writer.writerow(record)
        self.__update_records()

    def edit(self, record_id: int, record: dict) -> None:
        """Modify a record in `self.records`.
        Entirely rewrites the DB.
        """
        # TODO: optimize
        self.records[record_id - 1] = record
        with open(self.file, "w", encoding="utf-8", newline="") as f:
            writer = DictWriter(f, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(self.records)
        self.__update_records()

    def find(self) -> None:
        pass
