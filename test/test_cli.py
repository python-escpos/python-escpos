"""Test for the CLI

"""


import os
import shutil
import tempfile

import pytest
from scripttest import TestFileEnvironment as TFE

import escpos

TEST_DIR = tempfile.mkdtemp() + "/cli-test"

DEVFILE_NAME = "testfile"

DEVFILE = os.path.join(TEST_DIR, DEVFILE_NAME)
CONFIGFILE = "testconfig.yaml"
CONFIG_YAML = f"""
---

printer:
    type: file
    devfile: {DEVFILE}
"""


class TestCLI:
    """Contains setups, teardowns, and tests for CLI"""

    @classmethod
    def setup_class(cls):
        """Create a config file to read from"""
        with open(CONFIGFILE, "w") as config:
            config.write(CONFIG_YAML)

    @classmethod
    def teardown_class(cls):
        """Remove config file"""
        os.remove(CONFIGFILE)
        shutil.rmtree(TEST_DIR)

    def setup_method(self):
        """Create a file to print to and set up env"""
        self.env = None
        self.default_args = None

        self.env = TFE(
            base_path=TEST_DIR,
            cwd=os.getcwd(),
        )

        self.default_args = (
            "python-escpos",
            "-c",
            CONFIGFILE,
        )

        fhandle = open(DEVFILE, "a")
        try:
            os.utime(DEVFILE, None)
        finally:
            fhandle.close()

    def teardown_method(self):
        """Destroy printer file and env"""
        os.remove(DEVFILE)
        self.env.clear()

    def test_cli_help(self):
        """Test getting help from cli"""
        result = self.env.run("python-escpos", "-h")
        assert not result.stderr
        assert "usage" in result.stdout

    def test_cli_version(self):
        """Test the version string"""
        result = self.env.run("python-escpos", "version")
        assert not result.stderr
        assert escpos.__version__ == result.stdout.strip()

    def test_cli_version_extended(self):
        """Test the extended version information"""
        result = self.env.run("python-escpos", "version_extended")
        assert not result.stderr
        assert escpos.__version__ in result.stdout
        # test that additional information on e.g. Serial is printed
        assert "Serial" in result.stdout

    @pytest.mark.skip(
        reason="disable this test as it is not that easy anymore to predict the outcome of this call"
    )
    def test_cli_text(self):
        """Make sure text returns what we sent it"""
        test_text = "this is some text"
        result = self.env.run(
            *(
                self.default_args
                + (
                    "text",
                    "--txt",
                    test_text,
                )
            )
        )
        assert not result.stderr
        assert DEVFILE_NAME in result.files_updated.keys()
        assert result.files_updated[DEVFILE_NAME].bytes == test_text + "\n"

    def test_cli_text_invalid_args(self):
        """Test a failure to send valid arguments"""
        result = self.env.run(
            *(self.default_args + ("text", "--invalid-param", "some data")),
            expect_error=True,
            expect_stderr=True,
        )
        assert result.returncode == 2
        assert "error:" in result.stderr
        assert not result.files_updated
