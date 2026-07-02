import locale
import sys
import time
from datetime import datetime, timedelta

try:
    from PySide6 import QtCore, QtGui, QtWidgets
except ImportError:
    from PyQt6 import QtCore, QtGui, QtWidgets

from utils import resource_path, ICON_FILE, log_altyapisini_kur, log_kaydet, _enforce_topmost
from core_settings import PanelSettings, save_settings
from ui_settings import SettingsDialog
from hatirlatici_servisi import HatirlaticiServisi
from hatirlatici_modeli import HatirlaticiDurumu
from hatirlatici_popup import HatirlaticiBildirimPenceresi
from hatirlatici_listesi import HatirlaticiListesiDialog
from gorev_servisi import GorevServisi
from gorev_arayuzu import GorevArayuzuDialog
from pencere_araclari import aktif_popup_veya_modal_var, pencereyi_guvenli_tas, en_ustte_tut
from pil_servisi import PilServisi
from bildirim_servisi import BildirimServisi

# =======================
# ANA PENCERE
# =======================

from pencere_guncelleme import PencereGuncellemeKarishimi
from pencere_navigasyon import PencereNavigasyonKarishimi
from window_mouse_mixin import WindowMouseMixin
from window_lifecycle_mixin import WindowLifecycleMixin
from window_settings_mixin import WindowSettingsMixin
from serbest_duzen import SerbestDuzenKarishimi

def move_window_safely(window, settings):
    """DeskPilot.py tarafından kullanılan güvenli taşıma sarmalayıcısı."""
    return pencereyi_guvenli_tas(window, settings)

class DraggableTransparentWindow(WindowLifecycleMixin, WindowMouseMixin, WindowSettingsMixin, QtWidgets.QWidget, PencereGuncellemeKarishimi, PencereNavigasyonKarishimi, SerbestDuzenKarishimi):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.drag_pos = None
        self._full_charge_blink_on = False
        self._last_low_batt_alert_ts = 0
        self._low_batt_blink_on = False
        self._last_full_batt_alert_ts = 0
        self.free_time_window = None
        self.free_date_window = None
        self.free_battery_window = None
        self._free_layout_active = False
        self._keep_top_timer = None

        # Log altyapısını başlat (Task 1.2)
        log_altyapisini_kur()
        log_kaydet("Uygulama baslatildi.")


        flags = QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.Window
        if settings.her_zaman_ustte:
            flags |= QtCore.Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowOpacity(settings.seffaflik)
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








        self._zamanlayicilari_kur()
        self._servisleri_baslat()
        self._setup_keep_on_top()
        self.apply_settings()
        self.update_time()
        self.update_battery()

    def _zamanlayicilari_kur(self):
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

        self.hatirlatici_timer = QtCore.QTimer(self)
        self.hatirlatici_timer.timeout.connect(self.hatirlaticilari_kontrol_et)
        self.hatirlatici_timer.start(30000)

        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_menu)

    def _servisleri_baslat(self):
        self.pil_servisi = PilServisi(dusuk_esik=self.settings.battery_warning_level)
        self.bildirim_servisi = BildirimServisi()
        self.hatirlatici_servisi = HatirlaticiServisi()
        self.gorev_servisi = GorevServisi()
        self._aktif_popuplar = {}

    # ---------- AYARLAR ---------- *****************









    def show_menu(self, pos):
        self.show_menu_at(self.mapToGlobal(pos))


    def _setup_keep_on_top(self):
        if not self._keep_top_timer:
            self._keep_top_timer = QtCore.QTimer(self)
            self._keep_top_timer.setInterval(500)  # Ana pencere için daha seyrek kontrol
            self._keep_top_timer.timeout.connect(self._keep_on_top_tick)
        self._update_keep_on_top()

    def _update_keep_on_top(self):
        should_keep = self.isVisible() and self.settings.her_zaman_ustte
        if should_keep:
            if not self._keep_top_timer.isActive():
                self._keep_top_timer.start()
            if aktif_popup_veya_modal_var():
                return
            _enforce_topmost(self)
            self.raise_()
        else:
            if self._keep_top_timer.isActive():
                self._keep_top_timer.stop()

    def _keep_on_top_tick(self):
        if not self.isVisible() or not self.settings.her_zaman_ustte:
            if self._keep_top_timer.isActive():
                self._keep_top_timer.stop()
            return
        if aktif_popup_veya_modal_var():
            return
        _enforce_topmost(self)
        self.raise_()
