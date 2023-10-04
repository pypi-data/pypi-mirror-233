from typing import Tuple


def get_trailing_digits(s: str) -> Tuple[str, int]:
    """Returns the trailing digits of a string.

    Args:
        s: the string

    Returns:
        the trailing digits
    """
    for i in range(len(s)):
        if s[i:].isdigit():
            return s[:i],int(s[i:])
    else:
        return s, 1
