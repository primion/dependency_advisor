#!/usr/bin/env python3
"""This class represents a software package and contains all the available versions."""


import datetime
import hashlib
import json
import os
import sqlite3
# from pprint import pprint
from sqlite3 import Error
from typing import List, Optional, Union, Any

from pybraries.search import Search  # type: ignore
from app.severity import Severity
from app.version import Version
from app.vulnerability import Vulnerability
from app.release import Release


class Package():
    """A specific package, a package contains several releases."""

    def __init__(self, packagename: str, db_file: str, alternative_names: Optional[List[str]] = None) -> None:
        """Initialize a package.

        :param packagename: Exact name of a package so libraries.io can find it. Maybe test it in thier webui first. Example 'org.apache.tomcat:tomcat'
        :type packagename: str
        :param db_file: path to the grype db file
        :type db_file: str
        :param alternative_names: Alternative names for this package. For grype lookups
        :type alternative_names: a list of str or None
        """
        self.libraries = None              # Raw data from libraries.io
        self.packagename = packagename     # Name of the package, exact. Must match
        if alternative_names is None:
            self.alternative_names = []
        else:
            self.alternative_names = alternative_names

        self.releases: List[Release] = []                 # A list of Release-es
        self.download_libraries()
        self.db_file = db_file
        self.vulnerabilities: List[Vulnerability] = []
        self.load_grype()

    def latest_stable_version(self) -> Optional[Version]:
        """Return the latest stable version.

        :return: The latest stable version
        :rtype: Version or None
        """
        if self.libraries is None:
            return None
        try:
            return Version(self.libraries["latest_stable_release_number"])
        except ValueError:
            return None

    # TODO: Check if this can be removed
    def latest_stable_release_date(self) -> Optional[Version]:
        """Return the latest stable release date."""
        if self.libraries is None:
            return None
        try:
            return self.libraries["latest_stable_release_published_at"]
        except ValueError:
            return None

    def latest_version(self) -> Optional[Version]:
        """Return the latest version.

        :return: The latest version
        :rtype: Version or None
        """
        if self.libraries is None:
            return None
        return Version(self.libraries["latest_release_number"])

    # TODO: Check if this can be removed
    def latest_release_date(self) -> Optional[Version]:
        """Return the latest stable release date."""
        if self.libraries is None:
            return None
        return self.libraries["latest_release_published_at"]

    def get_release(self, version: Version) -> Optional[Release]:
        """Get a release by version.

        :param version: The version of a package to look up
        :type version: Version
        :return: The matching release
        :rtype: Release or None
        """
        for release in self.releases:
            if release.version == version:
                return release
        return None

    def sorted_releases(self, earliest: Optional[datetime.datetime] = None) -> List[Release]:
        """Return a list of sorted releases, if earliest is given: starting there.

        :param earliest: Earliest date to add to the sorted list
        :type earliest: datetime.datetime or None
        :return: a sorted list of releases after and including earliest
        :rtype: list of Release
        """
        res = []
        for release in self.releases:
            if earliest is None:
                res.append(release)
            elif release.published_at >= earliest:
                res.append(release)
        return res

    def sorted_releases_str(self, earliest: Optional[datetime.datetime] = None, details: bool = False) -> str:
        """Return a string containing date and version.

        :param earliest: Date of earliest release to include in the list
        :type earliest: datetime.datetime or None
        :param details: Also list the different vulnerabilities by severity
        :type details: bool
        :return: a text list of releases
        :rtype: str
        """
        res = ""
        for release in self.sorted_releases(earliest):

            self.count_vulnerabilities(release, Severity.LOW)

            if not details:
                res += f"{release.published_at}: {release.version}\n"
            else:
                res += f"{release.published_at}: {release.version} Low: {self.count_vulnerabilities(release, Severity.LOW)} Medium: {self.count_vulnerabilities(release, Severity.MEDIUM)} High: {self.count_vulnerabilities(release, Severity.HIGH)} Critical: {self.count_vulnerabilities(release, Severity.CRITICAL)}\n"
        return res

    def download_libraries(self) -> None:
        """Search libraries.io. Needs a API key set."""
        def sortkey(akey: Release) -> datetime.datetime:
            """Return the date this release was published at.

            @param akey:  The Release class to extract the publised_at date from
            """
            return akey.published_at

        namehash = hashlib.sha256()
        namehash.update(self.packagename.encode('utf-8'))
        filename = "cache/" + namehash.hexdigest() + ".json"
        if os.path.exists(filename):
            with open(filename, "rt", encoding="utf-8") as filehandle:
                info = json.load(filehandle)
        else:
            search = Search()

            info = search.project_search(keywords=self.packagename)  # , sort='stars', platform='pypi'

            if not os.path.exists("cache"):
                os.makedirs("cache")

            with open(filename, "wt", encoding="utf-8") as filehandle:
                filehandle.write(json.dumps(info, indent=4))

        for package in info:
            # We need an exact match
            if package["name"] == self.packagename:
                self.libraries = package
                if self.libraries is not None:
                    for release in self.libraries["versions"]:
                        self.releases.append(Release(release["number"], release["published_at"]))
                self.license = package["repository_license"]

        self.releases.sort(key=sortkey)

    def get_grype_scheme(self, cur: sqlite3.Cursor) -> int:
        """Get the grype database scheme.

        :param cur: database cursor
        :type cur: Cursor
        :return: The number indicating the database scheme
        :rtype: int
        """
        # Check Db has current scheme of 5
        cur.execute("SELECT schema_version from id")
        return cur.fetchone()[0]

    def find_package_in_grype_vulnerability(self, cur: sqlite3.Cursor, packagename: str) -> List[Any]:
        """Get the the list of entries for a package in the grype vulnerability database.

        :param cur: database cursor
        :type cur: Cursor
        :param packagename: the name of the package to look up
        :type packagename: str
        """
        selector = (packagename,)
        cur.execute("SELECT * FROM vulnerability WHERE package_name like ?", selector)
        return cur.fetchall()

    def find_metadata_in_grype_vulnerability_metadata(self, cur: sqlite3.Cursor, package_id: str) -> Any:
        """Get the metadata entry for a vulnerability.

        :param cur: database cursor
        :type cur: Cursor
        :param id: the id of the vulnerability
        :type packagename: str
        """
        cur.execute("SELECT * FROM vulnerability_metadata WHERE id = ?", (package_id,))
        return cur.fetchone()

    def test_grype(self) -> None:
        """Check the grype DB, print out everything found by package name as SQL text.

        Relevant to confirm that the package can be found in the database.
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
            print(sqlite3.version)

            cur = conn.cursor()

            stats = []

            rows = self.find_package_in_grype_vulnerability(cur, self.packagename)

            stats.append(f"Found {len(rows)} entries in grype for {self.packagename}")
            for row in rows:
                print(row)

            for aname in self.alternative_names:
                rows = self.find_package_in_grype_vulnerability(cur, aname)
                stats.append(f"Found {len(rows)} entries in grype for {aname}")
                for row in rows:
                    print(row)
        except Error as err:
            print(err)
        finally:
            if conn:
                conn.close()
        for stat in stats:
            print(stat)

    def load_grype(self) -> None:
        """Load the grype DB of vulnerabilities for this package."""
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
            print(sqlite3.version)

            cur = conn.cursor()

            if self.get_grype_scheme(cur) != 5:
                raise ValueError("Wrong Grype database scheme")

            # t = ("%"+keywords+"%",)
            rows = self.find_package_in_grype_vulnerability(cur, self.packagename)

            print(f"Found {len(rows)} entries in grype for {self.packagename}")

            for aname in self.alternative_names:
                rows = rows + self.find_package_in_grype_vulnerability(cur, aname)

            for row in rows:
                metadata = self.find_metadata_in_grype_vulnerability_metadata(cur, row[1])

                version = row[5]
                cve_data = row[8]
                cves = []
                if cve_data is not None:
                    data = json.loads(cve_data)
                    for entry in data:
                        if entry["id"].startswith("CVE-"):
                            cves.append(entry["id"])
                severity = metadata[4]
                urls = metadata[5]
                description = metadata[6]
                fixed = row[10]
                version_list = version.split(",")
                vmin = None
                vfix = None
                vlast_vulnerable = None
                vexact = None

                for version_item in version_list:
                    if version_item.strip().startswith("="):
                        vexact = Version(version_item.strip()[1:])
                    elif version_item.strip().startswith("<="):
                        vlast_vulnerable = Version(version_item.strip()[2:])
                    elif version_item.strip().startswith("<"):
                        vfix = Version(version_item.strip()[1:])
                    elif version_item.strip().startswith(">="):
                        vmin = Version(version_item.strip()[2:])
                    elif version_item.strip() == "":
                        pass
                    else:
                        print("Vulnerability DB version strings are not as expected. Let's go debugging !")
                        # breakpoint()   # Keeping abreakpoint here. I do not trust the DB :-)

                sev = Severity.parse(severity)
                vulnerability = Vulnerability(sev, exact_ver=vexact, min_ver=vmin, fix_ver=vfix, fixed=fixed, last_vulnerable=vlast_vulnerable, urls=urls, description=description, cves=cves)
                # print(v)
                self.vulnerabilities.append(vulnerability)

            # print(dir(conn))
            # print (conn.execute())
        except Error as err:
            print(err)
        finally:
            if conn:
                conn.close()

    def vulnerability_list(self, check_version: Union[str, Version]) -> List[Vulnerability]:
        """Check grype for the package and returns all found vulnerabilities.

        :param check_version: Returns a list of vulnerabilities matching for that version
        :type check_version: str or Version
        :return: all found vulnerabilities
        :rtype: list of vulnerabilities
        """
        found_vulnerabilities = []

        if isinstance(check_version, str):
            entry = Version(check_version)
        elif isinstance(check_version, Version):
            entry = check_version

        for vulnerability in self.vulnerabilities:
            if vulnerability.version_is_vulnerable(entry):
                found_vulnerabilities.append(vulnerability)

        return found_vulnerabilities

    def count_vulnerabilities(self, rel: Release, severity: Severity) -> int:
        """Return numbers of vulnerabilities of a given severity.

        :param rel: the release to count vulnerabilities in
        :type rel: Release
        :param severity: severity of vulnerabilities to count
        :type severity: Severity
        :return: Number of vulnerabilities of given severity
        :rtype: int
        """
        res = 0

        for vulnerability in self.vulnerability_list(rel.version):
            if vulnerability.severity == severity:
                res += 1
        return res

    def severity_dict(self, check_version: Union[str, Version]) -> dict[Severity, int]:
        """Create a severity dict for this version.

        :param check_version: The version to check
        :type check_version: str or Version
        :return: A dict of severities and their count in this version
        :rtype: a dict of severity and int
        """
        res = {Severity.LOW: 0,
               Severity.MEDIUM: 0,
               Severity.HIGH: 0,
               Severity.CRITICAL: 0}
        for vulnerability in self.vulnerability_list(check_version):
            res[vulnerability.severity] += 1
        return res
