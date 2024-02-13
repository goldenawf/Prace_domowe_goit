from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    pass


class Record:
    def __init__(self, name, phone):
        self.name = Name(name)
        self.phone = [Phone(phone)]

    def add_phone(self, phone):
        self.phone.append(Phone(phone))

    def remove_phone(self, phone):
        self.phone = [x for x in self.phone if x != phone]

    def edit_phone(self, phone, new_phone):
        for p in self.phone:
            if p.value == phone:
                p.value = new_phone

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
