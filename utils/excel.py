from openpyxl.worksheet.worksheet import Worksheet


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
