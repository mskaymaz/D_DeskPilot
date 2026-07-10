from dataclasses import dataclass, field, asdict
import json
import os
import shutil

MODULE_ORDER_KEYS = ("battery", "time", "date")
DEFAULT_MODULE_ORDER = list(MODULE_ORDER_KEYS)
TIME_BASE_FONT_SIZE = 30
DATE_BASE_FONT_SIZE = 30
BATTERY_BASE_FONT_SIZE = 30


def normalize_module_order(order):
    result = []
    for key in order if isinstance(order, list) else []:
        if key in MODULE_ORDER_KEYS and key not in result:
            result.append(key)
    for key in MODULE_ORDER_KEYS:
        if key not in result:
            result.append(key)
    return result

from utils import APP_DATA_DIR, SETTINGS_FILE, log_kaydet

UYGULAMA_SURUMU = "1.1.0"  # Uygulamanın merkezi sürüm numarası
AYAR_KURTARMA_MESAJI = ""

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
    time_font_family: str = "Stencil"
    time_color: str = "#00FF7F"
    time_bold: bool = False
    time_24h: bool = True
    time_format_mode: str = "24h"
    time_seconds_scale: float = 0.7
    time_seconds_bold: bool = False
    time_seconds_visible: bool = True

    date_visible: bool = True
    date_format: str = "g a y, h"
    date_font_family: str = "Segoe UI"
    date_color: str = "#000000"
    date_bold: bool = False
    date_show_week_number: bool = False

    battery_visible: bool = True
    battery_font_family: str = "Segoe UI"
    battery_color: str = "#FF0000"
    battery_bold: bool = True
    battery_warning_level: int = 20
    battery_alert_interval: int = 10
    battery_alert_sound_type: str = "Uyarı 1"
    battery_full_alert_enabled: bool = False
    battery_full_alert_level: int = 100

    alarm_visible: bool = True     # Alarm modülü görünürlüğü
    reminder_visible: bool = True  # Hatırlatıcı modülü görünürlüğü
    todo_visible: bool = True      # Görev modülü görünürlüğü


    task_priorities: list = field(default_factory=lambda: [
        {"key": "low", "name": "Düşük", "color": "#22c55e"},
        {"key": "normal", "name": "Normal", "color": "#3b82f6"},
        {"key": "high", "name": "Yüksek", "color": "#f97316"},
    ])
    todo_trash_retention_days: int = 30
    todo_completed_visible_days: int = 7
    todo_cancelled_visible_days: int = 7

    global_scale: float = 1.0      # Task 6.3: Genel ölçeklendirme çarpanı
    time_scale: float = 1.0        # Bağımsız saat ölçeği
    date_scale: float = 1.0        # Bağımsız tarih ölçeği
    battery_scale: float = 1.0     # Bağımsız pil ölçeği

    # --- Ayrı dikey boşluklar ---
    spacing_battery_time: int = 0
    spacing_time_date: int = 0
    spacing_battery_date_hidden: int = 2
    spacing_battery_time_offset: int = 0
    spacing_time_date_offset: int = 0
    spacing_battery_date_hidden_offset: int = 0
    quick_actions_icon_size: int = 38
    quick_actions_icon_spacing: int = 2
    module_order: list = field(default_factory=lambda: list(DEFAULT_MODULE_ORDER))

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
    group_locked: bool = True
    group_layout: dict = field(default_factory=dict)
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


def _clamp(value, min_value, max_value):
    return max(min_value, min(max_value, value))


def _valid_color(value):
    if not isinstance(value, str) or len(value) != 7 or not value.startswith("#"):
        return False
    try:
        int(value[1:], 16)
        return True
    except ValueError:
        return False


def _supported_languages():
    path = os.path.join(os.path.dirname(__file__), "translations")
    if not os.path.isdir(path):
        return {"tr"}
    return {os.path.splitext(name)[0] for name in os.listdir(path) if name.endswith(".json")} or {"tr"}


def _validated_settings_data(data):
    defaults = PanelSettings()
    allowed = set(PanelSettings.__dataclass_fields__.keys())
    data = {_normalize_key(k): v for k, v in data.items()}
    clean = {}

    bool_fields = {
        key for key, value in asdict(defaults).items()
        if isinstance(value, bool)
    }
    int_ranges = {
        "battery_warning_level": (1, 100),
        "battery_alert_interval": (1, 600),
        "battery_full_alert_level": (1, 100),
        "bildirim_soguma_suresi": (0, 3600),
        "quick_actions_icon_size": (24, 80),
        "quick_actions_icon_spacing": (0, 40),
        "spacing_battery_time_offset": (-200, 200),
        "spacing_time_date_offset": (-200, 200),
        "spacing_battery_date_hidden_offset": (-200, 200),
    }
    float_ranges = {
        "seffaflik": (0.1, 1.0),
        "date_opacity": (0.0, 1.0),
        "battery_opacity": (0.0, 1.0),
        "global_scale": (0.5, 2.5),
        "time_scale": (0.5, 3.0),
        "date_scale": (0.5, 3.0),
        "battery_scale": (0.5, 3.0),
        "time_seconds_scale": (0.3, 1.0),
    }
    color_fields = {"time_color", "date_color", "battery_color"}

    for key, value in data.items():
        if key not in allowed:
            continue
        default = getattr(defaults, key)
        if key in bool_fields:
            if isinstance(value, bool):
                clean[key] = value
        elif key in int_ranges:
            if isinstance(value, int) and not isinstance(value, bool):
                clean[key] = int(_clamp(value, *int_ranges[key]))
        elif key in float_ranges:
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                clean[key] = float(_clamp(float(value), *float_ranges[key]))
        elif key in color_fields:
            if _valid_color(value):
                clean[key] = value
        elif key == "language":
            if isinstance(value, str) and value in _supported_languages():
                clean[key] = value
        elif key == "time_format_mode":
            if value in {"24h", "12h_ampm", "12h_plain"}:
                clean[key] = value
        elif key == "module_order":
            clean[key] = normalize_module_order(value)
        elif isinstance(default, str):
            if isinstance(value, str):
                clean[key] = value
        elif isinstance(default, list):
            if isinstance(value, list):
                clean[key] = value
        else:
            clean[key] = value

    clean["module_order"] = normalize_module_order(clean.get("module_order"))
    if clean.get("free_layout_enabled") and clean.get("group_locked"):
        clean["free_layout_enabled"] = False
    return clean


def load_settings():
    global AYAR_KURTARMA_MESAJI
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
                    data = _validated_settings_data(data)
                return PanelSettings(**data)
        except Exception as e:
            log_kaydet(f"Ana dizinden ayarlar yuklenirken hata: {e}", "warning")
            # Yedekleme yap ve devam et
            _yedekle_bozuk_ayar(SETTINGS_FILE)
            AYAR_KURTARMA_MESAJI = "Ayarlar dosyasi okunamadi; yedeklenip varsayilanlar yuklendi."

    # Fall back to local settings file for development
    local_settings = os.path.join(os.path.dirname(__file__), "deskpilot.settings.json")
    if os.path.isfile(local_settings):
        try:
            with open(local_settings, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    log_kaydet("Yerel ayarlar dosyasi bos, varsayilanlar yukleniyor.", "warning")
                    return PanelSettings()
                data = json.loads(content)
                if isinstance(data, dict):
                    data = _validated_settings_data(data)
                    log_kaydet("Yerel ayarlar dosyasi basariyla yuklendi.")
                return PanelSettings(**data)
        except Exception as e:
            log_kaydet(f"Ayarlar yuklenirken hata: {e}", "error")
            _yedekle_bozuk_ayar(local_settings)
            AYAR_KURTARMA_MESAJI = "Yerel ayarlar dosyasi okunamadi; yedeklenip varsayilanlar yuklendi."

    return PanelSettings()

def _yedekle_bozuk_ayar(dosya_yolu):
    """Bozuk JSON dosyasını yedekler."""
    try:
        shutil.copy(dosya_yolu, f"{dosya_yolu}.broken_{int(os.path.getmtime(dosya_yolu))}")
    except Exception as e:
        log_kaydet(f"Bozuk ayar dosyasi yedeklenemedi: {e}", "warning")

def save_settings(settings: PanelSettings):
    try:
        os.makedirs(APP_DATA_DIR, exist_ok=True)
        gecici_dosya = SETTINGS_FILE + ".tmp"
        with open(gecici_dosya, "w", encoding="utf-8") as f:
            json.dump(asdict(settings), f, ensure_ascii=False, indent=2)
        os.replace(gecici_dosya, SETTINGS_FILE)
    except Exception as e:
        log_kaydet(f"Ayarlar kaydedilirken hata: {e}", "error")
