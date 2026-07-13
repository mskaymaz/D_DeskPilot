try:
    from PySide6 import QtCore, QtGui
except ImportError:
    from PyQt6 import QtCore, QtGui

from core_settings import save_settings


class WindowMouseMixin:
    def _update_date_switch_hover(self, pos):
        button = getattr(self, "date_switch_button", None)
        if button is None:
            return
        mode = getattr(self.settings, "date_display_mode", "miladi_hicri")
        if not self.settings.date_visible or mode not in {"miladi", "hicri"}:
            button.setVisible(False)
            return
        button.setVisible(True)
        top_left = self.date_container.mapTo(self, QtCore.QPoint(0, 0))
        date_rect = QtCore.QRect(top_left, self.date_container.size())
        inside = date_rect.contains(pos)
        self._set_date_switch_style(button, inside)

    def _group_widget_at(self, pos):
        canvas_pos = self.group_canvas.mapFrom(self, pos)
        modules = (self.battery_row, self.time_label, self.date_container)
        for widget in reversed(modules):
            if widget.isVisible() and widget.geometry().contains(canvas_pos):
                widget.raise_()
                return widget
        return None

    def _save_group_layout(self):
        self.settings.group_layout = {
            key: {"x": widget.x(), "y": widget.y()}
            for key, widget in (
                ("battery", self.battery_row),
                ("time", self.time_label),
                ("date", self.date_container),
            )
        }
        self.settings.pos_x = self.x()
        self.settings.pos_y = self.y()
        ekran = QtGui.QGuiApplication.screenAt(self.pos())
        if ekran:
            self.settings.grup_ekran_adi = ekran.name()
        save_settings(self.settings)

    def _resize_group_canvas_after_drag(self):
        right = max(
            1,
            self.battery_row.x() + self.battery_row.width(),
            self.time_label.x() + self.time_label.width(),
            self.date_container.x() + self.date_container.width(),
        )
        bottom = max(
            1,
            self.battery_row.y() + self.battery_row.height(),
            self.time_label.y() + self.time_label.height(),
            self.date_container.y() + self.date_container.height(),
        )
        self.group_canvas.setFixedSize(right, bottom)

    def mousePressEvent(self, e):
        if (
            e.button() == QtCore.Qt.MouseButton.LeftButton
            and getattr(self, "date_switch_button", None) is not None
            and self.date_switch_button.isVisible()
        ):
            top_left = self.date_switch_button.mapTo(self, QtCore.QPoint(0, 0))
            if QtCore.QRect(top_left, self.date_switch_button.size()).contains(e.position().toPoint()):
                self._toggle_date_display_mode()
                return
        if self.settings.settings_locked:
            return
        if e.button() == QtCore.Qt.MouseButton.LeftButton:
            if self._group_editing:
                widget = self._group_widget_at(e.position().toPoint())
                if widget is not None:
                    canvas_pos = self.group_canvas.mapFrom(
                        self, e.position().toPoint()
                    )
                    self._group_drag = (
                        widget,
                        canvas_pos - widget.pos(),
                    )
                    return
            self.drag_pos = e.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        self._update_date_switch_hover(e.position().toPoint())
        if self.settings.settings_locked:
            return
        if self._group_drag:
            widget, offset = self._group_drag
            canvas_pos = self.group_canvas.mapFromGlobal(
                e.globalPosition().toPoint()
            )
            target = canvas_pos - offset
            shift_x = max(0, -target.x())
            shift_y = max(0, -target.y())
            if shift_x or shift_y:
                for module in (self.battery_row, self.time_label, self.date_container):
                    if module.isVisible():
                        module.move(module.x() + shift_x, module.y() + shift_y)
                self.move(self.x() - shift_x, self.y() - shift_y)
                target += QtCore.QPoint(shift_x, shift_y)
            widget.move(target)
            self._resize_group_canvas_after_drag()
            return
        if not self.drag_pos:
            self._quick_hover(e.position().toPoint())
        if self.drag_pos:
            self.move(e.globalPosition().toPoint() - self.drag_pos)
            if hasattr(self, "settings_window") and self.settings_window.isVisible():
                self.position_settings_window(self.settings_window)

    def mouseReleaseEvent(self, e):
        if self._group_drag:
            self._group_drag = None
            self._save_group_layout()
            self.adjustSize()
            return
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
        for w in (self.battery_row, self.time_label, self.date_row):
            if not w.isVisible():
                continue
            cr = self.quick_actions.hit_rect_for_widget(w)
            hit_rects.append(cr)
            content_rect = cr if content_rect is None else content_rect.united(cr)
        self.quick_actions.show_hit_rects([content_rect] if content_rect else [])
        if content_rect and content_rect.contains(pos):
            self.quick_actions.place_for_content_rect(content_rect)
            return
        self.quick_actions.delayed_hide()

    def leaveEvent(self, e):
        if hasattr(self, "quick_actions"):
            self.quick_actions.delayed_hide()
        super().leaveEvent(e)
