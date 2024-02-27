from pathlib import Path


def relative_to(path: Path, other: Path):
    if path.is_relative_to(other):
        return path.relative_to(other)
    return path


def relative_to_cwd(path: Path):
    return relative_to(path, Path.cwd())
