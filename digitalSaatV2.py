"""
V2.R260206 Saat 11.00
DigitalSaatV2
Kisa aciklama: Dijital saat, tarih ve pil bilgisini gosteren, ayarlari olan masaustu uygulamasi.
Yerel klasor: D:\\Code\\CodePrivate\\DigitalSaatV2
GitHub repo: https://github.com/mskaymaz/DigitalSaatV2
Not: Bu dosya sadece uygulamayi baslatir; asil mantik modullerde.
"""

import sys
import locale
import ctypes

try:
    from PySide6 import QtCore, QtGui, QtWidgets
except ImportError:
    from PyQt6 import QtCore, QtGui, QtWidgets

from utils import APP_ID, ICON_FILE, resource_path
from core_settings import load_settings
from core_window import DraggableTransparentWindow, move_window_safely


# =======================
# MAIN
# =======================


def main():
    if sys.platform == "win32":
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)
        except Exception:
            pass
    app = QtWidgets.QApplication(sys.argv)
    locale.setlocale(locale.LC_TIME, "tr_TR")
    app.setWindowIcon(QtGui.QIcon(resource_path(ICON_FILE)))

    settings = load_settings()
    win = DraggableTransparentWindow(settings)
    if settings.free_layout_enabled:
        win.hide()
    else:
        win.show()
        move_window_safely(win, settings)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

