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
        if not self.drag_pos:
            self._quick_hover(e.position().toPoint())
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

    def _quick_hover(self, pos):
        if not hasattr(self, "quick_actions"):
            return
        hit_rects = []
        content_rect = None
        for w in (self.battery_row, self.time_label, self.date_label):
            if not w.isVisible():
                continue
            cr = self.quick_actions.hit_rect_for_widget(w)
            hit_rects.append(cr)
            content_rect = cr if content_rect is None else content_rect.united(cr)
        self.quick_actions.show_hit_rects(hit_rects)
        if content_rect and any(rect.contains(pos) for rect in hit_rects):
            self.quick_actions.place_for_content_rect(content_rect)
            return
        self.quick_actions.delayed_hide()

    def leaveEvent(self, e):
        if hasattr(self, "quick_actions"):
            self.quick_actions.delayed_hide()
        super().leaveEvent(e)
