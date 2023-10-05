# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2023)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

"""
Alternative implementations: using logging.Filter or logging.LoggerAdapter.
"""
import logging as lggg
import sys as sstm
from pathlib import Path as path_t
from typing import Callable, Literal, TextIO

from rich.console import Console as console_t

from logger_36.config import LOGGER_NAME
from logger_36.constant import MAX_DETAIL_NAME_LENGTH, SYSTEM_DETAILS
from logger_36.measure.memory import CanCheckMemory
from logger_36.measure.memory import FormattedUsage as FormattedMemoryUsage
from logger_36.type.console import console_handler_t
from logger_36.type.file import file_handler_t
from logger_36.type.generic import can_show_message_p, generic_handler_t

LOGGER = lggg.getLogger(name=LOGGER_NAME)
LOGGER.setLevel(lggg.DEBUG)
LOGGER.addHandler(console_handler_t(level=lggg.INFO))


def AddFileHandler(
    path: str | path_t, /, *args, level: int = lggg.INFO, **kwargs
) -> None:
    """"""
    if isinstance(path, str):
        path = path_t(path)
    if path.exists():
        raise ValueError(f"{path}: File already exists")

    handler = file_handler_t(path, *args, **kwargs)
    handler.setLevel(level)
    LOGGER.addHandler(handler)


def AddGenericHandler(
    interface: can_show_message_p | Callable[[str], None],
    /,
    *args,
    level: int = lggg.INFO,
    supports_html: bool = False,
    **kwargs,
) -> None:
    """"""
    handler = generic_handler_t(interface, *args, supports_html=supports_html, **kwargs)
    handler.setLevel(level)
    LOGGER.addHandler(handler)


def SetLOGLevel(level: int, /, *, which: Literal["c", "f", "a"] = "a") -> None:
    """
    which: c=console, f=file, a=all
    """
    if which not in "cfa":
        raise ValueError(
            f"{which}: Invalid handler specifier. "
            f'Expected="c" for console, "f" for file, or "a" for all'
        )

    for handler in LOGGER.handlers:
        if (
            (which == "a")
            or ((which == "c") and isinstance(handler, console_handler_t))
            or ((which == "f") and isinstance(handler, file_handler_t))
        ):
            handler.setLevel(level)


def SetExitOnError(exit_on_error: bool, /) -> None:
    """"""
    for handler in LOGGER.handlers:
        if hasattr(handler, "exit_on_error"):
            handler.exit_on_error = exit_on_error


def SetShowMemoryUsage(show_memory_usage: bool, /) -> None:
    """"""
    if show_memory_usage and not CanCheckMemory():
        LOGGER.warning('Cannot show memory usage: Package "psutil" not installed')
        return

    for handler in LOGGER.handlers:
        if hasattr(handler, "show_memory_usage"):
            handler.show_memory_usage = show_memory_usage


def MaximumUsage(
    *, unit: Literal["b", "k", "m", "g", "a"] | None = "a", decimals: int = None
) -> tuple[int | float, str]:
    """
    unit: b or None=bytes, k=kilo, m=mega, g=giga, a=auto
    """
    usage = max(getattr(_hdr, "max_memory_usage", -1) for _hdr in LOGGER.handlers)
    return FormattedMemoryUsage(usage, unit=unit, decimals=decimals)


def LogSystemDetails() -> None:
    """"""
    details = "\n".join(
        f"    {_key:>{MAX_DETAIL_NAME_LENGTH}}: {_vle}"
        for _key, _vle in SYSTEM_DETAILS.items()
    )

    modules = sstm.modules
    with_versions = []
    max_length = 0
    m_idx = 0
    for name in sorted(modules.keys(), key=str.lower):
        if name.startswith("_") or ("." in name):
            continue

        module = modules[name]
        version = getattr(module, "__version__", None)
        if version is None:
            continue

        if (m_idx > 0) and (m_idx % 4 == 0):
            with_versions.append("\n")
        with_versions.append(f"{name}={version}")
        max_length = max(max_length, name.__len__() + version.__len__() + 1)
        m_idx += 1

    max_length += 4
    AlignedInColumns = lambda _str: f"{_str:{max_length}}" if _str != "\n" else "\n    "
    with_versions = map(AlignedInColumns, with_versions)
    modules = "".join(with_versions)

    LOGGER.info(
        f"SYSTEM DETAILS\n"
        f"{details}\n"
        f"    {'Python Modules':>{MAX_DETAIL_NAME_LENGTH}}:\n"
        f"    {modules}"
    )


def SaveLOGasHTML(path: str | path_t | TextIO = None) -> None:
    """"""
    cannot_save = "Cannot save logging record as HTML"

    if path is None:
        for handler in LOGGER.handlers:
            if isinstance(handler, lggg.FileHandler):
                path = path_t(handler.baseFilename).with_suffix(".htm")
                break
        if path is None:
            LOGGER.warning(f"{cannot_save}: No file handler to build a filename from.")
            return
        if path.exists():
            LOGGER.warning(
                f'{cannot_save}: Automatically generated path "{path}" already exists.'
            )
            return
    elif isinstance(path, str):
        path = path_t(path)

    actual_file = isinstance(path, path_t)
    if actual_file and path.exists():
        LOGGER.warning(f'{cannot_save}: File "{path}" already exists.')
        return

    console = None
    found = False
    for handler in LOGGER.handlers:
        console = getattr(handler, "console", None)
        if found := isinstance(console, console_t):
            break

    if found:
        html = console.export_html()
        if actual_file:
            with open(path, "w") as accessor:
                accessor.write(html)
        else:
            path.write(html)
    else:
        LOGGER.warning(f"{cannot_save}: No handler has a RICH console.")
