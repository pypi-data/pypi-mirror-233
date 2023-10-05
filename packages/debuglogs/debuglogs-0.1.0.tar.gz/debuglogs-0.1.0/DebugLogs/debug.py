"""
Debug File
"""


class BColors:
    """
    Class Containing Ansi Escape Sequences for Color
    """

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    NORMAL = '\033[0m'


def log(text) -> None:
    """
    Debug Logs a message
    :param text: Text to display with debug.
    """
    print(f"{BColors.OKBLUE}Debug Log: {text}.")
    reset_color()


def log_i(text) -> None:
    """
    Debug Logs a message with important coloring.
    :param text: Text to display with debug.
    """
    print(f"{BColors.HEADER}Debug Log: {text}.")
    reset_color()


def log_e(text) -> None:
    """
    Error logs a weak warning.
    :param text: Text to display with debug.
    """
    print(f"{BColors.WARNING}Weak Error Log: {text}.")
    reset_color()


def reset_color() -> None:
    """
    Resets the color of printing
    """
    print(BColors.NORMAL)
