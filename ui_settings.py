from dataclasses import asdict

try:
    from PySide6 import QtCore, QtGui, QtWidgets
except ImportError:
    from PyQt6 import QtCore, QtGui, QtWidgets

from core_settings import PanelSettings, save_settings
from utils import set_autostart

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

        self.tabs = QtWidgets.QTabWidget()

        self.tabs.addTab(self._general_tab(), "Genel")
        
      
        self.battery_tab = self._battery_tab()
        self.time_tab = self._time_tab()
        self.date_tab = self._date_tab()


        self.tabs.addTab(self.battery_tab, "Pil")
        self.tabs.addTab(self.time_tab, "Saat")
        self.tabs.addTab(self.date_tab, "Tarih")


      

        
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


    # ================= GENEL =================

    def _general_tab(self):
        w = QtWidgets.QWidget()
        f = QtWidgets.QFormLayout(w)

        self.chk_top = QtWidgets.QCheckBox("Her zaman üstte")
        self.chk_top.setChecked(self.settings.her_zaman_ustte)
        self.chk_top.toggled.connect(lambda _: self._set_dirty(True))

        self.chk_autostart = QtWidgets.QCheckBox("Açılışta çalıştır")
        self.chk_autostart.setChecked(self.settings.acilista_calistir)
        self.chk_autostart.toggled.connect(lambda _: self._set_dirty(True))

        self.chk_free_layout = QtWidgets.QCheckBox("Serbest dağıt")
        self.chk_free_layout.setChecked(self.settings.free_layout_enabled)
        self.chk_free_layout.toggled.connect(self._apply_free_layout_preview)

        self.sld_opacity = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.sld_opacity.setRange(10, 100)
        self.sld_opacity.setValue(int(self.settings.seffaflik * 100))

        self.sld_opacity.valueChanged.connect(self._apply_opacity_preview)

        self.lbl_opacity_value = QtWidgets.QLabel(f"{self.sld_opacity.value()}%")
        f.addRow(self.chk_top)
        f.addRow(self.chk_autostart)
        f.addRow(self.chk_free_layout)
        opacity_row = QtWidgets.QHBoxLayout()
        opacity_row.addWidget(self.sld_opacity)
        opacity_row.addWidget(self.lbl_opacity_value)
        f.addRow("Şeffaflık (%)", opacity_row)

        # --- Pil ↔ Saat boşluğu ---
        self.spn_space_bt = QtWidgets.QSpinBox()
        self.spn_space_bt.setRange(-200, 200)
        self.spn_space_bt.setValue(self.settings.spacing_battery_time)
        self.spn_space_bt.valueChanged.connect(self._apply_general_preview)

        # --- Saat ↔ Tarih boşluğu ---
        self.spn_space_td = QtWidgets.QSpinBox()
        self.spn_space_td.setRange(-200, 200)
        self.spn_space_td.setValue(self.settings.spacing_time_date)
        self.spn_space_td.valueChanged.connect(self._apply_general_preview)

        # --- Pil ↔ Tarih (saat kapalı) ---
        self.spn_space_bd = QtWidgets.QSpinBox()
        self.spn_space_bd.setRange(-200, 200)
        self.spn_space_bd.setValue(self.settings.spacing_battery_date_hidden)
        self.spn_space_bd.valueChanged.connect(self._apply_general_preview)

        f.addRow("Pil ↔ Saat boşluğu", self.spn_space_bt)
        f.addRow("Saat ↔ Tarih boşluğu", self.spn_space_td)
        f.addRow("Pil \u2194 Tarih bo\u015flu\u011fu (saat kapal\u0131yken)", self.spn_space_bd)
        self._add_help_link(f)
        return w

   
    # ================= SAAT =================
    def _time_tab(self):
        w = QtWidgets.QWidget()
        f = QtWidgets.QFormLayout(w)

        self.chk_time_visible = QtWidgets.QCheckBox("Saat görünür")
        self.chk_time_visible.setChecked(self.settings.time_visible)
        self.chk_time_visible.toggled.connect(
            lambda v: self._apply_time_preview(visible=v)
        )

        self.cmb_time_font = QtWidgets.QFontComboBox()
        self.cmb_time_font.setCurrentFont(QtGui.QFont(self.settings.time_font_family))
        self.cmb_time_font.currentFontChanged.connect(
            lambda f: self._apply_time_preview(font=f.family())
        )

        self.spn_time_size = QtWidgets.QSpinBox()
        self.spn_time_size.setRange(20, 200)
        self.spn_time_size.setValue(self.settings.time_font_size)
        self.spn_time_size.valueChanged.connect(
            lambda v: self._apply_time_preview(size=v)
        )

        self.chk_time_bold = QtWidgets.QCheckBox("Kalın")
        self.chk_time_bold.setChecked(self.settings.time_bold)
        self.chk_time_bold.toggled.connect(
            lambda v: self._apply_time_preview(bold=v)
        )

        self.sld_sec_scale = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.sld_sec_scale.setRange(30, 100)
        self.sld_sec_scale.setValue(int(self.settings.time_seconds_scale * 100))
        self.sld_sec_scale.valueChanged.connect(self._apply_seconds_scale_preview)
        self.lbl_sec_scale_value = QtWidgets.QLabel(f"{self.sld_sec_scale.value()}%")

        self.chk_sec_bold = QtWidgets.QCheckBox("Saniye kalın")
        self.chk_sec_bold.setChecked(self.settings.time_seconds_bold)
        self.chk_sec_bold.toggled.connect(
            lambda v: self._apply_time_preview(seconds_bold=v)
        )

        self.chk_sec_visible = QtWidgets.QCheckBox("Saniyeyi gizle")
        self.chk_sec_visible.setChecked(not self.settings.time_seconds_visible)
        self.chk_sec_visible.toggled.connect(
            lambda v: self._apply_time_preview(seconds_visible=not v)
        )

        self.btn_time_color = QtWidgets.QPushButton(self.settings.time_color)
        self.btn_time_color.clicked.connect(
            lambda: self._pick_color(self.btn_time_color)
        )

        f.addRow(self.chk_time_visible)
        f.addRow("Font", self.cmb_time_font)
        f.addRow("Boyut", self.spn_time_size)
        sec_scale_row = QtWidgets.QHBoxLayout()
        sec_scale_row.addWidget(self.sld_sec_scale)
        sec_scale_row.addWidget(self.lbl_sec_scale_value)
        f.addRow("Saniye boyutu (%)", sec_scale_row)
        sec_opts_row = QtWidgets.QHBoxLayout()
        sec_opts_row.addWidget(self.chk_sec_bold)
        sec_opts_row.addWidget(self.chk_sec_visible)
        f.addRow(sec_opts_row)
        f.addRow("Renk", self.btn_time_color)
        f.addRow(self.chk_time_bold)
        self._add_help_link(f)
        return w

    def _apply_time_preview(self, font=None, size=None, bold=None, visible=None, seconds_scale=None, seconds_bold=None, seconds_visible=None):
        if font is not None:
            self.settings.time_font_family = font
        if size is not None:
            self.settings.time_font_size = size
        if bold is not None:
            self.settings.time_bold = bold
        if visible is not None:
            self.settings.time_visible = visible
        if seconds_scale is not None:
            self.settings.time_seconds_scale = seconds_scale
        if seconds_bold is not None:
            self.settings.time_seconds_bold = seconds_bold
        if seconds_visible is not None:
            self.settings.time_seconds_visible = seconds_visible

        self._set_dirty(True)
        self.parent().apply_settings()

    def _apply_seconds_scale_preview(self, value):
        self.settings.time_seconds_scale = value / 100
        self.lbl_sec_scale_value.setText(f"{value}%")
        self._set_dirty(True)
        self.parent().apply_settings()

    def _apply_general_preview(self):
        self.settings.spacing_battery_time = self.spn_space_bt.value()
        self.settings.spacing_time_date = self.spn_space_td.value()
        self.settings.spacing_battery_date_hidden = self.spn_space_bd.value()

        self._set_dirty(True)
        self.parent().apply_settings()

    def _apply_free_layout_preview(self, value):
        self.settings.free_layout_enabled = value
        self._set_dirty(True)
        self.parent().apply_settings()

    def _apply_opacity_preview(self, value):
        self.settings.seffaflik = value / 100
        self.lbl_opacity_value.setText(f"{value}%")
        self._set_dirty(True)
        self.parent().apply_settings()




    # ================= TARİH =================
    def _date_tab(self):
        w = QtWidgets.QWidget()
        f = QtWidgets.QFormLayout(w)

        self.chk_date_visible = QtWidgets.QCheckBox("Tarih görünür")
        self.chk_date_visible.setChecked(self.settings.date_visible)
        self.chk_date_visible.toggled.connect(
            lambda v: self._apply_date_preview(visible=v)
        )

        self.txt_date_format = QtWidgets.QLineEdit(self.settings.date_format)
        self.txt_date_format.textChanged.connect(lambda _: self._set_dirty(True))

        self.cmb_date_font = QtWidgets.QFontComboBox()
        self.cmb_date_font.setCurrentFont(QtGui.QFont(self.settings.date_font_family))
        self.cmb_date_font.currentFontChanged.connect(
            lambda f: self._apply_date_preview(font=f.family())
        )

        self.spn_date_size = QtWidgets.QSpinBox()
        self.spn_date_size.setRange(8, 100)
        self.spn_date_size.setValue(self.settings.date_font_size)
        self.spn_date_size.valueChanged.connect(
            lambda v: self._apply_date_preview(size=v)
        )

        self.chk_date_bold = QtWidgets.QCheckBox("Kalın")
        self.chk_date_bold.setChecked(self.settings.date_bold)
        self.chk_date_bold.toggled.connect(
            lambda v: self._apply_date_preview(bold=v)
        )

        self.btn_date_color = QtWidgets.QPushButton(self.settings.date_color)
        self.btn_date_color.clicked.connect(
            lambda: self._pick_color(self.btn_date_color)
        )

        f.addRow(self.chk_date_visible)
        f.addRow("Format", self.txt_date_format)
        f.addRow("Font", self.cmb_date_font)
        f.addRow("Renk", self.btn_date_color)
        f.addRow("Boyut", self.spn_date_size)
        f.addRow(self.chk_date_bold)
        self._add_help_link(f)
        return w


    def _apply_date_preview(self, font=None, size=None, bold=None, visible=None):
        if font is not None:
            self.settings.date_font_family = font
        if size is not None:
            self.settings.date_font_size = size
        if bold is not None:
            self.settings.date_bold = bold
        if visible is not None:
            self.settings.date_visible = visible

        self._set_dirty(True)
        self.parent().apply_settings()



    # ================= PİL =================
    def _battery_tab(self):
        w = QtWidgets.QWidget()
        f = QtWidgets.QFormLayout(w)

        # --- Görünürlük ---
        self.chk_batt_visible = QtWidgets.QCheckBox("Pil bilgisi görünür")
        self.chk_batt_visible.setChecked(self.settings.battery_visible)
        self.chk_batt_visible.toggled.connect(self._apply_batt_preview)

        # --- Font ---
        self.cmb_batt_font = QtWidgets.QFontComboBox()
        self.cmb_batt_font.setCurrentFont(
            QtGui.QFont(self.settings.battery_font_family)
        )
        self.cmb_batt_font.currentFontChanged.connect(self._apply_batt_preview)

        # --- Font boyutu ---
        self.spn_batt_size = QtWidgets.QSpinBox()
        self.spn_batt_size.setRange(8, 100)
        self.spn_batt_size.setValue(self.settings.battery_font_size)
        self.spn_batt_size.valueChanged.connect(self._apply_batt_preview)

        # --- Kalın ---
        self.chk_batt_bold = QtWidgets.QCheckBox("Kalın")
        self.chk_batt_bold.setChecked(self.settings.battery_bold)
        self.chk_batt_bold.toggled.connect(self._apply_batt_preview)

        # --- Uyarı seviyesi ---
        self.spn_batt_warn = QtWidgets.QSpinBox()
        self.spn_batt_warn.setRange(1, 100)
        self.spn_batt_warn.setValue(self.settings.battery_warning_level)
        self.spn_batt_warn.valueChanged.connect(self._apply_batt_preview)

        # --- Uyarı aralığı ---
        self.spn_batt_interval = QtWidgets.QSpinBox()
        self.spn_batt_interval.setRange(1, 600)
        self.spn_batt_interval.setValue(self.settings.battery_alert_interval)
        self.spn_batt_interval.valueChanged.connect(self._apply_batt_preview)

        # --- Uyarı sesi ---
        self.cmb_batt_sound = QtWidgets.QComboBox()
        self.cmb_batt_sound.addItems(["Uyarı 1", "Uyarı 2", "Uyarı 3"])
        self.cmb_batt_sound.setCurrentText(self.settings.battery_alert_sound_type)
        self.cmb_batt_sound.currentTextChanged.connect(self._apply_batt_preview)

        self.chk_batt_full = QtWidgets.QCheckBox("Tam dolu uyarisi (yesil yanip sonsun)")
        self.chk_batt_full.setChecked(self.settings.battery_full_alert_enabled)
        self.chk_batt_full.toggled.connect(self._apply_batt_preview)

        self.spn_batt_full_level = QtWidgets.QSpinBox()
        self.spn_batt_full_level.setRange(1, 100)
        self.spn_batt_full_level.setValue(self.settings.battery_full_alert_level)
        self.spn_batt_full_level.valueChanged.connect(self._apply_batt_preview)

        # --- Renk ---
        self.btn_batt_color = QtWidgets.QPushButton(self.settings.battery_color)
        self.btn_batt_color.clicked.connect(
            lambda: self._pick_color(self.btn_batt_color)
        )

        # --- Layout ---
        f.addRow(self.chk_batt_visible)
        f.addRow("Uyarı seviyesi (%)", self.spn_batt_warn)
        f.addRow("Uyarı aralığı (sn)", self.spn_batt_interval)
        f.addRow("Uyarı sesi", self.cmb_batt_sound)
        f.addRow(self.chk_batt_full)
        f.addRow("Tam dolu uyarı seviyesi (%)", self.spn_batt_full_level)
        f.addRow("Renk", self.btn_batt_color)
        f.addRow("Font", self.cmb_batt_font)
        f.addRow("Font boyutu", self.spn_batt_size)
        f.addRow(self.chk_batt_bold)
        self._add_help_link(f)
        return w


    def _apply_batt_preview(self):
        self.settings.battery_visible = self.chk_batt_visible.isChecked()
        self.settings.battery_font_family = self.cmb_batt_font.currentFont().family()
        self.settings.battery_font_size = self.spn_batt_size.value()
        self.settings.battery_bold = self.chk_batt_bold.isChecked()
        self.settings.battery_warning_level = self.spn_batt_warn.value()
        self.settings.battery_alert_interval = self.spn_batt_interval.value()
        self.settings.battery_alert_sound_type = self.cmb_batt_sound.currentText()
        self.settings.battery_full_alert_enabled = self.chk_batt_full.isChecked()
        self.settings.battery_full_alert_level = self.spn_batt_full_level.value()

        self._set_dirty(True)
        self.parent().apply_settings()



   

    # ================= ORTAK =================

    def _pick_color(self, btn):
        dlg = QtWidgets.QColorDialog(self)
        # Native dialog may close the app on some Windows setups;
        # use the Qt dialog for stability.
        dlg.setOption(
            QtWidgets.QColorDialog.ColorDialogOption.DontUseNativeDialog,
            True
        )
        try:
            dlg.setCurrentColor(QtGui.QColor(btn.text()))
        except Exception:
            pass
        if dlg.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            c = dlg.selectedColor()
            if c.isValid():
                btn.setText(c.name())
                self._set_dirty(True)

    def get_settings(self):
        s = self.settings

        s.her_zaman_ustte = self.chk_top.isChecked()
        s.acilista_calistir = self.chk_autostart.isChecked()
        s.seffaflik = self.sld_opacity.value() / 100
        s.free_layout_enabled = self.chk_free_layout.isChecked()

        s.time_visible = self.chk_time_visible.isChecked()
        s.time_font_family = self.cmb_time_font.currentFont().family()
        s.time_font_size = self.spn_time_size.value()
        s.time_bold = self.chk_time_bold.isChecked()
        s.time_color = self.btn_time_color.text()
        s.time_seconds_scale = self.sld_sec_scale.value() / 100
        s.time_seconds_bold = self.chk_sec_bold.isChecked()
        s.time_seconds_visible = not self.chk_sec_visible.isChecked()

        s.date_visible = self.chk_date_visible.isChecked()
        s.date_format = self.txt_date_format.text()
        s.date_font_family = self.cmb_date_font.currentFont().family()
        s.date_font_size = self.spn_date_size.value()

        s.date_bold = self.chk_date_bold.isChecked()
        s.date_color = self.btn_date_color.text()

        s.battery_visible = self.chk_batt_visible.isChecked()
        s.battery_warning_level = self.spn_batt_warn.value()
        s.battery_alert_interval = self.spn_batt_interval.value()
        s.battery_color = self.btn_batt_color.text()
        s.battery_font_size = self.spn_batt_size.value()
        s.battery_alert_sound_type = self.cmb_batt_sound.currentText()
        s.battery_full_alert_enabled = self.chk_batt_full.isChecked()
        s.battery_full_alert_level = self.spn_batt_full_level.value()

        s.spacing_battery_time = self.spn_space_bt.value()
        s.spacing_time_date = self.spn_space_td.value()
        s.spacing_battery_date_hidden = self.spn_space_bd.value()


        return s






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
    locale.setlocale(locale.LC_TIME, "tr_TR")
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
