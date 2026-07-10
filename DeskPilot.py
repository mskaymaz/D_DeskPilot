import sys
import locale
import ctypes
try:
    from PySide6 import QtWidgets, QtGui
except ImportError:
    from PyQt6 import QtWidgets, QtGui

from utils import APP_ID, resource_path, ICON_FILE, log_altyapisini_kur, log_kaydet
import core_settings
from core_settings import load_settings
from core_window import DraggableTransparentWindow, move_window_safely
from sistem_tepsisi import SistemTepsisi
from font_yonetimi import load_app_fonts, default_time_font_family
from startup_splash import show_startup_splash

_TEK_ORNEK_MUTEX = None

def tek_ornek_kilidi_al():
    global _TEK_ORNEK_MUTEX
    if sys.platform != "win32":
        return True

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    _TEK_ORNEK_MUTEX = kernel32.CreateMutexW(None, True, f"Local\\{APP_ID}")
    if not _TEK_ORNEK_MUTEX:
        return True
    return ctypes.get_last_error() != 183  # ERROR_ALREADY_EXISTS

def main():
    # Loglama altyapısını kur
    log_altyapisini_kur()

    # --- Tek Örnek Kontrolü (Single Instance Guard) ---
    # Aynı anda yalnız bir uygulama çalışsın; ikinci girişim sessizce çıkar.
    if not tek_ornek_kilidi_al():
        log_kaydet("Uygulama zaten calisiyor, ikinci ornek kapatiliyor.", "warning")
        return

    log_kaydet("Uygulama baslatiliyor...")

    if sys.platform == "win32":
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)
        except Exception as e:
            log_kaydet(f"AppUserModelID ayarlanamadi: {e}", "warning")

    app = QtWidgets.QApplication(sys.argv)
    load_app_fonts()
    locale.setlocale(locale.LC_TIME, "")
    app.setWindowIcon(QtGui.QIcon(resource_path(ICON_FILE)))
    show_startup_splash(app)

    settings = load_settings()
    if core_settings.AYAR_KURTARMA_MESAJI:
        QtWidgets.QMessageBox.warning(None, "Ayar Kurtarma", core_settings.AYAR_KURTARMA_MESAJI)
    if settings.time_font_family in ('', 'Segoe UI', 'Stencil', 'digital7Regular', 'Digital-7'):
        settings.time_font_family = default_time_font_family()
    win = DraggableTransparentWindow(settings)
    
    # Sistem tepsisini başlat ve referansını tut (GC'den korunmak için)
    tray = SistemTepsisi(win, app)
    win.tepsi_ikonu = tray
    tray.show()
    
    if settings.group_locked:
        win.show()
        move_window_safely(win, settings)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
