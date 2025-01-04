from models import AddressBook, Record
from utils import input_error, parse_input


@input_error
def add_contact(args, book):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."


@input_error
def delete_contact(args, book):
    name = args[0]
    book.delete(name)
    return "Contact deleted."


@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if not record.birthday:
        return "Birthday not set."
    return f"{name}'s birthday is on {record.birthday.value.strftime('%d.%m.%Y')}"


def show_all(book):
    if not book:
        return "No contacts found."
    return "\n".join([str(record) for record in book.values()])


@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    return str(record)


@input_error
def show_upcoming_birthdays(args, book):
    days = int(args[0]) if args else 7
    upcoming_birthdays = book.get_upcoming_birthdays(days)
    if not upcoming_birthdays:
        return "No upcoming birthdays."
    return "\n".join([str(record) for record in upcoming_birthdays])


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        match command:
            case "close" | "exit":
                print("Good bye!")
                break

            case "hello":
                print("How can I help you?")

            case "add":
                print(add_contact(args, book))

            case "change":
                print(change_contact(args, book))

            case "delete":
                print(delete_contact(args, book))

            case "phone":
                print(show_phone(args, book))

            case "all":
                print(show_all(book))

            case "add-birthday":
                print(add_birthday(args, book))

            case "show-birthday":
                print(show_birthday(args, book))

            case "birthdays":
                print(show_upcoming_birthdays(args, book))

            case _:
                print("Invalid command.")


if __name__ == "__main__":
    main()
