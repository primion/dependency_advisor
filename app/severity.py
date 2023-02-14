#!/usr/bin/env python
""" Vulnerability severity rating """


from enum import IntEnum

from typing import Union


class Severity(IntEnum):
    """ Enum for severity levels. With some convenience functions """
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

    @classmethod
    def parse(cls, user_data: Union[str, int, float]):
        """ Create enum from a text description of the severity (aka "low") or a CVSS level as float or int

        CVSS V3        Severity
        0.1-3.9        Low
        4.0-6.9        Medium
        7.0-8.9        High
        9.0-10.0       Critical
        """

        textmatch = {"NEGLIGIBLE": cls.LOW,    # Yeah, seriously. DB is haunted.
                     "UNKNOWN": cls.LOW,    # Yeah, seriously. DB is haunted.
                     "LOW": cls.LOW,
                     "MEDIUM": cls.MEDIUM,
                     "HIGH": cls.HIGH,
                     "CRITICAL": cls.CRITICAL}

        if isinstance(user_data, str):
            normalized = user_data.upper().strip()
            if normalized in textmatch:
                return cls(textmatch[normalized])

        # Maybe it is a CVSS score
        try:
            if isinstance(user_data, str):
                print(user_data)
                cvss = float(user_data.strip())
            if isinstance(user_data, int):
                cvss = float(user_data)
            if isinstance(user_data, float):
                cvss = user_data
        except Exception as exc:
            raise ValueError from exc
        if 0 < cvss <= 3.9:
            return cls(cls.LOW)
        if 4.0 <= cvss <= 6.9:
            return cls(cls.MEDIUM)
        if 7.0 <= cvss <= 8.9:
            return cls(cls.HIGH)
        if 9.0 <= cvss <= 10:
            return cls(cls.CRITICAL)

        # Ok, nothing worked
        raise ValueError

    def __str__(self) -> str:
        return self.name
