try:
    from PySide6 import QtCore, QtGui, QtWidgets
except ImportError:
    from PyQt6 import QtCore, QtGui, QtWidgets
from core_settings import PanelSettings, save_settings, load_settings, UYGULAMA_SURUMU, asdict
from utils import set_autostart, resource_path, ICON_FILE, APP_ID
import sys
import locale
import ctypes
from datetime import datetime

# ui_ayarlar_formlar modülünün mevcut olduğu varsayılmaktadır.
from ui_ayarlar_formlar import AyarFormlari
from oncelik_yonetimi import default_task_priorities
from font_yonetimi import load_app_fonts
from dil_yonetimi import SUPPORTED_LANGUAGES, t

# =======================
# AYARLAR DİYALOĞU
# =======================

class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, settings, parent=None, hedef_tur=None):
        super().__init__(parent)
        self.setWindowTitle("Ayarlar")
        self.settings = settings
        load_app_fonts()
        self._original_settings = PanelSettings(**asdict(settings))
        self._dirty = False

        self.setWindowIcon(QtGui.QIcon(resource_path(ICON_FILE)))
        self.setMinimumWidth(330)
        self.tabs = QtWidgets.QTabWidget()

        self.form_yoneticisi = AyarFormlari(self, self.settings)
        # Sekmeleri AyarFormlari sınıfından yüklüyoruz (Modüler Yapı)
        self.tabs.addTab(self.form_yoneticisi.genel_sekme_olustur(self._language_combo_olustur()), "Genel")
        self._hedef_sekmeleri_ekle(hedef_tur)
      
        
        self.btn_apply = QtWidgets.QPushButton("Uygula")
        self.btn_apply.setEnabled(False)
        self.btn_save = QtWidgets.QPushButton("Kaydet")
        self.btn_cancel = QtWidgets.QPushButton("İptal")
        self.btn_panel_default = QtWidgets.QPushButton("Varsayılan")
        for btn, width in (
            (self.btn_cancel, 58),
            (self.btn_apply, 64),
            (self.btn_save, 58),
            (self.btn_panel_default, 86),
        ):
            btn.setFixedWidth(width)

        self.btn_apply.clicked.connect(self.apply_now)
        self.btn_save.clicked.connect(self.save_and_close)
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_panel_default.clicked.connect(self._restore_current_tab_defaults)



        btns = QtWidgets.QHBoxLayout()
        btns.addWidget(self.btn_panel_default)
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

    def _hedef_sekmeleri_ekle(self, hedef_tur):
        sekmeler = {
            "battery": (self.form_yoneticisi.pil_sekme_olustur, "Pil"),
            "time": (self.form_yoneticisi.saat_sekme_olustur, "Saat"),
            "date": (self.form_yoneticisi.tarih_sekme_olustur, "Tarih"),
        }
        if hedef_tur in sekmeler:
            olustur, baslik = sekmeler[hedef_tur]
            self.tabs.addTab(olustur(), baslik)
            return
        for olustur, baslik in sekmeler.values():
            self.tabs.addTab(olustur(), baslik)

    def _language_tab_olustur(self):
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(tab)
        layout.addWidget(QtWidgets.QLabel("Uygulama dili:"))
        layout.addWidget(self._language_combo_olustur())
        layout.addStretch()
        return tab

    def _language_combo_olustur(self):
        self.cmb_language = QtWidgets.QComboBox()
        self.cmb_language.setFixedWidth(50)
        for lang in SUPPORTED_LANGUAGES:
            self.cmb_language.addItem(lang.upper(), lang)
        idx = self.cmb_language.findData(getattr(self.settings, "language", "tr"))
        self.cmb_language.setCurrentIndex(max(idx, 0))
        self.cmb_language.currentIndexChanged.connect(lambda: self._set_dirty(True))
        return self.cmb_language

    def _task_priorities_tab_olustur(self):
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(tab)

        info = QtWidgets.QLabel("Görev öncelik adlarını ve renklerini buradan düzenleyebilirsiniz. Ad sınırı: 7 karakter.")
        info.setWordWrap(True)
        layout.addWidget(info)

        self.tbl_task_priorities = QtWidgets.QTableWidget(0, 3)
        self.tbl_task_priorities.setHorizontalHeaderLabels(["Anahtar", "Ad", "Renk"])
        self.tbl_task_priorities.horizontalHeader().setStretchLastSection(True)
        self.tbl_task_priorities.verticalHeader().setVisible(False)
        self.tbl_task_priorities.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tbl_task_priorities.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        layout.addWidget(self.tbl_task_priorities)

        buttons = QtWidgets.QHBoxLayout()
        self.btn_priority_add = QtWidgets.QPushButton("Ekle")
        self.btn_priority_delete = QtWidgets.QPushButton("Seçileni Sil")
        self.btn_priority_default = QtWidgets.QPushButton("Varsayılanlara Dön")
        self.btn_priority_add.clicked.connect(self._task_priority_add)
        self.btn_priority_delete.clicked.connect(self._task_priority_delete)
        self.btn_priority_default.clicked.connect(self._task_priorities_restore_defaults)
        buttons.addWidget(self.btn_priority_add)
        buttons.addWidget(self.btn_priority_delete)
        buttons.addStretch()
        buttons.addWidget(self.btn_priority_default)
        layout.addLayout(buttons)

        self._priority_table_loading = False
        self._task_priorities_table_load()
        return tab

    def _task_priorities_table_load(self):
        self._priority_table_loading = True
        self.tbl_task_priorities.setRowCount(0)
        for item in getattr(self.settings, "task_priorities", []) or default_task_priorities():
            self._task_priority_row_add(item.get("key", ""), item.get("name", ""), item.get("color", "#3b82f6"))
        self._priority_table_loading = False

    def _task_priority_row_add(self, key, name, color):
        row = self.tbl_task_priorities.rowCount()
        self.tbl_task_priorities.insertRow(row)

        key_item = QtWidgets.QTableWidgetItem(str(key))
        key_item.setFlags(key_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
        self.tbl_task_priorities.setItem(row, 0, key_item)

        name_edit = QtWidgets.QLineEdit(str(name)[:7])
        name_edit.setMaxLength(7)
        name_edit.textChanged.connect(lambda _=None: self._task_priorities_changed())
        self.tbl_task_priorities.setCellWidget(row, 1, name_edit)

        color_btn = QtWidgets.QPushButton(str(color or "#3b82f6"))
        color_btn.clicked.connect(lambda _=None, b=color_btn: self._task_priority_pick_color(b))
        self.tbl_task_priorities.setCellWidget(row, 2, color_btn)

    def _task_priority_next_key(self):
        existing = {self.tbl_task_priorities.item(r, 0).text() for r in range(self.tbl_task_priorities.rowCount())}
        i = 1
        while f"custom_{i}" in existing:
            i += 1
        return f"custom_{i}"

    def _task_priority_add(self):
        self._task_priority_row_add(self._task_priority_next_key(), "Yeni", "#8b5cf6")
        self._task_priorities_changed()

    def _task_priority_delete(self):
        rows = sorted({i.row() for i in self.tbl_task_priorities.selectedIndexes()}, reverse=True)
        protected = {"low", "normal", "high"}
        for row in rows:
            item = self.tbl_task_priorities.item(row, 0)
            if item and item.text() not in protected:
                self.tbl_task_priorities.removeRow(row)
        self._task_priorities_changed()

    def _task_priority_pick_color(self, btn):
        color = self._pick_color(btn)
        if color:
            btn.setText(color)
            self._task_priorities_changed()

    def _task_priorities_restore_defaults(self):
        self.settings.task_priorities = default_task_priorities()
        self._task_priorities_table_load()
        self._task_priorities_changed()

    def _task_priorities_changed(self):
        if getattr(self, "_priority_table_loading", False):
            return
        self._sync_task_priorities_from_table()
        self._set_dirty(True)

    def _sync_task_priorities_from_table(self):
        items = []
        for row in range(self.tbl_task_priorities.rowCount()):
            key_item = self.tbl_task_priorities.item(row, 0)
            name_edit = self.tbl_task_priorities.cellWidget(row, 1)
            color_btn = self.tbl_task_priorities.cellWidget(row, 2)
            key = key_item.text().strip() if key_item else ""
            name = name_edit.text().strip() if name_edit else ""
            color = color_btn.text().strip() if color_btn else "#3b82f6"
            if key and name:
                items.append({"key": key, "name": name[:7], "color": color})
        self.settings.task_priorities = items or default_task_priorities()

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
            self.parent()._group_editing = (
                not self.settings.group_locked and not self.settings.free_layout_enabled
            )
            self.parent().apply_settings()
        self._set_dirty(False)

    def _restore_current_tab_defaults(self):
        defaults = PanelSettings()
        tab_name = self.tabs.tabText(self.tabs.currentIndex())
        fields_by_tab = {
            "Genel": (
                "language", "seffaflik", "her_zaman_ustte", "acilista_calistir",
                "acilis_animasyonu_goster", "sessiz_mod",
                "free_layout_enabled", "group_locked", "coklu_monitor_modu",
                "alarm_visible", "reminder_visible",
                "todo_visible",
                "global_scale", "quick_actions_icon_size",
                "quick_actions_icon_spacing",
            ),
            "Pil": (
                "battery_visible", "battery_font_family", "battery_color", "battery_bold",
                "battery_warning_level", "battery_alert_interval", "battery_alert_sound_type",
                "battery_scale",
            ),
            "Saat": (
                "time_visible", "time_font_family", "time_color", "time_bold", "time_24h",
                "time_format_mode", "time_seconds_scale", "time_seconds_visible", "time_scale",
            ),
            "Tarih": (
                "date_visible", "date_format", "date_font_family", "date_color", "date_bold",
                "date_show_week_number", "date_display_mode", "date_hicri_first", "date_scale",
                "date_hicri_scale",
            ),
        }
        for field_name in fields_by_tab.get(tab_name, ()):
            setattr(self.settings, field_name, getattr(defaults, field_name))
        self._sync_current_tab_defaults(tab_name)
        self._set_dirty(True)
        if self.parent():
            self.parent().apply_settings()

    def _set_value_silent(self, widget, value):
        widget.blockSignals(True)
        widget.setValue(value)
        widget.blockSignals(False)

    def _set_checked_silent(self, widget, value):
        widget.blockSignals(True)
        widget.setChecked(value)
        widget.blockSignals(False)

    def _sync_current_tab_defaults(self, tab_name):
        s = self.settings
        if tab_name == "Genel":
            self._set_checked_silent(self.chk_top, s.her_zaman_ustte)
            self._set_checked_silent(self.chk_autostart, s.acilista_calistir)
            self._set_checked_silent(self.chk_startup_animation, s.acilis_animasyonu_goster)
            self._set_checked_silent(self.chk_silent, s.sessiz_mod)
            self._set_checked_silent(self.chk_free_layout, s.free_layout_enabled)
            self._set_checked_silent(self.chk_group_locked, s.group_locked)
            self._set_checked_silent(self.chk_multi_mon, s.coklu_monitor_modu)
            self._set_checked_silent(self.chk_alarm_visible, s.alarm_visible)
            self._set_checked_silent(self.chk_reminder_visible, s.reminder_visible)
            self._set_checked_silent(self.chk_todo_visible, s.todo_visible)
            self._set_value_silent(self.sld_opacity, int(s.seffaflik * 100))
            self._set_value_silent(self.spn_opacity_value, int(s.seffaflik * 100))
            self._set_value_silent(self.sld_scale, int(s.global_scale * 100))
            self._set_value_silent(self.spn_scale_value, int(s.global_scale * 100))
            self._set_value_silent(self.spn_quick_icon_size, s.quick_actions_icon_size)
            self._set_value_silent(self.spn_quick_icon_spacing, s.quick_actions_icon_spacing)
        elif tab_name == "Pil":
            self._set_checked_silent(self.chk_batt_visible, s.battery_visible)
            self._set_checked_silent(self.chk_batt_bold, s.battery_bold)
            self._set_value_silent(self.spn_batt_warn, s.battery_warning_level)
            self._set_value_silent(self.spn_batt_interval, s.battery_alert_interval)
            self.cmb_batt_sound.setCurrentText(s.battery_alert_sound_type)
            self.btn_batt_color.setText(s.battery_color)
            self.cmb_batt_font.setCurrentFont(QtGui.QFont(s.battery_font_family))
            self._set_value_silent(self.sld_battery_scale, int(s.battery_scale * 100))
            self._set_value_silent(self.spn_battery_scale, int(s.battery_scale * 100))
        elif tab_name == "Saat":
            self._set_checked_silent(self.chk_time_visible, not s.time_visible)
            self._set_checked_silent(self.chk_time_bold, s.time_bold)
            self._set_checked_silent(self.chk_sec_visible, not s.time_seconds_visible)
            self.cmb_time_format.setCurrentIndex(max(0, self.cmb_time_format.findData(s.time_format_mode)))
            self.cmb_time_font.setCurrentIndex(max(0, self.cmb_time_font.findText(s.time_font_family)))
            self.btn_time_color.setText(s.time_color)
            self._set_value_silent(self.sld_sec_scale, int(s.time_seconds_scale * 100))
            self.lbl_sec_scale_value.setText(f"{int(s.time_seconds_scale * 100)}%")
            self._set_value_silent(self.sld_time_scale, int(s.time_scale * 100))
            self._set_value_silent(self.spn_time_scale, int(s.time_scale * 100))
        elif tab_name == "Tarih":
            self._set_checked_silent(self.chk_date_visible, s.date_visible)
            self._set_checked_silent(self.chk_date_bold, s.date_bold)
            self._set_checked_silent(self.chk_date_week_number, s.date_show_week_number)
            self._set_checked_silent(
                self.chk_date_hicri_first,
                getattr(s, "date_hicri_first", False)
            )
            self._set_checked_silent(
                self.chk_date_both,
                getattr(s, "date_display_mode", "miladi_hicri") == "miladi_hicri"
            )
            self.txt_date_format.setText(s.date_format)
            self.cmb_date_preset.setCurrentIndex(max(0, self.cmb_date_preset.findData(s.date_format)))
            self.cmb_date_font.setCurrentFont(QtGui.QFont(s.date_font_family))
            self.btn_date_color.setText(s.date_color)
            self._set_value_silent(self.sld_date_scale, int(s.date_scale * 100))
            self._set_value_silent(self.spn_date_scale, int(s.date_scale * 100))
            self._set_value_silent(self.sld_date_hicri_scale, int(s.date_hicri_scale * 100))
            self._set_value_silent(self.spn_date_hicri_scale, int(s.date_hicri_scale * 100))

    def _add_help_link(self, form_layout, extra_widget=None):
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
        top = QtWidgets.QVBoxLayout()
        top.setContentsMargins(0, 0, 0, 0)
        top.setSpacing(4)
        row = QtWidgets.QHBoxLayout()
        row.setContentsMargins(0, 0, 30, 0)
        if extra_widget is not None:
            row.addWidget(extra_widget)
        row.addStretch()
        row.addWidget(help_btn)
        top.addLayout(row)
        form_layout.insertRow(0, top)


    def show_help(self):
        idx = self.tabs.currentIndex()
        tab_name = self.tabs.tabText(idx)
        if tab_name == "Genel":
            text = (
                "Özet: Genel görünüm, saydamlık ve grup yerleşimi bu sekmeden yönetilir.\n"
                "\n"
                "Genel ayarlar (sırasıyla):\n"
                "- Her zaman üstte: Pencerenin diğer uygulamaların üstünde kalmasını sağlar.\n"
                "- Açılışta çalıştır: Uygulama Windows açılışında otomatik başlar.\n"
                "- Grup kilitli: Modüller kaydedilmiş grup konumlarını korur ve birlikte taşınır.\n"
                "- Modüller Serbest: Modüller kayıtlı bağımsız konumlarında ayrı ayrı taşınır.\n"
                "- Grup kilidi kapalıyken: Modül üzerine gelerek modülü yeniden konumlandırabilirsiniz.\n"
                "- Şeffaflık (%): Tüm satırların saydamlık seviyesini ayarlar.\n"
                "- Hover ikon boyutu ve aralığı: Hızlı işlem simgelerinin görünümünü ayarlar."
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
                "- Kalın: Pil yazısını kalın yapar."
            )
        elif tab_name == "Saat":
            text = (
                "Özet: Saat satırının görünümü ve saniye ayarları bu sekmeden yönetilir.\n"
                "\n"
                "Saat ayarları (sırasıyla):\n"
                "- Saat görünür: Saat satırını aç/kapat.\n"
                "- Font: Saat yazı tipi.\n"
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

    def _apply_time_preview(self, font=None, bold=None, visible=None, seconds_scale=None, seconds_bold=None, seconds_visible=None, time_24h=None, time_format_mode=None):
        if font is not None: self.settings.time_font_family = font
        if bold is not None: self.settings.time_bold = bold
        if visible is not None: self.settings.time_visible = visible
        if seconds_scale is not None: self.settings.time_seconds_scale = seconds_scale
        if seconds_bold is not None: self.settings.time_seconds_bold = seconds_bold
        if seconds_visible is not None: self.settings.time_seconds_visible = seconds_visible
        if time_24h is not None: self.settings.time_24h = time_24h
        if time_format_mode is not None:
            self.settings.time_format_mode = time_format_mode
            self.settings.time_24h = time_format_mode == "24h"
        self._set_dirty(True)
        if self.parent(): self.parent().apply_settings()

    def _apply_seconds_scale_preview(self, value):
        self.settings.time_seconds_scale = value / 100
        self.lbl_sec_scale_value.setText(f"{value}%")
        self._set_dirty(True)
        if self.parent(): self.parent().apply_settings()

    def _apply_general_preview(self, _=None):
        if hasattr(self, "spn_quick_icon_spacing"):
            self.settings.quick_actions_icon_spacing = self.spn_quick_icon_spacing.value()
        if hasattr(self, "spn_quick_icon_size"):
            self.settings.quick_actions_icon_size = self.spn_quick_icon_size.value()
        self._set_dirty(True)
        if self.parent(): self.parent().apply_settings()

    def _apply_free_layout_preview(self, value):
        if self.parent():
            if value:
                self.parent().enter_free_modules_mode()
            else:
                self.parent().restore_grouped_mode()
            self._set_checked_silent(self.chk_group_locked, self.settings.group_locked)
        else:
            self.settings.free_layout_enabled = bool(value)
        self._set_dirty(True)

    def _apply_group_lock_preview(self, value):
        if self.parent():
            if value:
                self.parent().lock_group_layout()
            else:
                self.parent().enter_group_edit_mode()
        else:
            self.settings.group_locked = bool(value)
        if self.parent():
            self._set_checked_silent(self.chk_free_layout, self.settings.free_layout_enabled)
        self._set_dirty(True)

    def _apply_opacity_preview(self, value):
        self.settings.seffaflik = value / 100
        if hasattr(self, "spn_opacity_value"):
            self.spn_opacity_value.blockSignals(True); self.spn_opacity_value.setValue(value); self.spn_opacity_value.blockSignals(False)
        self._set_dirty(True)
        if self.parent(): self.parent().apply_settings()

    def _apply_visibility_preview(self, field_name, value):
        setattr(self.settings, field_name, bool(value))
        self._set_dirty(True)
        if self.parent():
            self.parent().apply_settings()

    def _apply_scale_preview(self, value):
        self.settings.global_scale = value / 100
        self.spn_scale_value.blockSignals(True); self.spn_scale_value.setValue(value); self.spn_scale_value.blockSignals(False)
        self._set_dirty(True)
        if self.parent(): self.parent().apply_settings()

    def _apply_module_scale_preview(self, hedef_tur, value):
        setattr(self.settings, f"{hedef_tur}_scale", value / 100)
        self._set_dirty(True)
        if self.parent(): self.parent().apply_settings()

    def _apply_date_preview(
        self,
        font=None,
        bold=None,
        visible=None,
        format_text=None,
        week_number=None,
        display_mode=None,
        hicri_first=None,
    ):
        if font is not None: self.settings.date_font_family = font
        if bold is not None: self.settings.date_bold = bold
        if visible is not None: self.settings.date_visible = visible
        if format_text is not None:
            if self._date_format_valid(format_text):
                self.settings.date_format = format_text
                self.txt_date_format.setStyleSheet("")
            else:
                self.txt_date_format.setStyleSheet("border: 1px solid #cc0000;")
        if week_number is not None: self.settings.date_show_week_number = week_number
        if display_mode in {"miladi", "hicri", "miladi_hicri"}:
            self.settings.date_display_mode = display_mode
        if hicri_first is not None:
            self.settings.date_hicri_first = hicri_first
        self._set_dirty(True)
        if self.parent(): self.parent().apply_settings()

    def _date_format_valid(self, fmt):
        fmt = (fmt or "").strip()
        if not fmt:
            return False
        if "%" not in fmt:
            return True
        try:
            datetime.now().strftime(fmt)
            return True
        except Exception:
            return False

    def _apply_batt_preview(self, _=None):
        self.settings.battery_visible = self.chk_batt_visible.isChecked()
        self.settings.battery_font_family = self.cmb_batt_font.currentFont().family()
        self.settings.battery_bold = self.chk_batt_bold.isChecked()
        self.settings.battery_warning_level = self.spn_batt_warn.value()
        self.settings.battery_alert_interval = self.spn_batt_interval.value()
        self.settings.battery_alert_sound_type = self.cmb_batt_sound.currentText()
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
                color = c.name()
                btn.setText(color)
                if btn is getattr(self, "btn_time_color", None):
                    self.settings.time_color = color
                elif btn is getattr(self, "btn_date_color", None):
                    self.settings.date_color = color
                elif btn is getattr(self, "btn_batt_color", None):
                    self.settings.battery_color = color
                self._set_dirty(True)
                if self.parent():
                    self.parent().apply_settings()
                return color
        return None

    def get_settings(self):
        """UI elemanlarından ayarları toplar."""
        # Ayarlar artık preview metodları üzerinden anlık olarak self.settings'e yazılıyor.
        # Sadece line edit'ler gibi anlık tetiklenmeyenleri buradan alıyoruz.
        if hasattr(self, "txt_date_format"):
            fmt = self.txt_date_format.text()
            if self._date_format_valid(fmt):
                self.settings.date_format = fmt
            else:
                QtWidgets.QMessageBox.warning(self, "Tarih Formatı", "Geçersiz tarih formatı kaydedilmedi.")
        if hasattr(self, "chk_date_week_number"):
            self.settings.date_show_week_number = self.chk_date_week_number.isChecked()
        if hasattr(self, "chk_date_both"):
            if self.chk_date_both.isChecked():
                self.settings.date_display_mode = "miladi_hicri"
            elif getattr(self.settings, "date_display_mode", "miladi") not in {"miladi", "hicri"}:
                self.settings.date_display_mode = "miladi"
        if hasattr(self, "chk_date_hicri_first"):
            self.settings.date_hicri_first = self.chk_date_hicri_first.isChecked()
        if hasattr(self, "chk_startup_animation"):
            self.settings.acilis_animasyonu_goster = self.chk_startup_animation.isChecked()
        if hasattr(self, "cmb_language"):
            self.settings.language = self.cmb_language.currentData() or "tr"
        if hasattr(self, "tbl_task_priorities"):
            self._sync_task_priorities_from_table()
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
