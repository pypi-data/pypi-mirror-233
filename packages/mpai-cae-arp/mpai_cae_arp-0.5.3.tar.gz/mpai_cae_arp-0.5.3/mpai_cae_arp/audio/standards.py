"""Module containing enumerations of the standards used in the CAE-ARP standard."""
from enum import Enum


class EqualizationStandard(str, Enum):
    """An enumeration of the equalization standards used in the CAE-ARP standard.

    The following standards are available:

    - IEC
    - IEC1 (ex CCIR)
    - IEC2 (ex NAB)

    """

    IEC = "IEC"
    CCIR = "IEC1"
    NAB = "IEC2"


class SpeedStandard(float, Enum):
    """An enumeration of the tape playback speed standards used in the CAE-ARP standard.

    Options are:

    - 0.9375 ips
    - 1.875 ips
    - 3.75 ips
    - 7.5 ips
    - 15 ips
    - 30 ips

    """

    I = 0.9375  # noqa: E741
    II = 1.875
    III = 3.75
    IV = 7.5
    V = 15
    VI = 30
