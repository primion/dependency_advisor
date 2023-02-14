#!/usr/bin/env python3
#
#
#

import nox

supported_python_versions = ["3.10.7", "3.11.1"]

nox.error_on_external_run=False

@nox.session(python=supported_python_versions,venv_backend='venv')
def flake8(session):
    session.install("flake8")
    session.install("-r", "requirements.txt")
    # E 501 is long line
    session.run("flake8", "--ignore","E501", "lookup.py", "app/package.py", "app/severity.py", "app/version.py", "app/release.py", "app/vulnerability.py")

@nox.session(python=supported_python_versions,venv_backend='venv')
def safety(session):
    session.install("safety")
    session.install("-r", "requirements.txt")
    # safety check -r requirements.txt
    session.run("safety","check", "-r", "requirements.txt")

@nox.session(python=supported_python_versions,venv_backend='venv')
def bandit(session):
    session.install("bandit")
    session.install("-r", "requirements.txt")
    # Check for common vulnerabilities
    # bandit -ll -r  foo.py    ( -ll = medium level and higher, -r recursive)
    session.run("bandit","-ll", "-r", "lookup.py", "app/package.py", "app/severity.py", "app/version.py", "app/release.py", "app/vulnerability.py")

@nox.session(python=supported_python_versions,venv_backend='venv')
def mypy(session):
    session.install("mypy")
    session.install("-r", "requirements.txt")
    # Check for wrong types
    # mypy --strict-optional  app/ plugins/base/
    session.run("mypy","--strict-optional", "lookup.py", "app/package.py", "app/severity.py", "app/version.py", "app/release.py", "app/vulnerability.py")

@nox.session(python=supported_python_versions,venv_backend='venv')
def pylint(session):
    session.install("pylint")
    session.install("-r", "requirements.txt")    
    # pylint --rcfile=pylint.rc  foo.py
    session.run("pylint","--rcfile=pylint.rc", "lookup.py", "app/package.py", "app/severity.py", "app/version.py", "app/release.py", "app/vulnerability.py")

    
