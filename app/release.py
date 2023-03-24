#!/usr/bin/env python

"""A class describing a package release."""

import datetime
from typing import List, Union, Optional

from app.version import Version
from app.vulnerability import Vulnerability


class Release():
    """A specific release of the package."""

    def __init__(self, version: Union[Version, Optional[str]], published_at: Union[datetime.datetime, str]):
        """Initialize the release class.

        :param version: Version number of this release
        :type version: Version or str
        :param published_at: the time this release was published
        :type published_at: datetime.datetime or str to parse
        """
        if isinstance(version, Version):
            self.version = version
        else:
            self.version = Version(version)

        if isinstance(published_at, datetime.datetime):
            self.published_at = published_at
        else:
            try:
                self.published_at = datetime.datetime.fromisoformat(published_at)
            except ValueError:
                # Python < 3.11 can not handle time zone like in '2020-12-03T12:48:26.000Z'
                self.published_at = datetime.datetime.fromisoformat(published_at[:-1])

        self.vulnerabilities: List[Vulnerability] = []

    def add_vulnerability(self, vulnerability: Vulnerability) -> None:
        """Add a vulnerability to this version.
        
        :param vulnerability: The vulnerability to add to this release
        :type vulnerability: Vulnerability
        """
        self.vulnerabilities.append(vulnerability)

    def __str__(self) -> str:
        """Return a detailed string for the release also containing the CVEs.
        
        :return: a string description of this Release
        :rtype: str
        """
        cves: List[str] = []
        for vulnerability in self.vulnerabilities:
            cves = cves + vulnerability.get_cves()
        cvestring = ",".join(cves)
        return f"{self.published_at}: {self.version} {cvestring}"
