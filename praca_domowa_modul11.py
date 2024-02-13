from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

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
        self.birthday = birthday

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
            return self.birthday - datetime.now()
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
