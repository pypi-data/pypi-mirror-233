import uuid

from pydantic import BaseModel, Field
from typing_extensions import Self

from mpai_cae_arp.audio.standards import EqualizationStandard, SpeedStandard
from mpai_cae_arp.files import File, FileType


class Restoration(BaseModel):
    """
    .. versionadded:: 0.4.0.

    .. todo:: Add a description
    """

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        serialization_alias="RestorationID",
    )
    preservation_audio_file_start: str = Field(
        serialization_alias="PreservationAudioFileStart",
    )
    preservation_audio_file_end: str = Field(
        serialization_alias="PreservationAudioFileEnd",
    )
    restored_audio_file_URI: str = Field(serialization_alias="RestoredAudioFileURI")
    reading_backwards: bool = Field(serialization_alias="ReadingBackwards")
    applied_speed_standard: SpeedStandard = Field(
        serialization_alias="AppliedSpeedStandard",
    )
    applied_sample_frequency: int = Field(serialization_alias="AppliedSampleFrequency")
    applied_equalization_standard: EqualizationStandard = Field(
        serialization_alias="AppliedEqualisationStandard",
    )


class EditingList(BaseModel):
    """
    .. versionadded:: 0.4.0.

    .. todo:: Add a description
    """

    original_speed_standard: SpeedStandard = Field(
        serialization_alias="OriginalSpeedStandard",
    )
    original_equalization_standard: EqualizationStandard = Field(
        serialization_alias="OriginalEqualisationStandard",
    )
    original_sample_frequency: int = Field(
        serialization_alias="OriginalSampleFrequency",
    )
    restorations: list[Restoration] = Field(serialization_alias="Restorations")

    def add(self, restoration: Restoration) -> Self:
        self.restorations.append(restoration)
        return self

    def remove(self, restoration: Restoration) -> Self:
        self.restorations.remove(restoration)
        return self

    def remove_by_id(self, restoration_id: uuid.UUID) -> Self:
        filtered = list(filter(lambda r: r.id != restoration_id, self.restorations))

        if len(filtered) == len(self.restorations):
            msg = f"Restoration with ID {restoration_id} not found."
            raise ValueError(msg)

        self.restorations = filtered
        return self

    def save_as_json_file(self, path: str) -> None:
        File(path=path, format=FileType.JSON).write_content(
            self.model_dump(mode="json", by_alias=True),  # type: ignore
        )
