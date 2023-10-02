from datetime import datetime
from time import time
from colorama import Fore, init as colinit
from .colors import *
from .console import Settings
from re import sub


class log:
    def __init__(self) -> None:
        colinit(autoreset=True)

    @staticmethod
    def _get_timestamp():
        settings = Settings.presets.get(Settings.LOGPRESET, Settings.presets["default"])
        if Settings.timestamp:
            timestamp = (
                f"{settings.get('Primary')}[" if settings.get("ShowBracket") else ""
            ) + (
                f"{settings.get('Secondary')}"
                + f"{datetime.fromtimestamp(time()).strftime(settings.get('TSFormat'))}"
            ) + (
                f"{settings.get('Primary')}]" if settings.get("ShowBracket") else ""
            ) + f"{Fore.RESET}"
        else:
            timestamp = ""
        return timestamp, settings

    @staticmethod
    def _log_message(level, text, sep=" "):
        timestamp, settings = log._get_timestamp()
        xcol = settings.get("Primary")
        try: text = sub(r'\[(.*?)]', rf'{Settings.c_SECO}[{xcol}\1{Settings.c_SECO}]{Fore.RESET}', text)
        except: pass
        print(
            f"{timestamp} {settings.get(level)} {Fore.LIGHTBLACK_EX}{sep}{Fore.RESET}{text}"
        )

    @staticmethod
    def success(text: str, sep: str = " "):
        log._log_message("SucMsg", text, sep)

    @staticmethod
    def debug(text: str, sep: str = " "):
        log._log_message("DbgMsg", text, sep)

    @staticmethod
    def info(text: str, sep: str = " "):
        log._log_message("InfMsg", text, sep)

    @staticmethod
    def error(text: str, sep: str = " "):
        log._log_message("ErrorMsg", text, sep)

    @staticmethod
    def fatal(text: str, sep: str = " "):
        log._log_message("FtlMsg", text, sep)
