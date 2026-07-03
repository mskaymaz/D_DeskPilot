# TAMAMLAMA LİSTESİ

[x] PHASE 1 — BASELINE SAFETY
	- [x] Task 1.1 — Add app version constant
	- [x] Task 1.2 — Add logging foundation
	- [x] Task 1.3 — Safe JSON write
	- [x] Task 1.4 — Config validation fallback

[x] PHASE 2 — BATTERY MODULE
	- [x] Task 2.1 — Battery state model
	- [x] Task 2.2 — Battery thresholds
	- [x] Task 2.3 — Plug/unplug detection
	- [x] Task 2.4 — Optional battery health info

[x] PHASE 4 — REMINDER ENGINE
	- [x] Task 4.1 — Reminder model
	- [x] Task 4.2 — Reminder storage
	- [x] Task 4.3 — Due reminder detection
	- [x] Task 4.4 — Reminder popup
	- [x] Task 4.5 — Recurring reminder handling
	- [x] Task 4.6 — Reminder list UI

[x] PHASE 5 — MINI TODO
	- [x] Task 5.1 — Todo model
	- [x] Task 5.2 — Todo storage
	- [x] Task 5.3 — Todo basic UI
	- [x] Task 5.4 — Todo priority sorting

[x] PHASE 6 — MODULAR UI
	- [x] Task 6.1 — Module visibility settings
	- [x] Task 6.2 — Layout persistence
	- [x] Task 6.3 — Global scale setting
	- [x] Task 6.4 — Right mouse + wheel resize

[x] PHASE 7 — MULTI-MONITOR SUPPORT
	- [x] Task 7.1 — Screen info capture
	- [x] Task 7.2 — Restore module to correct monitor
	- [x] Task 7.3 — Move all modules
	- [x] Task 7.4 — Multi-monitor mode option

[x] PHASE 9 — FINAL STABILITY
	- [x] Task 9.1 — Startup crash safety
	- [x] Task 9.2 — Manual verification checklist

---
# DIGITALSAAT V1.1 — IMPLEMENTATION TASKS
 Do not introduce placeholder code.
- Every task must keep the app runnable.
- Preserve existing working clock/date/battery behavior.
- Prefer simple, testable services over large controller logic.
- No overengineering.

 Phase 0 — Project Structure Preparation

## Phase 0 — Project Structure Preparation

**Klasör Açıklamaları:**
delleri (ör: BatteryModel, ReminderModel, TodoModel)
a `app/controllers/` — UI ile servisler arası köprü (küçük projelerde service/ui ile birleştirilebilir)
- `data/` — Kalıcı veri dosyaları (örn: `reminders.json`, `todos.json`, `settings.json`)
- `logs/` — Uygulama log dosyaları (örn: `app.log`)
- `docs/` — Proje dokümantasyonu
- `tests/manual_checklist.md`
> Not: Fazlar ilerledikçe önce model, sonra servis, sonra UI ve controller katmanları oluşturulmalı. Her faz sonunda beklenen çıktı/sonuç kısa bir özetle belirtilmeli. Fazlar arası bağımlılıklar için, örneğin Reminder servisleri tamamlanmadan Reminder UI yapılmamalı.

---

# PHASE 1 — BASELINE SAFETY

## Task 1.1 — Add app version constant
Create a single app version source.

Expected:
- Add version constant.
- Show version in settings/about if such surface exists.
- No behavior change.

---

## Task 1.2 — Add logging foundation
Add basic file logging.

Expected:
- logs/app.log
- Log app startup, shutdown, config load/save errors.
- Do not spam logs.

---

## Task 1.3 — Safe JSON write
Improve JSON persistence with atomic write.

Expected:
- Write to temp file first.
- Replace target file only after successful write.
- Existing JSON behavior must continue.

---

## Task 1.4 — Config validation fallback
Add basic config validation.

Expected:
- Missing keys get defaults.
- Broken JSON is backed up.
- App opens safely with defaults.

---

# PHASE 2 — BATTERY MODULE

## Task 2.1 — Battery state model
Create/clean battery data model.

Expected:
- percent
- plugged
- status text
- timestamp

---

## Task 2.2 — Battery thresholds
Add low/critical threshold logic.

Expected:
- Normal
- Low
- Critical
- Default thresholds: 15 and 10

---

## Task 2.3 — Plug/unplug detection
Detect charging state changes.

Expected:
- Notify when charger plugged.
- Notify when charger unplugged.
- Avoid repeated spam notifications.

---

## Task 2.4 — Optional battery health info
Add optional battery health provider.

Expected:
- If supported, show health info.
- If unsupported, hide silently.
- App must not crash.

---

# PHASE 3 — NOTIFICATION SYSTEM

## Task 3.1 — Notification service
Create a small notification service.

Expected:
- Popup notification
- Tray notification if tray exists
- Common method for battery/reminder alerts

---

## Task 3.2 — Notification cooldown
Add spam protection.

Expected:
- Same notification should not repeat too frequently.
- Cooldown configurable internally.

---

## Task 3.3 — Silent mode
Add silent mode setting.

Expected:
- Visual notifications may continue.
- Sound/TTS disabled when silent mode is on.

---

# PHASE 4 — REMINDER ENGINE

## Task 4.1 — Reminder model
Create reminder model.

Expected:
- id
- title
- description
- due_at
- repeat_type: none/daily/weekly
- status: active/completed/missed
- snoozed_until
- created_at

---

## Task 4.2 — Reminder storage
Persist reminders safely.

Expected:
- reminders.json
- Load/save through storage layer
- Validate broken entries

---

## Task 4.3 — Due reminder detection
Add reminder scheduler polling.

Expected:
- Detect due reminders.
- Detect missed reminders after app restart.
- No blocking UI.

---

## Task 4.4 — Reminder popup
Show due reminder popup.

Expected:
- Complete
- Snooze 5 min
- Snooze 10 min
- Snooze 1 hour

---

## Task 4.5 — Recurring reminder handling
Implement daily/weekly recurrence.

Expected:
- Completing recurring reminder schedules next due time.
- One-time reminder becomes completed.

---

## Task 4.6 — Reminder list UI
Add active/history reminder list.

Expected:
- Active reminders visible.
- Completed/missed history visible.
- Keep UI simple.

---

# PHASE 5 — MINI TODO

## Task 5.1 — Todo model
Create todo model.

Expected:
- id
- title
- priority: low/normal/high
- done
- created_at
- due_date optional

---

## Task 5.2 — Todo storage
Persist todos safely.

Expected:
- todos.json
- Validation fallback
- No crash on broken entries

---

## Task 5.3 — Todo basic UI
Add simple TODO UI.

Expected:
- Add task
- Mark done
- Delete task
- Show today items

---

## Task 5.4 — Todo priority sorting
Sort TODO items.

Expected:
- Undone first
- High priority first
- Done items lower

---

# PHASE 6 — MODULAR UI

## Task 6.1 — Module visibility settings
Add show/hide per module.

Expected:
- Clock show/hide
- Date show/hide
- Battery show/hide
- Reminder show/hide if UI exists
- Todo show/hide if UI exists

---

## Task 6.2 — Layout persistence
Save module positions and sizes.

Expected:
- Works in normal and free mode.
- Restore safely on startup.
- Invalid positions corrected.

---

## Task 6.3 — Global scale setting
Add global UI scale value.

Expected:
- One scale value controls module size/font spacing.
- Minimum and maximum limits.
- Default: 1.0

---

## Task 6.4 — Right mouse + wheel resize
Implement scale shortcut.

Expected:
- Hold right mouse button + wheel up = scale up.
- Hold right mouse button + wheel down = scale down.
- Applies to focused module or main panel.
- Save scale value.

---

# PHASE 7 — MULTI-MONITOR SUPPORT

## Task 7.1 — Screen info capture
Store screen information per module.

Expected:
- screen name/id if available
- screen geometry
- module x/y/width/height

---

## Task 7.2 — Restore module to correct monitor
Restore modules to last monitor.

Expected:
- If monitor exists, restore there.
- If monitor missing, move module to visible area.

---

## Task 7.3 — Move all modules to one monitor
Add “collect to current monitor” action.

Expected:
- Context menu or tray action.
- Preserve relative positions as much as possible.
- Prevent off-screen placement.

---

## Task 7.4 — Multi-monitor mode option
Add layout mode option.

Expected:
- Single monitor mode
- Multi-monitor mode
- Safe fallback when monitor count changes

---

# PHASE 8 — SYSTEM TRAY

## Task 8.1 — Tray menu cleanup
Improve tray menu.

Expected:
- Show/hide app
- New reminder
- New todo
- Settings
- Quit

---

## Task 8.2 — Tray summary
Show useful status in tray.

Expected:
- Battery percent
- Next reminder if available
- App running status

---

# PHASE 9 — FINAL STABILITY

## Task 9.1 — Startup crash safety
Wrap startup with safe error handling.

Expected:
- Log startup errors.
- Show readable message if fatal.
- Do not lose config.

---

## Task 9.2 — Manual verification checklist
Create manual test checklist.

Expected:
- Clock works
- Date works
- Battery works
- Reminder due popup works
- Snooze works
- Todo works
- Layout saves
- Scale shortcut works
- Multi-monitor fallback works

---

## Task 9.3 - R.260701_1711 UI and startup stabilization
Completed.

Done:
- ComboBox and date popup focus/topmost behavior stabilized.
- Gorevlerim priority combo and popup width aligned.
- New task row compacted with date, time and add controls on one line.
- New task description expanded to two lines.
- Free layout startup no longer shows grouped window at the same time.

---

# DO NOT DO IN V1.1

- No world clock
- No Hijri calendar
- No advanced theme engine
- No SQLite migration
- No plugin system
- No complex category/tag TODO system
- No full update system
- No contact/support module expansion

## Globalization Task Track
- Add a lightweight translation manager: `dil_yonetimi.py`.
- Add `translations/tr.json`, `translations/en.json`, `translations/ar.json`.
- Replace new UI text with translation keys instead of hardcoded strings.
- Keep Turkish as the default language.
- Add Arabic RTL layout checks before release.

## i18n Acceptance Criteria
- Todo is the pilot i18n module.
- No new UI text without translation keys.
- Language is persisted in PanelSettings.
- Arabic requires separate RTL validation.

## Current Localization Scope
Current phase: Turkish-first stabilization.
Do not expand scope into full English/Arabic UI polishing until core Turkish workflows are stable.
