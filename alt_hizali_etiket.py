try:
    from PySide6 import QtCore, QtGui, QtWidgets
except ImportError:
    from PyQt6 import QtCore, QtGui, QtWidgets


class AltHizaliEtiket(QtWidgets.QLabel):
    def paintEvent(self, event):
        metin = self.text()
        if not metin:
            return
        painter = QtGui.QPainter(self)
        painter.setFont(self.font())
        painter.setPen(self.palette().color(QtGui.QPalette.ColorRole.WindowText))
        fm = QtGui.QFontMetrics(self.font())
        rect = fm.tightBoundingRect(metin)
        x = -rect.left()
        if self.alignment() & QtCore.Qt.AlignmentFlag.AlignHCenter:
            x += max(0, (self.width() - rect.width()) // 2)
        y = self.height() - rect.bottom()
        painter.drawText(x, y, metin)

    def sizeHint(self):
        fm = QtGui.QFontMetrics(self.font())
        rect = fm.tightBoundingRect(self.text() or "0")
        return QtCore.QSize(max(1, rect.width()), max(1, fm.height()))
