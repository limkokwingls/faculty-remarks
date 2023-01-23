from turtle import title
import openpyxl
from test_pages.files import test_pages
from bs4 import BeautifulSoup
import pandas as pd
from openpyxl.styles import PatternFill, Border, Side, Alignment, Font
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.workbook.workbook import Workbook
from openpyxl.cell.cell import Cell
from openpyxl.utils.dataframe import dataframe_to_rows

PARSER = "html5lib"


def main():
    with open(test_pages("graderesult.php.html")) as file:
        html = file.read()

        soup = BeautifulSoup(html, PARSER)
        table = soup.select('.ewReportTable tr')

        workbook = Workbook()
        sheet: Worksheet = workbook.active

        title_printed = False
        for row_i, row in enumerate(table):
            if title_printed:
                row_i += 3
            for col_i, col in enumerate(row):
                if row_i == 3 and col_i == 1:
                    title = col.get_text(separator='\n', strip=True)
                    title_lines = title.split("\n")
                    for i, line in enumerate(title_lines):
                        sheet.cell(i+1, 1).value = line
                    title_printed = True
                else:
                    val = col.get_text(strip=True)
                    cell = sheet.cell(row=row_i+1, column=col_i+1)
                    # add_border(cell)
                    cell.value = val

        workbook.save("data.xlsx")


def add_border(cell: Cell):
    cell.border = Border(left=Side(style='thin'),
                         right=Side(style='thin'),
                         top=Side(style='thin'),
                         bottom=Side(style='thin'))


if __name__ == '__main__':
    print(main())
