from datetime import timedelta
from pathlib import Path
import typing as t

from ._typealiases import SecondsT


def relative_to(path: Path, other: Path):
    if path.is_relative_to(other):  # TODO: 3.8 X
        return path.relative_to(other)
    return path


def relative_to_cwd(path: Path):
    return relative_to(path, Path.cwd())


def cast_seconds(seconds: t.Optional[SecondsT]):
    if isinstance(seconds, timedelta):
        return seconds.total_seconds()
    return seconds
