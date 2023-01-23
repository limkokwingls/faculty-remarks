from rich.prompt import Prompt
from pick import pick
from browser import Browser
from rich.prompt import Confirm
from rich.console import Console
from rich.prompt import Prompt
from rich import print

from credentials import read_credentials, write_credentials

console = Console()
error_console = Console(stderr=True, style="bold red")
browser = Browser()


def input_username_and_password():
    username = Prompt.ask("Username")
    password = Prompt.ask("Password", password=True)
    display_name = browser.login(username, password)
    if not display_name:
        error_console.print("Invalid Credentials")
    else:
        write_credentials(username, password)
        print()
    return display_name


def login():
    username, password, logged_in = None, None, False
    credentials = read_credentials()
    if credentials:
        username, password = credentials
        logged_in = browser.login(username, password)
    else:
        print("Enter CMS credentials")
        logged_in = input_username_and_password()

    while not logged_in:
        logged_in = input_username_and_password()

    console.print("Login Successful", style="green")


def main():
    while not browser.logged_in:
        try_function(login)

    # programs = browser.get_programs()

    # program, _ = pick(programs, "Pick Program", indicator='->')
    # program = program.split()[0]  # type: ignore
    # print(program)

    results = browser.read_transcript("901000010", 1)
    print(results)


def try_function(func, *args):
    retry = True
    results = None
    while retry:
        try:
            results = func(*args)
            retry = False
        except Exception as e:
            error_console.print("Error:", e)
            retry = Confirm.ask("Do you want to retry", default=True)
    return results


if __name__ == '__main__':
    # while True:
    main()
