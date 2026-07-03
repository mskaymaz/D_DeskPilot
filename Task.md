# D_DeskPilot Master Task Roadmap

## Rules
- One canonical task source: `Task.md`.
- Turkish-first v1 stabilization comes before full localization.
- Do not split/refactor working files unless required by bug, feature, performance, or size.
- Keep patches small, testable, and committed by feature.

## 0. Project Governance
- [x] Define SPP workflow.
- [x] Use one canonical task file.
- [ ] Keep `Task.md` updated after each completed feature.
- [ ] Keep commits feature-scoped.
- [ ] Add final release notes structure.

## 1. Core App / Startup
- [x] Add `main.py` launcher.
- [x] Keep `DeskPilot.py` as main application entry.
- [x] Basic startup logging exists.
- [ ] Verify startup on clean Windows session.
- [ ] Verify startup with broken/missing settings file.
- [ ] Verify startup with missing optional assets.
- [ ] Add clear user-facing fatal startup message if needed.

## 2. Clock Module
- [x] Clock module exists.
- [x] Embedded digital fonts added.
- [x] DS-Digital set as default clock font.
- [x] System fonts remain selectable for clock.
- [ ] Fix seconds-width horizontal jitter.
- [ ] Verify seconds visibility toggle.
- [ ] Verify clock font scaling.
- [ ] Verify clock behavior in free layout.
- [ ] Verify clock behavior after restart.

## 3. Date Module
- [x] Date module exists.
- [ ] Verify date format setting.
- [ ] Verify date font setting.
- [ ] Verify date visibility toggle.
- [ ] Verify date behavior in free layout.
- [ ] Verify date behavior after restart.

## 4. Battery Module
- [x] Battery module exists.
- [x] Battery thresholds exist.
- [x] Plug/unplug detection exists.
- [ ] Verify low battery warning.
- [ ] Verify critical battery warning.
- [ ] Verify full battery warning setting.
- [ ] Verify silent mode interaction.
- [ ] Verify battery display after restart.

## 5. Reminder Module
- [x] Reminder model/storage exists.
- [x] Reminder popup exists.
- [x] Reminder list UI exists.
- [ ] Verify one-time reminder flow.
- [ ] Verify snooze 5/10/60 minute flow.
- [ ] Verify recurring reminder flow.
- [ ] Verify missed reminder after restart.
- [ ] Polish reminder UI if needed.
- [ ] Route reminder alerts through common notification service.

## 6. Todo Module
- [x] Todo model/storage exists.
- [x] Todo UI exists.
- [x] Dynamic priority foundation exists.
- [x] Task card visual redesign exists.
- [x] New Task dialog exists.
- [x] Shared date/time editor exists.
- [x] Todo i18n pilot wiring exists.
- [ ] Polish Todo workflow in Turkish.
- [ ] Verify add task dialog.
- [ ] Verify edit task dialog.
- [ ] Verify task date/time save/load.
- [ ] Verify overdue state and icon.
- [ ] Verify completed state and icon.
- [ ] Verify cancelled/deleted state and icon.
- [ ] Verify priority sorting.
- [ ] Verify custom priority settings.
- [ ] Verify completed cleanup action.
- [ ] Audit remaining hardcoded Todo UI text.

## 7. Settings
- [x] Settings window exists.
- [x] Language tab exists.
- [x] Clock font selection updated for embedded fonts.
- [x] Task priority settings exists.
- [ ] Review Settings Turkish UX.
- [ ] Add restart notice when language changes.
- [ ] Verify every setting persists.
- [ ] Verify settings restore correctly after restart.
- [ ] Verify settings with missing/old keys.
- [ ] Verify task priority reset-to-default flow.

## 8. Window / Layout / Multi-monitor
- [x] Free layout exists.
- [x] Multi-monitor support exists.
- [x] Topmost behavior extracted/stabilized.
- [x] Popup focus/topmost behavior improved.
- [ ] Verify grouped window startup behavior.
- [ ] Verify free layout startup behavior.
- [ ] Verify move all modules behavior.
- [ ] Verify monitor missing fallback.
- [ ] Verify right mouse + wheel scaling.

## 9. Tray / Menu
- [x] Tray integration exists.
- [ ] Review tray menu items.
- [ ] Add/verify New Reminder action.
- [ ] Add/verify New Todo action.
- [ ] Verify show/hide behavior.
- [ ] Verify quit behavior.
- [ ] Verify tray summary if available.

## 10. Notification System
- [ ] Consolidate notification service behavior.
- [ ] Route battery alerts through common notification service.
- [ ] Route reminder alerts through common notification service.
- [ ] Route Todo alerts through common notification service if needed.
- [ ] Add cooldown rules.
- [ ] Verify silent mode rules.
- [ ] Verify notification behavior after restart.

## 11. i18n / Globalization
- [x] Add `dil_yonetimi.py`.
- [x] Add `translations/tr.json`.
- [x] Add `translations/en.json`.
- [x] Add `translations/ar.json`.
- [x] Add `PanelSettings.language`.
- [x] Add language selector.
- [x] Define Turkish-first v1 / full localization v2 rule.
- [ ] Keep new UI text i18n-compatible where practical.
- [ ] Do not polish English/Arabic in v1.
- [ ] v2: full English pass.
- [ ] v2: full Arabic pass.
- [ ] v2: RTL validation.
- [ ] v2: localization QA.

## 12. Assets / Fonts / Icons
- [x] Add embedded digital fonts.
- [x] Add logo assets.
- [x] Add hourglass icons.
- [x] Update overdue icon asset.
- [ ] Verify asset paths in source mode.
- [ ] Verify asset paths in packaged EXE mode.
- [ ] Remove unused assets if any.

## 13. Testing / Verification
- [ ] Create `tests/manual_checklist.md`.
- [ ] Add Turkish v1 manual checklist.
- [ ] Verify clock/date/battery manually.
- [ ] Verify reminder manually.
- [ ] Verify Todo manually.
- [ ] Verify settings manually.
- [ ] Verify tray manually.
- [ ] Verify startup/restart manually.
- [ ] Verify packaging manually.

## 14. Packaging / Release
- [ ] Define release build command.
- [ ] Verify EXE build.
- [ ] Verify settings path in EXE.
- [ ] Verify assets in EXE.
- [ ] Verify clean install behavior.
- [ ] Prepare v1 Turkish release checklist.
- [ ] Tag release.
- [ ] Push release artifacts if needed.

## 15. Deferred / Do Not Do in v1
- [ ] No SQLite migration.
- [ ] No plugin system.
- [ ] No advanced theme engine.
- [ ] No world clock.
- [ ] No full English/Arabic polishing.
- [ ] No unnecessary file splitting/refactor.
