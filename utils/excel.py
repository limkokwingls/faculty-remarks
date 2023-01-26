from types import NoneType
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.cell.cell import Cell


def set_value(cell: Cell, value: str):
    if type(value) == NoneType:
        return
    if value.isdigit():
        cell.value = int(value)
        cell.number_format = '0'
    elif value.replace(".", "").isdigit():
        cell.value = float(value)
        cell.number_format = '0.00'
    else:
        cell.value = value


def is_merged_cell(sheet: Worksheet, cell: Cell):
    found = False
    merged_ranges = sheet.merged_cells.ranges  # type: ignore
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
