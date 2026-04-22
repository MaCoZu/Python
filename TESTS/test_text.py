"""Tests for text processing utilities."""

from SRC.utils.text import normalize_whitespace, remove_mentions, remove_urls


def test_remove_urls() -> None:
    """Test URL removal."""
    text = "Check https://example.com and www.test.com for more"
    result = remove_urls(text)
    assert "https://example.com" not in result
    assert "www.test.com" not in result
    assert "Check" in result
    assert "for more" in result


def test_remove_mentions() -> None:
    """Test mention removal."""
    text = "Hello @user and @another nice to meet you"
    result = remove_mentions(text)
    assert "@user" not in result
    assert "@another" not in result
    assert "Hello" in result
    assert "nice to meet you" in result


def test_normalize_whitespace() -> None:
    """Test whitespace normalization."""
    text = "Hello    world\n\n  test   "
    result = normalize_whitespace(text)
    assert result == "Hello world test"


def test_normalize_whitespace_empty() -> None:
    """Test normalizing empty text."""
    assert normalize_whitespace("") == ""
    assert normalize_whitespace("   ") == ""
