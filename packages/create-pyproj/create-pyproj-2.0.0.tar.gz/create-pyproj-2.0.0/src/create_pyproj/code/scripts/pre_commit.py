"""Module Description.

pre-commit after running semantic_release
"""
import logging
import sys
from pathlib import Path

logger = logging.getLogger(__name__)


def read_version(VERSIONPATH: Path) -> str:
    with open(VERSIONPATH / "VERSION", "r") as f:
        VERSION = f.read().strip()
    return VERSION


def write_version(version: str, VERSIONPATH: Path) -> None:
    with open(VERSIONPATH / "VERSION", "w") as f:
        f.write(version)


def resolve_file_path(FILEPATH: Path = None, attempt: int = 0) -> Path:
    """Find the VERSION file in the current directory or its parents.

    Args:
        VERSIONPATH (Path, optional): The current path to the file. Defaults to None.
        attempt (int, optional): The current attempt. Defaults to 0.

    Returns:
        Path: The path of the file
    """
    filename = "VERSION"
    if not FILEPATH:
        FILEPATH = Path.cwd()

    if attempt == 3:
        raise FileNotFoundError(
            f"Could not find {filename} file in {FILEPATH} after 3 attempts"
        )

    if (FILEPATH / filename).exists():
        return FILEPATH

    FILEPATH = FILEPATH.parent
    attempt += 1
    return resolve_file_path(VERSIONPATH, attempt)


if __name__ == "__main__":
    version = sys.argv[1]
    VERSIONPATH = resolve_file_path()
    write_version(version, VERSIONPATH)
