try:
    from PySide6 import QtCore, QtGui, QtWidgets
except ImportError:
    from PyQt6 import QtCore, QtGui, QtWidgets

from utils import resource_path


class StartupSplash(QtWidgets.QWidget):
    """MSKLabs ve DeskPilot logolarını kısa bir başlangıç geçişiyle gösterir."""

    LOGO_MAX_SIZE = 440

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("startupSplash")
        self.setFixedSize(520, 520)
        self.setWindowFlags(
            QtCore.Qt.WindowType.SplashScreen
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setStyleSheet(
            "#startupSplash { background: white; border: 1px solid #d7e1ea; "
            "border-radius: 18px; }"
        )

        self._loop = None
        self._logo_stack = QtWidgets.QWidget(self)
        self._logo_stack.setFixedSize(450, 450)

        self._msk_label = QtWidgets.QLabel(self._logo_stack)
        self._deskpilot_label = QtWidgets.QLabel(self._logo_stack)
        for label in (self._msk_label, self._deskpilot_label):
            label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            label.setGeometry(self._logo_stack.rect())

        self._msk_label.setPixmap(self._logo_pixmap("img/logos/MSKLabsLogo.svg"))
        self._deskpilot_label.setPixmap(
            self._logo_pixmap("img/logos/DeskPilot logo transparent.png")
        )

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(35, 35, 35, 35)
        layout.addWidget(self._logo_stack, 0, QtCore.Qt.AlignmentFlag.AlignCenter)

        self._msk_effect = QtWidgets.QGraphicsOpacityEffect(self._msk_label)
        self._deskpilot_effect = QtWidgets.QGraphicsOpacityEffect(self._deskpilot_label)
        self._msk_label.setGraphicsEffect(self._msk_effect)
        self._deskpilot_label.setGraphicsEffect(self._deskpilot_effect)
        self._msk_effect.setOpacity(1.0)
        self._deskpilot_effect.setOpacity(0.0)
        self.setWindowOpacity(1.0)

    def _logo_pixmap(self, relative_path):
        path = resource_path(relative_path)
        if relative_path.lower().endswith(".svg"):
            pixmap = QtGui.QIcon(path).pixmap(
                QtCore.QSize(self.LOGO_MAX_SIZE, self.LOGO_MAX_SIZE)
            )
        else:
            pixmap = QtGui.QPixmap(path)
        return pixmap.scaled(
            self.LOGO_MAX_SIZE,
            self.LOGO_MAX_SIZE,
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation,
        )

    def showEvent(self, event):
        super().showEvent(event)
        screen = QtGui.QGuiApplication.primaryScreen()
        if screen:
            available = screen.availableGeometry()
            self.move(
                available.left() + (available.width() - self.width()) // 2,
                available.top() + (available.height() - self.height()) // 2,
            )
        QtCore.QTimer.singleShot(2000, self._crossfade_to_deskpilot)

    def _crossfade_to_deskpilot(self):
        self._crossfade = QtCore.QParallelAnimationGroup(self)
        for effect, start, end in (
            (self._msk_effect, 1.0, 0.0),
            (self._deskpilot_effect, 0.0, 1.0),
        ):
            animation = QtCore.QPropertyAnimation(effect, b"opacity", self)
            animation.setDuration(1000)
            animation.setStartValue(start)
            animation.setEndValue(end)
            self._crossfade.addAnimation(animation)
        self._crossfade.finished.connect(
            lambda: QtCore.QTimer.singleShot(2000, self._fade_out)
        )
        self._crossfade.start()

    def _fade_out(self):
        self._window_fade = QtCore.QPropertyAnimation(self, b"windowOpacity", self)
        self._window_fade.setDuration(500)
        self._window_fade.setStartValue(1.0)
        self._window_fade.setEndValue(0.0)
        self._window_fade.finished.connect(self._finish)
        self._window_fade.start()

    def _finish(self):
        if self._loop:
            self._loop.quit()
        self.close()

    def wait_until_finished(self, app):
        self._loop = QtCore.QEventLoop(self)
        self.show()
        self.raise_()
        app.processEvents()
        self._loop.exec()


def show_startup_splash(app):
    splash = StartupSplash()
    splash.wait_until_finished(app)
