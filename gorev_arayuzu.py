from datetime import datetime

try:
    from PySide6 import QtCore, QtWidgets
except ImportError:
    from PyQt6 import QtCore, QtWidgets

from gorev_servisi import GorevServisi
from gorev_modeli import GorevModeli, GorevOnceligi
from gorev_karti import GorevKarti
from oncelik_yonetimi import priority_key, task_priorities


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
            action = menu.addAction(self.itemText(i)); action.setData(i)
        secim = menu.exec(self.mapToGlobal(QtCore.QPoint(0, self.height())))
        if secim is not None and secim.data() is not None: self.setCurrentIndex(int(secim.data()))
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton: self.showPopup(); event.accept(); return
        super().mousePressEvent(event)
    def wheelEvent(self, event):
        event.ignore()


class GorevArayuzuDialog(QtWidgets.QDialog):
    def __init__(self, servis: GorevServisi, parent=None):
        super().__init__(parent)
        self.servis = servis
        self.settings = getattr(parent, "settings", None)
        self.setWindowTitle("Görevlerim")
        self.setFixedSize(540, 600)
        self._arayuz_kur()
        self.verileri_yukle()

    def _arayuz_kur(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)

        layout.addWidget(self._ekleme_formu_olustur())
        layout.addWidget(self._liste_alani_olustur(), 1)
        layout.addLayout(self._alt_butonlari_olustur())

        self._stili_uygula()
        self._popup_katmanlarini_duzelt()

    def _ekleme_formu_olustur(self):
        ekle_grubu = QtWidgets.QGroupBox("Yeni Görev Ekle")
        ekle_layout = QtWidgets.QGridLayout(ekle_grubu)
        ekle_layout.setHorizontalSpacing(15)
        ekle_layout.setVerticalSpacing(4)
        ekle_layout.setContentsMargins(10, 8, 10, 8)

        self.txt_yeni_gorev = QtWidgets.QLineEdit()
        self.txt_yeni_gorev.setPlaceholderText("Görev başlığı...")

        self.txt_aciklama = QtWidgets.QTextEdit()
        self.txt_aciklama.setPlaceholderText("Açıklama...")
        self.txt_aciklama.setFixedHeight(56)

        self.cmb_oncelik = KaliciComboBox()
        self._oncelik_combo_doldur(self.cmb_oncelik, "normal")

        self.dt_son_tarih = QtWidgets.QDateTimeEdit()
        self.dt_son_tarih.setCalendarPopup(True)
        self.dt_son_tarih.setDisplayFormat("dd.MM.yyyy")
        self.dt_son_tarih.setDateTime(QtCore.QDateTime.currentDateTime())

        self.txt_son_saat = QtWidgets.QLineEdit(QtCore.QTime.currentTime().toString("HH:mm"))
        self.txt_son_saat.setInputMask("00:00")
        self.txt_son_saat.setFixedWidth(46)

        self.chk_son_tarih = QtWidgets.QCheckBox()
        self.chk_son_tarih.toggled.connect(self.dt_son_tarih.setEnabled)
        self.chk_son_tarih.toggled.connect(self.txt_son_saat.setEnabled)
        self.dt_son_tarih.setEnabled(False)
        self.txt_son_saat.setEnabled(False)

        tarih_secim_satiri = QtWidgets.QHBoxLayout()
        tarih_secim_satiri.setContentsMargins(0, 0, 0, 0)
        tarih_secim_satiri.setSpacing(4)
        tarih_secim_satiri.addWidget(QtWidgets.QLabel("Tarih/Saat Ekle"))
        tarih_secim_satiri.addWidget(self.chk_son_tarih)

        self.btn_ekle = QtWidgets.QPushButton("Ekle")
        self.btn_ekle.setFixedWidth(82)
        self.btn_ekle.clicked.connect(self.gorev_ekle)

        ekle_layout.addWidget(self.txt_yeni_gorev, 0, 0, 1, 5)
        ekle_layout.addWidget(self.txt_aciklama, 1, 0, 1, 5)
        ekle_layout.addWidget(self.cmb_oncelik, 2, 0)
        ekle_layout.addLayout(tarih_secim_satiri, 2, 1)
        ekle_layout.addWidget(self.dt_son_tarih, 2, 2)
        ekle_layout.addWidget(self.txt_son_saat, 2, 3)
        ekle_layout.addWidget(self.btn_ekle, 2, 4)
        return ekle_grubu

    def _liste_alani_olustur(self):
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
        return self.scroll

    def _alt_butonlari_olustur(self):
        alt_layout = QtWidgets.QHBoxLayout()
        self.btn_kapat = QtWidgets.QPushButton("Kapat")
        self.btn_kapat.clicked.connect(self.accept)
        alt_layout.addStretch()
        alt_layout.addWidget(self.btn_kapat)
        return alt_layout

    def _stili_uygula(self):
        self.setStyleSheet("""
            QDialog { background:#f8fafc; }
            QGroupBox { font-weight:600; border:1px solid #e2e8f0; border-radius:10px; margin-top:8px; padding:10px; background:white; }
            QGroupBox::title { subcontrol-origin: margin; left:12px; padding:0 4px; color:#334155; }
            QLineEdit, QComboBox, QDateTimeEdit { padding:7px; border:1px solid #cbd5e1; border-radius:7px; background:white; }
            QPushButton { padding:7px 12px; border:none; border-radius:7px; background:#e2e8f0; color:#334155; font-weight:600; }
            QPushButton:hover { background:#cbd5e1; }
        """)
        self.btn_ekle.setStyleSheet("background:#22c55e; color:white;")

    def _oncelik_combo_doldur(self, combo, selected=None):
        combo.clear()
        selected_key = priority_key(selected)
        selected_index = 0
        for i, item in enumerate(task_priorities(self.settings)):
            key = item.get("key", "normal")
            combo.addItem(item.get("name", key), key)
            if key == selected_key:
                selected_index = i
        combo.setCurrentIndex(selected_index)

    def _oncelik_index(self, oncelik):
        selected_key = priority_key(oncelik)
        for i in range(self.cmb_oncelik.count()):
            if priority_key(self.cmb_oncelik.itemData(i)) == selected_key:
                return i
        return 0

    def _gorev_form_dialogu(self, gorev):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Görevi Düzenle")
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

        cmb_oncelik = KaliciComboBox()
        self._oncelik_combo_doldur(cmb_oncelik, gorev.oncelik)

        cmb_durum = KaliciComboBox()
        cmb_durum.addItem("Aktif", "active")
        cmb_durum.addItem("Tamamlandı", "completed")
        cmb_durum.addItem("İptal Edildi", "cancelled")
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
        btn_iptal = QtWidgets.QPushButton("Vazgeç")
        btn_kaydet.clicked.connect(dialog.accept)
        btn_iptal.clicked.connect(dialog.reject)

        layout.addWidget(QtWidgets.QLabel("Başlık"), 0, 0)
        layout.addWidget(txt_baslik, 0, 1, 1, 2)
        layout.addWidget(QtWidgets.QLabel("Açıklama"), 1, 0)
        layout.addWidget(txt_aciklama, 1, 1, 1, 2)
        layout.addWidget(QtWidgets.QLabel("Öncelik"), 2, 0)
        layout.addWidget(cmb_oncelik, 2, 1, 1, 2)
        layout.addWidget(QtWidgets.QLabel("Durum"), 3, 0)
        layout.addWidget(cmb_durum, 3, 1, 1, 2)
        layout.addWidget(chk_tarih, 4, 0)
        layout.addWidget(dt_tarih, 4, 1, 1, 2)
        layout.addWidget(btn_iptal, 5, 1)
        layout.addWidget(btn_kaydet, 5, 2)

        dialog.setStyleSheet(self.styleSheet())
        self._popup_katmanlarini_duzelt(dialog)
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
            kart = GorevKarti(gorev, settings=self.settings)
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
            saat = QtCore.QTime.fromString(self.txt_son_saat.text(), "HH:mm")
            if not saat.isValid():
                saat = QtCore.QTime(0, 0)
            bitis_tarihi = QtCore.QDateTime(
                self.dt_son_tarih.date(),
                saat
            ).toPython()

        self.servis.gorev_ekle(GorevModeli(
            baslik=baslik,
            aciklama=self.txt_aciklama.toPlainText().strip(),
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



