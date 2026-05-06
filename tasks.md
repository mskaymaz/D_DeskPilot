# DeskPilot — Step-by-Step Task Plan for Copilot / Gemini Code Assist / Codex

# EKO EXECUTION MODE (IMPLEMENTATION TASKS ONLY)

All implementation tasks in this file MUST be executed under EKO mode.
Planning, review, and documentation tasks may use normal analytical reasoning.

EKO MODE RULES:
- Execute ONLY the current implementation task
- Do NOT skip required task steps
- Do NOT implement future steps
- Do NOT redesign architecture unless the task explicitly asks for it
- Do NOT add features outside task scope
- Keep the project runnable after each change
- Keep files small and clean
- Business logic must stay in services, not UI

EKO TRIGGERS:
- `eko`
- `bismillah`
- `ekonomik token`

EKO stays active until the user explicitly says `eko off`.
While active, it is the first runtime gate before reading, searching, editing, testing, or replying.

TOKEN CONTROL:
- Use the minimum relevant files.
- Avoid unrelated searches.
- Avoid speculative suggestions.
- Avoid repeated explanations.
- Keep default final replies within 10 lines.
- Expand only when the user explicitly asks for detail.

OUTPUT GUIDELINE:
- Prefer minimal, task-scoped responses
- When code changes are requested, include the changed files and a short summary
- Avoid unnecessary alternatives or repetition

ERROR HANDLING:
- Recoverable errors must degrade gracefully
- Unrecoverable startup errors must be logged and shown clearly
- Prefer the simplest valid solution

FLOW:
- Read ONLY the current implementation task
- Execute the task
- Stop after the task is complete
- Wait for the next instruction

PRE-FLIGHT CHECK:
- Identify the files and layers that may change.
- Check whether similar logic already exists.
- Keep UI limited to rendering and user interaction.
- Keep service, storage, and scheduling responsibilities separate.
- Avoid hidden coupling through globals or scattered state.
- Extract first if a file is already overloaded.

This section has priority for implementation tasks only.


## GLOBAL RULE

Work in very small steps.
Do not implement future tasks early.
After each task:
- keep the app runnable
- do not break previous behavior
- avoid large files
- prefer services over UI logic
- do not overengineer

## TASK WRITING STANDARD

All task titles, task descriptions, acceptance criteria, and implementation notes must be written in English.

Every task should use the following structure:

## Task X.Y - Title

Goal:
- What problem is being solved?

Scope:
- Which files and layers may change?

Out of Scope:
- What must not be changed in this task?

Acceptance:
- How do we know the task is done?

Tests:
- Which automated or manual checks should pass?

Task titles should stay short and actionable.

## PROJECT LANGUAGE POLICY

- Task documents and task instructions: English
- User-facing conversation: Turkish
- UI labels and user-visible app text: Turkish
- Source code identifiers: ASCII English by default
- Inline comments and docstrings: English unless a file is explicitly user-facing documentation

---

# PHASE 0 — PROJECT FOUNDATION

## Task 0.1 — Create Project Skeleton
Create the DeskPilot folder structure.

Required:
- main.py
- requirements.txt
- README.md
- src/
- data/
- logs/
- tests/

Do not implement features yet.

---

## Task 0.2 — Add Basic PySide6 App Boot
Create a minimal PySide6 app that opens an empty main window.

Required:
- src/app/application.py
- src/ui/main_window.py
- main.py starts the app

Acceptance:
- app opens
- app closes cleanly

---

## Task 0.3 — Add Logger
Create logging system.

Required:
- src/utils/logger.py
- logs/app.log

Acceptance:
- app startup writes a log line
- errors can be logged safely

---

## Task 0.4 — Add Paths Helper
Create path helper.

Required:
- src/utils/paths.py
- project-safe paths for data/ and logs/

Acceptance:
- app finds data folder reliably

---

# PHASE 1 — STORAGE AND SETTINGS

## Task 1.1 — Create JSON Store
Create src/storage/json_store.py.

Required:
- read_json
- write_json
- defaults if missing
- safe broken JSON handling

Do not add backup yet.

---

## Task 1.2 — Add Atomic JSON Write
Improve json_store.py.

Required:
- write to temp file first
- replace original file after success

Acceptance:
- no partial JSON file on failure

---

## Task 1.3 — Add Backup on Write
Before replacing JSON, create .bak file.

Acceptance:
- config.json.bak appears after write

Notes:
- Backup handling must stay consistent with the central storage layer.
- Recovery behavior should be defined in the storage and backup tasks.

---

## Task 1.4 — Create Settings Service
Create src/core/settings_service.py.

Required config:
- display_mode
- show_clock
- show_date
- show_battery
- always_on_top
- opacity
- silent_mode
- tts_enabled
- notifications_enabled
- low_battery_threshold
- critical_battery_threshold

Acceptance:
- settings load from data/config.json
- missing keys get defaults

---

# PHASE 2 — CLOCK AND DATE

## Task 2.1 — Create Clock Service
Create src/core/clock_service.py.

Required:
- current time
- seconds precision
- no UI logic

---

## Task 2.2 — Create Date Service
Create src/core/date_service.py.

Required:
- current date
- simple formatted date string

---

## Task 2.3 — Create Clock Widget
Create src/ui/widgets/clock_widget.py.

Required:
- displays live time
- updates with QTimer
- no blocking

---

## Task 2.4 — Create Date Widget
Create src/ui/widgets/date_widget.py.

Required:
- displays current date
- updates safely

---

# PHASE 3 — BATTERY

## Task 3.1 — Create Battery Service
Create src/core/battery_service.py.

Required:
- battery percentage
- charging status
- safe fallback if battery unavailable

Use psutil if available.

---

## Task 3.2 — Add Battery State Logic
Add:
- normal
- low
- critical

Use settings thresholds.

---

## Task 3.3 — Create Battery Widget
Create src/ui/widgets/battery_widget.py.

Required:
- shows percentage
- shows charging/unplugged state
- does not crash if unavailable

---

# PHASE 4 — DESKTOP SURFACE

## Task 4.1 — Create Desktop Surface
Create src/ui/desktop_surface.py.

Required:
- contains clock/date/battery widgets
- clean layout
- minimal UI

---

## Task 4.2 — Add Always-on-top
Use settings always_on_top.

Acceptance:
- window can stay above others

---

## Task 4.3 — Add Opacity
Use settings opacity.

Acceptance:
- opacity applies on startup

---

## Task 4.4 — Save and Restore Position
Save window position in config.

Acceptance:
- app reopens in previous position

---

## Task 4.5 — Add Widget Visibility
Respect:
- show_clock
- show_date
- show_battery

---

# PHASE 5 — SYSTEM TRAY

## Task 5.1 — Create Tray Controller
Create src/ui/tray_controller.py.

Required:
- QSystemTrayIcon
- safe fallback if tray unavailable

---

## Task 5.2 — Add Tray Menu
Menu items:
- Show / Hide App
- New Reminder
- New Todo
- Toggle Silent Mode
- Open Settings
- Quit

Stub actions are acceptable for reminder/todo at this stage.

---

## Task 5.3 — Prevent Close from Exiting
Closing the main window must hide it, not quit.

Acceptance:
- app continues running in tray

---

## Task 5.4 — Add Tray Tooltip
Tooltip shows:
- DeskPilot running
- battery percentage if available

---

# PHASE 6 — DISPLAY MODE CONTROL

## Task 6.1 — Add Display Mode Setting
Use:
- desktop
- tray

---

## Task 6.2 — Implement Mode Switching
Switching mode changes UI surface only.

Acceptance:
- core services remain shared
- no duplicated clock/battery logic

---

# PHASE 7 — NOTIFICATION SYSTEM

## Task 7.1 — Create Notification Service
Create src/core/notification_service.py.

Required:
- notify(title, message, source, level)
- popup notification stub
- tray notification support

---

## Task 7.2 — Add Cooldown
Prevent spam.

Required:
- per-source cooldown
- configurable internal default

---

## Task 7.3 — Respect Silent Mode
Silent mode:
- no sound
- no TTS
- visual notification allowed

---

## Task 7.4 — Battery Notifications
Trigger:
- low battery
- critical battery
- charger plugged
- charger unplugged

---

# PHASE 8 — SETTINGS UI

## Task 8.1 — Create Settings Window
Create src/ui/settings_window.py.

Required controls:
- display mode
- show clock
- show date
- show battery
- always on top
- opacity
- silent mode
- notifications enabled
- TTS enabled

---

## Task Tracker

Use this checklist as the single progress source. Mark a task only after its acceptance and test notes are satisfied.

Phase 0 - Project Foundation
- [ ] Task 0.1 — Create Project Skeleton
- [ ] Task 0.2 — Add Basic PySide6 App Boot
- [ ] Task 0.3 — Add Logger
- [ ] Task 0.4 — Add Paths Helper

Phase 1 - Storage and Settings
- [ ] Task 1.1 — Create JSON Store
- [ ] Task 1.2 — Add Atomic JSON Write
- [ ] Task 1.3 — Add Backup on Write
- [ ] Task 1.4 — Create Settings Service

Phase 2 - Clock and Date
- [ ] Task 2.1 — Create Clock Service
- [ ] Task 2.2 — Create Date Service
- [ ] Task 2.3 — Create Clock Widget
- [ ] Task 2.4 — Create Date Widget

Phase 3 - Battery
- [ ] Task 3.1 — Create Battery Service
- [ ] Task 3.2 — Add Battery State Logic
- [ ] Task 3.3 — Create Battery Widget

Phase 4 - Desktop Surface
- [ ] Task 4.1 — Create Desktop Surface
- [ ] Task 4.2 — Add Always-on-top
- [ ] Task 4.3 — Add Opacity
- [ ] Task 4.4 — Save and Restore Position
- [ ] Task 4.5 — Add Widget Visibility

Phase 5 - System Tray
- [ ] Task 5.1 — Create Tray Controller
- [ ] Task 5.2 — Add Tray Menu
- [ ] Task 5.3 — Prevent Close from Exiting
- [ ] Task 5.4 — Add Tray Tooltip

Phase 6 - Display Mode Control
- [ ] Task 6.1 — Add Display Mode Setting
- [ ] Task 6.2 — Implement Mode Switching

Phase 7 - Notification System
- [ ] Task 7.1 — Create Notification Service
- [ ] Task 7.2 — Add Cooldown
- [ ] Task 7.3 — Respect Silent Mode
- [ ] Task 7.4 — Battery Notifications

Phase 8 - Settings UI
- [ ] Task 8.1 — Create Settings Window
- [ ] Task 8.2 — Save Settings from UI
- [ ] Task 8.3 — Apply Settings Without Restart Where Safe

Phase 9 - Reminders
- [ ] Task 9.1 — Create Reminder Service
- [ ] Task 9.2 — Create Reminder Dialog
- [ ] Task 9.3 — Store Reminders
- [ ] Task 9.4 — Trigger Due Reminders
- [ ] Task 9.5 — Detect Missed Reminders on Startup
- [ ] Task 9.6 — Add Snooze

Phase 10 - TTS
- [ ] Task 10.1 — Create TTS Service
- [ ] Task 10.2 — Connect TTS to Reminders
- [ ] Task 10.3 — Keep TTS Non-blocking

Phase 11 - Todo
- [ ] Task 11.1 — Create Todo Service
- [ ] Task 11.2 — Create Todo Panel
- [ ] Task 11.3 — Add Sorting
- [ ] Task 11.4 — Persist Todos

Phase 12 - History and Data Limits
- [ ] Task 12.1 — Create History Service
- [ ] Task 12.2 — Limit Notification History
- [ ] Task 12.3 — Limit Completed Todos
- [ ] Task 12.4 — Do Not Keep Old Reminder History

Phase 13 - Backup and Recovery
- [ ] Task 13.1 — Create Backup Service
- [ ] Task 13.2 — Add Recovery Logging
- [ ] Task 13.3 — Add Hidden Secondary Backup

Phase 14 - Widget System
- [ ] Task 14.1 — Add Widget Toggle System
- [ ] Task 14.2 — Add Compact Mode
- [ ] Task 14.3 — Add Normal Mode

Phase 15 - Recurring Reminders
- [ ] Task 15.1 — Add Daily Recurrence
- [ ] Task 15.2 — Add Weekly Recurrence
- [ ] Task 15.3 — Add Weekdays Recurrence
- [ ] Task 15.4 — Explicitly Reject Complex Recurrence

Phase 16 - Smart Todo
- [ ] Task 16.1 — Add Today View
- [ ] Task 16.2 — Add Priority View
- [ ] Task 16.3 — Add Completed History View

Phase 17 - Basic Insights
- [ ] Task 17.1 — Add Simple Daily Summary
- [ ] Task 17.2 — Avoid Battery Analytics

Phase 18 - Light Automation
- [ ] Task 18.1 — Create Simple Rule Model
- [ ] Task 18.2 — Supported Triggers Only
- [ ] Task 18.3 — Supported Actions Only
- [ ] Task 18.4 — Reject Complex Automation

Phase 19 - Tests
- [ ] Task 19.1 — Test JSON Store
- [ ] Task 19.2 — Test Backup Service
- [ ] Task 19.3 — Test Reminder Logic
- [ ] Task 19.4 — Test Notification Cooldown

Phase 20 - Final Stabilization
- [ ] Task 20.1 — Manual Test Checklist
- [ ] Task 20.2 — Clean Files
- [ ] Task 20.3 — Freeze Mini Release

---

## Recommended Additions (project health)

These tasks are recommended to improve reliability, testing and developer experience. Add them in the phases indicated or when convenient.

- [ ] Add unit tests for `json_store`, `backup_service`, `reminder_service`, `notification_service` (Phase 1/Testing)
- [ ] Add CI: GitHub Actions workflow to run tests and lint on push/PR (Phase 0/CI)
- [ ] Add TTS fallback layer (wrap `pyttsx3` with safe disable on failure) (Phase 16/TTS)
- [ ] Ensure service isolation: run long-running tasks in workers/QThread to avoid blocking UI (Phase 2/3)
- [ ] Add `data/config.json.example` with defaults and schema (Phase 1)
- [ ] Improve `README.md` with setup, EKO rules, and run instructions (Phase 0)
- [ ] Add simple pre-commit or CI checks to warn about large file edits / non-EKO changes (Phase 0/CI)

---

Note: Use the Task Tracker checkboxes to mark progress; keep changes minimal per EKO rules.

---

## Architecture Priorities

The following work items are recommended to keep the project scalable without overengineering:

- [ ] Add `src/models/` for typed data objects (`settings`, `reminder`, `todo`, `notification`, `automation_rule`)
- [ ] Add `src/app/service_registry.py` for dependency wiring
- [ ] Add `src/core/event_bus.py` for service-to-service signals
- [ ] Add `src/core/scheduler_service.py` for reminder and automation timing
- [ ] Add `src/core/state_service.py` for runtime UI, silent-mode, and tray state
- [ ] Add `src/storage/storage_interface.py` and `src/storage/schema.py` for storage abstraction and schema versioning
- [ ] Add `src/utils/result.py` for safe service results instead of raw exceptions where appropriate
- [ ] Add `src/core/error_handler.py` for centralized user-facing error handling
- [ ] Add async worker support for file I/O and background jobs to avoid blocking the UI thread
- [ ] Add early tests for `json_store`, `backup_service`, `reminder_service`, and `notification_service`

---

## Project Coding Rules

- Keep source files ideally under 400 lines.
- Use 600-700 lines only when a single logical unit clearly benefits from staying together.
- Prefer splitting by responsibility before a file becomes difficult to review.
- Use ASCII English identifiers for code symbols, file names, and module names.
- Keep UI labels and user-visible text in Turkish.
- Write comments and docstrings in English for consistency with tooling and task documents.
- Keep documentation and task instructions in English.
- Use a background maintenance task for trimming and cleanup instead of trimming on every write when the operation is not latency-sensitive.
- Add CI or pre-commit checks for file length, formatting, and core test execution.

---

## CI / Style Checks

- [ ] Add style checks to enforce the project coding rules
- [ ] Add a file-length check to flag files over the soft limit
- [ ] Add a formatting and linting hook for Python files
- [ ] Add a test hook for the core storage and service layer

Note: These checks should stay lightweight and must not block small iterative EKO tasks unnecessarily.

---

## Task 8.2 — Save Settings from UI
Changing settings updates config.json.

Acceptance:
- restart keeps settings

---

## Task 8.3 — Apply Settings Without Restart Where Safe
Apply:
- widget visibility
- opacity
- silent mode

Restart can be acceptable for complex surface rebuilds.

---

# PHASE 9 — REMINDERS

## Task 9.1 — Create Reminder Service
Create src/core/reminder_service.py.

Reminder fields:
- id
- date
- time
- message
- status
- created_at

---

## Task 9.2 — Create Reminder Dialog
Create src/ui/reminder_dialog.py.

Required:
- date
- time
- message
- save

---

## Task 9.3 — Store Reminders
Use data/reminders.json.

Acceptance:
- reminders persist after restart

---

## Task 9.4 — Trigger Due Reminders
Check due reminders using timer.

When due:
- popup
- tray notification

---

## Task 9.5 — Detect Missed Reminders on Startup
If reminder time passed while app was closed:
- mark as missed
- notify user once

---

## Task 9.6 — Add Snooze
Options:
- 5 minutes
- 10 minutes
- 60 minutes

---

# PHASE 10 — TTS

## Task 10.1 — Create TTS Service
Create src/core/tts_service.py.

Required:
- pyttsx3 offline backend
- fail silently if unavailable
- no online TTS

---

## Task 10.2 — Connect TTS to Reminders
Reminder due:
- speak message if enabled
- respect silent mode

---

## Task 10.3 — Keep TTS Non-blocking
Do not freeze UI while speaking.

---

# PHASE 11 — TODO

## Task 11.1 — Create Todo Service
Create src/core/todo_service.py.

Todo fields:
- id
- title
- priority
- status
- due_date
- created_at
- completed_at

---

## Task 11.2 — Create Todo Panel
Create src/ui/todo_panel.py.

Required:
- list todos
- add todo
- complete todo
- delete todo
- postpone todo

---

## Task 11.3 — Add Sorting
Sorting:
1. Today first
2. Active before postponed
3. High priority first
4. Completed last

---

## Task 11.4 — Persist Todos
Use data/todos.json.

---

# PHASE 12 — HISTORY AND DATA LIMITS

## Task 12.1 — Create History Service
Create src/core/history_service.py.

Store:
- time
- type
- title
- message
- source

---

## Task 12.2 — Limit Notification History
Rules:
- max 500 notification history records
- trim old entries on startup
- trim old entries after write

---

## Task 12.3 — Limit Completed Todos
Rules:
- max 300 completed todos
- older completed todos trimmed

---

## Task 12.4 — Do Not Keep Old Reminder History
Keep only:
- active
- snoozed
- missed if still unresolved

---

# PHASE 13 — BACKUP AND RECOVERY

## Task 13.1 — Create Backup Service
Create src/core/backup_service.py.

Required:
- backup JSON before overwrite
- restore from .bak if current file broken

---

## Task 13.2 — Add Recovery Logging
Log all recovery events to logs/app.log.

---

## Task 13.3 — Add Hidden Secondary Backup
Optional but recommended:
- copy data folder to safe local backup location on app exit

---

# PHASE 14 — WIDGET SYSTEM

## Task 14.1 — Add Widget Toggle System
Enable/disable:
- clock
- date
- battery
- reminder
- todo

---

## Task 14.2 — Add Compact Mode
Compact mode:
- smaller layout
- fewer details

---

## Task 14.3 — Add Normal Mode
Normal mode:
- full widget information

---

# PHASE 15 — RECURRING REMINDERS

## Task 15.1 — Add Daily Recurrence
Simple daily repeat.

---

## Task 15.2 — Add Weekly Recurrence
Weekly repeat on single selected day only.

---

## Task 15.3 — Add Weekdays Recurrence
Monday-Friday only.

---

## Task 15.4 — Explicitly Reject Complex Recurrence
Do not implement:
- holiday exclusions
- custom complex intervals
- full calendar logic

---

# PHASE 16 — SMART TODO

## Task 16.1 — Add Today View
Show todos due today first.

---

## Task 16.2 — Add Priority View
Filter high priority todos.

---

## Task 16.3 — Add Completed History View
Simple completed todos view only.

---

# PHASE 17 — BASIC INSIGHTS

## Task 17.1 — Add Simple Daily Summary
Show:
- completed tasks today
- missed reminders
- active reminders

---

## Task 17.2 — Avoid Battery Analytics
Do not add detailed battery statistics.

Only critical event count may be shown if already logged.

---

# PHASE 18 — LIGHT AUTOMATION

## Task 18.1 — Create Simple Rule Model
Rules stored in JSON.

Max:
- 10 rules

---

## Task 18.2 — Supported Triggers Only
Allowed triggers:
- battery_level_below
- charger_unplugged
- time_reached

---

## Task 18.3 — Supported Actions Only
Allowed actions:
- notify
- mute_notifications
- reduce_notification_frequency

---

## Task 18.4 — Reject Complex Automation
Do not implement:
- scripting
- nested logic
- chained rules
- plugin system

---

# PHASE 19 — TESTS

## Task 19.1 — Test JSON Store
Test:
- missing file
- broken JSON
- atomic write
- default keys

Notes:
- JSON store tests should be added as soon as the storage layer exists, not deferred until the final phase.

---

## Task 19.2 — Test Backup Service
Test:
- backup creation
- recovery from broken file

---

## Task 19.3 — Test Reminder Logic
Test:
- due reminder
- missed reminder
- snooze

---

## Task 19.4 — Test Notification Cooldown
Test:
- repeated same notification does not spam

---

# PHASE 20 — FINAL STABILIZATION

## Task 20.1 — Manual Test Checklist
Create MANUAL_TESTS.md.

Include:
- startup
- tray behavior
- close-to-tray
- clock update
- battery fallback
- settings save
- reminder due
- todo add/complete
- broken JSON recovery

Notes:
- Keep this checklist updated whenever a new user-visible behavior is added or changed.

---

## Task 20.2 — Clean Files
Check:
- no file over 500 lines unless justified
- no business logic inside UI
- no unused large abstractions

---

## Task 20.3 — Freeze Mini Release
Mini release must include:
- clock
- date
- battery
- desktop surface
- tray
- settings
- notifications
- safe storage

Do not continue to the Full version until Mini is stable.
