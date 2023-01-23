import openpyxl
from test_pages.files import test_pages
from bs4 import BeautifulSoup
import pandas as pd
from openpyxl.styles import PatternFill, Border, Side, Alignment, Font
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.workbook.workbook import Workbook
from openpyxl.cell.cell import Cell
from openpyxl.utils.dataframe import dataframe_to_rows
from utils import is_number
from rich import print


PARSER = "html5lib"


def get_marks_cols(sheet: Worksheet):
    courses = {}
    for col in sheet.iter_cols():
        for c in col:
            cell: Cell = c
            if cell.value == 'Mk':
                col_i = cell.col_idx
                row_i = cell.row
                grade_cell: Cell = sheet.cell(row_i-2, col_i)
                # courses[grade_cell.value] = grade_cell.column
                courses[grade_cell.column] = grade_cell.value
    return courses


def get_std_column(sheet: Worksheet):
    for col in sheet.iter_cols():
        for c in col:
            cell: Cell = c
            if cell.value == 'StudentID':
                return cell.column
    return 3


def get_remark_col(sheet: Worksheet):
    for col in sheet.iter_cols():
        for c in col:
            cell: Cell = c
            if cell and cell.value and 'remark' in str(cell.value).lower():
                return cell.column
    return -1


def get_student_numbers(sheet: Worksheet) -> dict[int, str]:
    data = {}
    std_col = get_std_column(sheet)

    for col in sheet.iter_cols():
        for c in col:
            cell: Cell = c
            if cell.column == std_col:
                if is_number(cell.value):
                    data[cell.row] = cell.value
    return data


def get_remarks(sheet: Worksheet):
    marks = get_marks_cols(sheet)
    students = get_student_numbers(sheet)

    data = {}
    for student_col in students:
        student_number = students[student_col]
        repeat = []
        sup = []
        for mark_col in marks:
            mark_value = sheet.cell(student_col, mark_col).value
            if is_number(mark_value):
                mark_value = int(mark_value)
                if mark_value >= 45 and mark_value < 50:
                    sup.append(marks[mark_col])
                elif mark_value < 45:
                    repeat.append(marks[mark_col])
        remarks = "Proceed"
        if len(repeat) >= 3:
            remarks = "Remain in Semester"

        if len(sup) > 0:
            remarks = f"{remarks}, Sup " + ", ".join(sup)
        if len(repeat) > 0:
            remarks = f"{remarks}, Repeat " + ", ".join(repeat)

        data[student_col] = remarks
    return data


def main():
    file_path = "Results 2022-08.xlsx"
    workbook: Workbook = openpyxl.load_workbook(file_path)

    sheet: Worksheet = workbook.active

    for ws in workbook:
        sheet: Worksheet = ws
        remarks = get_remarks(sheet)
        remarks_col = get_remark_col(sheet)
        for it in remarks:
            print(f"row={it}, col={remarks_col}")
            cell: Cell = sheet.cell(row=it, column=remarks_col)
            cell.value = remarks[it]

    workbook.save(file_path)


if __name__ == '__main__':
    print(main())
