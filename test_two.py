from turtle import title
import openpyxl
from html_utils import get_background
from model import Student
from test_pages.files import test_pages
from bs4 import BeautifulSoup, ResultSet, Tag
from openpyxl.styles import PatternFill, Border, Side, Alignment, Font
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.workbook.workbook import Workbook
from openpyxl.cell.cell import Cell
from openpyxl.utils.dataframe import dataframe_to_rows
from bs4.element import Tag
from rich import print

from utils.excel import delete_empty_columns, fit_column_width, is_merged_cell, set_value

PARSER = "html5lib"


def get_course_names(tr: Tag):
    data = {}
    td: Tag
    for i, td in enumerate(tr.find_all('td')):
        text = td.get_text(strip=True)
        if i == 0:
            continue
        if text == 'No. of Module(s)':
            break
        data[i] = text
    return data


def get_course_codes(tr: Tag):
    data = {}
    td: Tag
    for i, td in enumerate(tr.find_all('td')):
        text = td.get_text(strip=True)
        if i == 0:
            continue
        if not text:
            break
        data[i] = text
    return data


def read_grades(html_table: ResultSet[Tag]):
    course_names = get_course_names(html_table[3])
    course_codes = get_course_codes(html_table[4])
    for tr_i, tr in enumerate(html_table):
        if tr_i < 3:
            continue
        td: Tag
        for td_i, td in enumerate(tr.find_all('td')):
            text = td.get_text(strip=True)
            #     std = Student()
            # print(tr_i, td_i, text)

    print(course_codes)


def main():
    with open(test_pages("graderesult.php.html")) as file:
        html = file.read()
        soup = BeautifulSoup(html, PARSER)
        table = soup.select('.ewReportTable tr')
        read_grades(table)


if __name__ == '__main__':
    print(main())
