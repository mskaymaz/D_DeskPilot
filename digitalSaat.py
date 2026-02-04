# Ver. 03022026 Saat : 16.00  düzeltilmiş versiyon.
# Form 1 tamamlandı.
# pil boş ve dolu yapısı eklendi.



import sys
import os
import json
import locale
import winsound
import time
import winreg
import ctypes
from dataclasses import dataclass, asdict
from datetime import datetime

try:
    import psutil
except ImportError:
    psutil = None

try:
    from PySide6 import QtCore, QtGui, QtWidgets
except ImportError:
    from PyQt6 import QtCore, QtGui, QtWidgets

APP_NAME = "DigitalSaat"
APP_ID = "MSK.DigitalSaat"
APP_DATA_DIR = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), APP_NAME)
SETTINGS_FILE = os.path.join(APP_DATA_DIR, "settings.json")
ICON_FILE = "digitalsaaticon.ico"
RUN_REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"


def resource_path(relative_path: str) -> str:
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)


def _get_autostart_command():
    if getattr(sys, "frozen", False):
        return f"\"{sys.executable}\""
    script_path = os.path.abspath(sys.argv[0])
    return f"\"{sys.executable}\" \"{script_path}\""


def set_autostart(enabled: bool):
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


# =======================
# AYARLAR MODELİ
# =======================

@dataclass
class PanelSettings:
    şeffaflık: float = 0.85
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


# =======================
# AYAR OKU / YAZ
# =======================

def load_settings():
    if os.path.isfile(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
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


# =======================
# GÜVENLİ KONUM
# =======================

def move_window_safely(window, settings):
    app = QtWidgets.QApplication.instance()
    screen = app.screenAt(QtGui.QCursor.pos()) or app.primaryScreen()
    rect = screen.availableGeometry()

    window.adjustSize()
    w, h = window.width(), window.height()

    x, y = settings.pos_x, settings.pos_y

    if not rect.contains(QtCore.QPoint(x, y)):
        x = rect.left() + (rect.width() - w) // 2
        y = rect.top() + (rect.height() - h) // 2
        settings.pos_x = x
        settings.pos_y = y
        save_settings(settings)

    window.move(x, y)


# =======================
# ANA PENCERE
# =======================

class DraggableTransparentWindow(QtWidgets.QWidget):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.drag_pos = None
        self._full_charge_blink_on = False
        self._last_low_batt_alert_ts = 0
        self._low_batt_blink_on = False
        self._last_full_batt_alert_ts = 0


        flags = QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.Window
        if settings.her_zaman_üstte:
            flags |= QtCore.Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowOpacity(settings.şeffaflık)
        self.setWindowIcon(QtGui.QIcon(resource_path(ICON_FILE)))

        # --- Tarih ---
        self.date_label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        # --- Pil ---
        self.battery_label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.battery_icon_label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.battery_icon_label.setVisible(False)

        self.battery_row = QtWidgets.QWidget()
        self.battery_row_layout = QtWidgets.QHBoxLayout(self.battery_row)
        self.battery_row_layout.setContentsMargins(0, 0, 0, 0)
        self.battery_row_layout.setSpacing(4)
        self.battery_row_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.battery_row_layout.addWidget(self.battery_label)
        self.battery_row_layout.addWidget(self.battery_icon_label)


        # === ANA LAYOUT ===
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )
        self.main_layout.setSpacing(0)


        # --- Spacer: Pil ↔ Saat ---
        self.spacer_bt = QtWidgets.QSpacerItem(
            0,
            settings.spacing_battery_time,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Fixed
        )

        # --- Spacer: Saat ↔ Tarih ---
        self.spacer_td = QtWidgets.QSpacerItem(
            0,
            settings.spacing_time_date,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Fixed
        )

        self.time_label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)


        # --- Layout sıralaması ---
        self.main_layout.addWidget(self.battery_row)
        self.main_layout.addItem(self.spacer_bt)
        self.main_layout.addWidget(self.time_label)
        self.main_layout.addItem(self.spacer_td)
        self.main_layout.addWidget(self.date_label)



        for lbl in (
            self.time_label,
            self.date_label,
            self.battery_label,
            self.battery_icon_label
        ):
            lbl.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
            lbl.setContentsMargins(0, 0, 0, 0)
            lbl.setStyleSheet("""
                QLabel {
                    padding: 0px;
                    margin: 0px;
                }
            """)








        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(200)

        self.batt_timer = QtCore.QTimer(self)
        self.batt_timer.timeout.connect(self.update_battery)
        self.batt_timer.start(5000)

        self.full_charge_timer = QtCore.QTimer(self)
        self.full_charge_timer.timeout.connect(self._toggle_full_charge_blink)
        self.full_charge_timer.setInterval(500)

        self.low_batt_timer = QtCore.QTimer(self)
        self.low_batt_timer.timeout.connect(self._toggle_low_batt_blink)
        self.low_batt_timer.setInterval(500)

        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_menu)

        self.apply_settings()
        self.update_time()
        self.update_battery()

    # ---------- AYARLAR ---------- *****************


    def apply_settings(self):
        # --- Saat ---
        font_main = QtGui.QFont(
            self.settings.time_font_family,
            self.settings.time_font_size
        )
        font_main.setBold(self.settings.time_bold)

        self.time_label.setFont(font_main)
        self.time_label.setStyleSheet(
            f"""
            QLabel {{
                color: {self.settings.time_color};
                line-height: {self.settings.time_font_size}px;
                padding: 0px;
                margin: 0px;
            }}
            """
        )
        self.time_label.setVisible(self.settings.time_visible)
        # --- Tarih ---
        df = QtGui.QFont(
            self.settings.date_font_family,
            self.settings.date_font_size
        )
        df.setBold(self.settings.date_bold)
        self.date_label.setFont(df)
        self.date_label.setStyleSheet(
            f"color:{self.settings.date_color};"
            f"opacity:{self.settings.date_opacity};"
        )
        self.date_label.setVisible(self.settings.date_visible)
        self._lock_label_height(self.date_label, self.settings.date_font_size)


        # --- Pil ---
        bf = QtGui.QFont(
            self.settings.battery_font_family,
            self.settings.battery_font_size
        )
        bf.setBold(self.settings.battery_bold)
        self.battery_label.setFont(bf)
        self.battery_label.setStyleSheet(
            f"color:{self.settings.battery_color};"
            f"opacity:{self.settings.battery_opacity};"
        )
        self.battery_label.setVisible(self.settings.battery_visible)
        self._lock_label_height(self.battery_label, self.settings.battery_font_size)

        icon_size = max(1.0, float(self.settings.battery_font_size) * 0.8)
        # Use a symbol font to avoid emoji-size overrides
        bif = QtGui.QFont("Segoe UI Symbol")
        bif.setPointSizeF(icon_size)
        bif.setBold(False)
        self.battery_icon_label.setFont(bif)
        self.battery_icon_label.setStyleSheet(
            f"color:{self.settings.battery_color};"
            f"opacity:{self.settings.battery_opacity};"
            f"font-size:{icon_size}px;"
            "font-family:'Segoe UI Symbol';"
        )
        self._lock_label_height(self.battery_icon_label, int(icon_size))

        self._set_battery_color(self.settings.battery_color)
        self.battery_row_layout.invalidate()
        self.battery_row.adjustSize()
        self.battery_row.updateGeometry()


        # --- Spacer guncelle ---
        if self.settings.time_visible:
            bt_space = self.settings.spacing_battery_time
            td_space = self.settings.spacing_time_date
        else:
            # Saat yok -> pil ile tarih birbirine yakin olsun
            bt_space = 0
            td_space = self.settings.spacing_battery_date_hidden

        self.spacer_bt.changeSize(
            0,
            bt_space,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Fixed
        )

        self.spacer_td.changeSize(
            0,
            td_space,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Fixed
        )

        self.main_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        self.layout().invalidate()
        self.main_layout.activate()
        self.adjustSize()
        self.updateGeometry()
        self.setWindowOpacity(self.settings.şeffaflık)

    def _lock_label_height(self, label, font_size):
        fm = QtGui.QFontMetrics(label.font())
        h = fm.ascent() + fm.descent()
        label.setFixedHeight(h)


    def position_settings_window(self, dialog):
        app = QtWidgets.QApplication.instance()

        screen = app.screenAt(self.frameGeometry().center())
        if not screen:
            screen = app.primaryScreen()

        rect = screen.availableGeometry()

        dialog.adjustSize()
        dw, dh = dialog.width(), dialog.height()

        # Varsayılan: pencerenin SAĞINDA aç
        x = self.x() + self.width() + 10
        y = self.y()

        # Sağdan taşarsa → SOLA al
        if x + dw > rect.right():
            x = self.x() - dw - 10

        # Soldan taşarsa → ekran içine sabitle
        if x < rect.left():
            x = rect.left()

        # Alttan taşarsa → yukarı al
        if y + dh > rect.bottom():
            y = rect.bottom() - dh

        # Üstten taşarsa → aşağı sabitle
        if y < rect.top():
            y = rect.top()

        dialog.move(x, y)



    # ---------- MENÜ ----------

    def show_menu(self, pos):
        menu = QtWidgets.QMenu(self)
        act_settings = menu.addAction("Ayarlar")
        act_exit = menu.addAction("Çıkış")
        action = menu.exec(self.mapToGlobal(pos))
        if action == act_settings:
            self.settings_window = SettingsDialog(self.settings, self)
            self.position_settings_window(self.settings_window)
            self.settings_window.show()
            self.settings_window.raise_()

        elif action == act_exit:
            QtWidgets.QApplication.quit()





    # ---------- GÜNCELLEMELER ----------

    def update_time(self):
        now = datetime.now()
        self.time_label.setText(self._format_time_html(now))
        self.date_label.setText(self._format_date(now))

    def update_battery(self):
        if not psutil or not self.settings.battery_visible:
            self._stop_full_charge_blink()
            self._stop_low_batt_blink()
            return
        b = psutil.sensors_battery()
        if not b:
            self._stop_full_charge_blink()
            self._stop_low_batt_blink()
            return
        if b.power_plugged:
            self.battery_icon_label.setText("\u26A1")
            self.battery_icon_label.setVisible(True)
        else:
            self.battery_icon_label.setVisible(False)
        self.battery_label.setText(f"Pil: {int(b.percent)}%")

        full_alert = (
            self.settings.battery_full_alert_enabled
            and b.power_plugged
            and int(b.percent) >= self.settings.battery_full_alert_level
        )
        low_alert = (not b.power_plugged) and int(b.percent) <= self.settings.battery_warning_level

        if full_alert:
            self._stop_low_batt_blink()
            if not self.full_charge_timer.isActive():
                self._full_charge_blink_on = False
                self.full_charge_timer.start()
            now_ts = time.time()
            if now_ts - self._last_full_batt_alert_ts >= self.settings.battery_alert_interval:
                self._play_batt_alert_sound()
                self._last_full_batt_alert_ts = now_ts
        else:
            self._stop_full_charge_blink()
            self._last_full_batt_alert_ts = 0

        if low_alert and not full_alert:
            if not self.low_batt_timer.isActive():
                self._low_batt_blink_on = False
                self.low_batt_timer.start()
            now_ts = time.time()
            if now_ts - self._last_low_batt_alert_ts >= self.settings.battery_alert_interval:
                self._play_batt_alert_sound()
                self._last_low_batt_alert_ts = now_ts
        else:
            self._stop_low_batt_blink()
            self._last_low_batt_alert_ts = 0

    def _set_battery_color(self, color):
        self.battery_label.setStyleSheet(
            f"color:{color};"
            f"opacity:{self.settings.battery_opacity};"
        )
        icon_size = max(1.0, float(self.settings.battery_font_size) * 0.8)
        self.battery_icon_label.setStyleSheet(
            f"color:{color};"
            f"opacity:{self.settings.battery_opacity};"
            f"font-size:{icon_size}px;"
            "font-family:'Segoe UI Symbol';"
        )

    def _format_time_html(self, now):
        base_size = self.settings.time_font_size
        sec_size = max(1, int(base_size * self.settings.time_seconds_scale))
        weight = "bold" if self.settings.time_bold else "normal"
        sec_weight = "bold" if self.settings.time_seconds_bold else "normal"
        family = self.settings.time_font_family
        color = self.settings.time_color
        hhmm = now.strftime("%H:%M")
        ss = now.strftime("%S")
        if not self.settings.time_seconds_visible:
            return (
                f"<span style='font-family:{family};"
                f" font-size:{base_size}px;"
                f" font-weight:{weight};"
                f" color:{color};'>{hhmm}</span>"
            )
        return (
            f"<span style='font-family:{family};"
            f" font-size:{base_size}px;"
            f" font-weight:{weight};"
            f" color:{color};'>{hhmm}</span>"
            f"<span style='font-family:{family};"
            f" font-size:{sec_size}px;"
            f" font-weight:{sec_weight};"
            f" color:{color};'>:{ss}</span>"
        )

    def _format_date(self, now):
        fmt = self.settings.date_format
        if "%" in fmt:
            return now.strftime(fmt)
        mapping = {
            "g": "%d",
            "G": "%d",
            "a": "%b",
            "A": "%B",
            "y": "%y",
            "Y": "%Y",
            "h": "%a",
            "H": "%A",
        }
        out = []
        for ch in fmt:
            out.append(mapping.get(ch, ch))
        return now.strftime("".join(out))

    def _stop_full_charge_blink(self):
        if self.full_charge_timer.isActive():
            self.full_charge_timer.stop()
        if self._full_charge_blink_on:
            self._full_charge_blink_on = False
        self._set_battery_color(self.settings.battery_color)

    def _toggle_full_charge_blink(self):
        self._full_charge_blink_on = not self._full_charge_blink_on
        color = "#00cc66" if self._full_charge_blink_on else self.settings.battery_color
        self._set_battery_color(color)

    def _stop_low_batt_blink(self):
        if self.low_batt_timer.isActive():
            self.low_batt_timer.stop()
        if self._low_batt_blink_on:
            self._low_batt_blink_on = False
        self._set_battery_color(self.settings.battery_color)

    def _toggle_low_batt_blink(self):
        self._low_batt_blink_on = not self._low_batt_blink_on
        color = "#cc0000" if self._low_batt_blink_on else self.settings.battery_color
        self._set_battery_color(color)

    def _play_batt_alert_sound(self):
        if not winsound:
            return
        sound = self.settings.battery_alert_sound_type
        if sound == "Uyarı 2":
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        elif sound == "Uyarı 3":
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
        else:
            winsound.MessageBeep(winsound.MB_ICONHAND)

    # ---------- SÜRÜKLE ----------

    def mousePressEvent(self, e):
        if e.button() == QtCore.Qt.MouseButton.LeftButton:
            self.drag_pos = e.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        if self.drag_pos:
            self.move(e.globalPosition().toPoint() - self.drag_pos)

            if hasattr(self, "settings_window") and self.settings_window.isVisible():
                self.position_settings_window(self.settings_window)


    def mouseReleaseEvent(self, e):
        self.drag_pos = None
        self.settings.pos_x = self.x()
        self.settings.pos_y = self.y()
        save_settings(self.settings)


# =======================
# AYARLAR DİYALOĞU
# =======================

class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ayarlar")
        self.settings = settings
        self._original_settings = PanelSettings(**asdict(settings))
        self._dirty = False

        self.tabs = QtWidgets.QTabWidget()

        self.tabs.addTab(self._general_tab(), "Genel")
        
      
        self.battery_tab = self._battery_tab()
        self.time_tab = self._time_tab()
        self.date_tab = self._date_tab()


        self.tabs.addTab(self.battery_tab, "Pil")
        self.tabs.addTab(self.time_tab, "Saat")
        self.tabs.addTab(self.date_tab, "Tarih")


      

        
        self.btn_apply = QtWidgets.QPushButton("Uygula")
        self.btn_apply.setEnabled(False)
        self.btn_save = QtWidgets.QPushButton("Kaydet")
        self.btn_cancel = QtWidgets.QPushButton("İptal")

        self.btn_apply.clicked.connect(self.apply_now)
        self.btn_save.clicked.connect(self.save_and_close)
        self.btn_cancel.clicked.connect(self.reject)



        btns = QtWidgets.QHBoxLayout()
        btns.addStretch()
        btns.addWidget(self.btn_cancel)
        btns.addWidget(self.btn_apply)
        btns.addWidget(self.btn_save)


        main = QtWidgets.QVBoxLayout(self)
        main.addWidget(self.tabs)
        main.addLayout(btns)

    def apply_now(self):
        s = self.get_settings()
        self.parent().settings = s
        self.parent().apply_settings()
        if not set_autostart(s.açılışta_çalıştır):
            QtWidgets.QMessageBox.warning(
                self,
                "Açılış Ayarı",
                "Açılışta çalıştır ayarı uygulanamadı.\n"
                "Lütfen yetkileri ve sistem ayarlarını kontrol edin."
            )
        self._set_dirty(False)

    def save_and_close(self):
        self.apply_now()
        save_settings(self.settings)
        self.accept()
    
    def reject(self):
        self._restore_original_settings()
        super().reject()

    def _set_dirty(self, dirty=True):
        self._dirty = dirty
        self.btn_apply.setEnabled(dirty)

    def _restore_original_settings(self):
        for field_name in PanelSettings.__dataclass_fields__:
            setattr(self.settings, field_name, getattr(self._original_settings, field_name))
        if self.parent():
            self.parent().apply_settings()
        self._set_dirty(False)

    def _add_help_link(self, form_layout):
        help_btn = QtWidgets.QPushButton("Yardım")
        help_btn.setFlat(True)
        help_btn.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Fixed
        )
        help_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #C8F7C5;
                border: 1px solid #8ED88A;
                border-radius: 8px;
                color: #1E5E1E;
                padding: 4px 10px;
            }
            QPushButton:hover {
                background-color: #B8F0B4;
            }
            QPushButton:pressed {
                background-color: #A8E7A3;
            }
            """
        )
        help_btn.clicked.connect(self.show_help)
        row = QtWidgets.QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.addStretch()
        row.addWidget(help_btn)
        form_layout.insertRow(0, row)


    def show_help(self):
        idx = self.tabs.currentIndex()
        tab_name = self.tabs.tabText(idx)
        if tab_name == "Genel":
            text = (
                "Genel ayarlar:\n"
                "- Şeffaflık: Kaydırıcıyı sağa/sola çekerek saydamlığı ayarlayın.\n"
                "- Boşluklar: Pil-Saat ve Saat-Tarih arası mesafeyi ayarlayın.\n"
                "- Saat kapalıyken Pil-Tarih boşluğu ayrı ayarlanır."
            )
        elif tab_name == "Pil":
            text = (
                "Pil ayarları:\n"
                "- Uyarı seviyesi: Pil bu yüzdeye düşünce uyarı verir.\n"
                "- Uyarı aralığı: Uyarıların saniye cinsinden tekrar süresi.\n"
                "- Tam dolu uyarısı: Şarjda ve belirlenen yüzde üstünde yeşil yanıp söner.\n"
                "- Renk/Font: Pil satırının görünümünü değiştirir."
            )
        elif tab_name == "Saat":
            text = (
                "Saat ayarları:\n"
                "- Görünürlük: Saat satırını aç/kapat.\n"
                "- Font/Boyut/Renk: Saat görünümünü belirler.\n"
                "- Kalın: Saat ve dakika yazısını kalınlaştırır.\n"
                "- Saniye boyutu (%): Saniyelerin saat/dakikaya oranı.\n"
                "- Saniye kalın: Saniyeleri kalın yapar."
            )
        elif tab_name == "Tarih":
            text = (
                "Tarih ayarları:\n"
                "- Görünürlük: Tarih satırını aç/kapat.\n"
                "- Format: Tarihin yazım biçimini belirler.\n"
                "  Özel kısa format harfleri:\n"
                "  g = gün (01-31), G = gün (01-31)\n"
                "  a = ay kısa (Oca), A = ay uzun (Ocak)\n"
                "  y = yıl kısa (25), Y = yıl uzun (2025)\n"
                "  h = gün kısa (Pzt), H = gün uzun (Pazartesi)\n"
                "  Örnek: g a y, h\n"
                "  % işaretli formatlar da geçerlidir (strftime).\n"
                "- Font/Boyut/Renk: Tarih görünümünü belirler.\n"
                "- Kalın: Yazıyı kalınlaştırır."
            )
        else:
            text = "Bu sekme için yardım metni bulunamadı."

        QtWidgets.QMessageBox.information(self, f"Yardım - {tab_name}", text)


    # ================= GENEL =================

    def _general_tab(self):
        w = QtWidgets.QWidget()
        f = QtWidgets.QFormLayout(w)

        self.chk_top = QtWidgets.QCheckBox("Her zaman üstte")
        self.chk_top.setChecked(self.settings.her_zaman_üstte)
        self.chk_top.toggled.connect(lambda _: self._set_dirty(True))

        self.chk_autostart = QtWidgets.QCheckBox("Açılışta çalıştır")
        self.chk_autostart.setChecked(self.settings.açılışta_çalıştır)
        self.chk_autostart.toggled.connect(lambda _: self._set_dirty(True))

        self.sld_opacity = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.sld_opacity.setRange(10, 100)
        self.sld_opacity.setValue(int(self.settings.şeffaflık * 100))

        self.sld_opacity.valueChanged.connect(self._apply_opacity_preview)

        self.lbl_opacity_value = QtWidgets.QLabel(f"{self.sld_opacity.value()}%")
        f.addRow(self.chk_top)
        f.addRow(self.chk_autostart)
        opacity_row = QtWidgets.QHBoxLayout()
        opacity_row.addWidget(self.sld_opacity)
        opacity_row.addWidget(self.lbl_opacity_value)
        f.addRow("Şeffaflık (%)", opacity_row)

        # --- Pil ↔ Saat boşluğu ---
        self.spn_space_bt = QtWidgets.QSpinBox()
        self.spn_space_bt.setRange(-200, 200)
        self.spn_space_bt.setValue(self.settings.spacing_battery_time)
        self.spn_space_bt.valueChanged.connect(self._apply_general_preview)

        # --- Saat ↔ Tarih boşluğu ---
        self.spn_space_td = QtWidgets.QSpinBox()
        self.spn_space_td.setRange(-200, 200)
        self.spn_space_td.setValue(self.settings.spacing_time_date)
        self.spn_space_td.valueChanged.connect(self._apply_general_preview)

        # --- Pil ↔ Tarih (saat kapalı) ---
        self.spn_space_bd = QtWidgets.QSpinBox()
        self.spn_space_bd.setRange(-200, 200)
        self.spn_space_bd.setValue(self.settings.spacing_battery_date_hidden)
        self.spn_space_bd.valueChanged.connect(self._apply_general_preview)

        f.addRow("Pil ↔ Saat boşluğu", self.spn_space_bt)
        f.addRow("Saat ↔ Tarih boşluğu", self.spn_space_td)
        f.addRow("Pil \u2194 Tarih bo\u015flu\u011fu (saat kapal\u0131yken)", self.spn_space_bd)
        self._add_help_link(f)
        return w

   
    # ================= SAAT =================
    def _time_tab(self):
        w = QtWidgets.QWidget()
        f = QtWidgets.QFormLayout(w)

        self.chk_time_visible = QtWidgets.QCheckBox("Saat görünür")
        self.chk_time_visible.setChecked(self.settings.time_visible)
        self.chk_time_visible.toggled.connect(
            lambda v: self._apply_time_preview(visible=v)
        )

        self.cmb_time_font = QtWidgets.QFontComboBox()
        self.cmb_time_font.setCurrentFont(QtGui.QFont(self.settings.time_font_family))
        self.cmb_time_font.currentFontChanged.connect(
            lambda f: self._apply_time_preview(font=f.family())
        )

        self.spn_time_size = QtWidgets.QSpinBox()
        self.spn_time_size.setRange(20, 200)
        self.spn_time_size.setValue(self.settings.time_font_size)
        self.spn_time_size.valueChanged.connect(
            lambda v: self._apply_time_preview(size=v)
        )

        self.chk_time_bold = QtWidgets.QCheckBox("Kalın")
        self.chk_time_bold.setChecked(self.settings.time_bold)
        self.chk_time_bold.toggled.connect(
            lambda v: self._apply_time_preview(bold=v)
        )

        self.sld_sec_scale = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.sld_sec_scale.setRange(30, 100)
        self.sld_sec_scale.setValue(int(self.settings.time_seconds_scale * 100))
        self.sld_sec_scale.valueChanged.connect(self._apply_seconds_scale_preview)
        self.lbl_sec_scale_value = QtWidgets.QLabel(f"{self.sld_sec_scale.value()}%")

        self.chk_sec_bold = QtWidgets.QCheckBox("Saniye kalın")
        self.chk_sec_bold.setChecked(self.settings.time_seconds_bold)
        self.chk_sec_bold.toggled.connect(
            lambda v: self._apply_time_preview(seconds_bold=v)
        )

        self.chk_sec_visible = QtWidgets.QCheckBox("Saniyeyi gizle")
        self.chk_sec_visible.setChecked(not self.settings.time_seconds_visible)
        self.chk_sec_visible.toggled.connect(
            lambda v: self._apply_time_preview(seconds_visible=not v)
        )

        self.btn_time_color = QtWidgets.QPushButton(self.settings.time_color)
        self.btn_time_color.clicked.connect(
            lambda: self._pick_color(self.btn_time_color)
        )

        f.addRow(self.chk_time_visible)
        f.addRow("Font", self.cmb_time_font)
        f.addRow("Boyut", self.spn_time_size)
        sec_scale_row = QtWidgets.QHBoxLayout()
        sec_scale_row.addWidget(self.sld_sec_scale)
        sec_scale_row.addWidget(self.lbl_sec_scale_value)
        f.addRow("Saniye boyutu (%)", sec_scale_row)
        sec_opts_row = QtWidgets.QHBoxLayout()
        sec_opts_row.addWidget(self.chk_sec_bold)
        sec_opts_row.addWidget(self.chk_sec_visible)
        f.addRow(sec_opts_row)
        f.addRow("Renk", self.btn_time_color)
        f.addRow(self.chk_time_bold)
        self._add_help_link(f)
        return w

    def _apply_time_preview(self, font=None, size=None, bold=None, visible=None, seconds_scale=None, seconds_bold=None, seconds_visible=None):
        if font is not None:
            self.settings.time_font_family = font
        if size is not None:
            self.settings.time_font_size = size
        if bold is not None:
            self.settings.time_bold = bold
        if visible is not None:
            self.settings.time_visible = visible
        if seconds_scale is not None:
            self.settings.time_seconds_scale = seconds_scale
        if seconds_bold is not None:
            self.settings.time_seconds_bold = seconds_bold
        if seconds_visible is not None:
            self.settings.time_seconds_visible = seconds_visible

        self._set_dirty(True)
        self.parent().apply_settings()

    def _apply_seconds_scale_preview(self, value):
        self.settings.time_seconds_scale = value / 100
        self.lbl_sec_scale_value.setText(f"{value}%")
        self._set_dirty(True)
        self.parent().apply_settings()

    def _apply_general_preview(self):
        self.settings.spacing_battery_time = self.spn_space_bt.value()
        self.settings.spacing_time_date = self.spn_space_td.value()
        self.settings.spacing_battery_date_hidden = self.spn_space_bd.value()

        self._set_dirty(True)
        self.parent().apply_settings()

    def _apply_opacity_preview(self, value):
        self.settings.şeffaflık = value / 100
        self.lbl_opacity_value.setText(f"{value}%")
        self._set_dirty(True)
        self.parent().apply_settings()




    # ================= TARİH =================
    def _date_tab(self):
        w = QtWidgets.QWidget()
        f = QtWidgets.QFormLayout(w)

        self.chk_date_visible = QtWidgets.QCheckBox("Tarih görünür")
        self.chk_date_visible.setChecked(self.settings.date_visible)
        self.chk_date_visible.toggled.connect(
            lambda v: self._apply_date_preview(visible=v)
        )

        self.txt_date_format = QtWidgets.QLineEdit(self.settings.date_format)
        self.txt_date_format.textChanged.connect(lambda _: self._set_dirty(True))

        self.cmb_date_font = QtWidgets.QFontComboBox()
        self.cmb_date_font.setCurrentFont(QtGui.QFont(self.settings.date_font_family))
        self.cmb_date_font.currentFontChanged.connect(
            lambda f: self._apply_date_preview(font=f.family())
        )

        self.spn_date_size = QtWidgets.QSpinBox()
        self.spn_date_size.setRange(8, 100)
        self.spn_date_size.setValue(self.settings.date_font_size)
        self.spn_date_size.valueChanged.connect(
            lambda v: self._apply_date_preview(size=v)
        )

        self.chk_date_bold = QtWidgets.QCheckBox("Kalın")
        self.chk_date_bold.setChecked(self.settings.date_bold)
        self.chk_date_bold.toggled.connect(
            lambda v: self._apply_date_preview(bold=v)
        )

        self.btn_date_color = QtWidgets.QPushButton(self.settings.date_color)
        self.btn_date_color.clicked.connect(
            lambda: self._pick_color(self.btn_date_color)
        )

        f.addRow(self.chk_date_visible)
        f.addRow("Format", self.txt_date_format)
        f.addRow("Font", self.cmb_date_font)
        f.addRow("Renk", self.btn_date_color)
        f.addRow("Boyut", self.spn_date_size)
        f.addRow(self.chk_date_bold)
        self._add_help_link(f)
        return w


    def _apply_date_preview(self, font=None, size=None, bold=None, visible=None):
        if font is not None:
            self.settings.date_font_family = font
        if size is not None:
            self.settings.date_font_size = size
        if bold is not None:
            self.settings.date_bold = bold
        if visible is not None:
            self.settings.date_visible = visible

        self._set_dirty(True)
        self.parent().apply_settings()



    # ================= PİL =================
    def _battery_tab(self):
        w = QtWidgets.QWidget()
        f = QtWidgets.QFormLayout(w)

        # --- Görünürlük ---
        self.chk_batt_visible = QtWidgets.QCheckBox("Pil bilgisi görünür")
        self.chk_batt_visible.setChecked(self.settings.battery_visible)
        self.chk_batt_visible.toggled.connect(self._apply_batt_preview)

        # --- Font ---
        self.cmb_batt_font = QtWidgets.QFontComboBox()
        self.cmb_batt_font.setCurrentFont(
            QtGui.QFont(self.settings.battery_font_family)
        )
        self.cmb_batt_font.currentFontChanged.connect(self._apply_batt_preview)

        # --- Font boyutu ---
        self.spn_batt_size = QtWidgets.QSpinBox()
        self.spn_batt_size.setRange(8, 100)
        self.spn_batt_size.setValue(self.settings.battery_font_size)
        self.spn_batt_size.valueChanged.connect(self._apply_batt_preview)

        # --- Kalın ---
        self.chk_batt_bold = QtWidgets.QCheckBox("Kalın")
        self.chk_batt_bold.setChecked(self.settings.battery_bold)
        self.chk_batt_bold.toggled.connect(self._apply_batt_preview)

        # --- Uyarı seviyesi ---
        self.spn_batt_warn = QtWidgets.QSpinBox()
        self.spn_batt_warn.setRange(1, 100)
        self.spn_batt_warn.setValue(self.settings.battery_warning_level)
        self.spn_batt_warn.valueChanged.connect(self._apply_batt_preview)

        # --- Uyarı aralığı ---
        self.spn_batt_interval = QtWidgets.QSpinBox()
        self.spn_batt_interval.setRange(1, 600)
        self.spn_batt_interval.setValue(self.settings.battery_alert_interval)
        self.spn_batt_interval.valueChanged.connect(self._apply_batt_preview)

        # --- Uyarı sesi ---
        self.cmb_batt_sound = QtWidgets.QComboBox()
        self.cmb_batt_sound.addItems(["Uyarı 1", "Uyarı 2", "Uyarı 3"])
        self.cmb_batt_sound.setCurrentText(self.settings.battery_alert_sound_type)
        self.cmb_batt_sound.currentTextChanged.connect(self._apply_batt_preview)

        self.chk_batt_full = QtWidgets.QCheckBox("Tam dolu uyarisi (yesil yanip sonsun)")
        self.chk_batt_full.setChecked(self.settings.battery_full_alert_enabled)
        self.chk_batt_full.toggled.connect(self._apply_batt_preview)

        self.spn_batt_full_level = QtWidgets.QSpinBox()
        self.spn_batt_full_level.setRange(1, 100)
        self.spn_batt_full_level.setValue(self.settings.battery_full_alert_level)
        self.spn_batt_full_level.valueChanged.connect(self._apply_batt_preview)

        # --- Renk ---
        self.btn_batt_color = QtWidgets.QPushButton(self.settings.battery_color)
        self.btn_batt_color.clicked.connect(
            lambda: self._pick_color(self.btn_batt_color)
        )

        # --- Layout ---
        f.addRow(self.chk_batt_visible)
        f.addRow("Uyarı seviyesi (%)", self.spn_batt_warn)
        f.addRow("Uyarı aralığı (sn)", self.spn_batt_interval)
        f.addRow("Uyarı sesi", self.cmb_batt_sound)
        f.addRow(self.chk_batt_full)
        f.addRow("Tam dolu uyarı seviyesi (%)", self.spn_batt_full_level)
        f.addRow("Renk", self.btn_batt_color)
        f.addRow("Font", self.cmb_batt_font)
        f.addRow("Font boyutu", self.spn_batt_size)
        f.addRow(self.chk_batt_bold)
        self._add_help_link(f)
        return w


    def _apply_batt_preview(self):
        self.settings.battery_visible = self.chk_batt_visible.isChecked()
        self.settings.battery_font_family = self.cmb_batt_font.currentFont().family()
        self.settings.battery_font_size = self.spn_batt_size.value()
        self.settings.battery_bold = self.chk_batt_bold.isChecked()
        self.settings.battery_warning_level = self.spn_batt_warn.value()
        self.settings.battery_alert_interval = self.spn_batt_interval.value()
        self.settings.battery_alert_sound_type = self.cmb_batt_sound.currentText()
        self.settings.battery_full_alert_enabled = self.chk_batt_full.isChecked()
        self.settings.battery_full_alert_level = self.spn_batt_full_level.value()

        self._set_dirty(True)
        self.parent().apply_settings()



   

    # ================= ORTAK =================

    def _pick_color(self, btn):
        c = QtWidgets.QColorDialog.getColor()
        if c.isValid():
            btn.setText(c.name())
            self._set_dirty(True)

    def get_settings(self):
        s = self.settings

        s.her_zaman_üstte = self.chk_top.isChecked()
        s.açılışta_çalıştır = self.chk_autostart.isChecked()
        s.şeffaflık = self.sld_opacity.value() / 100

        s.time_visible = self.chk_time_visible.isChecked()
        s.time_font_family = self.cmb_time_font.currentFont().family()
        s.time_font_size = self.spn_time_size.value()
        s.time_bold = self.chk_time_bold.isChecked()
        s.time_color = self.btn_time_color.text()
        s.time_seconds_scale = self.sld_sec_scale.value() / 100
        s.time_seconds_bold = self.chk_sec_bold.isChecked()
        s.time_seconds_visible = not self.chk_sec_visible.isChecked()

        s.date_visible = self.chk_date_visible.isChecked()
        s.date_format = self.txt_date_format.text()
        s.date_font_family = self.cmb_date_font.currentFont().family()
        s.date_font_size = self.spn_date_size.value()

        s.date_bold = self.chk_date_bold.isChecked()
        s.date_color = self.btn_date_color.text()

        s.battery_visible = self.chk_batt_visible.isChecked()
        s.battery_warning_level = self.spn_batt_warn.value()
        s.battery_alert_interval = self.spn_batt_interval.value()
        s.battery_color = self.btn_batt_color.text()
        s.battery_font_size = self.spn_batt_size.value()
        s.battery_alert_sound_type = self.cmb_batt_sound.currentText()
        s.battery_full_alert_enabled = self.chk_batt_full.isChecked()
        s.battery_full_alert_level = self.spn_batt_full_level.value()

        s.spacing_battery_time = self.spn_space_bt.value()
        s.spacing_time_date = self.spn_space_td.value()
        s.spacing_battery_date_hidden = self.spn_space_bd.value()


        return s






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
    win.show()

    move_window_safely(win, settings)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
