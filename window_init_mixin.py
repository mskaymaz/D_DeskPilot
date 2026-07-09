try:
    from PySide6 import QtCore, QtGui, QtWidgets
except ImportError:
    from PyQt6 import QtCore, QtGui, QtWidgets

from utils import resource_path, ICON_FILE
from utils import log_altyapisini_kur, log_kaydet
from quick_actions import QuickActionsPanel
from alt_hizali_etiket import AltHizaliEtiket


class WindowInitMixin:
    def _init_state(self):
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

    def _init_logging(self):
        log_altyapisini_kur()
        log_kaydet("Uygulama baslatildi.")

    def _init_window(self):
        flags = QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.Window
        if self.settings.her_zaman_ustte:
            flags |= QtCore.Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowOpacity(self.settings.seffaflik)
        self.setWindowIcon(QtGui.QIcon(resource_path(ICON_FILE)))

    def _init_widgets(self):
        self.date_label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.date_week_separator_label = QtWidgets.QLabel("◆", alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.date_week_number_label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.date_week_text_label = QtWidgets.QLabel("HAFTA", alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.hicri_date_label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.date_week_separator_label.setVisible(False)
        self.date_week_number_label.setVisible(False)
        self.date_week_text_label.setVisible(False)
        self.battery_label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.battery_icon_label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.battery_icon_label.setVisible(False)

        self.date_row = QtWidgets.QWidget()
        self.date_row_layout = QtWidgets.QHBoxLayout(self.date_row)
        self.date_row_layout.setContentsMargins(0, 0, 0, 0)
        self.date_row_layout.setSpacing(0)
        self.date_row_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.date_row_layout.addWidget(self.date_label, 0, QtCore.Qt.AlignmentFlag.AlignBottom)
        self.date_row_layout.addWidget(self.date_week_separator_label, 0, QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.date_row_layout.addWidget(self.date_week_number_label, 0, QtCore.Qt.AlignmentFlag.AlignBottom)
        self.date_row_layout.addWidget(self.date_week_text_label, 0, QtCore.Qt.AlignmentFlag.AlignBottom)

        self.date_container = QtWidgets.QWidget()
        self.date_container_layout = QtWidgets.QVBoxLayout(self.date_container)
        self.date_container_layout.setContentsMargins(0, 0, 0, 0)
        self.date_container_layout.setSpacing(0)
        self.date_container_layout.addWidget(self.date_row)
        self.date_container_layout.addWidget(self.hicri_date_label)

        self.battery_row = QtWidgets.QWidget()
        self.battery_row_layout = QtWidgets.QHBoxLayout(self.battery_row)
        self.battery_row_layout.setContentsMargins(0, 0, 0, 0)
        self.battery_row_layout.setSpacing(4)
        self.battery_row_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.battery_row_layout.addWidget(self.battery_label)
        self.battery_row_layout.addWidget(self.battery_icon_label)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.time_label = QtWidgets.QWidget()
        self.time_label_layout = QtWidgets.QHBoxLayout(self.time_label)
        self.time_label_layout.setContentsMargins(0, 0, 0, 0)
        self.time_label_layout.setSpacing(0)
        self.time_label_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.time_main_label = AltHizaliEtiket(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.time_seconds_label = AltHizaliEtiket(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.time_ampm_label = AltHizaliEtiket(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.time_label_layout.addWidget(self.time_main_label, 0, QtCore.Qt.AlignmentFlag.AlignBottom)
        self.time_label_layout.addWidget(self.time_seconds_label, 0, QtCore.Qt.AlignmentFlag.AlignBottom)
        self.time_label_layout.addWidget(self.time_ampm_label, 0, QtCore.Qt.AlignmentFlag.AlignBottom)
        self.setMouseTracking(True)

        self.main_layout.addWidget(self.battery_row)
        self.main_layout.addWidget(self.time_label)
        self.main_layout.addWidget(self.date_container)

        self.quick_actions = QuickActionsPanel(self, self)

        for lbl in (
            self.time_label,
            self.time_main_label,
            self.time_seconds_label,
            self.time_ampm_label,
            self.date_label,
            self.date_week_separator_label,
            self.date_week_number_label,
            self.date_week_text_label,
            self.hicri_date_label,
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

    def _init_startup(self):
        self._zamanlayicilari_kur()
        self._servisleri_baslat()
        self._setup_keep_on_top()
        self.apply_settings()
        self.update_time()
