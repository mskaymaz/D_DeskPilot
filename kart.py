import os

try:
    from PySide6 import QtCore, QtGui, QtWidgets
    Signal = QtCore.Signal
    Signal = QtCore.Signal
except ImportError:
    from PyQt6 import QtCore, QtGui, QtWidgets
    Signal = QtCore.pyqtSignal
    Signal = QtCore.pyqtSignal

from gorev_modeli import GorevModeli, GorevOnceligi
from gorev_tema import GorevTema, VARSAYILAN_GOREV_TEMASI


class GorevKarti(QtWidgets.QFrame):
    durum_degisti = Signal(object, bool)
    sil_istendi = Signal(object)

    def __init__(self, gorev: GorevModeli, tema: GorevTema = VARSAYILAN_GOREV_TEMASI, parent=None):
        super().__init__(parent)
        self.gorev = gorev
        self.tema = tema
        self.setObjectName("gorevKarti")
        self._arayuz_kur()
        self._stili_uygula()

    def _arayuz_kur(self):
        ana = QtWidgets.QHBoxLayout(self)
        ana.setContentsMargins(10, 4, 10, 4)
        ana.setSpacing(0)

        self.sol_panel = QtWidgets.QFrame()
        self.sol_panel.setObjectName("oncelikPaneli")
        self.sol_panel.setFixedWidth(34)

        sol = QtWidgets.QVBoxLayout(self.sol_panel)
        sol.setContentsMargins(0, 0, 0, 0)
        sol.addStretch()

        self.btn_durum = QtWidgets.QPushButton()
        self.btn_durum.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_durum.setFixedSize(30, 34)
        self.btn_durum.clicked.connect(self._durum_butonu_tiklandi)
        sol.addWidget(self.btn_durum, 0, QtCore.Qt.AlignmentFlag.AlignCenter)

        sol.addStretch()
        ana.addWidget(self.sol_panel)

        self.govde = QtWidgets.QFrame()
        self.govde.setObjectName("gorevGovde")
        govde_layout = QtWidgets.QHBoxLayout(self.govde)
        govde_layout.setContentsMargins(14, 6, 10, 6)
        govde_layout.setSpacing(10)

        metin = QtWidgets.QVBoxLayout()
        metin.setContentsMargins(0, 0, 0, 0)
        metin.setSpacing(1)

        self.lbl_oncelik = QtWidgets.QLabel(self._oncelik_metni())
        self.lbl_baslik = QtWidgets.QLabel(self.gorev.baslik)
        self.lbl_baslik.setWordWrap(True)

        metin.addWidget(self.lbl_oncelik)
        metin.addWidget(self.lbl_baslik)
        metin.addStretch()
        govde_layout.addLayout(metin, 1)

        self.tarih_panel = QtWidgets.QFrame()
        self.tarih_panel.setObjectName("tarihPaneli")
        tarih_layout = QtWidgets.QVBoxLayout(self.tarih_panel)
        tarih_layout.setContentsMargins(9, 4, 9, 4)
        tarih_layout.setSpacing(1)

        self.lbl_tarih_baslik = QtWidgets.QLabel("Son Tarih")
        self.lbl_tarih = QtWidgets.QLabel(self._son_tarih_gun())
        self.lbl_saat = QtWidgets.QLabel(self._son_tarih_saat())

        tarih_layout.addWidget(self.lbl_tarih_baslik)
        tarih_layout.addWidget(self.lbl_tarih)
        tarih_layout.addWidget(self.lbl_saat)
        self.tarih_panel.setVisible(bool(self.gorev.bitis_tarihi))
        govde_layout.addWidget(self.tarih_panel, 0, QtCore.Qt.AlignmentFlag.AlignVCenter)

        self.btn_sil = QtWidgets.QPushButton("×")
        self.btn_sil.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_sil.setFixedSize(30, 30)
        self.btn_sil.clicked.connect(lambda: self.sil_istendi.emit(self.gorev))
        govde_layout.addWidget(self.btn_sil, 0, QtCore.Qt.AlignmentFlag.AlignVCenter)

        ana.addWidget(self.govde, 1)

    def _stili_uygula(self):
        renk = self._oncelik_rengi()
        baslik_renk = self.tema.tamamlandi_rengi if self.gorev.tamamlandi else self.tema.metin_rengi

        self.setMinimumHeight(72)
        self.setStyleSheet("""
            QFrame#gorevKarti {
                background:#edf2f7;
                border-radius:11px;
            }
            QFrame#gorevGovde {
                background:white;
                border:1px solid #dbe4ee;
                border-top-right-radius:11px;
                border-bottom-right-radius:11px;
            }
            QFrame#tarihPaneli {
                background:#f8fafc;
                border:1px solid #e2e8f0;
                border-radius:8px;
            }
        """)
        self.sol_panel.setStyleSheet(
            f"QFrame#oncelikPaneli {{ background:{renk}; border-top-left-radius:11px; border-bottom-left-radius:11px; }}"
        )

        self._durum_ikonunu_ayarla()

        self.lbl_oncelik.setStyleSheet(f"color:{renk}; font-size:9pt; font-weight:500;")
        self.lbl_baslik.setStyleSheet(f"color:{baslik_renk}; font-size:11pt; font-weight:700;")
        self.lbl_tarih_baslik.setStyleSheet("color:#64748b; font-size:8pt; font-weight:500;")
        self.lbl_tarih.setStyleSheet("color:#334155; font-size:9pt; font-weight:700;")
        self.lbl_saat.setStyleSheet("color:#475569; font-size:9pt;")
        self.btn_sil.setStyleSheet("""
            QPushButton { background:transparent; border:none; color:#94a3b8; font-size:22px; font-weight:300; }
            QPushButton:hover { background:#f1f5f9; color:#ef4444; border-radius:15px; }
        """)
        self.update()

    def _durum_ikonunu_ayarla(self):
        self.btn_durum.setStyleSheet("""
            QPushButton { background:transparent; border:none; color:white; font-size:23px; font-weight:800; }
            QPushButton:hover { background:rgba(255,255,255,42); border-radius:7px; }
        """)
        if self.gorev.tamamlandi:
            self.btn_durum.setIcon(QtGui.QIcon())
            self.btn_durum.setText("✔")
            return

        icon_path = os.path.join(os.path.dirname(__file__), "img", "icons", "Un1.svg")
        icon_path = os.path.join(os.path.dirname(__file__), "img", "icons", "Un1.svg")
        self.btn_durum.setText("")
        self.btn_durum.setIcon(QtGui.QIcon(icon_path))
        self.btn_durum.setIconSize(QtCore.QSize(27,27))
        self.btn_durum.setIcon(QtGui.QIcon(icon_path))
        self.btn_durum.setIconSize(QtCore.QSize(27, 27))

    def _durum_butonu_tiklandi(self):
        self.gorev.tamamlandi = not self.gorev.tamamlandi
        self._stili_uygula()
        self.durum_degisti.emit(self.gorev, self.gorev.tamamlandi)

    def paintEvent(self, event):
        super().paintEvent(event)
        if not self.gorev.tamamlandi:
            return

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing)
        painter.setOpacity(0.30)
        painter.setPen(QtGui.QColor("#111827"))

        font = painter.font()
        font.setPointSize(23)
        font.setBold(True)
        font.setLetterSpacing(QtGui.QFont.SpacingType.PercentageSpacing, 108)
        painter.setFont(font)

        painter.drawText(self.rect(), QtCore.Qt.AlignmentFlag.AlignCenter, "TAMAMLANDI")
        painter.end()

    def _oncelik_metni(self):
        if self.gorev.oncelik == GorevOnceligi.YUKSEK:
            return "Yüksek Öncelik"
        if self.gorev.oncelik == GorevOnceligi.DUSUK:
            return "Düşük Öncelik"
        return "Normal Öncelik"

    def _oncelik_rengi(self):
        if self.gorev.oncelik == GorevOnceligi.YUKSEK:
            return self.tema.yuksek_oncelik_rengi
        if self.gorev.oncelik == GorevOnceligi.DUSUK:
            return self.tema.dusuk_oncelik_rengi
        return self.tema.normal_oncelik_rengi

    def _son_tarih_gun(self):
        return "" if not self.gorev.bitis_tarihi else self.gorev.bitis_tarihi.strftime("%d.%m.%Y")

    def _son_tarih_saat(self):
        return "" if not self.gorev.bitis_tarihi else self.gorev.bitis_tarihi.strftime("%H:%M")




if __name__ == "__main__":
    from datetime import datetime, timedelta
    import sys

    app = QtWidgets.QApplication(sys.argv)

    pencere = QtWidgets.QWidget()
    pencere.setWindowTitle("Görev Kartı Önizleme")
    pencere.resize(620, 320)

    layout = QtWidgets.QVBoxLayout(pencere)
    layout.setContentsMargins(18, 18, 18, 18)
    layout.setSpacing(5)

    ornekler = [
        GorevModeli("Yüksek öncelikli görev kartı", GorevOnceligi.YUKSEK, False, bitis_tarihi=datetime.now() + timedelta(hours=2)),
        GorevModeli("Normal görev kartı", GorevOnceligi.NORMAL, False, bitis_tarihi=datetime.now() + timedelta(days=1)),
        GorevModeli("Düşük öncelikli görev kartı", GorevOnceligi.DUSUK, False, bitis_tarihi=datetime.now()),
    ]

    for gorev in ornekler:
        layout.addWidget(GorevKarti(gorev))

    layout.addStretch()
    pencere.show()
    sys.exit(app.exec())


