import wave
from collections.abc import Callable, Iterable
from functools import lru_cache
from pathlib import Path
from typing import Annotated, Literal

import librosa
import numpy as np
from typing_extensions import Self, deprecated

from mpai_cae_arp.audio import utils
from mpai_cae_arp.audio._noise import Noise
from mpai_cae_arp.audio.utils import Criterion

Scale = Literal["db", "normal"]


class AudioWave:
    """A class to represent an audio wave.

    Attributes
    ----------
    bit : int
        the bit depth of the audio
    channels : int
        the number of channels of the audio
    samplerate : int
        the sample rate of the audio
    data : numpy.ndarray
        the data of the audio as a numpy array

    Raises
    ------
    ValueError
        if ``bit_depth`` is not 8, 16, 24 or 32
    ValueError
        if ``sample_rate`` is not between 8000 and 192000

    Examples
    --------
    Here is an example of how to create a new AudioWave object containing a sine wave
    with a frequency of 440 Hz, 44100 Hz sample rate, 16 bit depth and 1 channel:

    .. testcode::

        import numpy as np
        from mpai_cae_arp.audio import AudioWave

        freq = 440   # Hz
        sr = 44100   # sample rate
        bit = 16     # bit depth
        channels = 1 # number of channels

        # create an array of 1 second length
        time = np.arange(0, 1, 1/sr)

        # create a sine wave
        signal = np.sin(2 * np.pi * freq * time)

        # set the signal to the maximum value of the bit depth
        signal *= 2 ** (bit - 1)
        signal = np.int16(signal)

        # create the AudioWave object
        audio = AudioWave(signal, bit, channels, sr)

        print(audio)

    the code above will print the following output:

    .. testoutput::

        <AudioWave(bit: 16, chn: 1, sr: 44100)>

    """

    array: np.ndarray
    bit: int
    samplerate: int
    channels: int

    def __init__(
        self,
        data: np.ndarray,
        bit: int,
        channels: int,
        samplerate: Annotated[int, "Hz between 8000 and 192000"],
    ):
        if bit not in [8, 16, 24, 32]:
            msg = "bit must be 8, 16, 24 or 32"
            raise ValueError(msg)
        if samplerate not in range(8000, 192001):
            msg = "samplerate must be between 8 and 192 kHz"
            raise ValueError(msg)
        self.bit = bit
        self.channels = channels
        self.samplerate = samplerate
        self.array = data

    def __len__(self):
        return len(self.array)

    def __iter__(self):
        return iter(self.array)

    def __getitem__(self, key):
        return AudioWave(self.array[key], self.bit, self.channels, self.samplerate)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, AudioWave):
            return (
                np.array_equal(self.array, __o.array)
                and self.bit == __o.bit
                and self.channels == __o.channels
                and self.samplerate == __o.samplerate
            )
        msg = f"cannot compare AudioWave with {type(__o)}"
        raise TypeError(msg)

    def __repr__(self) -> str:
        return (
            f"<AudioWave(bit: {self.bit}, chn: {self.channels}, sr: {self.samplerate})>"
        )

    @classmethod
    def from_file(
        cls,
        filepath: str,
        bit: int | None = None,
        channels: int | None = None,
        samplerate: int | None = None,
        bufferize: bool = False,
    ) -> Self:
        """Generate an AudioWave object from a file.

        It reads the binary headers of the file to automatically get the
        bit depth, the number of channels and the sample rate. If any of
        these values is given, it will be used instead of the one read
        from the file.

        """
        if bufferize:
            data = None
            for chunk in AudioWave.buffer_generator_from_file(filepath):
                if data is None:
                    bit = chunk.bit
                    channels = chunk.channels
                    samplerate = chunk.samplerate
                    data = chunk.array
                else:
                    data = np.concatenate((data, chunk.array), axis=0)

            if any(x is None for x in [data, bit, channels, samplerate]):
                msg = "Unable to read the file"
                raise ValueError(msg)

            return AudioWave(data, bit, channels, samplerate)  # type: ignore

        with wave.open(filepath, "rb") as filep:
            raw_data = filep.readframes(filep.getnframes())
            samplerate = filep.getframerate() if samplerate is None else samplerate
            channels = filep.getnchannels() if channels is None else channels
            bit = filep.getsampwidth() * 8 if bit is None else bit

        return AudioWave.from_bytes(raw_data, bit, channels, samplerate)

    @classmethod
    @lru_cache(maxsize=32)
    def read_file_metadata(cls, filepath: str) -> tuple[int, int, int]:
        """Read the metadata of an audio file.

        It reads the binary headers of the file to automatically get the
        bit depth, the number of channels and the sample rate.

        """
        with wave.open(filepath, "rb") as filep:
            samplerate = filep.getframerate()
            channels = filep.getnchannels()
            bit = filep.getsampwidth() * 8

        return bit, channels, samplerate

    @classmethod
    def buffer_generator_from_file(
        cls,
        filepath: str,
        buffer_size: int = 1024 * 1024 * 8,
    ):
        """Return a generator that yields AudioWave objects from a file.

        The generator will read the file in chunks of `buffer_size` bytes.

        Parameters
        ----------
        filepath: str
            The path to the file.
        buffer_size: int
            The size of audio chunks. Defaults to 1024*1024*8 (8 MegaBytes).

        Yields
        ------
        AudioWave
            An AudioWave object containing the audio data read from the file.

        """
        bit_dept, chn, sample_rate = cls.read_file_metadata(filepath)
        with wave.open(filepath, "rb") as wave_file:
            frames: bytes = wave_file.readframes(buffer_size)
            while frames != b"":
                yield cls.from_bytes(frames, bit_dept, chn, sample_rate)
                frames = wave_file.readframes(buffer_size)

    @classmethod
    def from_bytes(
        cls,
        raw_data: bytes,
        bit: int,
        channels: int,
        samplerate: int,
    ) -> Self:
        r"""Generate an AudioWave object from a stream of bytes.

        It is assumed that the data is in little endian format and that the bytes
        are signed integers.

        Parameters
        ----------
        raw_data: bytes
            The stream of bytes.
        bit: int
            The bit depth of the audio.
        channels: int
            The number of channels of the audio.
        samplerate: int
            The sample rate of the audio.

        Example
        -------

        The following example shows how to create an AudioWave object from a stream of
        bytes.

        .. doctest::

            >>> import numpy as np
            >>> from mpai_cae_arp.audio import AudioWave
            >>> audio = AudioWave.from_bytes(b'\x00\x00\x00\x00', 16, 2, 44100)
            >>> np.array_equal(audio.array, np.array([[0, 0]]))
            True

        """
        data = np.array(
            [
                int.from_bytes(
                    raw_data[i : i + bit // 8],
                    byteorder="little",
                    signed=True,
                )
                for i in range(0, len(raw_data), bit // 8)
            ],
            dtype=np.int64,
        )  # int32 (default in Windows) leds to overflow
        data = np.reshape(data, (-1, channels))
        return cls(data, bit, channels, samplerate)

    def save(self, filepath: str, force: bool = False) -> None:
        """Save the audio as a wave file at the given path.

        Parameters
        ----------
        filepath: str
            The path where to save the audio.
        force: bool
            If True, it will create the directory if it does not exist.

        Raises
        ------
        ValueError
            if the directory does not exist and force is False

        Examples
        --------
        .. code-block:: python

            from mpai_cae_arp.audio import AudioWave

            audio = AudioWave(np.array([[0, 0]]), 16, 2, 44100)
            audio.save('wrong/path/test.wav') # raises ValueError
            audio.save('force/path/test.wav', force=True) # creates the path and saves

        """
        if not Path(filepath).parent.exists():
            if force:
                Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            else:
                msg = f"Directory {Path(filepath).parent} does not exist"
                raise ValueError(msg)

        with wave.open(filepath, "wb") as filep:
            filep.setframerate(self.samplerate)
            filep.setnchannels(self.channels)
            filep.setsampwidth(self.bit // 8)
            filep.setnframes(self.number_of_frames())
            filep.writeframesraw(self.get_raw())

    def set_sample_rate(self, samplerate: int) -> None:
        """Set the sample rate of the audio.

        .. versionadded:: 0.4.0

        Parameters
        ----------
        samplerate: int
            The new sample rate.

        """
        self.array = librosa.resample(
            self.array,
            orig_sr=self.samplerate,
            target_sr=samplerate,
        )
        self.samplerate = samplerate

    def get_raw(self) -> bytes:
        """Get the raw data of the audio.

        Returns
        -------
        bytes
            A bytes stream in the form (left right left right ...), where left and right
            are the samples for the left and right channels respectively for each frame
            in little endian format and signed.

        """
        data: np.ndarray = np.reshape(self.array, (-1,))
        bytes_array = b"".join(
            [
                int(x).to_bytes(self.bit // 8, byteorder="little", signed=True)
                for x in data
            ],
        )

        return bytes_array

    def number_of_frames(self) -> int:
        """Get the number of frames in the audio.

        A frame is a sample for each channel. In a stereo audio, a frame is composed by
        two samples, one for each channel, in the form [left, right], where left and
        right are the samples for the left and right channels respectively.

        Returns
        -------
        int
            The number of frames in the audio

        """
        return len(self.array)

    def duration(self) -> float:
        r"""Get the duration of the audio in seconds.

        The duration is calculated by dividing the number of frames by the sample rate.

        .. math::

            time = \frac{frames}{sample\_rate}

        Returns
        -------
        float
            the duration of the audio in seconds

        """
        return self.number_of_frames() / self.samplerate

    def get_mfcc(self, n_mfcc: int = 13) -> np.ndarray:
        """Get the Mel-frequency cepstral coefficients (MFCC) of the audio.

        Parameters
        ----------
        n_mfcc: int
            The number of MFCC to return. Default is 13.

        Returns
        -------
        np.ndarray
            The mean of the first ``n_mfcc`` mfcc over the entire audio signal.
            If the audio is multichannel, the mean of the mfcc of each channel is
            returned.

        """
        mfcc_per_ch = []

        for channel in range(self.channels):
            signal = self.get_channel(channel).array
            signal = signal / (2 ^ (self.bit - 1))  # normalize the signal
            mfccs = librosa.feature.mfcc(y=signal, sr=self.samplerate, n_mfcc=n_mfcc)
            mean_mfccs = []
            for elem in mfccs:
                mean_mfccs.append(np.mean(elem))
            mfcc_per_ch.append(mean_mfccs)

        # return the mean of the mfcc of each channel
        return np.mean(mfcc_per_ch, axis=0)

    def rms(self, mode: Criterion = Criterion.MAX, scale: Scale = "normal") -> float:
        r"""Get the root-mean-square of the audio.

        The root-mean-square of the audio. It measures the power level of the
        entire signal. It is calculated by taking the square root of the mean of
        the square of the samples. In multichannel audio, the rms is calculated by
        taking the mean or the max of the rms of each channel.

        Parameters
        ----------
        mode: Criterion
            The mode to use to calculate the rms.
            It can be ``Criterion.MEAN`` or ``Criterion.MAX``.
            If ``Criterion.MEAN``, the rms is calculated by taking the mean of the rms
            of each channel. If ``Criterion.MAX``, the rms is calculated by taking the
            maximum of the rms between all channels. Default is ``Criterion.MAX``.
        scale: Scale
            The scale to use to calculate the rms. It can be ``"db"`` or ``"normal"``.

        Raises
        ------
        ValueError
            if the mode is not ``MEAN`` or ``MAX``

        Returns
        -------
        float
            The rms of the audio.

        """
        functions: dict[Scale, Callable[[int | float, int], float]] = {
            "db": utils.pcm_to_db,
            "normal": lambda x, _: x,
        }
        try:
            scale_funciton = functions[scale]
        except KeyError as err:
            msg = "Invalid scale"
            raise ValueError(msg) from err

        if self.channels == 1:
            return scale_funciton(utils.rms(self.array), self.bit)
        channels_rms = []
        for channel in range(self.channels):
            channels_rms.append(utils.rms(self.array[:, channel]))

        match mode:
            case Criterion.MEAN:
                return scale_funciton(np.array(channels_rms).mean(), self.bit)
            case Criterion.MAX:
                return scale_funciton(max(channels_rms), self.bit)
            case _:
                msg = "Invalid criterion"
                raise ValueError(msg)

    @deprecated("Use AudioWave.rms(scale='db') instead.")
    def db_rms(self, mode: Criterion = Criterion.MAX) -> float:
        """Get the rms of audio in decibel scale.

        It is a wrapper of ``self.rms()``, that converts the returned value to decibels.

        .. deprecated:: 0.5.2
            Use :meth:`AudioWave.rms` with argument :code:`scale="db"` instead.

        .. seealso::
            see also the method :meth:`AudioWave.rms` for a more detailed description
            of the parameters.

        """
        return utils.pcm_to_db(self.rms(mode), self.bit)

    def get_channel(self, channel: int) -> Self:
        """Create a new AudioWave object containing only the given channel.

        Parameters
        ----------
        channel: int
            the channel to extract from the audio, where 0 is the first channel,
            1 the second and so on.

        Raises
        ------
        IndexError
            if the channel is not found.

        Returns
        -------
        AudioWave
            An AudioWave object containing only the given channel.

        Example
        -------

        .. code-block:: python

            from mpai_cae_arp.audio import AudioWave

            # let's say 'sample.wav' is a stereo audio

            # returns an AudioWave object containing only the first channel
            audio_left = AudioWave.from_file('sample.wav').get_channel(0)

            # returns an AudioWave object containing only the second channel
            audio_right = AudioWave.from_file('sample.wav').get_channel(1)

            # raises IndexError because there are only two channels
            audio_third = AudioWave.from_file('sample.wav').get_channel(2)

        """
        if channel not in range(self.channels):
            msg = "Channel not found"
            raise IndexError(msg)

        if self.channels == 1:
            return AudioWave(self.array.squeeze(), self.bit, 1, self.samplerate)
        return AudioWave(self.array[:, channel], self.bit, 1, self.samplerate)

    def get_silence_slices(
        self,
        noise_list: Iterable[Noise],
        length: int,
    ) -> dict[str, list[tuple[int, int]]]:
        """Get the slices of silence in the given signal.

        Passing a list of ``Noise`` instances to the ``noise_list`` parameter,
        the function will return a dictionary of slices of silence in the given signal.
        The dictionary will have the label of the noise as key and a list of tuples as
        value. Each tuple will contain the starting and ending frames of a slice of
        silence.

        Parameters
        ----------
        noise_list: Iterable[Noise]
            the noise bands to use to detect the silence
        length: int
            the length of a slice of silence in milliseconds

        Raises
        ------
        ValueError
            if ``length`` is less than 1

        Returns
        -------
        dict[str, list[tuple[int, int]]]
            A dictionary with the label of the noise as key and a list of tuples as
            value. Each tuple will contain the starting and ending frames of a slice of
            silence. If the signal is completely silent, or the ``min_length`` required
            is greater than the signal length, the dictionary will contain an empty list
            for each noise in the ``noise_list``.

        Example
        -------

        For example, if we have the following audio:

        .. doctest::

            >>> from mpai_cae_arp.audio import AudioWave, Noise
            >>> noise_list = [Noise("noise1", -10, -20), Noise("noise2", -30, -40)]
            >>> array = np.array([10000 for _ in range(8000)])
            >>> audio = AudioWave(array, 16, 1, 8000)
            >>> audio.get_silence_slices(noise_list, 500)
            {'noise1': [(0, 4000), (4000, 8000)], 'noise2': []}


        .. note::
            The ``AudioWave`` abstraction makes possible to analyze the signal at a
            frame level. Nonetheless, the function will scan the signal at a millisecond
            interval.
            This is because in a millisecond there are many frames that can have a rms
            value which belongs to different ``Noise`` instances, but those variations
            are not relevant for the purpose of detecting silence since are not
            perceptible by the human ear.

        """
        # sanity checks on the parameters
        if not isinstance(length, int) or length < 1:
            msg = "min_length must be an integer greater or equal 1"
            raise ValueError(msg)

        window_frames = length * self.samplerate // 1000
        last_frame = self.number_of_frames() - window_frames

        # create an empty array of indexes for each noise to filter
        idxs = {noise.label: [] for noise in noise_list}

        # if the signal is too short, return an empty dict
        if last_frame < 1 or noise_list == []:
            return idxs

        # find the thresholds to be used to detect the noise
        upper_noise_limit = max(noise.db_max for noise in noise_list)
        lower_noise_limit = min(noise.db_min for noise in noise_list)

        i = 0

        while i <= last_frame:
            chunk = self[i : i + window_frames]
            max_pos = utils.get_last_index(
                chunk.array,
                utils.db_to_pcm(upper_noise_limit, chunk.bit),
            )
            # if there is a value over the threshold go to its index and start
            # seeking from here
            if max_pos is not None:
                # if multidimensional array get only the x value
                if isinstance(max_pos, tuple):
                    max_pos = max_pos[0]
                i += max_pos + 1
            # else all the signal is under the threshold
            else:
                # classification of the chunk based on rms
                for noise in noise_list:
                    if noise.db_min <= chunk.db_rms() < noise.db_max:
                        idxs[noise.label].append((i, i + window_frames))
                        break
                # if the signal power is under the minimum, assign it to the quieter
                # noise
                if chunk.db_rms() < lower_noise_limit:
                    idxs[min(noise_list).label].append((i, i + window_frames))
                i += window_frames

        return idxs
