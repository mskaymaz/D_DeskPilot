try:
    from PySide6 import QtCore, QtGui, QtWidgets
except ImportError:
    from PyQt6 import QtCore, QtGui, QtWidgets

from core_settings import PanelSettings
from font_yonetimi import time_font_families, default_time_font_family

class AyarFormlari:
    """
    Ayarlar penceresindeki sekmelerin form içeriklerini oluşturan yardımcı sınıf.
    Dosya boyutu disiplini (Rule: <400 lines) için ui_settings den ayrılmıştır.
    """
    def __init__(self, dialog, ayarlar: PanelSettings):
        self.dialog = dialog
        self.ayarlar = ayarlar

    def _birim_olcek_grubu(self, hedef_tur, baslik):
        dialog = self.dialog
        deger = int(float(getattr(self.ayarlar, f"{hedef_tur}_scale", 1.0)) * 100)
        grup = QtWidgets.QGroupBox(f"{baslik} büyütme")
        grup_layout = QtWidgets.QHBoxLayout(grup)
        grup_layout.setContentsMargins(10, 8, 10, 8)
        grup_layout.setSpacing(8)

        slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        slider.setRange(50, 300)
        slider.setValue(deger)

        spin = QtWidgets.QSpinBox()
        spin.setRange(50, 300)
        spin.setSuffix("%")
        spin.setFixedWidth(70)
        spin.setValue(deger)

        slider.valueChanged.connect(spin.setValue)
        spin.valueChanged.connect(slider.setValue)
        slider.valueChanged.connect(lambda v: dialog._apply_module_scale_preview(hedef_tur, v))

        grup_layout.addWidget(slider)
        grup_layout.addWidget(spin)
        return grup

    def genel_sekme_olustur(self, extra_widget=None):
        dialog = self.dialog
        ayarlar = self.ayarlar
        w = QtWidgets.QWidget()
        f = QtWidgets.QFormLayout(w)

        dialog.chk_top = QtWidgets.QCheckBox("Her zaman üstte")
        dialog.chk_top.setChecked(ayarlar.her_zaman_ustte)
        dialog.chk_top.toggled.connect(lambda _: dialog._set_dirty(True))

        dialog.chk_autostart = QtWidgets.QCheckBox("Açılışta çalıştır")
        dialog.chk_autostart.setChecked(ayarlar.acilista_calistir)
        dialog.chk_autostart.toggled.connect(lambda _: dialog._set_dirty(True))

        dialog.chk_silent = QtWidgets.QCheckBox("Sessiz Mod")
        dialog.chk_silent.setChecked(ayarlar.sessiz_mod)
        dialog.chk_silent.toggled.connect(lambda _: dialog._set_dirty(True))

        dialog.chk_free_layout = QtWidgets.QCheckBox("Serbest dağıt")
        dialog.chk_free_layout.setChecked(ayarlar.free_layout_enabled)
        dialog.chk_free_layout.toggled.connect(dialog._apply_free_layout_preview)

        dialog.chk_multi_mon = QtWidgets.QCheckBox("Çoklu Monitör Desteği")
        dialog.chk_multi_mon.setChecked(ayarlar.coklu_monitor_modu)
        dialog.chk_multi_mon.toggled.connect(lambda _: dialog._set_dirty(True))

        modul_grubu = QtWidgets.QGroupBox("Modül Görünürlüğü")
        modul_layout = QtWidgets.QVBoxLayout(modul_grubu)
        dialog.chk_reminder_visible = QtWidgets.QCheckBox("Hatırlatıcı Modülü Aktif")
        dialog.chk_reminder_visible.setChecked(ayarlar.reminder_visible)
        dialog.chk_reminder_visible.toggled.connect(lambda _: dialog._set_dirty(True))
        dialog.chk_todo_visible = QtWidgets.QCheckBox("Görev Modülü Aktif")
        dialog.chk_todo_visible.setChecked(ayarlar.todo_visible)
        dialog.chk_todo_visible.toggled.connect(lambda _: dialog._set_dirty(True))
        modul_layout.addWidget(dialog.chk_reminder_visible)
        modul_layout.addWidget(dialog.chk_todo_visible)

        dialog.sld_opacity = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        dialog.sld_opacity.setRange(10, 100)
        dialog.sld_opacity.setValue(int(ayarlar.seffaflik * 100))
        dialog.sld_opacity.valueChanged.connect(dialog._apply_opacity_preview)
        dialog.lbl_opacity_value = QtWidgets.QLabel(f"{dialog.sld_opacity.value()}%")

        dialog.sld_scale = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        dialog.sld_scale.setRange(50, 250)
        dialog.sld_scale.setValue(int(ayarlar.global_scale * 100))
        dialog.sld_scale.valueChanged.connect(dialog._apply_scale_preview)
        dialog.spn_scale_value = QtWidgets.QSpinBox()
        dialog.spn_scale_value.setRange(50, 250)
        dialog.spn_scale_value.setSuffix("%")
        dialog.spn_scale_value.setValue(dialog.sld_scale.value())
        dialog.spn_scale_value.valueChanged.connect(dialog.sld_scale.setValue)

        checkbox_col = QtWidgets.QVBoxLayout()
        checkbox_col.setContentsMargins(0, 0, 0, 0)
        checkbox_col.setSpacing(0)
        checkbox_col.addWidget(dialog.chk_top)
        checkbox_col.addWidget(dialog.chk_autostart)
        checkbox_col.addWidget(dialog.chk_silent)
        checkbox_col.addWidget(dialog.chk_free_layout)
        checkbox_col.addWidget(dialog.chk_multi_mon)
        checkbox_row = QtWidgets.QHBoxLayout()
        checkbox_row.setContentsMargins(0, 0, 0, 0)
        checkbox_row.setSpacing(10)
        checkbox_row.addLayout(checkbox_col)
        checkbox_row.addWidget(dialog._module_order_group(), 0, QtCore.Qt.AlignmentFlag.AlignTop)
        checkbox_row.addStretch()
        f.addRow(checkbox_row)
        f.addRow(modul_grubu)
        
        opacity_row = QtWidgets.QHBoxLayout()
        opacity_row.addWidget(dialog.sld_opacity)
        opacity_row.addWidget(dialog.lbl_opacity_value)
        f.addRow("Şeffaflık (%)", opacity_row)
        
        scale_row = QtWidgets.QHBoxLayout()
        scale_row.addWidget(dialog.sld_scale)
        scale_row.addWidget(dialog.spn_scale_value)
        f.addRow("Genel Ölçek (%)", scale_row)

        dialog.spn_space_bt = QtWidgets.QSpinBox()
        dialog.spn_space_bt.setRange(-200, 200)
        dialog.spn_space_bt.setFixedWidth(58)
        dialog.spn_space_bt.setValue(getattr(ayarlar, "spacing_battery_time_offset", 0))
        dialog.spn_space_bt.valueChanged.connect(dialog._apply_general_preview)

        dialog.spn_space_td = QtWidgets.QSpinBox()
        dialog.spn_space_td.setRange(-200, 200)
        dialog.spn_space_td.setFixedWidth(58)
        dialog.spn_space_td.setValue(getattr(ayarlar, "spacing_time_date_offset", 0))
        dialog.spn_space_td.valueChanged.connect(dialog._apply_general_preview)

        dialog.spn_space_bd = QtWidgets.QSpinBox()
        dialog.spn_space_bd.setRange(-200, 200)
        dialog.spn_space_bd.setFixedWidth(58)
        dialog.spn_space_bd.setValue(getattr(ayarlar, "spacing_battery_date_hidden_offset", 0))
        dialog.spn_space_bd.valueChanged.connect(dialog._apply_general_preview)

        dialog.spn_quick_icon_spacing = QtWidgets.QSpinBox()
        dialog.spn_quick_icon_spacing.setRange(0, 40)
        dialog.spn_quick_icon_spacing.setSuffix(" px")
        dialog.spn_quick_icon_spacing.setFixedWidth(68)
        dialog.spn_quick_icon_spacing.setValue(getattr(ayarlar, "quick_actions_icon_spacing", 2))
        dialog.spn_quick_icon_spacing.valueChanged.connect(dialog._apply_general_preview)

        f.addRow("Pil ↔ Saat boşluğu", dialog.spn_space_bt)
        f.addRow("Saat ↔ Tarih boşluğu", dialog.spn_space_td)
        f.addRow("Pil ↔ Tarih boşluğu (saat kapalıyken)", dialog.spn_space_bd)
        f.addRow("Hover ikon aralığı", dialog.spn_quick_icon_spacing)
        
        f.labelForField(dialog.spn_space_bd).setText("Pil \u2194 Tarih bo\u015flu\u011fu")
        dialog._add_help_link(f, extra_widget)
        return w

    def pil_sekme_olustur(self):
        dialog = self.dialog
        ayarlar = self.ayarlar
        w = QtWidgets.QWidget()
        f = QtWidgets.QFormLayout(w)

        dialog.chk_batt_visible = QtWidgets.QCheckBox("Pil bilgisi görünür")
        dialog.chk_batt_visible.setChecked(ayarlar.battery_visible)
        dialog.chk_batt_visible.toggled.connect(dialog._apply_batt_preview)

        dialog.spn_batt_warn = QtWidgets.QSpinBox()
        dialog.spn_batt_warn.setRange(1, 100)
        dialog.spn_batt_warn.setValue(ayarlar.battery_warning_level)
        dialog.spn_batt_warn.valueChanged.connect(dialog._apply_batt_preview)

        dialog.btn_batt_color = QtWidgets.QPushButton(ayarlar.battery_color)
        dialog.btn_batt_color.clicked.connect(lambda: dialog._pick_color(dialog.btn_batt_color))

        dialog.cmb_batt_font = QtWidgets.QFontComboBox()
        dialog.cmb_batt_font.setCurrentFont(QtGui.QFont(ayarlar.battery_font_family))
        dialog.cmb_batt_font.currentFontChanged.connect(dialog._apply_batt_preview)

        dialog.spn_batt_size = QtWidgets.QSpinBox()
        dialog.spn_batt_size.setRange(8, 100)
        dialog.spn_batt_size.setValue(ayarlar.battery_font_size)
        dialog.spn_batt_size.valueChanged.connect(dialog._apply_batt_preview)

        dialog.chk_batt_bold = QtWidgets.QCheckBox("Kalın")
        dialog.chk_batt_bold.setChecked(ayarlar.battery_bold)
        dialog.chk_batt_bold.toggled.connect(dialog._apply_batt_preview)

        f.addRow(dialog.chk_batt_visible)
        f.addRow("Uyarı seviyesi (%)", dialog.spn_batt_warn)
        f.addRow("Renk", dialog.btn_batt_color)
        f.addRow("Font", dialog.cmb_batt_font)
        f.addRow("Font boyutu", dialog.spn_batt_size)
        f.addRow(dialog.chk_batt_bold)
        f.addRow(self._birim_olcek_grubu("battery", "Pil"))
        
        dialog._add_help_link(f)
        return w

    def saat_sekme_olustur(self):
        dialog = self.dialog
        ayarlar = self.ayarlar
        w = QtWidgets.QWidget()
        f = QtWidgets.QFormLayout(w)

        dialog.chk_time_visible = QtWidgets.QCheckBox("Saati Gizle")
        dialog.chk_time_visible.setChecked(not ayarlar.time_visible)
        dialog.chk_time_visible.toggled.connect(lambda v: dialog._apply_time_preview(visible=not v))

        dialog.cmb_time_format = QtWidgets.QComboBox()
        dialog.cmb_time_format.addItem("24 saat", "24h")
        dialog.cmb_time_format.addItem("12 saat ÖS/ÖÖ", "12h_ampm")
        dialog.cmb_time_format.addItem("12 saat sade", "12h_plain")
        format_mode = getattr(ayarlar, "time_format_mode", "24h")
        if not getattr(ayarlar, "time_24h", True) and format_mode == "24h":
            format_mode = "12h_ampm"
        dialog.cmb_time_format.setCurrentIndex(max(0, dialog.cmb_time_format.findData(format_mode)))
        dialog.cmb_time_format.currentIndexChanged.connect(
            lambda _: dialog._apply_time_preview(time_format_mode=dialog.cmb_time_format.currentData())
        )

        dialog.cmb_time_font = QtWidgets.QComboBox()
        for family in time_font_families():
            dialog.cmb_time_font.addItem(family)
        secili_font = ayarlar.time_font_family or default_time_font_family()
        index = dialog.cmb_time_font.findText(secili_font)
        if index < 0:
            index = dialog.cmb_time_font.findText(default_time_font_family())
        dialog.cmb_time_font.setCurrentIndex(max(index, 0))
        dialog.cmb_time_font.setFixedWidth(140)
        dialog.cmb_time_font.currentTextChanged.connect(lambda f: dialog._apply_time_preview(font=f))

        dialog.spn_time_size = QtWidgets.QSpinBox()
        dialog.spn_time_size.setRange(20, 200)
        dialog.spn_time_size.setFixedWidth(58)
        dialog.spn_time_size.setValue(ayarlar.time_font_size)
        dialog.spn_time_size.valueChanged.connect(lambda v: dialog._apply_time_preview(size=v))

        dialog.chk_time_bold = QtWidgets.QCheckBox("Kalın")
        dialog.chk_time_bold.setChecked(ayarlar.time_bold)
        dialog.chk_time_bold.toggled.connect(lambda v: dialog._apply_time_preview(bold=v))

        dialog.sld_sec_scale = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        dialog.sld_sec_scale.setRange(30, 100)
        dialog.sld_sec_scale.setFixedWidth(100)
        dialog.sld_sec_scale.setValue(int(ayarlar.time_seconds_scale * 100))
        dialog.sld_sec_scale.valueChanged.connect(dialog._apply_seconds_scale_preview)
        dialog.lbl_sec_scale_value = QtWidgets.QLabel(f"{dialog.sld_sec_scale.value()}%")

        dialog.chk_sec_visible = QtWidgets.QCheckBox("Saniyeyi gizle")
        dialog.chk_sec_visible.setChecked(not ayarlar.time_seconds_visible)
        dialog.chk_sec_visible.toggled.connect(lambda v: dialog._apply_time_preview(seconds_visible=not v))

        dialog.btn_time_color = QtWidgets.QPushButton(ayarlar.time_color)
        dialog.btn_time_color.setFixedWidth(74)
        dialog.btn_time_color.clicked.connect(lambda: dialog._pick_color(dialog.btn_time_color))

        top_widget = QtWidgets.QWidget()
        top_row = QtWidgets.QHBoxLayout(top_widget)
        top_row.setContentsMargins(0, 0, 0, 0)
        top_row.setSpacing(10)
        top_row.addWidget(dialog.chk_time_visible)
        top_row.addWidget(dialog.cmb_time_format)
        f.addRow("Font", dialog.cmb_time_font)
        size_row = QtWidgets.QHBoxLayout()
        size_row.addWidget(dialog.spn_time_size)
        size_row.addWidget(dialog.chk_time_bold)
        size_row.addStretch()
        f.addRow("Boyut", size_row)
        
        sec_scale_row = QtWidgets.QHBoxLayout()
        sec_scale_row.addWidget(dialog.sld_sec_scale)
        sec_scale_row.addWidget(dialog.lbl_sec_scale_value)
        f.addRow("Saniye boyutu (%)", sec_scale_row)
        f.addRow(dialog.chk_sec_visible)
        f.addRow("Renk", dialog.btn_time_color)
        time_scale_group = self._birim_olcek_grubu("time", "Saat")
        time_scale_group.setMaximumWidth(180)
        f.addRow(time_scale_group)
        
        dialog._add_help_link(f, top_widget)
        return w

    def tarih_sekme_olustur(self):
        dialog = self.dialog
        ayarlar = self.ayarlar
        w = QtWidgets.QWidget()
        f = QtWidgets.QFormLayout(w)

        dialog.chk_date_visible = QtWidgets.QCheckBox("Tarih görünür")
        dialog.chk_date_visible.setChecked(ayarlar.date_visible)
        dialog.chk_date_visible.toggled.connect(lambda v: dialog._apply_date_preview(visible=v))

        dialog.txt_date_format = QtWidgets.QLineEdit(ayarlar.date_format)
        dialog.txt_date_format.textChanged.connect(lambda _: dialog._set_dirty(True))

        dialog.cmb_date_font = QtWidgets.QFontComboBox()
        dialog.cmb_date_font.setCurrentFont(QtGui.QFont(ayarlar.date_font_family))
        dialog.cmb_date_font.currentFontChanged.connect(lambda f: dialog._apply_date_preview(font=f.family()))

        dialog.spn_date_size = QtWidgets.QSpinBox()
        dialog.spn_date_size.setRange(8, 100)
        dialog.spn_date_size.setValue(ayarlar.date_font_size)
        dialog.spn_date_size.valueChanged.connect(lambda v: dialog._apply_date_preview(size=v))

        dialog.btn_date_color = QtWidgets.QPushButton(ayarlar.date_color)
        dialog.btn_date_color.clicked.connect(lambda: dialog._pick_color(dialog.btn_date_color))

        dialog.chk_date_bold = QtWidgets.QCheckBox("Kalın")
        dialog.chk_date_bold.setChecked(ayarlar.date_bold)
        dialog.chk_date_bold.toggled.connect(lambda v: dialog._apply_date_preview(bold=v))

        f.addRow(dialog.chk_date_visible)
        f.addRow("Format", dialog.txt_date_format)
        f.addRow("Font", dialog.cmb_date_font)
        f.addRow("Renk", dialog.btn_date_color)
        f.addRow("Boyut", dialog.spn_date_size)
        f.addRow(dialog.chk_date_bold)
        f.addRow(self._birim_olcek_grubu("date", "Tarih"))
        
        dialog._add_help_link(f)
        return w
