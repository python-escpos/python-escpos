# How to get your printer included in the database

We aim to list every ESC/POS printer in this database, and we need your help!

## Why is it good to have my printer listed?

Data from this project is used by multiple open source projects to improve
printer compatibility.

If your printer is listed with accurate information, then drivers which use
this data will know how to safely use features like images, QR codes,
barcodes, and non-ASCII text encoding.

## Is my printer in the database already?

Check [the browsable version of this database](https://mike42.me/escpos-printer-db/).

Some printers are sold under several names, so look out for similar model numbers as well.

## Is my printer eligible to be listed?

Any ESC/POS devices can be listed, including:

- ESC/POS thermal and impact printers
- Printers with ESC/POS emulation mode
- Non-printing ESC/POS devices like customer displays

If your printer does not understand ESC/POS, then we wont list it.

## Information to gather

The minimum info that you need to make a printer profile is:

- Vendor name and model number.
- Link to a vendor programming guide that lists supported features if it is available online.
- Paper width (58mm and 80mm are common).

If you don't have documentation, then you need to print some things to try to find out what your printer supports:

- Test page output listing supported character encodings.
- Output of some ESC/POS commands to see what works.

For testing out features, you can send [escpos-php test files](https://github.com/mike42/escpos-php/tree/master/test/integration/resources/output)
to your printer and note the output for each file.

Once you have this, file a [new issue](https://github.com/receipt-print-hq/escpos-printer-db/issues/new) with the information.

## How to write a printer profile

Profiles are written in `yml` syntax. Start by selecting a base profile, then override a
small number of options.

- The `default` profile is a good base for printers with a lot of features
- The `simple` profile is a good base for printers which have very few features

This example is the `TM-U220` profile, which is based on the `simple` profile but notes
that the printer supports two colors, and does not support high-density images.

```yaml
---
TM-U220:
  name: TM-U220
  vendor: Epson
  inherits: simple
  notes: Two-color impact printer with 80mm output
  features:
    bitImageRaster: false
    bitImageColumn: true
    highDensity: false
  colors:
    0: black
    1: alternate
  media:
    width:
      mm: 80
      pixels: Unknown
...
```

As another example, the `SP2000` profile is based on the `default` profile,
but lists the different code pages used by Star printers.

```yaml
---
SP2000:
  name: SP2000 Series
  vendor: Star Micronics
  inherits: default
  notes: Star SP2000 impact printer series with ESC/POS emulation enabled
  features:
    starCommands: true
  codePages:
    # "Normal"
    0: CP437
    1: CP437
    2: CP932
    3: CP437
    # .. code page list continues ...
```

Once you have written a profile for your own printer, send us a pull request with the
new file. The profile will need to pass `yamllint`, an automated build, and be reviewed
by a project contributor.
