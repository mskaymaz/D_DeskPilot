try:
    from PySide6 import QtCore, QtWidgets
except ImportError:
    from PyQt6 import QtCore, QtWidgets


class KaliciComboBox(QtWidgets.QComboBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedWidth(81)

    def showPopup(self):
        menu = QtWidgets.QMenu(self)
        menu.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint, True)
        menu.setFixedWidth(self.width())
        menu.setStyleSheet("""
            QMenu::item { padding: 4px 6px 4px 3px; }
            QMenu::icon { width: 0px; }
            QMenu::indicator { width: 0px; height: 0px; }
        """)
        for i in range(self.count()):
            action = menu.addAction(self.itemText(i))
            action.setData(i)
        secim = menu.exec(self.mapToGlobal(QtCore.QPoint(0, self.height())))
        if secim is not None and secim.data() is not None:
            self.setCurrentIndex(int(secim.data()))

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.showPopup()
            event.accept()
            return
        super().mousePressEvent(event)

    def wheelEvent(self, event):
        event.ignore()
