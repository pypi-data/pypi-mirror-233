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
from typing import ClassVar

from rich.color import Color as color_t
from rich.console import Console as console_t
from rich.markup import escape as PreProcessedForRich
from rich.style import Style as style_t
from rich.text import Text as text_t

from logger_36.config import ELAPSED_TIME_SEPARATOR, LEVEL_CLOSING, WHERE_SEPARATOR
from logger_36.constant import DATE_TIME_LENGTH
from logger_36.type.extension import handler_extension_t


class console_handler_t(lggg.Handler, handler_extension_t):
    TAB_SIZE: ClassVar[int] = 5  # => CONTEXT_SEPARATOR aligned for all log levels.
    DATE_TIME_COLOR: ClassVar[str] = "dodger_blue2"
    LEVEL_COLOR: ClassVar[dict[int, str | style_t]] = {
        lggg.DEBUG: "orchid",
        lggg.INFO: "white",
        lggg.WARNING: "yellow",
        lggg.ERROR: "orange1",
        lggg.CRITICAL: "red",
    }
    ELAPSED_TIME_COLOR: ClassVar[str] = "green"
    ACTUAL_COLOR: ClassVar[str] = "red"
    EXPECTED_COLOR: ClassVar[str] = "green"
    GRAY_STYLE: ClassVar[style_t] = style_t(color=color_t.from_rgb(150, 150, 150))
    ACTUAL_PATTERNS: ClassVar[tuple[str]] = (r" Actual=[^.]+;",)
    EXPECTED_PATTERNS: ClassVar[tuple[str]] = (r" Expected([!<>]=|: )[^.]+\.",)

    console: console_t

    def __init__(self, /, *, level: int = lggg.NOTSET) -> None:
        """"""
        lggg.Handler.__init__(self, level=level)
        handler_extension_t.__init__(self)

        self.setFormatter(self.formatter)
        self.console = console_t(
            tab_size=self.__class__.TAB_SIZE,
            highlight=False,
            force_terminal=True,
            record=True,
        )

    def emit(self, record: lggg.LogRecord, /) -> None:
        """"""
        first_line, next_lines = self.MessageLines(
            record, PreProcessed=PreProcessedForRich
        )
        highlighted = self.__class__.HighlightedVersion(
            first_line, next_lines, record.levelno
        )
        self.console.print(highlighted, crop=False, overflow="ignore")

        self.ExitOrNotIfError(record)

    @classmethod
    def HighlightedVersion(
        cls, first_line: str, next_lines: str | None, log_level: int, /
    ) -> text_t:
        """"""
        output = text_t(first_line)

        # Used instead of _CONTEXT_LENGTH which might include \t, thus creating a
        # mismatch between character length and length when displayed in console.
        context_end = first_line.find(LEVEL_CLOSING)
        elapsed_time_separator = first_line.rfind(ELAPSED_TIME_SEPARATOR)
        where_separator = first_line.rfind(
            WHERE_SEPARATOR, context_end, elapsed_time_separator
        )

        output.stylize(cls.DATE_TIME_COLOR, end=DATE_TIME_LENGTH)
        output.stylize(
            cls.LEVEL_COLOR[log_level],
            start=DATE_TIME_LENGTH,
            end=context_end + 1,
        )
        output.stylize(
            cls.GRAY_STYLE, start=where_separator, end=elapsed_time_separator
        )
        output.stylize(cls.ELAPSED_TIME_COLOR, start=elapsed_time_separator)

        if next_lines is not None:
            output.append(next_lines)

        output.highlight_words(cls.ACTUAL_PATTERNS, style=cls.ACTUAL_COLOR)
        output.highlight_words(cls.EXPECTED_PATTERNS, style=cls.EXPECTED_COLOR)

        return output
