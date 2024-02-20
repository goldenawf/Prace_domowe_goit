from collections import UserDict
from datetime import datetime, timedelta
import pickle


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    @property
    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def get_value(self):
        return self.value

    def set_value(self, new_value):
        if isinstance(new_value, str) and new_value.isdigit() and len(new_value) == 9:
            self.value = new_value
        else:
            raise ValueError('Phone number must be 9 digits long')


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)

    def get_value(self):
        return self.value

    def set_value(self, new_value):
        if isinstance(new_value, str) and len(new_value) == 10:
            self.value = new_value
        else:
            raise ValueError('Birthday must be 10 digits long')

    def days_to_birthday(self):
        if self.value:
            birthday = datetime.strptime(self.value, "%Y-%m-%d")
            now = datetime.now()
            next_birthday = datetime(now.year, birthday.month, birthday.day)
            if now > next_birthday:
                next_birthday += timedelta(days=365)
            return (next_birthday - now).days


class Record:
    def __init__(self, name, phone, birthday=None):
        self.name = Name(name)
        self.phone = [Phone(phone)]
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        self.phone.append(Phone(phone))

    def remove_phone(self, phone):
        self.phone = [x for x in self.phone if x != phone]

    def edit_phone(self, phone, new_phone):
        for p in self.phone:
            if p.value == phone:
                p.value = new_phone

    def days_to_birthday(self):
        if self.birthday:
            return self.birthday.days_to_birthday()
        else:
            return 'No birthday date'

    def __str__(self):
        phones_str = ", ".join(str(x) for x in self.phone)
        return f'Name: {self.name}, Phones {phones_str}'


class AddressBook(UserDict):
    def add_contact(self, name, phone):
        self.data[name] = Record(name, phone)

    def change_contact(self, name, phone):
        self.data[name] = Record(name, phone)

    def search_contact(self, name):
        result = ''
        for key, value in self.data.items():
            if name in key:
                result += f'{key}: {value}\n'
        return result

    def remove_contact(self, name):
        if name in self.data:
            del self.data[name]
        else:
            return 'Not found'

    def __str__(self):
        result = ''
        for key, value in self.data.items():
            result += f'{key}: {value}\n'
        return result

    def iterator(self, n=1):
        for key, value in self.data.items():
            if n == 0:
                break
            n -= 1
            yield f'{key}: {value}'

    def save(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)

    @classmethod
    def load(cls, filename):
        with open(filename, 'rb') as file:
            data = pickle.load(file)
        address_book = cls()
        address_book.data = data
        return address_book


address_book = AddressBook()


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except KeyError:
            return "Błąd: Nieprawidłowe polecenie."
        except ValueError:
            return "Błąd: Nieprawidłowe wartości."
        except IndexError:
            return "Błąd: Brakujące argumenty."
        except TypeError:
            return "Błąd: Brakuje argumentu."

    return wrapper


@input_error
def parse_command(command):
    command = command.split(" ")
    return command[0], command[1:]


@input_error
def say_hello():
    print("How can I help you?")


@input_error
def say_bye():
    print("Good bye!")
    return True


@input_error
def add_contact(contact_name, contact_number):
    if contact_name not in address_book:
        address_book.add_contact(contact_name, int(contact_number))
        print(f"Dodano nowy kontakt: {contact_name}, numer telefonu: {contact_number}")
    else:
        print(f"Kontakt {contact_name} już istnieje. Nie dodano.")


@input_error
def get_contacts():
    print(address_book)
    return address_book


@input_error
def change_contact(name, new_number):
    if name in address_book:
        address_book[name] = int(new_number)
        print(f"Zmieniono numer telefonu dla kontaktu {name} na {new_number}")
    else:
        print(f"Kontakt {name} nie istnieje. Nie można zmienić numeru telefonu.")


@input_error
def show_all_contacts():
    if address_book:
        print("Lista wszystkich kontaktów:")
        for name, number in address_book.items():
            print(f"Kontakt: {name}, Numer telefonu: {number}")
    else:
        print("Brak zapisanych kontaktów.")
    return address_book


@input_error
def phone(name):
    if name in address_book:
        return address_book[name]
    else:
        return "Brak kontaktu o takiej nazwie."


def search_contact(self, name):
    result = ''
    for key, value in self.data.items():
        if name.lower() in key.lower():
            result += f'{key}: {value}\n'
    return result


def main():
    command_handlers = {
        "hello": say_hello,
        "add": add_contact,
        "get_contacts": get_contacts,
        "goodbye": say_bye,
        "close": say_bye,
        "exit": say_bye,
        "change": change_contact,
        "show_all": show_all_contacts,
        "phone": phone,
        "search": search_contact
    }

    exit_program = False
    while not exit_program:
        print(". - close the app")
        command = input("Podaj polecenie: ")
        if command == ".":
            print("Good bye!")
            exit_program = True
        else:
            command, args = parse_command(command)
            if not args:
                command_handlers[command]()
            else:
                command_handlers[command](*args)


if __name__ == '__main__':
    main()
