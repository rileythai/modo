import os
from datetime import datetime
import pandas as pd
"""
We have to write a db file in some form, which we can start as parquet 
and update to support numerous methods
"""


def init_file():
    """Create the default empty file"""
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


def get_today() -> pd.Series | None:
    """Gets today's data. Returns None if doesn't exist"""
    df = read()
    # TODO: index via config's chosen format

    today = datetime.today().date().isoformat()
    try:
        return df.loc[today]
    except KeyError:
        return None


def test():
    df = read()
    today = datetime.today().date()
    df.loc[today] = [1, 2, None]
    print(df)
    print(df.index)


def write(**kwargs):
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
    except KeyError:
        pass
    df.loc[date] = patch

    # NOTE: this is a debug print
    print(df)
    save(df)
