#!/usr/bin/env python3
"""CLI for the dependency lookup tool."""

import argparse
import os
from app.package import Package, Version

##########


def subparser_list(arguments: argparse.Namespace) -> None:
    """Handle sub command list.

    :param arguments: command line arguments
    :type arguments: argparse.Namespace
    :return: None
    """
    apackage = Package(arguments.packagename, arguments.grype_db, alternative_names=arguments.alternative_names.split(","))
    print("Releases sorted by date")
    print(apackage.sorted_releases_str())


def subparser_check(arguments: argparse.Namespace) -> None:
    """Check a specific version.

    :param arguments: command line arguments
    :type arguments: argparse.Namespace
    :return: None
    """
    apackage = Package(arguments.packagename, arguments.grype_db, alternative_names=arguments.alternative_names.split(","))

    vulnerabilities = apackage.vulnerability_list(arguments.packageversion)
    print(f"Vulnerabilities in {arguments.packagename} {arguments.packageversion}")
    for vulnerability in vulnerabilities:
        print(vulnerability)
    print(apackage.severity_dict(arguments.packageversion))


def subparser_alternatives(arguments: argparse.Namespace) -> None:
    """Handle sub command list.

    :param arguments: command line arguments
    :type arguments: argparse.Namespace
    :return: None
    """
    apackage = Package(arguments.packagename, arguments.grype_db, alternative_names=arguments.alternative_names.split(","))
    print("Releases sorted by date")
    earliest = None
    start_release = apackage.get_release(Version(arguments.packageversion))
    if start_release is not None:
        earliest = start_release.published_at
    print(apackage.sorted_releases_str(earliest=earliest, details=True))


def subparser_grype(arguments: argparse.Namespace) -> None:
    """Direct grype call to test the database.

    :param arguments: command line arguments
    :type arguments: argparse.Namespace
    :return: None
    """
    apackage = Package(arguments.packagename, arguments.grype_db, alternative_names=arguments.alternative_names.split(","))
    apackage.test_grype()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog='lookup',
                                     description='looks up all available versions of a program and their vulnerabilities',
                                     epilog='Needs Grype and a API key for libraries.io')

    subparsers = parser.add_subparsers(help='sub-command help')

    # List all releases
    parser_list = subparsers.add_parser('list', help='list all releases and their dates')
    parser_list.set_defaults(func=subparser_list)
    parser_list.add_argument('packagename', help="The name of the package, like 'org.apache.tomcat:tomcat' ")           # positional argument
    parser_list.add_argument('--grype_db', default=os.path.join(os.path.expanduser("~"), ".cache/grype/db/5/vulnerability.db"), help="Exact path to the grype database file")      # option that takes a value
    parser_list.add_argument('--alternative_names', default="", help="A comma separated list of alternative names for grype lookup")      # option that takes a value

    # Check a specific version for issues
    parser_check = subparsers.add_parser('check', help='Check issues in a specific version')
    parser_check.set_defaults(func=subparser_check)
    parser_check.add_argument('packagename', help="The name of the package, like 'org.apache.tomcat:tomcat' ")           # positional argument
    parser_check.add_argument('packageversion', help="The version of the package, like '2.4.1' ")           # positional argument
    parser_check.add_argument('--grype_db', default=os.path.join(os.path.expanduser("~"), ".cache/grype/db/5/vulnerability.db"), help="Exact path to the grype database file")      # option that takes a value
    parser_check.add_argument('--alternative_names', default="", help="A comma separated list of alternative names for grype lookup")      # option that takes a value

    # Check for alternatives for a specific version
    parser_alternatives = subparsers.add_parser('alternatives', help='Find alternatives to update to for a specific version')
    parser_alternatives.set_defaults(func=subparser_alternatives)
    parser_alternatives.add_argument('packagename', help="The name of the package, like 'org.apache.tomcat:tomcat' ")           # positional argument
    parser_alternatives.add_argument('packageversion', help="The version of the package, like '2.4.1' ")           # positional argument
    parser_alternatives.add_argument('--grype_db', default=os.path.join(os.path.expanduser("~"), ".cache/grype/db/5/vulnerability.db"), help="Exact path to the grype database file")  # option that takes a value
    parser_alternatives.add_argument('--alternative_names', default="", help="A comma separated list of alternative names for grype lookup")      # option that takes a value

    # Direct grype cann, direct output.
    parser_grype = subparsers.add_parser('grype', help='Direct call to the grype database, output all matching packages found')
    parser_grype.set_defaults(func=subparser_grype)
    parser_grype.add_argument('packagename', help="The name of the package, like 'org.apache.tomcat:tomcat' ")  # positional argument
    parser_grype.add_argument('--grype_db', default=os.path.join(os.path.expanduser("~"), ".cache/grype/db/5/vulnerability.db"), help="Exact path to the grype database file")      # option that takes a value
    parser_grype.add_argument('--alternative_names', default="", help="A comma separated list of alternative names for grype lookup")      # option that takes a value

    # parser.add_argument('--check_version', default=None, help="like '2.4.1' ")  # positional argument
    args = parser.parse_args()

    args.func(args)

    # TODO output as table / csv
    # TODO outdate cache file
    # TODO smarter grype lookup

    p = Package(args.packagename, args.grype_db)
    print("Latest stable version: " + str(p.latest_stable_version()))
