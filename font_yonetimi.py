from pathlib import Path

try:
    from PySide6 import QtGui
except ImportError:
    from PyQt6 import QtGui

from utils import resource_path

_PRIMARY_TIME_FONT_FILES = ["DSDigital Bold 700.ttf", "digital7Regular.ttf"]
_OPTIONAL_TIME_FONT_FILES = ["Technology.ttf", "Technology-Bold.ttf"]

_loaded = False
_loaded_families = []


def _add_unique(items, value):
    if value and value not in items:
        items.append(value)


def load_app_fonts():
    global _loaded
    if _loaded:
        return list(_loaded_families)

    for filename in _PRIMARY_TIME_FONT_FILES + _OPTIONAL_TIME_FONT_FILES:
        path = Path(resource_path(f"assets/fonts/{filename}"))
        if not path.exists():
            continue
        font_id = QtGui.QFontDatabase.addApplicationFont(str(path))
        if font_id < 0:
            continue
        for family in QtGui.QFontDatabase.applicationFontFamilies(font_id):
            _add_unique(_loaded_families, family)

    _loaded = True
    return list(_loaded_families)


def default_time_font_family():
    families = load_app_fonts()
    return families[0] if families else "Segoe UI"


def time_font_families():
    result = []
    for family in load_app_fonts():
        _add_unique(result, family)

    try:
        system_families = sorted(QtGui.QFontDatabase.families())
    except TypeError:
        system_families = sorted(QtGui.QFontDatabase().families())

    for family in system_families:
        _add_unique(result, family)
    return result
