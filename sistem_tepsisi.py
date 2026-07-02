from PySide6 import QtCore, QtGui, QtWidgets
from utils import resource_path, ICON_FILE

class SistemTepsisi(QtWidgets.QSystemTrayIcon):
    """
    Uygulamanın sistem tepsisi (Tray) yönetimini sağlayan sınıf.
    Task 8.1 kapsamında oluşturulmuştur.
    """
    def __init__(self, ana_pencere, parent=None):
        super().__init__(parent)
        self.ana_pencere = ana_pencere
        self.setIcon(QtGui.QIcon(resource_path(ICON_FILE)))
        self.setToolTip("DeskPilot")
        
        self._menu_kur()
        self.activated.connect(self._tetiklendi)

    def _menu_kur(self):
        menu = QtWidgets.QMenu()
        
        self.act_goster = menu.addAction("Göster / Gizle")
        self.act_goster.triggered.connect(self._gorunurluk_degistir)
        
        menu.addSeparator()
        
        act_yeni_hatirlatici = menu.addAction("Yeni Hatırlatıcı")
        act_yeni_hatirlatici.triggered.connect(self.ana_pencere.show_reminder_list)
        
        act_yeni_todo = menu.addAction("Yeni Görev")
        act_yeni_todo.triggered.connect(self.ana_pencere.show_todo_list)
        
        menu.addSeparator()
        
        act_ayarlar = menu.addAction("Ayarlar")
        act_ayarlar.triggered.connect(lambda: self.ana_pencere.show_settings_at())
        
        act_cikis = menu.addAction("Çıkış")
        act_cikis.triggered.connect(QtWidgets.QApplication.quit)
        
        self.setContextMenu(menu)

    def _tetiklendi(self, sebep):
        if sebep == QtWidgets.QSystemTrayIcon.ActivationReason.Trigger:
            self._gorunurluk_degistir()

    def _gorunurluk_degistir(self):
        if self.ana_pencere.isVisible() or (self.ana_pencere.free_time_window and self.ana_pencere.free_time_window.isVisible()):
            if self.ana_pencere.settings.free_layout_enabled:
                self.ana_pencere._hide_free_windows()
            else:
                self.ana_pencere.hide()
        else:
            if self.ana_pencere.settings.free_layout_enabled:
                self.ana_pencere._show_free_windows()
            else:
                self.ana_pencere.show()

    def ozet_guncelle(self, pil_yuzdesi, sarjda, sonraki_hatirlatici_metni):
        """Tepsi ikonunun ipucunu günceller. Task 8.2 kapsamında eklenmiştir."""
        sarj_durumu = "(Şarjda)" if sarjda else ""
        hatirlatici_bilgi = f"\nSonraki: {sonraki_hatirlatici_metni}" if sonraki_hatirlatici_metni else ""
        self.setToolTip(f"DeskPilot\nPil: %{pil_yuzdesi} {sarj_durumu}{hatirlatici_bilgi}")