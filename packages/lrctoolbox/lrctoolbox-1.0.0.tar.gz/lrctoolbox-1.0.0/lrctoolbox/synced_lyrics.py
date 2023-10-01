"""A module that provides classes to work with synced lyrics."""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Any, ClassVar

from lrctoolbox.exceptions import FileTypeError
from lrctoolbox.lrc_metadata import LRCMetadata
from lrctoolbox.synced_lyric_line import SyncedLyricLine

logger = logging.getLogger(__name__)

synced_lyrics_pattern = re.compile(r"\[(\d+:\d+.\d+)\](.*)")
lyricist_pattern = re.compile(r"Lyricist:?\s*(.*)", re.I)
metadata_pattern = re.compile(r"\[(\w+):\s?(.*)\]")


class SyncedLyrics(LRCMetadata):
    """A class that represents synced lyrics."""

    SUPPORTED_FILE_TYPES: ClassVar[list[str]] = [".lrc", ".txt"]

    def __init__(self):
        super().__init__()
        self._synced_lines: list[SyncedLyricLine] = []

    def __str__(self) -> str:
        return "\n".join(self.lyrics)

    @property
    def synced_lines(self) -> list[SyncedLyricLine]:
        """returns the lines as a list of SyncedLyricLine objects"""
        return self._synced_lines

    @synced_lines.setter
    def synced_lines(self, lines: list[SyncedLyricLine]):
        """sets the lines from a list of SyncedLyricLine objects"""
        self._synced_lines = lines

    @property
    def lyrics(self) -> list[str]:
        """lyrics as a list of strings with timestamp if present"""

        if not self.is_synced:
            return [line.text for line in self._synced_lines]

        return [line.formatted_lyric for line in self._synced_lines]

    @lyrics.setter
    def lyrics(self, lyrics: list[str] | list[SyncedLyricLine]):
        """sets the lyrics from a list of strings or SyncedLyricLine objects"""
        if not lyrics:
            logger.warning("lyrics is empty")
            self._synced_lines = []
            return

        # only for convenience
        if all(isinstance(line, SyncedLyricLine) for line in lyrics):
            self._synced_lines = lyrics  # type: ignore
            return

        self._synced_lines = self.load_from_lines(lyrics).synced_lines  # type: ignore # noqa: E501
        # all this is done to preserve any metadata that was present

    @property
    def is_synced(self) -> bool:
        """checks if the lyrics is valid and synced
        Checks Performed:
           - lyrics is not empty
           - timestamp is in ascending order
           - timestamp is not all same

        """
        return bool(
            self._synced_lines
            and self.has_timestamps_in_ascending_order
            and not self.has_timestamps_all_equal
        )

    @property
    def has_timestamps_in_ascending_order(self) -> bool:
        """checks if the timestamp is in ascending order"""
        if not self._synced_lines:
            return False

        # if any of the timestamp is None return False
        if any(line.timestamp is None for line in self._synced_lines):
            return False

        return all(
            (self._synced_lines[i].timestamp <= self._synced_lines[i + 1].timestamp)  # type: ignore  # noqa: E501
            for i in range(len(self._synced_lines) - 1)
        )

    @property
    def has_timestamps_all_equal(self) -> bool:
        """checks if the timestamp is all same"""
        if not self._synced_lines:
            return False

        return all(
            self._synced_lines[i].timestamp
            == self._synced_lines[i + 1].timestamp
            for i in range(len(self._synced_lines) - 1)
        )

    @property
    def is_missing_any_timestamp(self) -> bool:
        """Check if any timestamp is None"""
        return any(line.timestamp is None for line in self._synced_lines)

    @classmethod
    def parse_str(cls, line: str) -> SyncedLyricLine | dict[str, str]:
        """Parse a line for lyrics or lrc metadata"""
        # match the lyricist
        match = re.search(lyricist_pattern, line)
        if match:
            logger.debug("Lyricist found: %s", line.encode("utf-8"))
            lyricist = match.group(1)
            return {"lyricist": lyricist.strip()}

        # match the synced lyrics
        match = re.search(synced_lyrics_pattern, line)
        if match:
            timestamp, lyric = match.groups()
            timestamp_pattern = re.compile(r"(\d+):(\d+).(\d+)")
            match = re.search(timestamp_pattern, timestamp)
            if not match:
                return SyncedLyricLine(lyric.strip())

            ms_ = int(match.group(3))
            # make sure the ms is 3 digits
            ms_ = ms_ * 10 ** (3 - len(str(ms_)))
            timestamp_in_ms = (
                int(match.group(1)) * 60 * 1000
                + int(match.group(2)) * 1000
                + ms_
            )
            # logger.debug(synced_lyrics._lines[-1])
            return SyncedLyricLine(lyric.strip(), timestamp_in_ms)

        # match the metadata
        match = re.search(metadata_pattern, line)
        if match:
            logger.debug("Metadata found: %s", line.encode("utf-8"))
            key, value = match.groups()
            key = cls.LRC_METADATA_MAPPINGS.get(key, key)
            return {key: value.strip()}

        # if the line is not matched by any of the patterns
        logger.debug("Line not matched: %s", line.encode("utf-8"))
        return SyncedLyricLine(line.strip())

    @classmethod
    def load_from_lines(cls, lines: list[str]) -> SyncedLyrics:
        """
        Load synced lyrics from a list of strings.
        """

        logger.debug("Loading synced lyrics from lines")

        # convert None to to empty string
        lines = [line or "" for line in lines]
        # if last lines are empty remove them
        while lines and not lines[-1]:
            lines.pop()

        # check if the lines is empty or not string
        if not lines or not all(isinstance(line, str) for line in lines):
            line_which_is_not_str = next(
                (line for line in lines if not isinstance(line, str)), None
            )
            exc = TypeError(
                (
                    "lines must be a list of str, got"
                    f" {type(line_which_is_not_str)}"
                ),
                line_which_is_not_str,
            )
            logger.exception(exc)
            raise exc

        # use regex to match the metadata and synced lyrics
        synced_lyrics = cls()

        for line in lines:
            parsed_line = cls.parse_str(line)
            if isinstance(parsed_line, SyncedLyricLine):
                synced_lyrics._synced_lines.append(parsed_line)
                continue
            synced_lyrics.update_metadata(parsed_line)

        if synced_lyrics.has_timestamps_all_equal:
            # set all timestamp to None
            for _line in synced_lyrics._synced_lines:
                _line.timestamp = None

        if (
            not synced_lyrics.has_timestamps_in_ascending_order
            and not synced_lyrics.has_timestamps_all_equal
        ):
            synced_lyrics._synced_lines.sort(key=lambda x: x.timestamp or 0)
        return synced_lyrics

    @classmethod
    def load_from_file(cls, path: Path | str):
        """convenience method to load from a file

        `path`: Path to the lrc file

        calls `load_from_lines` internally after reading the file
        """

        path = Path(path)

        # make sure the file exists and is lrc file
        if not path.exists() or path.suffix not in cls.SUPPORTED_FILE_TYPES:
            for ext in cls.SUPPORTED_FILE_TYPES:
                if path.with_suffix(ext).exists():
                    logger.warning(
                        "%s not found, using %s instead",
                        path,
                        path.with_suffix(ext),
                    )
                    path = path.with_suffix(ext)
                    break
            else:
                exc = (
                    FileNotFoundError(f"{path} not found")
                    if not path.exists()
                    else FileTypeError(path.suffix, cls.SUPPORTED_FILE_TYPES)
                )
                logger.exception(exc)
                raise exc

        with open(path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        if not lines:
            exc = ValueError(f"{path} is empty")
            logger.exception(exc)
            raise exc
        return cls.load_from_lines(lines)

    @classmethod
    def load(cls, maybe_lyrics: Any):  # TODO: fix type
        """Load synced lyrics from a object"""

        if isinstance(maybe_lyrics, list):
            return cls.load_from_lines(maybe_lyrics)
        if isinstance(maybe_lyrics, Path):
            return cls.load_from_file(maybe_lyrics)
        if isinstance(maybe_lyrics, str):
            if Path(maybe_lyrics).exists():
                return cls.load_from_file(maybe_lyrics)
            return cls.load_from_lines(maybe_lyrics.splitlines())

        exc = TypeError("maybe_lyrics must be a list, str or Path")
        logger.exception(exc)
        raise exc

    def update_metadata(self, metadata: dict[str, str]) -> SyncedLyrics:
        """updates the metadata of the synced lyrics"""
        for key, value in metadata.items():
            key = self.LRC_METADATA_MAPPINGS.get(key, key)
            setattr(self, key, value)

        return self
