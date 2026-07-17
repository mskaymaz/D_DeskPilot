try:
    from PySide6 import QtCore, QtGui, QtWidgets
except ImportError:
    from PyQt6 import QtCore, QtGui, QtWidgets


class AltHizaliEtiket(QtWidgets.QLabel):
    def paintEvent(self, event):
        metin = self.text()
        if not metin:
            super().paintEvent(event)
            return
        painter = QtGui.QPainter(self)
        painter.setFont(self.font())
        painter.setPen(self.palette().color(QtGui.QPalette.ColorRole.WindowText))
        fm = QtGui.QFontMetrics(self.font())
        satirlar = metin.splitlines()
        if len(satirlar) > 1:
            satir_araligi = 2
            toplam_yukseklik = (
                len(satirlar) * fm.height()
                + (len(satirlar) - 1) * satir_araligi
            )
            if self.alignment() & QtCore.Qt.AlignmentFlag.AlignVCenter:
                y = (self.height() - toplam_yukseklik) // 2 + fm.ascent()
            elif self.alignment() & QtCore.Qt.AlignmentFlag.AlignTop:
                y = fm.ascent()
            else:
                y = self.height() - toplam_yukseklik + fm.ascent()

            for satir in satirlar:
                rect = fm.tightBoundingRect(satir)
                if self.alignment() & QtCore.Qt.AlignmentFlag.AlignHCenter:
                    x = (self.width() - rect.width()) // 2 - rect.left()
                elif self.alignment() & QtCore.Qt.AlignmentFlag.AlignRight:
                    x = self.width() - rect.right()
                else:
                    x = -rect.left()
                painter.drawText(x, y, satir)
                y += fm.height() + satir_araligi
            return
        rect = fm.tightBoundingRect(metin)
        x = -rect.left()
        if self.alignment() & QtCore.Qt.AlignmentFlag.AlignHCenter:
            x += max(0, (self.width() - rect.width()) // 2)
        y = self.height() - rect.bottom()
        painter.drawText(x, y, metin)

    def sizeHint(self):
        fm = QtGui.QFontMetrics(self.font())
        satirlar = (self.text() or "0").splitlines() or ["0"]
        genislik = max(
            fm.tightBoundingRect(satir).width() for satir in satirlar
        )
        yukseklik = len(satirlar) * fm.height() + (len(satirlar) - 1) * 2
        return QtCore.QSize(max(1, genislik), max(1, yukseklik))
