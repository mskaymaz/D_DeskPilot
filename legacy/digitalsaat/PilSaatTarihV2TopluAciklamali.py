"""
PilSaatTarihV2TopluAciklamali
Tek dosyalık sürüm (toplu açıklamalı).

Bu dosya şu modüllerin birleşimidir:
- utils.py (yardımcı fonksiyonlar ve sabitler)
- core_settings.py (ayar modeli ve dosyaya kaydetme/yükleme)
- core_window.py (ana pencere ve pil/saat/tarih çizimi)
- ui_settings.py (Ayarlar penceresi)
- DeskPilot.py (uygulama giriş noktası)

Not: Yorumlar acemi seviyesine uygun, adım adım açıklamalar içerir.
"""

# =============================
# 1) STANDART KÜTÜPHANE İTHALATLARI
# =============================
# Bu importlar Python ile gelen temel modüllerdir.
import sys  # Program çalışma bilgileri
import os  # Dosya/dizin işlemleri
import json  # Ayarları JSON formatında kaydetmek/okumak
import locale  # Tarih/saat dilini Türkçe yapmak
import time  # Zaman ve bekleme ölçümleri
import ctypes  # Windows özel API erişimleri
import winreg  # Windows kayıt defteri (autostart)
from dataclasses import dataclass, asdict  # Ayar modelini sade yazmak
from datetime import datetime  # Şu anki tarih/saat bilgisi

# =============================
# 2) ÜÇÜNCÜ PARTİ KÜTÜPHANELER
# =============================
# PySide6 yoksa PyQt6 denenir (aynı API).
try:
    from PySide6 import QtCore, QtGui, QtWidgets
except ImportError:
    from PyQt6 import QtCore, QtGui, QtWidgets

# Pil bilgisi için psutil kullanılır. Kurulu değilse None olur.
try:
    import psutil
except ImportError:
    psutil = None

# Windows ses uyarıları için winsound kullanılır.
try:
    if sys.platform == "win32":
        import winsound
    else:
        winsound = None
except Exception:
    winsound = None

# =============================
# 3) UYGULAMA SABİTLERİ
# =============================
# Bu sabitler uygulama kimliği ve dosya yollarını belirler.
APP_NAME = "DigitalSaat"
APP_ID = "MSK.DigitalSaat"
APP_DATA_DIR = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), APP_NAME)
SETTINGS_FILE = os.path.join(APP_DATA_DIR, "settings.json")
ICON_FILE = "deskpilot.ico"
RUN_REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"

# =============================
# 4) YARDIMCI FONKSİYONLAR
# =============================
# Bu bölümde sık kullanılan küçük işlemler toplanır.
# AÇIKLAMA: Paketlenmiş exe veya kaynak klasörü için doğru dosya yolunu döndürür.
def resource_path(relative_path: str) -> str:
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)


# AÇIKLAMA: Uygulamayı başlatacak komut satırını oluşturur.
def _get_autostart_command():
    if getattr(sys, "frozen", False):
        return f"\"{sys.executable}\""
    script_path = os.path.abspath(sys.argv[0])
    return f"\"{sys.executable}\" \"{script_path}\""


# AÇIKLAMA: Windows başlangıç kaydını ekler/siler.
def set_autostart(enabled: bool):
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_REG_PATH, 0, winreg.KEY_SET_VALUE) as key:
            if enabled:
                winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, _get_autostart_command())
            else:
                try:
                    winreg.DeleteValue(key, APP_NAME)
                except FileNotFoundError:
                    pass
        return True
    except Exception:
        return False

# =============================
# 5) AYARLAR MODELİ VE DOSYA İŞLEMLERİ
# =============================
@dataclass
# SINIF AÇIKLAMA: Uygulamanın tüm ayarlarını tek yerde tutan veri sınıfı (dataclass).
class PanelSettings:
    # AÇIKLAMA: Ayarlar kilitliyse sürükleme ve konum değişimi engellenir.
    settings_locked: bool = False
    # AÇIKLAMA: Pencere saydamlık oranı (0.0 - 1.0 arası).
    seffaflik: float = 0.85
    # AÇIKLAMA: Pencere her zaman diğer uygulamaların üstünde kalsın mı?
    her_zaman_ustte: bool = True
    # AÇIKLAMA: Windows açılışında uygulama otomatik başlasın mı?
    acilista_calistir: bool = True

    # AÇIKLAMA: Saat satırı görünsün mü?
    time_visible: bool = True
    # AÇIKLAMA: Saat yazı tipi adı.
    time_font_family: str = "Segoe UI"
    # AÇIKLAMA: Saat yazı boyutu (piksel).
    time_font_size: int = 30
    # AÇIKLAMA: Saat yazı rengi (HEX).
    time_color: str = "#00FF7F"
    # AÇIKLAMA: Saat yazısı kalın mı?
    time_bold: bool = False
    # AÇIKLAMA: Saniye boyutu, saat boyutuna oranı.
    time_seconds_scale: float = 0.7
    # AÇIKLAMA: Saniye yazısı kalın mı?
    time_seconds_bold: bool = False
    # AÇIKLAMA: Saniye kısmı görünsün mü?
    time_seconds_visible: bool = True

    # AÇIKLAMA: Tarih satırı görünsün mü?
    date_visible: bool = True
    # AÇIKLAMA: Tarih formatı (özel kısa format veya strftime).
    date_format: str = "g a y, h"
    # AÇIKLAMA: Tarih yazı tipi adı.
    date_font_family: str = "Segoe UI"
    # AÇIKLAMA: Tarih yazı rengi (HEX).
    date_color: str = "#000000"
    # AÇIKLAMA: Tarih yazı boyutu (piksel).
    date_font_size: int = 30
    # AÇIKLAMA: Tarih yazısı kalın mı?
    date_bold: bool = False

    # AÇIKLAMA: Pil satırı görünsün mü?
    battery_visible: bool = True
    # AÇIKLAMA: Pil yazı tipi adı.
    battery_font_family: str = "Segoe UI"
    # AÇIKLAMA: Pil yazı rengi (HEX).
    battery_color: str = "#FF0000"
    # AÇIKLAMA: Pil yazısı kalın mı?
    battery_bold: bool = True
    # AÇIKLAMA: Pil uyarı seviyesi (%).
    battery_warning_level: int = 20
    # AÇIKLAMA: Uyarı sesi tekrar aralığı (saniye).
    battery_alert_interval: int = 10
    # AÇIKLAMA: Pil yazı boyutu (piksel).
    battery_font_size: int = 30
    # AÇIKLAMA: Uyarı ses tipi (Uyarı 1/2/3).
    battery_alert_sound_type: str = "Uyarı 1"
    # AÇIKLAMA: Tam dolu uyarısı aktif mi?
    battery_full_alert_enabled: bool = False
    # AÇIKLAMA: Tam dolu uyarı seviyesi (%).
    battery_full_alert_level: int = 100

    # --- Ayrı dikey boşluklar ---
    # AÇIKLAMA: Pil ↔ Saat dikey boşluğu.
    spacing_battery_time: int = 0
    # AÇIKLAMA: Saat ↔ Tarih dikey boşluğu.
    spacing_time_date: int = 0
    # AÇIKLAMA: Saat kapalıyken Pil ↔ Tarih boşluğu.
    spacing_battery_date_hidden: int = 2

    # --- Ayrı seffafliklar ---
    # AÇIKLAMA: Tarih satırı saydamlığı.
    date_opacity: float = 1.0
    # AÇIKLAMA: Pil satırı saydamlığı.
    battery_opacity: float = 1.0

    # --- Pencere pozisyonu ---
    # AÇIKLAMA: Pencerenin X konumu (sol).
    pos_x: int = 0
    # AÇIKLAMA: Pencerenin Y konumu (üst).
    pos_y: int = 0
    # AÇIKLAMA: Serbest dağıt modu açık mı?
    free_layout_enabled: bool = False
    # AÇIKLAMA: Serbest konumlar kaydedildi mi?
    free_layout_has_positions: bool = False
    # AÇIKLAMA: Saat satırının serbest X konumu.
    free_time_x: int = 0
    # AÇIKLAMA: Saat satırının serbest Y konumu.
    free_time_y: int = 0
    # AÇIKLAMA: Tarih satırının serbest X konumu.
    free_date_x: int = 0
    # AÇIKLAMA: Tarih satırının serbest Y konumu.
    free_date_y: int = 0
    # AÇIKLAMA: Pil satırının serbest X konumu.
    free_battery_x: int = 0
    # AÇIKLAMA: Pil satırının serbest Y konumu.
    free_battery_y: int = 0




# AÇIKLAMA: Ayar anahtarlarını ASCII ve standart isimlere çevirir.
def _normalize_key(key: str) -> str:
    tr_map = str.maketrans({
        "ş": "s", "Ş": "s",
        "ç": "c", "Ç": "c",
        "ğ": "g", "Ğ": "g",
        "ü": "u", "Ü": "u",
        "ö": "o", "Ö": "o",
        "ı": "i", "İ": "i",
    })
    lk = key.translate(tr_map).lower()
    if "seffaf" in lk:
        return "seffaflik"
    if "zaman" in lk and "ustte" in lk:
        return "her_zaman_ustte"
    if "acilista" in lk and "calistir" in lk:
        return "acilista_calistir"
    return key


# AÇIKLAMA: settings.json dosyasını okur ve PanelSettings olarak yükler.
def load_settings():
    if os.path.isfile(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    data = { _normalize_key(k): v for k, v in data.items() }
                    allowed = set(PanelSettings.__dataclass_fields__.keys())
                    data = {k: v for k, v in data.items() if k in allowed}
                return PanelSettings(**data)
        except Exception:
            pass
    return PanelSettings()


# AÇIKLAMA: PanelSettings nesnesini settings.json olarak kaydeder.
def save_settings(settings: PanelSettings):
    os.makedirs(APP_DATA_DIR, exist_ok=True)
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(asdict(settings), f, ensure_ascii=False, indent=2)

# =============================
# 6) ANA PENCERE VE GÖRSEL KATMAN
# =============================
# AÇIKLAMA: Pencereyi ekran içine güvenli şekilde taşır.
def move_window_safely(window, settings):
    app = QtWidgets.QApplication.instance()
    screen = app.screenAt(QtGui.QCursor.pos()) or app.primaryScreen()
    rect = screen.availableGeometry()

    window.adjustSize()
    w, h = window.width(), window.height()

    x, y = settings.pos_x, settings.pos_y

    if not rect.contains(QtCore.QPoint(x, y)):
        x = rect.left() + (rect.width() - w) // 2
        y = rect.top() + (rect.height() - h) // 2
        settings.pos_x = x
        settings.pos_y = y
        save_settings(settings)

    window.move(x, y)


"""
GÖREV ÇUBUĞU ÜSTÜNDE KALMA DAVRANIŞI (QT SÜRÜMÜ)

AMAÇ:
- Serbest dağıt modunda kullanıcı pencereyi görev çubuğu bandına sürüklerse,
  pencere "üstte kalma" davranışını sürekli korusun.
- Uygulama, otomatik olarak görev çubuğuna taşıma YAPMAZ.
  Yani kullanıcı taşımadıysa, pencere normal konumunda kalır.

NASIL ÇALIŞIR:
1) Ekranın "geometry" ve "availableGeometry" farkından görev çubuğu bandı hesaplanır.
2) Pencere bu banda değiyorsa, periyodik olarak topmost (HWND_TOPMOST) zorlanır.
3) Pencere bandın dışına çıkınca bu zorlamayı durdurur.
"""

# AÇIKLAMA: Windows üzerinde bir pencereyi "topmost" yapar (görev çubuğu üstünde kalması için).
def _enforce_topmost(window):
    if sys.platform != "win32":
        return
    try:
        hwnd = int(window.winId())
    except Exception:
        return
    # AÇIKLAMA: HWND_TOPMOST ile pencereyi en üst seviyeye çıkar.
    HWND_TOPMOST = -1
    SWP_NOMOVE = 0x0002
    SWP_NOSIZE = 0x0001
    SWP_NOACTIVATE = 0x0010
    SWP_SHOWWINDOW = 0x0040
    ctypes.windll.user32.SetWindowPos(
        hwnd,
        HWND_TOPMOST,
        0,
        0,
        0,
        0,
        SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE | SWP_SHOWWINDOW,
    )


# AÇIKLAMA: Ekrandaki görev çubuğu bandlarını hesaplar (üst/alt/sol/sağ olabilir).
# Not: Qt ile her monitör için geometry ve availableGeometry farkı kullanılır.
def _taskbar_bands_for_screen(screen):
    if not screen:
        return []
    geo = screen.geometry()
    avail = screen.availableGeometry()
    bands = []

    # Üstte görev çubuğu varsa: available top, geometry top'tan büyük olur.
    top_h = avail.top() - geo.top()
    if top_h > 0:
        bands.append(QtCore.QRect(geo.left(), geo.top(), geo.width(), top_h))

    # Altta görev çubuğu varsa: geometry bottom, available bottom'dan büyük olur.
    bottom_h = geo.bottom() - avail.bottom()
    if bottom_h > 0:
        bands.append(
            QtCore.QRect(
                geo.left(),
                avail.bottom() + 1,
                geo.width(),
                bottom_h,
            )
        )

    # Solda görev çubuğu varsa:
    left_w = avail.left() - geo.left()
    if left_w > 0:
        bands.append(QtCore.QRect(geo.left(), geo.top(), left_w, geo.height()))

    # Sağda görev çubuğu varsa:
    right_w = geo.right() - avail.right()
    if right_w > 0:
        bands.append(
            QtCore.QRect(
                avail.right() + 1,
                geo.top(),
                right_w,
                geo.height(),
            )
        )

    return bands


# AÇIKLAMA: Pencere görev çubuğu bandına denk geliyor mu?
def _is_window_on_taskbar(window):
    app = QtWidgets.QApplication.instance()
    screen = app.screenAt(window.frameGeometry().center()) if app else None
    if not screen and app:
        screen = app.primaryScreen()
    if not screen:
        return False
    rect = window.frameGeometry()
    for band in _taskbar_bands_for_screen(screen):
        if rect.intersects(band):
            return True
    return False



# =======================
# SERBEST SATIR PENCERESI
# =======================

# SINIF AÇIKLAMA: Serbest dağıt modunda her satırın ayrı pencere olduğu yapı.
class FreeLineWindow(QtWidgets.QWidget):
    # AÇIKLAMA: Sınıfın başlangıç kurulumunu yapar (ilk ayar ve arayüz kurulumları).
    def __init__(self, kind, settings, controller):
        super().__init__(None)
        self.kind = kind
        self.settings = settings
        self.controller = controller
        self.drag_pos = None
        # AÇIKLAMA: Görev çubuğu üstünde kaldığında sürekli topmost zorlamak için timer.
        self._keep_top_timer = None

        self._apply_window_flags()
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowOpacity(self.settings.seffaflik)
        self.setWindowIcon(QtGui.QIcon(resource_path(ICON_FILE)))

        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_menu)

        self._build_ui()
        # AÇIKLAMA: Görev çubuğu üstünde kalma davranışını hazırla.
        self._setup_keep_on_top()

    # AÇIKLAMA: Pencere bayraklarını (çerçevesiz, üstte vb.) uygular.
    def _apply_window_flags(self):
        flags = QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.Tool
        if self.settings.her_zaman_ustte:
            flags |= QtCore.Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(flags)

    # AÇIKLAMA: İçerik ve yerleşimi (layout) oluşturur.
    def _build_ui(self):
        if self.kind == "battery":
            self.battery_label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
            self.battery_icon_label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
            self.battery_icon_label.setVisible(False)

            row = QtWidgets.QWidget()
            row_layout = QtWidgets.QHBoxLayout(row)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(4)
            row_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            row_layout.addWidget(self.battery_label)
            row_layout.addWidget(self.battery_icon_label)
            self.content = row
        else:
            self.label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
            self.content = self.label

        for lbl in self._labels():
            lbl.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
            lbl.setContentsMargins(0, 0, 0, 0)
            lbl.setStyleSheet(
                """
                QLabel {
                    padding: 0px;
                    margin: 0px;
                }
                """
            )

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.content)

    # AÇIKLAMA: Etiket(ler)i döndürür.
    def _labels(self):
        if self.kind == "battery":
            return (self.battery_label, self.battery_icon_label)
        return (self.label,)

    # AÇIKLAMA: Bayrakları ve saydamlığı yeniler.
    def refresh_flags_and_opacity(self):
        was_visible = self.isVisible()
        self._apply_window_flags()
        self.setWindowOpacity(self.settings.seffaflik)
        if was_visible:
            self.show()
        # AÇIKLAMA: Bayraklar yenilenince görev çubuğu kontrolünü tekrar yap.
        self._update_keep_on_top()

    # AÇIKLAMA: Sağ tık menüsünü gösterir.
    def _show_menu(self, pos):
        global_pos = self.mapToGlobal(pos)
        anchor_pos = self.frameGeometry().topLeft()
        self.controller.show_menu_at(global_pos, anchor_pos)

    # AÇIKLAMA: Sürükleme başlangıcı.
    def mousePressEvent(self, e):
        if self.settings.settings_locked:
            return
        if e.button() == QtCore.Qt.MouseButton.LeftButton:
            self.drag_pos = e.globalPosition().toPoint() - self.frameGeometry().topLeft()

    # AÇIKLAMA: Sürükleme sırasında konumu günceller.
    def mouseMoveEvent(self, e):
        if self.settings.settings_locked:
            return
        if self.drag_pos:
            self.move(e.globalPosition().toPoint() - self.drag_pos)
            # AÇIKLAMA: Kullanıcı sürüklerken görev çubuğu bandına girip girmediğini kontrol et.
            self._update_keep_on_top()

    # AÇIKLAMA: Sürükleme bitişinde konumu kaydeder.
    def mouseReleaseEvent(self, e):
        if self.settings.settings_locked:
            self.drag_pos = None
            return
        if self.drag_pos:
            self.drag_pos = None
            self.controller.update_free_position(self.kind, self.x(), self.y())
            # AÇIKLAMA: Sürükleme bitti; görev çubuğu üstünde kalma gerekiyorsa devreye al.
            self._update_keep_on_top()

    # AÇIKLAMA: Görev çubuğu üstünde kalma için timer kurulumunu yapar.
    def _setup_keep_on_top(self):
        if not self._keep_top_timer:
            self._keep_top_timer = QtCore.QTimer(self)
            self._keep_top_timer.setInterval(100)  # 0.1 sn: Windows z-order değişimlerini yakalamak için
            self._keep_top_timer.timeout.connect(self._keep_on_top_tick)
        self._update_keep_on_top()

    # AÇIKLAMA: Pencere görev çubuğu bandında mı? Öyleyse topmost zorlamayı başlat.
    def _update_keep_on_top(self):
        # ÖNEMLİ: Kullanıcı görev çubuğuna taşımadıysa hiç devreye girmesin.
        should_keep = self.isVisible() and _is_window_on_taskbar(self)
        if should_keep:
            if not self._keep_top_timer.isActive():
                self._keep_top_timer.start()
            _enforce_topmost(self)
            self.raise_()
        else:
            if self._keep_top_timer.isActive():
                self._keep_top_timer.stop()

    # AÇIKLAMA: Periyodik topmost zorlaması.
    def _keep_on_top_tick(self):
        if not self.isVisible():
            if self._keep_top_timer.isActive():
                self._keep_top_timer.stop()
            return
        if not _is_window_on_taskbar(self):
            if self._keep_top_timer.isActive():
                self._keep_top_timer.stop()
            return
        _enforce_topmost(self)
        self.raise_()

    # AÇIKLAMA: Pencere görünür olunca görev çubuğu kontrolünü güncelle.
    def showEvent(self, e):
        super().showEvent(e)
        self._update_keep_on_top()

    # AÇIKLAMA: Pencere gizlenince topmost zorlamayı durdur.
    def hideEvent(self, e):
        super().hideEvent(e)
        self._update_keep_on_top()


# =======================
# ANA PENCERE
# =======================

# SINIF AÇIKLAMA: Ana pencere: sürükleme, stil, uyarı ve içerik yönetimi burada yapılır.
class DraggableTransparentWindow(QtWidgets.QWidget):
    # AÇIKLAMA: Sınıfın başlangıç kurulumunu yapar (ilk ayar ve arayüz kurulumları).
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

        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_menu)

        self.apply_settings()
        self.update_time()
        self.update_battery()

    # ---------- AYARLAR ---------- *****************


    # AÇIKLAMA: Ayarları tüm etiketlere ve pencerelere uygular.
    def apply_settings(self):
        self._apply_window_flags()

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
                self.free_battery_window.battery_label,
                self.free_battery_window.battery_icon_label
            )
            self.free_battery_window.setVisible(
                self.settings.free_layout_enabled and self.settings.battery_visible
            )
            self.free_battery_window.battery_icon_label.setVisible(self.settings.battery_visible)

        self._set_battery_color(self.settings.battery_color)
        self._refresh_battery_rows()

        # --- Spacer guncelle ---
        if self.settings.time_visible:
            bt_space = self.settings.spacing_battery_time
            td_space = self.settings.spacing_time_date
        else:
            # Saat yok -> pil ile tarih birbirine yakin olsun
            bt_space = 0
            td_space = self.settings.spacing_battery_date_hidden

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

    # AÇIKLAMA: Label yüksekliğini fonta göre sabitler.
    def _lock_label_height(self, label, font_size):
        fm = QtGui.QFontMetrics(label.font())
        h = fm.ascent() + fm.descent()
        label.setFixedHeight(h)

    # AÇIKLAMA: Pencere bayraklarını (çerçevesiz, üstte vb.) uygular.
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

    # AÇIKLAMA: Saat etiket stilini uygular.
    def _apply_time_style(self, label):
        font_main = QtGui.QFont(
            self.settings.time_font_family,
            self.settings.time_font_size
        )
        font_main.setBold(self.settings.time_bold)
        label.setFont(font_main)
        label.setStyleSheet(
            f"""
            QLabel {{
                color: {self.settings.time_color};
                line-height: {self.settings.time_font_size}px;
                padding: 0px;
                margin: 0px;
            }}
            """
        )

    # AÇIKLAMA: Tarih etiket stilini uygular.
    def _apply_date_style(self, label):
        df = QtGui.QFont(
            self.settings.date_font_family,
            self.settings.date_font_size
        )
        df.setBold(self.settings.date_bold)
        label.setFont(df)
        label.setStyleSheet(
            f"color:{self.settings.date_color};"
            f"opacity:{self.settings.date_opacity};"
        )
        self._lock_label_height(label, self.settings.date_font_size)

    # AÇIKLAMA: Pil etiket stilini uygular.
    def _apply_battery_style(self, label, icon_label):
        bf = QtGui.QFont(
            self.settings.battery_font_family,
            self.settings.battery_font_size
        )
        bf.setBold(self.settings.battery_bold)
        label.setFont(bf)
        label.setStyleSheet(
            f"color:{self.settings.battery_color};"
            f"opacity:{self.settings.battery_opacity};"
        )
        self._lock_label_height(label, self.settings.battery_font_size)

        icon_size = max(1.0, float(self.settings.battery_font_size) * 0.8)
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

    # AÇIKLAMA: Pil satırı layoutunu yeniler.
    def _refresh_battery_rows(self):
        self.battery_row_layout.invalidate()
        self.battery_row.adjustSize()
        self.battery_row.updateGeometry()
        if self.free_battery_window:
            self.free_battery_window.content.adjustSize()
            self.free_battery_window.adjustSize()
            self.free_battery_window.updateGeometry()

    # AÇIKLAMA: Serbest dağıt pencerelerini oluşturur.
    def _ensure_free_windows(self):
        created = False
        if not self.free_time_window:
            self.free_time_window = FreeLineWindow("time", self.settings, self)
            created = True
        if not self.free_date_window:
            self.free_date_window = FreeLineWindow("date", self.settings, self)
            created = True
        if not self.free_battery_window:
            self.free_battery_window = FreeLineWindow("battery", self.settings, self)
            created = True
        if created:
            self._apply_free_window_styles()

    # AÇIKLAMA: Serbest pencerelere stil uygular.
    def _apply_free_window_styles(self):
        if self.free_time_window:
            self._apply_time_style(self.free_time_window.label)
        if self.free_date_window:
            self._apply_date_style(self.free_date_window.label)
        if self.free_battery_window:
            self._apply_battery_style(
                self.free_battery_window.battery_label,
                self.free_battery_window.battery_icon_label
            )
            self._set_battery_color(self.settings.battery_color)
            self._refresh_battery_rows()

    # AÇIKLAMA: Pencereyi ekran sınırlarında tutar.
    def _clamp_window_position(self, window, x, y, allow_taskbar=False):
        app = QtWidgets.QApplication.instance()
        screen = app.screenAt(QtCore.QPoint(x, y)) or app.primaryScreen()
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

    # AÇIKLAMA: Serbest satır penceresini güvenli taşır.
    def _move_line_window_safely(self, window, x, y):
        x, y = self._clamp_window_position(window, x, y, allow_taskbar=True)
        window.move(x, y)

    # AÇIKLAMA: Serbest konumları gruptan yakalar.
    def _capture_free_positions_from_grouped(self):
        time_global = self.mapToGlobal(self.time_label.pos())
        date_global = self.mapToGlobal(self.date_label.pos())
        battery_global = self.mapToGlobal(self.battery_row.pos())

        self.settings.free_time_x = time_global.x()
        self.settings.free_time_y = time_global.y()
        self.settings.free_date_x = date_global.x()
        self.settings.free_date_y = date_global.y()
        self.settings.free_battery_x = battery_global.x()
        self.settings.free_battery_y = battery_global.y()
        self.settings.free_layout_has_positions = True
        save_settings(self.settings)

    # AÇIKLAMA: Serbest pencereleri gösterir.
    def _show_free_windows(self):
        self._ensure_free_windows()

        self._move_line_window_safely(
            self.free_time_window,
            self.settings.free_time_x,
            self.settings.free_time_y
        )
        self._move_line_window_safely(
            self.free_date_window,
            self.settings.free_date_x,
            self.settings.free_date_y
        )
        self._move_line_window_safely(
            self.free_battery_window,
            self.settings.free_battery_x,
            self.settings.free_battery_y
        )

        if self.settings.time_visible:
            self.free_time_window.show()
        if self.settings.date_visible:
            self.free_date_window.show()
        if self.settings.battery_visible:
            self.free_battery_window.show()

    # AÇIKLAMA: Serbest pencereleri gizler.
    def _hide_free_windows(self):
        if self.free_time_window:
            self.free_time_window.hide()
        if self.free_date_window:
            self.free_date_window.hide()
        if self.free_battery_window:
            self.free_battery_window.hide()

    # AÇIKLAMA: Gruplu pencereyi saat konumuna taşır.
    def _move_grouped_to_time_position(self):
        if not self.settings.free_layout_has_positions:
            return
        target_x = self.settings.free_time_x - self.time_label.pos().x()
        target_y = self.settings.free_time_y - self.time_label.pos().y()
        target_x, target_y = self._clamp_window_position(self, target_x, target_y)
        self.move(target_x, target_y)
        self.settings.pos_x = target_x
        self.settings.pos_y = target_y
        save_settings(self.settings)

    # AÇIKLAMA: Serbest dağıt modunu uygular.
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

    # AÇIKLAMA: Serbest pencerelerin konumunu kaydeder.
    def update_free_position(self, kind, x, y):
        if self.settings.settings_locked:
            return
        if kind == "time":
            self.settings.free_time_x = x
            self.settings.free_time_y = y
        elif kind == "date":
            self.settings.free_date_x = x
            self.settings.free_date_y = y
        elif kind == "battery":
            self.settings.free_battery_x = x
            self.settings.free_battery_y = y
        self.settings.free_layout_has_positions = True
        save_settings(self.settings)

    # AÇIKLAMA: Sağ tık menüsünü verilen koordinatta gösterir.
    def show_menu_at(self, global_pos, settings_anchor_pos=None):
        menu = QtWidgets.QMenu(self)
        if self.settings.settings_locked:
            act_settings = menu.addAction("Ayarlar (kilitli)")
            act_settings.setEnabled(False)
        else:
            act_settings = menu.addAction("Ayarlar")
        act_exit = menu.addAction("Çıkış")
        action = menu.exec(global_pos)
        if action == act_settings and not self.settings.settings_locked:
            self.show_settings_at(settings_anchor_pos)
        elif action == act_exit:
            QtWidgets.QApplication.quit()

    # AÇIKLAMA: Ayarlar penceresini istenen noktada açar.
    def show_settings_at(self, anchor_pos=None):
        if self.settings.settings_locked:
            return
        self.settings_window = SettingsDialog(self.settings, self)
        if anchor_pos is not None:
            self.position_settings_window_at(self.settings_window, anchor_pos)
        else:
            self.position_settings_window(self.settings_window)
        self.settings_window.show()
        self.settings_window.raise_()

    # AÇIKLAMA: Ayarlar penceresini bir noktaya hizalar.
    def position_settings_window_at(self, dialog, anchor_pos):
        app = QtWidgets.QApplication.instance()
        screen = app.screenAt(anchor_pos) or app.primaryScreen()
        rect = screen.availableGeometry()

        dialog.adjustSize()
        dw, dh = dialog.width(), dialog.height()

        x = anchor_pos.x()
        y = anchor_pos.y()

        if x + dw > rect.right():
            x = rect.right() - dw
        if y + dh > rect.bottom():
            y = rect.bottom() - dh
        if x < rect.left():
            x = rect.left()
        if y < rect.top():
            y = rect.top()

        dialog.move(x, y)


    # AÇIKLAMA: Ayarlar penceresini pencere yanına hizalar.
    def position_settings_window(self, dialog):
        app = QtWidgets.QApplication.instance()

        screen = app.screenAt(self.frameGeometry().center())
        if not screen:
            screen = app.primaryScreen()

        rect = screen.availableGeometry()

        dialog.adjustSize()
        dw, dh = dialog.width(), dialog.height()

        # Varsayılan: pencerenin SAĞINDA aç
        x = self.x() + self.width() + 10
        y = self.y()

        # Sağdan taşarsa → SOLA al
        if x + dw > rect.right():
            x = self.x() - dw - 10

        # Soldan taşarsa → ekran içine sabitle
        if x < rect.left():
            x = rect.left()

        # Alttan taşarsa → yukarı al
        if y + dh > rect.bottom():
            y = rect.bottom() - dh

        # Üstten taşarsa → aşağı sabitle
        if y < rect.top():
            y = rect.top()

        dialog.move(x, y)



    # ---------- MENÜ ----------

    # AÇIKLAMA: Sağ tık menüsünü gösterir.
    def show_menu(self, pos):
        self.show_menu_at(self.mapToGlobal(pos))





    # ---------- GÜNCELLEMELER ----------

    # AÇIKLAMA: Saat ve tarih metnini günceller.
    def update_time(self):
        now = datetime.now()
        time_text = self._format_time_html(now)
        date_text = self._format_date(now)
        self.time_label.setText(time_text)
        self.date_label.setText(date_text)
        if self.free_time_window:
            self.free_time_window.label.setText(time_text)
        if self.free_date_window:
            self.free_date_window.label.setText(date_text)

    # AÇIKLAMA: Pil durumunu günceller ve uyarıları yönetir.
    def update_battery(self):
        if not psutil or not self.settings.battery_visible:
            # Ensure icon hides when battery line is hidden.
            self.battery_icon_label.setVisible(False)
            if self.free_battery_window:
                self.free_battery_window.battery_icon_label.setVisible(False)
            self._stop_full_charge_blink()
            self._stop_low_batt_blink()
            return
        b = psutil.sensors_battery()
        if not b:
            self._stop_full_charge_blink()
            self._stop_low_batt_blink()
            return
        if b.power_plugged:
            self.battery_icon_label.setText("\u26A1")
            self.battery_icon_label.setVisible(True)
            if self.free_battery_window:
                self.free_battery_window.battery_icon_label.setText("\u26A1")
                self.free_battery_window.battery_icon_label.setVisible(True)
        else:
            self.battery_icon_label.setVisible(False)
            if self.free_battery_window:
                self.free_battery_window.battery_icon_label.setVisible(False)
        batt_text = f"Pil: {int(b.percent)}%"
        self.battery_label.setText(batt_text)
        if self.free_battery_window:
            self.free_battery_window.battery_label.setText(batt_text)

        full_alert = (
            self.settings.battery_full_alert_enabled
            and b.power_plugged
            and int(b.percent) >= self.settings.battery_full_alert_level
        )
        low_alert = (not b.power_plugged) and int(b.percent) <= self.settings.battery_warning_level

        if full_alert:
            self._stop_low_batt_blink()
            if not self.full_charge_timer.isActive():
                self._full_charge_blink_on = False
                self.full_charge_timer.start()
            now_ts = time.time()
            if now_ts - self._last_full_batt_alert_ts >= self.settings.battery_alert_interval:
                self._play_batt_alert_sound()
                self._last_full_batt_alert_ts = now_ts
        else:
            self._stop_full_charge_blink()
            self._last_full_batt_alert_ts = 0

        if low_alert and not full_alert:
            if not self.low_batt_timer.isActive():
                self._low_batt_blink_on = False
                self.low_batt_timer.start()
            now_ts = time.time()
            if now_ts - self._last_low_batt_alert_ts >= self.settings.battery_alert_interval:
                self._play_batt_alert_sound()
                self._last_low_batt_alert_ts = now_ts
        else:
            self._stop_low_batt_blink()
            self._last_low_batt_alert_ts = 0

    # AÇIKLAMA: Pil rengini uygular (normal/uyarı).
    def _set_battery_color(self, color):
        self.battery_label.setStyleSheet(
            f"color:{color};"
            f"opacity:{self.settings.battery_opacity};"
        )
        icon_size = max(1.0, float(self.settings.battery_font_size) * 0.8)
        self.battery_icon_label.setStyleSheet(
            f"color:{color};"
            f"opacity:{self.settings.battery_opacity};"
            f"font-size:{icon_size}px;"
            "font-family:'Segoe UI Symbol';"
        )
        if self.free_battery_window:
            self.free_battery_window.battery_label.setStyleSheet(
                f"color:{color};"
                f"opacity:{self.settings.battery_opacity};"
            )
            self.free_battery_window.battery_icon_label.setStyleSheet(
                f"color:{color};"
                f"opacity:{self.settings.battery_opacity};"
                f"font-size:{icon_size}px;"
                "font-family:'Segoe UI Symbol';"
            )

    # AÇIKLAMA: Saat metnini HTML ile formatlar.
    def _format_time_html(self, now):
        base_size = self.settings.time_font_size
        sec_size = max(1, int(base_size * self.settings.time_seconds_scale))
        weight = "bold" if self.settings.time_bold else "normal"
        sec_weight = "bold" if self.settings.time_seconds_bold else "normal"
        family = self.settings.time_font_family
        color = self.settings.time_color
        hhmm = now.strftime("%H:%M")
        ss = now.strftime("%S")
        if not self.settings.time_seconds_visible:
            return (
                f"<span style='font-family:{family};"
                f" font-size:{base_size}px;"
                f" font-weight:{weight};"
                f" color:{color};'>{hhmm}</span>"
            )
        return (
            f"<span style='font-family:{family};"
            f" font-size:{base_size}px;"
            f" font-weight:{weight};"
            f" color:{color};'>{hhmm}</span>"
            f"<span style='font-family:{family};"
            f" font-size:{sec_size}px;"
            f" font-weight:{sec_weight};"
            f" color:{color};'>:{ss}</span>"
        )

    # AÇIKLAMA: Tarihi formatlar (özel kısa format/strftime).
    def _format_date(self, now):
        fmt = self.settings.date_format
        if "%" in fmt:
            return now.strftime(fmt)
        mapping = {
            "g": "%d",
            "G": "%d",
            "a": "%b",
            "A": "%B",
            "y": "%y",
            "Y": "%Y",
            "h": "%a",
            "H": "%A",
        }
        out = []
        for ch in fmt:
            out.append(mapping.get(ch, ch))
        return now.strftime("".join(out))

    # AÇIKLAMA: Tam dolu uyarısını durdurur.
    def _stop_full_charge_blink(self):
        if self.full_charge_timer.isActive():
            self.full_charge_timer.stop()
        if self._full_charge_blink_on:
            self._full_charge_blink_on = False
        self._set_battery_color(self.settings.battery_color)

    # AÇIKLAMA: Tam dolu uyarısını yanıp söndürür.
    def _toggle_full_charge_blink(self):
        self._full_charge_blink_on = not self._full_charge_blink_on
        color = "#00cc66" if self._full_charge_blink_on else self.settings.battery_color
        self._set_battery_color(color)

    # AÇIKLAMA: Düşük pil uyarısını durdurur.
    def _stop_low_batt_blink(self):
        if self.low_batt_timer.isActive():
            self.low_batt_timer.stop()
        if self._low_batt_blink_on:
            self._low_batt_blink_on = False
        self._set_battery_color(self.settings.battery_color)

    # AÇIKLAMA: Düşük pil uyarısını yanıp söndürür.
    def _toggle_low_batt_blink(self):
        self._low_batt_blink_on = not self._low_batt_blink_on
        color = "#cc0000" if self._low_batt_blink_on else self.settings.battery_color
        self._set_battery_color(color)

    # AÇIKLAMA: Pil uyarısı sesi çalar.
    def _play_batt_alert_sound(self):
        if not winsound:
            return
        sound = self.settings.battery_alert_sound_type
        if sound == "Uyarı 2":
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        elif sound == "Uyarı 3":
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
        else:
            winsound.MessageBeep(winsound.MB_ICONHAND)

    # ---------- SÜRÜKLE ----------

    # AÇIKLAMA: Sürükleme başlangıcı.
    def mousePressEvent(self, e):
        if self.settings.settings_locked:
            return
        if e.button() == QtCore.Qt.MouseButton.LeftButton:
            self.drag_pos = e.globalPosition().toPoint() - self.frameGeometry().topLeft()

    # AÇIKLAMA: Sürükleme sırasında konumu günceller.
    def mouseMoveEvent(self, e):
        if self.settings.settings_locked:
            return
        if self.drag_pos:
            self.move(e.globalPosition().toPoint() - self.drag_pos)

            if hasattr(self, "settings_window") and self.settings_window.isVisible():
                self.position_settings_window(self.settings_window)


    # AÇIKLAMA: Sürükleme bitişinde konumu kaydeder.
    def mouseReleaseEvent(self, e):
        self.drag_pos = None
        if self.settings.settings_locked:
            return
        self.settings.pos_x = self.x()
        self.settings.pos_y = self.y()
        save_settings(self.settings)

# =============================
# 7) AYARLAR DİYALOĞU (UI)
# =============================
# SINIF AÇIKLAMA: Ayar penceresi: kullanıcı arayüzünü ve seçenekleri oluşturur.
class SettingsDialog(QtWidgets.QDialog):
    # AÇIKLAMA: Sınıfın başlangıç kurulumunu yapar (ilk ayar ve arayüz kurulumları).
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

    # AÇIKLAMA: Değişiklikleri anında uygular (autostart dahil).
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

    # AÇIKLAMA: Ayarları kaydeder ve dialogu kapatır.
    def save_and_close(self):
        self.apply_now()
        save_settings(self.settings)
        self.accept()
    
    # AÇIKLAMA: İptalde eski ayarları geri getirir.
    def reject(self):
        self._restore_original_settings()
        super().reject()

    # AÇIKLAMA: Değişiklik durumunu takip eder.
    def _set_dirty(self, dirty=True):
        self._dirty = dirty
        self.btn_apply.setEnabled(dirty)

    # AÇIKLAMA: Başlangıç ayarlarını geri yükler.
    def _restore_original_settings(self):
        for field_name in PanelSettings.__dataclass_fields__:
            setattr(self.settings, field_name, getattr(self._original_settings, field_name))
        if self.parent():
            self.parent().apply_settings()
        self._set_dirty(False)

    # AÇIKLAMA: Sekmeye yardım butonu ekler.
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


    # AÇIKLAMA: Aktif sekme için yardım metni gösterir.
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

    # AÇIKLAMA: Yardım dialogunu gösterir.
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

    # AÇIKLAMA: Yardım dialogunun konumunu ayarlar.
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

    # AÇIKLAMA: Genel ayarlar sekmesini oluşturur.
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
    # AÇIKLAMA: Saat ayarları sekmesini oluşturur.
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

    # AÇIKLAMA: Saat ayarlarını önizleme uygular.
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

    # AÇIKLAMA: Saniye oranını önizler.
    def _apply_seconds_scale_preview(self, value):
        self.settings.time_seconds_scale = value / 100
        self.lbl_sec_scale_value.setText(f"{value}%")
        self._set_dirty(True)
        self.parent().apply_settings()

    # AÇIKLAMA: Genel ayarları önizler.
    def _apply_general_preview(self):
        self.settings.spacing_battery_time = self.spn_space_bt.value()
        self.settings.spacing_time_date = self.spn_space_td.value()
        self.settings.spacing_battery_date_hidden = self.spn_space_bd.value()

        self._set_dirty(True)
        self.parent().apply_settings()

    # AÇIKLAMA: Serbest dağıt önizlemesi uygular.
    def _apply_free_layout_preview(self, value):
        self.settings.free_layout_enabled = value
        self._set_dirty(True)
        self.parent().apply_settings()

    # AÇIKLAMA: Saydamlık önizlemesi uygular.
    def _apply_opacity_preview(self, value):
        self.settings.seffaflik = value / 100
        self.lbl_opacity_value.setText(f"{value}%")
        self._set_dirty(True)
        self.parent().apply_settings()




    # ================= TARİH =================
    # AÇIKLAMA: Tarih ayarları sekmesini oluşturur.
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


    # AÇIKLAMA: Tarih ayarlarını önizler.
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
    # AÇIKLAMA: Pil ayarları sekmesini oluşturur.
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


    # AÇIKLAMA: Pil ayarlarını önizler.
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

    # AÇIKLAMA: Renk seçici açıp sonucu uygular.
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

    # AÇIKLAMA: UI değerlerinden PanelSettings oluşturur.
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

# =============================
# 8) UYGULAMA GİRİŞ NOKTASI
# =============================
# AÇIKLAMA: Uygulamayı başlatır, locale ve ikon ayarlar; ana pencereyi oluşturur.
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

