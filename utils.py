import sys
import os
import winreg
import logging
from datetime import datetime

# Uygulama Kimlikleri
APP_NAME = "DeskPilot"
APP_ID = "MSK.DeskPilot"
APP_DATA_DIR = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), APP_NAME)
SETTINGS_FILE = os.path.join(APP_DATA_DIR, "settings.json")
ICON_FILE = "assets/icon.ico" if os.path.exists("assets/icon.ico") else "deskpilot.ico"
RUN_REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"

# --- LOGLAMA ALTYAPISI (Task 1.2) ---
LOG_DIR = os.path.join(APP_DATA_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "app.log")

def log_altyapisini_kur():
    """Loglama altyapısını hazırlar."""
    if not os.path.exists(LOG_DIR):
        try:
            os.makedirs(LOG_DIR, exist_ok=True)
        except Exception:
            pass
    
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        encoding='utf-8'
    )

def log_kaydet(mesaj: str, seviye: str = "info"):
    """Belirtilen mesajı log dosyasına kaydeder."""
    seviye = seviye.lower()
    if seviye == "error":
        logging.error(mesaj)
    elif seviye == "warning":
        logging.warning(mesaj)
    else:
        logging.info(mesaj)
    # Konsola da yazdır (Hata ayıklama için)
    try:
        print(f"[{seviye.upper()}] {mesaj}")
    except UnicodeEncodeError:
        pass

def resource_path(relative_path: str) -> str:
    """Paketlenmiş exe veya kaynak klasörü için doğru dosya yolunu döndürür."""
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    full_path = os.path.join(base_path, relative_path)
    if not os.path.exists(full_path):
        # Fallback to current dir if assets are missing in expected path
        return os.path.join(os.path.abspath("."), os.path.basename(relative_path))
    return full_path

def _get_autostart_command():
    """Uygulamayı başlatacak komut satırını oluşturur."""
    if getattr(sys, "frozen", False):
        return f"\"{sys.executable}\""
    script_path = os.path.abspath(sys.argv[0])
    return f"\"{sys.executable}\" \"{script_path}\""

def set_autostart(enabled: bool) -> bool:
    """Windows başlangıç kaydını ekler/siler."""
    if sys.platform != "win32":
        return False
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

def ensure_app_data_dir():
    """Uygulama veri dizininin varlığını garanti eder."""
    if not os.path.exists(APP_DATA_DIR):
        try:
            os.makedirs(APP_DATA_DIR, exist_ok=True)
        except Exception:
            pass

def _enforce_topmost(window):
    """Windows üzerinde bir pencereyi 'topmost' yapar (Görev çubuğu üstünde kalması için)."""
    if sys.platform != "win32":
        return
    try:
        import ctypes
        hwnd = int(window.winId())
        # HWND_TOPMOST = -1
        # SWP_NOMOVE = 0x0002, SWP_NOSIZE = 0x0001, SWP_NOACTIVATE = 0x0010, SWP_SHOWWINDOW = 0x0040
        ctypes.windll.user32.SetWindowPos(
            hwnd, -1, 0, 0, 0, 0, 0x0002 | 0x0001 | 0x0010 | 0x0040
        )
    except Exception:
        pass