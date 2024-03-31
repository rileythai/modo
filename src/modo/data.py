from typing import Optional
import os
from datetime import datetime
import pandas as pd
"""
We have to write a db file in some form, which we can start as parquet 
and update to support numerous methods
"""


def init_file():
    """Create the default empty file"""
    datapath = f"{os.getenv('HOME')}/.local/share/modo/hours.parquet"
    os.makedirs(os.path.dirname(datapath), exist_ok=True)
    df = pd.DataFrame(columns=["date", "start", "end", "note"])
    df = df.set_index("date")

    # TODO: read file format and datapath based on config file
    save(df)


def read() -> pd.DataFrame:
    """Reads data file"""
    # TODO: read file format and datapath based on config file
    return pd.read_parquet(
        f"{os.getenv('HOME')}/.local/share/modo/hours.parquet")


def save(df: pd.DataFrame) -> None:
    """Wrapper for df write"""
    # TODO: read file format and datapath based on config file
    df.to_parquet(f"{os.getenv('HOME')}/.local/share/modo/hours.parquet")


def get_today(time: Optional[str] = None) -> pd.Series | None:
    """Gets a given date's data, defaulting to today. Returns None if doesn't exist"""
    df = read()
    # TODO: index via config's chosen format
    if time is None:
        today = datetime.today().date().isoformat()
    else:
        today = time
    try:
        return df.loc[today]
    except KeyError:
        return None


def test():
    write(date="2023-04-19", start="09:33", end="11:40")
    df = read()
    print(df)
    write(date="2023-04-20", start="09:33", note="foobar")
    df = read()
    print(df)
    write(date="2023-04-20", start="09:33", end="10:40")
    df = read()
    print(df)


def write(**kwargs) -> None:
    """Write a row to the dataframe"""
    df = read()
    patch = [None] * len(df.columns)  # has to be preassigned

    # ensure date is set
    try:
        date = kwargs["date"]
    except KeyError:
        raise ValueError("must specify a date for patch")

    # create patch from attributes
    for i, col in enumerate(df.columns):
        try:
            patch[i] = kwargs[col]
        except KeyError:
            continue

    # append current data if exists, else just patch
    try:
        current = df.loc[date]
        for i, part in enumerate(current):
            if patch[i] is None:
                patch[i] = current[i]

    except KeyError:
        pass
    df.loc[date] = patch

    save(df)


def write_start(time: datetime) -> None:
    """Write a start time via datetime object."""
    date = time.date().isoformat()
    start = time.time().isoformat()[:5]
    write(date=date, start=start)


def write_end(time: datetime) -> None:
    """Write a end time via datetime object."""
    date = time.date().isoformat()
    end = time.time().isoformat()[:5]
    write(date=date, end=end)
