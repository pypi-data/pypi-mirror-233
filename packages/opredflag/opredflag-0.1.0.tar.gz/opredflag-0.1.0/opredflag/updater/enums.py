"""
Py-opredflag
Copyright (C) 2023  BobDotCom

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from enum import Enum

__all__ = ("Compatibility",)


class VersionComparison(Enum):
    """Represents a comparison between semantic versions."""

    UNKNOWN = None
    NEWER_MAJOR = 3
    NEWER_MINOR = 2
    NEWER_PATCH = 1
    EQUAL = 0
    OLDER_PATCH = -1
    OLDER_MINOR = -2
    OLDER_MAJOR = -3


class Compatibility(Enum):
    """Represents a compatibility level between semantic versions."""

    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"

    def __str__(self) -> str:
        return self.value
