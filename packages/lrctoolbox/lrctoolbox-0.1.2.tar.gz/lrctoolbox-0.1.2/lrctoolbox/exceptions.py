""" Exceptions for the lrctoolbox package. """


class LRCError(Exception):
    """Base class for exceptions in this module."""


class FileTypeError(LRCError):
    """Raised when the file type is not supported."""

    def __init__(self, file_type: str, supported_file_types: list[str]):
        self.file_type = file_type
        self.supported_file_types = supported_file_types

    def __str__(self) -> str:
        return (
            f"File type {self.file_type} is not supported. "
            f"Supported file types are {self.supported_file_types}"
        )
