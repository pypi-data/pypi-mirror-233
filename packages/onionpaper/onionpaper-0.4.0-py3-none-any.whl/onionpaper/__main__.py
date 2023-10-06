import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import click
import humanfriendly
import yaml

from .ctypes import Action, Config, logger
from .core import trace as trace_internal

datetime_format: str = "%Y-%m-%dT%H:%M:%S"
loop_default: bool = False
stop_at_default: Optional[str] = "no:1"


# noinspection PyShadowingBuiltins
@click.command()
@click.argument("input", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--stop-at", default=stop_at_default)
def trace(
    input: Path,
    stop_at: str = stop_at_default,
) -> None:
    text = input.read_text()
    obj = yaml.safe_load(text)

    config = obj.get("config", None)
    config = Config.create_from_dict(config) if config else None
    actions = obj.get("actions", [])
    actions = [Action.create_from_dict(action) for action in actions]

    stop_type, stop_target = stop_at.split(":", maxsplit=1)

    if stop_type == "no":
        stop_target = int(stop_target)
    elif stop_type == "uptime":
        stop_target = float(stop_target)
    elif stop_type == "time":
        try:
            stop_target = datetime.strptime(stop_target, datetime_format)
        except ValueError:
            try:
                stop_target_time = datetime.strptime(stop_target, "%H:%M:%S")
                stop_target = datetime.now()
                stop_target = datetime(
                    year=stop_target.year,
                    month=stop_target.month,
                    day=stop_target.day,
                    hour=stop_target_time.hour,
                    minute=stop_target_time.minute,
                    second=stop_target_time.second,
                )
            except ValueError:
                stop_target_time = datetime.strptime(stop_target, "%H:%M")
                stop_target = datetime.now()
                stop_target = datetime(
                    year=stop_target.year,
                    month=stop_target.month,
                    day=stop_target.day,
                    hour=stop_target_time.hour,
                    minute=stop_target_time.minute,
                    second=0,
                )

    counter = 0
    time_start = time.time()

    while True:
        trace_internal(actions=actions, config=config)

        counter += 1
        now = datetime.now()
        time_up = time.time() - time_start
        time_up_str = humanfriendly.format_timespan(time_up)

        logger.info(
            "[{}] no: {} | uptime: {}".format(
                now.strftime(datetime_format),
                str(counter).rjust(4, "0"),
                time_up_str,
            )
        )

        if stop_type == "no" and counter >= stop_target:
            break
        elif stop_type == "uptime" and time_up >= stop_target:
            break
        elif stop_type == "time" and now >= stop_target:
            break


if __name__ == "__main__":
    trace()


__all__ = [
    "trace",
]
