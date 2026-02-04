from dataclasses import dataclass, asdict
import json
import os

from utils import APP_DATA_DIR, SETTINGS_FILE

# =======================
# AYARLAR MODELİ
# =======================

@dataclass
class PanelSettings:
    seffaflik: float = 0.85
    her_zaman_üstte: bool = True
    açılışta_çalıştır: bool = True

    time_visible: bool = True
    time_font_family: str = "Segoe UI"
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

    # --- Ayrı dikey boşluklar ---
    spacing_battery_time: int = 0
    spacing_time_date: int = 0
    spacing_battery_date_hidden: int = 2

    # --- Ayrı şeffaflıklar ---
    date_opacity: float = 1.0
    battery_opacity: float = 1.0

    # --- Pencere pozisyonu ---
    pos_x: int = 0
    pos_y: int = 0
    free_layout_enabled: bool = False
    free_layout_has_positions: bool = False
    free_time_x: int = 0
    free_time_y: int = 0
    free_date_x: int = 0
    free_date_y: int = 0
    free_battery_x: int = 0
    free_battery_y: int = 0




def _normalize_key(key: str) -> str:
    lk = key.lower()
    if "effaf" in lk:
        return "seffaflik"
    if "zaman" in lk and ("ust" in lk or "stte" in lk or "?stte" in lk):
        return "her_zaman_ustte"
    if "calistir" in lk or "calistir" in lk:
        return "acilista_calistir"
    return key


def load_settings():
    if os.path.isfile(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    data = { _normalize_key(k): v for k, v in data.items() }
                    allowed = set(PanelSettings.__dataclass_fields__.keys())
                    data = {k: v for k, v in data.items() if k in allowed}
                return PanelSettings(**data)
        except Exception:
            pass
    return PanelSettings()


def save_settings(settings: PanelSettings):
    os.makedirs(APP_DATA_DIR, exist_ok=True)
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(asdict(settings), f, ensure_ascii=False, indent=2)
