from PySide6 import QtCore, QtGui, QtWidgets
from ui_settings import SettingsDialog
from hatirlatici_listesi import HatirlaticiListesiDialog
from gorev_arayuzu import GorevArayuzuDialog
from core_settings import save_settings

class PencereNavigasyonKarishimi:
    """
    Pencere arası geçişleri ve menü yönetimini sağlayan karışım sınıfı.
    Dosya boyutu disiplini (Rule: <400 lines) için oluşturulmuştur.
    """
    def show_menu_at(self, global_pos, settings_anchor_pos=None):
        menu = QtWidgets.QMenu(self)
        if self.settings.settings_locked:
            act_settings = menu.addAction("Ayarlar (kilitli)")
            act_settings.setEnabled(False)
        else:
            act_settings = menu.addAction("Ayarlar")
            
        act_collect = menu.addAction("Tüm Modülleri Buraya Topla")

        act_reminders = None
        if self.settings.reminder_visible:
            act_reminders = menu.addAction("Hatırlatıcı Listesi")
            
        act_todos = None
        if self.settings.todo_visible:
            act_todos = menu.addAction("Görev Listesi")
            
        act_exit = menu.addAction("Çıkış")
        action = menu.exec(global_pos)
        
        if action == act_settings and not self.settings.settings_locked:
            self.show_settings_at(settings_anchor_pos)
        elif action == act_collect:
            self.tum_modulleri_topla()
        elif action == act_reminders:
            self.show_reminder_list()
        elif action == act_todos:
            self.show_todo_list()
        elif action == act_exit:
            QtWidgets.QApplication.quit()

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

    def show_reminder_list(self):
        self.list_window = HatirlaticiListesiDialog(self.hatirlatici_servisi, self)
        self.list_window.show()
        self.list_window.raise_()

    def show_todo_list(self):
        self.todo_window = GorevArayuzuDialog(self.gorev_servisi, self)
        self.todo_window.show()
        self.todo_window.raise_()

    def position_settings_window(self, dialog):
        app = QtWidgets.QApplication.instance()
        screen = app.screenAt(self.frameGeometry().center()) or app.primaryScreen()
        rect = screen.availableGeometry()

        dialog.adjustSize()
        dw, dh = dialog.width(), dialog.height()

        x = self.x() + self.width() + 10
        y = self.y()

        if x + dw > rect.right():
            x = self.x() - dw - 10
        if x < rect.left():
            x = rect.left()
        if y + dh > rect.bottom():
            y = rect.bottom() - dh
        if y < rect.top():
            y = rect.top()

        dialog.move(x, y)

    def position_settings_window_at(self, dialog, anchor_pos):
        app = QtWidgets.QApplication.instance()
        screen = app.screenAt(anchor_pos) or app.primaryScreen()
        rect = screen.availableGeometry()

        dialog.adjustSize()
        dw, dh = dialog.width(), dialog.height()

        x, y = anchor_pos.x(), anchor_pos.y()

        if x + dw > rect.right(): x = rect.right() - dw
        if y + dh > rect.bottom(): y = rect.bottom() - dh
        if x < rect.left(): x = rect.left()
        if y < rect.top(): y = rect.top()

        dialog.move(x, y)