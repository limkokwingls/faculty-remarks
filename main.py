from rich.prompt import Prompt
from pick import pick
from pip import main
from browser import Browser
from rich.prompt import Confirm
from rich.console import Console
from rich.prompt import Prompt

from term import get_term

console = Console()
error_console = Console(stderr=True, style="bold red")
browser = Browser()
faculty = None


def login():
    username = Prompt.ask("Username")
    password = Prompt.ask("Password", password=True)
    with open('credentials', 'r') as f:
        credentials = f.read().splitlines()
    if credentials:
        username = credentials[0]
        password = credentials[1]

    browser.login(username, password)


def main():
    while not browser.logged_in:
        try_function(login)

    global faculty
    if not faculty:
        faculty_list = browser.get_faculties()
        faculty, _ = pick(faculty_list, "Pick Faculty", indicator='->')
    print(faculty)

    programs = browser.get_programs(faculty)
    program, _ = pick(programs, "Pick Program", indicator='->')
    print("Program", program)

    sem: str = Prompt.ask("Semester", choices=[
                          '1', '2', '3', '4', '5', '6', '7', '8'])
    term = Prompt.ask("Term", default=get_term())
    students = browser.program_students(faculty, program, f"0{sem}", term)
    for i, std in enumerate(students):
        browser.print_transcript(std[3])
        print(f"{i+1}/{len(students)}) {std[3]} - {std[4]}, Done")


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
    while True:
        with console.screen():
            main()
