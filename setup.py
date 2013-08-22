#!/usr/bin/python

from distutils.core import setup

setup(
    name='escpos',
    version='2.7',
    url='http://code.google.com/p/python-escpos',
    download_url='http://python-escpos.googlecode.com/files/python-escpos-1.0.zip',
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
        'Topic :: System :: Pheripherals',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
