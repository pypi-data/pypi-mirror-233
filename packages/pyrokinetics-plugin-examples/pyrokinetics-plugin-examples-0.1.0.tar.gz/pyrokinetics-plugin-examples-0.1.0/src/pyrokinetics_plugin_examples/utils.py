"""
Defines a standard ``verify_file_type`` function for all plugins, and a function that
creates a compatible file.
"""

from pathlib import Path

HW = "Hello world!"


def verify(filename: Path) -> None:
    """
    Checks that the first line of the file reads "Hello world!". Otherwise
    raises an exception.
    """
    with open(filename) as f:
        if f.readline().rstrip() != HW:
            raise RuntimeError(f"First line of file should say {HW}.")


def make_plugin_example_file(filename: Path) -> None:
    """
    Create a file compatible with ``verify()``.
    """
    with open(filename, "w") as f:
        f.write(HW + "\n")
