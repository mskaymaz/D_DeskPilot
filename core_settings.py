from dataclasses import dataclass, field, asdict
import json
import os
import shutil

from utils import APP_DATA_DIR, SETTINGS_FILE, log_kaydet

UYGULAMA_SURUMU = "1.1.0"  # Uygulamanın merkezi sürüm numarası

# =======================
# AYARLAR MODELİ
# =======================

@dataclass
class PanelSettings:
    settings_locked: bool = False
    language: str = "tr"
    seffaflik: float = 0.85
    her_zaman_ustte: bool = True
    acilista_calistir: bool = True
    sessiz_mod: bool = False # Task 3.3: Sesli uyarilari kapatir
    bildirim_soguma_suresi: int = 60 # Task 3.2: Saniye cinsinden

    time_visible: bool = True
    time_font_family: str = "DS-Digital"
    time_font_size: int = 30
    time_color: str = "#00FF7F"
    time_bold: bool = False
    time_seconds_scale: float = 0.7
    time_seconds_bold: bool = False
    time_seconds_visible: bool = True

    date_visible: bool = True
    date_format: str = "g a y, h"
    date_font_family: str = "Segoe UI"
    date_color: str = "#000000"
    date_font_size: int = 30
    date_bold: bool = False

    battery_visible: bool = True
    battery_font_family: str = "Segoe UI"
    battery_color: str = "#FF0000"
    battery_bold: bool = True
    battery_warning_level: int = 20
    battery_alert_interval: int = 10
    battery_font_size: int = 30
    battery_alert_sound_type: str = "Uyarı 1"
    battery_full_alert_enabled: bool = False
    battery_full_alert_level: int = 100

    reminder_visible: bool = True # Task 6.1: Hatırlatıcı modülü görünürlüğü
    todo_visible: bool = True      # Task 6.1: Görev modülü görünürlüğü


    task_priorities: list = field(default_factory=lambda: [
        {"key": "low", "name": "Düşük", "color": "#22c55e"},
        {"key": "normal", "name": "Normal", "color": "#3b82f6"},
        {"key": "high", "name": "Yüksek", "color": "#f97316"},
    ])

    global_scale: float = 1.0      # Task 6.3: Genel ölçeklendirme çarpanı
    time_scale: float = 1.0        # Bağımsız saat ölçeği
    date_scale: float = 1.0        # Bağımsız tarih ölçeği
    battery_scale: float = 1.0     # Bağımsız pil ölçeği

    # --- Ayrı dikey boşluklar ---
    spacing_battery_time: int = 0
    spacing_time_date: int = 0
    spacing_battery_date_hidden: int = 2

    coklu_monitor_modu: bool = True # Task 7.4: Modülleri farklı ekranlara dağıtma izni

    # --- Ayrı seffafliklar ---
    date_opacity: float = 1.0
    battery_opacity: float = 1.0

    # --- Pencere pozisyonu ---
    pos_x: int = 0
    pos_y: int = 0
    grup_ekran_adi: str = ""        # Task 7.1: Grup modu ekran adı
    serbest_saat_ekran_adi: str = "" # Task 7.1: Serbest saat ekran adı
    serbest_tarih_ekran_adi: str = "" # Task 7.1: Serbest tarih ekran adı
    serbest_pil_ekran_adi: str = ""   # Task 7.1: Serbest pil ekran adı

    free_layout_enabled: bool = False
    free_layout_has_positions: bool = False
    free_time_x: int = 0
    free_time_y: int = 0
    free_date_x: int = 0
    free_date_y: int = 0
    free_battery_x: int = 0
    free_battery_y: int = 0




def _normalize_key(key: str) -> str:
    tr_map = str.maketrans({
        "ş": "s", "Ş": "s",
        "ç": "c", "Ç": "c",
        "ğ": "g", "Ğ": "g",
        "ü": "u", "Ü": "u",
        "ö": "o", "Ö": "o",
        "ı": "i", "İ": "i",
    })
    lk = key.translate(tr_map).lower()
    if "seffaf" in lk:
        return "seffaflik"
    if "zaman" in lk and "ustte" in lk:
        return "her_zaman_ustte"
    if "acilista" in lk and "calistir" in lk:
        return "acilista_calistir"
    return key


def load_settings():
    # First try the app data directory (for exe)
    if os.path.isfile(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    log_kaydet("Ayarlar dosyasi bos, varsayilanlar yukleniyor.", "warning")
                    return PanelSettings()
                f.seek(0)
                data = json.load(f)
                if isinstance(data, dict):
                    data = { _normalize_key(k): v for k, v in data.items() }
                    allowed = set(PanelSettings.__dataclass_fields__.keys())
                    data = {k: v for k, v in data.items() if k in allowed}
                return PanelSettings(**data)
        except Exception as e:
            log_kaydet(f"Ana dizinden ayarlar yuklenirken hata: {e}", "warning")
            # Yedekleme yap ve devam et
            _yedekle_bozuk_ayar(SETTINGS_FILE)

    # Fall back to local settings file for development
    local_settings = os.path.join(os.path.dirname(__file__), "deskpilot.settings.json")
    if os.path.isfile(local_settings):
        try:
            with open(local_settings, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    data = { _normalize_key(k): v for k, v in data.items() }
                    allowed = set(PanelSettings.__dataclass_fields__.keys())
                    data = {k: v for k, v in data.items() if k in allowed}
                    log_kaydet("Yerel ayarlar dosyasi basariyla yuklendi.")
                return PanelSettings(**data)
        except Exception as e:
            log_kaydet(f"Ayarlar yuklenirken hata: {e}", "error")
            _yedekle_bozuk_ayar(local_settings)

    return PanelSettings()

def _yedekle_bozuk_ayar(dosya_yolu):
    """Bozuk JSON dosyasını yedekler."""
    try:
        shutil.copy(dosya_yolu, f"{dosya_yolu}.broken_{int(os.path.getmtime(dosya_yolu))}")
    except Exception:
        pass

def save_settings(settings: PanelSettings):
    try:
        os.makedirs(APP_DATA_DIR, exist_ok=True)
        gecici_dosya = SETTINGS_FILE + ".tmp"
        with open(gecici_dosya, "w", encoding="utf-8") as f:
            json.dump(asdict(settings), f, ensure_ascii=False, indent=2)
        os.replace(gecici_dosya, SETTINGS_FILE)
    except Exception as e:
        log_kaydet(f"Ayarlar kaydedilirken hata: {e}", "error")
