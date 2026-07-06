# D_DeskPilot Master Task Roadmap

This is the single canonical implementation task file for D_DeskPilot.
Do not maintain another active task checklist. Supporting MD files may exist as references, but progress is tracked here only.

## Product Definition
D_DeskPilot is a local-first Windows desktop productivity assistant built with PySide6/PyQt6.

Core purpose:
- Show clock, date, and battery state on a lightweight desktop surface.
- Keep reminders, todos, notifications, settings, tray control, and layout behavior in one app.
- Stay private, offline, free, stable, and Turkish-first for v1.
- Track future localization and broader productivity features without starting them before v1 stability.

## Current Focus Lock
- Current focus is Phase 6 / Todo.
- Until Task 6.2 is complete, do not start Reminder, Sync, Mobile, Packaging, or global rollout work.
- Phase 10 is future vision only; do not implement it during the current Todo focus.

## Non-Negotiable Rules
- Turkish-first v1 stabilization comes before full localization.
- No paid service, paid API, cloud dependency, user account, or mandatory internet in v1.
- JSON persistence stays the storage model for v1.
- Business logic belongs to services/models; UI renders state and sends actions.
- Keep patches small and feature-scoped.
- Do not modify unrelated files while implementing the current task.
- Do not refactor working files unless needed for bug, feature, performance, or file-size risk.
- Prefer files under 400 lines; 600 lines only when unavoidable.
- Keep app runnable after each task.
- For Python code edits, run touched-file syntax check or state why skipped.

## Execution Gate
Before implementation:
- Read only the current task and directly relevant files.
- Identify files/layers that may change.
- Check whether similar logic already exists.
- Avoid future-task implementation.

After implementation:
- List changed files.
- Report syntax/test result or say clearly that it was not run.
- Mark the task done only after the requested scope is complete.
- Never continue to the next task until the current task is verified by the user.

## Current Repo State
- Branch noted in STATE: `v2`.
- Current focus: stabilize Turkish v1.
- Last completed note: QuickActions hover stability improved.
- QuickActions is considered stable/frozen. Do not modify unless explicitly requested.
- Dirty files may exist outside this task; do not overwrite unrelated changes.

## Current Architecture Snapshot
- Entry: `main.py` -> `DeskPilot.py`.
- App boot: single-instance guard, logging, settings load, app fonts, tray, main transparent window.
- Main window: `core_window.py` composed with window/runtime/navigation/settings/topmost/free-layout mixins.
- Settings: `core_settings.py`, `deskpilot.settings.json`, `ui_settings.py`, `ui_ayarlar_formlar.py`.
- Clock/date/battery: main panel widgets plus `pil_servisi.py`.
- Reminders: `hatirlatici_modeli.py`, `hatirlatici_servisi.py`, `hatirlatici_listesi.py`, `hatirlatici_popup.py`.
- Todos: `gorev_modeli.py`, `gorev_servisi.py`, `gorev_arayuzu.py`, `kart.py`, `quick_actions.py`.
- Tray: `sistem_tepsisi.py`.
- Notifications/logging: `bildirim_servisi.py`, `log_servisi.py`, `utils.py`.
- i18n foundation: `dil_yonetimi.py`, `translations/*.json`.

## Completion Legend
- `[x]` done and present in current repo.
- `[ ]` pending.
- `[~]` partial/in-progress; do not treat as complete.
- `[!]` blocked or needs explicit decision.

---

# Phase 0 - Governance and Safety

## Task 0.1 - Keep Single Task Source
Goal:
- Keep this file as the single progress source.

Scope:
- `Task.md` only.

Acceptance:
- [x] `Task.md` is the master roadmap.
- [x] Redundant task pointer documents were removed.
- [x] Excess per-module checklists were removed from this roadmap.
- [ ] After each completed feature, update this file.

## Task 0.2 - Preserve Scoped Execution Rules
Acceptance:
- [x] SPP/EKO style rules exist in repo instructions.
- [x] Economic-token workflow is defined.
- [ ] Keep final task responses short unless detail is requested.

## Task 0.3 - Release Notes Structure
Acceptance:
- [ ] Add simple release notes/changelog structure for v1.
- [ ] Record changed files and check results per feature.

---

# Phase 1 - Startup, Settings, Storage

## Task 1.1 - App Entry and Single Instance
Acceptance:
- [x] `main.py` launcher exists.
- [x] `DeskPilot.py` is main application entry.
- [x] Single-instance mutex exists on Windows.
- [ ] Add clear fatal startup message only if needed.

## Task 1.2 - Settings Model and JSON Persistence
Acceptance:
- [x] `PanelSettings` exists.
- [x] Settings load from app data or local fallback.
- [x] Missing/unknown keys are handled safely.
- [x] Atomic settings write uses temp + replace.
- [x] Broken settings file is backed up.
- [ ] Review old-key migration and defaults.

## Task 1.3 - General JSON Store Hardening
Goal:
- Apply the old repo safety vision to all JSON persistence.

Acceptance:
- [ ] Use atomic write for todos and reminders.
- [ ] Add `.bak` recovery plan for todos/reminders.
- [ ] Log recovery events.
- [ ] Add hidden secondary backup only if it stays simple.

---

# Phase 2 - Clock, Date, Battery

## Task 2.1 - Clock Module Stabilization
Acceptance:
- [x] Clock module exists.
- [x] Embedded digital fonts exist.
- [x] Stencil/default clock font path exists.
- [x] System fonts remain selectable.
- [x] Clock font scaling exists.
- [x] Clock settings survive restart.
- [ ] Keep seconds visibility behavior stable.
- [ ] Keep clock behavior stable in free layout.
- [ ] Defer seconds-width jitter fix unless explicitly requested.

## Task 2.2 - Date Module Stabilization
Acceptance:
- [x] Date module exists.
- [ ] Keep date format, font, visibility, restart, and free-layout behavior stable when touched.

## Task 2.3 - Battery Module Stabilization
Acceptance:
- [x] Battery module exists.
- [x] Battery thresholds exist.
- [x] Plug/unplug detection exists.
- [ ] Keep unavailable-battery fallback safe.
- [ ] Keep low/critical/full warning behavior stable.
- [ ] Keep silent mode respected by battery alerts.

---

# Phase 3 - Window, Layout, Tray

## Task 3.1 - Main Window Stability
Acceptance:
- [x] Transparent draggable main window exists.
- [x] Always-on-top behavior is extracted/stabilized.
- [x] Popup focus/topmost behavior improved.
- [ ] Keep grouped startup, missing-monitor fallback, and scaling behavior stable.

## Task 3.2 - Free Layout
Acceptance:
- [x] Free layout exists.
- [x] Multi-monitor fields exist in settings.
- [ ] Preserve free-layout startup behavior.
- [ ] Preserve move-all-modules behavior.
- [ ] Preserve per-widget saved positions and scaling bounds.

## Task 3.3 - System Tray
Acceptance:
- [x] Tray integration exists.
- [x] Show/hide action exists.
- [x] New Reminder action exists.
- [x] New Todo action exists.
- [x] Settings action exists.
- [x] Quit action exists.
- [x] Tray tooltip summary exists.
- [ ] Keep close/show/hide behavior stable.
- [ ] Keep unsupported-tray fallback simple.

---

# Phase 4 - Notification System

## Task 4.1 - Unified Notification Service
Goal:
- Route alert behavior through a common service without UI coupling.

Acceptance:
- [x] `bildirim_servisi.py` exists.
- [ ] Consolidate notification service behavior.
- [ ] Route battery alerts through common service.
- [ ] Route reminder alerts through common service.
- [ ] Add per-source cooldown rules.
- [ ] Respect silent mode: no sound/TTS, visual allowed.

## Task 4.2 - Notification History and Data Limits
Acceptance:
- [ ] Add simple notification history model if needed.
- [ ] Limit notification history to max 500 records.
- [ ] Trim old records on startup and after writes.
- [ ] Keep UI simple; no analytics system.

---

# Phase 5 - Reminder System

## Task 5.1 - Reminder Baseline
Acceptance:
- [x] Reminder model exists.
- [x] Reminder JSON service exists.
- [x] Reminder popup exists.
- [x] Reminder list UI exists.
- [x] Active/completed/missed states exist.
- [x] Daily/weekly recurrence foundation exists.

## Task 5.2 - Reminder Data Model Upgrade
Acceptance:
- [ ] Add optional `voice_enabled`.
- [ ] Add `voice_alerts` list.
- [ ] Add `voice_repeat_rule`.
- [ ] Add `notified_keys` to prevent duplicate alerts.
- [ ] Old reminders load with defaults.
- [ ] Broken records are skipped safely.

## Task 5.3 - Reminder Time Text
Acceptance:
- [ ] Generate Turkish remaining-time text.
- [ ] Cover minute/hour/day text.
- [ ] Cover `Zamani geldi` state.
- [ ] Handle past time safely.

## Task 5.4 - Reminder Trigger and Snooze
Acceptance:
- [ ] Support one-time reminder flow.
- [ ] Support snooze 5/10/60 minute flow.
- [ ] Handle missed reminder after restart.
- [ ] Keep repeated alerts from firing twice.

## Task 5.5 - Reminder UI Polish
Acceptance:
- [ ] Refresh add/edit form without overloading settings.
- [ ] Show preview of spoken text.
- [ ] Enforce invalid input rules.
- [ ] Polish reminder cards and status colors.
- [ ] Popup should not hide the main clock surface unnecessarily.

## Task 5.6 - Reminder TTS
Acceptance:
- [ ] Add offline Windows/pyttsx3 TTS wrapper if not already present.
- [ ] Prefer male voice when available.
- [ ] Fall back to system default voice.
- [ ] Keep TTS non-blocking.
- [ ] Disable silently/log safely if TTS fails.
- [ ] No cloud/API TTS.

---

# Phase 6 - Todo System

## Task 6.1 - Todo Baseline
Acceptance:
- [x] Todo model exists.
- [x] Todo JSON service exists.
- [x] Todo UI exists.
- [x] Dynamic priority foundation exists.
- [x] Task card visual redesign exists.
- [x] New Task dialog exists.
- [x] Shared date/time editor exists.
- [x] Todo i18n pilot wiring exists.

## Task 6.2 - Todo Data Model
Execution order:
- First inspect current Todo model, service, and UI fields.
- Then finalize only the minimal v1 data model fields.

Acceptance:
- [x] Confirm current fields before editing: title, description, status, priority, planned time, ordering, completed/cancelled times.
- [x] Decide whether subtasks/checklist stay deferred for v1.
- [x] Preserve old JSON compatibility.
- [x] Keep JSON readable and stable.
- [x] Do not reopen already-decided deleted/cancelled state behavior.

## Task 6.3 - Todo Workflow Polish
Acceptance:
- [ ] Polish Turkish workflow.
- [ ] Support add/edit task dialog behavior.
- [ ] Save/load task date and time.
- [ ] Show overdue, completed, cancelled, and deleted states clearly.
- [ ] Keep priority sorting and completed cleanup stable.

## Task 6.4 - Todo UI/UX
Acceptance:
- [ ] Keep card-based visual language.
- [ ] Keep quick task entry fast.
- [ ] Add/keep today, tomorrow, week, and completed filters.
- [ ] Add/keep search with Turkish characters.
- [ ] Keep empty state useful.
- [ ] Keep panel from looking flat/gray.

## Task 6.5 - Todo Theme and Resize
Acceptance:
- [ ] Keep mini panel theme controls inside Todo where practical.
- [ ] Save panel/card/text/border/accent colors.
- [ ] Apply colors immediately.
- [ ] Add contrast guard or safe fallback.
- [ ] Keep proportional resize behavior for text, checkbox, padding, and icons.

---

# Phase 7 - Settings, Design System, i18n

## Task 7.1 - Settings Window
Acceptance:
- [x] Settings window exists.
- [x] Language tab exists.
- [x] Clock font selection supports embedded fonts.
- [x] Task priority settings exist.
- [ ] Review Turkish settings UX.
- [ ] Add restart notice when language changes.
- [ ] Keep missing/old-key and reset-to-default flows stable.

## Task 7.2 - Design System Consolidation
Acceptance:
- [ ] Keep shared component style consistent.
- [ ] Avoid flat gray wall look.
- [ ] Keep cards readable and sympathetic.
- [ ] Keep resize proportional.
- [ ] Keep accessibility/contrast in mind.

## Task 7.3 - i18n Foundation
Acceptance:
- [x] `dil_yonetimi.py` exists.
- [x] `translations/tr.json`, `en.json`, `ar.json` exist.
- [x] `PanelSettings.language` exists.
- [x] Language selector exists.
- [x] Turkish-first v1 / v2 localization rule exists.
- [ ] New UI text should use translation keys where practical.
- [ ] Audit hardcoded Todo UI text.
- [ ] Do not polish English/Arabic in v1.
- [ ] v2: full English pass.
- [ ] v2: full Arabic/RTL pass.

---

# Phase 8 - Assets, Packaging, Release

## Task 8.1 - Assets and Fonts
Acceptance:
- [x] Embedded digital fonts exist.
- [x] Logo/icon assets exist.
- [x] Hourglass/overdue icons exist.
- [x] Source-mode asset paths work.
- [ ] Keep packaged asset paths stable before release.
- [ ] Remove unused assets only after review.

## Task 8.2 - Packaging
Acceptance:
- [ ] Define release build command.
- [ ] Build EXE.
- [ ] Preserve settings path in EXE.
- [ ] Preserve assets in EXE.
- [ ] Confirm clean install behavior before release.
- [ ] Prepare Turkish v1 release checklist.
- [ ] Tag release.

---

# Phase 9 - Code Health

## Task 9.1 - Lightweight Code Check Policy
Acceptance:
- [ ] For Python code edits, run touched-file syntax check or explain skip.
- [ ] For behavior-heavy changes, run targeted existing tests if relevant.
- [ ] Do not add per-task checklists.

## Task 9.2 - Core Service Tests
Acceptance:
- [ ] Test settings load defaults.
- [ ] Test broken JSON recovery.
- [ ] Test reminder trigger logic.
- [ ] Test notification cooldown.
- [ ] Test Todo sort/status behavior.

## Task 9.3 - Code Health
Acceptance:
- [ ] No new source file above 500 lines without reason.
- [ ] UI/business boundary remains clear.
- [ ] Remove dead code only when clearly unused.
- [ ] Do not rewrite the app into `src/` architecture in one step.

---

# Phase 10 - Future / v2+ Deferred Work

Note:
- This phase is deferred future vision only.
- Do not start Phase 10 work until v1 is stable and the current focus lock is released.

## Task 10.1 - Service Registry and Event Bus
Goal:
- Preserve the old repo architecture vision without forcing v1 rewrite.

Acceptance:
- [ ] Define when service registry is worth adding.
- [ ] Define event bus boundaries for services-to-UI signals.
- [ ] Migrate gradually only when touching related code.

## Task 10.2 - Backup Manager
Acceptance:
- [ ] Add simple backup manager if JSON recovery needs it.
- [ ] Keep backup local and private.
- [ ] No cloud sync.

## Task 10.3 - Smart Todo
Acceptance:
- [ ] Today view.
- [ ] Priority view.
- [ ] Completed history view.
- [ ] No complex project-management system.

## Task 10.4 - Basic Insights
Acceptance:
- [ ] Completed tasks count.
- [ ] Missed reminders count.
- [ ] Active reminders count.
- [ ] Avoid battery analytics.

## Task 10.5 - Light Automation
Acceptance:
- [ ] Max 10 simple JSON rules.
- [ ] Supported triggers only: battery below, charger unplugged, time reached.
- [ ] Supported actions only: notify, mute notifications, reduce notification frequency.
- [ ] No scripting, nested logic, chaining, or plugin system.

## Task 10.6 - Hotkeys and Clipboard
Acceptance:
- [ ] Global hotkey service for New Reminder and Toggle UI.
- [ ] Clipboard manager max 100 items if added.
- [ ] Keep both optional and lightweight.

## Task 10.7 - Optional Account and Multi-Desktop Sync
Status:
- Deferred future vision only.

Goal:
- After Turkish v1 is stable, add optional account-based sync so the same user can access data and alerts across their own desktop computers.

Recommendation:
- Prefer email magic link, OAuth, passkey, or trusted device pairing over storing raw email/password.
- Keep local-first desktop usage available without an account.

Acceptance:
- [ ] Decide identity option: email magic link, OAuth, passkey, device pairing, or a hybrid model.
- [ ] Define user, device, session, and trusted-device model.
- [ ] Define encrypted sync schema for settings, reminders, todos, and notification state.
- [ ] Add offline queue and background sync plan.
- [ ] Add conflict rules for edits from multiple computers.
- [ ] Add remote alert routing for reminders and todos.
- [ ] Add account recovery, export, delete, and privacy controls.
- [ ] Keep sync optional and disabled by default until stable.

## Task 10.8 - Android Mobile Companion
Status:
- Deferred future vision only.

Goal:
- After desktop account/sync is stable, add an Android-first mobile companion with a polished interface.

Recommendation:
- Prefer Flutter for mobile if later iOS/global UI reuse matters; consider native Android only if deep platform integration becomes the priority.

Acceptance:
- [ ] Design Android-first home, reminder, todo, and alert screens.
- [ ] Reuse the same account and sync API as desktop.
- [ ] Support push notifications with local fallback where possible.
- [ ] Support quick add reminder, quick add todo, snooze, complete, and dismiss flows.
- [ ] Keep mobile cache offline-first.
- [ ] Keep desktop and Android alert states consistent.
- [ ] Prepare iOS only after Android core is stable.

## Task 10.9 - Global Version Rollout
Status:
- Deferred future vision only.

Goal:
- Move to global versions only after desktop sync and Android companion work reliably.

Acceptance:
- [ ] Finish full i18n workflow after Turkish v1 and sync/mobile milestones.
- [ ] Complete English UI/content pass.
- [ ] Complete Arabic/RTL UI/content pass if still targeted.
- [ ] Add region, timezone, date/time, and notification locale rules.
- [ ] Prepare public privacy, data handling, and support documentation.
- [ ] Prepare global release assets after product behavior is stable.

---

# Deferred / Do Not Do in v1
- [ ] No SQLite migration.
- [ ] No plugin system.
- [ ] No cloud sync.
- [ ] No paid API or paid service.
- [ ] No world clock.
- [ ] No full English/Arabic polish.
- [ ] No advanced theme engine.
- [ ] No app-wide architectural rewrite.
- [ ] No complex recurrence/calendar engine.
- [ ] No complex automation/scripting.
