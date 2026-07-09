try:
    from PySide6 import QtCore, QtGui, QtWidgets
except ImportError:
    from PyQt6 import QtCore, QtGui, QtWidgets

from core_settings import DEFAULT_MODULE_ORDER, save_settings
from log_servisi import log_kaydet
from pencere_araclari import ekrani_bul
from serbest_pencere import SerbestSatirPenceresi


class SerbestDuzenKarishimi:
    """Serbest dağıt modundaki üç parçalı pencere yönetimi."""

    def _ensure_free_windows(self):
        created = False
        if not self.free_time_window:
            self.free_time_window = SerbestSatirPenceresi("time", self.settings, self)
            created = True
        if not self.free_date_window:
            self.free_date_window = SerbestSatirPenceresi("date", self.settings, self)
            created = True
        if not self.free_battery_window:
            self.free_battery_window = SerbestSatirPenceresi("battery", self.settings, self)
            created = True
        if created:
            self._apply_free_window_styles()

    def _apply_free_window_styles(self):
        if self.free_time_window:
            self._apply_time_style(
                self.free_time_window.saat_etiketi,
                self.free_time_window.saniye_etiketi,
                self.free_time_window.ampm_etiketi
            )
            self.free_time_window.etiket.adjustSize()
            self.free_time_window.adjustSize()

        if self.free_date_window:
            self._apply_date_style(self.free_date_window.etiket)
            if hasattr(self.free_date_window, "hafta_sayi_etiketi"):
                self._apply_date_week_style(
                    self.free_date_window.hafta_ayrac_etiketi,
                    self.free_date_window.hafta_sayi_etiketi,
                    self.free_date_window.hafta_yazi_etiketi
                )
            self.free_date_window.etiket.adjustSize()
            self.free_date_window.adjustSize()

        if self.free_battery_window:
            self._apply_battery_style(
                self.free_battery_window.pil_etiketi,
                self.free_battery_window.pil_ikon_etiketi,
            )
            self._set_battery_color(self.settings.battery_color)
            self._refresh_battery_rows()

    def _clamp_window_position(self, window, x, y, allow_taskbar=False, hedef_ekran_adi=""):
        app = QtWidgets.QApplication.instance()
        screen = ekrani_bul(hedef_ekran_adi)
        if not hedef_ekran_adi:
            screen = app.screenAt(QtCore.QPoint(x, y)) or screen

        rect = screen.geometry() if allow_taskbar else screen.availableGeometry()
        window.adjustSize()
        w, h = window.width(), window.height()

        x = max(rect.left(), min(x, rect.right() - w))
        y = max(rect.top(), min(y, rect.bottom() - h))
        return x, y

    def _move_line_window_safely(self, window, x, y, hedef_ekran_adi=""):
        x, y = self._clamp_window_position(
            window, x, y, allow_taskbar=False, hedef_ekran_adi=hedef_ekran_adi
        )
        window.move(x, y)

    def _capture_free_positions_from_grouped(self):
        time_global = self.mapToGlobal(self.time_label.pos())
        date_global = self.mapToGlobal(self.date_row.pos())
        battery_global = self.mapToGlobal(self.battery_row.pos())

        self.settings.free_time_x = time_global.x()
        self.settings.free_time_y = time_global.y()
        self.settings.free_date_x = date_global.x()
        self.settings.free_date_y = date_global.y()
        self.settings.free_battery_x = battery_global.x()
        self.settings.free_battery_y = battery_global.y()

        ekran = QtGui.QGuiApplication.screenAt(self.pos())
        if ekran:
            ekran_adi = ekran.name()
            self.settings.serbest_saat_ekran_adi = ekran_adi
            self.settings.serbest_tarih_ekran_adi = ekran_adi
            self.settings.serbest_pil_ekran_adi = ekran_adi

        self.settings.free_layout_has_positions = True
        save_settings(self.settings)

    def _capture_current_free_positions(self):
        hedefler = (
            (self.free_time_window, "free_time_x", "free_time_y", "serbest_saat_ekran_adi"),
            (self.free_date_window, "free_date_x", "free_date_y", "serbest_tarih_ekran_adi"),
            (self.free_battery_window, "free_battery_x", "free_battery_y", "serbest_pil_ekran_adi"),
        )
        guncellendi = False
        for pencere, x_alan, y_alan, ekran_alan in hedefler:
            if not pencere:
                continue
            setattr(self.settings, x_alan, pencere.x())
            setattr(self.settings, y_alan, pencere.y())
            ekran = QtGui.QGuiApplication.screenAt(pencere.pos())
            if ekran:
                setattr(self.settings, ekran_alan, ekran.name())
            guncellendi = True
        if guncellendi:
            self.settings.free_layout_has_positions = True

    def _show_free_windows(self):
        self._ensure_free_windows()
        pencereler = (
            (self.free_time_window, self.settings.free_time_x, self.settings.free_time_y,
             self.settings.serbest_saat_ekran_adi, self.settings.time_visible),
            (self.free_date_window, self.settings.free_date_x, self.settings.free_date_y,
             self.settings.serbest_tarih_ekran_adi, self.settings.date_visible),
            (self.free_battery_window, self.settings.free_battery_x, self.settings.free_battery_y,
             self.settings.serbest_pil_ekran_adi, self.settings.battery_visible),
        )

        for pencere, x, y, ekran_adi, gorunur in pencereler:
            self._move_line_window_safely(pencere, x, y, ekran_adi)
            if gorunur:
                pencere.show()
            else:
                pencere.hide()

    def _hide_free_windows(self):
        for pencere in (self.free_time_window, self.free_date_window, self.free_battery_window):
            if pencere:
                pencere.hide()

    def _move_grouped_to_time_position(self):
        if not self.settings.free_layout_has_positions:
            return

        target_x = self.settings.free_time_x - self.time_label.pos().x()
        target_y = self.settings.free_time_y - self.time_label.pos().y()
        target_x, target_y = self._clamp_window_position(
            self,
            target_x,
            target_y,
            allow_taskbar=False,
            hedef_ekran_adi=self.settings.serbest_saat_ekran_adi,
        )
        self.move(target_x, target_y)
        self.settings.pos_x = target_x
        self.settings.pos_y = target_y
        self.settings.grup_ekran_adi = self.settings.serbest_saat_ekran_adi
        save_settings(self.settings)

    def tum_modulleri_topla(self):
        app = QtWidgets.QApplication.instance()
        ekran = app.screenAt(QtGui.QCursor.pos()) or app.primaryScreen()
        alan = ekran.availableGeometry()
        log_kaydet(f"Tüm modüller '{ekran.name()}' ekranına toplanıyor.")
        self.settings.module_order = list(DEFAULT_MODULE_ORDER)

        if self.settings.free_layout_enabled:
            self._capture_current_free_positions()
        self.settings.free_layout_enabled = False
        self._free_layout_active = False
        self._hide_free_windows()
        self.apply_settings()
        self.show()
        self.adjustSize()
        x = alan.left() + (alan.width() - self.width()) // 2
        y = alan.top() + (alan.height() - self.height()) // 2
        self.move(x, y)
        self.settings.pos_x = x
        self.settings.pos_y = y
        self.settings.grup_ekran_adi = ekran.name()

        save_settings(self.settings)

    def _apply_free_layout_mode(self):
        if self.settings.free_layout_enabled:
            if not self._free_layout_active:
                self._ensure_free_windows()
                if not self.settings.free_layout_has_positions:
                    self._capture_free_positions_from_grouped()
                self._free_layout_active = True
            self._show_free_windows()
            self.hide()
            return

        if self._free_layout_active:
            self._free_layout_active = False
            self._hide_free_windows()
            self.show()
            self._move_grouped_to_time_position()
        else:
            self._hide_free_windows()

    def update_free_position(self, kind, x, y, ekran_adi=""):
        if self.settings.settings_locked:
            return

        hedefler = {
            "time": ("free_time_x", "free_time_y", "serbest_saat_ekran_adi"),
            "date": ("free_date_x", "free_date_y", "serbest_tarih_ekran_adi"),
            "battery": ("free_battery_x", "free_battery_y", "serbest_pil_ekran_adi"),
        }
        alanlar = hedefler.get(kind)
        if not alanlar:
            return

        setattr(self.settings, alanlar[0], x)
        setattr(self.settings, alanlar[1], y)
        setattr(self.settings, alanlar[2], ekran_adi)
        self.settings.free_layout_has_positions = True
        save_settings(self.settings)
