"""Functions to display information."""

from typing import Optional

from datetime import datetime

from rich import print
from rich.panel import Panel
from rich.table import Table
from rich.console import group

from .util import visuals
from .data import get_today


def panel(*args, **kwargs) -> Panel:
    """Wrapper for panel functionality with defaults."""
    return Panel(*args,
                 **kwargs,
                 title=visuals["title"],
                 highlight=True,
                 expand=False)


def clock_in(time: datetime) -> None:
    print(
        panel(
            f"\n\n:clock{time.hour if time.hour < 13 else time.hour - 12}: [bold green]Clock in set to {time.time().isoformat()[:5]}\n\n",
            subtitle=time.date().isoformat(),
        ))


@group()
def _clock_out(time: datetime):
    yield f"\n\n:clock{time.hour if time.hour < 13 else time.hour - 12}: [bold green]Clock out set to {time.time().isoformat()[:5]}\n\n"
    yield table_view(time.date().isoformat())


def clock_out(time: datetime) -> None:
    print(panel(_clock_out(time), subtitle=time.date().isoformat()))


def status_view(date: Optional[str] = None) -> None:
    if date is None:
        date = datetime.now().date().isoformat()
    print(panel(table_view(date), subtitle=date))


def table_view(date: Optional[str] = None) -> Table:
    if date is None:
        data = get_today()
    else:
        data = get_today(date)
    table = Table()
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
            hoursi, mini = map(int, data["start"].split(":"))
            hoursf, minf = map(int, data["end"].split(":"))
            if minf < mini:
                minf += 60
                hoursf -= 1

            # TODO: make it so it doesn't do it wrong and spit out -15 or 0 hours or 0 mins (non-plural)
            time_worked = f"{hoursf - hoursi} hours, {minf - mini} mins"
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
    return table
