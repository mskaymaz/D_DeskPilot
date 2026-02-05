import locale
import sys
import time
from datetime import datetime

try:
    import psutil
except ImportError:
    psutil = None

try:
    if sys.platform == "win32":
        import winsound
    else:
        winsound = None
except Exception:
    winsound = None

try:
    from PySide6 import QtCore, QtGui, QtWidgets
except ImportError:
    from PyQt6 import QtCore, QtGui, QtWidgets

from utils import resource_path, ICON_FILE
from core_settings import PanelSettings, save_settings
from ui_settings import SettingsDialog

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
# SERBEST SATIR PENCERESI
# =======================

class FreeLineWindow(QtWidgets.QWidget):
    def __init__(self, kind, settings, controller):
        super().__init__(None)
        self.kind = kind
        self.settings = settings
        self.controller = controller
        self.drag_pos = None

        self._apply_window_flags()
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowOpacity(self.settings.seffaflik)
        self.setWindowIcon(QtGui.QIcon(resource_path(ICON_FILE)))

        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_menu)

        self._build_ui()

    def _apply_window_flags(self):
        flags = QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.Tool
        if self.settings.her_zaman_ustte:
            flags |= QtCore.Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(flags)

    def _build_ui(self):
        if self.kind == "battery":
            self.battery_label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
            self.battery_icon_label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
            self.battery_icon_label.setVisible(False)

            row = QtWidgets.QWidget()
            row_layout = QtWidgets.QHBoxLayout(row)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(4)
            row_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            row_layout.addWidget(self.battery_label)
            row_layout.addWidget(self.battery_icon_label)
            self.content = row
        else:
            self.label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
            self.content = self.label

        for lbl in self._labels():
            lbl.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
            lbl.setContentsMargins(0, 0, 0, 0)
            lbl.setStyleSheet(
                """
                QLabel {
                    padding: 0px;
                    margin: 0px;
                }
                """
            )

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.content)

    def _labels(self):
        if self.kind == "battery":
            return (self.battery_label, self.battery_icon_label)
        return (self.label,)

    def refresh_flags_and_opacity(self):
        was_visible = self.isVisible()
        self._apply_window_flags()
        self.setWindowOpacity(self.settings.seffaflik)
        if was_visible:
            self.show()

    def _show_menu(self, pos):
        global_pos = self.mapToGlobal(pos)
        anchor_pos = self.frameGeometry().topLeft()
        self.controller.show_menu_at(global_pos, anchor_pos)

    def mousePressEvent(self, e):
        if e.button() == QtCore.Qt.MouseButton.LeftButton:
            self.drag_pos = e.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        if self.drag_pos:
            self.move(e.globalPosition().toPoint() - self.drag_pos)

    def mouseReleaseEvent(self, e):
        if self.drag_pos:
            self.drag_pos = None
            self.controller.update_free_position(self.kind, self.x(), self.y())


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
        self.free_time_window = None
        self.free_date_window = None
        self.free_battery_window = None
        self._free_layout_active = False


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
        self._apply_window_flags()

        # --- Saat ---
        self._apply_time_style(self.time_label)
        self.time_label.setVisible(self.settings.time_visible)
        if self.free_time_window:
            self._apply_time_style(self.free_time_window.label)
            self.free_time_window.setVisible(
                self.settings.free_layout_enabled and self.settings.time_visible
            )

        # --- Tarih ---
        self._apply_date_style(self.date_label)
        self.date_label.setVisible(self.settings.date_visible)
        if self.free_date_window:
            self._apply_date_style(self.free_date_window.label)
            self.free_date_window.setVisible(
                self.settings.free_layout_enabled and self.settings.date_visible
            )

        # --- Pil ---
        self._apply_battery_style(self.battery_label, self.battery_icon_label)
        self.battery_label.setVisible(self.settings.battery_visible)
        if self.free_battery_window:
            self._apply_battery_style(
                self.free_battery_window.battery_label,
                self.free_battery_window.battery_icon_label
            )
            self.free_battery_window.setVisible(
                self.settings.free_layout_enabled and self.settings.battery_visible
            )

        self._set_battery_color(self.settings.battery_color)
        self._refresh_battery_rows()

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
            self.free_time_window.refresh_flags_and_opacity()
        if self.free_date_window:
            self.free_date_window.refresh_flags_and_opacity()
        if self.free_battery_window:
            self.free_battery_window.refresh_flags_and_opacity()

    def _apply_time_style(self, label):
        font_main = QtGui.QFont(
            self.settings.time_font_family,
            self.settings.time_font_size
        )
        font_main.setBold(self.settings.time_bold)
        label.setFont(font_main)
        label.setStyleSheet(
            f"""
            QLabel {{
                color: {self.settings.time_color};
                line-height: {self.settings.time_font_size}px;
                padding: 0px;
                margin: 0px;
            }}
            """
        )

    def _apply_date_style(self, label):
        df = QtGui.QFont(
            self.settings.date_font_family,
            self.settings.date_font_size
        )
        df.setBold(self.settings.date_bold)
        label.setFont(df)
        label.setStyleSheet(
            f"color:{self.settings.date_color};"
            f"opacity:{self.settings.date_opacity};"
        )
        self._lock_label_height(label, self.settings.date_font_size)

    def _apply_battery_style(self, label, icon_label):
        bf = QtGui.QFont(
            self.settings.battery_font_family,
            self.settings.battery_font_size
        )
        bf.setBold(self.settings.battery_bold)
        label.setFont(bf)
        label.setStyleSheet(
            f"color:{self.settings.battery_color};"
            f"opacity:{self.settings.battery_opacity};"
        )
        self._lock_label_height(label, self.settings.battery_font_size)

        icon_size = max(1.0, float(self.settings.battery_font_size) * 0.8)
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
            self.free_battery_window.content.adjustSize()
            self.free_battery_window.adjustSize()
            self.free_battery_window.updateGeometry()

    def _ensure_free_windows(self):
        created = False
        if not self.free_time_window:
            self.free_time_window = FreeLineWindow("time", self.settings, self)
            created = True
        if not self.free_date_window:
            self.free_date_window = FreeLineWindow("date", self.settings, self)
            created = True
        if not self.free_battery_window:
            self.free_battery_window = FreeLineWindow("battery", self.settings, self)
            created = True
        if created:
            self._apply_free_window_styles()

    def _apply_free_window_styles(self):
        if self.free_time_window:
            self._apply_time_style(self.free_time_window.label)
        if self.free_date_window:
            self._apply_date_style(self.free_date_window.label)
        if self.free_battery_window:
            self._apply_battery_style(
                self.free_battery_window.battery_label,
                self.free_battery_window.battery_icon_label
            )
            self._set_battery_color(self.settings.battery_color)
            self._refresh_battery_rows()

    def _clamp_window_position(self, window, x, y, allow_taskbar=False):
        app = QtWidgets.QApplication.instance()
        screen = app.screenAt(QtCore.QPoint(x, y)) or app.primaryScreen()
        rect = screen.geometry() if allow_taskbar else screen.availableGeometry()
        window.adjustSize()
        w, h = window.width(), window.height()

        if x < rect.left():
            x = rect.left()
        if y < rect.top():
            y = rect.top()
        if x + w > rect.right():
            x = rect.right() - w
        if y + h > rect.bottom():
            y = rect.bottom() - h

        return x, y

    def _move_line_window_safely(self, window, x, y):
        x, y = self._clamp_window_position(window, x, y, allow_taskbar=True)
        window.move(x, y)

    def _capture_free_positions_from_grouped(self):
        time_global = self.mapToGlobal(self.time_label.pos())
        date_global = self.mapToGlobal(self.date_label.pos())
        battery_global = self.mapToGlobal(self.battery_row.pos())

        self.settings.free_time_x = time_global.x()
        self.settings.free_time_y = time_global.y()
        self.settings.free_date_x = date_global.x()
        self.settings.free_date_y = date_global.y()
        self.settings.free_battery_x = battery_global.x()
        self.settings.free_battery_y = battery_global.y()
        self.settings.free_layout_has_positions = True
        save_settings(self.settings)

    def _show_free_windows(self):
        self._ensure_free_windows()

        self._move_line_window_safely(
            self.free_time_window,
            self.settings.free_time_x,
            self.settings.free_time_y
        )
        self._move_line_window_safely(
            self.free_date_window,
            self.settings.free_date_x,
            self.settings.free_date_y
        )
        self._move_line_window_safely(
            self.free_battery_window,
            self.settings.free_battery_x,
            self.settings.free_battery_y
        )

        if self.settings.time_visible:
            self.free_time_window.show()
        if self.settings.date_visible:
            self.free_date_window.show()
        if self.settings.battery_visible:
            self.free_battery_window.show()

    def _hide_free_windows(self):
        if self.free_time_window:
            self.free_time_window.hide()
        if self.free_date_window:
            self.free_date_window.hide()
        if self.free_battery_window:
            self.free_battery_window.hide()

    def _move_grouped_to_time_position(self):
        if not self.settings.free_layout_has_positions:
            return
        target_x = self.settings.free_time_x - self.time_label.pos().x()
        target_y = self.settings.free_time_y - self.time_label.pos().y()
        target_x, target_y = self._clamp_window_position(self, target_x, target_y)
        self.move(target_x, target_y)
        self.settings.pos_x = target_x
        self.settings.pos_y = target_y
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
        else:
            if self._free_layout_active:
                self._free_layout_active = False
                self._hide_free_windows()
                self.show()
                self._move_grouped_to_time_position()
            else:
                self._hide_free_windows()

    def update_free_position(self, kind, x, y):
        if kind == "time":
            self.settings.free_time_x = x
            self.settings.free_time_y = y
        elif kind == "date":
            self.settings.free_date_x = x
            self.settings.free_date_y = y
        elif kind == "battery":
            self.settings.free_battery_x = x
            self.settings.free_battery_y = y
        self.settings.free_layout_has_positions = True
        save_settings(self.settings)

    def show_menu_at(self, global_pos, settings_anchor_pos=None):
        menu = QtWidgets.QMenu(self)
        act_settings = menu.addAction("Ayarlar")
        act_exit = menu.addAction("Çıkış")
        action = menu.exec(global_pos)
        if action == act_settings:
            self.show_settings_at(settings_anchor_pos)
        elif action == act_exit:
            QtWidgets.QApplication.quit()

    def show_settings_at(self, anchor_pos=None):
        self.settings_window = SettingsDialog(self.settings, self)
        if anchor_pos is not None:
            self.position_settings_window_at(self.settings_window, anchor_pos)
        else:
            self.position_settings_window(self.settings_window)
        self.settings_window.show()
        self.settings_window.raise_()

    def position_settings_window_at(self, dialog, anchor_pos):
        app = QtWidgets.QApplication.instance()
        screen = app.screenAt(anchor_pos) or app.primaryScreen()
        rect = screen.availableGeometry()

        dialog.adjustSize()
        dw, dh = dialog.width(), dialog.height()

        x = anchor_pos.x()
        y = anchor_pos.y()

        if x + dw > rect.right():
            x = rect.right() - dw
        if y + dh > rect.bottom():
            y = rect.bottom() - dh
        if x < rect.left():
            x = rect.left()
        if y < rect.top():
            y = rect.top()

        dialog.move(x, y)


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
        self.show_menu_at(self.mapToGlobal(pos))





    # ---------- GÜNCELLEMELER ----------

    def update_time(self):
        now = datetime.now()
        time_text = self._format_time_html(now)
        date_text = self._format_date(now)
        self.time_label.setText(time_text)
        self.date_label.setText(date_text)
        if self.free_time_window:
            self.free_time_window.label.setText(time_text)
        if self.free_date_window:
            self.free_date_window.label.setText(date_text)

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
            if self.free_battery_window:
                self.free_battery_window.battery_icon_label.setText("\u26A1")
                self.free_battery_window.battery_icon_label.setVisible(True)
        else:
            self.battery_icon_label.setVisible(False)
            if self.free_battery_window:
                self.free_battery_window.battery_icon_label.setVisible(False)
        batt_text = f"Pil: {int(b.percent)}%"
        self.battery_label.setText(batt_text)
        if self.free_battery_window:
            self.free_battery_window.battery_label.setText(batt_text)

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
        if self.free_battery_window:
            self.free_battery_window.battery_label.setStyleSheet(
                f"color:{color};"
                f"opacity:{self.settings.battery_opacity};"
            )
            self.free_battery_window.battery_icon_label.setStyleSheet(
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


