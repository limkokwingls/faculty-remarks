import asyncio
from pathlib import Path
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
from tqdm import tqdm

from credentials import read_credentials, write_credentials
from workbook_reader import get_remark_col, get_remarks, get_student_numbers, read_student_marks

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


async def get_cms_results(worksheet: Worksheet):
    label = worksheet.title
    student_numbers = list(get_student_numbers(worksheet).values())
    results = {}
    with console.status(f"Reading {label} transcripts..."):
        tasks = []
        for it in student_numbers:
            tasks.append(asyncio.create_task(browser.read_transcript(it, 1)))
        data = await asyncio.gather(*tasks)

        for i, it in enumerate(data):
            results[student_numbers[i]] = it

    return results


def open_file():
    # file = None
    # while file == None:
    #     try:
    #         file_path = Prompt.ask(
    #             "Excel File:", default="Results 2022-08_2.xlsx")
    #         file_path = file_path.strip('\"')
    #         if Path(file_path).is_file():
    #             file = file_path
    #     except Exception as e:
    #         error_console.print("Error:", e)
    # return file
    return "Results 2022-08_2.xlsx"


async def main():
    while not browser.logged_in:
        await login()

    file = open_file()
    workbook: Workbook = openpyxl.load_workbook(file)

    # sheet: Worksheet = workbook.active

    for ws in workbook:
        sheet: Worksheet = ws
        cms_results = await get_cms_results(sheet)
        remarks = get_remarks(sheet, cms_results)
        remarks_col = get_remark_col(sheet)
        for it in remarks:
            cell: Cell = sheet.cell(row=it, column=remarks_col)
            cell.value = remarks[it]

    workbook.save(file)
    print("[bold blue]Done!")

if __name__ == '__main__':
    # while True:
    asyncio.run(main())
