from PySide6 import QtCore, QtGui, QtWidgets
from core_settings import save_settings
from utils import resource_path

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
            act_settings = menu.addAction("Ayarlar (kilitli)")
            act_settings.setEnabled(False)
        else:
            act_settings = menu.addAction("Ayarlar")
        act_settings.setIcon(QtGui.QIcon(resource_path("img/icons/settings_icon.svg")))
        menu.addSeparator()
        act_alarm = None
        if self.settings.alarm_visible:
            act_alarm = menu.addAction("Alarm")
            act_alarm.setIcon(QtGui.QIcon(resource_path("img/icons/alarm_icon.svg")))
        act_menu_todos = None
        if self.settings.todo_visible:
            act_menu_todos = menu.addAction("Todo")
            act_menu_todos.setIcon(QtGui.QIcon(resource_path("img/icons/todo_icon.svg")))
        act_menu_reminders = None
        if self.settings.reminder_visible:
            act_menu_reminders = menu.addAction("Reminder")
            act_menu_reminders.setIcon(QtGui.QIcon(resource_path("img/icons/reminder_icon.svg")))
        menu.addSeparator()
        act_silent = menu.addAction("Sessiz Mod")
        act_silent.setCheckable(True)
        act_silent.setChecked(getattr(self.settings, "sessiz_mod", False))

        menu.addSeparator()
        grouped = not self.settings.free_layout_enabled
        group_locked = grouped and not getattr(self, "_group_editing", False)

        act_free_layout = menu.addAction("Modüller Serbest")
        act_free_layout.setCheckable(True)
        act_free_layout.setChecked(self.settings.free_layout_enabled)
        act_free_layout.setEnabled(not self.settings.settings_locked)

        act_group_mode = menu.addAction(
            "Modülleri Grupla" if group_locked else "Modülleri Ayarla"
        )
        act_group_mode.setCheckable(True)
        act_group_mode.setChecked(group_locked)
        act_group_mode.setEnabled(
            not self.settings.settings_locked and grouped
        )

        if hedef_tur is None:
            fare_lokal = self.mapFromGlobal(global_pos)
            if self.time_label.isVisible() and self.time_label.geometry().contains(fare_lokal):
                hedef_tur = "time"
            elif self.date_container.isVisible() and self.date_container.geometry().contains(fare_lokal):
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

        act_collect = menu.addAction("⊞  Tüm yapıyı ortada topla")

        menu.addSeparator()
        act_exit = menu.addAction("✕  Çıkış")
        act_exit.setIcon(QtGui.QIcon(resource_path("img/icons/exit_icon.svg")))

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
            self.show_settings_at(settings_anchor_pos or global_pos)
        elif act_alarm is not None and action == act_alarm:
            self.show_alarm_list()
        elif act_menu_todos is not None and action == act_menu_todos:
            self.show_todo_list()
        elif act_menu_reminders is not None and action == act_menu_reminders:
            self.show_reminder_list()
        elif action == act_silent:
            self.settings.sessiz_mod = action.isChecked()
            if hasattr(self, "settings_window") and hasattr(self.settings_window, "chk_silent"):
                self.settings_window.chk_silent.blockSignals(True)
                self.settings_window.chk_silent.setChecked(self.settings.sessiz_mod)
                self.settings_window.chk_silent.blockSignals(False)
            save_settings(self.settings)
        elif action == act_free_layout:
            if action.isChecked():
                self.enter_free_modules_mode()
            else:
                self.restore_grouped_mode()
        elif action == act_group_mode:
            if action.isChecked():
                self.lock_group_layout()
            else:
                self.enter_group_edit_mode()
        elif action == act_collect:
            self.tum_modulleri_topla()
        elif action == act_exit:
            QtWidgets.QApplication.quit()

    def show_settings_at(self, anchor_pos=None, hedef_tur=None):
        if self.settings.settings_locked:
            return
        if hasattr(self, "settings_window") and self.settings_window.isVisible():
            if anchor_pos is not None:
                self.position_settings_window_at(self.settings_window, anchor_pos)
            else:
                self.position_settings_window(self.settings_window)
            self.settings_window.raise_()
            self.settings_window.activateWindow()
            return
        from ui_settings import SettingsDialog

        self.settings_window = SettingsDialog(self.settings, self, hedef_tur)
        if anchor_pos is not None:
            self.position_settings_window_at(self.settings_window, anchor_pos)
        else:
            self.position_settings_window(self.settings_window)
        self.settings_window.show()
        self.settings_window.raise_()

    def show_reminder_list(self):
        if not getattr(self.settings, "reminder_visible", True):
            return
        if hasattr(self, "list_window") and self.list_window.isVisible():
            self.list_window.raise_()
            self.list_window.activateWindow()
            return
        from hatirlatici_listesi import HatirlaticiListesiDialog

        self.list_window = HatirlaticiListesiDialog(self.hatirlatici_servisi, self)
        self.list_window.show()
        self.list_window.raise_()

    def show_alarm_list(self):
        if not getattr(self.settings, "alarm_visible", True):
            return
        if hasattr(self, "alarm_window") and self.alarm_window.isVisible():
            self.alarm_window.raise_()
            self.alarm_window.activateWindow()
            return
        from alarm_listesi import AlarmListesiDialog

        self.alarm_window = AlarmListesiDialog(self.alarm_servisi, self)
        self.alarm_window.show()
        self.alarm_window.raise_()

    def show_todo_list(self):
        if not getattr(self.settings, "todo_visible", True):
            return
        if hasattr(self, "todo_window") and self.todo_window.isVisible():
            self.todo_window.raise_()
            self.todo_window.activateWindow()
            return
        from gorev_arayuzu import GorevArayuzuDialog

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
