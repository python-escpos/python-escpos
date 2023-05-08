"""Test for the CLI

"""


import os
import sys
from scripttest import TestFileEnvironment
from nose.tools import assert_equal, nottest
import escpos

TEST_DIR = os.path.abspath("test/test-cli-output")

DEVFILE_NAME = "testfile"

DEVFILE = os.path.join(TEST_DIR, DEVFILE_NAME)
CONFIGFILE = "testconfig.yaml"
CONFIG_YAML = """
---

printer:
    type: file
    devfile: {testfile}
""".format(
    testfile=DEVFILE,
)


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

    def setup(self):
        """Create a file to print to and set up env"""
        self.env = None
        self.default_args = None

        self.env = TestFileEnvironment(
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

    def teardown(self):
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
        assert_equal(escpos.__version__, result.stdout.strip())

    @nottest  # disable this test as it is not that easy anymore to predict the outcome of this call
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
        assert_equals(result.files_updated[DEVFILE_NAME].bytes, test_text + "\n")

    def test_cli_text_inavlid_args(self):
        """Test a failure to send valid arguments"""
        result = self.env.run(
            *(self.default_args + ("text", "--invalid-param", "some data")),
            expect_error=True,
            expect_stderr=True
        )
        assert_equal(result.returncode, 2)
        assert "error:" in result.stderr
        assert not result.files_updated
