.. _developer-manual-repository:

Repository
==========

:Last Reviewed: 2023-09-05

This project uses sub-projects and retrieves its versioning
information from version control.
Therefore it is crucial that you follow these rules when
working with the project (e.g. for packaging a
development version).

* Make sure that the git project is complete. A call to git status for example should succeed.
* Make sure that you have checked out all available sub-projects.
* Proper initialization of submodules can be ensured with ``git submodule update --init --recursive``

