from typing_extensions import Annotated
from typing import Optional
import os
from datetime import datetime

import typer
import rich
from rich import print
from rich.panel import Panel
from rich.table import Table

from .util import visuals
from .data import get_today, write, init_file

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

    # date not specified
    if date is None:
        date = datetime.now()
    # date specified
    else:
        date = datetime.fromisoformat(date)

    # time is specified
    if time is not None:
        date = date.replace(hour=int(time.split(":")[0]),
                            minute=int(time.split(":")[1]))
    else:
        pass
        # date = datetime.now()

    print(
        Panel(
            f"\n\n:clock{date.hour if date.hour < 13 else date.hour - 12}: [bold green]Clock in set to {date.hour}:{date.minute}\n\n",
            title=visuals["title"],
            # TODO: change to work if time and date are specified properly
            subtitle=datetime.today().date().isoformat(),
            highlight=True,
        ))
    write(date=date.date().isoformat(), start=time)


@app.command()
def bye(
    time: Annotated[Optional[str], typer.Argument()] = None,
    date: Annotated[Optional[str],
                    typer.Option(help="Date to log for")] = None,
):
    """Set end of work hours for today or anyday"""
    if time is None:
        time = datetime.now().time()
    else:
        if date is None:
            date = datetime.today()
            time.hour = time.split(":")[0]
            time.minute = time.split(":")[1]
        else:
            date = datetime.today()
            time = date.time()

    print(
        Panel(
            f"\n\n:clock{time.hour if time.hour < 13 else time.hour - 12}: [bold red]Clock out set to {time.hour}:{time.minute}\n\n",
            title=visuals["title"],
            subtitle=datetime.today().date().isoformat(),
            highlight=True,
        ))
    status()
    write(date=date, end=time)


@app.command()
def status(format: Annotated[Optional[str], typer.Argument()] = None):
    if format is None:
        format = "table"
    format = format.lower()

    # TODO: add check for format to be one of the supported formats
    if format == "table":
        table = Table()
        data = get_today()
        if data is None:
            print(
                Panel(
                    "\n\n[bold red] :stop_sign: No log for today.\n\n",
                    title=visuals["title"],
                ))
            return
        else:
            try:
                # TODO: move to diff function in util
                # TODO: add support for NON 24h calculation
                hoursi, mini = data["start"].split(":")
                hoursf, minf = data["end"].split(":")
                if minf < mini:
                    minf += 60
                    hoursf -= 1

                # TODO: make it so it doesn't do it wrong and spit out -15 or 0 hours or 0 mins (non-plural)
                time_worked = f"{hoursf - hoursi} hours, {hoursf-hoursi} mins"
            except KeyError:
                time_worked = None

            table.add_column(
                "Total hours worked",
                justify="right",
                style="cyan",
            )
            table.add_column(time_worked, style="magenta")
            for q in data.index:
                table.add_row(q, data[q])
            print(Panel(
                table,
                title=visuals["title"],
                subtitle=data.name,
            ))


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
