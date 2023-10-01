import math
from typing import List, Union, Tuple, Optional, Iterable


def format_table(title: str, headers: List[str], table: List[Tuple],
                 cell_len: Optional[Union[int, Iterable]] = None):

    table = [tuple([str(cell) for cell in row]) for row in table]

    row_len = len(table[0]) if table else 0
    optimus_cell_len = [max([len(max(row[i].split("\n"), key=lambda x: len(x)))
                             for row in table] + [len(headers[i])]) + 2
                        for i in range(row_len)]

    if isinstance(cell_len, int):
        cell_len = tuple([cell_len] * row_len)
    elif cell_len is None:
        cell_len = optimus_cell_len
    else:
        cell_len = [val2 if val1 is None else val1
                    for val1, val2 in zip(cell_len, optimus_cell_len)]

    x_size = max([len(title) + 2, sum(cell_len) + 2 * row_len])
    blank = x_size - len(title) - 1

    o, c = "{", "}"

    div_l = "├"
    div_l2 = "├"
    div_l3 = "╰"
    for c_len, index in zip(cell_len, range(1, len(cell_len) + 1)):
        div_l += "─" * (c_len + 1) + ("┬" if index < len(cell_len) else "┤")
        div_l2 += "─" * (c_len + 1) + ("┼" if index < len(cell_len) else "┤")
        div_l3 += "─" * (c_len + 1) + ("┴" if index < len(cell_len) else "╯")

    headers_str = "│" + "".join([f" {o}:^{i}{c}│"
                                 for i in cell_len]).format(*headers)[:-1]
    headers_str += "│"

    rows = [
        f"╭{'─' * (x_size - 1)}╮",
        f"│{' ' * math.floor(blank / 2)}{title}{' ' * math.ceil(blank / 2)}│",
        div_l,
        headers_str,
        div_l2
    ]

    counter = 0
    for row in table:
        counter += 1
        r_str = "│"
        row_ = []
        for n, cell, index in zip(cell_len, row, range(1, len(row) + 1)):
            r_str += f" {o}:<{n}{c}{'│' if index < len(row) else '│'}"
            lines = []
            for line in cell.split("\n"):
                lines += [line[i:i+n-2] for i in range(0, len(line), n-2)]
            row_.append(lines)

        max_cell_rows = len(max(row_, key=lambda c_: len(c_)))

        for cell in row_:
            for _ in range(max_cell_rows - len(cell)):
                cell.append("")

        row_ = [list(col) for col in zip(*row_)]

        for sub_row in row_:
            rows.append(r_str.format(*sub_row))

        rows.append(div_l2 if counter < len(table) else div_l3)

    return "\n".join(rows)
