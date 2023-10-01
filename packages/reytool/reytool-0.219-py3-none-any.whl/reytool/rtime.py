# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-05 14:11:50
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Time methods.
"""


from typing import Any, Dict, Literal, Optional, Union, overload, NoReturn
from pandas import DataFrame
from time import (
    struct_time as time_struct_time,
    strftime as time_strftime,
    time as time_time,
    sleep as time_sleep
)
from datetime import (
    datetime as datetime_datetime,
    date as datetime_date,
    time as datetime_time,
    timedelta as datetime_timedelta
)

from .rbase import exc
from .rnumber import digits, randn
from .rregular import search
from .rtext import rprint


__all__ = (
    "now",
    "time_to",
    "extract_time_str",
    "to_time",
    "sleep",
    "RTimeMark"
)


@overload
def now(format: Literal["datetime"] = "datetime") -> datetime_datetime: ...

@overload
def now(format: Literal["date"] = "datetime") -> datetime_date: ...

@overload
def now(format: Literal["time"] = "datetime") -> datetime_time: ...

@overload
def now(format: Literal["datetime_str", "date_str", "time_str"] = "datetime") -> str: ...

@overload
def now(format: Literal["timestamp"] = "datetime") -> int: ...

def now(
    format: Literal[
        "datetime",
        "date",
        "time",
        "datetime_str",
        "date_str",
        "time_str",
        "timestamp"
    ] = "datetime"
) -> Union[
    datetime_datetime,
    datetime_date,
    datetime_time,
    str,
    int
]:
    """
    Get the `now` time.

    Parameters
    ----------
    format : Format type.
        - `Literal['datetime']` : Return datetime object of datetime package.
        - `Literal['date']` : Return date object of datetime package.
        - `Literal['time']` : Return time object of datetime package.
        - `Literal['datetime_str']` : Return string in format `'%Y-%m-%d %H:%M:%S'`.
        - `Literal['date_str']` : Return string in format `'%Y-%m-%d'`.
        - `Literal['time_str']` : Return string in foramt `'%H:%M:%S'`.
        - `Literal['timestamp']` : Return time stamp in milliseconds.

    Returns
    -------
    The now time.
    """

    # Return.
    if format == "datetime":
        return datetime_datetime.now()
    elif format == "date":
        return datetime_datetime.now().date()
    elif format == "time":
        return datetime_datetime.now().time()
    elif format == "datetime_str":
        return datetime_datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elif format == "date_str":
        return datetime_datetime.now().strftime("%Y-%m-%d")
    elif format == "time_str":
        return datetime_datetime.now().strftime("%H:%M:%S")
    elif format == "timestamp":
        return int(time_time() * 1000)
    else:
        exc(ValueError, format)


@overload
def time_to(
    obj: Union[
        datetime_datetime,
        datetime_date,
        datetime_time,
        datetime_timedelta,
        time_struct_time
    ],
    raising: bool = True
) -> str: ...

@overload
def time_to(
    obj: Any,
    raising: Literal[True] = True
) -> NoReturn: ...

@overload
def time_to(
    obj: Any,
    raising: Literal[False] = True
) -> Any: ...

def time_to(
    obj: Any,
    raising: bool = True
) -> Any:
    """
    `Convert` time object to text.

    Parameters
    ----------
    obj : Time object.
        - `datetime` : Text format is `'%Y-%m-%d %H:%M:%S'`.
        - `date` : Text format is `'%Y-%m-%d'`.
        - `time` : Text format is `'%H:%M:%S'`.
        - `struct_time` : Text format is `'%Y-%m-%d %H:%M:%S'`.

    raising : When parameter `obj` value error, whether throw exception, otherwise return original value.

    Returns
    -------
    Converted text.
    """

    # Type "datetime".
    if obj.__class__ == datetime_datetime:
        text = obj.strftime("%Y-%m-%d %H:%M:%S")

    # Type "date".
    elif obj.__class__ == datetime_date:
        text = obj.strftime("%Y-%m-%d")

    # Type "time".
    elif obj.__class__ == datetime_time:
        text = obj.strftime("%H:%M:%S")

    # Type "timedelta".
    elif obj.__class__ == datetime_timedelta:
        timestamp = obj.total_seconds()
        obj = datetime_datetime.fromtimestamp(timestamp).time()
        text = obj.strftime("%H:%M:%S")

    # Type "struct_time".
    elif obj.__class__ == time_struct_time:
        text = time_strftime("%Y-%m-%d %H:%M:%S", obj)

    # Raise.
    elif raising:
        exc(TypeError, obj)

    # Not raise.
    else:
        return obj

    return text


def extract_time_str(string: str) -> Optional[
    Union[
        datetime_datetime,
        datetime_date,
        datetime_time
    ]
]:
    """
    Extract time object from string.

    Parameters
    ----------
    string : String.

    Returns
    -------
    Object or null.
    """

    # Get parameter.
    time_obj = None
    str_len = len(string)

    # Extract.

    ## Standard.
    if str_len == 19:
        try:
            time_obj = datetime_datetime.strptime(string, "%Y-%m-%d %H:%M:%S")
        except ValueError: ...
    elif str_len == 10:
        try:
            time_obj = datetime_datetime.strptime(string, "%Y-%m-%d").date()
        except ValueError: ...
    elif str_len == 8:
        try:
            time_obj = datetime_datetime.strptime(string, "%H:%M:%S").time()
        except ValueError: ...
    if time_obj is not None:
        return time_obj

    ## Regular.

    ### Type "datetime".
    if 14 <= str_len <= 19:
        pattern = "^(\d{4})\S(\d{1,2})\S(\d{1,2}).(\d{1,2})\S(\d{1,2})\S(\d{1,2})$"
        result = search(pattern, string)
        if result is not None:
            year, month, day, hour, minute, second = [
                int(value)
                for value in result
            ]
            time_obj = datetime_datetime(year, month, day, hour, minute, second)
            return time_obj

    ### Type "date".
    if 8 <= str_len <= 10:
        pattern = "^(\d{4})\S(\d{1,2})\S(\d{1,2})$"
        result = search(pattern, string)
        if result is not None:
            year, month, day = [
                int(value)
                for value in result
            ]
            time_obj = datetime_date(year, month, day)
            return time_obj

    ### Type "time".
    if 5 <= str_len <= 8:
        pattern = "^(\d{1,2})\S(\d{1,2})\S(\d{1,2})$"
        result = search(pattern, string)
        if result is not None:
            hour, minute, second = [
                int(value)
                for value in result
            ]
            time_obj = datetime_time(hour, minute, second)
            return time_obj


@overload
def to_time(
    obj: str,
    raising: bool = True
) -> Union[datetime_datetime, datetime_date, datetime_time]: ...

@overload
def to_time(
    obj: time_struct_time,
    raising: bool = True
) -> datetime_datetime: ...

@overload
def to_time(
    obj: float,
    raising: bool = True
) -> datetime_datetime: ...

@overload
def to_time(
    obj: Any,
    raising: Literal[True] = True
) -> NoReturn: ...

@overload
def to_time(
    obj: Any,
    raising: Literal[False] = True
) -> Any: ...

def to_time(
    obj: Any,
    raising: bool = True
) -> Any:
    """
    `Convert` object to time object.

    Parameters
    ----------
    obj : Object.
    raising : When parameter `obj` value error, whether throw exception, otherwise return original value.

    Returns
    -------
    Time object.
    """

    # Type "str".
    if obj.__class__ == str:
        time_obj = extract_time_str(obj)

    # Type "struct_time".
    elif obj.__class__ == time_struct_time:
        time_obj = datetime_datetime(
            obj.tm_year,
            obj.tm_mon,
            obj.tm_mday,
            obj.tm_hour,
            obj.tm_min,
            obj.tm_sec
        )

    # Type "float".
    elif obj.__class__ in (int, float):
        int_len, _ = digits(obj)
        if int_len == 10:
            time_obj = datetime_datetime.fromtimestamp(obj)
        elif int_len == 13:
            time_obj = datetime_datetime.fromtimestamp(obj / 1000)
        else:
            time_obj = None

    # No time object.
    if time_obj is None:

        ## Raise.
        if raising:
            exc(ValueError, obj)

        ## Not raise.
        else:
            return obj

    return time_obj


def sleep(*thresholds: float, precision: Optional[int] = None) -> float:
    """
    `Sleep` random seconds.

    Parameters
    ----------
    thresholds : Low and high thresholds of random range, range contains thresholds.
        - When `length is 0`, then low and high thresholds is `0` and `10`.
        - When `length is 1`, then sleep this value.
        - When `length is 2`, then low and high thresholds is `thresholds[0]` and `thresholds[1]`.
    
    precision : Precision of random range, that is maximum decimal digits of sleep seconds.
        - `None` : Set to Maximum decimal digits of element of parameter `thresholds`.
        - `int` : Set to this value.
    
    Returns
    -------
    Random seconds.
        - When parameters `precision` is `0`, then return int.
        - When parameters `precision` is `greater than 0`, then return float.
    """

    # Handle parameter.
    if len(thresholds) == 1:
        second = float(thresholds[0])
    else:
        second = randn(*thresholds, precision=precision)

    # Sleep.
    time_sleep(second)

    return second


class RTimeMark():
    """
    Rey`s `time mark` type.
    """


    def __init__(self) -> None:
        """
        Build `time mark` instance.
        """

        # Record table.
        self.record: Dict[
            int,
            Dict[
                Literal[
                    "timestamp",
                    "datetime",
                    "timedelta",
                    "note"
                ],
                Any
            ]
        ] = {}


    def mark(self, note: Optional[str] = None) -> int:
        """
        `Marking` now time.

        Parameters
        ----------
        note : Mark note.

        Returns
        -------
        Mark index.
        """

        # Get parametes.

        # Mark.
        index = len(self.record)
        now_timestamp = now("timestamp")
        now_datetime = now("datetime")
        record = {
            "timestamp": now_timestamp,
            "datetime": now_datetime,
            "timedelta": None,
            "note": note
        }

        ## Not first.
        if index != 0:
            last_index = index - 1
            last_datetime = self.record[last_index]["datetime"]
            record["timedelta"] = now_datetime - last_datetime

        ## Record.
        self.record[index] = record

        return index


    def report(self, title: Optional[str] = None) -> DataFrame:
        """
        `Print` and `return` time mark information table.

        Parameters
        ----------
        title : Print title.
            - `None` : Not print.
            - `str` : Print and use this title.

        Returns
        -------
        Time mark information table
        """

        # Get parameter.
        record_len = len(self.record)
        data = [
            info.copy()
            for info in self.record.values()
        ]
        indexes = [
            index
            for index in self.record
        ]

        # Generate report.

        ## No record.
        if record_len == 0:
            row = dict.fromkeys(("timestamp", "datetime", "timedelta", "note"))
            data = [row]
            indexes = [0]

        ## Add total row.
        if record_len > 2:
            row = dict.fromkeys(("timestamp", "datetime", "timedelta", "note"))
            max_index = record_len - 1
            total_timedelta = self.record[max_index]["datetime"] - self.record[0]["datetime"]
            row["timedelta"] = total_timedelta
            data.append(row)
            indexes.append("total")

        ## Convert.
        for row in data:
            if row["timestamp"] is not None:
                row["timestamp"] = str(row["timestamp"])
            if row["datetime"] is not None:
                row["datetime"] = str(row["datetime"])[:-3]
            if row["timedelta"] is not None:
                timedelta_str = str(row["timedelta"])[:-3]
                timedelta_str = timedelta_str.rsplit(" ", 1)[-1]
                if timedelta_str[1] == ":":
                    timedelta_str = "0" + timedelta_str
                if row["timedelta"].days != 0:
                    timedelta_str = "%sday %s" % (
                        row["timedelta"].days,
                        timedelta_str
                    )
                row["timedelta"] = timedelta_str
        df_info = DataFrame(data, index=indexes)
        df_info.fillna("-", inplace=True)

        # Print.
        if title is not None:
            rprint(df_info, title=title)

        return df_info


    __call__ = mark