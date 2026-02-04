# Ver. 02022026 Saat : 17.00  düzeltilmiş versiyon.

import sys
import os
import json
import locale
import winsound
import time
import subprocess
from dataclasses import dataclass, asdict
from datetime import datetime

try:
    import psutil
except ImportError:
    psutil = None

QT_LIB = None
try:
    from PySide6 import QtCore, QtGui, QtWidgets
    QT_LIB = "pyside6"
except ImportError:
    from PyQt6 import QtCore, QtGui, QtWidgets
    QT_LIB = "pyqt6"

APP_NAME = "DigitalSaat"
APP_DATA_DIR = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), APP_NAME)
SETTINGS_FILE = os.path.join(APP_DATA_DIR, "settings.json")


# =======================
# AYARLAR MODELİ
# =======================

@dataclass
class PanelSettings:
    şeffaflık: float = 0.75
    her_zaman_üstte: bool = True
    açılışta_çalıştır: bool = False

    time_visible: bool = True
    time_font_family: str = "Stencil"
    time_font_size: int = 80
    time_color: str = "#00FF7F"
    time_bold: bool = False

    date_visible: bool = True
    date_format: str = "%d %B %Y, %A"
    date_font_family: str = "Segoe UI"
    date_color: str = "#000000"
    date_bold: bool = False

    battery_visible: bool = True
    battery_font_family: str = "Segoe UI"
    battery_color: str = "#FF0000"
    battery_bold: bool = True
    battery_warning_level: int = 20
    battery_alert_interval: int = 10
    battery_alert_sound_type: str = "Uyarı 1"

    # --- Ayrı dikey boşluklar ---
    spacing_battery_time: int = 5
    spacing_time_date: int = 5

    # --- Ayrı font boyutları ---
    date_font_size: int = 22
    battery_font_size: int = 26

    # --- Ayrı şeffaflıklar ---
    time_opacity: float = 1.0
    date_opacity: float = 1.0
    battery_opacity: float = 1.0


    #spacing: int = -40
    margins: int = 0

    pos_x: int = 0
    pos_y: int = 0


# =======================
# AYAR OKU / YAZ
# =======================

def load_settings():
    if os.path.isfile(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return PanelSettings(**json.load(f))
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


        flags = QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.Window
        if settings.her_zaman_üstte:
            flags |= QtCore.Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowOpacity(settings.şeffaflık)

        # --- Tarih ---
        self.date_label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        # --- Pil ---
        self.battery_label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)


        # === ANA LAYOUT ===
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(
            settings.margins,
            settings.margins,
            settings.margins,
            settings.margins
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
        self.main_layout.addWidget(self.battery_label)
        self.main_layout.addItem(self.spacer_bt)
        self.main_layout.addWidget(self.time_label)
        self.main_layout.addItem(self.spacer_td)
        self.main_layout.addWidget(self.date_label)



        for lbl in (
            self.time_label,
            self.date_label,
            self.battery_label
        ):
            lbl.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)







        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(200)

        self.batt_timer = QtCore.QTimer(self)
        self.batt_timer.timeout.connect(self.update_battery)
        self.batt_timer.start(5000)

        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_menu)

        self.apply_settings()
        self.update_time()
        self.update_battery()

    # ---------- AYARLAR ---------- *****************


    def get_current_screen_geometry(self):
        center = self.frameGeometry().center()
        screen = QtWidgets.QApplication.screenAt(center)

        if screen is None:
            screen = QtWidgets.QApplication.primaryScreen()

        return screen.availableGeometry()

    
    def apply_settings(self):
        # --- Saat ---
        tf = QtGui.QFont(
            self.settings.time_font_family,
            self.settings.time_font_size
        )
        tf.setBold(self.settings.time_bold)
        
        base_size = self.settings.time_font_size
        ss_size = int(base_size * 0.5)

        font_main = QtGui.QFont(self.settings.time_font_family, base_size)
        font_main.setBold(self.settings.time_bold)

        font_sec = QtGui.QFont(self.settings.time_font_family, ss_size)
        font_sec.setBold(self.settings.time_bold)

        base = self.settings.time_font_size
        ss_size = int(base * 0.6)

        font_main = QtGui.QFont(self.settings.time_font_family, base)
        font_main.setBold(self.settings.time_bold)

        font_sec = QtGui.QFont(self.settings.time_font_family, ss_size)
        font_sec.setBold(self.settings.time_bold)

        font = QtGui.QFont(
            self.settings.time_font_family,
            self.settings.time_font_size
        )

        self.time_label.setFont(font)
        self.time_label.setStyleSheet(
            f"color:{self.settings.time_color};"
            f"opacity:{self.settings.time_opacity};"
        )
        self.time_label.setVisible(self.settings.time_visible)



        base_size = self.settings.time_font_size
        ss_size = int(base_size * 0.6)

        font_main = QtGui.QFont(self.settings.time_font_family, base_size)
        font_main.setBold(self.settings.time_bold)

        font_sec = QtGui.QFont(self.settings.time_font_family, ss_size)
        font_sec.setBold(self.settings.time_bold)


        self.time_label.setFont(font_main)
        self.time_label.setStyleSheet(
            f"color:{self.settings.time_color};"
            f"opacity:{self.settings.time_opacity};"
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

        # --- Spacer güncelle ---
        if self.settings.time_visible:
            bt_space = self.settings.spacing_battery_time
            td_space = self.settings.spacing_time_date
        else:
            # Saat yok → pil ile tarih birbirine yakın olsun
            bt_space = 2
            td_space = 2

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

       

        self.layout().invalidate()
        self.setWindowOpacity(self.settings.şeffaflık)




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
        
    def update_time(self):
        now = datetime.now()
        self.time_label.setText(now.strftime("%H:%M:%S"))
    


        self.date_label.setText(now.strftime(self.settings.date_format))

    def update_battery(self):
        if not psutil or not self.settings.battery_visible:
            return
        b = psutil.sensors_battery()
        if not b:
            return
        icon = " 🔌" if b.power_plugged else ""
        self.battery_label.setText(f"Pil: {int(b.percent)}%{icon}")

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

        self.tabs = QtWidgets.QTabWidget()

        self.tabs.addTab(self._general_tab(), "Genel")
        
      
        self.battery_tab = self._battery_tab()
        self.time_tab = self._time_tab()
        self.date_tab = self._date_tab()


        self.tabs.addTab(self.battery_tab, "Pil")
        self.tabs.addTab(self.time_tab, "Saat")
        self.tabs.addTab(self.date_tab, "Tarih")


      
        self.tabs.addTab(self._layout_tab(), "Yerleşim")

        
        btn_apply = QtWidgets.QPushButton("Uygula")
        btn_save = QtWidgets.QPushButton("Kaydet")
        btn_cancel = QtWidgets.QPushButton("İptal")

        btn_apply.clicked.connect(self.apply_now)
        btn_save.clicked.connect(self.save_and_close)
        btn_cancel.clicked.connect(self.reject)



        btns = QtWidgets.QHBoxLayout()
        btns.addStretch()
        btns.addWidget(btn_cancel)
        btns.addWidget(btn_apply)
        btns.addWidget(btn_save)


        main = QtWidgets.QVBoxLayout(self)
        main.addWidget(self.tabs)
        main.addLayout(btns)

    def apply_now(self):
        s = self.get_settings()
        self.parent().settings = s
        self.parent().apply_settings()

    def save_and_close(self):
        self.apply_now()
        save_settings(self.settings)
        self.accept()


    # ================= GENEL =================

    def _general_tab(self):
        w = QtWidgets.QWidget()
        f = QtWidgets.QFormLayout(w)

        self.chk_top = QtWidgets.QCheckBox("Her zaman üstte")
        self.chk_top.setChecked(self.settings.her_zaman_üstte)

        self.chk_autostart = QtWidgets.QCheckBox("Açılışta çalıştır")
        self.chk_autostart.setChecked(self.settings.açılışta_çalıştır)

        self.sld_opacity = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.sld_opacity.setRange(10, 100)
        self.sld_opacity.setValue(int(self.settings.şeffaflık * 100))

        f.addRow(self.chk_top)
        f.addRow(self.chk_autostart)
        f.addRow("Şeffaflık (%)", self.sld_opacity)
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

        self.btn_time_color = QtWidgets.QPushButton(self.settings.time_color)
        self.btn_time_color.clicked.connect(
            lambda: self._pick_color(self.btn_time_color)
        )

        f.addRow(self.chk_time_visible)
        f.addRow("Font", self.cmb_time_font)
        f.addRow("Boyut", self.spn_time_size)
        f.addRow("Renk", self.btn_time_color)
        f.addRow(self.chk_time_bold)
        return w

    def _apply_time_preview(self, font=None, size=None, bold=None, visible=None):
        if font is not None:
            self.settings.time_font_family = font
        if size is not None:
            self.settings.time_font_size = size
        if bold is not None:
            self.settings.time_bold = bold
        if visible is not None:
            self.settings.time_visible = visible

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
        self.spn_batt_interval.setRange(1, 120)
        self.spn_batt_interval.setValue(self.settings.battery_alert_interval)
        self.spn_batt_interval.valueChanged.connect(self._apply_batt_preview)

        # --- Renk ---
        self.btn_batt_color = QtWidgets.QPushButton(self.settings.battery_color)
        self.btn_batt_color.clicked.connect(
            lambda: self._pick_color(self.btn_batt_color)
        )

        # --- Layout ---
        f.addRow(self.chk_batt_visible)
        f.addRow("Uyarı seviyesi (%)", self.spn_batt_warn)
        f.addRow("Uyarı aralığı (dk)", self.spn_batt_interval)
        f.addRow("Renk", self.btn_batt_color)
        f.addRow("Font", self.cmb_batt_font)
        f.addRow("Font boyutu", self.spn_batt_size)
        f.addRow(self.chk_batt_bold)

        return w


    def _apply_batt_preview(self):
        self.settings.battery_visible = self.chk_batt_visible.isChecked()
        self.settings.battery_font_family = self.cmb_batt_font.currentFont().family()
        self.settings.battery_font_size = self.spn_batt_size.value()
        self.settings.battery_bold = self.chk_batt_bold.isChecked()
        self.settings.battery_warning_level = self.spn_batt_warn.value()
        self.settings.battery_alert_interval = self.spn_batt_interval.value()

        self.parent().apply_settings()



    # ================= YERLEŞİM ================= **************
    def _layout_tab(self):
        w = QtWidgets.QWidget()
        f = QtWidgets.QFormLayout(w)

        # --- Genel kenar boşluğu ---
        self.spn_margins = QtWidgets.QSpinBox()
        self.spn_margins.setRange(0, 100)
        self.spn_margins.setValue(self.settings.margins)

        # --- Pil ↔ Saat boşluğu ---
        self.spn_space_bt = QtWidgets.QSpinBox()
        self.spn_space_bt.setRange(-50, 200)
        self.spn_space_bt.setValue(self.settings.spacing_battery_time)

        # --- Saat ↔ Tarih boşluğu ---
        self.spn_space_td = QtWidgets.QSpinBox()
        self.spn_space_td.setRange(-50, 200)
        self.spn_space_td.setValue(self.settings.spacing_time_date)

        f.addRow("Kenar boşluğu (margin)", self.spn_margins)
        f.addRow("Pil ↔ Saat boşluğu", self.spn_space_bt)
        f.addRow("Saat ↔ Tarih boşluğu", self.spn_space_td)

        return w



    # ================= ORTAK =================

    def _pick_color(self, btn):
        c = QtWidgets.QColorDialog.getColor()
        if c.isValid():
            btn.setText(c.name())

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

        s.margins = self.spn_margins.value()

        s.spacing_battery_time = self.spn_space_bt.value()
        s.spacing_time_date = self.spn_space_td.value()


        return s






# =======================
# MAIN
# =======================

def main():
    app = QtWidgets.QApplication(sys.argv)
    locale.setlocale(locale.LC_TIME, "tr_TR")

    settings = load_settings()
    win = DraggableTransparentWindow(settings)
    win.show()

    move_window_safely(win, settings)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
