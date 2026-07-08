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
        lbl_baslik = QtWidgets.QLabel("Saat Alarmları")
        lbl_baslik.setStyleSheet("font-weight:bold; font-size:15px;")
        self.btn_ekle = self._ikon_buton("img/icons/add_icon.svg", "Ekle")

        ust_panel = QtWidgets.QHBoxLayout()
        ust_panel.addWidget(lbl_baslik)
        ust_panel.addStretch()
        ust_panel.addWidget(self.btn_ekle)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(ust_panel)
        layout.addWidget(self.lst_alarmlar)

        self.btn_ekle.clicked.connect(self._alarm_ekle)
        self.lst_alarmlar.itemDoubleClicked.connect(lambda _item: self._alarm_duzenle())
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
            if alarm.durum == AlarmDurumu.KACIRILDI:
                tekrar = "Kaçırıldı"
            else:
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
        btn_sil = self._ikon_buton("img/icons/delete_icon.svg", "Sil")
        btn_sil.setFixedSize(28, 26)

        row.addWidget(chk)
        row.addWidget(lbl_saat)
        row.addWidget(lbl_baslik, 1)
        row.addWidget(lbl_tekrar)
        row.addWidget(btn_sil)
        chk.toggled.connect(lambda checked, alarm_id=alarm.id: self._alarm_satir_aktiflik_degistir(alarm_id, checked))
        btn_sil.clicked.connect(lambda _checked=False, alarm_id=alarm.id: self._alarm_sil_id(alarm_id))
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
        txt_tts_metni = QtWidgets.QPlainTextEdit(getattr(alarm, "tts_metni", "") if alarm else "")
        txt_tts_metni.setFixedHeight(58)
        txt_tts_metni.setPlaceholderText("Boşsa başlık ve açıklama okunur.")
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
        cmb_ses.addItems(["Varsayılan", "Kısa zil", "Yumuşak zil", "TTS", "Müzik seç"])
        ses_tipi = getattr(alarm, "ses_tipi", "Varsayılan") if alarm else "Varsayılan"
        if alarm and getattr(alarm, "tts_aktif", False):
            ses_tipi = "TTS"
        cmb_ses.setCurrentText(ses_tipi)
        cmb_ses.setFixedWidth(110)

        secili_ses_dosyasi = {"path": getattr(alarm, "ses_dosyasi", "") if alarm else ""}
        btn_muzik_sec = QtWidgets.QPushButton("...")
        btn_muzik_sec.setFixedSize(28, 24)
        btn_muzik_sec.setToolTip("Müzik dosyası seç")

        def muzik_dosyasi_sec():
            dosya, _ = QtWidgets.QFileDialog.getOpenFileName(
                dialog,
                "Alarm Müziği Seç",
                secili_ses_dosyasi["path"],
                "Ses Dosyaları (*.mp3 *.wav *.ogg *.m4a);;Tüm Dosyalar (*)",
            )
            if dosya:
                secili_ses_dosyasi["path"] = dosya
                cmb_ses.setToolTip(dosya)
                return True
            return False

        def ses_tipi_degisti(text):
            muzik_secili = text == "Müzik seç"
            btn_muzik_sec.setVisible(muzik_secili)
            if muzik_secili:
                cmb_ses.setToolTip(secili_ses_dosyasi["path"])
                if not secili_ses_dosyasi["path"] and not muzik_dosyasi_sec():
                    cmb_ses.setCurrentText("Varsayılan")
            else:
                cmb_ses.setToolTip("")

        cmb_ses.currentTextChanged.connect(ses_tipi_degisti)
        btn_muzik_sec.clicked.connect(muzik_dosyasi_sec)
        ses_tipi_degisti(cmb_ses.currentText())

        spn_tekrar = QtWidgets.QSpinBox()
        spn_tekrar.setRange(1, 300)
        spn_tekrar.setSuffix(" sn")
        spn_tekrar.setValue(getattr(alarm, "tekrar_araligi_saniye", 5) if alarm else 5)
        spn_tekrar.setFixedWidth(58)
        spn_tekrar.setToolTip("Alarm tekrar arası")

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
        secenek_row.addWidget(btn_muzik_sec)
        secenek_row.addSpacing(10)
        secenek_row.addWidget(QtWidgets.QLabel("Tekrar arası"))
        secenek_row.addWidget(spn_tekrar)
        secenek_row.addStretch()

        cmb_tekrar = QtWidgets.QComboBox()
        cmb_tekrar.addItem("Günlük", AlarmTekrarTipi.GUNLUK)
        cmb_tekrar.addItem("Haftalık", AlarmTekrarTipi.HAFTALIK)
        cmb_tekrar.setFixedWidth(88)
        if alarm:
            cmb_tekrar.setCurrentIndex(max(0, cmb_tekrar.findData(alarm.tekrar_tipi)))

        tekrar_row = QtWidgets.QHBoxLayout()
        tekrar_row.setContentsMargins(0, 0, 0, 0)
        tekrar_row.setSpacing(8)
        tekrar_row.addWidget(cmb_tekrar)
        tekrar_row.addSpacing(20)
        tekrar_row.addWidget(QtWidgets.QLabel("Erteleme Süresi"))
        tekrar_row.addWidget(spn_ertele)
        tekrar_row.addStretch()

        gun_row = QtWidgets.QHBoxLayout()
        gunler = []
        for i, ad in enumerate(("Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz")):
            chk = QtWidgets.QCheckBox(ad)
            chk.setProperty("gun", i)
            if alarm and i in alarm.haftanin_gunleri:
                chk.setChecked(True)
            gunler.append(chk)
            gun_row.addWidget(chk)

        def gunleri_guncelle():
            haftalik = cmb_tekrar.currentData() == AlarmTekrarTipi.HAFTALIK
            for chk in gunler:
                chk.setEnabled(haftalik)

        cmb_tekrar.currentIndexChanged.connect(gunleri_guncelle)
        gunleri_guncelle()

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        aciklama_boslugu = QtWidgets.QWidget()
        aciklama_boslugu.setFixedHeight(15)
        tekrar_boslugu = QtWidgets.QWidget()
        tekrar_boslugu.setFixedHeight(15)
        buton_boslugu = QtWidgets.QWidget()
        buton_boslugu.setFixedHeight(15)

        form.addRow("Başlık", baslik_saat_row)
        form.addRow("Açıklama", txt_aciklama)
        form.addRow("", aciklama_boslugu)
        form.addRow("Alarm Seçenekleri", secenek_row)
        form.addRow("TTS Metni", txt_tts_metni)
        form.addRow("", tekrar_boslugu)
        form.addRow("Tekrar", tekrar_row)
        form.addRow("Günler", gun_row)
        form.addRow("", buton_boslugu)
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
                ses_dosyasi=secili_ses_dosyasi["path"] if cmb_ses.currentText() == "Müzik seç" else "",
                tekrar_araligi_saniye=spn_tekrar.value(),
                tts_aktif=cmb_ses.currentText() == "TTS",
                tts_metni=txt_tts_metni.toPlainText().strip(),
                snooze_dakika=spn_ertele.value(),
            )
        return AlarmModeli(
            baslik=txt_baslik.text().strip() or "Alarm",
            aciklama=txt_aciklama.text().strip(),
            saat=time_edit.time().toString("HH:mm"),
            tekrar_tipi=cmb_tekrar.currentData(),
            haftanin_gunleri=[chk.property("gun") for chk in gunler if chk.isChecked()],
            ses_tipi=cmb_ses.currentText(),
            ses_dosyasi=secili_ses_dosyasi["path"] if cmb_ses.currentText() == "Müzik seç" else "",
            tekrar_araligi_saniye=spn_tekrar.value(),
            tts_aktif=cmb_ses.currentText() == "TTS",
            tts_metni=txt_tts_metni.toPlainText().strip(),
            snooze_dakika=spn_ertele.value(),
        )

    def _alarm_sil(self):
        alarm = self._secili_alarm()
        if not alarm:
            return
        self._alarm_sil_id(alarm.id)

    def _alarm_sil_id(self, alarm_id):
        self.alarm_servisi.alarm_sil(alarm_id)
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
