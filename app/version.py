#!/usr/bin/env python
""" Class for flexible version handling """

from functools import total_ordering
import re

from typing import Optional, Tuple


@total_ordering
class Version():  # type: ignore
    """ Handline version strings major.minor.build-extension style """
    def __init__(self, as_string: Optional[str]) -> None:
        if as_string is None:
            raise ValueError()
        as_string = as_string.strip()

        # Debian handling:
        self.debian_version = None
        if "+deb" in as_string:
            self.debian_version = as_string.split("+deb")[1]
            as_string = as_string.split("+deb")[0]

        # Ubuntu handling
        self.ubuntu_version = None
        if "ubuntu" in as_string:
            self.ubuntu_version = as_string.split("ubuntu")[1]
            as_string = as_string.split("ubuntu")[0]

        # Very odd format fixed: '< 0:1.95.8-8.3.el5_4.2'
        if as_string.startswith("0:"):
            as_string = as_string[2:]
        parts = as_string.split(".")
        self.extension = 0
        self.major = int(parts[0])

        # Minor
        try:
            self.minor = int(parts[1])
        except IndexError:
            self.minor = 0
        except ValueError:
            # Split at first non-int value
            chunks = re.split(r"\D", parts[1])
            self.minor = int(chunks[0])
            try:
                self.extension = int(re.sub(r"\D", "", chunks[1]))
            except ValueError:
                self.extension = 0

        # Build
        self.build = 0
        try:
            self.build = int(parts[2])
        except IndexError:
            self.build = 0
        except ValueError:
            # Split at first non-int value
            chunks = re.split(r"\D", parts[2])
            try:
                self.build = int(chunks[0])
            except ValueError:
                self.build = 0
            try:
                self.extension = int(re.sub(r"\D", "", chunks[1]))
            except ValueError:
                self.extension = 0
            except IndexError:
                self.extension = 0

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.build}-{self.extension}"

    @property
    def version(self) -> Tuple[int, int, int, int]:
        """ The version number as 4 int tuple """
        return self.major, self.minor, self.build, self.extension

    def __eq__(self, other) -> bool:  # type: ignore
        return self.version == other.version

    def __lt__(self, other) -> bool:  # type: ignore
        return self.version < other.version
