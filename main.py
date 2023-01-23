import asyncio
from unittest import result
from rich.prompt import Prompt
from pick import pick
from browser import Browser
from rich.prompt import Confirm
from rich.console import Console
from rich.prompt import Prompt
from rich import print
from datetime import datetime
from rich.progress import track


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


async def login():
    username, password, logged_in = None, None, False
    credentials = read_credentials()
    if credentials:
        username, password = credentials
        logged_in = await browser.login(username, password)
    else:
        print("Enter CMS credentials")
        logged_in = input_username_and_password()

    while not logged_in:
        logged_in = input_username_and_password()


student_numbers = [
    901016893,
    901000052,
    901000098,
    901000120,
    901000166,
    901000167,
]


async def main():
    while not browser.logged_in:
        await login()

    # programs = browser.get_programs()

    # program, _ = pick(programs, "Pick Program", indicator='->')
    # program = program.split()[0]  # type: ignore
    # print(program)

    # results = []
    # startTime = datetime.now()
    # for i, it in enumerate(student_numbers):
    #     res = browser.read_transcript(
    #         it, 1, progress=f"{i}/{len(student_numbers)}")
    #     results.append(res)
    # print(results)
    # print(datetime.now() - startTime)

    results = []

    with console.status("Reading transcripts"):
        tasks = []
        for it in student_numbers:
            tasks.append(asyncio.create_task(browser.read_transcript(it, 1)))
    for it in track(asyncio.as_completed(tasks), total=len(tasks), description="Downloading transcripts"):
        results.append(await it)

    print(results)
    print(len(results))

if __name__ == '__main__':
    # while True:
    asyncio.run(main())
