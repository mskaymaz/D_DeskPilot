try:
    from PySide6 import QtGui
except ImportError:
    from PyQt6 import QtGui

_PREFERRED_TIME_FONTS = [
    "Stencil",
    "Consolas",
    "Bahnschrift",
    "Segoe UI",
    "Arial",
    "Verdana",
    "Tahoma",
    "Trebuchet MS",
]


def _add_unique(items, value):
    if value and value not in items:
        items.append(value)


def load_app_fonts():
    return []


def default_time_font_family():
    families = time_font_families()
    return "Stencil" if "Stencil" in families else (families[0] if families else "Segoe UI")


def time_font_families():
    result = []
    try:
        system_families = sorted(QtGui.QFontDatabase.families())
    except TypeError:
        system_families = sorted(QtGui.QFontDatabase().families())

    for family in _PREFERRED_TIME_FONTS:
        if family in system_families:
            _add_unique(result, family)

    for family in system_families:
        _add_unique(result, family)
    return result
