# D_DeskPilot Combined Master Task Roadmap

This file merges task structures from:
- current `main` / `Task.md`
- local `v2` branch `Task.md`
- `D:\Code\mskaymaz\D_DeskPilot_old` task roadmaps

Do not maintain duplicate active task lists. Use this as the combined planning reference unless `Task.md` is intentionally promoted later.

## Product Definition
D_DeskPilot is a local-first Windows desktop productivity assistant built with PySide6/PyQt6.

Core purpose:
- Show clock, date, and battery state on a lightweight desktop surface.
- Keep reminders, todos, notifications, settings, tray control, and layout behavior in one app.
- Stay private, offline, free, stable, and Turkish-first for v1.
- Track future localization, sync, mobile, and broader productivity features without starting them before v1 stability.

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
- Current branch after pull: `main`.
- Local branch `v2` still exists; its remote tracking branch was removed upstream.
- Current focus: stabilize Turkish v1.
- QuickActions is considered stable/frozen. Do not modify unless explicitly requested.
- Dirty files may exist outside a task; do not overwrite unrelated changes.

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
- Keep one active progress source and prevent parallel checklist drift.

Scope:
- Task roadmap documents only.

Acceptance:
- [x] `Task.md` is the current master roadmap.
- [x] Redundant task pointer documents were removed from current repo.
- [x] Excess per-module checklists were removed from the main roadmap.
- [ ] Decide whether `MyTask.md` replaces `Task.md` after review.
- [ ] After each completed feature, update the chosen master task file.

## Task 0.2 - Preserve Scoped Execution Rules
Acceptance:
- [x] SPP/EKO style rules exist in repo instructions.
- [x] Economic-token workflow is defined.
- [x] Task execution gate exists.
- [ ] Keep final task responses short unless detail is requested.
- [ ] Keep commits and patches feature-scoped.

## Task 0.3 - Release Notes Structure
Acceptance:
- [ ] Add simple release notes/changelog structure for v1.
- [ ] Record changed files and check results per feature.
- [ ] Add a lightweight package/release summary only when preparing release.

## Task 0.4 - Developer Health Docs
Acceptance:
- [ ] Add or update setup/run instructions.
- [ ] Document core verification commands.
- [ ] Keep documentation concise and aligned with local-first rules.

---

# Phase 1 - Startup, Settings, Storage

## Task 1.1 - App Entry and Single Instance
Acceptance:
- [x] `main.py` launcher exists.
- [x] `DeskPilot.py` is main application entry.
- [x] Single-instance mutex exists on Windows.
- [x] Basic startup logging exists.
- [ ] Verify startup on clean Windows session.
- [ ] Verify startup with missing optional assets.
- [ ] Add clear fatal startup message only if needed.

## Task 1.2 - Settings Model and JSON Persistence
Acceptance:
- [x] `PanelSettings` exists.
- [x] Settings load from app data or local fallback.
- [x] Missing/unknown keys are handled safely.
- [x] Atomic settings write uses temp + replace.
- [x] Broken settings file is backed up.
- [ ] Review old-key migration and defaults.
- [ ] Clamp scale, opacity, thresholds, intervals, and positions.
- [ ] Add config example only if it stays useful and maintained.

## Task 1.3 - General JSON Store Hardening
Goal:
- Apply the old repo safety vision to all JSON persistence.

Acceptance:
- [ ] Use atomic write for todos and reminders.
- [ ] Add `.bak` recovery plan for todos/reminders.
- [ ] Log recovery events.
- [ ] Add hidden secondary backup only if it stays simple.
- [ ] Avoid data loss if a write fails halfway.

## Task 1.4 - Application Lifecycle
Goal:
- Keep startup and shutdown ordering explicit.

Acceptance:
- [ ] Define startup order for logger, settings, storage, services, tray, and UI.
- [ ] Define shutdown order for timers, tray, services, and pending writes.
- [ ] Handle service startup failure without silent crashes.
- [ ] Keep lifecycle logic small; no framework rewrite.

## Task 1.5 - Event Bus
Status:
- Deferred unless needed by touched code.

Acceptance:
- [ ] Define event boundaries for service-to-UI updates.
- [ ] Add simple subscribe/unsubscribe/publish if direct coupling becomes risky.
- [ ] Prevent subscriber exceptions from breaking all events.
- [ ] Avoid introducing an async framework.

## Task 1.6 - Service Registry
Status:
- Deferred future architecture.

Acceptance:
- [ ] Define when registry is worth adding.
- [ ] Keep dependency wiring simple.
- [ ] Do not rewrite the app around a registry in one step.

---

# Phase 2 - Clock, Date, Battery

## Task 2.1 - Clock Module Stabilization
Acceptance:
- [x] Clock module exists.
- [x] Digital font rendering path exists for the clock.
- [x] Stencil/default clock font path exists.
- [x] System fonts remain selectable.
- [x] Clock font scaling exists.
- [x] Clock settings survive restart.
- [ ] Verify seconds visibility toggle.
- [ ] Keep seconds visibility behavior stable.
- [ ] Keep clock behavior stable in free layout.
- [ ] Defer seconds-width jitter fix unless explicitly requested.

## Task 2.2 - Date Module Stabilization
Acceptance:
- [x] Date module exists.
- [ ] Verify date format setting.
- [ ] Verify date font setting.
- [ ] Verify date visibility toggle.
- [ ] Keep date format, font, visibility, restart, and free-layout behavior stable when touched.

## Task 2.3 - Battery Module Stabilization
Acceptance:
- [x] Battery module exists.
- [x] Battery thresholds exist.
- [x] Plug/unplug detection exists.
- [ ] Keep unavailable-battery fallback safe.
- [ ] Keep low/critical/full warning behavior stable.
- [ ] Keep silent mode respected by battery alerts.
- [ ] Verify battery display after restart.

---

# Phase 3 - Window, Layout, Tray

## Task 3.1 - Main Window Stability
Acceptance:
- [x] Transparent draggable main window exists.
- [x] Always-on-top behavior is extracted/stabilized.
- [x] Popup focus/topmost behavior improved.
- [ ] Keep grouped startup, missing-monitor fallback, and scaling behavior stable.
- [ ] Verify right mouse + wheel scaling.

## Task 3.2 - Free Layout
Acceptance:
- [x] Free layout exists.
- [x] Multi-monitor fields exist in settings.
- [ ] Preserve free-layout startup behavior.
- [ ] Preserve move-all-modules behavior.
- [ ] Preserve per-widget saved positions and scaling bounds.
- [ ] Add arrange command only if it fits existing UI.

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
- [ ] Verify tray menu actions manually before release.

## Task 3.4 - Display Modes
Status:
- Existing app currently uses current main/free layout patterns; old overlay/combined/separated vision is deferred unless intentionally revived.

Acceptance:
- [ ] Decide whether taskbar overlay mode belongs in v1.
- [ ] Decide whether desktop combined mode differs from current main surface.
- [ ] Decide whether separated widgets are already covered by free layout.
- [ ] If revived, preserve shared clock/date/battery logic and avoid duplicate timers.

## Task 3.5 - Window Stacking Manager
Status:
- Deferred unless topmost instability returns.

Acceptance:
- [ ] Add configurable topmost refresh only if normal topmost behavior is insufficient.
- [ ] Clamp refresh interval to a safe range.
- [ ] Skip hidden or destroyed windows safely.
- [ ] Verify no CPU spike or focus-stealing regression.

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
- [ ] Route Todo alerts through common service only if needed.
- [ ] Add per-source cooldown rules.
- [ ] Respect silent mode: no sound/TTS, visual allowed.

## Task 4.2 - Notification History and Data Limits
Acceptance:
- [ ] Add simple notification history model if needed.
- [ ] Limit notification history to max 500 records.
- [ ] Trim old records on startup and after writes.
- [ ] Keep UI simple; no analytics system.

---

# Phase 5 - Reminder, Alarm, TTS

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

## Task 5.7 - Basic Alarm
Status:
- Deferred unless user explicitly wants alarm behavior separate from reminders.

Acceptance:
- [ ] Define whether alarm is separate from reminder in v1.
- [ ] If added, support one-shot and simple daily alarm.
- [ ] Add enable/disable and simple snooze if practical.
- [ ] Persist locally in JSON.
- [ ] Reuse notification/TTS rules.

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
- [ ] Support postpone only if it fits current model cleanly.

## Task 6.4 - Todo UI/UX
Acceptance:
- [ ] Keep card-based visual language.
- [ ] Keep quick task entry fast.
- [ ] Add/keep today, tomorrow, week, priority, and completed filters.
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

## Task 6.6 - Todo History Limits
Acceptance:
- [ ] Define completed todo retention rule.
- [ ] Limit completed todo history only if files can grow too much.
- [ ] Trim old completed todos safely and visibly.

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
- [ ] Verify every setting persists after restart.

## Task 7.2 - Design System Consolidation
Acceptance:
- [ ] Keep shared component style consistent.
- [ ] Avoid flat gray wall look.
- [ ] Keep cards readable and sympathetic.
- [ ] Keep resize proportional.
- [ ] Keep accessibility/contrast in mind.
- [ ] Keep hover icons/tooltips clear where used.

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

## Task 7.4 - Per-Widget Appearance Settings
Acceptance:
- [ ] Keep clock/date/battery font controls stable.
- [ ] Keep per-widget colors and bold settings stable where present.
- [ ] Preserve scale bounds for each widget.
- [ ] Add live preview only where it does not destabilize settings.

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

## Task 8.3 - Windows Autostart
Status:
- Optional v1 polish.

Acceptance:
- [ ] Decide whether Windows autostart belongs in v1.
- [ ] If added, handle registry/permission errors safely.
- [ ] Keep setting disabled unless user enables it.

---

# Phase 9 - Code Health and Verification

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
- [ ] Test battery state classification when service logic is touched.

## Task 9.3 - Code Health
Acceptance:
- [ ] No new source file above 500 lines without reason.
- [ ] UI/business boundary remains clear.
- [ ] Remove dead code only when clearly unused.
- [ ] Do not rewrite the app into `src/` architecture in one step.

## Task 9.4 - Manual Test Checklist
Acceptance:
- [ ] Add or update manual checklist before release.
- [ ] Cover startup, tray, close-to-tray, clock, date, battery, settings, reminders, todos, TTS, JSON recovery, and packaging.
- [ ] Keep checklist practical enough to run.

## Task 9.5 - CI and Style Checks
Status:
- Optional developer-health work.

Acceptance:
- [ ] Add lightweight test command documentation.
- [ ] Add CI only when tests are stable enough.
- [ ] Avoid blocking small EKO/SPP tasks with heavy tooling.

---

# Phase 10 - Future / v2+ Deferred Work

Note:
- This phase is deferred future vision only.
- Do not start Phase 10 work until v1 is stable and the current focus lock is released.

## Task 10.1 - Service Registry and Event Bus
Acceptance:
- [ ] Define when service registry is worth adding.
- [ ] Define event bus boundaries for services-to-UI signals.
- [ ] Migrate gradually only when touching related code.

## Task 10.2 - Backup Manager
Acceptance:
- [ ] Add simple backup manager if JSON recovery needs it.
- [ ] Keep backup local and private.
- [ ] Backup stays local and private; no sync behavior is introduced here.

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
- [ ] Clipboard history must be opt-in and local only.

## Task 10.7 - Optional Account and Multi-Desktop Sync
Status:
- Deferred future vision only.

Goal:
- After Turkish v1 is stable, add optional account-based sync so the same user can access data and alerts across their own desktop computers.

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

## Task 10.10 - Advanced Widget Interaction
Acceptance:
- [ ] Revisit individual drag/drop only if current free layout is insufficient.
- [ ] Keep mouse wheel scaling within safe min/max bounds.
- [ ] Keep hover action routing stable and non-intrusive.

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
- [ ] No mandatory account.
- [ ] No web interface.
- [ ] No QML/C++ rewrite.
