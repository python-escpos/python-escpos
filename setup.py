#!/usr/bin/python

import os
import sys
from setuptools import find_packages, setup
from setuptools.command.test import test as test_command


base_dir = os.path.dirname(__file__)
src_dir = os.path.join(base_dir, "src")

# When executing the setup.py, we need to be able to import ourselves, this
# means that we need to add the src/ directory to the sys.path.
sys.path.insert(0, src_dir)


def read(fname):
    """read file from same path as setup.py"""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


class Tox(test_command):
    """proxy class that enables tox to be run with setup.py test"""
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        """initialize the user-options"""
        test_command.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        """finalize user-options"""
        test_command.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        """run tox and pass on user-options"""
        # import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)

setup(
    name='python-escpos',
    use_scm_version=True,
    url='https://github.com/python-escpos/python-escpos',
    download_url='https://github.com/python-escpos/python-escpos/archive/master.zip',
    description='Python library to manipulate ESC/POS Printers',
    bugtrack_url='https://github.com/python-escpos/python-escpos/issues',
    license='GNU GPL v3',
    long_description=read('README.rst'),
    author='Manuel F Martinez and others',
    author_email='manpaz@bashlinux.com',
    maintainer='Patrick Kanzler',
    maintainer_email='patrick.kanzler@fablab.fau.de',
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
    package_data={'': ['COPYING']},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
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
        'pyyaml',
    ],
    setup_requires=[
        'setuptools_scm',
    ],
    tests_require=['tox', 'nose', 'scripttest'],
    cmdclass={'test': Tox},
    entry_points={
        'console_scripts': [
            'python-escpos = escpos.cli:main'
        ]
    },
)
