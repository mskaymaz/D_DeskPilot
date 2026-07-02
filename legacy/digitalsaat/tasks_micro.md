# tasks_micro.md

## Purpose
This file is a very small-step implementation plan for Gemini Code Assist and Codex.
It is based on `task_edit.md` and must be used to update the existing DigitalSaat project safely.

The goal is NOT to rebuild the project blindly.
The goal is to repair, align, modularize, test, and polish the existing project while preserving the intended DigitalSaat UI identity.

## Global Rules for AI Coding Assistants

- [ ] Read `task_edit.md` fully before editing any file.
- [ ] Read this `tasks_micro.md` fully before editing any file.
- [ ] Inspect the whole project structure before making changes.
- [ ] Do not replace the UI with a generic/simple interface.
- [ ] Treat the UI mismatch as a critical issue.
- [ ] Preserve the intended DigitalSaat identity: transparent, compact, frameless, draggable clock/date/battery panel.
- [ ] Preserve free-layout behavior for separate clock/date/battery windows.
- [ ] Do not remove legacy/reference files without explicit confirmation.
- [ ] Prefer small modular edits over large rewrites.
- [ ] After each meaningful change, run the relevant verification step.
- [ ] Mark each finished task with `[x]`.
- [ ] If there is a real conflict, stop and write the problem in Turkish with the exact files involved and the decision needed.
- [ ] Do not ask questions for normal implementation steps.
- [ ] When all possible tasks are complete, write: `Bitti.` and summarize changes briefly.

## Line Count and Responsibility Rules

- [ ] Before editing, list files over 500 lines.
- [ ] Do not expand any already-large file unless necessary.
- [ ] Keep new source files under 300 lines when practical.
- [ ] Keep normal active runtime files under 500 lines when practical.
- [ ] Split files only when it improves clarity and does not break behavior.
- [ ] Avoid files that mix UI, storage, notification, tray, battery, and reminder logic together.
- [ ] Ensure each core responsibility has one clear owner module.
- [ ] Do not create duplicate engines, duplicate timers, duplicate storage managers, or duplicate notification controllers.

---

# Phase 0 — Safe Project Inspection

## 0.1 Open and understand project files

- [ ] Open `task_edit.md`.
  - Goal: Understand the correction plan.
  - Affected files: `task_edit.md`.
  - Expected result: Main risks and required sections are understood before editing.
  - Verification: No code edited before reading this file.
  - Risk note: Skipping this causes blind rebuilding.

- [ ] Open `README.md` if present.
  - Goal: Understand intended app identity.
  - Affected files: `README.md`.
  - Expected result: UI and feature intent are known.
  - Verification: Note whether README describes transparent clock/date/battery UI.
  - Risk note: Do not overwrite README intent with a generic dashboard.

- [ ] Open `Task.md` if present.
  - Goal: Compare claimed completed tasks with actual implementation.
  - Affected files: `Task.md`.
  - Expected result: Identify features marked complete but not actually working.
  - Verification: Create notes inside this task file if needed.
  - Risk note: A checked task is not proof of working code.

- [ ] Open `CORE.md`, `STATE.md`, and `AGENTS.md` if present.
  - Goal: Understand project workflow rules.
  - Affected files: `CORE.md`, `STATE.md`, `AGENTS.md`.
  - Expected result: Existing project conventions are respected.
  - Verification: No conflicting workflow changes introduced.
  - Risk note: These may contain important project memory.

- [ ] Open `PilSaatTarihV2TopluAciklamali.py` as UI/reference material only.
  - Goal: Preserve previous stable UI behavior.
  - Affected files: `PilSaatTarihV2TopluAciklamali.py`.
  - Expected result: Previous visual/taskbar/free-layout behavior is understood.
  - Verification: Do not delete or rewrite this file.
  - Risk note: This file may be legacy but is important reference.

## 0.2 Create baseline diagnostics

- [ ] Run a file tree listing.
  - Goal: See all files and folders.
  - Affected files: none.
  - Expected result: Generated/cache/build/legacy areas are known.
  - Verification: Save mental or temporary notes; do not create permanent noise files.
  - Risk note: Hidden generated files may pollute release ZIPs.

- [ ] Run Python compile check.
  - Goal: Identify syntax errors.
  - Affected files: all `.py` files.
  - Expected result: Exact failing files and line numbers are known.
  - Verification: Run `python -m compileall .`.
  - Risk note: Do not fix by deleting feature files blindly.

- [ ] Run import smoke checks for key modules.
  - Goal: Detect broken imports.
  - Affected files: `DeskPilot.py`, `core_window.py`, `pil_servisi.py`, `core_settings.py`.
  - Expected result: Broken imports are listed.
  - Verification: Use simple `python -c "import module_name"` commands where safe.
  - Risk note: GUI import may require environment; document failures clearly.

- [ ] Run line count check.
  - Goal: Detect oversized active files.
  - Affected files: all `.py` files.
  - Expected result: Files over 500 lines are listed.
  - Verification: Use `wc -l *.py` or equivalent.
  - Risk note: Do not split reference files unnecessarily.

---

# Phase 1 — Compile and Import Repair

## 1.1 Repair `core_window.py` syntax structure

- [ ] Inspect top 120 lines of `core_window.py`.
  - Goal: Locate misplaced indented method fragments.
  - Affected files: `core_window.py`.
  - Expected result: Exact invalid indentation area is known.
  - Verification: Confirm the class begins cleanly after imports.
  - Risk note: Do not remove behavior before comparing with reference.

- [ ] Move valid misplaced methods into the correct class or remove safe duplicates.
  - Goal: Make `core_window.py` syntactically valid.
  - Affected files: `core_window.py`.
  - Expected result: No top-level indented methods appear before a class.
  - Verification: `python -m py_compile core_window.py`.
  - Risk note: Preserve topmost/taskbar behavior.

- [ ] Remove duplicate imports inside `core_window.py`.
  - Goal: Keep imports clear and non-conflicting.
  - Affected files: `core_window.py`.
  - Expected result: Each dependency is imported once unless justified.
  - Verification: Manual inspection and compile check.
  - Risk note: Do not remove needed fallback imports.

- [ ] Confirm `DraggableTransparentWindow` is defined once.
  - Goal: Avoid duplicate main window classes.
  - Affected files: `core_window.py`.
  - Expected result: One canonical main window class.
  - Verification: Search class definitions.
  - Risk note: Duplicate classes cause UI behavior drift.

## 1.2 Repair broken module imports

- [ ] Search for `app.` imports.
  - Goal: Find imports pointing to a non-existing package.
  - Affected files: all `.py` files.
  - Expected result: All `app.*` imports are identified.
  - Verification: Search text for `from app` and `import app`.
  - Risk note: Do not create a new package unless necessary.

- [ ] Fix `pil_servisi.py` import path.
  - Goal: Use the local `pil_modeli.py` file.
  - Affected files: `pil_servisi.py`.
  - Expected result: `PilDurumu` imports from `pil_modeli` or a confirmed canonical package path.
  - Verification: `python -c "from pil_servisi import PilServisi"`.
  - Risk note: Simple local import is preferred.

- [ ] Search for missing names used in `core_window.py`.
  - Goal: Detect undefined functions/classes.
  - Affected files: `core_window.py`.
  - Expected result: Undefined names such as logging/topmost helpers are resolved.
  - Verification: Import/compile plus static inspection.
  - Risk note: Do not stub silently if real implementation exists elsewhere.

- [ ] Fix logging imports or function names.
  - Goal: Ensure `log_altyapisini_kur`, `log_kaydet`, or equivalent names exist and are imported correctly.
  - Affected files: `core_window.py`, `log_servisi.py`.
  - Expected result: Logging calls use one consistent API.
  - Verification: Import main modules and trigger one log call.
  - Risk note: Avoid two logging systems.

## 1.3 Repair dependency file

- [ ] Open `requirements.txt`.
  - Goal: Detect corrupted dependency lines.
  - Affected files: `requirements.txt`.
  - Expected result: Each dependency is on its own valid line.
  - Verification: Manual inspection.
  - Risk note: Invalid requirements break setup.

- [ ] Fix invalid `pytest-mocktests` or attached dependency text.
  - Goal: Make requirements installable.
  - Affected files: `requirements.txt`.
  - Expected result: Only valid needed packages remain.
  - Verification: `pip install -r requirements.txt` in a safe environment if possible.
  - Risk note: Do not add heavy dependencies without need.

- [ ] Keep PySide/PyQt fallback dependency logic clear.
  - Goal: Avoid conflicting GUI framework setup.
  - Affected files: `requirements.txt`, GUI imports.
  - Expected result: Primary framework is clear; fallback does not break app.
  - Verification: Run import smoke tests.
  - Risk note: Mixing PySide6 and PyQt6 carelessly can break runtime.

---

# Phase 2 — UI Identity Restoration and Protection

## 2.1 Establish UI reference

- [ ] Compare current main window with `PilSaatTarihV2TopluAciklamali.py`.
  - Goal: Identify visual drift.
  - Affected files: `core_window.py`, `PilSaatTarihV2TopluAciklamali.py`.
  - Expected result: List exact UI differences.
  - Verification: Visual/manual comparison after app can launch.
  - Risk note: This is a critical blocker.

- [ ] Confirm intended main UI is not a dashboard.
  - Goal: Prevent wrong product direction.
  - Affected files: `core_window.py`, `gorev_arayuzu.py`, `hatirlatici_listesi.py`.
  - Expected result: First visible app surface remains clock/date/battery.
  - Verification: Launch app and inspect first screen.
  - Risk note: Todo/reminder UI must stay secondary.

- [ ] Confirm transparent frameless window behavior.
  - Goal: Preserve DigitalSaat identity.
  - Affected files: `core_window.py`.
  - Expected result: Main window is transparent, frameless, draggable, compact.
  - Verification: Manual launch test.
  - Risk note: Do not replace with normal bordered window.

- [ ] Confirm intended fonts load correctly.
  - Goal: Preserve produced visual identity.
  - Affected files: `core_window.py`, `assets/fonts/Technology.ttf`, `assets/fonts/Technology-Bold.ttf`.
  - Expected result: Technology font or intended configured font is used.
  - Verification: Launch app and inspect typography.
  - Risk note: Avoid generic fallback unless font missing.

## 2.2 Main clock UI tasks

- [ ] Verify battery/time/date order.
  - Goal: Keep visual hierarchy.
  - Affected files: `core_window.py`.
  - Expected result: Order matches intended produced UI.
  - Verification: Manual screenshot check.
  - Risk note: Do not reorder based on generic assumptions.

- [ ] Verify time update loop.
  - Goal: Ensure clock updates without duplicate timers.
  - Affected files: `core_window.py`.
  - Expected result: One clear timer updates time/date/battery UI.
  - Verification: Search timers; observe app for 60 seconds.
  - Risk note: Duplicate timers create CPU/load bugs.

- [ ] Verify seconds visibility and size scaling.
  - Goal: Settings must affect visible UI correctly.
  - Affected files: `core_window.py`, `core_settings.py`, `ui_settings.py`.
  - Expected result: Seconds can be shown/hidden and scaled correctly.
  - Verification: Change setting, Apply, Save, restart.
  - Risk note: Do not break base time layout.

- [ ] Verify date format behavior.
  - Goal: Date display follows settings.
  - Affected files: `core_window.py`, `core_settings.py`.
  - Expected result: Selected/custom date format renders correctly.
  - Verification: Change date format, Apply, Save, restart.
  - Risk note: Locale fallback must not crash.

## 2.3 Free-layout/taskbar UI tasks

- [ ] Verify free-layout mode can be enabled.
  - Goal: Separate battery/time/date windows work.
  - Affected files: `core_window.py`, `serbest_pencere.py`, `pencere_araclari.py`.
  - Expected result: Separate windows appear correctly.
  - Verification: Enable free-layout from settings/menu.
  - Risk note: Do not lose main grouped mode.

- [ ] Verify each free window is draggable.
  - Goal: User can reposition each module.
  - Affected files: `serbest_pencere.py`.
  - Expected result: Battery/time/date windows move independently.
  - Verification: Manual drag test.
  - Risk note: Mouse event handlers must not conflict.

- [ ] Verify free windows stay topmost when intended.
  - Goal: Preserve desktop overlay behavior.
  - Affected files: `serbest_pencere.py`, `pencere_araclari.py`.
  - Expected result: Windows remain visible above normal windows if configured.
  - Verification: Open another app and test overlap.
  - Risk note: Topmost enforcement must not create timer conflict.

- [ ] Verify taskbar placement behavior.
  - Goal: App must not incorrectly jump behind or away from taskbar.
  - Affected files: `serbest_pencere.py`, `pencere_araclari.py`, `core_window.py`.
  - Expected result: User-placed free windows can remain near/over taskbar as intended.
  - Verification: Manual Windows taskbar test.
  - Risk note: Do not clamp everything to availableGeometry.

- [ ] Verify positions are saved and restored.
  - Goal: Free-layout placements persist.
  - Affected files: `core_settings.py`, `serbest_pencere.py`, `digitalSaat.settings.json`.
  - Expected result: Restart restores last positions.
  - Verification: Move windows, save, restart.
  - Risk note: Invalid old positions should recover safely.

## 2.4 Settings UI tasks

- [ ] Verify settings dialog tabs.
  - Goal: Preserve intended settings structure.
  - Affected files: `ui_settings.py`, `ui_ayarlar_formlar.py`.
  - Expected result: General, Battery, Time, Date tabs exist.
  - Verification: Open settings and inspect tabs.
  - Risk note: Do not remove controls to simplify.

- [ ] Verify Apply button behavior.
  - Goal: Preview changes without closing settings.
  - Affected files: `ui_settings.py`, `core_window.py`.
  - Expected result: Apply updates visible UI immediately.
  - Verification: Change color/size, click Apply.
  - Risk note: Apply must not permanently save unless intended.

- [ ] Verify Save button behavior.
  - Goal: Persist settings.
  - Affected files: `ui_settings.py`, `core_settings.py`.
  - Expected result: Save writes settings and restart restores them.
  - Verification: Save, close, restart app.
  - Risk note: Avoid partial setting writes.

- [ ] Verify Cancel behavior.
  - Goal: Discard unsaved changes.
  - Affected files: `ui_settings.py`.
  - Expected result: Cancel restores previous settings.
  - Verification: Change settings, cancel, inspect UI.
  - Risk note: Preview state must be rolled back.

- [ ] Verify UI styling consistency of settings.
  - Goal: Settings must look aligned with DigitalSaat style.
  - Affected files: `ui_settings.py`, `ui_ayarlar_formlar.py`.
  - Expected result: Clean, modern, lightweight, not generic/conflicting.
  - Verification: Manual visual inspection.
  - Risk note: Avoid heavy effects or overdesigned panels.

## 2.5 Reminder/todo UI tasks

- [ ] Verify reminder list UI is secondary.
  - Goal: Reminder UI must not replace main clock.
  - Affected files: `hatirlatici_listesi.py`, `core_window.py`, `sistem_tepsisi.py`.
  - Expected result: Reminder list opens from menu/tray/settings action.
  - Verification: Launch app; first view remains clock.
  - Risk note: Avoid dashboard conversion.

- [ ] Verify reminder popup visual style.
  - Goal: Popup should be clean and aligned with app identity.
  - Affected files: `hatirlatici_popup.py`.
  - Expected result: Popup is readable, lightweight, not visually random.
  - Verification: Trigger test reminder.
  - Risk note: Do not make popup intrusive beyond intended behavior.

- [ ] Verify todo UI is secondary.
  - Goal: Todo list must not dominate main app.
  - Affected files: `gorev_arayuzu.py`, `core_window.py`, `sistem_tepsisi.py`.
  - Expected result: Todo UI opens on demand.
  - Verification: Open todo list from menu/tray.
  - Risk note: Keep DigitalSaat primary.

---

# Phase 3 — Architecture and Ownership Cleanup

## 3.1 Define module ownership

- [ ] Assign main window ownership.
  - Goal: `core_window.py` owns only main window coordination.
  - Affected files: `core_window.py`.
  - Expected result: Main window does not contain full storage/tray/reminder engines if avoidable.
  - Verification: Inspect responsibilities.
  - Risk note: Do not over-split during urgent repair.

- [ ] Assign settings ownership.
  - Goal: `core_settings.py` owns settings model/load/save.
  - Affected files: `core_settings.py`, `ui_settings.py`.
  - Expected result: UI does not directly parse/write raw JSON unless delegated.
  - Verification: Search JSON access.
  - Risk note: Duplicate setting writes cause data loss.

- [ ] Assign battery ownership.
  - Goal: `pil_servisi.py` owns battery reading/interpretation.
  - Affected files: `pil_servisi.py`, `pil_modeli.py`.
  - Expected result: UI receives clean battery state.
  - Verification: Mock or smoke test battery service.
  - Risk note: Desktop no-battery case must be safe.

- [ ] Assign notification ownership.
  - Goal: `bildirim_servisi.py` owns notification cooldown and dispatch decision.
  - Affected files: `bildirim_servisi.py`, `core_window.py`, `hatirlatici_popup.py`.
  - Expected result: No duplicate cooldown logic in UI files.
  - Verification: Search cooldown code.
  - Risk note: Multiple cooldown engines cause missed/spam alerts.

- [ ] Assign reminder ownership.
  - Goal: `hatirlatici_servisi.py` owns reminder storage and due logic.
  - Affected files: `hatirlatici_servisi.py`, `hatirlatici_modeli.py`.
  - Expected result: UI calls service methods, not raw list manipulation.
  - Verification: Search reminder JSON/list handling.
  - Risk note: UI-based state can lose data.

- [ ] Assign todo ownership.
  - Goal: `gorev_servisi.py` owns todo storage and sorting.
  - Affected files: `gorev_servisi.py`, `gorev_modeli.py`, `gorev_arayuzu.py`.
  - Expected result: UI delegates add/complete/delete to service.
  - Verification: Search direct data manipulation in UI.
  - Risk note: Duplicate todo state creates inconsistency.

- [ ] Assign tray ownership.
  - Goal: `sistem_tepsisi.py` owns tray icon and menu creation.
  - Affected files: `sistem_tepsisi.py`, `core_window.py`, `DeskPilot.py`.
  - Expected result: Main window initializes tray once and retains reference.
  - Verification: Manual tray test.
  - Risk note: Lost object reference can hide tray icon.

## 3.2 Remove duplication safely

- [ ] Search duplicate reminder check methods.
  - Goal: Avoid multiple schedulers.
  - Affected files: all `.py` files.
  - Expected result: One active due-check loop.
  - Verification: Search `hatirlaticilari_kontrol_et` and similar names.
  - Risk note: Duplicate loops show repeated popups.

- [ ] Search duplicate notification cooldown logic.
  - Goal: Keep cooldown centralized.
  - Affected files: all `.py` files.
  - Expected result: Cooldown lives in one service.
  - Verification: Search `cooldown`, `son_bildirim`, `last_notification`.
  - Risk note: Multiple cooldown stores conflict.

- [ ] Search duplicate tray initialization.
  - Goal: Create tray once.
  - Affected files: `sistem_tepsisi.py`, `core_window.py`, `DeskPilot.py`.
  - Expected result: Only one tray object created.
  - Verification: Manual tray launch and search code.
  - Risk note: Duplicate tray menus confuse user.

- [ ] Search duplicate free-window handling.
  - Goal: Keep one clear free-layout controller.
  - Affected files: `core_window.py`, `serbest_pencere.py`, `pencere_navigasyon.py`.
  - Expected result: Free windows created/hidden/saved from one flow.
  - Verification: Enable/disable free mode repeatedly.
  - Risk note: Duplicate windows can appear.

- [ ] Search duplicate raw JSON functions.
  - Goal: Prevent inconsistent storage.
  - Affected files: all `.py` files.
  - Expected result: Shared safe storage behavior or one service per domain.
  - Verification: Search `json.load`, `json.dump`, `.json`.
  - Risk note: Unsafe writes can corrupt data.

---

# Phase 4 — Storage and Data Reliability

## 4.1 Settings storage

- [ ] Verify settings file path.
  - Goal: Use predictable settings location.
  - Affected files: `core_settings.py`, `digitalSaat.settings.json`.
  - Expected result: App can find settings consistently.
  - Verification: Rename settings temporarily and launch app.
  - Risk note: Do not destroy user settings.

- [ ] Add missing default settings creation if absent.
  - Goal: App starts cleanly without settings file.
  - Affected files: `core_settings.py`.
  - Expected result: Missing settings file creates defaults safely.
  - Verification: Move settings file aside, run app.
  - Risk note: Backup old settings before tests.

- [ ] Add corrupted settings recovery.
  - Goal: App does not crash on invalid JSON.
  - Affected files: `core_settings.py`.
  - Expected result: Corrupted file is backed up and defaults are used.
  - Verification: Put invalid JSON in copy and run app.
  - Risk note: Never silently delete corrupted data.

- [ ] Validate settings values.
  - Goal: Prevent invalid colors/sizes/positions from breaking UI.
  - Affected files: `core_settings.py`.
  - Expected result: Invalid values fall back safely.
  - Verification: Manually inject invalid values.
  - Risk note: Overstrict validation may discard valid custom settings.

## 4.2 Reminder storage

- [ ] Verify reminder data filename and path.
  - Goal: Store reminders consistently.
  - Affected files: `hatirlatici_servisi.py`.
  - Expected result: One canonical reminder JSON file.
  - Verification: Create reminder and inspect file.
  - Risk note: Avoid multiple reminder files.

- [ ] Create reminder file if missing.
  - Goal: First run works.
  - Affected files: `hatirlatici_servisi.py`.
  - Expected result: Empty list/default structure created safely.
  - Verification: Delete/move file and launch app.
  - Risk note: Do not overwrite existing data.

- [ ] Add corrupted reminder file recovery.
  - Goal: Invalid JSON does not crash app.
  - Affected files: `hatirlatici_servisi.py`.
  - Expected result: Corrupt file is backed up and empty/default data used.
  - Verification: Test with invalid JSON.
  - Risk note: Preserve corrupt file for possible manual recovery.

- [ ] Use atomic write for reminders.
  - Goal: Avoid partial/corrupt writes.
  - Affected files: `hatirlatici_servisi.py`.
  - Expected result: Write temp file then replace.
  - Verification: Inspect implementation and run save test.
  - Risk note: Windows file locking must be handled safely.

## 4.3 Todo storage

- [ ] Verify todo data filename and path.
  - Goal: Store tasks consistently.
  - Affected files: `gorev_servisi.py`.
  - Expected result: One canonical todo JSON file.
  - Verification: Add task and inspect file.
  - Risk note: Avoid duplicate todo data files.

- [ ] Create todo file if missing.
  - Goal: First run works.
  - Affected files: `gorev_servisi.py`.
  - Expected result: Empty list/default structure created safely.
  - Verification: Delete/move file and launch app.
  - Risk note: Do not overwrite existing data.

- [ ] Add corrupted todo file recovery.
  - Goal: Invalid JSON does not crash app.
  - Affected files: `gorev_servisi.py`.
  - Expected result: Corrupt file is backed up and empty/default data used.
  - Verification: Test with invalid JSON.
  - Risk note: Preserve corrupt file.

- [ ] Use atomic write for todos.
  - Goal: Avoid partial/corrupt writes.
  - Affected files: `gorev_servisi.py`.
  - Expected result: Write temp file then replace.
  - Verification: Inspect implementation and run save test.
  - Risk note: Keep code simple.

## 4.4 Shared backup/logging behavior

- [ ] Verify logs folder creation.
  - Goal: Logging works on clean project.
  - Affected files: `log_servisi.py`.
  - Expected result: `logs/` created automatically if needed.
  - Verification: Launch app and inspect log file.
  - Risk note: Logs should not be required for app startup.

- [ ] Ensure log file path is safe.
  - Goal: Avoid writing into protected locations unexpectedly.
  - Affected files: `log_servisi.py`.
  - Expected result: Log path is project-local or user-data-local as intended.
  - Verification: Manual inspection and run.
  - Risk note: Packaged EXE path may be read-only.

- [ ] Add `.gitignore` entries for logs/backups/cache.
  - Goal: Keep repo clean.
  - Affected files: `.gitignore`.
  - Expected result: Generated files are ignored.
  - Verification: `git status` after running app.
  - Risk note: Do not ignore source assets.

---

# Phase 5 — Feature Completion Micro Tasks

## 5.1 Clock and date

- [ ] Verify current time display at startup.
  - Goal: App shows correct time immediately.
  - Affected files: `core_window.py`.
  - Expected result: No blank/stale time at launch.
  - Verification: Launch app.
  - Risk note: Timer must update quickly.

- [ ] Verify date display at startup.
  - Goal: App shows correct date immediately.
  - Affected files: `core_window.py`.
  - Expected result: Date appears with configured format.
  - Verification: Launch app.
  - Risk note: Locale must be safe.

- [ ] Verify date changes after midnight logic if testable.
  - Goal: Date updates without restart.
  - Affected files: `core_window.py`.
  - Expected result: Date refreshes on timer.
  - Verification: Unit/mock or manual time simulation if possible.
  - Risk note: Avoid system clock manipulation unless safe.

## 5.2 Battery

- [ ] Verify no-battery environment behavior.
  - Goal: Desktop PCs do not crash.
  - Affected files: `pil_servisi.py`, `core_window.py`.
  - Expected result: Safe placeholder or hidden battery state.
  - Verification: Mock `psutil.sensors_battery()` returning `None`.
  - Risk note: Common on desktop computers.

- [ ] Verify battery percentage display.
  - Goal: Show accurate percentage when available.
  - Affected files: `pil_servisi.py`, `core_window.py`.
  - Expected result: Percent matches service result.
  - Verification: Mock battery percent values.
  - Risk note: Avoid direct psutil calls in UI.

- [ ] Verify charging icon/label.
  - Goal: Show charging state correctly.
  - Affected files: `pil_servisi.py`, `core_window.py`.
  - Expected result: Plugged/unplugged states are reflected.
  - Verification: Mock plugged true/false.
  - Risk note: Do not confuse full battery with plugged state.

- [ ] Verify low battery threshold.
  - Goal: Low warning triggers at configured value.
  - Affected files: `core_settings.py`, `pil_servisi.py`, `bildirim_servisi.py`.
  - Expected result: Warning only when threshold condition met.
  - Verification: Mock 19%, 20%, 21% with threshold 20.
  - Risk note: Cooldown should prevent spam.

- [ ] Verify full battery threshold.
  - Goal: Full/charged warning triggers correctly.
  - Affected files: `core_settings.py`, `pil_servisi.py`, `bildirim_servisi.py`.
  - Expected result: Full warning respects setting.
  - Verification: Mock 100% plugged state.
  - Risk note: Avoid repeated warnings every second.

## 5.3 Notifications and cooldown

- [ ] Verify notification service exists and is used.
  - Goal: Centralize notification decisions.
  - Affected files: `bildirim_servisi.py`, `core_window.py`.
  - Expected result: UI calls notification service, not duplicate cooldown code.
  - Verification: Search calls.
  - Risk note: Duplicate service causes conflicts.

- [ ] Verify same notification cooldown.
  - Goal: Prevent repeated same alert spam.
  - Affected files: `bildirim_servisi.py`.
  - Expected result: Same key is blocked during cooldown.
  - Verification: Unit test or small script.
  - Risk note: Too long cooldown may hide important reminders.

- [ ] Verify different notifications are independent.
  - Goal: Low battery and reminder alerts do not block each other incorrectly.
  - Affected files: `bildirim_servisi.py`.
  - Expected result: Different notification keys behave independently.
  - Verification: Unit test two keys.
  - Risk note: Global cooldown can suppress valid alerts.

- [ ] Verify silent mode behavior.
  - Goal: Silent mode disables sound/TTS but not visual alert.
  - Affected files: `core_settings.py`, `bildirim_servisi.py`, popup modules.
  - Expected result: Visual popup still works; audio is muted.
  - Verification: Manual or mocked alert test.
  - Risk note: Do not suppress critical visual warnings.

## 5.4 Reminders

- [ ] Verify reminder model fields.
  - Goal: Reminder data is complete.
  - Affected files: `hatirlatici_modeli.py`.
  - Expected result: id, title, description, due time, status, repeat/snooze fields if intended.
  - Verification: Inspect model and serialization.
  - Risk note: Avoid breaking old reminder data.

- [ ] Verify create reminder flow.
  - Goal: User can create a reminder.
  - Affected files: `hatirlatici_listesi.py`, `hatirlatici_servisi.py`.
  - Expected result: New reminder appears in list and data file.
  - Verification: Manual UI test.
  - Risk note: If creation UI missing, add small dialog or action.

- [ ] Verify edit reminder flow if present.
  - Goal: Existing reminder can be updated safely.
  - Affected files: `hatirlatici_listesi.py`, `hatirlatici_servisi.py`.
  - Expected result: Changes persist.
  - Verification: Edit and restart.
  - Risk note: Do not duplicate reminder id.

- [ ] Verify delete reminder flow.
  - Goal: User can remove reminders.
  - Affected files: `hatirlatici_listesi.py`, `hatirlatici_servisi.py`.
  - Expected result: Deleted reminder removed from UI and JSON.
  - Verification: Delete and restart.
  - Risk note: Confirm destructive action if UI supports it.

- [ ] Verify due reminder detection.
  - Goal: Reminder fires when due.
  - Affected files: `hatirlatici_servisi.py`, `core_window.py`.
  - Expected result: Due reminder creates popup/notification.
  - Verification: Create reminder due in one minute.
  - Risk note: Avoid blocking UI loop.

- [ ] Verify complete action.
  - Goal: User can mark reminder complete.
  - Affected files: `hatirlatici_popup.py`, `hatirlatici_servisi.py`.
  - Expected result: Completed reminder does not fire again unless repeating.
  - Verification: Trigger and click complete.
  - Risk note: Repeating reminders need special handling.

- [ ] Verify snooze action.
  - Goal: User can postpone reminder.
  - Affected files: `hatirlatici_popup.py`, `hatirlatici_servisi.py`.
  - Expected result: Snoozed reminder fires later.
  - Verification: Snooze 5 minutes or shorter test mode.
  - Risk note: Avoid duplicate popups during snooze.

- [ ] Verify missed reminder recovery after restart.
  - Goal: App handles reminders due while closed.
  - Affected files: `hatirlatici_servisi.py`, `core_window.py`.
  - Expected result: Missed due reminders are shown or handled according to spec.
  - Verification: Create past-due reminder, launch app.
  - Risk note: Do not spam many old reminders without control.

## 5.5 Todos/tasks

- [ ] Verify todo model fields.
  - Goal: Task data is complete.
  - Affected files: `gorev_modeli.py`.
  - Expected result: id, title, description optional, priority, completed, timestamps.
  - Verification: Inspect model and serialization.
  - Risk note: Avoid breaking old todo data.

- [ ] Verify add todo flow.
  - Goal: User can add task.
  - Affected files: `gorev_arayuzu.py`, `gorev_servisi.py`.
  - Expected result: Task appears and persists.
  - Verification: Add task, inspect JSON, restart.
  - Risk note: UI must stay secondary.

- [ ] Verify complete todo flow.
  - Goal: User can mark task done.
  - Affected files: `gorev_arayuzu.py`, `gorev_servisi.py`.
  - Expected result: Completed state persists.
  - Verification: Complete task, restart.
  - Risk note: Sorting should still be sensible.

- [ ] Verify delete todo flow.
  - Goal: User can delete task.
  - Affected files: `gorev_arayuzu.py`, `gorev_servisi.py`.
  - Expected result: Deleted task does not reappear.
  - Verification: Delete and restart.
  - Risk note: Confirm destructive action if appropriate.

- [ ] Verify priority sorting.
  - Goal: Important tasks appear first if intended.
  - Affected files: `gorev_servisi.py`, `gorev_arayuzu.py`.
  - Expected result: High priority incomplete tasks are visually prioritized.
  - Verification: Add low/medium/high tasks.
  - Risk note: Do not hide completed tasks unless intended.

## 5.6 Tray

- [ ] Verify tray icon file.
  - Goal: Tray has a valid icon.
  - Affected files: `sistem_tepsisi.py`, `assets/icon.ico`, `deskpilot.ico`.
  - Expected result: One canonical icon path works.
  - Verification: Launch app and inspect tray.
  - Risk note: Packaged path may differ from source path.

- [ ] Verify tray object lifetime.
  - Goal: Tray icon does not disappear.
  - Affected files: `core_window.py`, `DeskPilot.py`, `sistem_tepsisi.py`.
  - Expected result: Tray manager is stored on a live object.
  - Verification: Launch and wait 2 minutes.
  - Risk note: Garbage collection can remove tray icon.

- [ ] Verify tray Show/Hide action.
  - Goal: User can show/hide app from tray.
  - Affected files: `sistem_tepsisi.py`, `core_window.py`.
  - Expected result: Action works in grouped and free-layout modes.
  - Verification: Manual tray test.
  - Risk note: Do not close app when hiding.

- [ ] Verify tray Settings action.
  - Goal: Settings opens from tray.
  - Affected files: `sistem_tepsisi.py`, `ui_settings.py`.
  - Expected result: Settings dialog appears.
  - Verification: Click menu item.
  - Risk note: Avoid multiple duplicate settings dialogs.

- [ ] Verify tray Reminder actions.
  - Goal: Reminder list/new reminder accessible.
  - Affected files: `sistem_tepsisi.py`, `hatirlatici_listesi.py`.
  - Expected result: Reminder UI opens from tray.
  - Verification: Click menu item.
  - Risk note: Keep menu concise.

- [ ] Verify tray Todo actions.
  - Goal: Todo list/new todo accessible.
  - Affected files: `sistem_tepsisi.py`, `gorev_arayuzu.py`.
  - Expected result: Todo UI opens from tray.
  - Verification: Click menu item.
  - Risk note: Keep main UI clean.

- [ ] Verify tray Quit action.
  - Goal: App exits cleanly.
  - Affected files: `sistem_tepsisi.py`, `DeskPilot.py`.
  - Expected result: Timers stop; app closes; no orphan process.
  - Verification: Quit from tray and inspect process list if needed.
  - Risk note: Hide and quit must not be confused.

## 5.7 Startup behavior

- [ ] Verify startup setting UI.
  - Goal: User can toggle launch at startup.
  - Affected files: `ui_settings.py`, `core_settings.py`.
  - Expected result: Setting visible and saved.
  - Verification: Toggle, save, restart app.
  - Risk note: UI setting must match actual registry state if possible.

- [ ] Verify registry helper.
  - Goal: Windows startup entry works.
  - Affected files: `utils.py`.
  - Expected result: Enable/disable startup writes/removes correct Run key.
  - Verification: Manual registry check.
  - Risk note: Do not require admin unless necessary.

- [ ] Verify startup failure logging.
  - Goal: User can diagnose failure.
  - Affected files: `utils.py`, `log_servisi.py`.
  - Expected result: Failures are logged and do not crash app.
  - Verification: Mock failure or inspect exception handling.
  - Risk note: Registry operations can fail on restricted systems.

---

# Phase 6 — Tests and Verification

## 6.1 Automated test baseline

- [ ] List existing tests.
  - Goal: Know current coverage.
  - Affected files: `test_*.py`, `tests/` if present.
  - Expected result: All test files are known.
  - Verification: File listing.
  - Risk note: Existing tests may be stale.

- [ ] Run existing tests.
  - Goal: See actual status.
  - Affected files: test files.
  - Expected result: Pass/fail list is known.
  - Verification: Run `pytest` if available.
  - Risk note: GUI tests may need special handling.

- [ ] Fix tests broken by import path only.
  - Goal: Make tests runnable after code path repair.
  - Affected files: test files.
  - Expected result: Tests import current modules.
  - Verification: Run `pytest`.
  - Risk note: Do not rewrite tests to hide real failures.

## 6.2 Add targeted tests

- [ ] Add battery service tests.
  - Goal: Validate battery states.
  - Affected files: `test_battery_service.py` or existing test file.
  - Expected result: Tests cover no battery, low, normal, full, plugged.
  - Verification: Run targeted pytest.
  - Risk note: Mock psutil, do not require real laptop battery.

- [ ] Add notification cooldown tests.
  - Goal: Prevent alert spam.
  - Affected files: `test_notification_service.py`.
  - Expected result: Same key cooldown and different key independence covered.
  - Verification: Run targeted pytest.
  - Risk note: Time-dependent tests should be stable.

- [ ] Add settings storage tests.
  - Goal: Verify defaults, save/load, corrupted recovery.
  - Affected files: `test_settings_storage.py`.
  - Expected result: Missing/corrupt settings handled safely.
  - Verification: Run targeted pytest with temp directory.
  - Risk note: Do not modify real user settings in tests.

- [ ] Add reminder service tests.
  - Goal: Verify create/save/load/due/snooze/complete.
  - Affected files: `test_reminder_service.py`.
  - Expected result: Core reminder logic covered without GUI.
  - Verification: Run targeted pytest.
  - Risk note: Use temp JSON files.

- [ ] Add todo service tests.
  - Goal: Verify add/complete/delete/sort/persist.
  - Affected files: `test_todo_service.py`.
  - Expected result: Core todo logic covered without GUI.
  - Verification: Run targeted pytest.
  - Risk note: Use temp JSON files.

## 6.3 Manual checklist

- [ ] Update or create manual verification checklist.
  - Goal: Cover UI and Windows-only behavior.
  - Affected files: `manuel_dogrulama.md` or `tests/manual_checklist.md`.
  - Expected result: Manual checklist exists and is detailed.
  - Verification: Open checklist and confirm sections.
  - Risk note: Automated tests cannot fully verify taskbar/tray UI.

- [ ] Add main UI checklist items.
  - Goal: Prevent UI drift.
  - Affected files: manual checklist file.
  - Expected result: Transparent frameless grouped UI, fonts, spacing, colors included.
  - Verification: Manual checklist review.
  - Risk note: This is critical for DigitalSaat.

- [ ] Add free-layout checklist items.
  - Goal: Verify taskbar behavior.
  - Affected files: manual checklist file.
  - Expected result: Drag, topmost, taskbar placement, save/restore included.
  - Verification: Manual checklist review.
  - Risk note: Must test on Windows.

- [ ] Add tray checklist items.
  - Goal: Verify tray lifecycle.
  - Affected files: manual checklist file.
  - Expected result: Show/hide/settings/reminder/todo/quit included.
  - Verification: Manual checklist review.
  - Risk note: Tray can behave differently in packaged EXE.

- [ ] Add storage checklist items.
  - Goal: Verify persistence manually.
  - Affected files: manual checklist file.
  - Expected result: Settings/reminders/todos persist after restart.
  - Verification: Manual checklist review.
  - Risk note: Avoid deleting real user data.

---

# Phase 7 — Cleanup and Release Hygiene

## 7.1 Identify generated files

- [ ] List `__pycache__` folders.
  - Goal: Exclude generated cache.
  - Affected files: `__pycache__/`, nested cache folders.
  - Expected result: Caches identified.
  - Verification: File tree search.
  - Risk note: Do not include caches in source ZIP.

- [ ] List `.pyc` files.
  - Goal: Exclude compiled Python artifacts.
  - Affected files: `*.pyc`.
  - Expected result: All `.pyc` files identified.
  - Verification: File search.
  - Risk note: Delete only after confirmation or as cleanup task.

- [ ] List build/dist folders.
  - Goal: Exclude build outputs.
  - Affected files: `build/`, `dist/`, generated EXEs if present.
  - Expected result: Build outputs identified.
  - Verification: File tree search.
  - Risk note: Do not delete release artifacts without confirmation.

- [ ] List old ZIP files.
  - Goal: Exclude old snapshots.
  - Affected files: `*.zip`.
  - Expected result: Old archives identified.
  - Verification: File search.
  - Risk note: Do not delete automatically.

## 7.2 `.gitignore` cleanup

- [ ] Ensure `.gitignore` includes Python cache rules.
  - Goal: Keep repo clean.
  - Affected files: `.gitignore`.
  - Expected result: `__pycache__/`, `*.pyc` ignored.
  - Verification: `git status` after running app/tests.
  - Risk note: Do not ignore source files.

- [ ] Ensure `.gitignore` includes build artifacts.
  - Goal: Avoid committing generated EXE/build folders.
  - Affected files: `.gitignore`.
  - Expected result: `build/`, `dist/`, relevant generated outputs ignored.
  - Verification: `git status`.
  - Risk note: Keep `.spec` files if canonical.

- [ ] Ensure `.gitignore` includes logs/backups where appropriate.
  - Goal: Avoid committing runtime data.
  - Affected files: `.gitignore`.
  - Expected result: `logs/`, backup JSON files ignored unless intentionally tracked.
  - Verification: `git status` after corrupt recovery test.
  - Risk note: Do not ignore default example config if needed.

## 7.3 Legacy files

- [ ] Mark `PilSaatTarihV2TopluAciklamali.py` as reference.
  - Goal: Prevent accidental deletion.
  - Affected files: documentation or task file.
  - Expected result: File clearly treated as UI reference, not active rewrite target.
  - Verification: Manual inspection.
  - Risk note: It may contain the original correct UI behavior.

- [ ] Identify canonical `.spec` file.
  - Goal: Avoid build confusion.
  - Affected files: `*.spec`.
  - Expected result: One build spec is marked canonical; others are legacy candidates.
  - Verification: Manual review.
  - Risk note: Do not delete old specs without confirmation.

- [ ] Identify old docs/reference docs.
  - Goal: Separate runtime from documentation.
  - Affected files: `DigitalSaatV2_Envanter.txt`, `DigitalSaatV2_Fonksiyon_Aciklama.txt`, `ozet_kaldigimizYer.txt`.
  - Expected result: Docs are preserved but not treated as runtime code.
  - Verification: Manual inspection.
  - Risk note: These may contain project decisions.

---

# Phase 8 — Final Full Verification

## 8.1 Compile and tests

- [ ] Run full compile check.
  - Goal: No syntax errors remain.
  - Affected files: all `.py` files.
  - Expected result: `python -m compileall .` passes.
  - Verification: Command output.
  - Risk note: Include all project files, not only edited files.

- [ ] Run full test suite.
  - Goal: Automated tests pass.
  - Affected files: tests.
  - Expected result: `pytest` passes or failures are documented with reason.
  - Verification: Command output.
  - Risk note: Do not ignore failing tests silently.

- [ ] Run app startup test.
  - Goal: App launches.
  - Affected files: runtime app.
  - Expected result: Main DigitalSaat UI appears.
  - Verification: `python DeskPilot.py` manual launch.
  - Risk note: Test on Windows/PySide6 environment when possible.

## 8.2 UI acceptance

- [ ] Confirm main UI matches intended DigitalSaat design.
  - Goal: Block generic UI drift.
  - Affected files: UI files.
  - Expected result: Transparent compact clock/date/battery UI is primary.
  - Verification: Manual visual check.
  - Risk note: This is mandatory.

- [ ] Confirm free-layout behavior works.
  - Goal: Separate windows are usable.
  - Affected files: free-layout modules.
  - Expected result: Drag/topmost/taskbar/save/restore works.
  - Verification: Manual Windows test.
  - Risk note: Critical behavior.

- [ ] Confirm settings behavior works.
  - Goal: Apply/Save/Cancel and restart persistence work.
  - Affected files: settings modules.
  - Expected result: Settings are reliable.
  - Verification: Manual checklist.
  - Risk note: Settings bugs damage user trust.

## 8.3 Feature acceptance

- [ ] Confirm tray behavior works.
  - Goal: Tray icon and menu are reliable.
  - Affected files: tray modules.
  - Expected result: Show/hide/settings/reminder/todo/quit work.
  - Verification: Manual tray test.
  - Risk note: Tray must keep live reference.

- [ ] Confirm reminders work.
  - Goal: Reminder lifecycle is complete.
  - Affected files: reminder modules.
  - Expected result: Create/due/popup/complete/snooze/persist work.
  - Verification: Manual and automated tests.
  - Risk note: Avoid duplicate alerts.

- [ ] Confirm todos work.
  - Goal: Todo lifecycle is complete.
  - Affected files: todo modules.
  - Expected result: Add/complete/delete/sort/persist work.
  - Verification: Manual and automated tests.
  - Risk note: Todo UI must not dominate main UI.

- [ ] Confirm battery behavior works.
  - Goal: Battery display and warnings are reliable.
  - Affected files: battery modules.
  - Expected result: No battery/low/full/plugged states handled.
  - Verification: Mock tests and manual laptop test if available.
  - Risk note: Desktop no-battery case is important.

- [ ] Confirm notification cooldown works.
  - Goal: No notification spam.
  - Affected files: notification modules.
  - Expected result: Cooldown prevents repeated same alerts.
  - Verification: Test repeated triggers.
  - Risk note: Do not suppress unrelated alerts.

- [ ] Confirm silent mode works.
  - Goal: Visual alerts without sound/TTS.
  - Affected files: settings/notification modules.
  - Expected result: Silent mode behaves consistently.
  - Verification: Manual or mock alert test.
  - Risk note: Visual warnings should remain.

## 8.4 Cleanup acceptance

- [ ] Confirm generated files are excluded.
  - Goal: Clean repo/release package.
  - Affected files: `.gitignore`, generated folders.
  - Expected result: Cache/build/log files are not included accidentally.
  - Verification: `git status` and file tree review.
  - Risk note: Do not delete user data automatically.

- [ ] Confirm no active runtime file is excessively large without reason.
  - Goal: Maintainability.
  - Affected files: all active `.py` files.
  - Expected result: Files over 500 lines are split or justified.
  - Verification: Line count check.
  - Risk note: Reference legacy file may remain large.

- [ ] Confirm `task_edit.md` and this file reflect completed work.
  - Goal: Progress traceability.
  - Affected files: `task_edit.md`, `tasks_micro.md`.
  - Expected result: Completed tasks are checked.
  - Verification: Manual review.
  - Risk note: Do not mark incomplete tasks complete.

---

# Final Done Condition

The project is considered complete only when all applicable items below are true:

- [ ] App compiles successfully.
- [ ] App launches successfully.
- [ ] Main UI matches the intended DigitalSaat design.
- [ ] UI is not replaced by a generic dashboard.
- [ ] Free-layout/taskbar behavior works.
- [ ] Settings Apply/Save/Cancel work.
- [ ] Settings persist after restart.
- [ ] Battery display and warnings work.
- [ ] Date/time behavior works.
- [ ] Tray icon and menu work.
- [ ] Reminder creation, due popup, complete, snooze, and persistence work.
- [ ] Todo add, complete, delete, sort, and persistence work.
- [ ] Notification cooldown works.
- [ ] Silent mode works.
- [ ] JSON files are safely created, read, written, backed up, and recovered.
- [ ] Logs are created safely.
- [ ] Tests pass or any remaining failures are explicitly documented.
- [ ] Manual verification checklist exists and is usable.
- [ ] Generated/cache/build files are excluded from clean source package.
- [ ] No active runtime file is oversized without reason.
- [ ] No duplicate engines/timers/managers remain.
- [ ] No suspicious legacy/reference file is deleted without confirmation.

When finished, write exactly:

`Bitti.`

Then provide a short summary of changed files and tests run.
