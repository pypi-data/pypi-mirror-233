"""The ``utils`` module contains tools used to perform common tasks in the audio
processing."""  # noqa: D205, D209

from enum import Enum

import numpy as np


class Criterion(Enum):
    """Represents a mathematical criterion.

    Some kinds of calculations can be done in different ways and often we want to have
    control over the way they are
    done. For example, when calculating the RMS of a signal, we can either take
    the maximum value of the RMS of each channel, or the mean value of the RMS of
    each channel.

    The following values are available:

    * ``MAX``: which value is the string ``'max'``.
    * ``MIN``: which value is the string ``'min'``.
    * ``MEAN``: which value is the string ``'mean'``.

    """

    MAX = "max"
    MIN = "min"
    MEAN = "mean"


def db_to_pcm(decibels: int, bit_depth: int) -> int:
    r"""Convert a dB value to a float value.

    The dB value is converted to a PCM value using the following formula:

    .. math::

        \text{PCM} = \left\lfloor 2^{bit\_depth - 1} \times 10^{\frac{decibels}{20}}
        \right\rceil

    where :math:`\lfloor x \rceil` is the *round* function, which approximates the
    result to the nearest integer (it introduces the quantization error).

    Parameters
    ----------
    decibels : int
        The dB value to convert.
    bit_depth : int
        The bit depth of the PCM value, this is used to calculate the maximum value of
        the PCM value.

    Returns
    -------
    int
        The PCM value corresponding to the given dB value.

    """
    return round(10 ** (decibels / 20) * 2 ** (bit_depth - 1))


def pcm_to_db(pcm: int | float, bit_depth: int) -> float:
    r"""Convert the given signal power to a dB value.

    The PCM value is converted to a dB value using the following formula:

    .. math::

        db = 20 \times log_{10}\left(\frac{\text{PCM}}{2^{bit\_depth - 1}}\right)

    Parameters
    ----------
    pcm : int
        The PCM value to convert.
    bit_depth : int
        The bit depth of the PCM value, this is used to calculate the maximum value of
        the PCM value.

    Returns
    -------
    float
        The dB value corresponding to the given PCM value.


    Notes
    -----
    Due to the formula the result on input ``0`` should be ``-inf``, nonetheless,
    as we are threating discrete quantities, we return the minimum value that can be
    represented by the given bit depth based on the following table:

    +---------+--------------------+
    | Bit     | Minimum value (dB) |
    +=========+====================+
    | 16      | -98                |
    +---------+--------------------+
    | 24      | -146               |
    +---------+--------------------+
    | 32      | -194               |
    +---------+--------------------+

    for a more detailed explanation see about `audio bit depth
    <https://en.wikipedia.org/wiki/Audio_bit_depth#Quantization>`_.

    """
    min_val = {
        "16": -98,
        "24": -146,
        "32": -194,
    }

    if pcm == 0:
        return min_val[str(bit_depth)]

    return 20 * np.log10(abs(pcm / 2 ** (bit_depth - 1)))


def rms(array: np.ndarray) -> float:
    r"""Calculate the RMS of the given array.

    The Root Mean Square (RMS) is the square root of the mean of the squares of the
    values in the array. It is a measure of the magnitude of a signal.
    It is calculated using the following formula:

    .. math::

        \text{RMS} = \sqrt{\frac{1}{n} \sum_{i=1}^{n} x_i^2}

    where :math:`x_i` is the value of the array at index :math:`i` and :math:`n` is the
    length of the array.

    Parameters
    ----------
    array : np.ndarray
        The array to calculate the RMS of.

    Returns
    -------
    float
        The RMS of the given array.

    """
    mean_squares = np.square(array).mean()
    if mean_squares == 0:
        return 0
    return np.sqrt(mean_squares)


def get_last_index(haystack: np.ndarray, threshold) -> int | tuple | None:
    """Get the index of the last occurrence of a value greater than ``threshold`` in the
    given array.

    Parameters
    ----------
    haystack : np.ndarray
        the array to inspect
    threshold : int
        the threshold to use

    Returns
    -------
    int | tuple | None
        The index of the last occurrence of a value greater than the given limit in the
        array, if the array is multi-dimensional it returns a tuple. If there is no
        match, None is returned

    """  # noqa: D205
    positions = np.where(haystack >= threshold)
    indexes = positions[0]
    if indexes.size == 0:
        return None
    if len(positions) > 1:
        return list(zip(*positions, strict=False))[-1]
    return indexes[-1]
