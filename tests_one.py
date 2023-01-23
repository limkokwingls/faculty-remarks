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

        for row_i, row in enumerate(table):
            for col_i, col in enumerate(row):
                if row_i >= 4:
                    break
                if row_i == 3 and col_i == 1:
                    text = col.get_text(separator='\n', strip=True)
                    print(text.split("\n"))
                val = col.get_text(strip=True)
                sheet.cell(row=row_i+1, column=col_i+1).value = val

        workbook.save("data.xlsx")


if __name__ == '__main__':
    print(main())
