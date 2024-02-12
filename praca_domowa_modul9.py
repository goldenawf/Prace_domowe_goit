contacts = {}


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
    exit_program = True


@input_error
def add_contact(contact_name, contact_number):
    if contact_name not in contacts:
        contacts[contact_name] = int(contact_number)
        print(f"Dodano nowy kontakt: {contact_name}, numer telefonu: {contact_number}")
    else:
        print(f"Kontakt {contact_name} już istnieje. Nie dodano.")


@input_error
def get_contacts():
    print(contacts)
    return contacts


@input_error
def change_contact(name, new_number):
    if name in contacts:
        contacts[name] = int(new_number)
        print(f"Zmieniono numer telefonu dla kontaktu {name} na {new_number}")
    else:
        print(f"Kontakt {name} nie istnieje. Nie można zmienić numeru telefonu.")


@input_error
def show_all_contacts():
    if contacts:
        print("Lista wszystkich kontaktów:")
        for name, number in contacts.items():
            print(f"Kontakt: {name}, Numer telefonu: {number}")
    else:
        print("Brak zapisanych kontaktów.")
    return contacts


@input_error
def phone(name):
    if name in contacts:
        return contacts[name]
    else:
        return "Brak kontaktu o takiej nazwie."


@input_error
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
        "phone": phone
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


main()


