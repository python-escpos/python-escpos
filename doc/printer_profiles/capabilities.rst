.. _capabilities-profile-intro:

Capabilities
------------
:Last Reviewed: 2023-08-10

Since the used command set often differs between printers,
a model for supporting different printers is implemented.
This feature is called `capabilities`.

The `capabilities`-feature allows this library to know
which features are supported.
If no further information is specified, python-escpos will
try to automatically use features based on the supplied information.

In order to use the `capabilities`-database, the printer instance
simply has to be created with the parameter `profile` set to the
relevant identifier.
The identifier can be found in :ref:`available-profiles`.

This documentation describes the profiles in the database file that
is bundled with this release.
If another configuration is to be used, this chapter can be followed
for information on how to side-load another `capabilities`-database:
:ref:`advanced-usage-change-capabilities-profile`.

