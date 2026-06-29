try:
    from PySide6 import QtCore, QtGui, QtWidgets
except ImportError:
    from PyQt6 import QtCore, QtGui, QtWidgets

from core_settings import PanelSettings, save_settings, load_settings, UYGULAMA_SURUMU, asdict
from utils import set_autostart, resource_path, ICON_FILE, APP_ID
import sys
import locale
import ctypes

# ui_ayarlar_formlar modülünün mevcut olduğu varsayılmaktadır.
from ui_ayarlar_formlar import AyarFormlari

# =======================
# AYARLAR DİYALOĞU
# =======================

class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ayarlar")
        self.settings = settings
        self._original_settings = PanelSettings(**asdict(settings))
        self._dirty = False

        self.setWindowIcon(QtGui.QIcon(resource_path(ICON_FILE)))
        self.tabs = QtWidgets.QTabWidget()

        self.form_yoneticisi = AyarFormlari(self, self.settings)
        # Sekmeleri AyarFormlari sınıfından yüklüyoruz (Modüler Yapı)
        self.tabs.addTab(self.form_yoneticisi.genel_sekme_olustur(), "Genel")
        self.tabs.addTab(self.form_yoneticisi.pil_sekme_olustur(), "Pil")
        self.tabs.addTab(self.form_yoneticisi.saat_sekme_olustur(), "Saat")
        self.tabs.addTab(self.form_yoneticisi.tarih_sekme_olustur(), "Tarih")
      
        
        self.btn_apply = QtWidgets.QPushButton("Uygula")
        self.btn_apply.setEnabled(False)
        self.btn_save = QtWidgets.QPushButton("Kaydet")
        self.btn_cancel = QtWidgets.QPushButton("İptal")

        self.btn_apply.clicked.connect(self.apply_now)
        self.btn_save.clicked.connect(self.save_and_close)
        self.btn_cancel.clicked.connect(self.reject)



        btns = QtWidgets.QHBoxLayout()
        btns.addStretch()
        btns.addWidget(self.btn_cancel)
        btns.addWidget(self.btn_apply)
        btns.addWidget(self.btn_save)


        main = QtWidgets.QVBoxLayout(self)
        main.addWidget(self.tabs)

        # Alt kısma sürüm bilgisini ekle
        self.surum_etiketi = QtWidgets.QLabel(f"Sürüm: {UYGULAMA_SURUMU}")
        self.surum_etiketi.setStyleSheet("color: gray; font-size: 10px; margin-left: 5px;")
        main.addWidget(self.surum_etiketi)
        main.addLayout(btns)

    def apply_now(self):
        prev_autostart = self.settings.acilista_calistir
        s = self.get_settings()
        self.parent().settings = s
        self.parent().apply_settings()
        ok = set_autostart(s.acilista_calistir)
        if not ok:
            QtWidgets.QMessageBox.warning(
                self,
                "Açılış Ayarı",
                "Açılışta çalıştır ayarı uygulanamadı.\n"
                "Lütfen yetkileri ve sistem ayarlarını kontrol edin."
            )
        elif s.acilista_calistir != prev_autostart:
            msg = (
                "Uygulama başlangıca eklendi."
                if s.acilista_calistir
                else "Uygulama başlangıçtan kaldırıldı."
            )
            info = QtWidgets.QMessageBox(self)
            info.setWindowTitle("Açılış Ayarı")
            info.setText(msg)
            info.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            info.setIcon(QtWidgets.QMessageBox.Icon.NoIcon)
            info.exec()
        self._set_dirty(False)

    def save_and_close(self):
        self.apply_now()
        save_settings(self.settings)
        self.accept()
    
    def reject(self):
        self._restore_original_settings()
        super().reject()

    def _set_dirty(self, dirty=True):
        self._dirty = dirty
        self.btn_apply.setEnabled(dirty)

    def _restore_original_settings(self):
        for field_name in PanelSettings.__dataclass_fields__:
            setattr(self.settings, field_name, getattr(self._original_settings, field_name))
        if self.parent():
            self.parent().apply_settings()
        self._set_dirty(False)

    def _add_help_link(self, form_layout):
        help_btn = QtWidgets.QPushButton("Yardım")
        help_btn.setFlat(True)
        help_btn.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Fixed
        )
        help_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #C8F7C5;
                border: 1px solid #8ED88A;
                border-radius: 8px;
                color: #1E5E1E;
                padding: 4px 10px;
            }
            QPushButton:hover {
                background-color: #B8F0B4;
            }
            QPushButton:pressed {
                background-color: #A8E7A3;
            }
            """
        )
        help_btn.clicked.connect(self.show_help)
        row = QtWidgets.QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.addStretch()
        row.addWidget(help_btn)
        form_layout.insertRow(0, row)


    def show_help(self):
        idx = self.tabs.currentIndex()
        tab_name = self.tabs.tabText(idx)
        if tab_name == "Genel":
            text = (
                "Özet: Genel görünüm, saydamlık, satır aralıkları ve serbest dağıt bu sekmeden yönetilir.\n"
                "\n"
                "Genel ayarlar (sırasıyla):\n"
                "- Her zaman üstte: Pencerenin diğer uygulamaların üstünde kalmasını sağlar.\n"
                "- Açılışta çalıştır: Uygulama Windows açılışında otomatik başlar.\n"
                "- Serbest dağıt: Pil/Saat/Tarih satırları ayrı pencereler olur, her biri bağımsız taşınır.\n"
                "- Şeffaflık (%): Tüm satırların saydamlık seviyesini ayarlar.\n"
                "- Pil ↔ Saat boşluğu: Pil satırı ile saat satırı arasındaki dikey mesafe.\n"
                "- Saat ↔ Tarih boşluğu: Saat satırı ile tarih satırı arasındaki dikey mesafe.\n"
                "- Pil ↔ Tarih boşluğu (saat kapalıyken): Saat görünmüyorsa pil ve tarih arası mesafe."
            )
        elif tab_name == "Pil":
            text = (
                "Özet: Pil satırının görünümü ve uyarı davranışları bu sekmeden ayarlanır.\n"
                "\n"
                "Pil ayarları (sırasıyla):\n"
                "- Pil bilgisi görünür: Pil satırını aç/kapat.\n"
                "- Uyarı seviyesi (%): Pil bu seviyenin altına düşünce uyarı verir.\n"
                "- Uyarı aralığı (sn): Uyarıların kaç saniyede bir tekrar edeceği.\n"
                "- Uyarı sesi: Uyarı sesinin tipi (Uyarı 1/2/3).\n"
                "- Tam dolu uyarısı (yeşil yanıp sönsün): Şarjdayken ve belirlenen yüzde üstünde yeşil yanıp söner.\n"
                "- Tam dolu uyarı seviyesi (%): Tam dolu uyarısının devreye gireceği seviye.\n"
                "- Renk: Pil satırının yazı rengi.\n"
                "- Font: Pil satırı yazı tipi.\n"
                "- Font boyutu: Pil satırı yazı boyutu.\n"
                "- Kalın: Pil yazısını kalın yapar."
            )
        elif tab_name == "Saat":
            text = (
                "Özet: Saat satırının görünümü ve saniye ayarları bu sekmeden yönetilir.\n"
                "\n"
                "Saat ayarları (sırasıyla):\n"
                "- Saat görünür: Saat satırını aç/kapat.\n"
                "- Font: Saat yazı tipi.\n"
                "- Boyut: Saat yazı boyutu.\n"
                "- Saniye boyutu (%): Saniyelerin saat/dakikaya oranı.\n"
                "- Saniye kalın: Saniyeleri kalın yapar.\n"
                "- Saniyeyi gizle: Saniyeleri göstermez (sadece saat:dakika).\n"
                "- Renk: Saat yazı rengi.\n"
                "- Kalın: Saat/dakika yazısını kalın yapar."
            )
        elif tab_name == "Tarih":
            text = (
                "Özet: Tarih satırının görünümü ve formatı bu sekmeden ayarlanır.\n"
                "\n"
                "Tarih ayarları (sırasıyla):\n"
                "- Tarih görünür: Tarih satırını aç/kapat.\n"
                "- Format: Tarihin yazım biçimini belirler.\n"
                "  Özel kısa format harfleri:\n"
                "  g = gün (01-31), G = gün (01-31)\n"
                "  a = ay kısa (Oca), A = ay uzun (Ocak)\n"
                "  y = yıl kısa (25), Y = yıl uzun (2025)\n"
                "  h = gün kısa (Pzt), H = gün uzun (Pazartesi)\n"
                "  Örnek: g a y, h\n"
                "  % işaretli formatlar da geçerlidir (strftime).\n"
                "- Font: Tarih yazı tipi.\n"
                "- Renk: Tarih yazı rengi.\n"
                "- Boyut: Tarih yazı boyutu.\n"
                "- Kalın: Yazıyı kalınlaştırır."
            )
        else:
            text = "Bu sekme için yardım metni bulunamadı."

        self._show_help_box(tab_name, text)

    def _show_help_box(self, tab_name, text):
        box = QtWidgets.QMessageBox(self)
        box.setWindowTitle(f"Yardım - {tab_name}")
        box.setText(text)
        box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        # Ses çıkmaması için icon kullanma
        box.setIcon(QtWidgets.QMessageBox.Icon.NoIcon)
        box.adjustSize()
        self._position_help_box(box)
        box.exec()

    def _position_help_box(self, box):
        app = QtWidgets.QApplication.instance()
        screen = app.screenAt(self.frameGeometry().center()) or app.primaryScreen()
        rect = screen.availableGeometry()

        box.adjustSize()
        bw, bh = box.width(), box.height()
        padding = 10

        dlg = self.frameGeometry()

        candidates = [
            (dlg.right() + padding, dlg.top()),            # right
            (dlg.left() - bw - padding, dlg.top()),        # left
            (dlg.left(), dlg.bottom() + padding),          # below
            (dlg.left(), dlg.top() - bh - padding),        # above
        ]

        def fits(x, y):
            return (
                x >= rect.left()
                and y >= rect.top()
                and x + bw <= rect.right()
                and y + bh <= rect.bottom()
            )

        x, y = None, None
        for cx, cy in candidates:
            if fits(cx, cy):
                x, y = cx, cy
                break

        if x is None:
            x = min(max(rect.left(), dlg.right() + padding), rect.right() - bw)
            y = min(max(rect.top(), dlg.top()), rect.bottom() - bh)

        box.move(x, y)

    def _apply_time_preview(self, font=None, size=None, bold=None, visible=None, seconds_scale=None, seconds_bold=None, seconds_visible=None):
        if font is not None: self.settings.time_font_family = font
        if size is not None: self.settings.time_font_size = size
        if bold is not None: self.settings.time_bold = bold
        if visible is not None: self.settings.time_visible = visible
        if seconds_scale is not None: self.settings.time_seconds_scale = seconds_scale
        if seconds_bold is not None: self.settings.time_seconds_bold = seconds_bold
        if seconds_visible is not None: self.settings.time_seconds_visible = seconds_visible
        self._set_dirty(True)
        if self.parent(): self.parent().apply_settings()

    def _apply_seconds_scale_preview(self, value):
        self.settings.time_seconds_scale = value / 100
        self.lbl_sec_scale_value.setText(f"{value}%")
        self._set_dirty(True)
        if self.parent(): self.parent().apply_settings()

    def _apply_general_preview(self, _=None):
        self.settings.spacing_battery_time = self.spn_space_bt.value()
        self.settings.spacing_time_date = self.spn_space_td.value()
        self.settings.spacing_battery_date_hidden = self.spn_space_bd.value()
        self._set_dirty(True)
        if self.parent(): self.parent().apply_settings()

    def _apply_free_layout_preview(self, value):
        self.settings.free_layout_enabled = value
        self._set_dirty(True)
        if self.parent(): self.parent().apply_settings()

    def _apply_opacity_preview(self, value):
        self.settings.seffaflik = value / 100
        self.lbl_opacity_value.setText(f"{value}%")
        self._set_dirty(True)
        if self.parent(): self.parent().apply_settings()

    def _apply_scale_preview(self, value):
        self.settings.global_scale = value / 100
        self.lbl_scale_value.setText(f"{value}%")
        self._set_dirty(True)
        if self.parent(): self.parent().apply_settings()

    def _apply_date_preview(self, font=None, size=None, bold=None, visible=None):
        if font is not None: self.settings.date_font_family = font
        if size is not None: self.settings.date_font_size = size
        if bold is not None: self.settings.date_bold = bold
        if visible is not None: self.settings.date_visible = visible
        self._set_dirty(True)
        if self.parent(): self.parent().apply_settings()

    def _apply_batt_preview(self, _=None):
        self.settings.battery_visible = self.chk_batt_visible.isChecked()
        self.settings.battery_font_family = self.cmb_batt_font.currentFont().family()
        self.settings.battery_font_size = self.spn_batt_size.value()
        self.settings.battery_bold = self.chk_batt_bold.isChecked()
        self.settings.battery_warning_level = self.spn_batt_warn.value()
        self._set_dirty(True)
        if self.parent(): self.parent().apply_settings()

    # ================= ORTAK =================

    def _pick_color(self, btn):
        """Renk seçici diyaloğunu açar."""
        dlg = QtWidgets.QColorDialog(self)
        dlg.setOption(QtWidgets.QColorDialog.ColorDialogOption.DontUseNativeDialog, True)
        try:
            dlg.setCurrentColor(QtGui.QColor(btn.text()))
        except Exception:
            pass

        if dlg.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            c = dlg.selectedColor()
            if c.isValid():
                btn.setText(c.name())
                self._set_dirty(True)
                return c.name()
        return None

    def get_settings(self):
        """UI elemanlarından ayarları toplar."""
        # Ayarlar artık preview metodları üzerinden anlık olarak self.settings'e yazılıyor.
        # Sadece line edit'ler gibi anlık tetiklenmeyenleri buradan alıyoruz.
        self.settings.date_format = self.txt_date_format.text()
        return self.settings





# =======================
# MAIN
# =======================

def main():
    if sys.platform == "win32":
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)
        except Exception:
            pass
    app = QtWidgets.QApplication(sys.argv)
    locale.setlocale(locale.LC_TIME, "")
    app.setWindowIcon(QtGui.QIcon(resource_path(ICON_FILE)))

    settings = load_settings()
    win = DraggableTransparentWindow(settings)
    if settings.free_layout_enabled:
        win.hide()
    else:
        win.show()
        move_window_safely(win, settings)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
