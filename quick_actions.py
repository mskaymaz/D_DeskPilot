import math

from PySide6 import QtCore, QtGui, QtWidgets
from utils import resource_path

class QuickActionsPanel(QtWidgets.QFrame):
    BASE_SIZE = 46

    def __init__(self, owner, controller):
        super().__init__(owner)
        self.owner = owner
        self.controller = controller
        self.setVisible(False)
        self.setObjectName("quickActions")
        self._hit_overlays = []
        self._hide_timer = QtCore.QTimer(self)
        self._hide_timer.setSingleShot(True)
        self._hide_timer.timeout.connect(lambda: self.hide() if not self.underMouse() else None)
        self._apply_window_flags()
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        self.btn_settings = QtWidgets.QPushButton("⚙")
        self.btn_reminders = QtWidgets.QPushButton("🔔")
        self.btn_todos = QtWidgets.QPushButton()
        self.btn_todos.setIcon(QtGui.QIcon(resource_path("img/icons/todo_icon.svg")))

        for btn in (self.btn_settings, self.btn_reminders, self.btn_todos):
            btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            layout.addWidget(btn)

        self.btn_settings.clicked.connect(self._settings_clicked)
        self.btn_reminders.clicked.connect(controller.show_reminder_list)
        self.btn_todos.clicked.connect(controller.show_todo_list)
        self._apply_size()

    def _settings_clicked(self):
        self.controller.show_settings_at(hedef_tur=getattr(self.owner, "tur", None))

    def _scale(self):
        return float(getattr(getattr(self.controller, "settings", None), "global_scale", 1.0))

    def _apply_window_flags(self):
        flags = QtCore.Qt.WindowType.Tool | QtCore.Qt.WindowType.FramelessWindowHint
        settings = getattr(self.controller, "settings", None) or getattr(self.owner, "ayarlar", None)
        if getattr(settings, "her_zaman_ustte", False):
            flags |= QtCore.Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(flags)

    def _apply_size(self):
        size = max(24, min(72, int(self.BASE_SIZE * self._scale() * 0.935)))
        for btn in (self.btn_settings, self.btn_reminders, self.btn_todos):
            btn.setFixedSize(size, size)
        self.btn_settings.setStyleSheet(f"font-size:{int(size*0.62)}px;")
        self.btn_reminders.setStyleSheet(f"font-size:{int(size*0.62*0.90)}px;")
        self.btn_todos.setIconSize(QtCore.QSize(int(size*0.84*0.76), int(size*0.84*0.76)))
        self.setStyleSheet(f"QFrame#quickActions{{background:transparent;}} QPushButton{{background:transparent;border:none;color:white;font-size:{max(14, int(size*0.62))}px;}} QPushButton:hover{{background:rgba(255,255,255,35);border-radius:8px;}}")
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
        local_rect = QtCore.QRect(
            local_left,
            local_top,
            max(1, local_right - local_left),
            max(1, local_bottom - local_top),
        )
        return local_rect

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
            return False
        return super().eventFilter(obj, event)

    def place_for_widget(self, widget):
        self.place_for_content_rect(self._content_rect(widget))

    def place_for_content_rect(self, content_rect):
        if self._hide_timer.isActive():
            self._hide_timer.stop()
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
