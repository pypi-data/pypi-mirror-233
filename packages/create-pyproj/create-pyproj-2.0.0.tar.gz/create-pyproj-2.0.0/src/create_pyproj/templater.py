"""Module Description."""
import logging
from pathlib import Path

from mako.template import Template

DIR = Path(__file__).parent.absolute()

logger = logging.getLogger(__name__)


def writeTemplate(
    filename: str,
    outputpath: Path,
    data: dict = {},
    templatepath: Path = None,
    templateroot: Path = DIR / "templates",
) -> None:
    """Write a template file to the outputpath.

    Args:
        filename (str): The name of the file to write.
        outputpath (Path): The path to write the file to.
        data (dict, optional): The data to pass to the template. Defaults to {}.
        templatepath (Path, optional): The path to the template file. Defaults to None.
        templateroot (Path, optional): The root path to the templates.
            Defaults to DIR / "templates".
    """
    if templatepath is None:
        path = templateroot
    else:
        path = templateroot / templatepath

    template = str(path / f"{filename}.tmpl")
    mytemplate = Template(filename=template, output_encoding="utf-8")
    outputpath.mkdir(exist_ok=True, parents=True)
    (outputpath / filename).write_bytes(mytemplate.render(**data))
