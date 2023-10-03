import re


def __reseparate(string: str, separator: str) -> str:
    """Reseparates a string with a given separator.

    Args:
        string (str): The string to reseparate.
        separator (str): The separator to use.

    Returns:
        str: The reseparated string.
    """
    SEPARATOR_REGEX = re.compile(r"(?:\s+|_+|-+)")
    CAPITALISED_REGEX = re.compile(r"(?<=[A-Za-z])(?=[A-Z])")
    COMBINED_REGEX = re.compile(
        SEPARATOR_REGEX.pattern + "|" + CAPITALISED_REGEX.pattern
    )
    return re.sub(COMBINED_REGEX, separator, string).lower()


def camel(string: str) -> str:
    """Converts a string to camel case.

    Args:
        str (str): The string to convert.

    Returns:
        str: The converted string.
    """
    base = pascal(string)
    return base[0].lower() + base[1:]


def kebab(string: str) -> str:
    """Converts a string to kebab case.

    Args:
        str (str): The string to convert.

    Returns:
        str: The converted string.
    """
    return __reseparate(string, "-")


def normal(string: str) -> str:
    """Converts a string to normal case.

    Args:
        str (str): The string to convert.

    Returns:
        str: The converted string.
    """
    return __reseparate(string, " ")


def pascal(string: str) -> str:
    """Converts a string to pascal case.

    Args:
        str (str): The string to convert.

    Returns:
        str: The converted string.
    """
    return "".join([el.title() for el in __reseparate(string, " ").split(" ")])


def snake(string: str) -> str:
    """Converts a string to snake case.

    Args:
        str (str): The string to convert.

    Returns:
        str: The converted string.
    """
    return __reseparate(string, "_")
