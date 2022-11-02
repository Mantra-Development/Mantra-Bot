import math
import re
from datetime import datetime, timedelta

import lightbulb


class TimeError(lightbulb.LightbulbError):
    pass


time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}

ordinal = lambda n: "%d%s" % (
    n,
    "tsnrhtdd"[(math.floor(n / 10) % 10 != 1) * (n % 10 < 4) * n % 10 :: 4],
)


steps = dict(
    year=timedelta(days=365),
    week=timedelta(days=7),
    day=timedelta(days=1),
    hour=timedelta(hours=1),
    minute=timedelta(minutes=1),
    second=timedelta(seconds=1),
    millisecond=timedelta(milliseconds=1),
)

steps_shortened = dict(
    y=timedelta(days=365),
    w=timedelta(days=7),
    d=timedelta(days=1),
    h=timedelta(hours=1),
    m=timedelta(minutes=1),
    s=timedelta(seconds=1),
    ms=timedelta(milliseconds=1),
)


def pretty_timedelta_shortened(td: timedelta) -> str:
    """Returns a pretty shortened string of a timedelta"""

    if not isinstance(td, timedelta):
        raise ValueError(f"timedelta expected, '{type(td)}' given.")

    parts = []
    for name, span in steps_shortened.items():
        if td >= span:
            count = int(td / span)
            td -= count * span
            parts.append("{}{}".format(count, name))
            if len(parts) >= 2 or name == "s":
                break
        elif len(parts):
            break

    return " : ".join(parts)


def pretty_timedelta(td: timedelta) -> str:
    """Returns a pretty string of a timedelta"""

    if not isinstance(td, timedelta):
        raise ValueError("timedelta expected, '{}' given".format(type(td)))

    parts = []

    for name, span in steps.items():
        if td >= span:
            count = int(td / span)
            td -= count * span
            parts.append("{} {}{}".format(count, name, "s" if count > 1 else ""))
            if len(parts) >= 2 or name == "second":
                break
        elif len(parts):
            break

    return ", ".join(parts)


def pretty_seconds_shortened(s) -> str:
    return pretty_timedelta_shortened(timedelta(seconds=s))


def pretty_seconds(s) -> str:
    return pretty_timedelta(timedelta(seconds=s))


def pretty_datetime(dt: datetime, ignore_time=False) -> str:
    if not isinstance(dt, datetime):
        raise ValueError("datetime expected, '{}' given".format(type(dt)))

    return "{0} {1}".format(
        ordinal(int(dt.strftime("%d"))),
        dt.strftime("%b %Y" + ("" if ignore_time else " %H:%M")),
    )


def time_converter(argument: str) -> float:
    """Function that converts given time into seconds.
    Parameters
    ----------
    argument : str
        Time to be converted
    Returns
    -------
    float
        Time in seconds.
    Raises
    ------
    TimeError
        When the values are wrong and when the input doesn't match the input regex.
    """
    args = argument.lower()
    matches = re.findall(time_regex, args)
    time = 0
    for v, k in matches:
        try:
            time += time_dict[k] * float(v)
        except KeyError:
            raise TimeError("{} is an invalid time-key! h/m/s/d are valid!".format(k))
        except ValueError:
            raise TimeError("{} is not a number!".format(v))
    return time
