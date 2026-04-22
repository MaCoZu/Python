"""Text processing utilities."""

import re


def remove_urls(text: str) -> str:
    """Remove URLs from text.

    Args:
        text: Input text

    Returns:
        Text with URLs removed

    Example:
        >>> remove_urls("Check https://example.com for more")
        'Check  for more'
    """
    url_pattern = r"https?://\S+|www\.\S+"
    return re.sub(url_pattern, "", text)


def remove_mentions(text: str) -> str:
    """Remove @mentions from text.

    Args:
        text: Input text

    Returns:
        Text with mentions removed

    Example:
        >>> remove_mentions("Hello @user nice to meet you")
        'Hello  nice to meet you'
    """
    return re.sub(r"@\w+", "", text)


def normalize_whitespace(text: str) -> str:
    """Normalize whitespace in text.

    Args:
        text: Input text

    Returns:
        Text with normalized whitespace

    Example:
        >>> normalize_whitespace("Hello    world\\n\\n  test")
        'Hello world test'
    """
    return re.sub(r"\s+", " ", text).strip()
