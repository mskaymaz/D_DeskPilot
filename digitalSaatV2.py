import sys
import locale
import ctypes
try:
    from PySide6 import QtWidgets, QtGui
except ImportError:
    from PyQt6 import QtWidgets, QtGui

from utils import APP_ID, resource_path, ICON_FILE, log_altyapisini_kur, log_kaydet
from core_settings import load_settings
from core_window import DraggableTransparentWindow, move_window_safely
from sistem_tepsisi import SistemTepsisi

def main():
    # Loglama altyapısını kur
    log_altyapisini_kur()
    log_kaydet("Uygulama baslatiliyor...")

    if sys.platform == "win32":
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)
        except Exception as e:
            log_kaydet(f"AppUserModelID ayarlanamadi: {e}", "warning")

    app = QtWidgets.QApplication(sys.argv)
    locale.setlocale(locale.LC_TIME, "tr_TR")
    app.setWindowIcon(QtGui.QIcon(resource_path(ICON_FILE)))

    settings = load_settings()
    win = DraggableTransparentWindow(settings)
    
    # Sistem tepsisini başlat ve referansını tut (GC'den korunmak için)
    tray = SistemTepsisi(win, app)
    win.tepsi_ikonu = tray
    tray.show()
    
    win.show()
    move_window_safely(win, settings)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()