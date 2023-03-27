# dependency_advisor
Guides you through the process of finding a updated version for a dependency with vulnerabilities

## Requirements

A libraries.io API key (https://libraries.io/api):

export LIBRARIES_API_KEY="your_libraries.io_api_key_goes_here"

The python module being used here is https://pypi.org/project/pybraries/

## Vulnerabilities, dependencies and best practice

Most projects contain heaps of dependencies. If not maintained properly they will introduce vulnerabilities (by accidental bugs) or even intentional backdoors.

This is why you should monitor the dependencies you use with tools like Grype.

But what should you do if it is time to update the dependency and move to a new version ? Move to the newest ? Maybe find a version with the same API and fixed vulnerabilities ?

This tool lists the available versions for a specific dependency and the known vulnerabilities there.

YMMV, but I would pick a version with the same major version, all vulnerabilities fixed and a few months old if I have to update a dependency because it is vulnerable.

This tool is your guide.

# Usage

## Finding alternatives for a specific version

./lookup.py alternatives org.springframework.security:spring-security-core 5.4.5

## Check for vulnerabilities in a specific version

./lookup.py check org.springframework.security:spring-security-core 5.6.9

## Alternative names

Some packages have different names in libraries.io and grype. Add grype names als --alternative_names:

./lookup.py alternatives --alternative_names='org.apache.xmlgraphics:batik'  org.apache.xmlgraphics:batik-svggen 1.6
2.6.0
Found 0 entries in grype for org.apache.xmlgraphics:batik-svggen
Found 9 entries in grype for org.apache.xmlgraphics:batik
Releases sorted by date
2008-01-09 10:43:04: 1.7.0-0 Low: 0 Medium: 3 High: 5 Critical: 1
2015-05-11 13:01:01: 1.8.0-0 Low: 0 Medium: 2 High: 5 Critical: 1
2015-11-26 22:57:12: 1.6.1-0 Low: 0 Medium: 3 High: 5 Critical: 1
2016-12-16 15:52:25: 1.7.1-0 Low: 0 Medium: 3 High: 5 Critical: 1
2017-04-11 08:24:23: 1.9.0-0 Low: 0 Medium: 2 High: 4 Critical: 1
2017-07-25 15:03:48: 1.9.1-0 Low: 0 Medium: 2 High: 4 Critical: 1
2018-05-11 14:01:48: 1.10.0-0 Low: 0 Medium: 2 High: 4 Critical: 0
2019-02-01 15:55:09: 1.11.0-0 Low: 0 Medium: 2 High: 4 Critical: 0
2019-10-25 10:29:50: 1.12.0-0 Low: 0 Medium: 2 High: 4 Critical: 0
2020-05-05 13:46:35: 1.13.0-0 Low: 0 Medium: 2 High: 3 Critical: 0
2021-01-12 13:40:46: 1.14.0-0 Low: 0 Medium: 2 High: 3 Critical: 0
2022-09-15 10:37:03: 1.15.0-0 Low: 0 Medium: 0 High: 2 Critical: 0
2022-10-14 11:25:45: 1.16.0-0 Low: 0 Medium: 0 High: 0 Critical: 0

1.16.0 is a bugfix only release (see changelog online), is a few months old already and has 0 reported vulnerabilities. A good candidate.

