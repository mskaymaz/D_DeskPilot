import math

from PySide6 import QtCore, QtGui, QtWidgets
from utils import resource_path


class QuickActionsPanel(QtWidgets.QFrame):
    def __init__(self, owner, controller):
        super().__init__(owner)
        self.owner = owner
        self.controller = controller
        self.setVisible(False)
        self.setObjectName("quickActions")
        self._hit_overlays = []
        self._last_anchor_pos = None
        self._hide_timer = QtCore.QTimer(self)
        self._hide_timer.setSingleShot(True)
        self._hide_timer.timeout.connect(lambda: self.hide() if not self.underMouse() else None)
        self._apply_window_flags()
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self._layout = QtWidgets.QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(self._icon_spacing())
        self._layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetFixedSize)

        self.btn_settings = QtWidgets.QPushButton("\u2699")
        self.btn_alarm = QtWidgets.QPushButton()
        self.btn_alarm.setIcon(QtGui.QIcon(resource_path("img/icons/alarm_icon.svg")))
        self.btn_reminders = QtWidgets.QPushButton("\U0001f514")
        self.btn_todos = QtWidgets.QPushButton()
        self.btn_todos.setIcon(QtGui.QIcon(resource_path("img/icons/todo_icon.svg")))
        self.btn_settings.setToolTip("Ayarlar")
        self.btn_alarm.setToolTip("Alarm")
        self.btn_reminders.setToolTip("Reminder")
        self.btn_todos.setToolTip("Todo")

        for btn in (self.btn_settings, self.btn_alarm, self.btn_reminders, self.btn_todos):
            btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            btn.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
            self._layout.addWidget(btn)

        self.btn_settings.clicked.connect(self._settings_clicked)
        self.btn_alarm.clicked.connect(controller.show_alarm_list)
        self.btn_reminders.clicked.connect(controller.show_reminder_list)
        self.btn_todos.clicked.connect(controller.show_todo_list)
        self._apply_size()

    def _settings_clicked(self):
        anchor_pos = self._last_anchor_pos or self.mapToGlobal(self.rect().center())
        self.controller.show_settings_at(anchor_pos, hedef_tur=getattr(self.owner, "tur", None))

    def _icon_spacing(self):
        settings = getattr(self.controller, "settings", None) or getattr(self.owner, "ayarlar", None)
        return max(0, int(getattr(settings, "quick_actions_icon_spacing", 2) or 0))

    def _icon_size(self):
        settings = getattr(self.controller, "settings", None) or getattr(self.owner, "ayarlar", None)
        return max(24, min(80, int(getattr(settings, "quick_actions_icon_size", 38) or 38)))

    def _apply_window_flags(self):
        flags = QtCore.Qt.WindowType.Tool | QtCore.Qt.WindowType.FramelessWindowHint
        settings = getattr(self.controller, "settings", None) or getattr(self.owner, "ayarlar", None)
        if getattr(settings, "her_zaman_ustte", False):
            flags |= QtCore.Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(flags)

    def _apply_size(self):
        self._layout.setSpacing(self._icon_spacing())
        size = self._icon_size()
        settings = getattr(self.controller, "settings", None) or getattr(self.owner, "ayarlar", None)
        self.btn_alarm.setVisible(bool(getattr(settings, "alarm_visible", True)))
        self.btn_reminders.setVisible(bool(getattr(settings, "reminder_visible", True)))
        self.btn_todos.setVisible(bool(getattr(settings, "todo_visible", True)))
        for btn in (self.btn_settings, self.btn_alarm, self.btn_reminders, self.btn_todos):
            btn.setFixedSize(size, size)
        alarm_icon_size = int(size * 0.84 * 0.76 * 1.32)
        self.btn_alarm.setIconSize(QtCore.QSize(alarm_icon_size, alarm_icon_size))
        self.btn_todos.setIconSize(QtCore.QSize(int(size * 0.84 * 0.76), int(size * 0.84 * 0.76)))
        self.setStyleSheet(
            "QFrame#quickActions{background:transparent;}"
            f"QPushButton{{background:transparent;border:none;color:white;font-size:{max(14, int(size * 0.62))}px;padding:0px;margin:0px;}}"
            "QPushButton:hover{background:rgba(255,255,255,35);border-radius:8px;}"
        )
        self.btn_settings.setStyleSheet(f"font-size:{int(size * 0.62)}px;padding:0px;margin:0px;")
        self.btn_reminders.setStyleSheet(f"font-size:{int(size * 0.62 * 0.99)}px;padding:0px;margin:0px;")
        self.adjustSize()

    def _rendered_rect(self, widget):
        if widget.width() <= 0 or widget.height() <= 0:
            return widget.rect()

        dpr = widget.devicePixelRatioF()
        image_size = QtCore.QSize(
            max(1, math.ceil(widget.width() * dpr)),
            max(1, math.ceil(widget.height() * dpr)),
        )
        image = QtGui.QImage(image_size, QtGui.QImage.Format.Format_ARGB32_Premultiplied)
        image.setDevicePixelRatio(dpr)
        image.fill(QtCore.Qt.GlobalColor.transparent)
        widget.render(
            image,
            QtCore.QPoint(),
            QtGui.QRegion(),
            QtWidgets.QWidget.RenderFlag.DrawChildren,
        )

        left = image.width()
        top = image.height()
        right = -1
        bottom = -1
        for y in range(image.height()):
            for x in range(image.width()):
                if image.pixelColor(x, y).alpha():
                    left = min(left, x)
                    top = min(top, y)
                    right = max(right, x)
                    bottom = max(bottom, y)

        if right < left or bottom < top:
            return widget.rect()

        local_left = math.floor(left / dpr)
        local_top = math.floor(top / dpr)
        local_right = math.ceil((right + 1) / dpr)
        local_bottom = math.ceil((bottom + 1) / dpr)
        return QtCore.QRect(
            local_left,
            local_top,
            max(1, local_right - local_left),
            max(1, local_bottom - local_top),
        )

    def _content_rect(self, widget):
        labels = [w for w in widget.findChildren(QtWidgets.QLabel) if w.isVisible()]
        if isinstance(widget, QtWidgets.QLabel) and widget.isVisible():
            labels.insert(0, widget)
        rect = None
        for label in labels:
            local = self._rendered_rect(label)
            mapped = QtCore.QRect(label.mapTo(self.owner, local.topLeft()), local.size())
            rect = mapped if rect is None else rect.united(mapped)
        if rect is not None:
            return rect
        local_rect = self._rendered_rect(widget)
        return QtCore.QRect(widget.mapTo(self.owner, local_rect.topLeft()), local_rect.size())

    def hit_rect_for_widget(self, widget):
        return self._content_rect(widget)

    def show_hit_rects(self, rects):
        while len(self._hit_overlays) < len(rects):
            overlay = QtWidgets.QFrame(self.owner)
            overlay.setMouseTracking(True)
            overlay.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
            overlay.installEventFilter(self)
            overlay.setStyleSheet("background:rgba(255,255,0,0);border:none;")
            self._hit_overlays.append(overlay)

        for overlay, rect in zip(self._hit_overlays, rects):
            overlay.setGeometry(rect)
            overlay.raise_()
            overlay.show()
        for overlay in self._hit_overlays[len(rects):]:
            overlay.hide()

    def eventFilter(self, obj, event):
        if obj in self._hit_overlays and event.type() == QtCore.QEvent.Type.MouseMove:
            if hasattr(self.owner, "_quick_hover"):
                self.owner._quick_hover(obj.mapTo(self.owner, event.position().toPoint()))
            if getattr(self.owner, "drag_pos", None) or getattr(self.owner, "surukleme_konumu", None) or getattr(self.owner, "_group_drag", None):
                self.owner.mouseMoveEvent(event)
            return False
        if obj in self._hit_overlays:
            if event.type() not in (
                QtCore.QEvent.Type.MouseButtonPress,
                QtCore.QEvent.Type.MouseButtonRelease,
            ):
                return super().eventFilter(obj, event)
            global_pos = event.globalPosition().toPoint()
            if event.type() == QtCore.QEvent.Type.MouseButtonPress:
                if event.button() == QtCore.Qt.MouseButton.RightButton:
                    local_pos = self.owner.mapFromGlobal(global_pos)
                    if hasattr(self.owner, "_menuyu_goster"):
                        self.owner._menuyu_goster(local_pos)
                    elif hasattr(self.owner, "show_menu"):
                        self.owner.show_menu(local_pos)
                    return True
                if event.button() == QtCore.Qt.MouseButton.LeftButton:
                    if hasattr(self.owner, "surukleme_konumu"):
                        self.owner.surukleme_konumu = global_pos - self.owner.frameGeometry().topLeft()
                    elif getattr(self.owner, "_group_editing", False):
                        local_pos = obj.mapTo(self.owner, event.position().toPoint())
                        widget = self.owner._group_widget_at(local_pos)
                        if widget is not None:
                            canvas_pos = self.owner.group_canvas.mapFrom(self.owner, local_pos)
                            self.owner._group_drag = (widget, canvas_pos - widget.pos())
                    else:
                        self.owner.drag_pos = global_pos - self.owner.frameGeometry().topLeft()
                    return True
            elif event.type() == QtCore.QEvent.Type.MouseButtonRelease:
                if event.button() == QtCore.Qt.MouseButton.LeftButton:
                    self.owner.mouseReleaseEvent(event)
                    return True
        return super().eventFilter(obj, event)

    def place_for_widget(self, widget):
        self.place_for_content_rect(self._content_rect(widget))

    def place_for_content_rect(self, content_rect):
        if self._hide_timer.isActive():
            self._hide_timer.stop()
        self._last_anchor_pos = self.owner.mapToGlobal(content_rect.center())
        self._apply_window_flags()
        self._apply_size()
        anchor_top = content_rect.top()
        anchor_center_x = content_rect.center().x()
        panel_bottom = self._rendered_rect(self).bottom() + 1
        top_left = self.owner.mapToGlobal(QtCore.QPoint(anchor_center_x, anchor_top))
        x = top_left.x() - self.width() // 2
        y = top_left.y() - panel_bottom - 8

        screen = QtGui.QGuiApplication.screenAt(top_left)
        if screen:
            available = screen.availableGeometry()
            x = max(available.left(), min(x, available.right() - self.width()))
            y = max(available.top(), y)
        self.move(x, y)
        self.raise_()
        self.show()

    def delayed_hide(self):
        self._hide_timer.start(500)
