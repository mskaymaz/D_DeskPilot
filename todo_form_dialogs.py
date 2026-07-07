from datetime import datetime

try:
    from PySide6 import QtCore, QtWidgets
except ImportError:
    from PyQt6 import QtCore, QtWidgets

from todo_icons import LIST_ICON_PATH, svg_icon
from todo_widgets import KaliciComboBox


def _yapilacaklari_metne_cevir(maddeler):
    return "\n".join(str(madde).strip() for madde in (maddeler or []) if str(madde).strip())


def _metni_yapilacaklara_cevir(metin):
    return [satir.strip() for satir in (metin or "").splitlines() if satir.strip()]


def yapilacak_listesi_duzenle(owner, parent, maddeler):
    dialog = QtWidgets.QDialog(parent)
    dialog.setWindowTitle("Yapılacak Listesi")
    dialog.setModal(True)
    dialog.setFixedSize(420, 320)

    layout = QtWidgets.QVBoxLayout(dialog)
    layout.setContentsMargins(14, 14, 14, 14)
    layout.setSpacing(8)

    txt_liste = QtWidgets.QTextEdit(dialog)
    txt_liste.setPlaceholderText("Her maddeyi ayrı satıra yazın...")
    txt_liste.setPlainText(_yapilacaklari_metne_cevir(maddeler))
    layout.addWidget(txt_liste, 1)

    butonlar = QtWidgets.QHBoxLayout()
    btn_iptal = QtWidgets.QPushButton(owner._tr("todo.cancel", "Vazgeç"), dialog)
    btn_kaydet = QtWidgets.QPushButton(owner._tr("todo.edit.save", "Kaydet"), dialog)
    btn_iptal.clicked.connect(dialog.reject)
    btn_kaydet.clicked.connect(dialog.accept)
    butonlar.addStretch()
    butonlar.addWidget(btn_iptal)
    butonlar.addWidget(btn_kaydet)
    layout.addLayout(butonlar)

    dialog.setStyleSheet(owner.styleSheet())
    owner._popup_katmanlarini_duzelt(dialog)
    if dialog.exec() != QtWidgets.QDialog.DialogCode.Accepted:
        return None
    return _metni_yapilacaklara_cevir(txt_liste.toPlainText())


def ekleme_formu_olustur(owner):
    ekle_grubu = QtWidgets.QGroupBox(owner._tr("todo.add.group", "Yeni Görev Ekle"), owner)
    ekle_layout = QtWidgets.QGridLayout(ekle_grubu)
    ekle_layout.setHorizontalSpacing(15)
    ekle_layout.setVerticalSpacing(6)
    ekle_layout.setContentsMargins(10, 8, 10, 8)

    owner.txt_yeni_gorev = QtWidgets.QLineEdit(ekle_grubu)
    owner.txt_yeni_gorev.setPlaceholderText(owner._tr("todo.add.placeholder.title", "Görev başlığı..."))

    owner.txt_aciklama = QtWidgets.QTextEdit(ekle_grubu)
    owner.txt_aciklama.setPlaceholderText(owner._tr("todo.add.placeholder.description", "Açıklama..."))
    owner.txt_aciklama.setFixedHeight(76)
    owner._yeni_yapilacaklar = []

    owner.cmb_oncelik = KaliciComboBox(ekle_grubu)
    owner._oncelik_combo_doldur(owner.cmb_oncelik, "normal")

    tarih_widget, owner.chk_son_tarih, owner.dt_son_tarih, owner.txt_son_saat = owner._tarih_saat_widget_olustur(False, None, parent=ekle_grubu)

    owner.btn_ekle = QtWidgets.QPushButton(owner._tr("todo.add.submit", "Ekle"), ekle_grubu)
    owner.btn_ekle.setFixedWidth(82)
    owner.btn_ekle.clicked.connect(owner.gorev_ekle)

    owner.btn_yeni_iptal = QtWidgets.QPushButton(owner._tr("todo.cancel", "Vazgeç"), ekle_grubu)
    owner.btn_yeni_iptal.setFixedWidth(82)
    owner.btn_yeni_iptal.clicked.connect(lambda: getattr(owner, "_aktif_yeni_gorev_dialogu", None).reject())

    owner.btn_yeni_liste = QtWidgets.QPushButton(ekle_grubu)
    owner.btn_yeni_liste.setIcon(svg_icon(LIST_ICON_PATH, 22))
    owner.btn_yeni_liste.setIconSize(QtCore.QSize(22, 22))
    owner.btn_yeni_liste.setToolTip("Yapılacak listesi")
    owner.btn_yeni_liste.setFixedWidth(42)
    owner.btn_yeni_liste.clicked.connect(owner._yeni_yapilacak_listesi_ac)

    ekle_layout.addWidget(owner.txt_yeni_gorev, 0, 0, 1, 4)
    ekle_layout.addWidget(owner.txt_aciklama, 1, 0, 1, 4)
    ekle_layout.addWidget(owner.cmb_oncelik, 2, 0)
    ekle_layout.addWidget(tarih_widget, 2, 1, 1, 3)
    ekle_layout.addWidget(owner.btn_yeni_liste, 3, 0)
    ekle_layout.addWidget(owner.btn_yeni_iptal, 3, 2)
    ekle_layout.addWidget(owner.btn_ekle, 3, 3)
    return ekle_grubu


def yeni_yapilacak_listesi_ac(owner):
    maddeler = yapilacak_listesi_duzenle(owner, getattr(owner, "_aktif_yeni_gorev_dialogu", owner), owner._yeni_yapilacaklar)
    if maddeler is not None:
        owner._yeni_yapilacaklar = maddeler


def yeni_gorev_paneli_ac(owner):
    dialog = QtWidgets.QDialog(owner)
    dialog.setWindowTitle(owner._tr("todo.add.window", "Yeni Görev"))
    dialog.setModal(True)
    dialog.setFixedWidth(520)
    owner._aktif_yeni_gorev_dialogu = dialog

    layout = QtWidgets.QVBoxLayout(dialog)
    layout.setContentsMargins(12, 12, 12, 12)
    layout.addWidget(owner._ekleme_formu_olustur())

    dialog.setStyleSheet(owner.styleSheet())
    owner._popup_katmanlarini_duzelt(dialog)
    dialog.exec()
    owner._aktif_yeni_gorev_dialogu = None


def gorev_form_dialogu(owner, gorev):
    dialog = QtWidgets.QDialog(owner)
    dialog.setWindowTitle(owner._tr("todo.edit.window", "Görevi Düzenle"))
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
    owner._oncelik_combo_doldur(cmb_oncelik, gorev.oncelik)

    cmb_durum = KaliciComboBox(dialog)
    cmb_durum.addItem("Aktif", "active")
    cmb_durum.addItem(owner._tr("todo.status.completed", "Tamamlandı"), "completed")
    cmb_durum.addItem("İptal Edildi", "cancelled")
    cmb_durum.setCurrentIndex(2 if gorev.iptal_edildi else 1 if gorev.tamamlandi else 0)

    tarih_widget, chk_tarih, dt_tarih, txt_saat = owner._tarih_saat_widget_olustur(bool(gorev.bitis_tarihi), gorev.bitis_tarihi, owner._tr("todo.date.use_due", "Son tarih kullan"), parent=dialog)
    yapilacaklar = list(gorev.yapilacaklar or [])

    btn_liste = QtWidgets.QPushButton(dialog)
    btn_liste.setIcon(svg_icon(LIST_ICON_PATH, 22))
    btn_liste.setIconSize(QtCore.QSize(22, 22))
    btn_liste.setToolTip("Yapılacak listesi")
    btn_liste.setFixedWidth(42)
    btn_kaydet = QtWidgets.QPushButton(owner._tr("todo.edit.save", "Kaydet"), dialog)
    btn_iptal = QtWidgets.QPushButton(owner._tr("todo.cancel", "Vazgeç"), dialog)

    def _listeyi_duzenle():
        yeni_maddeler = yapilacak_listesi_duzenle(owner, dialog, yapilacaklar)
        if yeni_maddeler is not None:
            yapilacaklar[:] = yeni_maddeler

    def _kaydetmeyi_dene():
        if not txt_baslik.text().strip():
            owner._uyari_goster(dialog, owner._tr("todo.warning.title_required", "Görev başlığı boş bırakılamaz."))
            txt_baslik.setFocus()
            return
        if not owner._tarih_saat_gecerli_mi(chk_tarih, txt_saat):
            owner._uyari_goster(dialog, owner._tr("todo.warning.invalid_time", "Saat 00:00 - 23:59 aralığında olmalıdır."))
            txt_saat.setFocus()
            return
        dialog.accept()

    btn_liste.clicked.connect(_listeyi_duzenle)
    btn_kaydet.clicked.connect(_kaydetmeyi_dene)
    btn_iptal.clicked.connect(dialog.reject)

    layout.addWidget(QtWidgets.QLabel(owner._tr("todo.edit.title", "Başlık")), 0, 0)
    layout.addWidget(txt_baslik, 0, 1, 1, 2)
    layout.addWidget(QtWidgets.QLabel(owner._tr("todo.edit.description", "Açıklama")), 1, 0)
    layout.addWidget(txt_aciklama, 1, 1, 1, 2)
    layout.addWidget(QtWidgets.QLabel(owner._tr("todo.edit.priority", "Öncelik")), 2, 0)
    layout.addWidget(cmb_oncelik, 2, 1, 1, 2)
    layout.addWidget(QtWidgets.QLabel("Durum"), 3, 0)
    layout.addWidget(cmb_durum, 3, 1, 1, 2)
    layout.addWidget(QtWidgets.QLabel(owner._tr("todo.date.label", "Son Tarih:")), 4, 0)
    layout.addWidget(tarih_widget, 4, 1, 1, 2)
    layout.addWidget(btn_liste, 5, 0)
    layout.addWidget(btn_iptal, 5, 1)
    layout.addWidget(btn_kaydet, 5, 2)

    dialog.setStyleSheet(owner.styleSheet())
    owner._popup_katmanlarini_duzelt(dialog)
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
    gorev.bitis_tarihi = owner._tarih_saat_degeri(chk_tarih, dt_tarih, txt_saat)
    gorev.tamamlandi = durum == "completed"
    gorev.iptal_edildi = durum == "cancelled"
    gorev.tamamlanma_zamani = datetime.now() if gorev.tamamlandi and not gorev.tamamlanma_zamani else None if not gorev.tamamlandi else gorev.tamamlanma_zamani
    gorev.iptal_zamani = datetime.now() if gorev.iptal_edildi and not gorev.iptal_zamani else None if not gorev.iptal_edildi else gorev.iptal_zamani
    return True
