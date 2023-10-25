from pathlib import Path
from csv import DictReader, DictWriter


class Phonebook:
    """The class that contains and manipulates all records"""

    def __init__(self, file_path: Path = Path(__file__).resolve().parent.parent / "phonebook.csv") -> None:
        self.file = file_path
        self.fieldnames = ("ID", "Имя", "Отчество", "Фамилия", "Организация", "Рабочий телефон", "Личный телефон")
        self.records: list[dict] = []

        if not self.file.exists():
            with open(self.file, "w", encoding="utf-8", newline="") as f:
                writer = DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()
        else:
            with open(self.file, "r", encoding="utf-8", newline="") as f:
                reader = DictReader(f)
                self.records = list(reader)

    def add(self, record: dict) -> None:
        """Add new record to DB and file"""
        self.records.append(record)
        with open(self.file, "a", encoding="utf-8", newline="") as f:
            writer = DictWriter(f, fieldnames=self.fieldnames)
            writer.writerow(record)

    def edit(self, record_id: int, record: dict) -> None:
        """Modify a DB record. Write updated DB to file."""
        self.records[record_id - 1] = record
        with open(self.file, "w", encoding="utf-8", newline="") as f:
            writer = DictWriter(f, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(self.records)

    def search(self, search_criteria: dict, is_strict: bool, is_case_sensitive: bool) -> list[dict]:
        """Return the list of records matching specified criteria"""
        result = []

        # Remove pairs with None and "" values, taking the case sensitivity flag into account
        if is_case_sensitive:
            search_criteria = {k: v for k, v in search_criteria.items() if v}
        else:
            search_criteria = {k: v.lower() for k, v in search_criteria.items() if v}

        if is_strict:
            # Use `==` to compare records
            for record in self.records:
                if all(search_criteria[key] == record[key].lower() for key in search_criteria):
                    result.append(record)
        else:
            # Use `in` to compare records
            for record in self.records:
                if all(search_criteria[key] in record[key].lower() for key in search_criteria):
                    result.append(record)

        return result
