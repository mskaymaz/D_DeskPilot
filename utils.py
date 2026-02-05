import sys
import os
import json
import locale
import winsound
import time
import winreg
import ctypes
from dataclasses import dataclass, asdict
from datetime import datetime

try:
    import psutil
except ImportError:
    psutil = None

try:
    from PySide6 import QtCore, QtGui, QtWidgets
except ImportError:
    from PyQt6 import QtCore, QtGui, QtWidgets

APP_NAME = "DigitalSaat"
APP_ID = "MSK.DigitalSaat"
APP_DATA_DIR = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), APP_NAME)
SETTINGS_FILE = os.path.join(APP_DATA_DIR, "settings.json")
ICON_FILE = "digitalsaaticon.ico"
RUN_REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"


def resource_path(relative_path: str) -> str:
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)


def _get_autostart_command():
    if getattr(sys, "frozen", False):
        return f"\"{sys.executable}\""
    script_path = os.path.abspath(sys.argv[0])
    return f"\"{sys.executable}\" \"{script_path}\""


def set_autostart(enabled: bool):
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_REG_PATH, 0, winreg.KEY_SET_VALUE) as key:
            if enabled:
                winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, _get_autostart_command())
            else:
                try:
                    winreg.DeleteValue(key, APP_NAME)
                except FileNotFoundError:
                    pass
        return True
    except Exception:
        return False
