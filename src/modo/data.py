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
    # TODO: set datapath from config
    # https://unix.stackexchange.com/questions/312988/understanding-home-configuration-file-locations-config-and-local-sha
    datapath = f"{os.getenv('HOME')}/.local/share/modo/hours.parquet"
    os.makedirs(os.path.dirname(datapath), exist_ok=True)
    df = pd.DataFrame(columns=["date", "start", "end", "note"])

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
    mask = df['date'] == today
    try:
        return df[mask].iloc[0]
    except KeyError:
        return None


def get_between_dates(start_date: str, end_date: str) -> pd.DataFrame:
    """Get between different dates"""
    df = read()
    mask = (df['date'] > start_date) & (df['date'] <= end_date)
    dff = df[mask]
    return dff if len(dff) > 0 else None


def write(**patch) -> None:
    """Write a row to the dataframe"""
    # TODO: change this to not use pandas at all
    df = read()
    columns = ['date', 'start', 'end', 'note']

    # ensure date is set
    try:
        date = patch["date"]
    except KeyError:
        raise ValueError("error in write, date isn't specified for entry")

    patch.update((k, None) for k in columns if k not in patch.keys())

    # append current data if exists, else just patch
    try:
        current = df[df['date'] == date]
        assert len(current) > 0, 'zero length exit case'

        # if we're two entries on a day, then we need to get the last one
        if len(current) > 1:
            current = current[current.index == current.index.values[-1]]

        # add if not in the current
        for col in current.columns:
            if current[col].values[0] is None:
                print('adding', patch[col], 'to', col)
                current[col] = [patch[col]]
        df.iloc[current.index.values[0]] = current.iloc[0]  # set to series

    except AssertionError as e:
        df = pd.concat((df, pd.DataFrame(dict(**patch), index=pd.Index([0]))),
                       axis=0,
                       ignore_index=True)
    finally:
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
