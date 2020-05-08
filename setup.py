#!/usr/bin/env python

import os
import sys
from setuptools import find_packages, setup


base_dir = os.path.dirname(__file__)
src_dir = os.path.join(base_dir, "src")

# When executing the setup.py, we need to be able to import ourselves, this
# means that we need to add the src/ directory to the sys.path.
sys.path.insert(0, src_dir)


def read(fname):
    """read file from same path as setup.py"""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setuptools_scm_template = """\
# coding: utf-8
# file generated by setuptools_scm
# don't change, don't track in version control

version = '{version}'
"""


setup(
    name='python-escpos',
    use_scm_version={
        'write_to': 'src/escpos/version.py',
        'write_to_template': setuptools_scm_template,
    },
    url='https://github.com/python-escpos/python-escpos',
    download_url='https://github.com/python-escpos/python-escpos/archive/master.zip',
    description='Python library to manipulate ESC/POS Printers',
    license='MIT',
    long_description=read('README.rst'),
    author='Manuel F Martinez and others',
    author_email='manpaz@bashlinux.com',
    maintainer='Patrick Kanzler',
    maintainer_email='dev@pkanzler.de',
    keywords=[
        'ESC/POS',
        'thermoprinter',
        'voucher printer',
        'printing',
        'receipt,',
    ],
    platforms='any',
    package_dir={"": "src"},
    packages=find_packages(where="src", exclude=["tests", "tests.*"]),
    package_data={'escpos': ['capabilities.json']},
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Office/Business :: Financial :: Point-Of-Sale',
    ],
    install_requires=[
        'pyusb>=1.0.0',
        'Pillow>=2.0',
        'qrcode>=4.0',
        'pyserial',
        'six',
        'appdirs',
        'PyYAML',
        'argparse',
        'argcomplete',
        'future',
        'python-barcode>=0.9.1,<1'
    ],
    setup_requires=[
        'setuptools_scm',
    ],
    tests_require=[
        'jaconv',
        'tox',
        'pytest!=3.2.0,!=3.3.0',
        'pytest-cov',
        'pytest-mock',
        'nose',
        'scripttest',
        'mock',
        'hypothesis>4',
        'flake8'
    ],
    entry_points={
        'console_scripts': [
            'python-escpos = escpos.cli:main'
        ]
    },
)
