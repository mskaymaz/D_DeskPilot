import re
from dataclasses import replace

from PySide6 import QtCore, QtGui, QtWidgets

from alarm_modeli import AlarmModeli, AlarmDurumu, AlarmTekrarTipi
from utils import resource_path


class AlarmListesiDialog(QtWidgets.QDialog):
    def __init__(self, alarm_servisi, parent=None):
        super().__init__(parent)
        self.alarm_servisi = alarm_servisi
        self.setWindowTitle("Saat Alarmları")
        self.resize(460, 360)

        self.lst_alarmlar = QtWidgets.QListWidget()
        self.btn_ekle = self._ikon_buton("img/icons/add_icon.svg", "Ekle")
        self.btn_duzenle = self._ikon_buton("img/icons/duzenle.svg", "Düzenle")
        self.btn_sil = self._ikon_buton("img/icons/delete_icon.svg", "Sil")

        btns = QtWidgets.QHBoxLayout()
        btns.addWidget(self.btn_ekle)
        btns.addWidget(self.btn_duzenle)
        btns.addWidget(self.btn_sil)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.lst_alarmlar)
        layout.addLayout(btns)

        self.btn_ekle.clicked.connect(self._alarm_ekle)
        self.btn_duzenle.clicked.connect(self._alarm_duzenle)
        self.btn_sil.clicked.connect(self._alarm_sil)
        self._liste_yenile()

    def _ikon_buton(self, ikon_yolu, ipucu):
        btn = QtWidgets.QPushButton()
        btn.setIcon(QtGui.QIcon(resource_path(ikon_yolu)))
        btn.setIconSize(QtCore.QSize(22, 22))
        btn.setFixedSize(34, 30)
        btn.setToolTip(ipucu)
        return btn

    def _liste_yenile(self):
        self.lst_alarmlar.clear()
        for alarm in self.alarm_servisi.alarmlari_al():
            tekrar = "Günlük" if alarm.tekrar_tipi == AlarmTekrarTipi.GUNLUK else "Haftalık"
            item = QtWidgets.QListWidgetItem()
            item.setData(QtCore.Qt.ItemDataRole.UserRole, alarm.id)
            item.setSizeHint(QtCore.QSize(0, 34))
            self.lst_alarmlar.addItem(item)
            self.lst_alarmlar.setItemWidget(item, self._alarm_satir_widget(alarm, tekrar))

    def _alarm_satir_widget(self, alarm, tekrar):
        widget = QtWidgets.QWidget()
        row = QtWidgets.QHBoxLayout(widget)
        row.setContentsMargins(6, 2, 6, 2)
        row.setSpacing(10)

        chk = QtWidgets.QCheckBox()
        chk.setChecked(alarm.durum == AlarmDurumu.AKTIF)
        chk.setToolTip("Aktif/Pasif")

        lbl_saat = QtWidgets.QLabel(alarm.saat)
        lbl_saat.setFixedWidth(46)
        lbl_baslik = QtWidgets.QLabel(alarm.baslik or "Alarm")
        lbl_tekrar = QtWidgets.QLabel(tekrar)
        lbl_tekrar.setFixedWidth(58)

        row.addWidget(chk)
        row.addWidget(lbl_saat)
        row.addWidget(lbl_baslik, 1)
        row.addWidget(lbl_tekrar)
        chk.toggled.connect(lambda checked, alarm_id=alarm.id: self._alarm_satir_aktiflik_degistir(alarm_id, checked))
        return widget

    def _alarm_satir_aktiflik_degistir(self, alarm_id, aktif):
        self.alarm_servisi.alarm_aktiflik_degistir(alarm_id, aktif)

    def _secili_alarm(self):
        item = self.lst_alarmlar.currentItem()
        if not item:
            return None
        alarm_id = item.data(QtCore.Qt.ItemDataRole.UserRole)
        for alarm in self.alarm_servisi.alarmlari_al():
            if alarm.id == alarm_id:
                return alarm
        return None

    def _alarm_ekle(self):
        alarm = self._alarm_formu()
        if not alarm:
            return
        self.alarm_servisi.alarm_ekle(alarm)
        self._liste_yenile()

    def _alarm_duzenle(self):
        alarm = self._secili_alarm()
        if not alarm:
            return
        yeni_alarm = self._alarm_formu(alarm)
        if not yeni_alarm:
            return
        self.alarm_servisi.alarm_guncelle(yeni_alarm)
        self._liste_yenile()

    def _alarm_formu(self, alarm=None):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Alarm Düzenle" if alarm else "Alarm Ekle")
        form = QtWidgets.QFormLayout(dialog)

        txt_baslik = QtWidgets.QLineEdit(alarm.baslik if alarm else self._siradaki_alarm_adi())
        txt_baslik.setFixedWidth(190)
        txt_aciklama = QtWidgets.QLineEdit(alarm.aciklama if alarm else "")
        alarm_time = QtCore.QTime.fromString(alarm.saat, "HH:mm") if alarm else QtCore.QTime.currentTime()
        if not alarm_time.isValid():
            alarm_time = QtCore.QTime.currentTime()
        time_edit = QtWidgets.QTimeEdit(alarm_time)
        time_edit.setDisplayFormat("HH:mm")
        time_edit.setFixedWidth(76)

        baslik_saat_row = QtWidgets.QHBoxLayout()
        baslik_saat_row.setContentsMargins(0, 0, 0, 0)
        baslik_saat_row.setSpacing(8)
        baslik_saat_row.addWidget(txt_baslik)
        baslik_saat_row.addStretch()
        baslik_saat_row.addWidget(QtWidgets.QLabel("Saat"))
        baslik_saat_row.addWidget(time_edit)

        cmb_ses = QtWidgets.QComboBox()
        cmb_ses.addItems(["Varsayılan", "Kısa zil", "Yumuşak zil"])
        cmb_ses.setCurrentText(getattr(alarm, "ses_tipi", "Varsayılan") if alarm else "Varsayılan")
        cmb_ses.setFixedWidth(110)

        spn_ses = QtWidgets.QSpinBox()
        spn_ses.setRange(0, 100)
        spn_ses.setSuffix("%")
        spn_ses.setValue(getattr(alarm, "ses_seviyesi", 70) if alarm else 70)
        spn_ses.setFixedWidth(62)

        chk_tts = QtWidgets.QCheckBox("TTS")
        chk_tts.setChecked(getattr(alarm, "tts_aktif", False) if alarm else False)

        spn_ertele = QtWidgets.QSpinBox()
        spn_ertele.setRange(1, 60)
        spn_ertele.setSuffix(" dk")
        spn_ertele.setValue(getattr(alarm, "snooze_dakika", 5) if alarm else 5)
        spn_ertele.setFixedWidth(72)
        spn_ertele.setToolTip("Erteleme süresi")

        secenek_row = QtWidgets.QHBoxLayout()
        secenek_row.setContentsMargins(0, 0, 0, 0)
        secenek_row.setSpacing(8)
        secenek_row.addWidget(cmb_ses)
        secenek_row.addWidget(spn_ses)
        secenek_row.addWidget(chk_tts)
        secenek_row.addWidget(spn_ertele)
        secenek_row.addStretch()

        cmb_tekrar = QtWidgets.QComboBox()
        cmb_tekrar.addItem("Günlük", AlarmTekrarTipi.GUNLUK)
        cmb_tekrar.addItem("Haftalık", AlarmTekrarTipi.HAFTALIK)
        if alarm:
            cmb_tekrar.setCurrentIndex(max(0, cmb_tekrar.findData(alarm.tekrar_tipi)))

        gun_row = QtWidgets.QHBoxLayout()
        gunler = []
        for i, ad in enumerate(("Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz")):
            chk = QtWidgets.QCheckBox(ad)
            chk.setProperty("gun", i)
            if alarm and i in alarm.haftanin_gunleri:
                chk.setChecked(True)
            gunler.append(chk)
            gun_row.addWidget(chk)

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        form.addRow("Başlık", baslik_saat_row)
        form.addRow("Açıklama", txt_aciklama)
        form.addRow("Alarm Seçenekleri", secenek_row)
        form.addRow("Tekrar", cmb_tekrar)
        form.addRow("Günler", gun_row)
        form.addRow(buttons)

        if dialog.exec() != QtWidgets.QDialog.DialogCode.Accepted:
            return None

        if alarm:
            return replace(
                alarm,
                baslik=txt_baslik.text().strip() or "Alarm",
                aciklama=txt_aciklama.text().strip(),
                saat=time_edit.time().toString("HH:mm"),
                tekrar_tipi=cmb_tekrar.currentData(),
                haftanin_gunleri=[chk.property("gun") for chk in gunler if chk.isChecked()],
                ses_tipi=cmb_ses.currentText(),
                ses_seviyesi=spn_ses.value(),
                tts_aktif=chk_tts.isChecked(),
                snooze_dakika=spn_ertele.value(),
            )
        return AlarmModeli(
            baslik=txt_baslik.text().strip() or "Alarm",
            aciklama=txt_aciklama.text().strip(),
            saat=time_edit.time().toString("HH:mm"),
            tekrar_tipi=cmb_tekrar.currentData(),
            haftanin_gunleri=[chk.property("gun") for chk in gunler if chk.isChecked()],
            ses_tipi=cmb_ses.currentText(),
            ses_seviyesi=spn_ses.value(),
            tts_aktif=chk_tts.isChecked(),
            snooze_dakika=spn_ertele.value(),
        )

    def _alarm_sil(self):
        alarm = self._secili_alarm()
        if not alarm:
            return
        self.alarm_servisi.alarm_sil(alarm.id)
        self._liste_yenile()

    def _siradaki_alarm_adi(self):
        kullanilan = set()
        for alarm in self.alarm_servisi.alarmlari_al():
            eslesme = re.fullmatch(r"Alarm(\d+)", alarm.baslik.strip())
            if eslesme:
                kullanilan.add(int(eslesme.group(1)))
        sayi = 1
        while sayi in kullanilan:
            sayi += 1
        return f"Alarm{sayi}"
