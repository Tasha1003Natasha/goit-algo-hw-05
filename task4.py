from colorama import Fore, Style, init

init(autoreset=True)
BROWN = "\033[38;5;94m"


def input_error(value_error_msg=None, key_error_msg=None, index_error_msg=None):

    def decorator(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except KeyError:
                return (
                    key_error_msg
                    or f"{Fore.RED}Error{Style.RESET_ALL}: contact not found"
                )
            except ValueError:
                return value_error_msg or "Enter the argument for the command"
            except IndexError:
                return index_error_msg or "Error: not enough arguments provided."
            except Exception as e:
                return f"Unexpected error: {e}"

        return inner

    return decorator


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error(
    value_error_msg=f"{Fore.RED}Error{Style.RESET_ALL}: you must provide both name and phone number (example: {Fore.MAGENTA}add Alice 12345{Style.RESET_ALL})"
)
def add_contact(args, contacts):
    name, phone = args
    contacts[name] = phone
    return f"{Style.RESET_ALL}Contact added."


@input_error(
    value_error_msg=f"{Fore.RED}Error{Style.RESET_ALL}: you must provide both name and phone number (example: {Fore.MAGENTA}change Alice 54321{Style.RESET_ALL}) "
)
def change_contact(args, contacts):
    name, phone = args
    if name in contacts:
        contacts[name] = phone
        return f"{Style.RESET_ALL}Contact {BROWN}'{name}'{Style.RESET_ALL} updated."
    else:
        raise KeyError


@input_error(
    value_error_msg=f"{Fore.RED}Error{Style.RESET_ALL}: you must provide a name (example: {Fore.MAGENTA}phone Alice{Style.RESET_ALL})"
)
def show_phone(args, contacts):
    if not args:
        raise ValueError
    if len(args) > 1:
        raise ValueError

    name = args[0]
    if name in contacts:
        phone = contacts[name]
        return f"{Style.RESET_ALL}Phone '{name}': {BROWN}'{phone} {Style.RESET_ALL}."
    else:
        raise KeyError


@input_error(
    key_error_msg="No contacts.",
    index_error_msg=f"{Fore.RED}Error{Style.RESET_ALL}: you must provide (example: {Fore.MAGENTA} all{Style.RESET_ALL})",
)
def show_all(args, contacts):
    if not contacts:
        raise KeyError
    if args:
        raise IndexError

    return f"{BROWN}{contacts}{Style.RESET_ALL}"


def main():
    # консольний бот помічник
    contacts = {}

    print("Welcome to the assistant bot!")
    while True:
        user_input = input(
            f"Enter {Fore.MAGENTA}a command{Style.RESET_ALL}: {Fore.CYAN}"
        )
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print(f"{Style.RESET_ALL}Good bye!")
            break
        elif command == "hello":
            print(f"{Style.RESET_ALL}How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(args, contacts))
        else:
            print(f"{Style.RESET_ALL}Invalid command.")


if __name__ == "__main__":
    main()
