from datetime import datetime

try:
    from PySide6 import QtCore, QtWidgets
except ImportError:
    from PyQt6 import QtCore, QtWidgets

from gorev_servisi import GorevServisi
from gorev_modeli import GorevModeli, GorevOnceligi
from gorev_karti import GorevKarti
from oncelik_yonetimi import priority_key, task_priorities
from dil_yonetimi import t, is_rtl
from todo_form_dialogs import (
    ekleme_formu_olustur,
    gorev_form_dialogu,
    yapilacak_listesi_duzenle,
    yeni_gorev_paneli_ac,
    yeni_yapilacak_listesi_ac,
)
from todo_filters import filtrelenmis_gorevleri_al, todo_ayar_degeri
from todo_icons import SETTINGS_ICON_PATH, svg_icon
from todo_settings_dialog import todo_ayarlarini_ac
from todo_widgets import KaliciComboBox


class GorevArayuzuDialog(QtWidgets.QDialog):
    def __init__(self, servis: GorevServisi, parent=None):
        super().__init__(parent)
        self.servis = servis
        self.settings = getattr(parent, "settings", None)
        self.language = getattr(self.settings, "language", "tr")
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft if is_rtl(self.language) else QtCore.Qt.LayoutDirection.LeftToRight)
        self.setWindowTitle(self._tr("todo.title", "Görevlerim"))
        self.setFixedSize(540, 600)
        self._arayuz_kur()
        self.verileri_yukle()

    def _tr(self, key, fallback=None):
        return t(key, self.language, fallback)

    def _arayuz_kur(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)

        layout.addLayout(self._ust_butonlari_olustur())
        layout.addWidget(self._liste_alani_olustur(), 1)
        layout.addLayout(self._alt_butonlari_olustur())

        self._stili_uygula()
        self._popup_katmanlarini_duzelt()

    def _ust_butonlari_olustur(self):
        ust_layout = QtWidgets.QHBoxLayout()
        self.btn_yeni_gorev = QtWidgets.QPushButton(self._tr("todo.add.button", "+ Yeni Görev"), self)
        self.btn_yeni_gorev.clicked.connect(self.yeni_gorev_paneli_ac)
        ust_layout.addWidget(self.btn_yeni_gorev)
        ust_layout.addStretch()
        self.cmb_liste_filtresi = KaliciComboBox(self)
        self.cmb_liste_filtresi.setFixedWidth(150)
        self._liste_filtresi_doldur()
        self.cmb_liste_filtresi.currentIndexChanged.connect(self.verileri_yukle)
        ust_layout.addWidget(self.cmb_liste_filtresi)
        self.btn_todo_ayarlar = QtWidgets.QPushButton(self)
        self.btn_todo_ayarlar.setIcon(svg_icon(SETTINGS_ICON_PATH, 22))
        self.btn_todo_ayarlar.setIconSize(QtCore.QSize(22, 22))
        self.btn_todo_ayarlar.setToolTip("Görevlerim ayarları")
        self.btn_todo_ayarlar.setFixedSize(34, 34)
        self.btn_todo_ayarlar.clicked.connect(self.todo_ayarlarini_ac)
        ust_layout.addWidget(self.btn_todo_ayarlar)
        return ust_layout

    def _liste_filtresi_doldur(self):
        secenekler = [
            ("all", self._tr("todo.filter.all", "Tümü")),
            ("date", self._tr("todo.filter.date", "Tarihe göre (tümü)")),
            ("today", self._tr("todo.filter.today", "Bugün")),
            ("tomorrow", self._tr("todo.filter.tomorrow", "Yarın")),
            ("week", self._tr("todo.filter.week", "Bu hafta")),
            ("no_date", self._tr("todo.filter.no_date", "Tarihsiz görevler")),
            ("overdue", self._tr("todo.filter.overdue", "Süresi geçenler")),
            ("completed", self._tr("todo.filter.completed", "Tamamlananlar")),
            ("cancelled", self._tr("todo.filter.cancelled", "İptal edilenler")),
            ("trash", self._tr("todo.filter.trash", "Çöp Kutusu")),
        ]
        for key, text in secenekler:
            self.cmb_liste_filtresi.addItem(text, key)

    def _tarih_saat_widget_olustur(self, checked=False, tarih_saat=None, label=None, parent=None):
        parent = parent or self
        kapsayici = QtWidgets.QWidget(parent)
        satir = QtWidgets.QHBoxLayout(kapsayici)
        satir.setContentsMargins(0, 0, 0, 0)
        satir.setSpacing(4)

        chk = QtWidgets.QCheckBox(label or self._tr("todo.date.add", "Tarih/Saat Ekle"), kapsayici)
        dt = QtWidgets.QDateTimeEdit(kapsayici)
        dt.setCalendarPopup(True)
        dt.setDisplayFormat("dd.MM.yyyy")
        dt.setDateTime(QtCore.QDateTime(tarih_saat) if tarih_saat else QtCore.QDateTime.currentDateTime())

        txt_saat = QtWidgets.QLineEdit(QtCore.QDateTime(tarih_saat).time().toString("HH:mm") if tarih_saat else QtCore.QTime.currentTime().toString("HH:mm"), kapsayici)
        txt_saat.setInputMask("00:00")
        txt_saat.setFixedWidth(56)

        chk.setChecked(checked)
        dt.setEnabled(checked)
        txt_saat.setEnabled(checked)
        chk.toggled.connect(dt.setEnabled)
        chk.toggled.connect(txt_saat.setEnabled)

        satir.addWidget(chk)
        satir.addWidget(dt)
        satir.addWidget(txt_saat)
        satir.addStretch()
        return kapsayici, chk, dt, txt_saat

    def _tarih_saat_degeri(self, chk, dt, txt_saat):
        if not chk.isChecked():
            return None
        saat = QtCore.QTime.fromString(txt_saat.text(), "HH:mm")
        if not saat.isValid():
            return None
        return QtCore.QDateTime(dt.date(), saat).toPython()

    def _tarih_saat_gecerli_mi(self, chk, txt_saat):
        return not chk.isChecked() or QtCore.QTime.fromString(txt_saat.text(), "HH:mm").isValid()

    def _uyari_goster(self, parent, mesaj):
        QtWidgets.QMessageBox.warning(parent, self._tr("todo.warning.title", "Eksik bilgi"), mesaj)

    def _todo_ayar_degeri(self, alan, varsayilan):
        return todo_ayar_degeri(self.settings, alan, varsayilan)

    def todo_ayarlarini_ac(self):
        todo_ayarlarini_ac(self)

    def _ekleme_formu_olustur(self):
        return ekleme_formu_olustur(self)

    def _yeni_yapilacak_listesi_ac(self):
        yeni_yapilacak_listesi_ac(self)

    def yeni_gorev_paneli_ac(self):
        yeni_gorev_paneli_ac(self)

    def _liste_alani_olustur(self):
        self.scroll = QtWidgets.QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop)
        self.scroll.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)

        self.liste_kapsayici = QtWidgets.QWidget(self.scroll)
        self.liste_kapsayici.setFixedWidth(520)
        self.liste_layout = QtWidgets.QVBoxLayout(self.liste_kapsayici)
        self.liste_layout.setContentsMargins(2, 2, 2, 2)
        self.liste_layout.setSpacing(5)
        self.liste_layout.addStretch()

        self.scroll.setWidget(self.liste_kapsayici)
        return self.scroll

    def _alt_butonlari_olustur(self):
        alt_layout = QtWidgets.QHBoxLayout()
        self.btn_kapat = QtWidgets.QPushButton(self._tr("todo.close", "Kapat"), self)
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
        if hasattr(self, "btn_ekle"):
            self.btn_ekle.setStyleSheet("background:#22c55e; color:white;")
        if hasattr(self, "btn_yeni_gorev"):
            self.btn_yeni_gorev.setStyleSheet("background:#22c55e; color:white;")

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

    def _filtrelenmis_gorevleri_al(self):
        filtre = self.cmb_liste_filtresi.currentData() if hasattr(self, "cmb_liste_filtresi") else "all"
        return filtrelenmis_gorevleri_al(self.servis.gorevleri_sirali_al(), filtre, self.settings)

    def _gorev_form_dialogu(self, gorev):
        return gorev_form_dialogu(self, gorev)

    def _popup_katmanlarini_duzelt(self, kok=None):
        kok = kok or self
        popup_flag = QtCore.Qt.WindowType.WindowStaysOnTopHint
        for d in kok.findChildren(QtWidgets.QDateTimeEdit):
            cal=d.calendarWidget()
            if cal: cal.window().setWindowFlag(popup_flag,True)
    def verileri_yukle(self):
        self._cop_suresi_dolanlari_temizle()
        scroll_degeri = self.scroll.verticalScrollBar().value()
        self.setUpdatesEnabled(False)
        self.scroll.setUpdatesEnabled(False)
        self.scroll.viewport().setUpdatesEnabled(False)
        self.liste_kapsayici.setUpdatesEnabled(False)
        try:
            while self.liste_layout.count() > 1:
                item = self.liste_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.hide()
                    widget.deleteLater()

            for gorev in self._filtrelenmis_gorevleri_al():
                kart = self._gorev_karti_olustur(gorev)
                self.liste_layout.insertWidget(self.liste_layout.count() - 1, kart, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        finally:
            self.liste_kapsayici.setUpdatesEnabled(True)
            self.scroll.viewport().setUpdatesEnabled(True)
            self.scroll.setUpdatesEnabled(True)
            self.setUpdatesEnabled(True)

        def _yenilemeyi_bitir():
            self.scroll.verticalScrollBar().setValue(scroll_degeri)
            self.update()

        QtCore.QTimer.singleShot(0, _yenilemeyi_bitir)

    def _gorev_karti_olustur(self, gorev):
        kart = GorevKarti(gorev, settings=self.settings, parent=self.liste_kapsayici)
        kart.durum_degisti.connect(self.durum_degistir)
        kart.sil_istendi.connect(self.gorev_sil)
        kart.cope_istendi.connect(self.gorev_cope_tasi)
        kart.geri_yukle_istendi.connect(self.gorev_geri_yukle)
        kart.kalici_sil_istendi.connect(self.gorev_kalici_sil)
        kart.duzenle_istendi.connect(self.gorev_duzenle)
        kart.liste_istendi.connect(self.gorev_yapilacak_listesi_duzenle)
        return kart

    def _gorev_kartini_bul(self, gorev):
        for kart in self.liste_kapsayici.findChildren(GorevKarti):
            if kart.gorev is gorev:
                return kart
        return None

    def _listeyi_yeniden_sirala(self):
        self._cop_suresi_dolanlari_temizle()
        kartlar = {id(kart.gorev): kart for kart in self.liste_kapsayici.findChildren(GorevKarti)}
        self.setUpdatesEnabled(False)
        self.liste_kapsayici.setUpdatesEnabled(False)
        try:
            while self.liste_layout.count() > 1:
                item = self.liste_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.hide()

            for gorev in self._filtrelenmis_gorevleri_al():
                kart = kartlar.get(id(gorev)) or self._gorev_karti_olustur(gorev)
                kart.refresh()
                self.liste_layout.insertWidget(self.liste_layout.count() - 1, kart, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
                kart.show()
        finally:
            self.liste_kapsayici.setUpdatesEnabled(True)
            self.setUpdatesEnabled(True)
            self.update()

    def _cop_suresi_dolanlari_temizle(self):
        self.servis.cop_suresi_dolanlari_sil(self._todo_ayar_degeri("todo_trash_retention_days", 30))

    def gorev_ekle(self):
        baslik = self.txt_yeni_gorev.text().strip()
        if not baslik:
            self._uyari_goster(getattr(self, "_aktif_yeni_gorev_dialogu", self), self._tr("todo.warning.title_required", "Görev başlığı boş bırakılamaz."))
            self.txt_yeni_gorev.setFocus()
            return
        if not self._tarih_saat_gecerli_mi(self.chk_son_tarih, self.txt_son_saat):
            self._uyari_goster(getattr(self, "_aktif_yeni_gorev_dialogu", self), self._tr("todo.warning.invalid_time", "Saat 00:00 - 23:59 aralığında olmalıdır."))
            self.txt_son_saat.setFocus()
            return

        self.servis.gorev_ekle(GorevModeli(
            baslik=baslik,
            aciklama=self.txt_aciklama.toPlainText().strip(),
            yapilacaklar=list(getattr(self, "_yeni_yapilacaklar", [])),
            oncelik=self.cmb_oncelik.currentData(),
            bitis_tarihi=self._tarih_saat_degeri(self.chk_son_tarih, self.dt_son_tarih, self.txt_son_saat)
        ))

        self.verileri_yukle()
        dialog = getattr(self, "_aktif_yeni_gorev_dialogu", None)
        if dialog:
            dialog.accept()

    def durum_degistir(self, gorev, durum):
        gorev.tamamlandi = durum
        gorev.tamamlanma_zamani = datetime.now() if durum else None
        self.servis.kaydet()
        self._listeyi_yeniden_sirala()

    def gorev_duzenle(self, gorev):
        if self._gorev_form_dialogu(gorev):
            self.servis.kaydet()
            self._listeyi_yeniden_sirala()

    def gorev_yapilacak_listesi_duzenle(self, gorev):
        maddeler = yapilacak_listesi_duzenle(self, self, gorev.yapilacaklar)
        if maddeler is None:
            return
        gorev.yapilacaklar = maddeler
        self.servis.kaydet()
        self._listeyi_yeniden_sirala()

    def gorev_sil(self, gorev):
        gorev.iptal_edildi = True
        gorev.tamamlandi = False
        gorev.tamamlanma_zamani = None
        gorev.iptal_zamani = datetime.now()
        self.servis.kaydet()
        self._listeyi_yeniden_sirala()

    def gorev_cope_tasi(self, gorev):
        cevap = QtWidgets.QMessageBox.question(
            self,
            self._tr("todo.trash.move.title", "Çöp Kutusuna Taşı"),
            self._tr("todo.trash.move.message", "Bu görev çöp kutusuna taşınsın mı?"),
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
            QtWidgets.QMessageBox.StandardButton.No,
        )
        if cevap != QtWidgets.QMessageBox.StandardButton.Yes:
            return
        self.servis.cope_tasi(gorev)
        self._listeyi_yeniden_sirala()

    def gorev_geri_yukle(self, gorev):
        self.servis.copten_geri_yukle(gorev)
        self._listeyi_yeniden_sirala()

    def gorev_kalici_sil(self, gorev):
        ilk_cevap = QtWidgets.QMessageBox.question(
            self,
            self._tr("todo.trash.delete.title", "Kalıcı Sil"),
            self._tr("todo.trash.delete.message", "Bu görev kalıcı olarak silinsin mi?"),
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
            QtWidgets.QMessageBox.StandardButton.No,
        )
        if ilk_cevap != QtWidgets.QMessageBox.StandardButton.Yes:
            return
        ikinci_cevap = QtWidgets.QMessageBox.question(
            self,
            self._tr("todo.trash.delete.confirm.title", "Son Onay"),
            self._tr("todo.trash.delete.confirm.message", "Bu işlem geri alınamaz. Emin misiniz?"),
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
            QtWidgets.QMessageBox.StandardButton.No,
        )
        if ikinci_cevap != QtWidgets.QMessageBox.StandardButton.Yes:
            return
        self.servis.kalici_sil(gorev)
        self._listeyi_yeniden_sirala()



