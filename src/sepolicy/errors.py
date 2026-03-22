"""
Error Module

Error handling utilities.
"""


class SepolicyError(Exception):
    """Base exception for sepolicy errors."""
    pass


class ParseError(SepolicyError):
    """Error parsing AVC denial."""
    pass


class ValidationError(SepolicyError):
    """Error validating rules."""
    pass


class ExportError(SepolicyError):
    """Error exporting rules."""
    pass


class DeviceError(SepolicyError):
    """Error with ADB device."""
    pass
