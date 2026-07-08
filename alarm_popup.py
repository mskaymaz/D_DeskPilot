from PySide6 import QtCore, QtGui, QtWidgets
try:
    from PySide6.QtTextToSpeech import QTextToSpeech
except ImportError:
    QTextToSpeech = None
try:
    import winsound
except ImportError:
    winsound = None


class AlarmBildirimPenceresi(QtWidgets.QWidget):
    durduruldu_sinyali = QtCore.Signal(str)
    ertelendi_sinyali = QtCore.Signal(str, int)

    def __init__(self, alarm, parent=None):
        super().__init__(
            parent,
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.WindowStaysOnTopHint
            | QtCore.Qt.WindowType.Tool,
        )
        self.alarm = alarm
        self._tts = None
        self._dongu_aktif = True
        tekrar_saniye = max(1, int(getattr(self.alarm, "tekrar_araligi_saniye", 5) or 5))
        self._tekrar_araligi_ms = tekrar_saniye * 1000
        self._tekrar_timer = QtCore.QTimer(self)
        self._tekrar_timer.setSingleShot(True)
        self._tekrar_timer.timeout.connect(self._alarm_cal)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self._arayuz_kur()
        self._konumlandir()
        self._alarm_cal()

    def _alarm_cal(self):
        if not self._dongu_aktif:
            return
        if self._tts_secili_mi():
            if not self._metni_oku():
                self._tekrar_zamanla()
            return
        self._ses_cal()
        self._tekrar_zamanla()

    def _tekrar_zamanla(self):
        if self._dongu_aktif:
            self._tekrar_timer.start(self._tekrar_araligi_ms)

    def _arayuz_kur(self):
        govde = QtWidgets.QFrame(self)
        govde.setObjectName("Govde")
        govde.setStyleSheet(
            """
            #Govde { background:#111827; border:2px solid #facc15; border-radius:12px; }
            QLabel { color:white; font-family:'Segoe UI'; }
            QPushButton { background:#374151; color:white; border-radius:6px; padding:8px; font-weight:bold; }
            QPushButton:hover { background:#facc15; color:#111827; }
            #Baslik { font-size:17px; font-weight:bold; color:#facc15; }
            #Aciklama { font-size:13px; color:#d1d5db; }
            """
        )
        layout = QtWidgets.QVBoxLayout(govde)
        lbl_baslik = QtWidgets.QLabel(self.alarm.baslik or "Alarm")
        lbl_baslik.setObjectName("Baslik")
        lbl_baslik.setWordWrap(True)
        lbl_aciklama = QtWidgets.QLabel(self.alarm.aciklama or f"Alarm zamanı geldi: {self.alarm.saat}")
        lbl_aciklama.setObjectName("Aciklama")
        lbl_aciklama.setWordWrap(True)

        ertele_dakika = max(1, int(getattr(self.alarm, "snooze_dakika", 5) or 5))
        btn_durdur = QtWidgets.QPushButton("Durdur")
        btn_ertele = QtWidgets.QPushButton(f"{ertele_dakika} dk ertele")
        btn_durdur.clicked.connect(self._durdur)
        btn_ertele.clicked.connect(lambda: self._ertele(ertele_dakika))

        btns = QtWidgets.QHBoxLayout()
        btns.addWidget(btn_durdur)
        btns.addWidget(btn_ertele)

        layout.addWidget(lbl_baslik)
        layout.addWidget(lbl_aciklama)
        layout.addSpacing(10)
        layout.addLayout(btns)

        main = QtWidgets.QVBoxLayout(self)
        main.addWidget(govde)
        self.setFixedSize(300, 160)

    def _konumlandir(self):
        ekran = QtGui.QGuiApplication.primaryScreen().availableGeometry()
        x = ekran.left() + (ekran.width() - self.width()) // 2
        y = ekran.top() + (ekran.height() - self.height()) // 2
        self.move(x, y)

    def _ses_cal(self):
        if not winsound:
            return
        ses_tipi = getattr(self.alarm, "ses_tipi", "Varsayılan")
        sesler = {
            "Varsayılan": winsound.MB_OK,
            "Kısa zil": winsound.MB_ICONEXCLAMATION,
            "Yumuşak zil": winsound.MB_ICONASTERISK,
        }
        winsound.MessageBeep(sesler.get(ses_tipi, winsound.MB_OK))

    def _tts_secili_mi(self):
        return getattr(self.alarm, "ses_tipi", "") == "TTS" or getattr(self.alarm, "tts_aktif", False)

    def _metni_oku(self):
        if not self._tts_secili_mi() or QTextToSpeech is None:
            return False
        metin = (getattr(self.alarm, "tts_metni", "") or "").strip()
        if not metin:
            metin = " ".join(
            parca.strip()
            for parca in (self.alarm.baslik, self.alarm.aciklama)
            if parca and parca.strip()
            ) or f"Alarm zamanı geldi: {self.alarm.saat}"
        if self._tts is None:
            self._tts = QTextToSpeech(self)
            self._turkce_erkek_sesi_sec(self._tts)
            self._tts.stateChanged.connect(self._tts_durum_degisti)
        self._tts.say(metin)
        return True

    def _tts_durum_degisti(self, durum):
        durum_adi = getattr(durum, "name", str(durum)).lower()
        if "ready" in durum_adi or "error" in durum_adi:
            self._tekrar_zamanla()

    def _turkce_erkek_sesi_sec(self, tts):
        try:
            turkce = QtCore.QLocale(QtCore.QLocale.Language.Turkish)
            if hasattr(tts, "setLocale"):
                tts.setLocale(turkce)
            voices = list(tts.availableVoices())

            def turkce_mi(voice):
                locale = voice.locale()
                return (
                    locale.language() == QtCore.QLocale.Language.Turkish
                    or locale.name().lower().startswith("tr")
                )

            def erkek_mi(voice):
                gender = voice.gender()
                ad = getattr(gender, "name", str(gender)).lower()
                return "male" in ad and "female" not in ad

            for voice in voices:
                if turkce_mi(voice) and erkek_mi(voice):
                    tts.setVoice(voice)
                    return
            for voice in voices:
                if turkce_mi(voice):
                    tts.setVoice(voice)
                    return
        except Exception:
            return

    def _tts_durdur(self):
        self._tekrar_timer.stop()
        tts = getattr(self, "_tts", None)
        if tts:
            tts.stop()

    def _durdur(self):
        self._dongu_aktif = False
        self._tts_durdur()
        self.durduruldu_sinyali.emit(self.alarm.id)
        self.close()

    def _ertele(self, dakika):
        self._dongu_aktif = False
        self._tts_durdur()
        self.ertelendi_sinyali.emit(self.alarm.id, dakika)
        self.close()
