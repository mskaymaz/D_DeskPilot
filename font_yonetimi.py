import os
import sys

try:
    from PySide6 import QtGui
except ImportError:
    from PyQt6 import QtGui

_FONT_EXTENSIONS = (".ttf", ".otf")
_LOADED_FONT_FAMILIES = None

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


def _resource_roots():
    roots = []
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        roots.append(meipass)
    if getattr(sys, "frozen", False):
        roots.append(os.path.dirname(sys.executable))
    roots.append(os.path.dirname(os.path.abspath(__file__)))

    result = []
    for root in roots:
        root = os.path.abspath(root)
        if root not in result:
            result.append(root)
    return result


def _font_files():
    result = []
    for root in _resource_roots():
        font_dir = os.path.join(root, "assets", "fonts")
        if not os.path.isdir(font_dir):
            continue
        for name in sorted(os.listdir(font_dir)):
            if name.lower().endswith(_FONT_EXTENSIONS):
                path = os.path.join(font_dir, name)
                if path not in result:
                    result.append(path)
    return result


def load_app_fonts():
    global _LOADED_FONT_FAMILIES
    if _LOADED_FONT_FAMILIES is not None:
        return list(_LOADED_FONT_FAMILIES)

    loaded = []
    for font_path in _font_files():
        font_id = QtGui.QFontDatabase.addApplicationFont(font_path)
        if font_id < 0:
            continue
        try:
            families = QtGui.QFontDatabase.applicationFontFamilies(font_id)
        except TypeError:
            families = QtGui.QFontDatabase().applicationFontFamilies(font_id)
        for family in families:
            _add_unique(loaded, family)

    _LOADED_FONT_FAMILIES = loaded
    return list(loaded)


def default_time_font_family():
    families = time_font_families()
    return "Stencil" if "Stencil" in families else (families[0] if families else "Segoe UI")


def time_font_families():
    load_app_fonts()
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
