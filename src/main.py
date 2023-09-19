from sys import version_info

from program import Program


def main() -> None:
    py_major_ver_req, py_minor_ver_req = 3, 10

    if version_info.major < py_major_ver_req or version_info.minor < py_minor_ver_req:
        Program.clear_screen()
        input(
            f"Запуск невозможен. Минимальная требуемая версия Python — {py_major_ver_req}.{py_minor_ver_req}.\n\n"
            "Нажмите Enter для выхода из программы..."
        )
        Program.clear_screen()
    else:
        program = Program()
        program.run()


if __name__ == "__main__":
    main()
