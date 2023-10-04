__version__ = "0.1.5"


class ComelException(Exception):
    """Base Comel exception."""


class InvalidInstanceException(ComelException):
    """Error when passed in invalid instance."""
