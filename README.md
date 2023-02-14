# dependency_advisor
Guides you through the process of finding a updated version for a dependency with vulnerabilities

## Vulnerabilities, dependencies and best practice

Most projects contain heaps of dependencies. If not maintained properly they will introduce vulnerabilities (by accidental bugs) or even intentional backdoors.

This is why you should monitor the dependencies you use with tools like Grype.

But what should you do if it is time to update the dependency and move to a new version ? Move to the newest ? Maybe find a version with the same API and fixed vulnerabilities ?

This tool lists the available versions for a specific dependency and the known vulnerabilities there.

YMMV, but I would pick a version with the same major version, all vulnerabilities fixed and a few months old if I have to update a dependency because it is vulnerable.

This tool is your guide.