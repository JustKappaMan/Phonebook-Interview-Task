from pathlib import Path
from csv import DictReader, DictWriter


class Phonebook:
    """The main class that contains and manipulates all the records"""

    def __init__(self) -> None:
        self.file = Path("phonebook.csv")
        self.fieldnames = ("first_name", "middle_name", "last_name", "organization", "phone_work", "phone_personal")
        self.records: list[dict] = []

        if not self.file.exists():
            with open(self.file, "w", encoding="utf-8", newline="") as f:
                writer = DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()
        else:
            self.__update_records()

    def __update_records(self):
        with open(self.file, "r", encoding="utf-8", newline="") as f:
            reader = DictReader(f)
            self.records = list(reader)

    def display(self) -> None:
        """TODO: rewrite using some module for pretty tables"""
        print(*(f"{field:<16}" for field in self.fieldnames), sep="|")
        for record in self.records:
            print(*(f"{value:<16}" for value in record.values()), sep="|")

    def add(self, record: list[str]) -> None:
        with open(self.file, "a", encoding="utf-8", newline="") as f:
            writer = DictWriter(f, fieldnames=self.fieldnames)
            writer.writerow({k: v for k, v in zip(self.fieldnames, record)})
        self.__update_records()

    def edit(self) -> None:
        pass

    def find(self) -> None:
        pass


def main():
    phonebook = Phonebook()
    phonebook.display()
    phonebook.add(["Иван", "Иванович", "Иванов", "Яндекс", "+79220000000", "+79221111111"])
    phonebook.display()


if __name__ == "__main__":
    main()
