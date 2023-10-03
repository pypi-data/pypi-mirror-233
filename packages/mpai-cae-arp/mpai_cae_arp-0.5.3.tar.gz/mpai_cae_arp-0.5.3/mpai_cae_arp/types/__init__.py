"""The types module contains the data types specified in the MPAI-CAE-ARP standard.

Here we have the following data types:

- :class:`Irregularity`: an event of interest that has been detected in the audio or
  video signal.
- :class:`IrregularityFile`: a file containing a list of irregularities that is used to
   exchange messages between the different components of the system.
- :class:`IrregularityProperties`: a set of properties that describe an irregularity
   (only for audio ones).
- :class:`IrregularityType`: the type of irregularity.
- :class:`Restoration`: a restoration that has been applied to the audio signal.
- :class:`EditingList`: a list of restorations.

"""

from . import schema
from ._irregularity import (
    Irregularity,
    IrregularityFile,
    IrregularityProperties,
    IrregularityType,
    Source,
)
from ._restoration import EditingList, Restoration

__all__ = [
    "Irregularity",
    "IrregularityFile",
    "IrregularityProperties",
    "IrregularityType",
    "Restoration",
    "EditingList",
    "schema",
    "Source",
]
