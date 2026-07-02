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
from window_init_mixin import WindowInitMixin
from serbest_duzen import SerbestDuzenKarishimi

def move_window_safely(window, settings):
    """DeskPilot.py tarafından kullanılan güvenli taşıma sarmalayıcısı."""
    return pencereyi_guvenli_tas(window, settings)

class DraggableTransparentWindow(WindowLifecycleMixin, WindowMouseMixin, WindowSettingsMixin, WindowInitMixin, QtWidgets.QWidget, PencereGuncellemeKarishimi, PencereNavigasyonKarishimi, SerbestDuzenKarishimi):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self._init_state()
        self._init_logging()
        self._init_window()
        self._init_widgets()
        self._init_startup()






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
