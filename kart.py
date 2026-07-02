import os

try:
    from PySide6 import QtCore, QtGui, QtWidgets
    Signal = QtCore.Signal
except ImportError:
    from PyQt6 import QtCore, QtGui, QtWidgets
    Signal = QtCore.pyqtSignal

from gorev_modeli import GorevModeli, GorevOnceligi
from gorev_tema import GorevTema, VARSAYILAN_GOREV_TEMASI
from oncelik_yonetimi import priority_name, priority_color



class RotatedLabel(QtWidgets.QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(parent)
        self._text = ""
        self.setFixedSize(28, 82)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setText(text)

    def setText(self, text):
        self._text = str(text or "")
        pixmap = QtGui.QPixmap(28, 82)
        pixmap.fill(QtCore.Qt.GlobalColor.transparent)

        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing)
        painter.setPen(QtGui.QColor("#ffffff"))
        font = QtGui.QFont("Segoe UI", 10)
        font.setBold(True)
        painter.setFont(font)
        painter.translate(14, 41)
        painter.rotate(-90)
        rect = QtCore.QRectF(-41, -14, 82, 28)
        painter.drawText(rect, QtCore.Qt.AlignmentFlag.AlignCenter, self._text)
        painter.end()

        self.setPixmap(pixmap)


class GorevKarti(QtWidgets.QFrame):
    durum_degisti = Signal(object, bool)
    sil_istendi = Signal(object)
    duzenle_istendi = Signal(object)

    def __init__(self, gorev: GorevModeli, tema: GorevTema = VARSAYILAN_GOREV_TEMASI, settings=None, parent=None):
        super().__init__(parent)
        self.gorev = gorev
        self.tema = tema
        self.settings = settings
        self.setObjectName("gorevKarti")
        self.setFixedSize(500, 82)
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        self._arayuz_kur()
        self.lbl_overlay = QtWidgets.QLabel("TAMAMLANDI", self)
        self.lbl_overlay.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lbl_overlay.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.lbl_overlay.setStyleSheet("background:transparent; color:rgba(17,24,39,128); font-family:'Segoe UI'; font-size:19pt; font-weight:800;")
        self.lbl_overlay.hide()
        self._stili_uygula()

    def _arayuz_kur(self):
        ana = QtWidgets.QHBoxLayout(self)
        ana.setContentsMargins(10, 3, 10, 3)
        ana.setSpacing(0)

        ana.addWidget(self._sol_panel_olustur())
        ana.addWidget(self._govde_panel_olustur(), 1)

    def _sol_panel_olustur(self):
        self.sol_panel = QtWidgets.QFrame()
        self.sol_panel.setFixedWidth(68)

        self.lbl_oncelik = RotatedLabel("", self.sol_panel)
        self.lbl_oncelik.setGeometry(0, 0, 28, 82)

        self.btn_durum = QtWidgets.QPushButton(self.sol_panel)
        self.btn_durum.setFixedSize(34, 34)
        self.btn_durum.move(30, 24)
        self.btn_durum.clicked.connect(self._durum_butonu_tiklandi)

        self.lbl_oncelik.raise_()
        self.btn_durum.raise_()
        return self.sol_panel

    def _govde_panel_olustur(self):
        govde = QtWidgets.QFrame()
        govde.setObjectName("gorevGovde")
        govde_layout = QtWidgets.QHBoxLayout(govde)
        govde_layout.setContentsMargins(14, 5, 12, 5)
        govde_layout.setSpacing(10)

        govde_layout.addLayout(self._metin_alani_olustur(), 1)
        govde_layout.addWidget(self._tarih_paneli_olustur(), 0, QtCore.Qt.AlignmentFlag.AlignVCenter)
        govde_layout.addWidget(self._buton_paneli_olustur(), 0, QtCore.Qt.AlignmentFlag.AlignVCenter)
        return govde

    def _metin_alani_olustur(self):
        metin = QtWidgets.QVBoxLayout()
        metin.setContentsMargins(0, 0, 0, 0)
        metin.setSpacing(1)

        self.lbl_baslik = QtWidgets.QLabel(self.gorev.baslik)
        self.lbl_aciklama = QtWidgets.QLabel(self._kisa_aciklama())
        self.lbl_aciklama.setVisible(bool(self.gorev.aciklama))

        self.btn_aciklama = QtWidgets.QPushButton()
        self.btn_aciklama.setFixedSize(30, 24)
        self.btn_aciklama.setVisible(len(self.gorev.aciklama) > 80)
        aciklama_icon_path = os.path.join(os.path.dirname(__file__), "img", "icons", "aciklama.svg")
        self.btn_aciklama.setIcon(QtGui.QIcon(aciklama_icon_path))
        self.btn_aciklama.setIconSize(QtCore.QSize(18, 18))
        self.btn_aciklama.setToolTip("Açıklamayı görüntüle")
        self.btn_aciklama.clicked.connect(self._aciklama_goster)

        aciklama_satiri = QtWidgets.QHBoxLayout()
        aciklama_satiri.setContentsMargins(0, 0, 0, 0)
        aciklama_satiri.setSpacing(4)
        aciklama_satiri.addWidget(self.lbl_aciklama, 1)
        aciklama_satiri.addWidget(self.btn_aciklama, 0)

        metin.addWidget(self.lbl_baslik)
        metin.addLayout(aciklama_satiri)
        metin.addStretch()
        return metin

    def _tarih_paneli_olustur(self):
        self.tarih_panel = QtWidgets.QFrame()
        tarih_layout = QtWidgets.QVBoxLayout(self.tarih_panel)
        tarih_layout.setContentsMargins(8, 3, 8, 3)
        tarih_layout.setSpacing(1)

        self.lbl_tarih_baslik = QtWidgets.QLabel("Son Tarih")
        self.lbl_tarih = QtWidgets.QLabel(self._son_tarih_gun())
        self.lbl_saat = QtWidgets.QLabel(self._son_tarih_saat())

        tarih_layout.addWidget(self.lbl_tarih_baslik)
        tarih_layout.addWidget(self.lbl_tarih)
        tarih_layout.addWidget(self.lbl_saat)
        self.tarih_panel.setVisible(bool(self.gorev.bitis_tarihi))
        return self.tarih_panel

    def _buton_paneli_olustur(self):
        buton_panel = QtWidgets.QFrame()
        buton_panel.setFixedWidth(34)
        buton_layout = QtWidgets.QVBoxLayout(buton_panel)
        buton_layout.setContentsMargins(0, 0, 0, 0)
        buton_layout.setSpacing(2)

        self.btn_duzenle = QtWidgets.QPushButton()
        self.btn_duzenle.setFixedSize(32, 28)
        self.btn_duzenle.setIcon(QtGui.QIcon(os.path.join(os.path.dirname(__file__), "img", "icons", "duzenle.svg")))
        self.btn_duzenle.setIconSize(QtCore.QSize(24, 24))
        self.btn_duzenle.clicked.connect(lambda: self.duzenle_istendi.emit(self.gorev))

        self.btn_sil = QtWidgets.QPushButton("×")
        self.btn_sil.setFixedSize(32, 34)
        self.btn_sil.clicked.connect(lambda: self.sil_istendi.emit(self.gorev))

        buton_layout.addWidget(self.btn_duzenle, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        buton_layout.addWidget(self.btn_sil, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        return buton_panel

    def _stili_uygula(self):
        renk = self._oncelik_rengi()
        baslik_renk = self.tema.tamamlandi_rengi if self.gorev.tamamlandi else self.tema.metin_rengi
        self._kart_stilini_uygula(renk)
        self._metin_stilini_uygula(renk, baslik_renk)
        self._buton_stilini_uygula()
        self._overlay_stilini_uygula()
        self.update()

    def _kart_stilini_uygula(self, renk):
        self.setStyleSheet("""
            QFrame#gorevKarti { background:#edf2f7; border-radius:10px; }
            QFrame#gorevGovde { background:white; border:1px solid #d8e0ea; border-top-right-radius:10px; border-bottom-right-radius:10px; }
        """)
        self.sol_panel.setStyleSheet(f"background:{renk}; border-top-left-radius:10px; border-bottom-left-radius:10px;")
        self._durum_ikonunu_ayarla()

    def _metin_stilini_uygula(self, renk, baslik_renk):
        self.lbl_oncelik.setText(self._oncelik_dikey_metni())
        self.lbl_baslik.setStyleSheet(f"color:{baslik_renk}; font-size:11pt; font-weight:700;")
        self.lbl_aciklama.setStyleSheet("color:#64748b; font-size:9pt;")
        self.lbl_tarih_baslik.setStyleSheet("color:#64748b; font-size:8pt;")
        self.lbl_tarih.setStyleSheet("color:#334155; font-size:9pt; font-weight:700;")
        self.lbl_saat.setStyleSheet("color:#334155; font-size:9pt;")

    def _buton_stilini_uygula(self):
        self.btn_duzenle.setStyleSheet("QPushButton{background:transparent;border:none;color:#94a3b8;font-size:18px;} QPushButton:hover{color:#2563eb;}")
        self.btn_sil.setStyleSheet("QPushButton{background:transparent;border:none;color:#94a3b8;font-size:32px;font-weight:700;} QPushButton:hover{color:#ef4444;}")
        self.btn_duzenle.setStyleSheet("QPushButton{background:transparent;border:none;}")
        self.btn_aciklama.setStyleSheet("QPushButton{background:#f1f5f9;border:none;border-radius:8px;color:#475569;font-size:8pt;font-weight:700;} QPushButton:hover{background:#e2e8f0;}")

    def _overlay_stilini_uygula(self):
        self.lbl_overlay.setGeometry(self.rect())
        metin, renk = self._overlay_bilgisi()
        self.lbl_overlay.setText(metin)
        self.lbl_overlay.setStyleSheet(f"background:transparent; color:{renk}; font-family:'Segoe UI'; font-size:19pt; font-weight:800;")
        self.lbl_overlay.setVisible(bool(metin))
        self.lbl_overlay.raise_()

    def _durum_ikonunu_ayarla(self):
        self.btn_durum.setIcon(QtGui.QIcon())
        self.btn_durum.setStyleSheet("QPushButton{background:transparent;border:none;color:white;font-size:28px;font-weight:800;padding:0px;} QPushButton:hover{background:rgba(255,255,255,40);border-radius:6px;}")

        if self.gorev.iptal_edildi:
            self.btn_durum.setText("✖")
            return
        if self.gorev.tamamlandi:
            self.btn_durum.setText("✔")
            return
        if self.gorev.suresi_gecti_mi():
            icon_path = os.path.join(os.path.dirname(__file__), "img", "icons", "Un3.svg")
            self.btn_durum.setText("")
            self.btn_durum.setIcon(QtGui.QIcon(icon_path))
            self.btn_durum.setIconSize(QtCore.QSize(36, 36))
            return

        self.btn_durum.setText("⌛")

    def _durum_butonu_tiklandi(self):
        if self.gorev.iptal_edildi:
            self.gorev.iptal_edildi = False
            self.gorev.iptal_zamani = None
            self.gorev.tamamlandi = False
            self.gorev.tamamlanma_zamani = None
        else:
            self.gorev.tamamlandi = not self.gorev.tamamlandi
        self._stili_uygula()
        self.durum_degisti.emit(self.gorev, self.gorev.tamamlandi)

    def _aciklama_goster(self):
        dialog = self._aciklama_dialogu_olustur()
        dialog.exec()

    def _aciklama_dialogu_olustur(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Açıklamanın Tamamı")
        dialog.setModal(True)
        dialog.setFixedSize(420, 240)

        layout = QtWidgets.QVBoxLayout(dialog)
        layout.setContentsMargins(16, 14, 16, 14)

        baslik = QtWidgets.QLabel(self.gorev.baslik)
        baslik.setStyleSheet("font-size:13pt;font-weight:700;color:#1f2937;")
        baslik.setWordWrap(True)
        layout.addWidget(baslik)

        metin = QtWidgets.QTextEdit()
        metin.setReadOnly(True)
        metin.setPlainText(self.gorev.aciklama)
        metin.setStyleSheet("font-size:12pt; color:#334155; border:1px solid #e2e8f0; border-radius:8px; padding:8px; background:white;")

        btn = QtWidgets.QPushButton("Kapat")
        btn.clicked.connect(dialog.accept)
        layout.addWidget(metin, 1)
        layout.addWidget(btn, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        return dialog

    def _kisa_aciklama(self):
        return self.gorev.aciklama if len(self.gorev.aciklama) <= 80 else self.gorev.aciklama[:80].rstrip() + "..."

    def _overlay_bilgisi(self):
        if self.gorev.iptal_edildi:
            return "\u0130PTAL ED\u0130LD\u0130", "rgba(71,85,105,128)"
        if self.gorev.tamamlandi:
            return "TAMAMLANDI", "rgba(22,163,74,128)"
        if self.gorev.suresi_gecti_mi():
            return "S\u00dcRES\u0130 GE\u00c7T\u0130", "rgba(220,38,38,128)"
        return "", "transparent"

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.lbl_overlay.setGeometry(self.rect())
        metin, renk = self._overlay_bilgisi()
        self.lbl_overlay.setText(metin)
        self.lbl_overlay.setStyleSheet(f"background:transparent; color:{renk}; font-family:'Segoe UI'; font-size:19pt; font-weight:800;")
        self.lbl_overlay.setVisible(bool(metin))
        self.lbl_overlay.raise_()
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.gorev.iptal_edildi or not self.gorev.tamamlandi:
            return
        painter = QtGui.QPainter(self)
        painter.setOpacity(0.50)
        painter.setPen(QtGui.QColor("#111827"))
        font = painter.font()
        font.setPointSize(24)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(self.rect(), QtCore.Qt.AlignmentFlag.AlignCenter, "TAMAMLANDI")
        painter.end()

    def _oncelik_dikey_metni(self):
        return self._oncelik_metni().replace(" Öncelik", "").strip().upper()

    def _oncelik_metni(self):
        return f"{priority_name(self.settings, self.gorev.oncelik)} Öncelik"

    def _oncelik_rengi(self):
        return priority_color(self.settings, self.gorev.oncelik)

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
    layout.addWidget(GorevKarti(GorevModeli("Yüksek öncelikli görev", "Bu görev açıklamasının ilk satırı kartta görünür; devamı için ikon kullanılır.", GorevOnceligi.YUKSEK, False, bitis_tarihi=datetime.now() + timedelta(hours=2))))
    layout.addWidget(GorevKarti(GorevModeli("Normal görev", "Kısa açıklama.", GorevOnceligi.NORMAL, False, bitis_tarihi=datetime.now() + timedelta(days=1))))
    layout.addStretch()
    pencere.show()
    sys.exit(app.exec())
