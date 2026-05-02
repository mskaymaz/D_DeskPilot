import locale
import sys
import time
from datetime import datetime, timedelta

try:
    from PySide6 import QtCore, QtGui, QtWidgets
except ImportError:
    from PyQt6 import QtCore, QtGui, QtWidgets

from utils import resource_path, ICON_FILE, log_altyapisini_kur, log_kaydet, _enforce_topmost
from core_settings import PanelSettings, save_settings
from ui_settings import SettingsDialog
from hatirlatici_servisi import HatirlaticiServisi
from hatirlatici_modeli import HatirlaticiDurumu
from hatirlatici_popup import HatirlaticiBildirimPenceresi
from hatirlatici_listesi import HatirlaticiListesiDialog
from gorev_servisi import GorevServisi
from gorev_arayuzu import GorevArayuzuDialog
from pencere_araclari import pencereyi_guvenli_tas, en_ustte_tut, ekrani_bul
from pil_servisi import PilServisi
from bildirim_servisi import BildirimServisi
from serbest_pencere import SerbestSatirPenceresi

# =======================
# ANA PENCERE
# =======================

from pencere_guncelleme import PencereGuncellemeKarishimi
from pencere_navigasyon import PencereNavigasyonKarishimi

def move_window_safely(window, settings):
    """digitalSaatV2.py tarafından kullanılan güvenli taşıma sarmalayıcısı."""
    return pencereyi_guvenli_tas(window, settings)

class DraggableTransparentWindow(QtWidgets.QWidget, PencereGuncellemeKarishimi, PencereNavigasyonKarishimi):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.drag_pos = None
        self._full_charge_blink_on = False
        self._last_low_batt_alert_ts = 0
        self._low_batt_blink_on = False
        self._last_full_batt_alert_ts = 0
        self.free_time_window = None
        self.free_date_window = None
        self.free_battery_window = None
        self._free_layout_active = False
        self._keep_top_timer = None

        # Log altyapısını başlat (Task 1.2)
        log_altyapisini_kur()
        log_kaydet("Uygulama baslatildi.")


        flags = QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.Window
        if settings.her_zaman_ustte:
            flags |= QtCore.Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowOpacity(settings.seffaflik)
        self.setWindowIcon(QtGui.QIcon(resource_path(ICON_FILE)))

        # --- Tarih ---
        self.date_label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        # --- Pil ---
        self.battery_label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.battery_icon_label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.battery_icon_label.setVisible(False)

        self.battery_row = QtWidgets.QWidget()
        self.battery_row_layout = QtWidgets.QHBoxLayout(self.battery_row)
        self.battery_row_layout.setContentsMargins(0, 0, 0, 0)
        self.battery_row_layout.setSpacing(4)
        self.battery_row_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.battery_row_layout.addWidget(self.battery_label)
        self.battery_row_layout.addWidget(self.battery_icon_label)


        # === ANA LAYOUT ===
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )
        self.main_layout.setSpacing(0)


        # --- Spacer: Pil ↔ Saat ---
        self.spacer_bt = QtWidgets.QSpacerItem(
            0,
            settings.spacing_battery_time,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Fixed
        )

        # --- Spacer: Saat ↔ Tarih ---
        self.spacer_td = QtWidgets.QSpacerItem(
            0,
            settings.spacing_time_date,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Fixed
        )

        self.time_label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)


        # --- Layout sıralaması ---
        self.main_layout.addWidget(self.battery_row)
        self.main_layout.addItem(self.spacer_bt)
        self.main_layout.addWidget(self.time_label)
        self.main_layout.addItem(self.spacer_td)
        self.main_layout.addWidget(self.date_label)



        for lbl in (
            self.time_label,
            self.date_label,
            self.battery_label,
            self.battery_icon_label
        ):
            lbl.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
            lbl.setContentsMargins(0, 0, 0, 0)
            lbl.setStyleSheet("""
                QLabel {
                    padding: 0px;
                    margin: 0px;
                }
            """)








        self._zamanlayicilari_kur()
        self._servisleri_baslat()
        self._setup_keep_on_top()
        self.apply_settings()
        self.update_time()
        self.update_battery()

    def _zamanlayicilari_kur(self):
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(200)

        self.batt_timer = QtCore.QTimer(self)
        self.batt_timer.timeout.connect(self.update_battery)
        self.batt_timer.start(5000)

        self.full_charge_timer = QtCore.QTimer(self)
        self.full_charge_timer.timeout.connect(self._toggle_full_charge_blink)
        self.full_charge_timer.setInterval(500)

        self.low_batt_timer = QtCore.QTimer(self)
        self.low_batt_timer.timeout.connect(self._toggle_low_batt_blink)
        self.low_batt_timer.setInterval(500)

        self.hatirlatici_timer = QtCore.QTimer(self)
        self.hatirlatici_timer.timeout.connect(self.hatirlaticilari_kontrol_et)
        self.hatirlatici_timer.start(30000)

        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_menu)

    def _servisleri_baslat(self):
        self.pil_servisi = PilServisi(dusuk_esik=self.settings.battery_warning_level)
        self.bildirim_servisi = BildirimServisi()
        self.hatirlatici_servisi = HatirlaticiServisi()
        self.gorev_servisi = GorevServisi()
        self._aktif_popuplar = {}

    # ---------- AYARLAR ---------- *****************


    def apply_settings(self):
        self._apply_window_flags()
        scale = self.settings.global_scale

        # --- Saat ---
        self._apply_time_style(self.time_label)
        self.time_label.setVisible(self.settings.time_visible)
        if self.free_time_window:
            self._apply_time_style(self.free_time_window.label)
            self.free_time_window.setVisible(
                self.settings.free_layout_enabled and self.settings.time_visible
            )

        # --- Tarih ---
        self._apply_date_style(self.date_label)
        self.date_label.setVisible(self.settings.date_visible)
        if self.free_date_window:
            self._apply_date_style(self.free_date_window.label)
            self.free_date_window.setVisible(
                self.settings.free_layout_enabled and self.settings.date_visible
            )

        # --- Pil ---
        self._apply_battery_style(self.battery_label, self.battery_icon_label)
        self.battery_label.setVisible(self.settings.battery_visible)
        self.battery_icon_label.setVisible(self.settings.battery_visible)
        if self.free_battery_window:
            self._apply_battery_style(
                self.free_battery_window.pil_etiketi,
                self.free_battery_window.pil_ikon_etiketi
            )
            self.free_battery_window.setVisible(
                self.settings.free_layout_enabled and self.settings.battery_visible
            )
            self.free_battery_window.battery_icon_label.setVisible(self.settings.battery_visible)

        self._set_battery_color(self.settings.battery_color)
        self._refresh_battery_rows()

        # --- Spacer guncelle ---
        if self.settings.time_visible:
            bt_space = int(self.settings.spacing_battery_time * scale)
            td_space = int(self.settings.spacing_time_date * scale)
        else:
            # Saat yok -> pil ile tarih birbirine yakin olsun
            bt_space = 0
            td_space = int(self.settings.spacing_battery_date_hidden * scale)

        self.spacer_bt.changeSize(
            0,
            bt_space,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Fixed
        )

        self.spacer_td.changeSize(
            0,
            td_space,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Fixed
        )

        self.main_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        self.layout().invalidate()
        self.main_layout.activate()
        self.adjustSize()
        self.updateGeometry()
        self.setWindowOpacity(self.settings.seffaflik)

        if self.free_time_window:
            self.free_time_window.setWindowOpacity(self.settings.seffaflik)
        if self.free_date_window:
            self.free_date_window.setWindowOpacity(self.settings.seffaflik)
        if self.free_battery_window:
            self.free_battery_window.setWindowOpacity(self.settings.seffaflik)

        self._apply_free_layout_mode()

    def _lock_label_height(self, label, font_size):
        fm = QtGui.QFontMetrics(label.font())
        h = fm.ascent() + fm.descent()
        label.setFixedHeight(h)

    def _apply_window_flags(self):
        flags = QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.Window
        if self.settings.her_zaman_ustte:
            flags |= QtCore.Qt.WindowType.WindowStaysOnTopHint
        was_visible = self.isVisible()
        self.setWindowFlags(flags)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        if was_visible:
            self.show()
        if self.free_time_window:
            self.free_time_window.refresh_flags_and_opacity()
        if self.free_date_window:
            self.free_date_window.refresh_flags_and_opacity()
        if self.free_battery_window:
            self.free_battery_window.refresh_flags_and_opacity()

    def _apply_time_style(self, label):
        scale = self.settings.global_scale
        font_main = QtGui.QFont(
            self.settings.time_font_family,
            int(self.settings.time_font_size * scale)
        )
        font_main.setBold(self.settings.time_bold)
        label.setFont(font_main)
        label.setStyleSheet(
            f"""
            QLabel {{
                color: {self.settings.time_color};
                line-height: {int(self.settings.time_font_size * scale)}px;
                padding: 0px;
                margin: 0px;
            }}
            """
        )

    def _apply_date_style(self, label):
        scale = self.settings.global_scale
        df = QtGui.QFont(
            self.settings.date_font_family,
            int(self.settings.date_font_size * scale)
        )
        df.setBold(self.settings.date_bold)
        label.setFont(df)
        label.setStyleSheet(
            f"color:{self.settings.date_color};"
            f"opacity:{self.settings.date_opacity};"
        )
        self._lock_label_height(label, int(self.settings.date_font_size * scale))

    def _apply_battery_style(self, label, icon_label):
        scale = self.settings.global_scale
        bf = QtGui.QFont(
            self.settings.battery_font_family,
            int(self.settings.battery_font_size * scale)
        )
        bf.setBold(self.settings.battery_bold)
        label.setFont(bf)
        label.setStyleSheet(
            f"color:{self.settings.battery_color};"
            f"opacity:{self.settings.battery_opacity};"
        )
        self._lock_label_height(label, int(self.settings.battery_font_size * scale))

        icon_size = max(1.0, float(self.settings.battery_font_size * scale) * 0.8)
        # Use a symbol font to avoid emoji-size overrides
        bif = QtGui.QFont("Segoe UI Symbol")
        bif.setPointSizeF(icon_size)
        bif.setBold(False)
        icon_label.setFont(bif)
        icon_label.setStyleSheet(
            f"color:{self.settings.battery_color};"
            f"opacity:{self.settings.battery_opacity};"
            f"font-size:{icon_size}px;"
            "font-family:'Segoe UI Symbol';"
        )
        self._lock_label_height(icon_label, int(icon_size))

    def _refresh_battery_rows(self):
        self.battery_row_layout.invalidate()
        self.battery_row.adjustSize()
        self.battery_row.updateGeometry()
        if self.free_battery_window:
            self.free_battery_window.content.adjustSize()
            self.free_battery_window.adjustSize()
            self.free_battery_window.updateGeometry()

    def _ensure_free_windows(self):
        created = False
        if not self.free_time_window:
            self.free_time_window = SerbestSatirPenceresi("time", self.settings, self)
            created = True
        if not self.free_date_window:
            self.free_date_window = SerbestSatirPenceresi("date", self.settings, self)
            created = True
        if not self.free_battery_window:
            self.free_battery_window = SerbestSatirPenceresi("battery", self.settings, self)
            created = True
        if created:
            self._apply_free_window_styles()

    def _apply_free_window_styles(self):
        if self.free_time_window:
            self._apply_time_style(self.free_time_window.etiket)
        if self.free_date_window:
            self._apply_date_style(self.free_date_window.etiket)
        if self.free_battery_window:
            self._apply_battery_style(
                self.free_battery_window.pil_etiketi,
                self.free_battery_window.pil_ikon_etiketi
            )
            self._set_battery_color(self.settings.battery_color)
            self._refresh_battery_rows()

    def _clamp_window_position(self, window, x, y, allow_taskbar=False, hedef_ekran_adi=""):
        """Task 7.2: Pencereyi belirli bir ekranın sınırları içinde tutar."""
        app = QtWidgets.QApplication.instance()
        # Kaydedilen ekranı ara, bulamazsa koordinata göre bak, o da yoksa ana ekran
        screen = ekrani_bul(hedef_ekran_adi)
        if not hedef_ekran_adi:
            screen = app.screenAt(QtCore.QPoint(x, y)) or screen
            
        rect = screen.geometry() if allow_taskbar else screen.availableGeometry()
        window.adjustSize()
        w, h = window.width(), window.height()

        if x < rect.left():
            x = rect.left()
        if y < rect.top():
            y = rect.top()
        if x + w > rect.right():
            x = rect.right() - w
        if y + h > rect.bottom():
            y = rect.bottom() - h

        return x, y

    def _move_line_window_safely(self, window, x, y, hedef_ekran_adi=""):
        # Task 6.2: Serbest moddaki pencereleri güvenli alana yerleştir
        x, y = self._clamp_window_position(window, x, y, allow_taskbar=False, hedef_ekran_adi=hedef_ekran_adi)
        window.move(x, y)

    def _capture_free_positions_from_grouped(self):
        """Grup modundan serbest moda geçerken mevcut konumları yakalar."""
        time_global = self.mapToGlobal(self.time_label.pos())
        date_global = self.mapToGlobal(self.date_label.pos())
        battery_global = self.mapToGlobal(self.battery_row.pos())

        self.settings.free_time_x = time_global.x()
        self.settings.free_time_y = time_global.y()
        self.settings.free_date_x = date_global.x()
        self.settings.free_date_y = date_global.y()
        self.settings.free_battery_x = battery_global.x()
        self.settings.free_battery_y = battery_global.y()
        
        ekran = QtGui.QGuiApplication.screenAt(self.pos())
        if ekran:
            self.settings.serbest_saat_ekran_adi = ekran.name()
            self.settings.serbest_tarih_ekran_adi = ekran.name()
            self.settings.serbest_pil_ekran_adi = ekran.name()
            
        self.settings.free_layout_has_positions = True
        save_settings(self.settings)

    def _show_free_windows(self):
        """Serbest mod pencerelerini kaydedilmiş güvenli konumlarda gösterir."""
        self._ensure_free_windows()

        self._move_line_window_safely(
            self.free_time_window,
            self.settings.free_time_x,
            self.settings.free_time_y,
            self.settings.serbest_saat_ekran_adi
        )
        self._move_line_window_safely(
            self.free_date_window,
            self.settings.free_date_x,
            self.settings.free_date_y,
            self.settings.serbest_tarih_ekran_adi
        )
        self._move_line_window_safely(
            self.free_battery_window,
            self.settings.free_battery_x,
            self.settings.free_battery_y,
            self.settings.serbest_pil_ekran_adi
        )

        if self.settings.time_visible:
            self.free_time_window.show()
        if self.settings.date_visible:
            self.free_date_window.show()
        if self.settings.battery_visible:
            self.free_battery_window.show()

    def _hide_free_windows(self):
        if self.free_time_window:
            self.free_time_window.hide()
        if self.free_date_window:
            self.free_date_window.hide()
        if self.free_battery_window:
            self.free_battery_window.hide()

    def _move_grouped_to_time_position(self):
        """Serbest moddan grup moduna dönerken ana pencereyi saat konumuna taşır."""
        if not self.settings.free_layout_has_positions:
            return
        target_x = self.settings.free_time_x - self.time_label.pos().x()
        target_y = self.settings.free_time_y - self.time_label.pos().y()
        target_x, target_y = self._clamp_window_position(
            self, target_x, target_y, 
            allow_taskbar=False, 
            hedef_ekran_adi=self.settings.serbest_saat_ekran_adi
        )
        self.move(target_x, target_y)
        self.settings.pos_x = target_x
        self.settings.pos_y = target_y
        self.settings.grup_ekran_adi = self.settings.serbest_saat_ekran_adi
        save_settings(self.settings)

    def tum_modulleri_topla(self):
        """
        Tüm modülleri farenin bulunduğu monitöre toplar.
        Task 7.3 kapsamında eklenmiştir.
        """
        app = QtWidgets.QApplication.instance()
        ekran = app.screenAt(QtGui.QCursor.pos()) or app.primaryScreen()
        alan = ekran.availableGeometry()
        
        log_kaydet(f"Tüm modüller '{ekran.name()}' ekranına toplanıyor.")
        
        if not self.settings.free_layout_enabled:
            # Grup modu: Ana pencereyi merkeze taşı
            self.adjustSize()
            x = alan.left() + (alan.width() - self.width()) // 2
            y = alan.top() + (alan.height() - self.height()) // 2
            self.move(x, y)
            self.settings.pos_x = x
            self.settings.pos_y = y
            self.settings.grup_ekran_adi = ekran.name()
        else:
            # Serbest mod: Pencereleri sol üstten başlayarak alt alta diz
            pencereler = [
                (self.free_time_window, "time"),
                (self.free_date_window, "date"),
                (self.free_battery_window, "battery")
            ]
            
            baslangic_x = alan.left() + 50
            baslangic_y = alan.top() + 50
            mevcut_y = baslangic_y
            
            for win, tur in pencereler:
                if win and win.isVisible():
                    win.move(baslangic_x, mevcut_y)
                    self.update_free_position(tur, win.x(), win.y(), ekran.name())
                    mevcut_y += win.height() + 10
        
        save_settings(self.settings)

    def _apply_free_layout_mode(self):
        if self.settings.free_layout_enabled:
            if not self._free_layout_active:
                self._ensure_free_windows()
                if not self.settings.free_layout_has_positions:
                    self._capture_free_positions_from_grouped()
                self._free_layout_active = True
            self._show_free_windows()
            self.hide()
        else:
            if self._free_layout_active:
                self._free_layout_active = False
                self._hide_free_windows()
                self.show()
                self._move_grouped_to_time_position()
            else:
                self._hide_free_windows()

    def update_free_position(self, kind, x, y, ekran_adi=""):
        if self.settings.settings_locked:
            return
        if kind == "time":
            self.settings.free_time_x = x
            self.settings.free_time_y = y
            self.settings.serbest_saat_ekran_adi = ekran_adi
        elif kind == "date":
            self.settings.free_date_x = x
            self.settings.free_date_y = y
            self.settings.serbest_tarih_ekran_adi = ekran_adi
        elif kind == "battery":
            self.settings.free_battery_x = x
            self.settings.free_battery_y = y
            self.settings.serbest_pil_ekran_adi = ekran_adi
        self.settings.free_layout_has_positions = True
        save_settings(self.settings)

    def show_menu(self, pos):
        self.show_menu_at(self.mapToGlobal(pos))


    def mousePressEvent(self, e):
        if self.settings.settings_locked:
            return
        if e.button() == QtCore.Qt.MouseButton.LeftButton:
            self.drag_pos = e.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        if self.settings.settings_locked:
            return
        if self.drag_pos:
            self.move(e.globalPosition().toPoint() - self.drag_pos)

            if hasattr(self, "settings_window") and self.settings_window.isVisible():
                self.position_settings_window(self.settings_window)


    def mouseReleaseEvent(self, e):
        self.drag_pos = None
        if self.settings.settings_locked:
            return
        self.settings.pos_x = self.x()
        self.settings.pos_y = self.y()
        
        ekran = QtGui.QGuiApplication.screenAt(self.pos())
        if ekran:
            self.settings.grup_ekran_adi = ekran.name()
            
        save_settings(self.settings)
        self._update_keep_on_top()

    def _setup_keep_on_top(self):
        if not self._keep_top_timer:
            self._keep_top_timer = QtCore.QTimer(self)
            self._keep_top_timer.setInterval(500)  # Ana pencere için daha seyrek kontrol
            self._keep_top_timer.timeout.connect(self._keep_on_top_tick)
        self._update_keep_on_top()

    def _update_keep_on_top(self):
        should_keep = self.isVisible() and self.settings.her_zaman_ustte
        if should_keep:
            if not self._keep_top_timer.isActive():
                self._keep_top_timer.start()
            _enforce_topmost(self)
            self.raise_()
        else:
            if self._keep_top_timer.isActive():
                self._keep_top_timer.stop()

    def _keep_on_top_tick(self):
        if not self.isVisible() or not self.settings.her_zaman_ustte:
            if self._keep_top_timer.isActive():
                self._keep_top_timer.stop()
            return
        _enforce_topmost(self)
        self.raise_()

    def wheelEvent(self, event):
        """Sağ tık basılıyken tekerlek hareketi ile ölçeklendirme yapar (Task 6.4)."""
        if event.buttons() & QtCore.Qt.MouseButton.RightButton:
            derece_farki = event.angleDelta().y()
            eski_olcek = self.settings.global_scale
            
            # Tekerlek yukarı -> %5 büyüt, Aşağı -> %5 küçült
            adim = 0.05 if derece_farki > 0 else -0.05
            yeni_olcek = round(max(0.5, min(2.0, eski_olcek + adim)), 2)
            
            if yeni_olcek != eski_olcek:
                self.settings.global_scale = yeni_olcek
                self.apply_settings()
                save_settings(self.settings)
            
            event.accept()
        else:
            super().wheelEvent(event)

    def showEvent(self, e):
        super().showEvent(e)
        self._update_keep_on_top()

    def hideEvent(self, e):
        super().hideEvent(e)
        self._update_keep_on_top()

    def moveEvent(self, e):
        super().moveEvent(e)
        self._update_keep_on_top()
