try:
    from PySide6 import QtCore
except ImportError:
    from PyQt6 import QtCore

from bildirim_servisi import BildirimServisi
from pil_servisi import PilServisi
from hatirlatici_servisi import HatirlaticiServisi
from gorev_servisi import GorevServisi


class WindowRuntimeMixin:
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
