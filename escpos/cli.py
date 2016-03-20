#!/usr/bin/env python

from __future__ import absolute_import

import argparse
import sys
import six
from . import config

# Used in demo method
# Key: The name of escpos function and the argument passed on the CLI. Some
#   manual translation is done in the case of barcodes_a -> barcode.
# Value: A list of dictionaries to pass to the escpos function as arguments.
DEMO_FUNCTIONS = {
    'text': [
        {'txt': 'Hello, World!',}
    ],
    'qr': [
        {'text': 'This tests a QR code'},
        {'text': 'https://en.wikipedia.org/'}
    ],
    'barcodes_a': [
        {'bc': 'UPC-A', 'code': '13243546576'},
        {'bc': 'UPC-E', 'code': '132435'},
        {'bc': 'EAN13', 'code': '1324354657687'},
        {'bc': 'EAN8', 'code': '1324354'},
        {'bc': 'CODE39', 'code': 'TEST'},
        {'bc': 'ITF', 'code': '55867492279103'},
        {'bc': 'NW7', 'code': 'A00000000A'},
    ],
    'barcodes_b': [
        {'bc': 'UPC-A', 'code': '13243546576', 'function_type': 'B'},
        {'bc': 'UPC-E', 'code': '132435', 'function_type': 'B'},
        {'bc': 'EAN13', 'code': '1324354657687', 'function_type': 'B'},
        {'bc': 'EAN8', 'code': '1324354', 'function_type': 'B'},
        {'bc': 'CODE39', 'code': 'TEST', 'function_type': 'B'},
        {'bc': 'ITF', 'code': '55867492279103', 'function_type': 'B'},
        {'bc': 'NW7', 'code': 'A00000000A', 'function_type': 'B'},
        {'bc': 'CODE93', 'code': 'A00000000A', 'function_type': 'B'},
        {'bc': 'CODE93', 'code': '1324354657687', 'function_type': 'B'},
        {'bc': 'CODE128A', 'code': 'TEST', 'function_type': 'B'},
        {'bc': 'CODE128B', 'code': 'TEST', 'function_type': 'B'},
        {'bc': 'CODE128C', 'code': 'TEST', 'function_type': 'B'},
        {'bc': 'GS1-128', 'code': '00123456780000000001', 'function_type': 'B'},
        {'bc': 'GS1 DataBar Omnidirectional', 'code': '0000000000000', 'function_type': 'B'},
        {'bc': 'GS1 DataBar Truncated', 'code': '0000000000000', 'function_type': 'B'},
        {'bc': 'GS1 DataBar Limited', 'code': '0000000000000', 'function_type': 'B'},
        {'bc': 'GS1 DataBar Expanded', 'code': '00AAAAAAA', 'function_type': 'B'},
    ]
}

def main():
    """

    Handles loading of configuration and creating and processing of command
    line arguments. Called when run from a CLI.

    """
    saved_config = config.Config()
    printer = saved_config.printer()

    parser = argparse.ArgumentParser(
        description='CLI for python-escpos',
        epilog='Printer configuration is defined in the python-escpos config'
        'file. See documentation for details.',
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

    parser_command_block_text = command_subparsers.add_parser('block_text',
                                                              help='Print wrapped text')
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
    # parser_command_direct_image = command_subparsers.add_parser('direct_direct_image',
    # help='Print an direct_image')
    # parser_command_direct_image.set_defaults(func='direct_image')

    parser_command_charcode = command_subparsers.add_parser('charcode',
                                                            help='Set character code table')
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

    parser_command_panel_buttons = command_subparsers.add_parser('panel_buttons',
                                                                 help='Disables panel buttons')
    parser_command_panel_buttons.set_defaults(func='panel_buttons')
    parser_command_panel_buttons.add_argument(
        '--enable',
        help='Feed button enabled',
        type=bool,
        required=True
    )

    parser_command_raw = command_subparsers.add_parser('raw', help='Raw text')
    parser_command_raw.set_defaults(func='_raw')
    parser_command_raw.add_argument(
        '--msg',
        help='Raw data to send',
        required=True
    )

    parser_command_demo = command_subparsers.add_parser('demo',
                                                        help='Demonstrates various functions')
    parser_command_demo.set_defaults(func='demo')
    demo_group = parser_command_demo.add_mutually_exclusive_group()
    demo_group.add_argument(
        '--barcodes-a',
        help='Print demo barcodes for function type A',
        action='store_true',
    )
    demo_group.add_argument(
        '--barcodes-b',
        help='Print demo barcodes for function type B',
        action='store_true',
    )
    demo_group.add_argument(
        '--qr',
        help='Print some demo QR codes',
        action='store_true',
    )
    demo_group.add_argument(
        '--text',
        help='Print some demo text',
        action='store_true',
    )

    # Get only arguments actually passed
    args_dict = vars(parser.parse_args())
    if not args_dict:
        parser.print_help()
        sys.exit()
    command_arguments = dict([k, v] for k, v in six.iteritems(args_dict) if v)

    if not printer:
        raise Exception('No printers loaded from config')


    target_command = command_arguments.pop('func')

    if hasattr(printer, target_command):
        # print command with args
        getattr(printer, target_command)(**command_arguments)
    else:
        command_arguments['printer'] = printer
        globals()[target_command](**command_arguments)

def demo(printer, **kwargs):
    """
    Prints specificed demos. Called when CLI is passed `demo`. This function
    uses the DEMO_FUNCTIONS dictionary.

    :param printer: A printer from escpos.printer
    :param kwargs: A dict with a key for each function you want to test. It's
        in this format since it usually comes from argparse.
    """
    for demo_choice in kwargs.keys():
        command = getattr(
            printer,
            demo_choice
            .replace('barcodes_a', 'barcode')
            .replace('barcodes_b', 'barcode')
        )
        for params in DEMO_FUNCTIONS[demo_choice]:
            command(**params)
        printer.cut()

if __name__ == '__main__':
    main()
