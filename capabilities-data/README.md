# ESC/POS printer database [![Build Status](https://travis-ci.org/receipt-print-hq/escpos-printer-db.svg?branch=master)](https://travis-ci.org/receipt-print-hq/escpos-printer-db)

This is a community-maintained database of thermal receipt printer capabilities.

The capability data is shared by multiple open source receipt printing projects,
to allow improvements in hardware support, compatibility and localization.

Only features of ESC/POS printers are tracked at this stage. If you have a ZPL,
DPL, or ESC/P printer, it is not in-scope for being listed in this database.

## Browse

A browsable version of the printer database is hosted [here](https://mike42.me/escpos-printer-db). The single-page app that hosts this data is [also open to contributions](https://github.com/receipt-print-hq/escpos-printer-db-browser).

The [data/](https://github.com/receipt-print-hq/escpos-printer-db/tree/master/data) directory in this repository contains the actual printer data, and is where you should send corrections.

## Contribute

This project is open to any kind of contribution, eg.

- Submitting information about your printer
- Writing new profiles
- Typing up legacy code pages

### Add your printer

See: [How to get your printer included in the database](https://github.com/receipt-print-hq/escpos-printer-db/blob/master/doc/add-your-printer.md)

## License

This data and documentation is provided under [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/). See LICENSE.md for details.

## Participating projects

- [python-escpos](https://github.com/python-escpos/python-escpos)
- [escpos-php](https://github.com/mike42/escpos-php)

