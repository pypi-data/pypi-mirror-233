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

import platform as pltf
from datetime import datetime as dttm

from logger_36.config import (
    CONTEXT_SEPARATOR,
    DATE_TIME_FORMAT,
    LEVEL_CLOSING,
    LEVEL_OPENING,
    SYSTEM_DETAILS,
)

# This module is certainly imported early. Therefore, the current time should be close
# enough to the real start time.
START_TIME = dttm.now()

DATE_TIME_LENGTH = START_TIME.strftime(DATE_TIME_FORMAT).__len__()
LOG_LEVEL_LENGTH = (
    max(map(len, ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")))
    + LEVEL_OPENING.__len__()
    + LEVEL_CLOSING.__len__()
)
CONTEXT_LENGTH = DATE_TIME_LENGTH + LOG_LEVEL_LENGTH
NEXT_LINE_PROLOGUE = "\n" + (CONTEXT_LENGTH + CONTEXT_SEPARATOR.__len__() + 1) * " "

SYSTEM_DETAILS = {_dtl.capitalize(): getattr(pltf, _dtl)() for _dtl in SYSTEM_DETAILS}
MAX_DETAIL_NAME_LENGTH = max(map(len, SYSTEM_DETAILS.keys()))
