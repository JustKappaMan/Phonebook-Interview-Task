from dataclasses import dataclass


@dataclass
class Record:
    """An individual record in the phonebook"""

    first_name: str
    middle_name: str
    last_name: str
    organization: str
    phone_number_work: str
    phone_number_personal: str


class Phonebook:
    """The main class that contains and manipulates all the records"""

    def __init__(self):
        self.records: list[Record] = ...

    def display(self):
        pass

    def add(self):
        pass

    def edit(self):
        pass

    def delete(self):
        pass

    def find(self):
        pass


def main():
    pass


if __name__ == "__main__":
    main()
