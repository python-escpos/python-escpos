#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
""" CLI

This module acts as a command line interface for python-escpos. It mirrors
closely the available ESCPOS commands while adding a couple extra ones for convenience.

It requires you to have a configuration file. See documentation for details.

"""


import argparse

try:
    import argcomplete
except ImportError:
    # this CLI works nevertheless without argcomplete
    pass  # noqa
import sys
import six
from . import config
from . import version


# Must be defined before it's used in DEMO_FUNCTIONS
def str_to_bool(string):
    """Used as a type in argparse so that we get back a proper
    bool instead of always True
    """
    return string.lower() in ("y", "yes", "1", "true")


# A list of functions that work better with a newline to be sent after them.
REQUIRES_NEWLINE = ("qr", "barcode", "text", "block_text")


# Used in demo method
# Key: The name of escpos function and the argument passed on the CLI. Some
#   manual translation is done in the case of barcodes_a -> barcode.
# Value: A list of dictionaries to pass to the escpos function as arguments.
DEMO_FUNCTIONS = {
    "text": [
        {
            "txt": "Hello, World!\n",
        }
    ],
    "qr": [
        {"content": "This tests a QR code"},
        {"content": "https://en.wikipedia.org/"},
    ],
    "barcodes_a": [
        {"bc": "UPC-A", "code": "13243546576"},
        {"bc": "UPC-E", "code": "132435"},
        {"bc": "EAN13", "code": "1324354657687"},
        {"bc": "EAN8", "code": "1324354"},
        {"bc": "CODE39", "code": "TEST"},
        {"bc": "ITF", "code": "55867492279103"},
        {"bc": "NW7", "code": "A00000000A"},
    ],
    "barcodes_b": [
        {"bc": "UPC-A", "code": "13243546576", "function_type": "B"},
        {"bc": "UPC-E", "code": "132435", "function_type": "B"},
        {"bc": "EAN13", "code": "1324354657687", "function_type": "B"},
        {"bc": "EAN8", "code": "1324354", "function_type": "B"},
        {"bc": "CODE39", "code": "TEST", "function_type": "B"},
        {"bc": "ITF", "code": "55867492279103", "function_type": "B"},
        {"bc": "NW7", "code": "A00000000A", "function_type": "B"},
        {"bc": "CODE93", "code": "A00000000A", "function_type": "B"},
        {"bc": "CODE93", "code": "1324354657687", "function_type": "B"},
        {"bc": "CODE128A", "code": "TEST", "function_type": "B"},
        {"bc": "CODE128B", "code": "TEST", "function_type": "B"},
        {"bc": "CODE128C", "code": "TEST", "function_type": "B"},
        {"bc": "GS1-128", "code": "00123456780000000001", "function_type": "B"},
        {
            "bc": "GS1 DataBar Omnidirectional",
            "code": "0000000000000",
            "function_type": "B",
        },
        {"bc": "GS1 DataBar Truncated", "code": "0000000000000", "function_type": "B"},
        {"bc": "GS1 DataBar Limited", "code": "0000000000000", "function_type": "B"},
        {"bc": "GS1 DataBar Expanded", "code": "00AAAAAAA", "function_type": "B"},
    ],
}

# Used to build the CLI
# A list of dictionaries. Each dict is a CLI argument.
# Keys:
# parser: A dict of args for command_parsers.add_parser
# defaults: A dict of args for subparser.set_defaults
# arguments: A list of dicts of args for subparser.add_argument
ESCPOS_COMMANDS = [
    {
        "parser": {
            "name": "qr",
            "help": "Print a QR code",
        },
        "defaults": {
            "func": "qr",
        },
        "arguments": [
            {
                "option_strings": ("--content",),
                "help": "Text to print as a qr code",
                "required": True,
            },
            {
                "option_strings": ("--size",),
                "help": "QR code size (1-16) [default:3]",
                "required": False,
                "type": int,
            },
        ],
    },
    {
        "parser": {
            "name": "barcode",
            "help": "Print a barcode",
        },
        "defaults": {
            "func": "barcode",
        },
        "arguments": [
            {
                "option_strings": ("--code",),
                "help": "Barcode data to print",
                "required": True,
            },
            {
                "option_strings": ("--bc",),
                "help": "Barcode format",
                "required": True,
            },
            {
                "option_strings": ("--height",),
                "help": "Barcode height in px",
                "type": int,
            },
            {
                "option_strings": ("--width",),
                "help": "Barcode width",
                "type": int,
            },
            {
                "option_strings": ("--pos",),
                "help": "Label position",
                "choices": ["BELOW", "ABOVE", "BOTH", "OFF"],
            },
            {
                "option_strings": ("--font",),
                "help": "Label font",
                "choices": ["A", "B"],
            },
            {
                "option_strings": ("--align_ct",),
                "help": "Align barcode center",
                "type": str_to_bool,
            },
            {
                "option_strings": ("--function_type",),
                "help": "ESCPOS function type",
                "choices": ["A", "B"],
            },
        ],
    },
    {
        "parser": {
            "name": "text",
            "help": "Print plain text",
        },
        "defaults": {
            "func": "text",
        },
        "arguments": [
            {
                "option_strings": ("--txt",),
                "help": "Plain text to print",
                "required": True,
            }
        ],
    },
    {
        "parser": {
            "name": "block_text",
            "help": "Print wrapped text",
        },
        "defaults": {
            "func": "block_text",
        },
        "arguments": [
            {
                "option_strings": ("--txt",),
                "help": "block_text to print",
                "required": True,
            },
            {
                "option_strings": ("--columns",),
                "help": "Number of columns",
                "type": int,
            },
        ],
    },
    {
        "parser": {
            "name": "cut",
            "help": "Cut the paper",
        },
        "defaults": {
            "func": "cut",
        },
        "arguments": [
            {
                "option_strings": ("--mode",),
                "help": "Type of cut",
                "choices": ["FULL", "PART"],
            },
        ],
    },
    {
        "parser": {
            "name": "cashdraw",
            "help": "Kick the cash drawer",
        },
        "defaults": {
            "func": "cashdraw",
        },
        "arguments": [
            {
                "option_strings": ("--pin",),
                "help": "Which PIN to kick",
                "choices": [2, 5],
            },
        ],
    },
    {
        "parser": {
            "name": "image",
            "help": "Print an image",
        },
        "defaults": {
            "func": "image",
        },
        "arguments": [
            {
                "option_strings": ("--img_source",),
                "help": "Path to image",
                "required": True,
            },
            {
                "option_strings": ("--impl",),
                "help": "Implementation to use",
                "choices": ["bitImageRaster", "bitImageColumn", "graphics"],
            },
            {
                "option_strings": ("--high_density_horizontal",),
                "help": "Image density (horizontal)",
                "type": str_to_bool,
            },
            {
                "option_strings": ("--high_density_vertical",),
                "help": "Image density (vertical)",
                "type": str_to_bool,
            },
        ],
    },
    {
        "parser": {
            "name": "fullimage",
            "help": "Print a fullimage",
        },
        "defaults": {
            "func": "fullimage",
        },
        "arguments": [
            {
                "option_strings": ("--img",),
                "help": "Path to img",
                "required": True,
            },
            {
                "option_strings": ("--max_height",),
                "help": "Max height of image in px",
                "type": int,
            },
            {
                "option_strings": ("--width",),
                "help": "Max width of image in px",
                "type": int,
            },
            {
                "option_strings": ("--histeq",),
                "help": "Equalize the histrogram",
                "type": str_to_bool,
            },
            {
                "option_strings": ("--bandsize",),
                "help": "Size of bands to divide into when printing",
                "type": int,
            },
        ],
    },
    {
        "parser": {
            "name": "charcode",
            "help": "Set character code table",
        },
        "defaults": {
            "func": "charcode",
        },
        "arguments": [
            {
                "option_strings": ("--code",),
                "help": "Character code",
                "required": True,
            },
        ],
    },
    {
        "parser": {
            "name": "set",
            "help": "Set text properties",
        },
        "defaults": {
            "func": "set",
        },
        "arguments": [
            {
                "option_strings": ("--align",),
                "help": "Horizontal alignment",
                "choices": ["left", "center", "right"],
            },
            {
                "option_strings": ("--font",),
                "help": "Font choice",
                "choices": ["left", "center", "right"],
            },
            {
                "option_strings": ("--text_type",),
                "help": "Text properties",
                "choices": ["B", "U", "U2", "BU", "BU2", "NORMAL"],
            },
            {
                "option_strings": ("--width",),
                "help": "Width multiplier",
                "type": int,
            },
            {
                "option_strings": ("--height",),
                "help": "Height multiplier",
                "type": int,
            },
            {
                "option_strings": ("--density",),
                "help": "Print density",
                "type": int,
            },
            {
                "option_strings": ("--invert",),
                "help": "White on black printing",
                "type": str_to_bool,
            },
            {
                "option_strings": ("--smooth",),
                "help": "Text smoothing. Effective on >:  4x4 text",
                "type": str_to_bool,
            },
            {
                "option_strings": ("--flip",),
                "help": "Text smoothing. Effective on >:  4x4 text",
                "type": str_to_bool,
            },
        ],
    },
    {
        "parser": {
            "name": "hw",
            "help": "Hardware operations",
        },
        "defaults": {
            "func": "hw",
        },
        "arguments": [
            {
                "option_strings": ("--hw",),
                "help": "Operation",
                "choices": ["INIT", "SELECT", "RESET"],
                "required": True,
            },
        ],
    },
    {
        "parser": {
            "name": "control",
            "help": "Control sequences",
        },
        "defaults": {
            "func": "control",
        },
        "arguments": [
            {
                "option_strings": ("--ctl",),
                "help": "Control sequence",
                "choices": ["LF", "FF", "CR", "HT", "VT"],
                "required": True,
            },
            {
                "option_strings": ("--pos",),
                "help": "Horizontal tab position (1-4)",
                "type": int,
            },
        ],
    },
    {
        "parser": {
            "name": "panel_buttons",
            "help": "Controls panel buttons",
        },
        "defaults": {
            "func": "panel_buttons",
        },
        "arguments": [
            {
                "option_strings": ("--enable",),
                "help": "Feed button enabled",
                "type": str_to_bool,
                "required": True,
            },
        ],
    },
    {
        "parser": {
            "name": "raw",
            "help": "Raw data",
        },
        "defaults": {
            "func": "_raw",
        },
        "arguments": [
            {
                "option_strings": ("--msg",),
                "help": "Raw data to send",
                "required": True,
            },
        ],
    },
]


def main():
    """

    Handles loading of configuration and creating and processing of command
    line arguments. Called when run from a CLI.

    """

    parser = argparse.ArgumentParser(
        description="CLI for python-escpos",
        epilog="Printer configuration is defined in the python-escpos config"
        "file. See documentation for details.",
    )

    parser.register("type", "bool", str_to_bool)

    # Allow config file location to be passed
    parser.add_argument(
        "-c",
        "--config",
        help="Alternate path to the configuration file",
    )

    # Everything interesting runs off of a subparser so we can use the format
    # cli [subparser] -args
    command_subparsers = parser.add_subparsers(
        title="ESCPOS Command",
        dest="parser",
    )
    # fix inconsistencies in the behaviour of some versions of argparse
    command_subparsers.required = False  # force 'required' testing

    # Build the ESCPOS command arguments
    for command in ESCPOS_COMMANDS:
        parser_command = command_subparsers.add_parser(**command["parser"])
        parser_command.set_defaults(**command["defaults"])
        for argument in command["arguments"]:
            option_strings = argument.pop("option_strings")
            parser_command.add_argument(*option_strings, **argument)

    # Build any custom arguments
    parser_command_demo = command_subparsers.add_parser(
        "demo", help="Demonstrates various functions"
    )
    parser_command_demo.set_defaults(func="demo")
    demo_group = parser_command_demo.add_mutually_exclusive_group()
    demo_group.add_argument(
        "--barcodes-a",
        help="Print demo barcodes for function type A",
        action="store_true",
    )
    demo_group.add_argument(
        "--barcodes-b",
        help="Print demo barcodes for function type B",
        action="store_true",
    )
    demo_group.add_argument(
        "--qr",
        help="Print some demo QR codes",
        action="store_true",
    )
    demo_group.add_argument(
        "--text",
        help="Print some demo text",
        action="store_true",
    )

    parser_command_version = command_subparsers.add_parser(
        "version", help="Print the version of python-escpos"
    )
    parser_command_version.set_defaults(version=True)

    # hook in argcomplete
    if "argcomplete" in globals():
        argcomplete.autocomplete(parser)

    # Get only arguments actually passed
    args_dict = vars(parser.parse_args())
    if not args_dict:
        parser.print_help()
        sys.exit()
    command_arguments = dict(
        [k, v] for k, v in six.iteritems(args_dict) if v is not None
    )

    # If version should be printed, do this, then exit
    print_version = command_arguments.pop("version", None)
    if print_version:
        print(version.version)
        sys.exit()

    # If there was a config path passed, grab it
    config_path = command_arguments.pop("config", None)

    # Load the configuration and defined printer
    saved_config = config.Config()
    saved_config.load(config_path)
    printer = saved_config.printer()

    if not printer:
        raise Exception("No printers loaded from config")

    target_command = command_arguments.pop("func")

    # remove helper-argument 'parser' from dict
    command_arguments.pop("parser", None)

    if hasattr(printer, target_command):
        # print command with args
        getattr(printer, target_command)(**command_arguments)
        if target_command in REQUIRES_NEWLINE:
            printer.text("\n")
    else:
        command_arguments["printer"] = printer
        globals()[target_command](**command_arguments)


def demo(printer, **kwargs):
    """
    Prints demos. Called when CLI is passed `demo`. This function
    uses the DEMO_FUNCTIONS dictionary.

    :param printer: A printer from escpos.printer
    :param kwargs: A dict with a key for each function you want to test. It's
        in this format since it usually comes from argparse.
    """
    for demo_choice in kwargs.keys():
        command = getattr(
            printer,
            demo_choice.replace("barcodes_a", "barcode").replace(
                "barcodes_b", "barcode"
            ),
        )
        for params in DEMO_FUNCTIONS[demo_choice]:
            command(**params)
        printer.cut()


if __name__ == "__main__":
    main()
