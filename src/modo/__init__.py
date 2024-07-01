from typing_extensions import Annotated
from typing import Optional
from datetime import datetime

import typer
from rich.table import Table
from rich import print

from .display import clock_in, clock_out, status_view
from .data import write_start, write_end, read

app = typer.Typer()


@app.command()
def reset():
    init_file()


@app.command()
def hi(
    time: Annotated[Optional[str],
                    typer.Argument(help="Start time")] = None,
    date: Annotated[Optional[str],
                    typer.Option(help="Date to log for")] = None,
):
    """Set start of work hours for today or anyday"""
    if date is None and time is None:
        date = datetime.now()
    elif date is None:
        date = datetime.today()
        date = date.replace(hour=int(time.split(":")[0]),
                            minute=int(time.split(":")[1]))
    else:  # manual spec of date and time
        date = datetime.fromisoformat(date)
        date = date.replace(hour=int(time.split(":")[0]),
                            minute=int(time.split(":")[1]))
    write_start(date)
    clock_in(date)


@app.command()
def bye(
    time: Annotated[Optional[str], typer.Argument()] = None,
    date: Annotated[Optional[str],
                    typer.Option(help="Date to log for")] = None,
):
    """Set end of work hours for today or anyday"""
    if date is None and time is None:
        date = datetime.now()
    elif date is None:
        date = datetime.today()
        date = date.replace(hour=int(time.split(":")[0]),
                            minute=int(time.split(":")[1]))
    else:  # manual spec of date and time
        date = datetime.fromisoformat(date)
        date = date.replace(hour=int(time.split(":")[0]),
                            minute=int(time.split(":")[1]))

    write_end(date)
    clock_out(date)


@app.command()
def status(format: Annotated[Optional[str], typer.Argument()] = None):
    # TODO: add check for format to be one of the supported formats
    status_view()


@app.command()
def hours(format: Annotated[Optional[str], typer.Argument()] = None):
    if format is None:
        format = "table"
    format = format.lower()

    # TODO: add check for format to be one of the supported formats
    if format == "table":
        table = Table()
        df = read()


if __name__ == "__main__":
    app()
