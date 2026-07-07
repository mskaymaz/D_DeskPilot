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
    def show_menu_at(self, global_pos, settings_anchor_pos=None, hedef_tur=None):
        menu = QtWidgets.QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #1e1e2e;
                color: #cdd6f4;
                border: 1px solid #45475a;
                border-radius: 6px;
                padding: 4px;
                font-size: 13px;
            }
            QMenu::item { padding: 6px 20px 6px 12px; border-radius: 4px; }
            QMenu::item:selected { background-color: #313244; }
            QMenu::item:disabled { color: #6c7086; }
            QMenu::separator { height: 1px; background: #45475a; margin: 4px 8px; }
        """)

        if self.settings.settings_locked:
            act_settings = menu.addAction("⚙  Ayarlar (kilitli)")
            act_settings.setEnabled(False)
        else:
            act_settings = menu.addAction("⚙  Ayarlar")

        if hedef_tur is None:
            fare_lokal = self.mapFromGlobal(global_pos)
            if self.time_label.isVisible() and self.time_label.geometry().contains(fare_lokal):
                hedef_tur = "time"
            elif self.date_label.isVisible() and self.date_label.geometry().contains(fare_lokal):
                hedef_tur = "date"
            elif self.battery_row.isVisible() and self.battery_row.geometry().contains(fare_lokal):
                hedef_tur = "battery"

        tur_etiketleri = {
            "time": "Saat Boyutu",
            "date": "Tarih Boyutu",
            "battery": "Pil Boyutu",
        }

        if hedef_tur in tur_etiketleri:
            menu.addSeparator()
            scale_attr = f"{hedef_tur}_scale"
            mevcut = round(float(getattr(self.settings, scale_attr, 1.0)), 1)

            boyut_menu = menu.addMenu(tur_etiketleri[hedef_tur])
            boyut_menu.setStyleSheet(menu.styleSheet())

            for i in range(5, 31):
                carpan = round(i / 10, 1)
                secili = "●" if abs(mevcut - carpan) < 0.01 else "○"
                act = boyut_menu.addAction(f"{secili}  ×{carpan:.1f}")
                act.setData((scale_attr, carpan))

        menu.addSeparator()
        act_collect = menu.addAction("⊞  Tüm Modülleri Buraya Topla")

        act_reminders = None
        if self.settings.reminder_visible:
            act_reminders = menu.addAction("🔔  Hatırlatıcı Listesi")

        act_todos = None
        if self.settings.todo_visible:
            act_todos = menu.addAction("☑  Görev Listesi")

        menu.addSeparator()
        act_exit = menu.addAction("✕  Çıkış")

        action = menu.exec(global_pos)
        if action is None:
            return

        if action.data() is not None:
            scale_attr, carpan = action.data()
            setattr(self.settings, scale_attr, carpan)
            self.apply_settings()
            save_settings(self.settings)
            return

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
        if hasattr(self, "settings_window") and self.settings_window.isVisible():
            self.settings_window.raise_()
            self.settings_window.activateWindow()
            return
        self.settings_window = SettingsDialog(self.settings, self)
        if anchor_pos is not None:
            self.position_settings_window_at(self.settings_window, anchor_pos)
        else:
            self.position_settings_window(self.settings_window)
        self.settings_window.show()
        self.settings_window.raise_()

    def show_reminder_list(self):
        if hasattr(self, "list_window") and self.list_window.isVisible():
            self.list_window.raise_()
            self.list_window.activateWindow()
            return
        self.list_window = HatirlaticiListesiDialog(self.hatirlatici_servisi, self)
        self.list_window.show()
        self.list_window.raise_()

    def show_todo_list(self):
        if hasattr(self, "todo_window") and self.todo_window.isVisible():
            self.todo_window.raise_()
            self.todo_window.activateWindow()
            return
        self.todo_window = GorevArayuzuDialog(self.gorev_servisi, self)
        self.todo_window.setWindowOpacity(0.0)
        self._move_todo_window_offscreen(self.todo_window)
        self.todo_window.show()
        self.todo_window.raise_()

        def _todo_window_ready():
            if hasattr(self, "todo_window") and self.todo_window:
                self._center_todo_window(self.todo_window)
                self.todo_window.setWindowOpacity(1.0)
                self.todo_window.raise_()

        QtCore.QTimer.singleShot(0, _todo_window_ready)

    def _center_todo_window(self, dialog):
        app = QtWidgets.QApplication.instance()
        anchor_rect = self.frameGeometry()
        screen = app.screenAt(anchor_rect.center()) or app.primaryScreen()
        rect = screen.availableGeometry()
        x = rect.left() + (rect.width() - dialog.width()) // 2
        y = rect.top() + (rect.height() - dialog.height()) // 2
        dialog.move(x, y)

    def _move_todo_window_offscreen(self, dialog):
        app = QtWidgets.QApplication.instance()
        screens = app.screens() if app else []
        if not screens:
            dialog.move(10000, 10000)
            return
        rect = screens[0].geometry()
        for screen in screens[1:]:
            rect = rect.united(screen.geometry())
        dialog.move(rect.right() + dialog.width() + 200, rect.bottom() + dialog.height() + 200)

    def _clamp_dialog_position(self, dialog, x, y, rect):
        dialog.adjustSize()
        dw, dh = dialog.width(), dialog.height()

        x = max(rect.left(), min(x, rect.right() - dw))
        y = max(rect.top(), min(y, rect.bottom() - dh))
        return x, y

    def _place_dialog_around_rect(self, dialog, anchor_rect, screen_rect):
        dialog.adjustSize()
        dw, dh = dialog.width(), dialog.height()
        gap = 16

        candidates = [
            # sağ
            (anchor_rect.right() + gap, anchor_rect.top()),
            # sol
            (anchor_rect.left() - dw - gap, anchor_rect.top()),
            # alt
            (anchor_rect.left(), anchor_rect.bottom() + gap),
            # üst
            (anchor_rect.left(), anchor_rect.top() - dh - gap),
        ]

        for x, y in candidates:
            fits_x = x >= screen_rect.left() and x + dw <= screen_rect.right()
            fits_y = y >= screen_rect.top() and y + dh <= screen_rect.bottom()
            if fits_x and fits_y:
                dialog.move(x, y)
                return

        x, y = self._clamp_dialog_position(
            dialog,
            anchor_rect.right() + gap,
            anchor_rect.top(),
            screen_rect,
        )
        dialog.move(x, y)

    def position_settings_window(self, dialog):
        app = QtWidgets.QApplication.instance()
        anchor_rect = self.frameGeometry()
        screen = app.screenAt(anchor_rect.center()) or app.primaryScreen()
        self._place_dialog_around_rect(dialog, anchor_rect, screen.availableGeometry())

    def position_settings_window_at(self, dialog, anchor_pos):
        app = QtWidgets.QApplication.instance()
        screen = app.screenAt(anchor_pos) or app.primaryScreen()

        # Serbest moddaki küçük parçalar için yaklaşık hedef alan.
        anchor_rect = QtCore.QRect(anchor_pos, QtCore.QSize(220, 80))
        self._place_dialog_around_rect(dialog, anchor_rect, screen.availableGeometry())
