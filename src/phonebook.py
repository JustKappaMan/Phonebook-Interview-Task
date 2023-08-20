from pathlib import Path
from csv import DictReader, DictWriter


class Phonebook:
    """The class that contains and manipulates all the records"""

    def __init__(self) -> None:
        self.file = Path("..", "phonebook.csv")
        self.fieldnames = ("first_name", "middle_name", "last_name", "organization", "phone_work", "phone_personal")
        self.records: list[dict] = []

        if not self.file.exists():
            with open(self.file, "w", encoding="utf-8", newline="") as f:
                writer = DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()
        else:
            self.__update_records()

    def __update_records(self) -> None:
        with open(self.file, "r", encoding="utf-8", newline="") as f:
            reader = DictReader(f)
            self.records = list(reader)

    def add(self, record: list[str]) -> None:
        with open(self.file, "a", encoding="utf-8", newline="") as f:
            writer = DictWriter(f, fieldnames=self.fieldnames)
            writer.writerow({k: v for k, v in zip(self.fieldnames, record)})
        self.__update_records()

    def edit(self) -> None:
        pass

    def find(self) -> None:
        pass
