# task_edit.md

## 0. Project Inspection Summary

- Current project purpose:
  - DigitalSaatV2 is a Windows desktop floating digital clock application built with PySide6/PyQt6 fallback.
  - The original stable identity is a transparent, frameless, draggable desktop panel that shows battery, time, and date.
  - It also supports a free-layout mode where battery, time, and date can be separated into independent draggable line windows.
  - Newer planned V1.1 areas include reminders, todo/tasks, notifications, silent mode, cooldown, tray, multi-monitor behavior, storage reliability, logging, and verification.

- Current UI direction detected:
  - README and inventory describe the intended UI as the previously produced compact transparent clock/date/battery display, not a generic productivity dashboard.
  - The intended settings UI is tabbed: General, Battery, Time, Date, with live preview via Apply and persistence via Save.
  - Free-layout windows must preserve the previous produced design: frameless, transparent, draggable, visually aligned with the main clock/date/battery typography and spacing.
  - New reminder/todo UI must not visually replace or dominate the clock UI. These should be secondary dialogs or tray/menu actions unless the existing spec explicitly says otherwise.

- Main modules detected:
  - Entry point: `DeskPilot.py`
  - Main window and free-layout logic: `core_window.py`, `serbest_pencere.py`, `pencere_araclari.py`, `pencere_guncelleme.py`, `pencere_navigasyon.py`
  - Settings: `core_settings.py`, `ui_settings.py`, `ui_ayarlar_formlar.py`, `digitalSaat.settings.json`
  - Battery: `pil_modeli.py`, `pil_servisi.py`
  - Notification/logging: `bildirim_servisi.py`, `log_servisi.py`
  - Reminder: `hatirlatici_modeli.py`, `hatirlatici_servisi.py`, `hatirlatici_popup.py`, `hatirlatici_listesi.py`
  - Todo/tasks: `gorev_modeli.py`, `gorev_servisi.py`, `gorev_arayuzu.py`
  - Tray: `sistem_tepsisi.py`
  - Tests/checklists: `test_faz1_faz2_faz3.py`, `test_faz4_hatirlatici.py`, `test_faz5_gorev.py`, `test_hatirlatici_mantigi.py`, `manuel_dogrulama.md`
  - Legacy/reference files: `PilSaatTarihV2TopluAciklamali.py`, several `.spec` files, `DigitalSaatV2_Envanter.txt`, `DigitalSaatV2_Fonksiyon_Aciklama.txt`, `ozet_kaldigimizYer.txt`, `Besmele/` operational documents.

- Existing strengths:
  - The project still contains the previous stable UI reference in `PilSaatTarihV2TopluAciklamali.py`; this file appears to preserve important behavior, especially taskbar/free-layout handling.
  - There is a clear original minimal entry point in `DeskPilot.py`.
  - Settings have a dataclass model in `core_settings.py`.
  - Reminder, todo, battery, notification, tray, and test files exist as separate modules, which is a useful direction.
  - `Task.md` contains a broad feature roadmap and acceptance expectations.
  - `README.md` still describes the intended visual identity and core behavior.

- Critical risks:
  - The app currently does not compile: `core_window.py` has an `IndentationError` near line 24. There are method fragments at top level before the `DraggableTransparentWindow` class.
  - `core_window.py` imports duplicated reminder modules and uses functions such as `log_altyapisini_kur`, `log_kaydet`, and `_enforce_topmost` without valid visible imports/definitions in the inspected top section.
  - `pil_servisi.py` imports `PilDurumu` from `app.models.pil_modeli`, but there is no `app/` package in the project. The actual local file is `pil_modeli.py`.
  - `requirements.txt` appears corrupted because `pytest-mocktests` is attached incorrectly or is likely not a valid intended dependency line.
  - The current modularization appears partially generated and inconsistent with the previous stable UI implementation.
  - UI risk is severe: the current added dialogs for todo/reminder/settings look generic and may not match the previous intended/produced DigitalSaat visual identity.
  - Tray support exists in `sistem_tepsisi.py`, but it is not clearly initialized from `DeskPilot.py` or `core_window.py`.
  - Several files appear duplicated or overlapping: `core_window.py` vs `pencere_guncelleme.py` vs `pencere_navigasyon.py`; `serbest_pencere.py` vs fragments inside `core_window.py`; `test_faz4_hatirlatici.py` vs `test_hatirlatici_mantigi.py`.
  - Existing tests cannot be trusted until import/compile errors are fixed.
  - `Task.md` marks several phases as complete, but the implementation does not currently satisfy that claim.

- Files that appear legacy or suspicious:
  - `PilSaatTarihV2TopluAciklamali.py`: likely legacy/reference, but very important because it may preserve the real intended UI and taskbar behavior.
  - `PilSaatTarihV2TopluAciklamali.spec`, `DigitalSaatV.040226.H2.spec`, `DigitalSaat_V030226.help.spec`, `DigitalSaatV2.spec`, `DeskPilot.spec`: multiple build specs require review; only one should be canonical.
  - `DigitalSaatV2_Envanter.txt`, `DigitalSaatV2_Fonksiyon_Aciklama.txt`, `ozet_kaldigimizYer.txt`: useful reference docs, not runtime files.
  - `__pycache__/` folders and `.pyc` files: generated artifacts and should not be included in clean source ZIPs.
  - `Besmele/tools/__pycache__/`: generated artifacts.
  - `core_window.py`: suspicious because it contains misplaced method fragments and duplicated imports.
  - `pencere_guncelleme.py` and `pencere_navigasyon.py`: may be intended mixins, but currently not clearly connected.
  - `ui_ayarlar_formlar.py`: partially extracted settings UI; must be checked for missing methods and visual mismatch.

- Files that must not be deleted without confirmation:
  - `PilSaatTarihV2TopluAciklamali.py` because it may be the best available reference for the previous produced UI and taskbar behavior.
  - `digitalSaat.settings.json` because it may contain user/default visual settings.
  - `assets/fonts/Technology.ttf` and `assets/fonts/Technology-Bold.ttf` because they may be part of the intended clock identity.
  - `assets/icon.ico` and `deskpilot.ico` until the canonical icon is confirmed.
  - `Besmele/`, `CORE.md`, `STATE.md`, `AGENTS.md` because they appear to be operational workflow files.
  - `README.md`, `Task.md`, `manuel_dogrulama.md`, `DigitalSaatV2_Envanter.txt`, `DigitalSaatV2_Fonksiyon_Aciklama.txt` because they contain project/spec history.

## 1. Architecture Correction Tasks

- [ ] Task A1 — Restore a compilable application baseline
  - Goal: Make the project importable and runnable without changing the intended UI identity.
  - Affected files: `core_window.py`, `DeskPilot.py`, `pil_servisi.py`, `requirements.txt`.
  - Exact expected result: `python -m compileall .` completes without syntax/import path failures caused by project code structure.
  - Verification method: Run `python -m compileall .`; then run `python DeskPilot.py` in a Windows/PySide6 environment and confirm the main clock window opens.
  - Risk note: Do not fix this by replacing the UI with a generic window. Use the previous stable UI as the baseline.

- [ ] Task A2 — Repair `core_window.py` structure before feature work
  - Goal: Remove misplaced top-level method fragments and place each method inside the correct class or delete only if duplicated safely.
  - Affected files: `core_window.py`, `serbest_pencere.py`, `pencere_araclari.py`.
  - Exact expected result: `core_window.py` starts with imports, then class/function definitions only; no indented methods exist before a class definition.
  - Verification method: `python -m py_compile core_window.py`; inspect that free-line behavior still has one canonical implementation.
  - Risk note: Topmost/taskbar behavior is sensitive; compare with `PilSaatTarihV2TopluAciklamali.py` before removing anything.

- [ ] Task A3 — Fix broken local imports
  - Goal: Ensure all modules import from actual project paths.
  - Affected files: `pil_servisi.py`, any file importing non-existing `app.*` paths.
  - Exact expected result: `pil_servisi.py` imports `PilDurumu` from local `pil_modeli.py`, or a real package structure is created consistently.
  - Verification method: Run `python -c "from pil_servisi import PilServisi; from pil_modeli import PilDurumu"`.
  - Risk note: Prefer the simple local import unless a full `app/` package migration is explicitly planned.

- [ ] Task A4 — Define one canonical main-window architecture
  - Goal: Decide whether `core_window.py` contains all main-window behavior or whether behavior is split into mixins/helpers.
  - Affected files: `core_window.py`, `pencere_guncelleme.py`, `pencere_navigasyon.py`, `pencere_araclari.py`, `serbest_pencere.py`.
  - Exact expected result: No duplicated reminder update methods, menu methods, or free-window methods exist in multiple active files without a clear relationship.
  - Verification method: Search for duplicate method names: `hatirlaticilari_kontrol_et`, `show_menu`, `_hatirlatici_tamamla`, `_hatirlatici_ertele`, `_show_free_windows`, `_hide_free_windows`.
  - Risk note: Do not split aggressively. The immediate goal is clarity and stability, not a large rewrite.

- [ ] Task A5 — Keep files within reasonable responsibility and size
  - Goal: Reduce oversized files only where it improves safety and maintainability.
  - Affected files: `core_window.py` currently about 1000+ lines, `ui_settings.py` about 400+ lines, `PilSaatTarihV2TopluAciklamali.py` about 2000+ lines.
  - Exact expected result: Active files should generally stay under 500 lines when practical; any exception must be justified in a comment or documentation.
  - Verification method: Run line count check with `wc -l *.py`; confirm active runtime modules are not monolithic without reason.
  - Risk note: `PilSaatTarihV2TopluAciklamali.py` may remain as a reference/legacy file; do not refactor it blindly.

- [ ] Task A6 — Correct `requirements.txt`
  - Goal: Make dependency installation reliable.
  - Affected files: `requirements.txt`.
  - Exact expected result: Each dependency appears on its own line; invalid merged text is removed or corrected.
  - Verification method: Run `pip install -r requirements.txt` in a clean virtual environment.
  - Risk note: Do not add heavy dependencies unless the current implementation actually uses them.

- [ ] Task A7 — Establish canonical build spec
  - Goal: Identify one PyInstaller spec for current release/build flow.
  - Affected files: `DeskPilot.spec`, `DigitalSaatV2.spec`, `DigitalSaatV.040226.H2.spec`, `DigitalSaat_V030226.help.spec`, `PilSaatTarihV2TopluAciklamali.spec`, `scripts/release.ps1`, `.gitignore`.
  - Exact expected result: One active spec is documented; older specs are marked legacy/reference or moved to a docs/archive location after confirmation.
  - Verification method: Run the release script in dry/manual review mode and confirm it references the canonical spec only.
  - Risk note: Do not delete old specs until the previous release path is confirmed.

## 2. UI Consistency Tasks

- [ ] Task U1 — Treat UI mismatch as a blocking issue
  - Goal: Confirm whether the current UI matches the previously intended/produced DigitalSaat design.
  - Affected files: `core_window.py`, `serbest_pencere.py`, `ui_settings.py`, `ui_ayarlar_formlar.py`, `gorev_arayuzu.py`, `hatirlatici_listesi.py`, `hatirlatici_popup.py`, `README.md`, `PilSaatTarihV2TopluAciklamali.py`.
  - Exact expected result: A short UI comparison note is added inside this task file or a separate documented checklist showing: intended UI, current UI, mismatch, required correction.
  - Verification method: Run the current app after compile fixes and visually compare the main window, free-layout windows, settings dialog, reminder popup, and todo dialog against the previous UI reference.
  - Risk note: This project must not become a generic todo/reminder dashboard. The clock/date/battery visual identity is primary.

- [ ] Task U2 — Restore the original clock/date/battery visual hierarchy
  - Goal: Ensure the main display remains the compact transparent DigitalSaat panel.
  - Affected files: `core_window.py`, `core_settings.py`, `digitalSaat.settings.json`, `assets/fonts/Technology.ttf`, `assets/fonts/Technology-Bold.ttf`.
  - Exact expected result: Battery, time, and date order, alignment, spacing, opacity, colors, font handling, and seconds scaling match the intended previous design unless explicitly changed by settings.
  - Verification method: Manual screenshot comparison against the previous produced UI or `PilSaatTarihV2TopluAciklamali.py` behavior.
  - Risk note: Do not default to Segoe UI if the intended produced design used Technology fonts or another specific visual identity.

- [ ] Task U3 — Preserve free-layout/taskbar visual behavior
  - Goal: Keep the previously important behavior where free-layout windows can be moved over the Windows taskbar area when intended.
  - Affected files: `serbest_pencere.py`, `pencere_araclari.py`, `core_window.py`, `PilSaatTarihV2TopluAciklamali.py`.
  - Exact expected result: Free time/date/battery windows remain frameless, transparent, draggable, topmost when required, and can stay above the taskbar band only when user places them there.
  - Verification method: Manual Windows test: enable free-layout, drag each module near/over taskbar, release, confirm it remains visible and does not jump unexpectedly.
  - Risk note: This is one of the most important UI behaviors. Do not “fix” it by clamping every window to availableGeometry only.

- [ ] Task U4 — Prevent reminder/todo UI from replacing the clock UI
  - Goal: Keep reminder and todo features as secondary surfaces.
  - Affected files: `gorev_arayuzu.py`, `hatirlatici_listesi.py`, `hatirlatici_popup.py`, `sistem_tepsisi.py`, `core_window.py`.
  - Exact expected result: Reminder/todo dialogs open from right-click/tray/settings actions and do not appear as permanent large modules in the main clock panel unless explicitly enabled and visually designed.
  - Verification method: Launch app and confirm the first visible UI remains DigitalSaat, not a generic productivity panel.
  - Risk note: The wording “module visibility” must not be interpreted as redesigning the main display into a dashboard.

- [ ] Task U5 — Align settings UI with the existing design language
  - Goal: Ensure the settings dialog remains functional and recognizable from the previous produced settings UI.
  - Affected files: `ui_settings.py`, `ui_ayarlar_formlar.py`, `core_settings.py`.
  - Exact expected result: Tabs remain General/Pil/Saat/Tarih; controls do not lose existing settings; Apply previews changes; Save persists; Cancel restores original values.
  - Verification method: Change font, color, size, spacing, opacity, free-layout, and startup settings; test Apply, Save, Cancel separately.
  - Risk note: Do not remove existing controls just to simplify the dialog.

- [ ] Task U6 — Create a UI regression checklist
  - Goal: Add explicit manual UI checks so future AI changes do not drift from the intended design.
  - Affected files: `manuel_dogrulama.md` or `tests/manual_checklist.md` if created.
  - Exact expected result: Checklist includes main grouped mode, free-layout mode, taskbar placement, settings tabs, color picker, font picker, opacity, spacing, tray menu, reminder popup, todo dialog.
  - Verification method: Manual checklist can be completed line by line after each major UI change.
  - Risk note: This is required because the current UI appears detached from the intended produced design.

## 3. Feature Completion Tasks

- [ ] Task F1 — Reconfirm clock/date feature behavior
  - Goal: Ensure time and date update correctly and match formatting settings.
  - Affected files: `core_window.py`, `core_settings.py`, `ui_settings.py`, `digitalSaat.settings.json`.
  - Exact expected result: Time updates smoothly; seconds visibility and scale work; date format supports the intended short custom format and/or strftime behavior.
  - Verification method: Toggle seconds visibility; change date format; confirm live preview and saved restart behavior.
  - Risk note: Locale handling may fail on some Windows machines if `tr_TR` is unavailable; handle safely.

- [ ] Task F2 — Reconfirm battery feature behavior
  - Goal: Make battery reading, threshold state, charging icon, low/full warnings, and hidden battery behavior reliable.
  - Affected files: `pil_modeli.py`, `pil_servisi.py`, `core_window.py`, `core_settings.py`, `ui_settings.py`.
  - Exact expected result: Battery percent displays; charging status and icon display correctly; low/critical/full alert settings work; hiding battery also hides charging icon.
  - Verification method: Mock `psutil.sensors_battery()` in automated tests and perform one manual laptop battery test if available.
  - Risk note: Desktop PCs may not have battery data; app must not crash or show broken text.

- [ ] Task F3 — Complete notification service integration
  - Goal: Use one notification service for battery, reminder, plug/unplug, and future alerts.
  - Affected files: `bildirim_servisi.py`, `core_window.py`, `hatirlatici_popup.py`, `sistem_tepsisi.py`.
  - Exact expected result: Notification cooldown works centrally; tray notifications are used when tray exists; visual popup remains available.
  - Verification method: Trigger repeated same alert and confirm it does not spam; trigger different alert and confirm it can show.
  - Risk note: Notification service currently only tracks cooldown; it does not yet clearly show tray/system notifications.

- [ ] Task F4 — Complete silent mode behavior
  - Goal: Make silent mode consistently disable sound/TTS while allowing visual notifications.
  - Affected files: `core_settings.py`, `ui_ayarlar_formlar.py`, `core_window.py`, `bildirim_servisi.py`.
  - Exact expected result: When `sessiz_mod` is true, no battery/reminder sound plays; visual warning/popup can still appear.
  - Verification method: Enable silent mode, trigger a low battery/reminder alert, confirm no sound; disable silent mode and confirm sound path still works.
  - Risk note: Do not silence visual warnings unless explicitly intended.

- [ ] Task F5 — Complete reminder model and scheduler behavior
  - Goal: Ensure reminders can be created, stored, detected, completed, snoozed, repeated, and recovered after restart.
  - Affected files: `hatirlatici_modeli.py`, `hatirlatici_servisi.py`, `hatirlatici_popup.py`, `hatirlatici_listesi.py`, `core_window.py`.
  - Exact expected result: Reminder fields include id, title, description, due time, repeat type, status, snooze, created timestamp; due detection does not block UI.
  - Verification method: Add a reminder due in one minute; confirm popup; test Complete, Snooze 5/10/60 minutes, restart with missed reminder.
  - Risk note: Current list UI appears read-only or incomplete for creating/editing reminders; verify actual user flow.

- [ ] Task F6 — Complete todo/task behavior
  - Goal: Ensure todo creation, completion, deletion, priority sorting, and persistence are reliable.
  - Affected files: `gorev_modeli.py`, `gorev_servisi.py`, `gorev_arayuzu.py`, `core_window.py`, `sistem_tepsisi.py`.
  - Exact expected result: User can add, mark done, delete, and view sorted tasks; undone high priority items appear first; data persists after restart.
  - Verification method: Add three tasks with different priorities, complete one, restart app, confirm order and state.
  - Risk note: Todo UI style must remain secondary and not override the main DigitalSaat design.

- [ ] Task F7 — Complete system tray integration
  - Goal: Ensure tray icon is created, shown, and connected to app lifecycle.
  - Affected files: `sistem_tepsisi.py`, `core_window.py`, `DeskPilot.py`.
  - Exact expected result: Tray menu includes Show/Hide, New Reminder/List, New Todo/List, Settings, Quit; tooltip shows battery and next reminder if available.
  - Verification method: Launch app and confirm tray icon exists; use each menu action; close/hide/show behavior works in grouped and free-layout modes.
  - Risk note: Tray object must be retained by a live reference or it may disappear due to garbage collection.

- [ ] Task F8 — Complete startup behavior safely
  - Goal: Make Windows autostart reliable and non-destructive.
  - Affected files: `utils.py`, `ui_settings.py`, `core_settings.py`.
  - Exact expected result: Autostart setting writes/removes registry entry correctly; failure shows a readable warning and logs the error.
  - Verification method: Toggle setting on/off; verify registry Run key or use existing helper; restart test if possible.
  - Risk note: Do not request admin unless truly necessary.

- [ ] Task F9 — Complete multi-monitor behavior
  - Goal: Restore grouped and free windows to correct monitors and recover safely if monitor layout changes.
  - Affected files: `core_settings.py`, `pencere_araclari.py`, `core_window.py`, `serbest_pencere.py`.
  - Exact expected result: Screen name/geometry is saved per module; missing monitor moves window to visible area; collect-to-current-monitor action exists if specified.
  - Verification method: Manual two-monitor test; then disconnect second monitor and restart.
  - Risk note: Do not break taskbar placement while adding monitor safety.

- [ ] Task F10 — Complete settings lock behavior
  - Goal: Ensure `settings_locked` actually prevents movement/settings changes where intended.
  - Affected files: `core_settings.py`, `core_window.py`, `serbest_pencere.py`, `ui_settings.py`.
  - Exact expected result: When locked, user cannot accidentally drag or alter layout; unlock path remains available.
  - Verification method: Enable lock, try dragging grouped/free windows and opening settings; confirm intended behavior.
  - Risk note: Do not create a lockout where user cannot restore settings.

## 4. Storage and Data Reliability Tasks

- [ ] Task S1 — Define canonical data directory and filenames
  - Goal: Ensure settings, reminders, todos, logs, and backups are stored consistently.
  - Affected files: `utils.py`, `core_settings.py`, `hatirlatici_servisi.py`, `gorev_servisi.py`, `log_servisi.py`.
  - Exact expected result: All runtime data goes under one app data directory; no service writes unexpectedly into the source root.
  - Verification method: Run app and inspect generated files; confirm expected paths.
  - Risk note: Existing user settings must be migrated or read safely.

- [ ] Task S2 — Standardize JSON safe read/write helper
  - Goal: Avoid duplicating unsafe or inconsistent JSON storage logic.
  - Affected files: `core_settings.py`, `hatirlatici_servisi.py`, `gorev_servisi.py`, new helper module only if necessary.
  - Exact expected result: Atomic writes use temp file + replace; read validates type and schema; broken files are backed up before fallback.
  - Verification method: Corrupt each JSON file manually and confirm app starts with defaults and creates `.broken` or timestamped backup.
  - Risk note: Do not overwrite broken user data without backup.

- [ ] Task S3 — Validate settings types, not only keys
  - Goal: Prevent invalid values from entering `PanelSettings`.
  - Affected files: `core_settings.py`, `test_faz1_faz2_faz3.py`.
  - Exact expected result: Wrong types such as `seffaflik: "hatali_tip"` fall back to defaults or are converted safely.
  - Verification method: Automated test with invalid type values; confirm no crash and expected defaults.
  - Risk note: Current tests expect fallback, but current implementation appears to pass invalid types into dataclass.

- [ ] Task S4 — Standardize reminder/todo filenames or document Turkish names
  - Goal: Resolve mismatch between roadmap names (`reminders.json`, `todos.json`) and implementation names (`hatirlaticilar.json`, likely Turkish task file names).
  - Affected files: `Task.md`, `hatirlatici_servisi.py`, `gorev_servisi.py`, docs/checklists.
  - Exact expected result: Either English filenames from spec are used, or Turkish filenames are explicitly documented as canonical.
  - Verification method: Add reminder and todo; confirm files are created exactly where expected.
  - Risk note: Renaming may require migration from existing files.

- [ ] Task S5 — Add backup/recovery verification for all JSON data
  - Goal: Ensure corrupted settings/reminders/todos can be recovered safely.
  - Affected files: `core_settings.py`, `hatirlatici_servisi.py`, `gorev_servisi.py`, tests.
  - Exact expected result: Each data service backs up corrupted JSON and continues with defaults/valid entries.
  - Verification method: Create corrupted JSON for each file and run tests.
  - Risk note: Partial valid data should be preserved when possible.

- [ ] Task S6 — Fix logging path consistency
  - Goal: Ensure logs go to app data logs directory unless source-root logs are intentionally required.
  - Affected files: `log_servisi.py`, `utils.py`, `core_window.py`, `DeskPilot.py`.
  - Exact expected result: `logs/app.log` location is documented; release/runtime behavior does not write unexpectedly into protected or temporary directories.
  - Verification method: Launch app and confirm log file creation in expected path.
  - Risk note: Packaged EXE path handling must be tested.

## 5. Test and Verification Tasks

- [ ] Task T1 — Add compile/import smoke test
  - Goal: Catch syntax and import path failures early.
  - Affected files: tests, optionally `pytest.ini`.
  - Exact expected result: Test suite fails if any active runtime module cannot compile/import.
  - Verification method: Run `python -m compileall .` and `pytest`.
  - Risk note: Exclude legacy/reference files only if documented.

- [ ] Task T2 — Repair existing tests so they reflect real behavior
  - Goal: Make tests trustworthy.
  - Affected files: `test_faz1_faz2_faz3.py`, `test_faz4_hatirlatici.py`, `test_hatirlatici_mantigi.py`, `test_faz5_gorev.py`.
  - Exact expected result: Tests pass in a clean environment and do not depend on broken imports or invalid assumptions.
  - Verification method: Run `pytest -q`.
  - Risk note: Do not mark broken features as complete by weakening tests.

- [ ] Task T3 — Add UI manual verification checklist
  - Goal: Protect the intended UI identity from future drift.
  - Affected files: `manuel_dogrulama.md` or `tests/manual_checklist.md`.
  - Exact expected result: Checklist covers grouped UI, free-layout UI, taskbar placement, settings tabs, tray, reminder popup, todo dialog.
  - Verification method: Manual completion before release.
  - Risk note: Screenshots may be added later, but do not include generated screenshots in source ZIP unless needed.

- [ ] Task T4 — Add battery mocked tests
  - Goal: Verify battery behavior without requiring a laptop.
  - Affected files: `test_faz1_faz2_faz3.py`, `pil_servisi.py`.
  - Exact expected result: Tests cover no battery, normal, low, critical, plugged, unplugged, and unsupported health info.
  - Verification method: Mock `psutil.sensors_battery()`.
  - Risk note: Avoid tests that fail on desktops because no battery exists.

- [ ] Task T5 — Add reminder persistence and missed-reminder tests
  - Goal: Verify reminder reliability across restarts.
  - Affected files: `test_faz4_hatirlatici.py`, `hatirlatici_servisi.py`, `hatirlatici_modeli.py`.
  - Exact expected result: Tests cover due, missed, snoozed, completed, daily recurring, weekly recurring, corrupted JSON.
  - Verification method: Use `tmp_path` and controlled datetimes.
  - Risk note: Avoid real timers in unit tests.

- [ ] Task T6 — Add todo persistence/sorting tests
  - Goal: Verify todo data survives reload and sorts correctly.
  - Affected files: `test_faz5_gorev.py`, `gorev_servisi.py`, `gorev_modeli.py`.
  - Exact expected result: Tests cover add, complete, delete, priority sort, corrupted JSON fallback.
  - Verification method: Use `tmp_path` and reload service from disk.
  - Risk note: UI tests are optional; service tests are required.

- [ ] Task T7 — Add tray behavior manual test
  - Goal: Verify tray behavior in real Windows environment.
  - Affected files: `manuel_dogrulama.md`, `sistem_tepsisi.py`.
  - Exact expected result: Manual checklist confirms tray icon appears, tooltip updates, menu actions work, quit exits.
  - Verification method: Windows manual test.
  - Risk note: Tray behavior may differ in VM or restricted environments.

- [ ] Task T8 — Add release ZIP hygiene test
  - Goal: Prevent generated artifacts from entering clean ZIP snapshots.
  - Affected files: `.gitignore`, release script, manual checklist.
  - Exact expected result: ZIP excludes `__pycache__`, `.pyc`, build outputs, old exe artifacts, temporary files, and old ZIPs.
  - Verification method: Create release ZIP and inspect file list.
  - Risk note: Do not exclude required assets/fonts/icons.

## 6. Cleanup Tasks

- [ ] Task C1 — Remove generated Python cache files from source control/ZIP output
  - Goal: Keep source snapshots clean.
  - Affected files/folders: `__pycache__/`, `Besmele/tools/__pycache__/`, `*.pyc`, `.gitignore`, release script.
  - Exact expected result: Generated caches are excluded from future ZIPs and are not tracked.
  - Verification method: Run `find . -name __pycache__ -o -name "*.pyc"` before release; expected none in release ZIP.
  - Risk note: Do not delete from working tree automatically in this task plan; confirm first or clean during release packaging.

- [ ] Task C2 — Classify legacy/reference files
  - Goal: Prevent accidental deletion of important historical UI reference files.
  - Affected files: `PilSaatTarihV2TopluAciklamali.py`, old `.spec` files, inventory/function docs, `ozet_kaldigimizYer.txt`.
  - Exact expected result: Each file is marked as active, reference, legacy, or removable candidate in a cleanup note.
  - Verification method: Manual review and confirmation before moving/deleting.
  - Risk note: `PilSaatTarihV2TopluAciklamali.py` must be treated as a UI/behavior reference until the active modular app is proven equivalent.

- [ ] Task C3 — Normalize build artifacts and release folders
  - Goal: Keep source separate from generated exe/build outputs.
  - Affected files/folders: `.gitignore`, `scripts/release.ps1`, any `build/`, `dist/`, `dagitim/`, `*.exe`, `*.zip` if present.
  - Exact expected result: Build outputs are excluded from clean source ZIP unless explicitly required by release policy.
  - Verification method: Create ZIP and inspect size/file list.
  - Risk note: `STATE.md` mentions `dagitim/`; confirm whether binaries are intentionally versioned before changing policy.

- [ ] Task C4 — Resolve duplicate tests
  - Goal: Avoid maintaining two copies of the same reminder tests.
  - Affected files: `test_faz4_hatirlatici.py`, `test_hatirlatici_mantigi.py`.
  - Exact expected result: One canonical reminder test file exists, or duplicate files cover clearly different scopes.
  - Verification method: Compare test names and assertions; run `pytest -q`.
  - Risk note: Do not delete coverage; merge if needed.

- [ ] Task C5 — Review `.gitignore` for current project needs
  - Goal: Ensure future commits/ZIPs exclude generated clutter but include required assets.
  - Affected files: `.gitignore`.
  - Exact expected result: Ignore rules include `__pycache__/`, `*.pyc`, `build/`, generic `dist/` unless intentional exception, `*.log`, `.pytest_cache/`, `.mypy_cache/`, old ZIPs/exes if not release-managed.
  - Verification method: Run `git status --ignored` and inspect release ZIP contents.
  - Risk note: Current `.gitignore` has an exception for a specific exe; confirm policy before changing.

- [ ] Task C6 — Remove or document stale TODO/spec conflicts
  - Goal: Prevent old task files from misleading future AI assistants.
  - Affected files: `TODO.md`, `Task.md`, `README.md`, `CORE.md`, `STATE.md`, `Besmele/` docs.
  - Exact expected result: Current implementation plan is clearly `task_edit.md`; older docs are marked as reference or updated to point to the current plan.
  - Verification method: Open README and task docs; confirm no contradiction about completed/incomplete phases.
  - Risk note: Do not rewrite workflow docs unless requested.

## 7. Final Acceptance Checklist

- [ ] UI matches the intended previously produced DigitalSaat design, not a generic dashboard.
- [ ] Main grouped UI shows battery, time, and date with correct typography, spacing, transparency, and visibility settings.
- [ ] Free-layout mode shows separate battery/time/date windows and preserves previous taskbar placement behavior.
- [ ] Core clock and date behavior works after restart.
- [ ] Battery display, charging icon, low/critical/full warning behavior works or fails gracefully on devices without a battery.
- [ ] Tray icon appears, remains alive, and all tray menu actions work.
- [ ] Reminder creation/list/popup/complete/snooze/repeat/missed-after-restart behavior works.
- [ ] Todo add/complete/delete/priority-sort/persistence behavior works.
- [ ] Notification cooldown prevents spam.
- [ ] Silent mode disables sound/TTS but does not hide visual warnings.
- [ ] Settings Apply/Save/Cancel work correctly and settings are restored after restart.
- [ ] Startup/autostart behavior works or reports a clear error.
- [ ] Data persistence uses safe atomic writes and backs up corrupted JSON files before fallback.
- [ ] Logs are created in the documented location and do not spam.
- [ ] Automated tests pass with `pytest -q`.
- [ ] Compile/import check passes with `python -m compileall .`.
- [ ] Manual UI checklist is present and completed before release.
- [ ] No unnecessary generated files are included in the source ZIP.
- [ ] No old ZIPs, EXEs, build outputs, `.pyc`, or `__pycache__` folders are included in the clean project snapshot unless explicitly required.
- [ ] No active runtime file is excessively large without a clear reason.
- [ ] Legacy/reference files are not deleted without explicit confirmation.
