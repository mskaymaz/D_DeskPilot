try:
    from PySide6 import QtCore, QtWidgets
except ImportError:
    from PyQt6 import QtCore, QtWidgets

from core_settings import save_settings
from todo_filters import todo_ayar_degeri


def _gun_secici_olustur(tooltip, deger, parent):
    spin = QtWidgets.QSpinBox(parent)
    spin.setRange(0, 365)
    spin.setSuffix(" gün")
    spin.setValue(deger)
    spin.setToolTip(tooltip)
    spin.setFixedWidth(110)
    return spin


def _todo_ayarini_yaz(settings, alan, deger):
    if settings is None:
        return
    setattr(settings, alan, int(deger))


def todo_ayarlarini_ac(owner):
    dialog = QtWidgets.QDialog(owner)
    dialog.setWindowTitle("Görevlerim Ayarları")
    dialog.setModal(True)
    dialog.setFixedWidth(540)

    layout = QtWidgets.QVBoxLayout(dialog)
    layout.setContentsMargins(16, 14, 16, 14)
    layout.setSpacing(16)

    aciklama = QtWidgets.QLabel(
        "Liste görünümü ve çöp kutusu saklama süresini buradan yönetebilirsiniz.",
        dialog,
    )
    aciklama.setWordWrap(True)
    aciklama.setStyleSheet("color:#475569;font-size:11pt;")
    layout.addWidget(aciklama)

    form = QtWidgets.QFormLayout()
    form.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
    form.setFormAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
    form.setVerticalSpacing(16)

    spn_cop = _gun_secici_olustur(
        "Çöp kutusunda kalma süresi",
        todo_ayar_degeri(owner.settings, "todo_trash_retention_days", 30),
        dialog,
    )
    spn_tamamlanan = _gun_secici_olustur(
        "Tamamlananlar Tümü listesinde",
        todo_ayar_degeri(owner.settings, "todo_completed_visible_days", 7),
        dialog,
    )
    spn_iptal = _gun_secici_olustur(
        "İptal edilenler Tümü listesinde",
        todo_ayar_degeri(owner.settings, "todo_cancelled_visible_days", 7),
        dialog,
    )

    form.addRow("Silinen görevler", spn_cop)
    form.addRow("Tamamlanan görevler", spn_tamamlanan)
    form.addRow("İptal edilen görevler", spn_iptal)
    layout.addLayout(form)

    not_metni = QtWidgets.QLabel(
        "0 gün seçilirse ilgili işlem hemen uygulanır. Özel filtrelerde kayıtlar ayrıca görüntülenebilir.",
        dialog,
    )
    not_metni.setWordWrap(True)
    not_metni.setStyleSheet("color:#64748b;font-size:10pt;")
    layout.addWidget(not_metni)

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
    dialog.setStyleSheet(dialog.styleSheet() + " QLabel{font-size:11pt;} QSpinBox{font-size:11pt; padding:7px;} ")
    owner._popup_katmanlarini_duzelt(dialog)
    if dialog.exec() != QtWidgets.QDialog.DialogCode.Accepted:
        return False

    _todo_ayarini_yaz(owner.settings, "todo_trash_retention_days", spn_cop.value())
    _todo_ayarini_yaz(owner.settings, "todo_completed_visible_days", spn_tamamlanan.value())
    _todo_ayarini_yaz(owner.settings, "todo_cancelled_visible_days", spn_iptal.value())
    if owner.settings is not None:
        save_settings(owner.settings)
    owner.verileri_yukle()
    return True
