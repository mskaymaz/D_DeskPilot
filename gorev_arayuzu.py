from datetime import datetime, timedelta

try:
    from PySide6 import QtCore, QtGui, QtWidgets
except ImportError:
    from PyQt6 import QtCore, QtGui, QtWidgets

from gorev_servisi import GorevServisi
from gorev_modeli import GorevModeli, GorevOnceligi
from gorev_karti import GorevKarti
from oncelik_yonetimi import default_task_priorities, priority_key, task_priorities
from dil_yonetimi import t, is_rtl
from core_settings import save_settings


LIST_ICON_PATH = (
    "M348.5-291.5Q360-303 360-320t-11.5-28.5Q337-360 320-360t-28.5 11.5Q280-337 280-320"
    "t11.5 28.5Q303-280 320-280t28.5-11.5Zm0-160Q360-463 360-480t-11.5-28.5Q337-520 320-520"
    "t-28.5 11.5Q280-497 280-480t11.5 28.5Q303-440 320-440t28.5-11.5Zm0-160Q360-623 360-640"
    "t-11.5-28.5Q337-680 320-680t-28.5 11.5Q280-657 280-640t11.5 28.5Q303-600 320-600"
    "t28.5-11.5ZM440-280h240v-80H440v80Zm0-160h240v-80H440v80Zm0-160h240v-80H440v80Z"
    "M200-120q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h560q33 0 56.5 23.5T840-760"
    "v560q0 33-23.5 56.5T760-120H200Zm0-80h560v-560H200v560Zm0-560v560-560Z"
)

SETTINGS_ICON_PATH = (
    "m370-80-16-128q-13-5-24.5-12T307-235l-119 50L78-375l103-78q-1-7-1-13.5v-27q0-6.5 1-13.5"
    "L78-585l110-190 119 50q11-8 23-15t24-12l16-128h220l16 128q13 5 24.5 12t22.5 15l119-50 110 190"
    "-103 78q1 7 1 13.5v27q0 6.5-2 13.5l103 78-110 190-118-50q-11 8-23 15t-24 12L590-80H370Z"
    "m70-80h79l14-106q31-8 57.5-23.5T639-327l99 41 39-68-86-65q5-14 7-29.5t2-31.5q0-16-2-31.5"
    "t-7-29.5l86-65-39-68-99 42q-22-23-48.5-38.5T533-694l-13-106h-79l-14 106q-31 8-57.5 23.5T321-633"
    "l-99-41-39 68 86 64q-5 15-7 30t-2 32q0 16 2 31t7 30l-86 65 39 68 99-42q22 23 48.5 38.5T427-266"
    "l13 106Zm42-180q58 0 99-41t41-99q0-58-41-99t-99-41q-59 0-99.5 41T342-480q0 58 40.5 99t99.5 41Z"
    "m-2-140Z"
)


def _svg_icon(path, size=24, color="#020617"):
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" height="{size}px" viewBox="0 -960 960 960" '
        f'width="{size}px" fill="{color}"><path d="{path}"/></svg>'
    )
    pixmap = QtGui.QPixmap(size, size)
    pixmap.loadFromData(svg.encode("utf-8"), "SVG")
    return QtGui.QIcon(pixmap)


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
        self.language = getattr(self.settings, "language", "tr")
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft if is_rtl(self.language) else QtCore.Qt.LayoutDirection.LeftToRight)
        self.setWindowTitle(self._tr("todo.title", "Görevlerim"))
        self.setFixedSize(540, 600)
        self.setWindowOpacity(0.0)
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
        self.btn_todo_ayarlar.setIcon(_svg_icon(SETTINGS_ICON_PATH, 22))
        self.btn_todo_ayarlar.setIconSize(QtCore.QSize(22, 22))
        self.btn_todo_ayarlar.setToolTip("Görevlerim ayarları")
        self.btn_todo_ayarlar.setFixedSize(34, 34)
        self.btn_todo_ayarlar.clicked.connect(self.todo_ayarlarini_ac)
        ust_layout.addWidget(self.btn_todo_ayarlar)
        return ust_layout

    def _liste_filtresi_doldur(self):
        secenekler = [
            ("all", self._tr("todo.filter.all", "Tümü")),
            ("date", self._tr("todo.filter.date", "Tarihe göre")),
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
        try:
            return max(0, int(getattr(self.settings, alan, varsayilan)))
        except (TypeError, ValueError):
            return varsayilan

    def _todo_ayarini_yaz(self, alan, deger):
        if self.settings is None:
            return
        setattr(self.settings, alan, int(deger))

    def todo_ayarlarini_ac(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Görevlerim Ayarları")
        dialog.setModal(True)
        dialog.setFixedWidth(540)

        layout = QtWidgets.QVBoxLayout(dialog)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(16)

        aciklama = QtWidgets.QLabel("Liste görünümü ve çöp kutusu saklama süresini buradan yönetebilirsiniz.", dialog)
        aciklama.setWordWrap(True)
        aciklama.setStyleSheet("color:#475569;font-size:11pt;")
        layout.addWidget(aciklama)

        form = QtWidgets.QFormLayout()
        form.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        form.setFormAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        form.setVerticalSpacing(16)

        spn_cop = self._gun_secici_olustur("Çöp kutusunda kalma süresi", self._todo_ayar_degeri("todo_trash_retention_days", 30), dialog)
        spn_tamamlanan = self._gun_secici_olustur("Tamamlananlar Tümü listesinde", self._todo_ayar_degeri("todo_completed_visible_days", 7), dialog)
        spn_iptal = self._gun_secici_olustur("İptal edilenler Tümü listesinde", self._todo_ayar_degeri("todo_cancelled_visible_days", 7), dialog)

        form.addRow("Silinen görevler", spn_cop)
        form.addRow("Tamamlanan görevler", spn_tamamlanan)
        form.addRow("İptal edilen görevler", spn_iptal)
        layout.addLayout(form)
        layout.addWidget(self._todo_oncelik_grubu_olustur(dialog))

        not_metni = QtWidgets.QLabel("0 gün seçilirse ilgili işlem hemen uygulanır. Özel filtrelerde kayıtlar ayrıca görüntülenebilir.", dialog)
        not_metni.setWordWrap(True)
        not_metni.setStyleSheet("color:#64748b;font-size:10pt;")
        layout.addWidget(not_metni)

        butonlar = QtWidgets.QHBoxLayout()
        btn_iptal = QtWidgets.QPushButton(self._tr("todo.cancel", "Vazgeç"), dialog)
        btn_kaydet = QtWidgets.QPushButton(self._tr("todo.edit.save", "Kaydet"), dialog)
        btn_iptal.clicked.connect(dialog.reject)
        btn_kaydet.clicked.connect(dialog.accept)
        butonlar.addStretch()
        butonlar.addWidget(btn_iptal)
        butonlar.addWidget(btn_kaydet)
        layout.addLayout(butonlar)

        dialog.setStyleSheet(self.styleSheet())
        dialog.setStyleSheet(dialog.styleSheet() + " QLabel{font-size:11pt;} QSpinBox{font-size:11pt; padding:7px;} ")
        self._popup_katmanlarini_duzelt(dialog)
        if dialog.exec() != QtWidgets.QDialog.DialogCode.Accepted:
            return

        self._todo_ayarini_yaz("todo_trash_retention_days", spn_cop.value())
        self._todo_ayarini_yaz("todo_completed_visible_days", spn_tamamlanan.value())
        self._todo_ayarini_yaz("todo_cancelled_visible_days", spn_iptal.value())
        if self.settings is not None:
            self._todo_oncelikleri_kaydet()
            save_settings(self.settings)
        self.verileri_yukle()

    def _gun_secici_olustur(self, tooltip, deger, parent):
        spin = QtWidgets.QSpinBox(parent)
        spin.setRange(0, 365)
        spin.setSuffix(" gün")
        spin.setValue(deger)
        spin.setToolTip(tooltip)
        spin.setFixedWidth(110)
        return spin

    def _todo_oncelik_grubu_olustur(self, parent):
        grup = QtWidgets.QGroupBox("Görev Öncelikleri", parent)
        layout = QtWidgets.QVBoxLayout(grup)
        layout.setSpacing(8)

        bilgi = QtWidgets.QLabel("Öncelik adlarını ve renklerini buradan düzenleyebilirsiniz. Ad sınırı: 7 karakter.", grup)
        bilgi.setWordWrap(True)
        bilgi.setStyleSheet("color:#475569;font-size:10pt;")
        layout.addWidget(bilgi)

        self.tbl_todo_oncelikler = QtWidgets.QTableWidget(0, 3, grup)
        self.tbl_todo_oncelikler.setHorizontalHeaderLabels(["Anahtar", "Ad", "Renk"])
        self.tbl_todo_oncelikler.horizontalHeader().setStretchLastSection(True)
        self.tbl_todo_oncelikler.verticalHeader().setVisible(False)
        self.tbl_todo_oncelikler.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tbl_todo_oncelikler.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tbl_todo_oncelikler.setFixedHeight(145)
        layout.addWidget(self.tbl_todo_oncelikler)

        butonlar = QtWidgets.QHBoxLayout()
        btn_ekle = QtWidgets.QPushButton("Ekle", grup)
        btn_sil = QtWidgets.QPushButton("Seçileni Sil", grup)
        btn_varsayilan = QtWidgets.QPushButton("Varsayılanlara Dön", grup)
        btn_ekle.clicked.connect(self._todo_oncelik_ekle)
        btn_sil.clicked.connect(self._todo_oncelik_sil)
        btn_varsayilan.clicked.connect(self._todo_oncelikleri_varsayilan)
        butonlar.addWidget(btn_ekle)
        butonlar.addWidget(btn_sil)
        butonlar.addStretch()
        butonlar.addWidget(btn_varsayilan)
        layout.addLayout(butonlar)

        self._todo_oncelikleri_yukle()
        return grup

    def _todo_oncelikleri_yukle(self):
        self.tbl_todo_oncelikler.setRowCount(0)
        for item in task_priorities(self.settings) or default_task_priorities():
            self._todo_oncelik_satiri_ekle(item.get("key", ""), item.get("name", ""), item.get("color", "#3b82f6"))

    def _todo_oncelik_satiri_ekle(self, key, name, color):
        row = self.tbl_todo_oncelikler.rowCount()
        self.tbl_todo_oncelikler.insertRow(row)
        key_item = QtWidgets.QTableWidgetItem(str(key))
        key_item.setFlags(key_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
        self.tbl_todo_oncelikler.setItem(row, 0, key_item)

        name_edit = QtWidgets.QLineEdit(str(name)[:7])
        name_edit.setMaxLength(7)
        self.tbl_todo_oncelikler.setCellWidget(row, 1, name_edit)

        color_btn = QtWidgets.QPushButton(str(color or "#3b82f6"))
        color_btn.clicked.connect(lambda _=None, b=color_btn: self._todo_oncelik_rengi_sec(b))
        self.tbl_todo_oncelikler.setCellWidget(row, 2, color_btn)

    def _todo_oncelik_sonraki_anahtar(self):
        mevcut = {self.tbl_todo_oncelikler.item(r, 0).text() for r in range(self.tbl_todo_oncelikler.rowCount())}
        i = 1
        while f"custom_{i}" in mevcut:
            i += 1
        return f"custom_{i}"

    def _todo_oncelik_ekle(self):
        self._todo_oncelik_satiri_ekle(self._todo_oncelik_sonraki_anahtar(), "Yeni", "#8b5cf6")

    def _todo_oncelik_sil(self):
        satirlar = sorted({i.row() for i in self.tbl_todo_oncelikler.selectedIndexes()}, reverse=True)
        korunan = {"low", "normal", "high"}
        for row in satirlar:
            item = self.tbl_todo_oncelikler.item(row, 0)
            if item and item.text() not in korunan:
                self.tbl_todo_oncelikler.removeRow(row)

    def _todo_oncelikleri_varsayilan(self):
        if self.settings is not None:
            self.settings.task_priorities = default_task_priorities()
        self._todo_oncelikleri_yukle()

    def _todo_oncelik_rengi_sec(self, btn):
        color = QtWidgets.QColorDialog.getColor(QtGui.QColor(btn.text()), self, "Renk Seç")
        if color.isValid():
            btn.setText(color.name())

    def _todo_oncelikleri_kaydet(self):
        items = []
        for row in range(self.tbl_todo_oncelikler.rowCount()):
            key_item = self.tbl_todo_oncelikler.item(row, 0)
            name_edit = self.tbl_todo_oncelikler.cellWidget(row, 1)
            color_btn = self.tbl_todo_oncelikler.cellWidget(row, 2)
            key = key_item.text().strip() if key_item else ""
            name = name_edit.text().strip() if name_edit else ""
            color = color_btn.text().strip() if color_btn else "#3b82f6"
            if key and name:
                items.append({"key": key, "name": name[:7], "color": color})
        self.settings.task_priorities = items or default_task_priorities()

    def _yapilacaklari_metne_cevir(self, maddeler):
        return "\n".join(str(madde).strip() for madde in (maddeler or []) if str(madde).strip())

    def _metni_yapilacaklara_cevir(self, metin):
        return [satir.strip() for satir in (metin or "").splitlines() if satir.strip()]

    def _yapilacak_listesi_duzenle(self, parent, maddeler):
        dialog = QtWidgets.QDialog(parent)
        dialog.setWindowTitle("Yapılacak Listesi")
        dialog.setModal(True)
        dialog.setFixedSize(420, 320)

        layout = QtWidgets.QVBoxLayout(dialog)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(8)

        txt_liste = QtWidgets.QTextEdit(dialog)
        txt_liste.setPlaceholderText("Her maddeyi ayrı satıra yazın...")
        txt_liste.setPlainText(self._yapilacaklari_metne_cevir(maddeler))
        layout.addWidget(txt_liste, 1)

        butonlar = QtWidgets.QHBoxLayout()
        btn_iptal = QtWidgets.QPushButton(self._tr("todo.cancel", "Vazgeç"), dialog)
        btn_kaydet = QtWidgets.QPushButton(self._tr("todo.edit.save", "Kaydet"), dialog)
        btn_iptal.clicked.connect(dialog.reject)
        btn_kaydet.clicked.connect(dialog.accept)
        butonlar.addStretch()
        butonlar.addWidget(btn_iptal)
        butonlar.addWidget(btn_kaydet)
        layout.addLayout(butonlar)

        dialog.setStyleSheet(self.styleSheet())
        self._popup_katmanlarini_duzelt(dialog)
        if dialog.exec() != QtWidgets.QDialog.DialogCode.Accepted:
            return None
        return self._metni_yapilacaklara_cevir(txt_liste.toPlainText())

    def _ekleme_formu_olustur(self):
        ekle_grubu = QtWidgets.QGroupBox(self._tr("todo.add.group", "Yeni Görev Ekle"), self)
        ekle_layout = QtWidgets.QGridLayout(ekle_grubu)
        ekle_layout.setHorizontalSpacing(15)
        ekle_layout.setVerticalSpacing(6)
        ekle_layout.setContentsMargins(10, 8, 10, 8)

        self.txt_yeni_gorev = QtWidgets.QLineEdit(ekle_grubu)
        self.txt_yeni_gorev.setPlaceholderText(self._tr("todo.add.placeholder.title", "Görev başlığı..."))

        self.txt_aciklama = QtWidgets.QTextEdit(ekle_grubu)
        self.txt_aciklama.setPlaceholderText(self._tr("todo.add.placeholder.description", "Açıklama..."))
        self.txt_aciklama.setFixedHeight(76)
        self._yeni_yapilacaklar = []

        self.cmb_oncelik = KaliciComboBox(ekle_grubu)
        self._oncelik_combo_doldur(self.cmb_oncelik, "normal")

        tarih_widget, self.chk_son_tarih, self.dt_son_tarih, self.txt_son_saat = self._tarih_saat_widget_olustur(False, None, parent=ekle_grubu)

        self.btn_ekle = QtWidgets.QPushButton(self._tr("todo.add.submit", "Ekle"), ekle_grubu)
        self.btn_ekle.setFixedWidth(82)
        self.btn_ekle.clicked.connect(self.gorev_ekle)

        self.btn_yeni_iptal = QtWidgets.QPushButton(self._tr("todo.cancel", "Vazgeç"), ekle_grubu)
        self.btn_yeni_iptal.setFixedWidth(82)
        self.btn_yeni_iptal.clicked.connect(lambda: getattr(self, "_aktif_yeni_gorev_dialogu", None).reject())

        self.btn_yeni_liste = QtWidgets.QPushButton(ekle_grubu)
        self.btn_yeni_liste.setIcon(_svg_icon(LIST_ICON_PATH, 22))
        self.btn_yeni_liste.setIconSize(QtCore.QSize(22, 22))
        self.btn_yeni_liste.setToolTip("Yapılacak listesi")
        self.btn_yeni_liste.setFixedWidth(42)
        self.btn_yeni_liste.clicked.connect(self._yeni_yapilacak_listesi_ac)

        ekle_layout.addWidget(self.txt_yeni_gorev, 0, 0, 1, 4)
        ekle_layout.addWidget(self.txt_aciklama, 1, 0, 1, 4)
        ekle_layout.addWidget(self.cmb_oncelik, 2, 0)
        ekle_layout.addWidget(tarih_widget, 2, 1, 1, 3)
        ekle_layout.addWidget(self.btn_yeni_liste, 3, 0)
        ekle_layout.addWidget(self.btn_yeni_iptal, 3, 2)
        ekle_layout.addWidget(self.btn_ekle, 3, 3)
        return ekle_grubu

    def _yeni_yapilacak_listesi_ac(self):
        maddeler = self._yapilacak_listesi_duzenle(getattr(self, "_aktif_yeni_gorev_dialogu", self), self._yeni_yapilacaklar)
        if maddeler is not None:
            self._yeni_yapilacaklar = maddeler

    def yeni_gorev_paneli_ac(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle(self._tr("todo.add.window", "Yeni Görev"))
        dialog.setModal(True)
        dialog.setFixedWidth(520)
        self._aktif_yeni_gorev_dialogu = dialog

        layout = QtWidgets.QVBoxLayout(dialog)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.addWidget(self._ekleme_formu_olustur())

        dialog.setStyleSheet(self.styleSheet())
        self._popup_katmanlarini_duzelt(dialog)
        dialog.exec()
        self._aktif_yeni_gorev_dialogu = None

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
        gorevler = list(self.servis.gorevleri_sirali_al())
        bugun = datetime.now().date()
        yarin = bugun + timedelta(days=1)
        hafta_sonu = bugun + timedelta(days=7)

        if filtre == "date":
            gorevler = [g for g in gorevler if not g.cope_atildi]
            return sorted(
                gorevler,
                key=lambda g: (
                    0 if g.bitis_tarihi else 1,
                    g.bitis_tarihi or g.olusturulma_zamani,
                    g.sira,
                ),
            )
        if filtre == "today":
            return [g for g in gorevler if g.bitis_tarihi and g.bitis_tarihi.date() == bugun and not g.tamamlandi and not g.iptal_edildi and not g.cope_atildi]
        if filtre == "tomorrow":
            return [g for g in gorevler if g.bitis_tarihi and g.bitis_tarihi.date() == yarin and not g.tamamlandi and not g.iptal_edildi and not g.cope_atildi]
        if filtre == "week":
            return [g for g in gorevler if g.bitis_tarihi and bugun <= g.bitis_tarihi.date() <= hafta_sonu and not g.tamamlandi and not g.iptal_edildi and not g.cope_atildi]
        if filtre == "no_date":
            return [g for g in gorevler if not g.bitis_tarihi and not g.tamamlandi and not g.iptal_edildi and not g.cope_atildi]
        if filtre == "overdue":
            return [g for g in gorevler if g.suresi_gecti_mi() and not g.cope_atildi]
        if filtre == "completed":
            return [g for g in gorevler if g.tamamlandi and not g.cope_atildi]
        if filtre == "cancelled":
            return [g for g in gorevler if g.iptal_edildi and not g.cope_atildi]
        if filtre == "trash":
            return [g for g in gorevler if g.cope_atildi]
        return [g for g in gorevler if not g.cope_atildi and self._varsayilan_listede_gorunur_mu(g)]

    def _varsayilan_listede_gorunur_mu(self, gorev):
        if gorev.tamamlandi:
            return self._durum_suresi_icinde_mi(gorev.tamamlanma_zamani, "todo_completed_visible_days", 7)
        if gorev.iptal_edildi:
            return self._durum_suresi_icinde_mi(gorev.iptal_zamani, "todo_cancelled_visible_days", 7)
        return True

    def _durum_suresi_icinde_mi(self, zaman, alan, varsayilan):
        if not zaman:
            return True
        return datetime.now() - zaman <= timedelta(days=self._todo_ayar_degeri(alan, varsayilan))

    def _gorev_form_dialogu(self, gorev):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle(self._tr("todo.edit.window", "Görevi Düzenle"))
        dialog.setModal(True)
        dialog.setFixedWidth(500)

        layout = QtWidgets.QGridLayout(dialog)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setHorizontalSpacing(8)
        layout.setVerticalSpacing(8)

        txt_baslik = QtWidgets.QLineEdit(gorev.baslik, dialog)
        txt_aciklama = QtWidgets.QTextEdit(dialog)
        txt_aciklama.setPlainText(gorev.aciklama)
        txt_aciklama.setFixedHeight(110)

        cmb_oncelik = KaliciComboBox(dialog)
        self._oncelik_combo_doldur(cmb_oncelik, gorev.oncelik)

        cmb_durum = KaliciComboBox(dialog)
        cmb_durum.addItem("Aktif", "active")
        cmb_durum.addItem(self._tr("todo.status.completed", "Tamamlandı"), "completed")
        cmb_durum.addItem("İptal Edildi", "cancelled")
        cmb_durum.setCurrentIndex(2 if gorev.iptal_edildi else 1 if gorev.tamamlandi else 0)

        tarih_widget, chk_tarih, dt_tarih, txt_saat = self._tarih_saat_widget_olustur(bool(gorev.bitis_tarihi), gorev.bitis_tarihi, self._tr("todo.date.use_due", "Son tarih kullan"), parent=dialog)
        yapilacaklar = list(gorev.yapilacaklar or [])

        btn_liste = QtWidgets.QPushButton(dialog)
        btn_liste.setIcon(_svg_icon(LIST_ICON_PATH, 22))
        btn_liste.setIconSize(QtCore.QSize(22, 22))
        btn_liste.setToolTip("Yapılacak listesi")
        btn_liste.setFixedWidth(42)
        btn_kaydet = QtWidgets.QPushButton(self._tr("todo.edit.save", "Kaydet"), dialog)
        btn_iptal = QtWidgets.QPushButton(self._tr("todo.cancel", "Vazgeç"), dialog)

        def _listeyi_duzenle():
            yeni_maddeler = self._yapilacak_listesi_duzenle(dialog, yapilacaklar)
            if yeni_maddeler is not None:
                yapilacaklar[:] = yeni_maddeler

        def _kaydetmeyi_dene():
            if not txt_baslik.text().strip():
                self._uyari_goster(dialog, self._tr("todo.warning.title_required", "Görev başlığı boş bırakılamaz."))
                txt_baslik.setFocus()
                return
            if not self._tarih_saat_gecerli_mi(chk_tarih, txt_saat):
                self._uyari_goster(dialog, self._tr("todo.warning.invalid_time", "Saat 00:00 - 23:59 aralığında olmalıdır."))
                txt_saat.setFocus()
                return
            dialog.accept()

        btn_liste.clicked.connect(_listeyi_duzenle)
        btn_kaydet.clicked.connect(_kaydetmeyi_dene)
        btn_iptal.clicked.connect(dialog.reject)

        layout.addWidget(QtWidgets.QLabel(self._tr("todo.edit.title", "Başlık")), 0, 0)
        layout.addWidget(txt_baslik, 0, 1, 1, 2)
        layout.addWidget(QtWidgets.QLabel(self._tr("todo.edit.description", "Açıklama")), 1, 0)
        layout.addWidget(txt_aciklama, 1, 1, 1, 2)
        layout.addWidget(QtWidgets.QLabel(self._tr("todo.edit.priority", "Öncelik")), 2, 0)
        layout.addWidget(cmb_oncelik, 2, 1, 1, 2)
        layout.addWidget(QtWidgets.QLabel("Durum"), 3, 0)
        layout.addWidget(cmb_durum, 3, 1, 1, 2)
        layout.addWidget(QtWidgets.QLabel(self._tr("todo.date.label", "Son Tarih:")), 4, 0)
        layout.addWidget(tarih_widget, 4, 1, 1, 2)
        layout.addWidget(btn_liste, 5, 0)
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
        gorev.yapilacaklar = yapilacaklar
        gorev.oncelik = cmb_oncelik.currentData()
        gorev.bitis_tarihi = self._tarih_saat_degeri(chk_tarih, dt_tarih, txt_saat)
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
        maddeler = self._yapilacak_listesi_duzenle(self, gorev.yapilacaklar)
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



