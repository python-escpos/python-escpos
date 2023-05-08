import pytest
from escpos.capabilities import get_profile, NotSupported, BARCODE_B, Profile


@pytest.fixture
def profile():
    return get_profile("default")


class TestBaseProfile:
    """Test the `BaseProfile` class."""

    def test_get_font(self, profile):
        with pytest.raises(NotSupported):
            assert profile.get_font("3")
        assert profile.get_font(1) == 1
        assert profile.get_font("a") == 0

    def test_supports(self, profile):
        assert not profile.supports("asdf asdf")
        assert profile.supports(BARCODE_B)

    def test_get_columns(self, profile):
        assert profile.get_columns("a") > 5
        with pytest.raises(NotSupported):
            assert profile.get_columns("asdfasdf")


class TestCustomProfile:
    """Test custom profile options with the `Profile` class."""

    def test_columns(self):
        assert Profile(columns=10).get_columns("sdfasdf") == 10

    def test_features(self):
        assert Profile(features={"foo": True}).supports("foo")
