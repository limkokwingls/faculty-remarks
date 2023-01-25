from turtle import title
import openpyxl
from test_pages.files import test_pages
from bs4 import BeautifulSoup, ResultSet, Tag
from openpyxl.styles import PatternFill, Border, Side, Alignment, Font
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.workbook.workbook import Workbook
from openpyxl.cell.cell import Cell
from openpyxl.utils.dataframe import dataframe_to_rows

from utils.excel import delete_empty_columns

PARSER = "html5lib"


def format_sheet(sheet: Worksheet):
    border = Border(left=Side(style='thin'),
                    right=Side(style='thin'),
                    top=Side(style='thin'),
                    bottom=Side(style='thin'))
    delete_empty_columns(sheet)
    # was_deleted = False
    for i, col in enumerate(sheet.iter_cols()):
        # if not was_deleted:
        #     sheet.delete_cols(i, i)
        for cell in col:
            ...
            # cell.border = border


def write_to_sheet(sheet: Worksheet, html_table: ResultSet[Tag]):
    title_printed = False
    for row_i, row in enumerate(html_table):
        if title_printed:
            row_i += 3
        for col_i, col in enumerate(row):
            val = col.get_text(strip=True)
            cell: Cell = sheet.cell(row=row_i+1, column=col_i+1)
            if row_i == 3 and col_i == 1:
                val = col.get_text(separator='\n', strip=True)
            if row_i == 3:
                sheet.column_dimensions[cell.column_letter].width = 37
                sheet.row_dimensions[cell.row].height = 120
                cell.alignment = Alignment(
                    vertical='center', wrap_text=True)
            cell.value = val
    format_sheet(sheet)


def html_to_excel():
    workbook = Workbook()
    sheet: Worksheet = workbook.active

    with open(test_pages("graderesult.php.html")) as file:
        html = file.read()
        soup = BeautifulSoup(html, PARSER)
        table = soup.select('.ewReportTable tr')
        write_to_sheet(sheet, table)

    workbook.save("data.xlsx")


def main():
    html_to_excel()


if __name__ == '__main__':
    print(main())
