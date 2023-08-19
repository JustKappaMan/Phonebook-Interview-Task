from phonebook import Phonebook


def main():
    phonebook = Phonebook()
    phonebook.display()
    phonebook.add(["Иван", "Иванович", "Иванов", "Яндекс", "+79220000000", "+79221111111"])
    phonebook.display()


if __name__ == "__main__":
    main()
