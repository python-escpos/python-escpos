#!/usr/bin/python

from distutils.core import setup

setup(
    name='escpos',
    version='1.0.8',
    url='https://github.com/manpaz/python-escpos',
    download_url='https://github.com/manpaz/python-escpos.git',
    description='Python library to manipulate ESC/POS Printers',
    license='GNU GPL v3',
    long_description=open('README').read(),
    author='Manuel F Martinez',
    author_email='manpaz@bashlinux.com',
    platforms=['linux'],
    packages=[
        'escpos',
    ],
    package_data={'': ['COPYING']},
    classifiers=[
        'Development Status :: 1 - Alpha',
        'License :: OSI Approved :: GNU GPL v3',
        'Operating System :: GNU/Linux',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: System :: Peripherals',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'pyusb',
        'Pillow>=2.0',
        'qrcode>=4.0',
        'pyserial',
    ],
)
