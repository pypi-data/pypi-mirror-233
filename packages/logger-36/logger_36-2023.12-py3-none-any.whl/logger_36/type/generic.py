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
from typing import Callable, Protocol

from rich.console import Console as console_t
from rich.markup import escape as PreProcessedForRich
from rich.terminal_theme import DEFAULT_TERMINAL_THEME

from logger_36.type.console import console_handler_t
from logger_36.type.extension import handler_extension_t


class can_show_message_p(Protocol):
    def Show(self, message: str, /) -> None:
        ...


class generic_handler_t(lggg.Handler, handler_extension_t):
    __slots__ = ("console", "Show")
    console: console_t | None
    Show: Callable[[str], None]

    def __init__(
        self,
        interface: can_show_message_p | Callable[[str], None],
        /,
        *args,
        supports_html: bool = False,
        **kwargs,
    ) -> None:
        """"""
        lggg.Handler.__init__(self, *args, **kwargs)
        handler_extension_t.__init__(self)

        if supports_html:
            self.console = console_t(
                tab_size=console_handler_t.TAB_SIZE,
                highlight=False,
                force_terminal=True,
            )
        else:
            self.console = None
        if hasattr(interface, "Show"):
            self.Show = interface.Show
        else:
            self.Show = interface
        self.setFormatter(self.formatter)

    def emit(self, record: lggg.LogRecord, /) -> None:
        """"""
        if self.console is None:
            message, _ = self.MessageLines(record, should_fully_format=True)
        else:
            first_line, next_lines = self.MessageLines(
                record, PreProcessed=PreProcessedForRich
            )
            highlighted = console_handler_t.HighlightedVersion(
                first_line, next_lines, record.levelno
            )
            segments = self.console.render(highlighted)

            # Inspired from the code of: rich.console.export_html.
            html_segments = []
            for text, style, _ in segments:
                if text == "\n":
                    html_segments.append("\n")
                else:
                    if style is not None:
                        style = style.get_html_style(DEFAULT_TERMINAL_THEME)
                        if (style is not None) and (style.__len__() > 0):
                            text = f'<span style="{style}">{text}</span>'
                    html_segments.append(text)
            if html_segments[-1] == "\n":
                html_segments = html_segments[:-1]

            # /!\ For some reason, the widget splits the message into lines, place each line
            # inside a pre tag, and set margin-bottom of the first and list lines to 12px.
            # This can be seen by printing self.contents.toHtml(). To avoid the unwanted
            # extra margins, margin-bottom is set to 0 below.
            message = (
                "<pre style='margin-bottom:0px'>" + "".join(html_segments) + "</pre>"
            )

        self.Show(message)

        self.ExitOrNotIfError(record)
