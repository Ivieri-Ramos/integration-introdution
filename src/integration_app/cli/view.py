from rich.console import Console
from rich.panel import Panel
from rich.table import Table

import sys

_console_out = Console()
_console_err = Console(stderr=True)

def show(message: str):
    if _console_out.is_terminal:
        panel = Panel(
            message,
            border_style="green",
            expand=False,
        )

        _console_out.print(panel)
    else:
        print(message)

def show_error(message: str):
    if _console_out.is_terminal:
        panel = Panel(
            message,
            border_style="red",
            expand=False,
        )

        _console_err.print(panel)
    else:
        print(message, file=sys.stderr)


def show_table(title: str, columns: list[str], rows: list[list[str]]) -> None:
    if _console_out.is_terminal:
        table = Table(title=title, border_style="cyan")

        for col in columns:
            table.add_column(col, justify="center")

        for row in rows:
            table.add_row(*row)

        _console_out.print(table)
    else:
        print(title)
        print(" | ".join(columns))
        for row in rows:
            print(" | ".join(row))