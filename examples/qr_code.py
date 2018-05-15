from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys

from escpos.printer import Usb


def usage():
    print('usage: qr_code.py <content>')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)

    content = sys.argv[1]

    # Adapt to your needs
    p = Usb(0x0416, 0x5011, profile='POS-5890')
    p.qr(content, center=True)
