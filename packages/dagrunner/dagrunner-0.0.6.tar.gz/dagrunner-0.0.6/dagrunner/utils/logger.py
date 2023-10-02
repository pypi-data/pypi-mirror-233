"""Logger class for logging information"""
from termcolor import cprint, colored


class Logger:
    """Logger class for logging information"""
    @staticmethod
    def info(msg):
        """Log debug information"""
        cprint(msg)

    @staticmethod
    def success(msg):
        """Log success message"""
        cprint(colored(msg, "green", attrs=["bold"]))

    @staticmethod
    def error(msg):
        """Log error message"""
        cprint(colored(msg, "red", attrs=["bold"]))

    @staticmethod
    def debug(msg):
        """Log debug information"""
        cprint(colored(msg, attrs=["bold"]))
