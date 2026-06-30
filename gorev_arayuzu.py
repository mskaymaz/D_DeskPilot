from datetime import datetime

try:
    from PySide6 import QtCore, QtWidgets
except ImportError:
    from PyQt6 import QtCore, QtWidgets

from gorev_servisi import GorevServisi
from gorev_modeli import GorevModeli, GorevOnceligi
from gorev_karti import GorevKarti


class GorevArayuzuDialog(QtWidgets.QDialog):
    def __init__(self, servis: GorevServisi, parent=None):
        super().__init__(parent)
        self.servis = servis
        self.setWindowTitle("Görevlerim")
        self.setFixedSize(540, 600)
        self._arayuz_kur()
        self.verileri_yukle()

    def _arayuz_kur(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)

        ekle_grubu = QtWidgets.QGroupBox("Yeni Görev Ekle")
        ekle_layout = QtWidgets.QGridLayout(ekle_grubu)
        ekle_layout.setHorizontalSpacing(8)
        ekle_layout.setVerticalSpacing(6)

        self.txt_yeni_gorev = QtWidgets.QLineEdit()
        self.txt_yeni_gorev.setPlaceholderText("Görev başlığı...")

        self.txt_aciklama = QtWidgets.QLineEdit()
        self.txt_aciklama.setPlaceholderText("Açıklama...")

        self.cmb_oncelik = QtWidgets.QComboBox()
        self.cmb_oncelik.addItem("Düşük", GorevOnceligi.DUSUK)
        self.cmb_oncelik.addItem("Normal", GorevOnceligi.NORMAL)
        self.cmb_oncelik.addItem("Yüksek", GorevOnceligi.YUKSEK)
        self.cmb_oncelik.setCurrentIndex(1)

        self.dt_son_tarih = QtWidgets.QDateTimeEdit()
        self.dt_son_tarih.setCalendarPopup(True)
        self.dt_son_tarih.setDisplayFormat("dd.MM.yyyy HH:mm")
        self.dt_son_tarih.setDateTime(QtCore.QDateTime.currentDateTime())

        self.chk_son_tarih = QtWidgets.QCheckBox("Son tarih kullan")
        self.chk_son_tarih.toggled.connect(self.dt_son_tarih.setEnabled)
        self.dt_son_tarih.setEnabled(False)

        self.btn_ekle = QtWidgets.QPushButton("Ekle")
        self.btn_ekle.clicked.connect(self.gorev_ekle)

        ekle_layout.addWidget(self.txt_yeni_gorev, 0, 0, 1, 3)
        ekle_layout.addWidget(self.txt_aciklama, 1, 0, 1, 3)
        ekle_layout.addWidget(self.cmb_oncelik, 2, 0)
        ekle_layout.addWidget(self.chk_son_tarih, 2, 1)
        ekle_layout.addWidget(self.dt_son_tarih, 2, 2)
        ekle_layout.addWidget(self.btn_ekle, 3, 2)

        layout.addWidget(ekle_grubu)

        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop)
        self.scroll.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)

        self.liste_kapsayici = QtWidgets.QWidget()
        self.liste_kapsayici.setFixedWidth(520)
        self.liste_layout = QtWidgets.QVBoxLayout(self.liste_kapsayici)
        self.liste_layout.setContentsMargins(2, 2, 2, 2)
        self.liste_layout.setSpacing(5)
        self.liste_layout.addStretch()

        self.scroll.setWidget(self.liste_kapsayici)
        layout.addWidget(self.scroll, 1)

        alt_layout = QtWidgets.QHBoxLayout()
        self.btn_kapat = QtWidgets.QPushButton("Kapat")
        self.btn_kapat.clicked.connect(self.accept)
        alt_layout.addStretch()
        alt_layout.addWidget(self.btn_kapat)
        layout.addLayout(alt_layout)

        self.setStyleSheet("""
            QDialog { background:#f8fafc; }
            QGroupBox { font-weight:600; border:1px solid #e2e8f0; border-radius:10px; margin-top:8px; padding:10px; background:white; }
            QGroupBox::title { subcontrol-origin: margin; left:12px; padding:0 4px; color:#334155; }
            QLineEdit, QComboBox, QDateTimeEdit { padding:7px; border:1px solid #cbd5e1; border-radius:7px; background:white; }
            QPushButton { padding:7px 12px; border:none; border-radius:7px; background:#e2e8f0; color:#334155; font-weight:600; }
            QPushButton:hover { background:#cbd5e1; }
        """)
        self.btn_ekle.setStyleSheet("background:#22c55e; color:white;")
        self._popup_katmanlarini_duzelt()

    def _oncelik_index(self, oncelik):
        for i in range(self.cmb_oncelik.count()):
            if self.cmb_oncelik.itemData(i) == oncelik:
                return i
        return 1

    def _gorev_form_dialogu(self, gorev):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("G??revi D??zenle")
        dialog.setModal(True)
        dialog.setFixedWidth(500)

        layout = QtWidgets.QGridLayout(dialog)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setHorizontalSpacing(8)
        layout.setVerticalSpacing(8)

        txt_baslik = QtWidgets.QLineEdit(gorev.baslik)
        txt_aciklama = QtWidgets.QTextEdit()
        txt_aciklama.setPlainText(gorev.aciklama)
        txt_aciklama.setFixedHeight(110)

        cmb_oncelik = QtWidgets.QComboBox()
        cmb_oncelik.addItem("D??????k", GorevOnceligi.DUSUK)
        cmb_oncelik.addItem("Normal", GorevOnceligi.NORMAL)
        cmb_oncelik.addItem("Y??ksek", GorevOnceligi.YUKSEK)
        for i in range(cmb_oncelik.count()):
            if cmb_oncelik.itemData(i) == gorev.oncelik:
                cmb_oncelik.setCurrentIndex(i)

        cmb_durum = QtWidgets.QComboBox()
        cmb_durum.addItem("Aktif", "active")
        cmb_durum.addItem("Tamamland??", "completed")
        cmb_durum.addItem("??ptal Edildi", "cancelled")
        cmb_durum.setCurrentIndex(2 if gorev.iptal_edildi else 1 if gorev.tamamlandi else 0)

        chk_tarih = QtWidgets.QCheckBox("Son tarih kullan")
        dt_tarih = QtWidgets.QDateTimeEdit()
        dt_tarih.setCalendarPopup(True)
        dt_tarih.setDisplayFormat("dd.MM.yyyy HH:mm")
        dt_tarih.setDateTime(QtCore.QDateTime(gorev.bitis_tarihi) if gorev.bitis_tarihi else QtCore.QDateTime.currentDateTime())
        chk_tarih.setChecked(bool(gorev.bitis_tarihi))
        dt_tarih.setEnabled(bool(gorev.bitis_tarihi))
        chk_tarih.toggled.connect(dt_tarih.setEnabled)

        btn_kaydet = QtWidgets.QPushButton("Kaydet")
        btn_iptal = QtWidgets.QPushButton("Vazge??")
        btn_kaydet.clicked.connect(dialog.accept)
        btn_iptal.clicked.connect(dialog.reject)

        layout.addWidget(QtWidgets.QLabel("Ba??l??k"), 0, 0)
        layout.addWidget(txt_baslik, 0, 1, 1, 2)
        layout.addWidget(QtWidgets.QLabel("A????klama"), 1, 0)
        layout.addWidget(txt_aciklama, 1, 1, 1, 2)
        layout.addWidget(QtWidgets.QLabel("??ncelik"), 2, 0)
        layout.addWidget(cmb_oncelik, 2, 1, 1, 2)
        layout.addWidget(QtWidgets.QLabel("Durum"), 3, 0)
        layout.addWidget(cmb_durum, 3, 1, 1, 2)
        layout.addWidget(chk_tarih, 4, 0)
        layout.addWidget(dt_tarih, 4, 1, 1, 2)
        layout.addWidget(btn_iptal, 5, 1)
        layout.addWidget(btn_kaydet, 5, 2)

        dialog.setStyleSheet(self.styleSheet())
        if dialog.exec() != QtWidgets.QDialog.DialogCode.Accepted:
            return False

        baslik = txt_baslik.text().strip()
        if not baslik:
            return False

        durum = cmb_durum.currentData()
        gorev.baslik = baslik
        gorev.aciklama = txt_aciklama.toPlainText().strip()
        gorev.oncelik = cmb_oncelik.currentData()
        gorev.bitis_tarihi = dt_tarih.dateTime().toPython() if chk_tarih.isChecked() else None
        gorev.tamamlandi = durum == "completed"
        gorev.iptal_edildi = durum == "cancelled"
        gorev.tamamlanma_zamani = datetime.now() if gorev.tamamlandi and not gorev.tamamlanma_zamani else None if not gorev.tamamlandi else gorev.tamamlanma_zamani
        gorev.iptal_zamani = datetime.now() if gorev.iptal_edildi and not gorev.iptal_zamani else None if not gorev.iptal_edildi else gorev.iptal_zamani
        return True

    def _popup_katmanlarini_duzelt(self, kok=None):
        kok = kok or self
        popup_flag = QtCore.Qt.WindowType.WindowStaysOnTopHint
        for c in kok.findChildren(QtWidgets.QComboBox): c.view().window().setWindowFlag(popup_flag,True)
        for d in kok.findChildren(QtWidgets.QDateTimeEdit):
            cal=d.calendarWidget()
            if cal: cal.window().setWindowFlag(popup_flag,True)
    def verileri_yukle(self):
        scroll_degeri = self.scroll.verticalScrollBar().value()
        while self.liste_layout.count() > 1:
            item = self.liste_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        for gorev in self.servis.gorevleri_sirali_al():
            kart = GorevKarti(gorev)
            kart.durum_degisti.connect(self.durum_degistir)
            kart.sil_istendi.connect(self.gorev_sil)
            kart.duzenle_istendi.connect(self.gorev_duzenle)
            self.liste_layout.insertWidget(self.liste_layout.count() - 1, kart, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)

        QtCore.QTimer.singleShot(0, lambda: self.scroll.verticalScrollBar().setValue(scroll_degeri))

    def gorev_ekle(self):
        baslik = self.txt_yeni_gorev.text().strip()
        if not baslik:
            return

        bitis_tarihi = None
        if self.chk_son_tarih.isChecked():
            bitis_tarihi = self.dt_son_tarih.dateTime().toPython()

        self.servis.gorev_ekle(GorevModeli(
            baslik=baslik,
            aciklama=self.txt_aciklama.text().strip(),
            oncelik=self.cmb_oncelik.currentData(),
            bitis_tarihi=bitis_tarihi
        ))

        self.txt_yeni_gorev.clear()
        self.txt_aciklama.clear()
        self.chk_son_tarih.setChecked(False)
        self.verileri_yukle()

    def durum_degistir(self, gorev, durum):
        gorev.tamamlandi = durum
        gorev.tamamlanma_zamani = datetime.now() if durum else None
        self.servis.kaydet()
        self.verileri_yukle()

    def gorev_duzenle(self, gorev):
        if self._gorev_form_dialogu(gorev):
            self.servis.kaydet()
            self.verileri_yukle()

    def gorev_sil(self, gorev):
        gorev.iptal_edildi = True
        gorev.tamamlandi = False
        gorev.tamamlanma_zamani = None
        gorev.iptal_zamani = datetime.now()
        self.servis.kaydet()
        self.verileri_yukle()



