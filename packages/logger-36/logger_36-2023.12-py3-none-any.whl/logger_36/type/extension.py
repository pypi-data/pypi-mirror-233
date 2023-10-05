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

import logging as lggg
import sys as sstm
from typing import Callable

from logger_36.config import DATE_TIME_FORMAT, MESSAGE_FORMAT
from logger_36.constant import LOG_LEVEL_LENGTH, NEXT_LINE_PROLOGUE
from logger_36.measure.chronos import ElapsedTime
from logger_36.measure.memory import CurrentUsage as CurrentMemoryUsage
from logger_36.measure.memory import WithAutoUnit as MemoryWithAutoUnit


class handler_extension_t:
    __slots__ = ("formatter", "show_memory_usage", "max_memory_usage", "exit_on_error")
    formatter: lggg.Formatter
    show_memory_usage: bool
    max_memory_usage: int
    exit_on_error: bool

    def __init__(self) -> None:
        """"""
        self.formatter = lggg.Formatter(fmt=MESSAGE_FORMAT, datefmt=DATE_TIME_FORMAT)
        self.show_memory_usage = False
        self.max_memory_usage = -1
        self.exit_on_error = False

    def MessageLines(
        self,
        record: lggg.LogRecord,
        /,
        *,
        PreProcessed: Callable[[str], str] | None = None,
        should_fully_format: bool = False,
    ) -> tuple[str, str | None]:
        """
        Note: "message" is not yet an attribute of record (it will be set by format());
        Use "msg" instead.
        """
        if not isinstance(record.msg, str):
            record.msg = str(record.msg)
        if PreProcessed is not None:
            record.msg = PreProcessed(record.msg)
        if "\n" in record.msg:
            original_message = record.msg
            lines = original_message.splitlines()
            record.msg = lines[0]
            next_lines = NEXT_LINE_PROLOGUE.join(lines[1:])
            next_lines = f"{NEXT_LINE_PROLOGUE}{next_lines}"
        else:
            original_message = next_lines = None

        # The record is shared between handlers, so do not re-assign if already there.
        if not hasattr(record, "elapsed_time"):
            record.elapsed_time = ElapsedTime()
        # Re-assign for each handler in case they have different show properties.
        if self.show_memory_usage:
            record.memory_usage = self.FormattedMemoryUsage()
        else:
            record.memory_usage = ""

        padding = (LOG_LEVEL_LENGTH - record.levelname.__len__() - 1) * " "
        first_line = self.formatter.format(record).replace("\t", padding)

        # Revert the record message to its original value for subsequent handlers.
        if original_message is not None:
            record.msg = original_message

        if should_fully_format:
            if next_lines is None:
                return first_line, None
            else:
                return f"{first_line}{next_lines}", None
        else:
            return first_line, next_lines

    def FormattedMemoryUsage(self) -> str:
        """"""
        if self.show_memory_usage:
            usage = CurrentMemoryUsage()
            if usage > self.max_memory_usage:
                self.max_memory_usage = usage

            usage, unit = MemoryWithAutoUnit(usage, 1)

            return f" :{usage}{unit}"
        else:
            return ""

    def ExitOrNotIfError(self, record: lggg.LogRecord, /) -> None:
        """"""
        if self.exit_on_error and (record.levelno in (lggg.ERROR, lggg.CRITICAL)):
            sstm.exit(1)
