import asyncio
from unittest import result
import openpyxl
from rich.prompt import Prompt
from pick import pick
from browser import Browser
from rich.prompt import Confirm
from rich.console import Console
from rich.prompt import Prompt
from rich import print
from datetime import datetime
from rich.progress import track
from openpyxl.styles import PatternFill, Border, Side, Alignment, Font
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.workbook.workbook import Workbook
from openpyxl.cell.cell import Cell
from openpyxl.utils.dataframe import dataframe_to_rows


from credentials import read_credentials, write_credentials
from workbook_reader import get_remark_col, get_remarks, get_student_numbers

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


async def get_results(worksheet: Worksheet):

    label = worksheet.title
    student_numbers = list(get_student_numbers(worksheet).values())

    results = {}
    with console.status(f"Reading {label} transcripts"):
        tasks = []
        for it in student_numbers:
            tasks.append(asyncio.create_task(browser.read_transcript(it, 1)))
    for i, it in enumerate(track(asyncio.as_completed(tasks), total=len(tasks), description=f"Downloading {label} transcripts")):
        results[student_numbers[i]] = await it
    return results


async def main():
    while not browser.logged_in:
        await login()

    file_path = "Results 2022-08_2.xlsx"
    workbook: Workbook = openpyxl.load_workbook(file_path)

    sheet: Worksheet = workbook.active

    for ws in workbook:
        sheet: Worksheet = ws
        results = await get_results(sheet)
        print(results)
        # remarks = get_remarks(sheet, results)
        # remarks_col = get_remark_col(sheet)
        # for it in remarks:
        #     print(f"row={it}, col={remarks_col}")
        #     cell: Cell = sheet.cell(row=it, column=remarks_col)
        #     cell.value = remarks[it]

        exit()

    workbook.save(file_path)

if __name__ == '__main__':
    # while True:
    asyncio.run(main())
