from PySide6 import QtCore, QtGui, QtWidgets
from utils import resource_path, ICON_FILE
from pencere_araclari import aktif_popup_veya_modal_var, en_ustte_tut, pencere_gorev_cubugunda_mi
from quick_actions import QuickActionsPanel

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
        self.setCursor(QtCore.Qt.CursorShape.SizeAllCursor)
        self.setMouseTracking(True)

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
        self.quick_actions = QuickActionsPanel(self, self.kontrolcu)
        self._icerigi_suruklemeye_ac()

    def _icerigi_suruklemeye_ac(self):
        """ç etiketler fareyi yutmasın; sürükleme ana pencereye gelsin."""
        self.icerik.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        for alt_bilesen in self.icerik.findChildren(QtWidgets.QWidget):
            alt_bilesen.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

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
        self.kontrolcu.show_menu_at(global_konum, ust_sol, hedef_tur=self.tur)

    def mousePressEvent(self, e):
        if self.ayarlar.settings_locked: return
        if e.button() == QtCore.Qt.MouseButton.LeftButton:
            self.surukleme_konumu = e.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        if self.ayarlar.settings_locked: return
        if not self.surukleme_konumu:
            hit_rect = self.quick_actions.hit_rect_for_widget(self.icerik)
            self.quick_actions.show_hit_rects([hit_rect])
            if hit_rect.contains(e.position().toPoint()):
                self.quick_actions.place_for_content_rect(hit_rect)
            else:
                self.quick_actions.hide()
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
            if aktif_popup_veya_modal_var():
                return
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
        if aktif_popup_veya_modal_var():
            return
        en_ustte_tut(self)
        self.raise_()


    def enterEvent(self, e):
        if hasattr(self, "quick_actions"):
            hit_rect = self.quick_actions.hit_rect_for_widget(self.icerik)
            self.quick_actions.show_hit_rects([hit_rect])
            if hit_rect.contains(e.position().toPoint()):
                self.quick_actions.place_for_content_rect(hit_rect)
        super().enterEvent(e)

    def leaveEvent(self, e):
        if hasattr(self, "quick_actions"):
            self.quick_actions.delayed_hide()
        super().leaveEvent(e)
