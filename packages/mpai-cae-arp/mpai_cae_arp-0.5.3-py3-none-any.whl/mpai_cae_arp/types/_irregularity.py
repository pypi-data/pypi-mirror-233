import uuid
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field
from typing_extensions import Self, deprecated

from mpai_cae_arp.audio.standards import EqualizationStandard, SpeedStandard
from mpai_cae_arp.files import File, FileType
from mpai_cae_arp.time import time_to_seconds


class IrregularityType(str, Enum):
    BRANDS_ON_TAPE = "b"
    SPLICE = "sp"
    START_OF_TAPE = "sot"
    ENDS_OF_TAPE = "eot"
    DAMAGED_TAPE = "da"
    DIRT = "di"
    MARKS = "m"
    SHADOWS = "s"
    WOW_AND_FLUTTER = "wf"
    PLAY_PAUSE_STOP = "pps"
    SPEED = "ssv"
    EQUALIZATION = "esv"
    SPEED_AND_EQUALIZATION = "ssv"  # noqa: PIE796
    BACKWARD = "sb"


class Source(str, Enum):
    AUDIO = "a"
    VIDEO = "v"
    BOTH = "b"


Json = dict[str, Any]


class IrregularityProperties(BaseModel):
    reading_speed: SpeedStandard = Field(serialization_alias="ReadingSpeedStandard")
    reading_equalisation: EqualizationStandard = Field(
        serialization_alias="ReadingEqualisationStandard",
    )
    writing_speed: SpeedStandard = Field(serialization_alias="WritingSpeedStandard")
    writing_equalisation: EqualizationStandard = Field(
        serialization_alias="WritingEqualisationStandard",
    )

    @classmethod
    @deprecated("Use directly the constructor instead.")
    def from_json(cls, json_property: Json) -> Self:
        return cls(
            reading_speed=SpeedStandard(json_property["ReadingSpeedStandard"]),
            reading_equalisation=EqualizationStandard(
                json_property["ReadingEqualisationStandard"],
            ),
            writing_speed=SpeedStandard(json_property["WritingSpeedStandard"]),
            writing_equalisation=EqualizationStandard(
                json_property["WritingEqualisationStandard"],
            ),
        )

    @deprecated("Use IrregularityProperties.json instead.")
    def to_json(self) -> Json:
        """Convert the properties to a dictionary.

        .. deprecated:: 0.4.0
            Use :meth:`IrregularityProperties.json` instead.

        """
        return {
            "ReadingSpeedStandard": self.reading_speed.value,
            "ReadingEqualisationStandard": self.reading_equalisation.value,
            "WritingSpeedStandard": self.writing_speed.value,
            "WritingEqualisationStandard": self.writing_equalisation.value,
        }

    def get_irregularity_type(self) -> IrregularityType | None:
        if self.reading_equalisation != self.writing_equalisation:
            if self.reading_speed != self.writing_speed:
                return IrregularityType.SPEED_AND_EQUALIZATION
            return IrregularityType.EQUALIZATION
        if self.reading_speed != self.writing_speed:
            return IrregularityType.SPEED
        return None


class Irregularity(BaseModel):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        serialization_alias="IrregularityID",
    )
    source: Source = Field(serialization_alias="Source")
    time_label: str = Field(serialization_alias="TimeLabel")
    type: IrregularityType | None = Field(
        default=None,
        serialization_alias="IrregularityType",
    )
    properties: IrregularityProperties | None = Field(
        default=None,
        serialization_alias="IrregularityProperties",
    )
    image_URI: str | None = Field(default=None, serialization_alias="ImageURI")
    audio_block_URI: str | None = Field(
        default=None,
        serialization_alias="AudioBlockURI",
    )

    @classmethod
    @deprecated("Use directly the constructor instead.")
    def from_json(cls, json_irreg: Json) -> Self:
        """Convert a JSON irregularity to an Irregularity object.

        .. deprecated:: 0.5.3
            Use :class:`Irregularity` constructor instead.

        """
        properties: IrregularityProperties | None = json_irreg.get(
            "IrregularityProperties",
        )
        irregularity_type: IrregularityType | None = None

        if properties is not None:
            properties = IrregularityProperties.from_json(
                json_irreg["IrregularityProperties"],
            )

        raw_irreg_type: str | None = json_irreg.get("IrregularityType")

        if raw_irreg_type:
            if raw_irreg_type is not (
                IrregularityType.SPEED.value
                or IrregularityType.SPEED_AND_EQUALIZATION.value
            ):
                irregularity_type = IrregularityType(raw_irreg_type)
            else:
                if properties is None:
                    msg = "Unexpected value: properties is None"
                    raise ValueError(msg)
                if properties.reading_equalisation != properties.writing_equalisation:
                    irregularity_type = IrregularityType.SPEED_AND_EQUALIZATION
                else:
                    irregularity_type = IrregularityType.SPEED

        return cls(
            id=uuid.UUID(json_irreg["IrregularityID"]),
            source=Source(json_irreg["Source"]),
            time_label=json_irreg["TimeLabel"],
            type=irregularity_type,
            properties=properties,
            image_URI=json_irreg.get("ImageURI"),
            audio_block_URI=json_irreg.get("AudioBlockURI"),
        )

    @deprecated("Use Irregularity.json instead.")
    def to_json(self) -> Json:
        """Create a dictionary with the irregularity information.

        .. deprecated:: 0.4.0
            Use :func:`Irregularity.json` instead.

        """
        dictionary: Json = {
            "IrregularityID": str(self.id),
            "Source": self.source.value,
            "TimeLabel": self.time_label,
        }

        if self.type:
            dictionary["IrregularityType"] = self.type.value

        if self.image_URI:
            dictionary["ImageURI"] = self.image_URI

        if self.audio_block_URI:
            dictionary["AudioBlockURI"] = self.audio_block_URI

        if self.properties:
            dictionary["IrregularityProperties"] = self.properties.to_json()

        return dictionary


class IrregularityFile(BaseModel):
    irregularities: list[Irregularity] = Field(serialization_alias="Irregularities")
    offset: int | None = Field(default=None, serialization_alias="Offset")

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, IrregularityFile):
            return False

        return self.irregularities == __o.irregularities and self.offset == __o.offset

    @classmethod
    @deprecated("Use directly the constructor instead.")
    def from_json(cls, json_irreg: Json) -> Self:
        """Create an IrregularityFile object from a JSON dictionary.

        .. deprecated:: 0.4.0
            Use :class:`IrregularityFile` constructor instead.

        """
        irregularities: list[Irregularity] = []

        for irreg in json_irreg["Irregularities"]:
            irregularities.append(Irregularity.from_json(irreg))

        return IrregularityFile(
            irregularities=irregularities,
            offset=json_irreg.get("Offset"),
        )

    @deprecated("Use IrregularityFile.json instead.")
    def to_json(self) -> Json:
        """Convert the IrregularityFile to a dictionary.

        .. deprecated:: 0.4.0
            Use :meth:`IrregularityFile.json` instead.

        """
        dictionary: Json = {
            "Irregularities": [
                irregularity.to_json() for irregularity in self.irregularities
            ],
        }

        if self.offset:
            dictionary["Offset"] = self.offset

        return dictionary

    def add(self, irregularity: Irregularity) -> Self:
        """Add an irregularity to the list of irregularities.

        Parameters
        ----------
        irregularity : Irregularity
            the irregularity to add

        Raises
        ------
        TypeError
            if the irregularity is not a py:class:`Irregularity` object

        """
        if not isinstance(irregularity, Irregularity):
            msg = "IrregularityFile.add() expects an Irregularity object"
            raise TypeError(msg)
        self.irregularities.append(irregularity)
        self.order()
        return self

    def order(self) -> Self:
        """Sort the irregularities by time label."""
        self.irregularities.sort(key=lambda x: time_to_seconds(x.time_label))
        return self

    def join(self, other) -> Self:
        """Merge two irregularity files."""
        if not isinstance(other, IrregularityFile):
            msg = "other must be an instance of IrregularityFile"
            raise TypeError(msg)
        self.irregularities += other.irregularities
        self.order()
        return self

    def save_as_json_file(self, path: str) -> None:
        """Save the irregularity file as a JSON file at the given path.

        .. versionadded:: 0.4.0

        """
        File(path=path, format=FileType.JSON).write_content(
            self.model_dump(by_alias=True),  # type: ignore
        )
