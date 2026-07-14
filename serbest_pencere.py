from PySide6 import QtCore, QtGui, QtWidgets
from utils import resource_path, ICON_FILE
from pencere_araclari import aktif_popup_veya_modal_var, en_ustte_tut, pencere_gorev_cubugunda_mi
from quick_actions import QuickActionsPanel
from alt_hizali_etiket import AltHizaliEtiket

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
            satir_layout.setAlignment(
                QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignBottom
            )
            satir_layout.addWidget(
                self.pil_etiketi, 0, QtCore.Qt.AlignmentFlag.AlignBottom
            )
            satir_layout.addWidget(
                self.pil_ikon_etiketi, 0, QtCore.Qt.AlignmentFlag.AlignBottom
            )
            self.icerik = satir
        elif self.tur == "date":
            self.etiket = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
            self.hafta_ayrac_etiketi = QtWidgets.QLabel("◆", alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
            self.hafta_sayi_etiketi = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
            self.hafta_yazi_etiketi = QtWidgets.QLabel("HAFTA", alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
            self.hicri_etiketi = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
            self.date_switch_button = QtWidgets.QPushButton()
            self.date_switch_button.setFixedSize(30, 30)
            self.date_switch_button.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
            self.hafta_ayrac_etiketi.setVisible(False)
            self.hafta_sayi_etiketi.setVisible(False)
            self.hafta_yazi_etiketi.setVisible(False)

            satir = QtWidgets.QWidget()
            satir_layout = QtWidgets.QHBoxLayout(satir)
            satir_layout.setContentsMargins(0, 0, 0, 0)
            satir_layout.setSpacing(0)
            satir_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            satir_layout.addWidget(self.etiket, 0, QtCore.Qt.AlignmentFlag.AlignBottom)
            satir_layout.addWidget(self.hafta_ayrac_etiketi, 0, QtCore.Qt.AlignmentFlag.AlignVCenter)
            satir_layout.addWidget(self.hafta_sayi_etiketi, 0, QtCore.Qt.AlignmentFlag.AlignBottom)
            satir_layout.addWidget(self.hafta_yazi_etiketi, 0, QtCore.Qt.AlignmentFlag.AlignBottom)
            kutu = QtWidgets.QWidget()
            kutu_layout = QtWidgets.QHBoxLayout(kutu)
            kutu_layout.setContentsMargins(0, 0, 0, 0)
            kutu_layout.setSpacing(0)
            self.date_row = satir
            date_stack = QtWidgets.QWidget()
            self.date_layout = QtWidgets.QVBoxLayout(date_stack)
            self.date_layout.setContentsMargins(0, 0, 0, 0)
            self.date_layout.setSpacing(0)
            self.date_layout.addWidget(satir)
            self.date_layout.addWidget(self.hicri_etiketi)
            kutu_layout.addWidget(self.date_switch_button, 0, QtCore.Qt.AlignmentFlag.AlignVCenter)
            kutu_layout.addWidget(date_stack, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
            self.icerik = kutu
        elif self.tur == "time":
            self.etiket = QtWidgets.QWidget()
            satir_layout = QtWidgets.QHBoxLayout(self.etiket)
            satir_layout.setContentsMargins(0, 0, 0, 0)
            satir_layout.setSpacing(0)
            satir_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.saat_etiketi = AltHizaliEtiket(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
            self.saniye_etiketi = AltHizaliEtiket(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
            self.ampm_etiketi = AltHizaliEtiket(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
            satir_layout.addWidget(self.saat_etiketi, 0, QtCore.Qt.AlignmentFlag.AlignBottom)
            satir_layout.addWidget(self.saniye_etiketi, 0, QtCore.Qt.AlignmentFlag.AlignBottom)
            satir_layout.addWidget(self.ampm_etiketi, 0, QtCore.Qt.AlignmentFlag.AlignBottom)
            self.icerik = self.etiket
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
        button = getattr(self, "date_switch_button", None)
        if (
            e.button() == QtCore.Qt.MouseButton.LeftButton
            and button is not None
            and button.isVisible()
        ):
            top_left = button.mapTo(self, QtCore.QPoint(0, 0))
            if QtCore.QRect(top_left, button.size()).contains(e.position().toPoint()):
                self.kontrolcu._toggle_date_display_mode()
                return
        if self.ayarlar.settings_locked: return
        if e.button() == QtCore.Qt.MouseButton.LeftButton:
            self.surukleme_konumu = e.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        button = getattr(self, "date_switch_button", None)
        if button is not None:
            mode = getattr(self.ayarlar, "date_display_mode", "miladi_hicri")
            inside = (
                self.ayarlar.date_visible
                and mode in {"miladi", "hicri"}
                and self.icerik.rect().contains(e.position().toPoint())
            )
            button.setVisible(self.ayarlar.date_visible and mode in {"miladi", "hicri"})
            self.kontrolcu._set_date_switch_style(button, inside)
        if self.ayarlar.settings_locked: return
        if not self.surukleme_konumu:
            hit_rect = self.quick_actions.hit_rect_for_widget(self.icerik)
            self.quick_actions.show_hit_rects([hit_rect])
            if hit_rect.contains(e.position().toPoint()):
                self.quick_actions.place_for_content_rect(hit_rect)
            else:
                self.quick_actions.delayed_hide()
        if self.surukleme_konumu:
            hedef = e.globalPosition().toPoint() - self.surukleme_konumu
            if self.ayarlar.group_locked:
                self.kontrolcu.move_free_group(self, hedef.x(), hedef.y())
            else:
                self.move(hedef)
            self._ustte_tutma_guncelle()

    def mouseReleaseEvent(self, e):
        if self.ayarlar.settings_locked:
            self.surukleme_konumu = None
            return
        if self.surukleme_konumu:
            self.surukleme_konumu = None
            if self.ayarlar.group_locked:
                self.kontrolcu.update_free_group_position()
            elif not getattr(self.kontrolcu, "_group_editing", False):
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
