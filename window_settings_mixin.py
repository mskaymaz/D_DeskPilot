try:
    from PySide6 import QtCore, QtGui, QtWidgets
except ImportError:
    from PyQt6 import QtCore, QtGui, QtWidgets


class WindowSettingsMixin:
    def apply_settings(self):
        self._apply_window_flags()
        scale = self.settings.global_scale

        # --- Saat ---
        self._apply_time_style(self.time_label)
        self.time_label.setVisible(self.settings.time_visible)
        if self.free_time_window:
            self._apply_time_style(self.free_time_window.etiket)
            self.free_time_window.etiket.adjustSize()
            self.free_time_window.adjustSize()
            self.free_time_window.setVisible(
                self.settings.free_layout_enabled and self.settings.time_visible
            )

        # --- Tarih ---
        self._apply_date_style(self.date_label)
        self.date_label.setVisible(self.settings.date_visible)
        if self.free_date_window:
            self._apply_date_style(self.free_date_window.etiket)
            self.free_date_window.etiket.adjustSize()
            self.free_date_window.adjustSize()
            self.free_date_window.setVisible(
                self.settings.free_layout_enabled and self.settings.date_visible
            )

        # --- Pil ---
        self._apply_battery_style(self.battery_label, self.battery_icon_label)
        self.battery_label.setVisible(self.settings.battery_visible)
        self.battery_icon_label.setVisible(self.settings.battery_visible)
        if self.free_battery_window:
            self._apply_battery_style(
                self.free_battery_window.pil_etiketi,
                self.free_battery_window.pil_ikon_etiketi
            )
            self.free_battery_window.setVisible(
                self.settings.free_layout_enabled and self.settings.battery_visible
            )
            self.free_battery_window.pil_ikon_etiketi.setVisible(self.settings.battery_visible)

        self._set_battery_color(self.settings.battery_color)
        self._refresh_battery_rows()

        # --- Spacer guncelle ---
        if self.settings.time_visible:
            bt_space = int(self.settings.spacing_battery_time * scale)
            td_space = int(self.settings.spacing_time_date * scale)
        else:
            # Saat yok -> pil ile tarih birbirine yakin olsun
            bt_space = 0
            td_space = int(self.settings.spacing_battery_date_hidden * scale)

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
        self.setWindowOpacity(self.settings.seffaflik)

        if self.free_time_window:
            self.free_time_window.setWindowOpacity(self.settings.seffaflik)
        if self.free_date_window:
            self.free_date_window.setWindowOpacity(self.settings.seffaflik)
        if self.free_battery_window:
            self.free_battery_window.setWindowOpacity(self.settings.seffaflik)

        self._apply_free_layout_mode()

    def _lock_label_height(self, label, font_size):
        fm = QtGui.QFontMetrics(label.font())
        h = fm.ascent() + fm.descent()
        label.setFixedHeight(h)

    def _apply_window_flags(self):
        flags = QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.Window
        if self.settings.her_zaman_ustte:
            flags |= QtCore.Qt.WindowType.WindowStaysOnTopHint
        was_visible = self.isVisible()
        self.setWindowFlags(flags)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        if was_visible:
            self.show()
        if self.free_time_window:
            self.free_time_window.bayrak_ve_saydamlik_yenile()
        if self.free_date_window:
            self.free_date_window.bayrak_ve_saydamlik_yenile()
        if self.free_battery_window:
            self.free_battery_window.bayrak_ve_saydamlik_yenile()

    def _apply_time_style(self, label):
        scale = self.settings.global_scale * self.settings.time_scale
        font_main = QtGui.QFont(
            self.settings.time_font_family,
            int(self.settings.time_font_size * scale)
        )
        font_main.setBold(self.settings.time_bold)
        label.setFont(font_main)
        label.setStyleSheet(
            f"""
            QLabel {{
                color: {self.settings.time_color};
                line-height: {int(self.settings.time_font_size * scale)}px;
                padding: 0px;
                margin: 0px;
            }}
            """
        )
        self._lock_label_height(label, int(self.settings.time_font_size * scale))

    def _apply_date_style(self, label):
        scale = self.settings.global_scale * self.settings.date_scale
        df = QtGui.QFont(
            self.settings.date_font_family,
            int(self.settings.date_font_size * scale)
        )
        df.setBold(self.settings.date_bold)
        label.setFont(df)
        label.setStyleSheet(
            f"color:{self.settings.date_color};"
            f"opacity:{self.settings.date_opacity};"
        )
        self._lock_label_height(label, int(self.settings.date_font_size * scale))

    def _apply_battery_style(self, label, icon_label):
        scale = self.settings.global_scale * self.settings.battery_scale
        bf = QtGui.QFont(
            self.settings.battery_font_family,
            int(self.settings.battery_font_size * scale)
        )
        bf.setBold(self.settings.battery_bold)
        label.setFont(bf)
        label.setStyleSheet(
            f"color:{self.settings.battery_color};"
            f"opacity:{self.settings.battery_opacity};"
        )
        self._lock_label_height(label, int(self.settings.battery_font_size * scale))

        icon_size = max(1.0, float(self.settings.battery_font_size * scale) * 0.8)
        # Use a symbol font to avoid emoji-size overrides
        bif = QtGui.QFont("Segoe UI Symbol")
        bif.setPointSizeF(icon_size)
        bif.setBold(False)
        icon_label.setFont(bif)
        icon_label.setStyleSheet(
            f"color:{self.settings.battery_color};"
            f"opacity:{self.settings.battery_opacity};"
            f"font-size:{icon_size}px;"
            "font-family:'Segoe UI Symbol';"
        )
        self._lock_label_height(icon_label, int(icon_size))

    def _refresh_battery_rows(self):
        self.battery_row_layout.invalidate()
        self.battery_row.adjustSize()
        self.battery_row.updateGeometry()
        if self.free_battery_window:
            self.free_battery_window.icerik.adjustSize()
            self.free_battery_window.adjustSize()
            self.free_battery_window.updateGeometry()
