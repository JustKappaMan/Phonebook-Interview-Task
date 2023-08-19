from typing import cast
from pathlib import Path
from csv import DictReader


class Phonebook:
    """The main class that contains and manipulates all the records"""

    def __init__(self) -> None:
        self.file = Path("phonebook.csv")
        with open(self.file, "r", encoding="utf-8", newline="") as f:
            reader = DictReader(f)
            self.headers: list[str] = cast(reader.fieldnames, list[str])
            self.records: list[dict] = list(reader)

    def display(self) -> None:
        """TODO: rewrite using some module for pretty tables"""
        print(*(f"{header:<16}" for header in self.headers), sep="|")
        for record in self.records:
            print(*(f"{value:<16}" for value in record.values()), sep="|")

    def add(self) -> None:
        pass

    def edit(self) -> None:
        pass

    def delete(self) -> None:
        pass

    def find(self) -> None:
        pass


def main():
    phonebook = Phonebook()
    phonebook.display()


if __name__ == "__main__":
    main()
