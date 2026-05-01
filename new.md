# Desktop Daily Assistant - Full Project Specification

## 0. Purpose

This project defines a single, local-first, always-running desktop assistant application.

It is built from scratch using PySide6.

It replaces and unifies the concepts of:

- DigitalSaat
- GcPilUyari

No legacy code is reused. Only concepts are reused.

---

## 1. Product Definition

The application is a lightweight desktop assistant that continuously runs and provides:

- Time awareness
- Date awareness
- Battery awareness
- Notifications
- Reminders
- Todo tracking
- System tray control
- Desktop floating interface
- Voice alerts (TTS)
- Data persistence with safety
- Notification history
- Backup and recovery

---

## 2. Core Principle

One application.

One shared core logic.

Multiple UI surfaces.

All business logic must live inside services.

UI components:

- Only render state
- Only send user actions to services

No business logic inside UI.

---

## 3. Display Modes

### 3.1 Desktop Mode

- Floating window
- Movable
- Always-on-top (optional)
- Opacity configurable
- Widget-based layout

### 3.2 Tray Mode

- Application runs in background
- Controlled via system tray
- Main window may be hidden

### 3.3 Rule

Switching display mode:

- MUST NOT affect core services
- MUST ONLY change UI layer

---

## 4. Architecture

```text
project_root/
  main.py

  src/
    app/
      application.py
      lifecycle.py

    core/
      clock_service.py
      date_service.py
      battery_service.py
      settings_service.py
      notification_service.py
      reminder_service.py
      todo_service.py
      tts_service.py
      backup_service.py
      history_service.py

    ui/
      main_window.py
      desktop_surface.py
      tray_controller.py
      settings_window.py
      reminder_dialog.py
      todo_panel.py
      history_panel.py

      widgets/
        clock_widget.py
        date_widget.py
        battery_widget.py
        reminder_widget.py
        todo_widget.py

    storage/
      json_store.py

    utils/
      logger.py
      paths.py
      constants.py

  data/
    config.json
    reminders.json
    todos.json
    notification_history.json

  logs/
    app.log

  tests/
```

---

## 5. Global Rules

- No overengineering
- No plugin system
- No cloud sync
- No user accounts
- No SQLite; use JSON
- App must always be runnable
- Never crash

System must survive:

- Missing battery info
- Missing tray support
- Broken JSON files
- Missing TTS support

All failures must degrade gracefully.

### 5.1 APPLICATION STARTUP ORDER

1. Load settings_service
2. Initialize logger
3. Initialize json_store
4. Start clock_service
5. Start date_service
6. Start battery_service
7. Start notification_service
8. Start tray_controller
9. Build UI surface

---

## 6. Settings Structure

`config.json`:

```json
{
  "display_mode": "desktop",
  "show_clock": true,
  "show_date": true,
  "show_battery": true,
  "always_on_top": true,
  "opacity": 1.0,
  "silent_mode": false,
  "tts_enabled": true,
  "notifications_enabled": true,
  "low_battery_threshold": 15,
  "critical_battery_threshold": 10
}
```

---

## 7. Clock System

- Live updating clock
- Seconds precision
- Non-blocking
- Must not freeze UI
- Uses system time

---

## 8. Date System

- Current date display
- Lightweight
- Locale-aware if possible

---

## 9. Battery System

- Battery percentage
- Charging / unplugged detection

States:

- Normal
- Low
- Critical

Thresholds:

- Low: 15%
- Critical: 10%

Must NOT crash if battery is unavailable.

---

## 10. Desktop Surface

- Frameless or clean window
- Movable
- Position saved
- Restored on startup
- Always-on-top option
- Opacity setting
- Widget visibility toggle

---

## 11. System Tray

Tray is a primary control interface.

Tray menu:

- Show / Hide App
- New Reminder
- New Todo
- Toggle Silent Mode
- Open Settings
- Quit

Tray rules:

- Closing window MUST NOT exit app
- App continues running
- Tray notifications must work without UI
- If tray is not supported, fallback safely

---

## 12. Display Mode Control

Config:

```text
display_mode = desktop | tray
```

Changing mode:

- Rebuild UI surface
- Keep services intact

---

## 13. Notification System

Single unified service.

Sources:

- Battery
- Reminder
- Todo (future)

Types:

- Popup
- Tray notification

Rules:

- Cooldown system required
- No spam
- Silent mode respected

---

## 14. Reminder System

Each reminder:

- `id`
- `date`
- `time`
- `message`
- `status`
- `created_at`

Behavior when triggered:

- Show popup
- Show tray notification
- Speak via TTS, if enabled

Features:

- Snooze for 5, 10, or 60 minutes
- Missed reminder detection on startup
- Stored in `reminders.json`

### 14.1 RECURRING REMINDER RULES (STRICT)

Allowed:
- daily
- weekly (single day only)
- weekdays

NOT allowed:
- custom intervals
- complex schedules
- exclusions (holiday logic vs.)

Reason:
Keep logic simple and predictable

---

## 15. Todo System

Each todo:

- `id`
- `title`
- `priority`: `low`, `normal`, or `high`
- `status`: `active`, `postponed`, or `completed`
- `due_date` (optional)
- `created_at`
- `completed_at`

Actions:

- Add
- Complete
- Delete
- Postpone

Sorting:

- Today first
- Active before postponed
- High priority first
- Completed last

---

## 16. TTS System

- Used only for reminders
- Non-blocking
- Respects silent mode
- Respects `tts_enabled`
- Fails silently if unsupported

### 16.1 TTS IMPLEMENTATION

Primary backend: pyttsx3 (offline)

Rules:
- If pyttsx3 fails → disable TTS silently
- No online TTS usage
- No API-based TTS
- Must not block UI

---

## 17. Storage System

JSON-based.

Files:

- `config.json`
- `reminders.json`
- `todos.json`
- `notification_history.json`

Rules:

- Atomic write using temp + replace
- Backup before overwrite
- Detect corruption
- Recover safely

### 17.1 DATA RETENTION POLICY

- notification_history.json max 500 kayıt
- todos.json completed items max 300 (older trimmed)
- reminders.json geçmiş kayıt tutulmaz (sadece aktif + snoozed)

Trimming rules:
- App startup sırasında çalışır
- Her write işleminden sonra limit aşılırsa çalışır

---

## 18. Backup System

- Automatic `.bak` creation
- Recovery from corrupted JSON
- Log recovery events

---

## 19. Notification History

Stored in `notification_history.json`.

Each entry:

- `time`
- `type`
- `title`
- `message`
- `source`

Rules:

- Limited size
- Old entries trimmed
- Simple UI panel

---

## 20. Widget System

Widgets:

- Clock
- Date
- Battery
- Reminder
- Todo

Features:

- Enable / disable
- Compact mode
- Normal mode

No plugin system allowed.

---

## 21. Recurring Reminders

Supported:

- Daily
- Weekly
- Weekdays
- Simple intervals

No calendar UI.

---

## 22. Smart Todo

- Today view
- Priority filtering
- Completed history

No complex task management.

---

## 23. Basic Insights

- Completed tasks count
- Missed reminders count
- Battery critical count

Simple only. No analytics system.

---

24. LIGHT AUTOMATION

Simple rule system:

Examples:

If battery < X → notify
If unplugged → notify
If night → reduce alerts
If silent mode → suppress TTS

Rules must be simple JSON.

No scripting.
No engine complexity.


### 24.1 AUTOMATION LIMITS

Supported triggers:
- battery_level_below
- charger_unplugged
- time_reached

Supported actions:
- notify
- mute_notifications
- reduce_notification_frequency

Rules:
- Max 10 rules
- No chaining
- No nested logic
- No scripting

---

## 25. Error Handling

Must never crash.

Handle:

- Missing files
- Corrupt JSON
- Missing tray
- Missing battery
- Missing TTS

Log everything to:

```text
logs/app.log
```

User messages must be minimal and clear.

## 26. TEST STRATEGY

Required unit tests:

- json_store
- backup_service
- reminder_service (trigger logic)
- notification_service (cooldown logic)

Rules:
- UI testing not required
- Focus on core services
- Focus on data integrity

---

## 27. Final Principle

Mini version:

- Shows and warns

Maksi version:

- Guides and organizes

System must remain:

- Stable
- Predictable
- Lightweight
- Maintainable
- Local-first
- Private

Reliability is more important than features.
