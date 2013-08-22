python-escpos
=============

Ensure the library is installed on ${lib_arch}/${python_ver}/site-packages/escpos

On CLi you must run:
# python setup.py build
# sudo python setup.py install

On Linux, ensure you belongs to the proper group so you can have access to the printer.
This can be done, by adding yourself to 'dialout' group, this might require to re-login
so the changes make effect.

Then, add the following rule to /etc/udev/rules.d/99-escpos.rules
SUBSYSTEM=="usb", ATTRS{idVendor}=="04b8", ATTRS{idProduct}=="0202", MODE="0664", GROUP="dialout"

and restar udev rules.
# sudo service udev restart

Enjoy !!!
And please, don't forget to ALWAYS add Epson.cut() at the end of your printing :)

Manuel F Martinez <manpaz@bashlinux.com>
