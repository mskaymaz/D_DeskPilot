try:
    from PySide6 import QtCore
except ImportError:
    from PyQt6 import QtCore
from log_servisi import log_kaydet

class WindowRuntimeMixin:
    def _zamanlayicilari_kur(self):
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(self._saat_timer_araligi())

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

        self.alarm_timer = QtCore.QTimer(self)
        self.alarm_timer.timeout.connect(self.alarmlari_kontrol_et)
        self.alarm_timer.start(10000)

        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_menu)

    def _saat_timer_araligi(self):
        return 1000 if getattr(self.settings, "time_seconds_visible", True) else 60000

    def _saat_timer_araligini_guncelle(self):
        if hasattr(self, "timer") and self.timer.interval() != self._saat_timer_araligi():
            self.timer.setInterval(self._saat_timer_araligi())

    def _servisleri_baslat(self):
        self.pil_servisi = None
        self.bildirim_servisi = None
        self.hatirlatici_servisi = None
        self.gorev_servisi = None
        self.alarm_servisi = None
        self._aktif_popuplar = {}
        self._aktif_alarm_popuplar = {}
        QtCore.QTimer.singleShot(100, self._agir_servisleri_baslat)

    def _agir_servisleri_baslat(self):
        from bildirim_servisi import BildirimServisi
        from pil_servisi import PilServisi
        from hatirlatici_servisi import HatirlaticiServisi
        from gorev_servisi import GorevServisi
        from alarm_servisi import AlarmServisi

        baslatmalar = (
            ("pil_servisi", lambda: PilServisi(dusuk_esik=self.settings.battery_warning_level)),
            ("bildirim_servisi", lambda: BildirimServisi(
                varsayilan_soguma_suresi=self.settings.bildirim_soguma_suresi
            )),
            ("hatirlatici_servisi", HatirlaticiServisi),
            ("gorev_servisi", GorevServisi),
            ("alarm_servisi", AlarmServisi),
        )
        for ad, olustur in baslatmalar:
            try:
                setattr(self, ad, olustur())
            except Exception as e:
                log_kaydet(f"{ad} baslatilamadi: {e}", "error")
        self.update_battery()
        QtCore.QTimer.singleShot(500, self._baslangic_kacirilan_alarmlari_goster)
        QtCore.QTimer.singleShot(600, self._baslangic_kacirilan_hatirlaticilari_goster)
