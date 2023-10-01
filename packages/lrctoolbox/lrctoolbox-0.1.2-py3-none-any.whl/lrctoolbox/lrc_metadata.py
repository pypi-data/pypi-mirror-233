"""A module that contains classes that represent LRC metadata."""

from dataclasses import dataclass
from typing import ClassVar, Optional


class BaseLRCMetadata:
    """A class that represents base LRC metadata."""

    LRC_METADATA_MAPPINGS: dict[str, str] = {}

    @property
    def lrc_formatted_metadata(self) -> list[str]:
        """returns the module metadata as a list of strings with LRC metadata format"""
        formatted_metadata = []
        for key, value in self.LRC_METADATA_MAPPINGS.items():
            if not getattr(self, value):
                continue
            formatted_metadata.append(f"[{key}:{getattr(self, value)}]")
        return formatted_metadata


@dataclass()
class TrackMetadataMixin:
    """A class that represents track metadata."""

    artist: Optional[str] = None
    title: Optional[str] = None
    album: Optional[str] = None
    length: Optional[str] = None
    lyricist: Optional[str] = None
    mbid: Optional[str] = None
    uri: Optional[str] = None
    language: Optional[str] = None

    LRC_METADATA_MAPPINGS: ClassVar[dict[str, str]] = {
        "ar": "artist",
        "ti": "title",
        "al": "album",
        "au": "lyricist",
        "uri": "uri",
        "mbid": "mbid",
        "length": "length",
        "language": "language",
    }


@dataclass()
class ModuleMetadataMixin:
    """A class that represents module metadata."""

    re_name: Optional[str] = None
    version: Optional[str] = None
    author: Optional[str] = None

    LRC_METADATA_MAPPINGS: ClassVar[dict[str, str]] = {
        "re": "re_name",
        "ve": "version",
        "by": "author",
    }


class LRCMetadata(BaseLRCMetadata, TrackMetadataMixin, ModuleMetadataMixin):
    """A class that represents combined metadata of module and track."""

    LRC_METADATA_MAPPINGS: dict[str, str] = {
        **TrackMetadataMixin.LRC_METADATA_MAPPINGS,
        **ModuleMetadataMixin.LRC_METADATA_MAPPINGS,
    }


class TrackMetadata(BaseLRCMetadata, TrackMetadataMixin):
    """A class that represents track metadata."""

    LRC_METADATA_MAPPINGS = TrackMetadataMixin.LRC_METADATA_MAPPINGS


class ModuleMetadata(BaseLRCMetadata, ModuleMetadataMixin):
    """A class that represents module metadata."""

    LRC_METADATA_MAPPINGS = ModuleMetadataMixin.LRC_METADATA_MAPPINGS
