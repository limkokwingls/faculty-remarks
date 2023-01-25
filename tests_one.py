from turtle import title
import openpyxl
from test_pages.files import test_pages
from bs4 import BeautifulSoup, ResultSet, Tag
from openpyxl.styles import PatternFill, Border, Side, Alignment, Font
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.workbook.workbook import Workbook
from openpyxl.cell.cell import Cell
from openpyxl.utils.dataframe import dataframe_to_rows

from utils.excel import delete_empty_columns, is_merged_cell

PARSER = "html5lib"


def format_sheet(sheet: Worksheet):
    border = Border(left=Side(style='thin'),
                    right=Side(style='thin'),
                    top=Side(style='thin'),
                    bottom=Side(style='thin'))
    # cell.border = border
    delete_empty_columns(sheet)
    sheet.delete_rows(1, 3)
    sheet.row_dimensions[1].height = 120  # type:ignore

    first_cell = sheet['A1']
    first_cell.alignment = Alignment(
        vertical='center', wrap_text=True)


def write_to_sheet(sheet: Worksheet, html_table: ResultSet[Tag]):

    for tr_i, tr in enumerate(html_table, start=1):
        for td_i, td in enumerate(tr.find_all('td'), start=1):
            cell: Cell = sheet.cell(row=tr_i, column=td_i)
            text = td.get_text(strip=True)
            if tr_i == 3 and td_i == 1:
                text = td.get_text(separator='\n', strip=True)
            if not is_merged_cell(sheet, cell):
                cell.value = text
                if td.get('colspan'):
                    span = int(td.get('colspan'))
                    sheet.merge_cells(start_row=cell.row, start_column=cell.column,
                                      end_row=cell.row, end_column=cell.column+span)

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
