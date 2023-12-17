Changelog
=========

2023-12-17 - Version 3.1 - "Rubric Of Ruin"
-------------------------------------------
This is the minor release of the new version 3.1.
It adds a modification of the API of the qr-method,
hence the minor release.

changes
^^^^^^^
- extend API of the qr-method to allow passing image
  parameters in non-native mode
- use version 0.15 and upwards of python-barcode
- fix an issue in the config provider that prevented
  config files to be found when only a path was supplied
- Improve type annotations, usage of six and other
  packaging relevant parts.

contributors
^^^^^^^^^^^^
- Patrick Kanzler
- Alexandre Detiste
- tuxmaster
- belono


2023-11-17 - Version 3.0 - "Quietly Confident"
----------------------------------------------
This is the major release of the new version 3.0.
A big thank you to @belono for their many contributions
for the finalization of v3!

The third major release of this library drops support for
Python 2 and requires a Python version of at least 3.8.
The API has been reworked to be more consistent and two
new concepts have been introduced:

`Capabilities` allow the library to know which features
the currently used printer implements and send fitting
commands.
`Magic Encode` is a new feature that uses the
capability information and encodes Unicode automatically
with the correct code page while sending also the
code page change commands.

The license of the project has been changed to MIT
in accordance with its contributors.

The changes listed here are a summary of the changes
of the previous alpha releases. For details please
read the changelog of the alpha releases.


changes
^^^^^^^
- change the project's license to MIT in accordance with the contributors (see python-escpos/python-escpos#171)
- feature: add "capabilities" which are shared with escpos-php, capabilities are stored in
  `escpos-printer-db <https://github.com/receipt-print-hq/escpos-printer-db>`_
- feature: the driver tries now to guess the appropriate codepage and sets it automatically (called "magic encode")
- as an alternative you can force the codepage with the old API
- fix the encoding search so that lower encodings are found first
- automatically handle cases where full cut or partial cut is not available
- refactor of the set-method
- preliminary support of POS "line display" printing
- add support for software-based barcode-rendering
- make feed for cut optional
- implemented paper sensor querying command
- Include support for CUPS based printer interfaces
- add Win32Raw-Printer on Windows-platforms
- add and improve Windows support of USB-class
- pickle capabilities for faster startup

contributors
^^^^^^^^^^^^
This is a list of contributors since the last v2 release.

- Ahmed Tahri
- akeonly
- Alexander Bougakov
- AlexandroJaez
- Asuki Kono
- belono
- brendanhowell
- Brian
- Christoph Heuel
- csoft2k
- Curtis // mashedkeyboard
- Dmytro Katyukha
- Foaly
- Gerard Marull-Paretas
- Justin Vieira
- kedare
- kennedy
- Lucy Linder
- Maximilian Wagenbach
- Michael Billington
- Michael Elsdörfer
- mrwunderbar666
- NullYing
- Omer Akram
- Patrick Kanzler
- primax79
- Ramon Poca
- reck31
- Romain Porte
- Sam Cheng
- Scott Rotondo
- Sergio Pulgarin
- Thijs Triemstra
- Yaisel Hurtado
- ysuolmai

and others

2023-05-11 - Version 3.0a9 - "Pride Comes Before A Fall"
--------------------------------------------------------
This release is the 10th alpha release of the new version 3.0.
After three years hiatus, a new release is in work in order to
finally get a version 3.0 out.

changes
^^^^^^^
- Include support for CUPS based printer interfaces
- Move the build tool chain to GitHub

contributors
^^^^^^^^^^^^
- belono
- brendanhowell
- AlexandroJaez
- NullYing
- kedare
- Foaly
- patkan
- and others

2020-05-12 - Version 3.0a8 - "Only Slightly Bent"
-------------------------------------------------
This release is the ninth alpha release of the new version 3.0.
Please be aware that the API is subject to change until v3.0 is
released.

This release drops support for Python 2, requiring at least
version 3.5 of Python.

changes
^^^^^^^
- Drop support for Python 2 and mark in setuptools as only supporting 3.5 and upwards
- remove landscape.io badge
- replace viivakoodi with python-barcode which is maintained
- add configuration for Visual Studio Code
- use pkg_resources for the retrieval of the capabilities.json

contributors
^^^^^^^^^^^^
- Romain Porte
- Patrick Kanzler

2020-05-09 - Version 3.0a7 - "No Fixed Abode"
---------------------------------------------
This release is the eight alpha release of the new version 3.0.
Please be aware that the API is subject to change until v3.0
is released.

This release also marks the point at which the project transitioned
to having only a master-branch (and not an additional development branch).

changes
^^^^^^^
- add Exception for NotImplementedError in detach_kernel_driver
- update installation information
- update and improve documentation
- add error handling to image centering flag
- update and fix tox and CI environment, preparing drop of support for Python 2

contributors
^^^^^^^^^^^^
- Alexander Bougakov
- Brian
- Yaisel Hurtado
- Maximilian Wagenbach
- Patrick Kanzler

2019-06-19 - Version 3.0a6 - "Mistake not..."
---------------------------------------------
This release is the seventh alpha release of the new version 3.0.
Please be aware that the API is subject to change until v3.0 is
released.

changes
^^^^^^^
- fix inclusion of the capabilities-file
- execute CI jobs also on Windows and MacOS-targets
- improve documentation

contributors
^^^^^^^^^^^^
- Patrick Kanzler

2019-06-16 - Version 3.0a5 - "Lightly Seared On The Reality Grill"
------------------------------------------------------------------
This release is the sixth alpha release of the new version 3.0. Please
be aware that the API is subject to change until v3.0 is released.

changes
^^^^^^^
- allow arbitrary USB arguments in USB-class
- add Win32Raw-Printer on Windows-platforms
- add and improve Windows support of USB-class
- use pyyaml safe_load()
- improve doc
- implement _read method of Network printer class

contributors
^^^^^^^^^^^^
- Patrick Kanzler
- Gerard Marull-Paretas
- Ramon Poca
- akeonly
- Omer Akram
- Justin Vieira

2018-05-15 - Version 3.0a4 - "Kakistocrat"
------------------------------------------
This release is the fifth alpha release of the new version 3.0. Please
be aware that the API will still change until v3.0 is released.

changes
^^^^^^^
- raise exception when TypeError occurs in cashdraw (#268)
- Feature/clear content in dummy printer (#271)
- fix is_online() (#282)
- improve documentation
- Modified submodule to always pull from master branch (#283)
- parameter for implementation of nonnative qrcode (#289)
- improve platform independence (#296)

contributors
^^^^^^^^^^^^
- Christoph Heuel
- Patrick Kanzler
- kennedy
- primax79
- reck31
- Thijs Triemstra

2017-10-08 - Version 3.0a3 - "Just Testing"
-------------------------------------------
This release is the fourth alpha release of the new version 3.0. Please
be aware that the API will still change until v3.0 is released.

changes
^^^^^^^
- minor changes in documentation, tests and examples
- pickle capabilities for faster startup
- first implementation of centering images and QR
- check barcodes based on regex

contributors
^^^^^^^^^^^^
- Patrick Kanzler
- Lucy Linder
- Romain Porte
- Sergio Pulgarin

2017-08-04 - Version 3.0a2 - "It's My Party And I'll Sing If I Want To"
-----------------------------------------------------------------------
This release is the third alpha release of the new version 3.0. Please
be aware that the API will still change until v3.0 is released.

changes
^^^^^^^
- refactor of the set-method
- preliminary support of POS "line display" printing
- improvement of tests
- added ImageWidthError
- list authors in repository
- add support for software-based barcode-rendering
- fix SerialException when trying to close device on __del__
- added the DLE EOT querying command for USB and Serial
- ensure QR codes have a large enough border
- make feed for cut optional
- fix the behavior of horizontal tabs
- added test script for hard an soft barcodes
- implemented paper sensor querying command
- added weather forecast example script
- added a method for simpler newlines

contributors
^^^^^^^^^^^^
- csoft2k
- Patrick Kanzler
- mrwunderbar666
- Romain Porte
- Ahmed Tahri

2017-03-29 - Version 3.0a1 - "Headcrash"
----------------------------------------
This release is the second alpha release of the new version 3.0. Please
be aware that the API will still change until v3.0 is released.

changes
^^^^^^^
- automatically upload releases to GitHub
- add environment variable ESCPOS_CAPABILITIES_FILE
- automatically handle cases where full cut or partial cut is not available
- add print_and_feed

contributors
^^^^^^^^^^^^
- Sam Cheng
- Patrick Kanzler
- Dmytro Katyukha

2017-01-31 - Version 3.0a - "Grey Area"
---------------------------------------
This release is the first alpha release of the new version 3.0. Please
be aware that the API will still change until v3.0 is released.

changes
^^^^^^^
- change the project's license to MIT in accordance with the contributors (see python-escpos/python-escpos#171)
- feature: add "capabilities" which are shared with escpos-php, capabilities are stored in
  `escpos-printer-db <https://github.com/receipt-print-hq/escpos-printer-db>`_
- feature: the driver tries now to guess the appropriate codepage and sets it automatically (called "magic encode")
- as an alternative you can force the codepage with the old API
- updated and improved documentation
- changed constructor of main class due to introduction of capabilities
- changed interface of method `blocktext`, changed behavior of multiple methods, for details refer to the documentation
  on `python-escpos.readthedocs.io <https://python-escpos.readthedocs.io>`_
- add support for custom cash drawer sequence
- enforce flake8 on the src-files, test py36 and py37 on travis

contributors
^^^^^^^^^^^^
- Michael Billington
- Michael Elsdörfer
- Patrick Kanzler (with code by Frédéric Van der Essen)
- Asuki Kono
- Benito López
- Curtis // mashedkeyboard
- Thijs Triemstra
- ysuolmai

2016-08-26 - Version 2.2.0 - "Fate Amenable To Change"
------------------------------------------------------

changes
^^^^^^^
- fix improper API-use in qrcode()
- change setup.py shebang to make it compatible with virtualenvs.
- add constants for sheet mode and colors
- support changing the line spacing

contributors
^^^^^^^^^^^^
- Michael Elsdörfer
- Patrick Kanzler

2016-08-10 - Version 2.1.3 - "Ethics Gradient"
----------------------------------------------

changes
^^^^^^^
- configure readthedocs and travis
- update doc with hint on image preprocessing
- add fix for printing large images (by splitting them into multiple images)

contributors
^^^^^^^^^^^^
- Patrick Kanzler

2016-08-02 - Version 2.1.2 - "Death and Gravity"
------------------------------------------------

changes
^^^^^^^
- fix File-printer: flush after every call of _raw()
- fix lists in documentation
- fix CODE128: by adding the control character to the barcode-selection-sequence the barcode became unusable

contributors
^^^^^^^^^^^^
- Patrick Kanzler

2016-08-02 - Version 2.1.1 - "Contents May Differ"
--------------------------------------------------

changes
^^^^^^^
- rename variable interface in USB-class to timeout
- add support for hypothesis and move pypy3 to the allowed failures (pypy3 is not supported by hypothesis)

contributors
^^^^^^^^^^^^
- Patrick Kanzler
- Renato Lorenzi

2016-07-23 - Version 2.1.0 - "But Who's Counting?"
--------------------------------------------------

changes
^^^^^^^
- packaging: configured the coverage-analysis codecov.io
- GitHub: improved issues-template
- documentation: add troubleshooting tip to network-interface
- the module, CLI and documentation is now aware of the version of python-escpos
- the CLI does now support basic tab completion

contributors
^^^^^^^^^^^^
- Patrick Kanzler

2016-06-24 - Version 2.0.0 - "Attitude Adjuster"
------------------------------------------------

This version is based on the original version of python-escpos by Manuel F Martinez. However, many contributions have
greatly improved the old codebase. Since this version does not completely match the interface of the version published
on PyPi and has many improvements, it will be released as version 2.0.0.

changes
^^^^^^^
- refactor complete code in order to be compatible with Python 2 and 3
- modernize packaging
- add testing and CI
- merge various forks into codebase, fixing multiple issues with barcode-, QR-printing, cash-draw and structure
- improve the documentation
- extend support of barcode-codes to type B
- add function to disable panel-buttons
- the text-functions are now intended for unicode, the driver will automatically encode the string based on the selected
  codepage
- the image-functions are now much more flexible
- added a CLI
- restructured the constants

contributors
^^^^^^^^^^^^
- Thomas van den Berg
- Michael Billington
- Nate Bookham
- Davis Goglin
- Christoph Heuel
- Patrick Kanzler
- Qian LinFeng

2016-01-24 - Version 1.0.9
--------------------------

- fix constant definition for PC1252
- move documentation to Sphinx

2015-10-27 - Version 1.0.8
--------------------------

- Merge pull request #59 from zouppen/master
    - Support for images vertically longer than 256 pixels
    - Sent by Joel Lehtonen <joel.lehtonen@koodilehto.fi>
- Updated README

2015-08-22 - Version 1.0.7
--------------------------

- Issue #57: Fixed transparent images

2015-07-06 - Version 1.0.6
--------------------------

- Merge pull request #53 from ldos/master
    - Extended params for serial printers
    - Sent by ldos <cafeteria.ldosalzira@gmail.com>

2015-04-21 - Version 1.0.5
--------------------------

- Merge pull request #45 from Krispy2009/master
    - Raising the right error when wrong charcode is used
    - Sent by Kristi <Krispy2009@gmail.com>

2014-05-20 - Version 1.0.4
--------------------------

- Issue #20: Added Density support (Sent by thomas.erbacher@ragapack.de)
- Added charcode tables
- Fixed Horizontal Tab
- Fixed code tabulators

2014-02-23 - Version 1.0.3
--------------------------

- Issue #18: Added quad-area characters (Sent by syncman1x@gmail.com)
- Added exception for PIL import

2013-12-30 - Version 1.0.2
--------------------------

- Issue #5: Fixed vertical tab
- Issue #9: Fixed indentation inconsistency

2013-03-14 - Version 1.0.1
--------------------------

- Issue #8: Fixed set font
- Added QR support

2012-11-15 - Version 1.0
------------------------

- Issue #2: Added Ethernet support
- Issue #3: Added compatibility with libusb-1.0.1
- Issue #4: Fixed typo in escpos.py
