from PySide6 import QtCore, QtGui, QtWidgets
from utils import resource_path, ICON_FILE


class SistemTepsisi(QtWidgets.QSystemTrayIcon):
    def __init__(self, ana_pencere, parent=None):
        super().__init__(parent)
        self.ana_pencere = ana_pencere
        self.setIcon(QtGui.QIcon(resource_path(ICON_FILE)))
        self.setToolTip("DeskPilot")

        self._menu_kur()
        self.activated.connect(self._tetiklendi)

    def _menu_kur(self):
        menu = QtWidgets.QMenu()

        self.act_goster = menu.addAction("G\u00f6ster / Gizle")
        self.act_goster.triggered.connect(self._gorunurluk_degistir)

        menu.addSeparator()

        if self.ana_pencere.settings.alarm_visible:
            act_alarm = menu.addAction("Alarm")
            act_alarm.setIcon(QtGui.QIcon(resource_path("img/icons/alarm_icon.svg")))
            act_alarm.triggered.connect(self.ana_pencere.show_alarm_list)

        if self.ana_pencere.settings.todo_visible:
            act_yeni_todo = menu.addAction("Todo")
            act_yeni_todo.setIcon(QtGui.QIcon(resource_path("img/icons/todo_icon.svg")))
            act_yeni_todo.triggered.connect(self.ana_pencere.show_todo_list)

        if self.ana_pencere.settings.reminder_visible:
            act_yeni_hatirlatici = menu.addAction("Reminder")
            act_yeni_hatirlatici.setIcon(QtGui.QIcon(resource_path("img/icons/reminder_icon.svg")))
            act_yeni_hatirlatici.triggered.connect(self.ana_pencere.show_reminder_list)

        menu.addSeparator()

        act_ayarlar = menu.addAction("Ayarlar")
        act_ayarlar.setIcon(QtGui.QIcon(resource_path("img/icons/settings_icon.svg")))
        act_ayarlar.triggered.connect(lambda: self.ana_pencere.show_settings_at())

        act_cikis = menu.addAction("\u00c7\u0131k\u0131\u015f")
        act_cikis.setIcon(QtGui.QIcon(resource_path("img/icons/exit_icon.svg")))
        act_cikis.triggered.connect(QtWidgets.QApplication.quit)

        self.setContextMenu(menu)

    def _tetiklendi(self, sebep):
        if sebep == QtWidgets.QSystemTrayIcon.ActivationReason.Trigger:
            self._gorunurluk_degistir()

    def _gorunurluk_degistir(self):
        if self.ana_pencere.isVisible() or (
            self.ana_pencere.free_time_window and self.ana_pencere.free_time_window.isVisible()
        ):
            if self.ana_pencere.settings.free_layout_enabled:
                self.ana_pencere._hide_free_windows()
            else:
                self.ana_pencere.hide()
        else:
            if self.ana_pencere.settings.free_layout_enabled:
                self.ana_pencere._show_free_windows()
            else:
                self.ana_pencere.show()

    def ozet_guncelle(self, pil_yuzdesi, sarjda, sonraki_hatirlatici_metni):
        sarj_durumu = (
            "Dolu" if sarjda and pil_yuzdesi >= 100
            else "\u015earj oluyor" if sarjda
            else "Pilde \u00e7al\u0131\u015f\u0131yor"
        )
        hatirlatici_bilgi = f"\nSonraki: {sonraki_hatirlatici_metni}" if sonraki_hatirlatici_metni else ""
        self.setToolTip(f"DeskPilot\nPil: %{pil_yuzdesi} ({sarj_durumu}){hatirlatici_bilgi}")
