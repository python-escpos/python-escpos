#!/usr/bin/env python

from __future__ import absolute_import

import argparse
import sys
import serial
import six
import os
import itertools
from ConfigParser import ConfigParser
from escpos import printer

config_filenames = [
    '.python-escpos',
    'python-escpos.ini'
]
config_dirs = [
    os.path.join(os.environ['HOME'], '.config')
]

for environ in ('HOME', 'XDG_CONFIG_HOME'):
    if environ in os.environ:
        config_dirs.append(os.environ[environ])

config_files = [os.path.join(x, y) for x, y in list(itertools.product(config_dirs, config_filenames))]

config = ConfigParser()
files_read = config.read(config_files)
if not files_read:
    raise Exception('Couldn\'t find config files at {config_files}'.format(
        config_files=config_files,
    ))

if 'printer' not in config.sections():
    raise Exception('Couldn\'t find [printer] config section in config_file(s): {files}'.format(
        files="\n".join(files_read),
    ))

printer_config = dict(config.items('printer'))
printer_name = printer_config.pop('type').title()

if not hasattr(printer, printer_name):
    raise Exception('Couldn\'t find printer type {printer_name}'.format(
        printer_name=printer_name,
    ))

try:
    target_printer = getattr(printer, printer_name)(**printer_config)
except TypeError as e:
    raise Exception('Unable to create {printer_name} printer: {error}'.format(
        printer_name=printer_name,
        error=str(e),
    ))

parser = argparse.ArgumentParser(
    description='CLI for python-escpos',
    epilog='Printer configuration is defined in the python-escpos config file.',
)

command_subparsers = parser.add_subparsers(
    title='ESCPOS Command', 
)

# From here on func needs to be a string, since we don't have a printer to work on yet
parser_command_qr = command_subparsers.add_parser('qr', help='Print a QR code')
parser_command_qr.set_defaults(func='qr')
parser_command_qr.add_argument(
    '--text',
    help='Text to print as a qr code',
    required=True
)

parser_command_barcode = command_subparsers.add_parser('barcode', help='Print a barcode')
parser_command_barcode.set_defaults(func='barcode')
parser_command_barcode.add_argument(
    '--code',
    help='Barcode data to print',
    required=True
)
parser_command_barcode.add_argument(
    '--bc',
    help='Barcode format',
    required=True
)
parser_command_barcode.add_argument(
    '--height',
    help='Barcode height in px',
    type=int
)
parser_command_barcode.add_argument(
    '--width',
    help='Barcode width',
    type=int
) 
parser_command_barcode.add_argument(
    '--pos',
    help='Label position',
    choices=['BELOW', 'ABOVE', 'BOTH', 'OFF']
)
parser_command_barcode.add_argument(
    '--font',
    help='Label font',
    choices=['A', 'B']
)
parser_command_barcode.add_argument(
    '--align_ct',
    help='Align barcode center',
    type=bool
)
parser_command_barcode.add_argument(
    '--function_type',
    help='ESCPOS function type',
    choices=['A', 'B']
)

parser_command_text = command_subparsers.add_parser('text', help='Print plain text')
parser_command_text.set_defaults(func='text')
parser_command_text.add_argument(
    '--txt',
    help='Text to print',
    required=True
)

parser_command_block_text = command_subparsers.add_parser('block_text', help='Print wrapped text')
parser_command_block_text.set_defaults(func='block_text')
parser_command_block_text.add_argument(
    '--txt',
    help='block_text to print',
    required=True
)
parser_command_block_text.add_argument(
    '--columns',
    help='Number of columns',
    type=int
)

parser_command_cut = command_subparsers.add_parser('cut', help='Cut the paper')
parser_command_cut.set_defaults(func='cut')
parser_command_cut.add_argument(
    '--mode',
    help='Type of cut',
    choices=['FULL', 'PART']
)

parser_command_cashdraw = command_subparsers.add_parser('cashdraw', help='Kick the cash drawer')
parser_command_cashdraw.set_defaults(func='cashdraw')
parser_command_cashdraw.add_argument(
    '--pin',
    help='Which PIN to kick',
    choices=[2, 5]
)

parser_command_image = command_subparsers.add_parser('image', help='Print an image')
parser_command_image.set_defaults(func='image')
parser_command_image.add_argument(
    '--path_img',
    help='Path to image',
    required=True
)

parser_command_fullimage = command_subparsers.add_parser('fullimage', help='Print an fullimage')
parser_command_fullimage.set_defaults(func='fullimage')
parser_command_fullimage.add_argument(
    '--img',
    help='Path to img',
    required=True
)
parser_command_fullimage.add_argument(
    '--max_height',
    help='Max height of image in px',
    type=int
)
parser_command_fullimage.add_argument(
    '--width',
    help='Max width of image in px',
    type=int
)
parser_command_fullimage.add_argument(
    '--histeq',
    help='Equalize the histrogram',
    type=bool
)
parser_command_fullimage.add_argument(
    '--bandsize',
    help='Size of bands to divide into when printing',
    type=int
)

# Not supported
# parser_command_direct_image = command_subparsers.add_parser('direct_direct_image', help='Print an direct_image')
# parser_command_direct_image.set_defaults(func='direct_image')

parser_command_charcode = command_subparsers.add_parser('charcode', help='Set character code table')
parser_command_charcode.set_defaults(func='charcode')
parser_command_charcode.add_argument(
    '--code',
    help='Character code',
    required=True
)

parser_command_set = command_subparsers.add_parser('set', help='Set text properties')
parser_command_set.set_defaults(func='set')
parser_command_set.add_argument(
    '--align',
    help='Horizontal alignment',
    choices=['left', 'center', 'right']
)
parser_command_set.add_argument(
    '--font',
    help='Font choice',
    choices=['left', 'center', 'right']
)
parser_command_set.add_argument(
    '--text_type',
    help='Text properties',
    choices=['B', 'U', 'U2', 'BU', 'BU2', 'NORMAL']
)
parser_command_set.add_argument(
    '--width',
    help='Width multiplier',
    type=int
)
parser_command_set.add_argument(
    '--height',
    help='Height multiplier',
    type=int
)
parser_command_set.add_argument(
    '--density',
    help='Print density',
    type=int
)
parser_command_set.add_argument(
    '--invert',
    help='White on black printing',
    type=bool
)
parser_command_set.add_argument(
    '--smooth',
    help='Text smoothing. Effective on >= 4x4 text',
    type=bool
)
parser_command_set.add_argument(
    '--flip',
    help='Text smoothing. Effective on >= 4x4 text',
    type=bool
)

parser_command_hw = command_subparsers.add_parser('hw', help='Hardware operations')
parser_command_hw.set_defaults(func='hw')
parser_command_hw.add_argument(
    '--hw',
    help='Operation',
    choices=['INIT', 'SELECT', 'RESET'],
    required=True
)

parser_command_control = command_subparsers.add_parser('control', help='Control sequences')
parser_command_control.set_defaults(func='control')
parser_command_control.add_argument(
    '--ctl',
    help='Control sequence',
    choices=['LF', 'FF', 'CR', 'HT', 'VT'],
    required=True
)
parser_command_control.add_argument(
    '--pos',
    help='Horizontal tab position (1-4)',
    type=int
)

parser_command_panel_buttons = command_subparsers.add_parser('panel_buttons', help='Disables panel buttons')
parser_command_panel_buttons.set_defaults(func='panel_buttons')
parser_command_panel_buttons.add_argument(
    '--enable',
    help='Feed button enabled',
    type=bool,
    required=True
)

# Get only arguments actually passed
args = dict([k, v] for k, v in six.iteritems(vars(parser.parse_args())) if v)

target_command = args.pop('func')
command_arguments = args

# print command with args
getattr(target_printer, target_command)(**command_arguments)
