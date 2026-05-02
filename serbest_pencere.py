from PySide6 import QtCore, QtGui, QtWidgets
from utils import resource_path, ICON_FILE
from pencere_araclari import en_ustte_tut, pencere_gorev_cubugunda_mi

class SerbestSatirPenceresi(QtWidgets.QWidget):
    """
    Serbest dağıt modunda her satırın (saat, tarih, pil) ayrı pencere olduğu yapı.
    Task 6.2 kapsamında yönetilir.
    """
    def __init__(self, tur, ayarlar, kontrolcu):
        super().__init__(None)
        self.tur = tur # Pencere türü: 'time', 'date', 'battery'
        self.ayarlar = ayarlar
        self.kontrolcu = kontrolcu
        self.surukleme_konumu = None
        self._ustte_tut_zamanlayici = None

        self._pencere_bayraklarini_uygula()
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowOpacity(self.ayarlar.seffaflik)
        self.setWindowIcon(QtGui.QIcon(resource_path(ICON_FILE)))

        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._menuyu_goster)

        self._arayuz_kur()
        self._ustte_tutma_ayari()

    def _pencere_bayraklarini_uygula(self):
        bayraklar = QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.Tool
        if self.ayarlar.her_zaman_ustte:
            bayraklar |= QtCore.Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(bayraklar)

    def _arayuz_kur(self):
        if self.tur == "battery":
            self.pil_etiketi = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
            self.pil_ikon_etiketi = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
            self.pil_ikon_etiketi.setVisible(False)

            satir = QtWidgets.QWidget()
            satir_layout = QtWidgets.QHBoxLayout(satir)
            satir_layout.setContentsMargins(0, 0, 0, 0)
            satir_layout.setSpacing(4)
            satir_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            satir_layout.addWidget(self.pil_etiketi)
            satir_layout.addWidget(self.pil_ikon_etiketi)
            self.icerik = satir
        else:
            self.etiket = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
            self.icerik = self.etiket

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.icerik)

    def bayrak_ve_saydamlik_yenile(self):
        gorunur = self.isVisible()
        self._pencere_bayraklarini_uygula()
        self.setWindowOpacity(self.ayarlar.seffaflik)
        if gorunur:
            self.show()
        self._ustte_tutma_guncelle()

    def _menuyu_goster(self, konum):
        global_konum = self.mapToGlobal(konum)
        ust_sol = self.frameGeometry().topLeft()
        self.kontrolcu.show_menu_at(global_konum, ust_sol)

    def mousePressEvent(self, e):
        if self.ayarlar.settings_locked: return
        if e.button() == QtCore.Qt.MouseButton.LeftButton:
            self.surukleme_konumu = e.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        if self.ayarlar.settings_locked: return
        if self.surukleme_konumu:
            self.move(e.globalPosition().toPoint() - self.surukleme_konumu)
            self._ustte_tutma_guncelle()

    def mouseReleaseEvent(self, e):
        if self.ayarlar.settings_locked:
            self.surukleme_konumu = None
            return
        if self.surukleme_konumu:
            self.surukleme_konumu = None
            ekran = QtGui.QGuiApplication.screenAt(self.pos())
            ekran_adi = ekran.name() if ekran else ""
            self.kontrolcu.update_free_position(self.tur, self.x(), self.y(), ekran_adi)
            self._ustte_tutma_guncelle()

    def _ustte_tutma_ayari(self):
        if not self._ustte_tut_zamanlayici:
            self._ustte_tut_zamanlayici = QtCore.QTimer(self)
            self._ustte_tut_zamanlayici.setInterval(250)
            self._ustte_tut_zamanlayici.timeout.connect(self._ustte_tutma_tik)
        self._ustte_tutma_guncelle()

    def _ustte_tutma_guncelle(self):
        ustte_kalmali = self.isVisible() and self.ayarlar.her_zaman_ustte
        if ustte_kalmali:
            if not self._ustte_tut_zamanlayici.isActive():
                self._ustte_tut_zamanlayici.start()
            en_ustte_tut(self)
            self.raise_()
        else:
            if self._ustte_tut_zamanlayici.isActive():
                self._ustte_tut_zamanlayici.stop()

    def _ustte_tutma_tik(self):
        if not self.isVisible() or not self.ayarlar.her_zaman_ustte:
            if self._ustte_tut_zamanlayici.isActive():
                self._ustte_tut_zamanlayici.stop()
            return

    def wheelEvent(self, event):
        """Sağ tık basılıyken tekerlek hareketi ile ölçeklendirme yapar (Task 6.4)."""
        if event.buttons() & QtCore.Qt.MouseButton.RightButton:
            derece_farki = event.angleDelta().y()
            eski_olcek = self.ayarlar.global_scale
            
            adim = 0.05 if derece_farki > 0 else -0.05
            yeni_olcek = round(max(0.5, min(2.0, eski_olcek + adim)), 2)
            
            if yeni_olcek != eski_olcek:
                self.ayarlar.global_scale = yeni_olcek
                self.kontrolcu.apply_settings()
                from core_settings import save_settings
                save_settings(self.ayarlar)
            
            event.accept()
        else:
            super().wheelEvent(event)
        en_ustte_tut(self)
        self.raise_()