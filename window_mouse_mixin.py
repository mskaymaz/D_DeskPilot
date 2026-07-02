try:
    from PySide6 import QtCore, QtGui
except ImportError:
    from PyQt6 import QtCore, QtGui

from core_settings import save_settings


class WindowMouseMixin:
    def mousePressEvent(self, e):
        if self.settings.settings_locked:
            return
        if e.button() == QtCore.Qt.MouseButton.LeftButton:
            self.drag_pos = e.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        if self.settings.settings_locked:
            return
        if self.drag_pos:
            self.move(e.globalPosition().toPoint() - self.drag_pos)
            if hasattr(self, "settings_window") and self.settings_window.isVisible():
                self.position_settings_window(self.settings_window)

    def mouseReleaseEvent(self, e):
        self.drag_pos = None
        if self.settings.settings_locked:
            return
        self.settings.pos_x = self.x()
        self.settings.pos_y = self.y()
        ekran = QtGui.QGuiApplication.screenAt(self.pos())
        if ekran:
            self.settings.grup_ekran_adi = ekran.name()
        save_settings(self.settings)