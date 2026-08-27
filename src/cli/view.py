from rich.console import Console
from rich.panel import Panel

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