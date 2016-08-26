*********
Changelog
*********

2016-08-?? - Version 2.?.? - "?"
------------------------------------------------

changes
^^^^^^^
- feature: the driver tries now to guess the appropriate codepage and sets it automatically
- as an alternative you can force the codepage with the old API

contributors
^^^^^^^^^^^^
- Patrick Kanzler (with code by Frédéric Van der Essen)


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
- the module, cli and documentation is now aware of the version of python-escpos
- the cli does now support basic tabcompletion

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
- merge various forks into codebase, fixing multiple issues with barcode-, QR-printing, cashdraw and structure
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
- Issue #9: Fixed identation inconsistence

2013-03-14 - Version 1.0.1
--------------------------

- Issue #8: Fixed set font
- Added QR support

2012-11-15 - Version 1.0
------------------------

- Issue #2: Added ethernet support
- Issue #3: Added compatibility with libusb-1.0.1
- Issue #4: Fixed typo in escpos.py
