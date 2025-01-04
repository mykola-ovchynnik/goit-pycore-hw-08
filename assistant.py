from models import Record
from utils import input_error, parse_input, save_data, load_data


class AssistantBot:
    def __init__(self):
        self.book = load_data()

    @input_error
    def add_contact(self, args):
        name, phone, *_ = args
        record = self.book.find(name)
        message = "Contact updated."
        if record is None:
            record = Record(name)
            self.book.add_record(record)
            message = "Contact added."
        if phone:
            record.add_phone(phone)
        return message

    @input_error
    def change_contact(self, args):
        name, old_phone, new_phone = args
        record = self.book.find(name)
        record.edit_phone(old_phone, new_phone)
        return "Contact updated."

    @input_error
    def delete_contact(self, args):
        name = args[0]
        self.book.delete(name)
        return "Contact deleted."

    @input_error
    def add_birthday(self, args):
        name, birthday = args
        record = self.book.find(name)
        record.add_birthday(birthday)
        return "Birthday added."

    @input_error
    def show_birthday(self, args):
        name = args[0]
        record = self.book.find(name)
        if not record.birthday:
            return "Birthday not set."
        return f"{name}'s birthday is on {record.birthday.value.strftime('%d.%m.%Y')}"

    def show_all(self):
        if not self.book:
            return "No contacts found."
        return "\n".join([str(record) for record in self.book.values()])

    @input_error
    def show_phone(self, args):
        name = args[0]
        record = self.book.find(name)
        return str(record)

    @input_error
    def show_upcoming_birthdays(self, args):
        days = int(args[0]) if args else 7
        upcoming_birthdays = self.book.get_upcoming_birthdays(days)
        if not upcoming_birthdays:
            return "No upcoming birthdays."
        return "\n".join([str(record) for record in upcoming_birthdays])

    def show_help(self):
        help_text = """Available commands:
            hello                - Greet the assistant
            add <name> <phone>   - Add a new contact
            change <name> <old_phone> <new_phone> - Change an existing contact's phone number
            delete <name>        - Delete a contact
            phone <name>         - Show contact details
            all                  - Show all contacts
            add-birthday <name> <birthday> - Add a birthday to a contact (format: DD.MM.YYYY)
            show-birthday <name> - Show a contact's birthday
            birthdays <days>     - Show upcoming birthdays within the next <days> days
            help                 - Show this help message
            close | exit         - Exit the assistant"""
        print(help_text)

    def handle_command(self, command, args):
        match command:
            case "close" | "exit":
                save_data(self.book)
                print("Good bye!")
                return False

            case "hello":
                print("How can I help you?")

            case "add":
                print(self.add_contact(args))

            case "change":
                print(self.change_contact(args))

            case "delete":
                print(self.delete_contact(args))

            case "phone":
                print(self.show_phone(args))

            case "all":
                print(self.show_all())

            case "add-birthday":
                print(self.add_birthday(args))

            case "show-birthday":
                print(self.show_birthday(args))

            case "birthdays":
                print(self.show_upcoming_birthdays(args))

            case "help":
                self.show_help()

            case _:
                print("Invalid command.")
        return True

    def run(self):
        print("Welcome to the assistant bot!")
        try:
            while True:
                user_input = input("Enter a command: ")
                command, args = parse_input(user_input)
                if not self.handle_command(command, args):
                    break
        except (KeyboardInterrupt, Exception) as e:
            save_data(self.book)
            print(f"An unexpected error occurred: {e}")
            print("\nGood bye!")


if __name__ == "__main__":
    bot = AssistantBot()
    bot.run()
