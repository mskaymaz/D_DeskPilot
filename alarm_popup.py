from PySide6 import QtCore, QtGui, QtWidgets
try:
    import winsound
except ImportError:
    winsound = None


class AlarmBildirimPenceresi(QtWidgets.QWidget):
    durduruldu_sinyali = QtCore.Signal(str)
    ertelendi_sinyali = QtCore.Signal(str, int)

    def __init__(self, alarm, parent=None):
        super().__init__(
            parent,
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.WindowStaysOnTopHint
            | QtCore.Qt.WindowType.Tool,
        )
        self.alarm = alarm
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self._arayuz_kur()
        self._konumlandir()
        self._ses_cal()

    def _arayuz_kur(self):
        govde = QtWidgets.QFrame(self)
        govde.setObjectName("Govde")
        govde.setStyleSheet(
            """
            #Govde { background:#111827; border:2px solid #facc15; border-radius:12px; }
            QLabel { color:white; font-family:'Segoe UI'; }
            QPushButton { background:#374151; color:white; border-radius:6px; padding:8px; font-weight:bold; }
            QPushButton:hover { background:#facc15; color:#111827; }
            #Baslik { font-size:17px; font-weight:bold; color:#facc15; }
            #Aciklama { font-size:13px; color:#d1d5db; }
            """
        )
        layout = QtWidgets.QVBoxLayout(govde)
        lbl_baslik = QtWidgets.QLabel(self.alarm.baslik or "Alarm")
        lbl_baslik.setObjectName("Baslik")
        lbl_baslik.setWordWrap(True)
        lbl_aciklama = QtWidgets.QLabel(self.alarm.aciklama or f"Alarm zamanı geldi: {self.alarm.saat}")
        lbl_aciklama.setObjectName("Aciklama")
        lbl_aciklama.setWordWrap(True)

        ertele_dakika = max(1, int(getattr(self.alarm, "snooze_dakika", 5) or 5))
        btn_durdur = QtWidgets.QPushButton("Durdur")
        btn_ertele = QtWidgets.QPushButton(f"{ertele_dakika} dk ertele")
        btn_durdur.clicked.connect(self._durdur)
        btn_ertele.clicked.connect(lambda: self._ertele(ertele_dakika))

        btns = QtWidgets.QHBoxLayout()
        btns.addWidget(btn_durdur)
        btns.addWidget(btn_ertele)

        layout.addWidget(lbl_baslik)
        layout.addWidget(lbl_aciklama)
        layout.addSpacing(10)
        layout.addLayout(btns)

        main = QtWidgets.QVBoxLayout(self)
        main.addWidget(govde)
        self.setFixedSize(300, 160)

    def _konumlandir(self):
        ekran = QtGui.QGuiApplication.primaryScreen().availableGeometry()
        x = ekran.left() + (ekran.width() - self.width()) // 2
        y = ekran.top() + (ekran.height() - self.height()) // 2
        self.move(x, y)

    def _ses_cal(self):
        if winsound:
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)

    def _durdur(self):
        self.durduruldu_sinyali.emit(self.alarm.id)
        self.close()

    def _ertele(self, dakika):
        self.ertelendi_sinyali.emit(self.alarm.id, dakika)
        self.close()
