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
from pencere_araclari import aktif_popup_veya_modal_var, pencereyi_guvenli_tas, en_ustte_tut
from pil_servisi import PilServisi
from bildirim_servisi import BildirimServisi

# =======================
# ANA PENCERE
# =======================

from pencere_guncelleme import PencereGuncellemeKarishimi
from pencere_navigasyon import PencereNavigasyonKarishimi
from window_mouse_mixin import WindowMouseMixin
from window_lifecycle_mixin import WindowLifecycleMixin
from window_settings_mixin import WindowSettingsMixin
from window_init_mixin import WindowInitMixin
from window_runtime_mixin import WindowRuntimeMixin
from window_topmost_mixin import WindowTopmostMixin
from serbest_duzen import SerbestDuzenKarishimi

def move_window_safely(window, settings):
    """DeskPilot.py tarafından kullanılan güvenli taşıma sarmalayıcısı."""
    return pencereyi_guvenli_tas(window, settings)

class DraggableTransparentWindow(WindowLifecycleMixin, WindowMouseMixin, WindowSettingsMixin, WindowInitMixin, WindowRuntimeMixin, WindowTopmostMixin, QtWidgets.QWidget, PencereGuncellemeKarishimi, PencereNavigasyonKarishimi, SerbestDuzenKarishimi):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self._init_state()
        self._init_logging()
        self._init_window()
        self._init_widgets()
        self._init_startup()








    # ---------- AYARLAR ---------- *****************









    def show_menu(self, pos):
        self.show_menu_at(self.mapToGlobal(pos))
