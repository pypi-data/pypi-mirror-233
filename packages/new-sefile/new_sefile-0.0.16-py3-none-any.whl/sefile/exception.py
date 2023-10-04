"""
This file contain all custom exception that very useful, especially for controller, callback, etc.
So used all of this custom exception in this file, 
if a program catch an error that has related to all of this custom exception.
"""
# sefile/exception.py

class InvalidFormat(Exception): ...
class InvalidFileFormat(Exception): ...
class InvalidFilename(Exception): ...
class InvalidPath(Exception): ...
class ReadOnlyAttribute(Exception): ...


def exception_factory(exception, message: str) -> Exception:
    """
    Custom exception factory
    """
    raise exception(message)
