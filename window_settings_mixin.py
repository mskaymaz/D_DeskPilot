try:
    from PySide6 import QtCore, QtGui, QtWidgets
except ImportError:
    from PyQt6 import QtCore, QtGui, QtWidgets

from core_settings import BATTERY_BASE_FONT_SIZE, DATE_BASE_FONT_SIZE, TIME_BASE_FONT_SIZE, normalize_module_order


class WindowSettingsMixin:
    def apply_settings(self):
        self._apply_window_flags()
        if hasattr(self, "_saat_timer_araligini_guncelle"):
            self._saat_timer_araligini_guncelle()
        scale = self.settings.global_scale

        # --- Saat ---
        self._apply_time_style(
            self.time_main_label,
            self.time_seconds_label,
            self.time_ampm_label
        )
        self.time_label.setVisible(self.settings.time_visible)
        if self.free_time_window:
            self._apply_time_style(
                self.free_time_window.saat_etiketi,
                self.free_time_window.saniye_etiketi,
                self.free_time_window.ampm_etiketi
            )
            self.free_time_window.etiket.adjustSize()
            self.free_time_window.adjustSize()
            self.free_time_window.setVisible(
                self.settings.free_layout_enabled and self.settings.time_visible
            )

        # --- Tarih ---
        self._apply_date_style(self.date_label)
        self._apply_hicri_date_style(self.hicri_date_label)
        self._apply_date_week_style(
            self.date_week_separator_label,
            self.date_week_number_label,
            self.date_week_text_label
        )
        self.date_container.setVisible(self.settings.date_visible)
        if self.free_date_window:
            self._apply_date_style(self.free_date_window.etiket)
            self._apply_hicri_date_style(self.free_date_window.hicri_etiketi)
            if hasattr(self.free_date_window, "hafta_sayi_etiketi"):
                self._apply_date_week_style(
                    self.free_date_window.hafta_ayrac_etiketi,
                    self.free_date_window.hafta_sayi_etiketi,
                    self.free_date_window.hafta_yazi_etiketi
                )
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

        self._rebuild_module_layout(scale)
        if hasattr(self, "quick_actions"):
            self.quick_actions._apply_size()
        if hasattr(self, "tepsi_ikonu"):
            self.tepsi_ikonu._menu_kur()

        self.main_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        self.layout().invalidate()
        self.main_layout.activate()
        self._rebuild_module_layout(scale)
        self.main_layout.activate()
        self.adjustSize()
        self._rebuild_module_layout(scale)
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

    def _module_gap(self, first, second, scale):
        pair = {first, second}
        if pair == {"battery", "time"}:
            value = (
                self.settings.spacing_battery_time
                + getattr(self.settings, "spacing_battery_time_offset", 0)
            )
        elif pair == {"time", "date"}:
            value = (
                self.settings.spacing_time_date
                + getattr(self.settings, "spacing_time_date_offset", 0)
            )
        else:
            value = (
                self.settings.spacing_battery_date_hidden
                + getattr(self.settings, "spacing_battery_date_hidden_offset", 0)
            )
        if pair == {"battery", "time"}:
            return 3
        min_gap = 8
        return max(min_gap, int(value * scale))

    def _rebuild_module_layout(self, scale):
        modules = {
            "battery": (self.battery_row, self.settings.battery_visible),
            "time": (self.time_label, self.settings.time_visible),
            "date": (self.date_container, self.settings.date_visible),
        }
        visible = [
            (key, modules[key][0])
            for key in normalize_module_order(getattr(self.settings, "module_order", []))
            if modules[key][1]
        ]

        stored = getattr(self.settings, "group_layout", {})
        valid = isinstance(stored, dict) and all(
            isinstance(stored.get(key), dict)
            and isinstance(stored[key].get("x"), int)
            and isinstance(stored[key].get("y"), int)
            for key, _ in visible
        )
        if not valid:
            stored = {}
            previous = None
            y = 0
            for key, widget in visible:
                widget.adjustSize()
                if previous is not None:
                    y += self._module_gap(previous, key, scale)
                stored[key] = {"x": 0, "y": y}
                y += widget.height()
                previous = key
            self.settings.group_layout = stored

        for key, (widget, is_visible) in modules.items():
            widget.setParent(self.group_canvas)
            widget.setVisible(is_visible)
            if is_visible and key in stored:
                widget.adjustSize()
                widget.move(stored[key]["x"], stored[key]["y"])

        right = 1
        bottom = 1
        for key, widget in visible:
            position = stored[key]
            right = max(right, position["x"] + widget.width())
            bottom = max(bottom, position["y"] + widget.height())
        self.group_canvas.setFixedSize(right, bottom)
        self.group_canvas.adjustSize()

    def _lock_label_height(self, label, _size):
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

    def _apply_time_style(self, label, seconds_label=None, ampm_label=None):
        scale = self.settings.global_scale * self.settings.time_scale
        size = int(TIME_BASE_FONT_SIZE * scale)
        font_main = QtGui.QFont(
            self.settings.time_font_family,
            size
        )
        font_main.setBold(self.settings.time_bold)
        label.setFont(font_main)
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignBottom)
        label.setStyleSheet(
            f"""
            QLabel {{
                color: {self.settings.time_color};
                line-height: {size}px;
                padding: 0px;
                margin: 0px;
            }}
            """
        )
        self._lock_label_height(label, size)
        main_height = label.height()
        if seconds_label is not None:
            sec_size = max(1, int(size * self.settings.time_seconds_scale))
            sec_font = QtGui.QFont(self.settings.time_font_family, sec_size)
            sec_font.setBold(self.settings.time_seconds_bold)
            seconds_label.setFont(sec_font)
            seconds_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignBottom)
            seconds_label.setStyleSheet(f"color:{self.settings.time_color};")
            seconds_label.setFixedHeight(main_height)
        if ampm_label is not None:
            ampm_size = max(1, int(size * self.settings.time_seconds_scale) // 2)
            ampm_font = QtGui.QFont(self.settings.time_font_family, ampm_size)
            ampm_label.setFont(ampm_font)
            ampm_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignBottom)
            ampm_label.setStyleSheet(f"color:{self.settings.time_color};")
            ampm_label.setFixedHeight(main_height)

    def _apply_date_style(self, label):
        scale = self.settings.global_scale * self.settings.date_scale
        size = int(DATE_BASE_FONT_SIZE * scale)
        df = QtGui.QFont(
            self.settings.date_font_family,
            size
        )
        df.setBold(self.settings.date_bold)
        label.setFont(df)
        label.setStyleSheet(
            f"color:{self.settings.date_color};"
            f"opacity:{self.settings.date_opacity};"
        )
        self._lock_label_height(label, size)

    def _apply_date_week_style(self, separator_label, number_label, text_label):
        scale = self.settings.global_scale * self.settings.date_scale
        number_size = max(1, int(DATE_BASE_FONT_SIZE * scale * 0.80))
        separator_size = max(1, int(number_size * 0.35))
        text_size = max(1, int(DATE_BASE_FONT_SIZE * scale * 0.50))
        separator_font = QtGui.QFont(self.settings.date_font_family, separator_size)
        number_font = QtGui.QFont(self.settings.date_font_family, number_size)
        number_font.setBold(self.settings.date_bold)
        text_font = QtGui.QFont(self.settings.date_font_family, text_size)
        text_font.setWeight(QtGui.QFont.Weight.Normal)
        text_font.setBold(False)
        text_font.setStretch(90)
        for label, font, size in (
            (separator_label, separator_font, separator_size),
            (number_label, number_font, number_size),
            (text_label, text_font, text_size),
        ):
            label.setFont(font)
            extra_style = ""
            if label is text_label:
                extra_style = "padding-bottom:6px;"
            elif label is separator_label:
                extra_style = "padding-left:8px;padding-right:8px;"
            label.setStyleSheet(
                f"color:{self.settings.date_color};"
                f"opacity:{self.settings.date_opacity};"
                f"{extra_style}"
            )
            self._lock_label_height(label, size)
            label.setVisible(self.settings.date_visible and getattr(self.settings, "date_show_week_number", False))

    def _apply_hicri_date_style(self, label):
        scale = self.settings.global_scale * self.settings.date_scale
        size = max(1, int(DATE_BASE_FONT_SIZE * scale * 0.55))
        font = QtGui.QFont(self.settings.date_font_family, size)
        label.setFont(font)
        label.setStyleSheet(
            f"color:{self.settings.date_color};"
            f"opacity:{self.settings.date_opacity};"
        )
        self._lock_label_height(label, size)
        label.setVisible(self.settings.date_visible)

    def _apply_battery_style(self, label, icon_label):
        scale = self.settings.global_scale * self.settings.battery_scale
        size = int(BATTERY_BASE_FONT_SIZE * scale)
        bf = QtGui.QFont(
            self.settings.battery_font_family,
            size
        )
        bf.setBold(self.settings.battery_bold)
        label.setFont(bf)
        label.setStyleSheet(
            f"color:{self.settings.battery_color};"
            f"opacity:{self.settings.battery_opacity};"
        )
        self._lock_label_height(label, size)

        icon_size = max(1.0, float(size) * 0.8)
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
