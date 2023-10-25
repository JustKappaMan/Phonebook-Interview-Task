from pathlib import Path
from configparser import ConfigParser


class Config(ConfigParser):
    """The class that contains and manipulates all settings"""

    def __init__(self, file: Path = Path("..", "settings.ini")) -> None:
        super().__init__()

        # Make config case-sensitive
        self.optionxform = str

        self.file = file
        self.file_not_found = not self.file.exists()

        if self.file_not_found:
            self.add_section("Appearance")
            self.set("Appearance", "ColumnWidth", "16")
            self.set("Appearance", "RecordsPerPage", "10")
            self.add_section("Search")
            self.set("Search", "Strict", "False")
            self.set("Search", "CaseSensitive", "False")

            with open(file, "w", encoding="utf-8") as f:
                self.write(f)
        else:
            with open(file, "r", encoding="utf-8") as f:
                self.read_file(f, source=file.name)

        # Table column width and max table cell value length at the same time.
        # Can't be less than 16 to be displayed properly.
        self.column_width = self.getint("Appearance", "ColumnWidth", fallback=16)
        self.column_width = max(self.column_width, 16)

        # Number of table rows per page when viewing records.
        # The recommended (and default) value is 10. The min value is 1.
        self.records_per_page = self.getint("Appearance", "RecordsPerPage", fallback=10)
        self.records_per_page = 10 if self.records_per_page < 1 else self.records_per_page

        # If True, the `==` operator is used when searching, otherwise `in` is used.
        # The default value is False.
        self.search_is_strict = self.getboolean("Search", "Strict", fallback=False)

        # If True, the search is case-sensitive, otherwise it's not.
        # The default value is False.
        self.search_is_case_sensitive = self.getboolean("Search", "CaseSensitive", fallback=False)
