from phonebook import Phonebook
from misc import *


class InputHandler:
    def __init__(self):
        self.phonebook = Phonebook()
        self.user_input = None

    @clear_screen
    def run(self):
        print(screens["start_screen"])
        self.user_input = input("Введите номер пункта меню: ")

        match self.user_input:
            case "1":
                self.view_records()
            case "2":
                self.add_record()
            case "3":
                self.edit_record()
            case "4":
                self.find_records()
            case "5":
                self.close()
            case _:
                self.wrong_input()

    @clear_screen
    def view_records(self):
        self.phonebook.display()
        input("Press any key to continue...")
        self.run()

    @clear_screen
    def add_record(self):
        input("Adding record...press any key to continue...")
        self.run()

    @clear_screen
    def edit_record(self):
        input("Editing record...press any key to continue...")
        self.run()

    @clear_screen
    def find_records(self):
        input("Finding record...press any key to continue...")
        self.run()

    @clear_screen
    def close(self):
        exit()

    @clear_screen
    def wrong_input(self):
        input("Wrong input! Press any key to continue...")
        self.run()
