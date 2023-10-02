
from typing import List

def create_table(column_label: str, row_label: str, data: List[List],
                 info_row: List[str] = None, info_column: List[str] = None,
                 dynamic: bool = False, padding: int = 0):
    # ... (Rest des Codes)
    if info_row is None:
        info_row = [str(i + 1) for i in range(len(data[0]))]
    if info_column is None:
        info_column = [str(i + 1) for i in range(len(data))]

    if len(info_row) != len(data[0]) or len(info_column) != len(data) or padding < 0:
        raise ValueError('Invalid parameters.')

    column_widths = [max(len(str(elem)) + padding for elem in col) for col in zip(*([info_row] + data))]
    if not dynamic:
        max_width = max(column_widths)
        column_widths = len(info_row) * [max_width]

    first_column_width = max(len(column_label), len(row_label), len(str(len(data))))

    header = column_label.rjust(first_column_width) + '  ' + " ".join(
        str(cell).ljust(column_widths[i]) for i, cell in enumerate(info_row))

    data_rows = "\n".join(
        info_column[i].rjust(first_column_width) + '  ' + " ".join(
            str(cell).ljust(column_widths[j]) for j, cell in enumerate(row))
        for i, row in enumerate(data))

    return f"{header}\n{row_label.rjust(first_column_width)}\n{data_rows}"
