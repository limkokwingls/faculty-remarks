import openpyxl
from test_pages.files import test_pages
from bs4 import BeautifulSoup
import pandas as pd
from openpyxl.styles import PatternFill, Border, Side, Alignment, Font
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.workbook.workbook import Workbook
from openpyxl.cell.cell import Cell
from openpyxl.utils.dataframe import dataframe_to_rows
from utils import is_number, to_int
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


def get_remarks(sheet: Worksheet, transcript: dict[int, list[dict[str, float]]]):
    marks_dict = get_marks_cols(sheet)
    students = get_student_numbers(sheet)

    data = {}
    for student_col in students:
        student_number = to_int(students[student_col])
        results = transcript[student_number]
        repeat = []
        sup = []
        for mark_col, course_code in marks_dict.items():
            cell: Cell = sheet.cell(student_col, mark_col)
            if is_number(cell.value):
                mark_value = float(cell.value)
                if mark_value >= 45 and mark_value < 50:
                    sup.append(course_code)
                elif mark_value < 45:
                    repeat.append(course_code)
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
    pass


if __name__ == '__main__':
    print(main())
