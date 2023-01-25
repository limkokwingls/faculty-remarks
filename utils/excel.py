from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.cell.cell import Cell


def is_merged_cell(sheet: Worksheet, cell: Cell):
    found = False
    merged_ranges = sheet.merged_cells.ranges
    for merged_range in merged_ranges:
        if cell.coordinate in merged_range:
            found = True
    return found


def delete_empty_columns(sheet: Worksheet):
    for col in sheet.iter_cols():
        empty = True
        for cell in col:
            if cell.value:
                empty = False
                break
        if empty:
            col_idx = col[0].column
            sheet.delete_cols(col_idx)
