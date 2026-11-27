# DESKPILOT TASK

## Status Legend
- `[x]` Completed
- `[~]` In progress
- `[ ]` Not started
- `[!]` Blocked / decision required

## Project: D_DeskPilot
## Technology Stack: Flutter/Dart (UI) + Karma Motor Mimarisi
## Platform: Windows (initial), macOS/Linux (future)

---

## Phase 0 — Flutter Project Foundation ✅ COMPLETE

### Tasks
- [x] Clean C++/Qt codebase removed
- [x] Remote URL updated to https://github.com/mskaymaz/D_DeskPilotF
- [x] Flutter project initialized (`flutter create`)
- [x] `pubspec.yaml` configured with `window_manager` and `flutter_lints`
- [x] `window_manager`, `tray_manager`, `drift`, `riverpod` configured
- [x] Minimal `lib/main.dart` running with window_manager
- [x] Windows embedding configured
- [x] Build and run verified (`flutter build windows --debug` → `desk_pilot_f.exe`)
- [x] Git commit and push

### Completion Criteria
- `flutter build windows --debug` produces working `desk_pilot_f.exe`
- `window_manager` works: transparent background, hidden title bar, always-on-top
- Project structure follows clean architecture
- All project files renamed: `desk_pilot_c` → `desk_pilot_f`, `DeskPilotC` → `DeskPilotF`

### Notes
- `flutter run -d windows` has `INSTALL.vcxproj` MSB3073 issue (Permission/CMAKE_INSTALL_PREFIX) — use `flutter build windows --debug` + run `.exe` directly
- D:\Code dışına yazma yasak kesintisiz

---

## Phase 1 — Design System and Desktop Window Foundation ✅ COMPLETE

### Tasks
- [x] Color tokens (light/dark theme) — `lib/core/design_tokens/colors.dart`
- [x] Typography tokens — `lib/core/design_tokens/typography.dart`
- [x] Spacing tokens — `lib/core/design_tokens/spacing.dart`
- [x] Radius tokens — `lib/core/design_tokens/radius.dart`
- [x] Sizing tokens — `lib/core/design_tokens/sizing.dart`
- [x] Z-layer tokens — `lib/core/design_tokens/z_layers.dart`
- [x] Motion/animation tokens — `lib/core/design_tokens/motion.dart`
- [x] Global scale system (75%–150%)
- [x] High-DPI strategy
- [x] Reusable base widgets
- [x] Localization infrastructure (`lib/core/localization/app_localizations.dart`, `l10n/app_tr.arb`, `l10n/app_en.arb`)
- [x] `flutter_localizations` + `intl` + `riverpod` dependencies

### Window Foundation
- [ ] Frameless transparent desktop window ✅ (already working via `window_manager`)
- [x] Always-on-top support
- [ ] Window drag behavior (mouse region)
- [ ] Window position persistence
- [ ] Multi-monitor detection
- [ ] Grouped/free layout foundation
- [ ] Stable focus/show/hide lifecycle

### Completion Criteria
- Design tokens centralized in `lib/core/design_tokens/`
- Localization working with TR/EN
- `flutter build windows --debug` produces working `desk_pilot_f.exe`
- All tokens consumed by widgets (no hardcoded values)

### Notes
- `flutter build windows --debug` fails at `INSTALL.vcxproj` — manually copy `build\flutter_assets\*` to `build\windows\x64\runner\Debug\data\` after build
- D:\Code dışına yazma yasak kesintisiz

---

## Phase 2 — Clock Module ✅ COMPLETE

### Tasks
- [x] Clock domain model (time service, format logic) — `clock_model.dart`, `clock_service.dart`
- [x] 24-hour/12-hour time format
- [x] Optional seconds
- [x] Independent seconds scaling (Timer.periodic)
- [x] Embedded custom font loading (Digital-7, Stencil, Technology, DS-Digital)
- [x] System font support
- [x] Font selection, color, bold
- [x] Clock visibility toggle
- [x] Independent clock scaling
- [x] Stable rendering without jitter
- [x] Grouped and free layout integration
- [x] Persistent clock settings
- [x] IClockService abstract interface + Timer-based implementation
- [x] ClockNotifier (StateNotifier) + Riverpod provider
- [x] ClockWindow UI with live time display
- [x] ProviderScope integration in main.dart

### Completion Criteria
- Clock displays live time in transparent window
- 24h/12h format supported
- Seconds toggle supported
- Font selection supported
- Timer-based updates working
- App builds and runs

### Notes
- `flutter build windows --debug` fails at `INSTALL.vcxproj` — manually copy `build\flutter_assets\*` to `build\windows\x64\runner\Debug\data\` after build
- D:\Code dışına yazma yasak kesintisiz

---

## Phase 3 — Date Module ✅ COMPLETE

### Tasks
- [x] Date domain model — `date_model.dart` (DateSettings, DateState, DateFormatType, DateOrder)
- [x] Date service interface — `date_service.dart` (IDateService)
- [x] Gregorian date support (dotted, slash, ISO formats)
- [x] Hijri date support via `intl` (ar_SA locale)
- [x] Combined Gregorian/Hijri display
- [x] Date order configuration (Gregorian-first/Hijri-first)
- [x] Optional week number support
- [x] Font selection, color, bold
- [x] Independent scaling
- [x] Timer-based updates (1-second interval)
- [x] DateNotifier + StateNotifierProvider
- [x] DateWindow UI
- [x] ProviderScope integration in main.dart

### Completion Criteria
- Date displays Gregorian + Hijri in transparent window
- Turkish locale formatting working
- Timer-based updates working
- App builds and runs

### Notes
- `flutter build windows --debug` fails at `INSTALL.vcxproj` — manually copy `build\flutter_assets\*` to `build\windows\x64\runner\Debug\data\` after build
- D:\Code dışına yazma yasak kesintisiz

### Tasks
- [ ] Date service
- [ ] Gregorian date display
- [ ] Hijri (IslamicCivil) date display
- [ ] Combined Gregorian/Hijri display
- [ ] Date ordering options (Gregorian-first/Hijri-first)
- [ ] Date format choices (dotted, slash, ISO)
- [ ] Optional ISO week number
- [ ] Week number display
- [ ] Font selection, color, bold
- [ ] Date visibility toggle
- [ ] Independent date scaling
- [ ] Grouped and free layout integration
- [ ] Persistent date settings
- [ ] Turkish locale correctness verified

### Completion Criteria
- Gregorian/Hijri presentation is correct
- Turkish-first date presentation
- All settings persist correctly

---

## Phase 4 — Battery Module ✅ COMPLETE

### Tasks
- [x] Platform-independent battery abstraction (IBatteryService) — `battery_service.dart`
- [x] Windows battery implementation (WMI with `-NoProfile`) — `battery_service_impl.dart`
- [x] Battery percentage/status display
- [x] Charging/plugged-in detection
- [x] Optional battery icon (lightning SVG)
- [x] Battery visibility toggle
- [x] Font, color, bold settings
- [x] Independent battery scaling
- [x] Low-battery threshold (configurable)
- [x] Full-charge threshold (configurable)
- [x] Alert interval setting
- [x] Alert sound configuration
- [x] Silent mode respect
- [x] No-battery fallback behavior
- [x] Efficient 30-second coarse polling
- [x] Grouped and free layout integration
- [x] BatteryNotifier + StateNotifierProvider
- [x] BatteryWindow UI with SVG lightning icon on right
- [x] ProviderScope integration in main.dart

### Completion Criteria
- Battery percentage correctly shows via WMI
- Lightning SVG icon displays on right when charging
- App builds and runs
- Clock + Date + Battery all displayed

### Notes
- `flutter build windows --debug` fails at `INSTALL.vcxproj` — manually copy `build\flutter_assets\*` to `build\windows\x64\runner\Debug\data\` after build
- D:\Code dışına yazma yasak kesintisiz
- [ ] Font, color, bold settings
- [ ] Independent battery scaling
- [ ] Low-battery threshold (configurable)
- [ ] Full-charge threshold (configurable)
- [ ] Alert interval setting
- [ ] Alert sound configuration
- [ ] Silent mode respect
- [ ] No-battery fallback behavior
- [ ] Efficient 30-second coarse polling
- [ ] Unchanged-state suppression
- [ ] Grouped and free layout integration

### Completion Criteria
- Battery module works without excessive CPU usage
- Alerts ready for unified notification system
- Stable on battery and non-battery systems

---

## Phase 5 — Layout System and Quick Actions

### Layout System
- [ ] Final grouped-layout behavior
- [ ] Final free-layout behavior
- [ ] Independent Clock/Date/Battery positioning
- [ ] Position persistence (per module)
- [ ] Layout lock/unlock
- [ ] Configurable inter-module spacing
- [ ] Scale interactions (global and per-module)
- [ ] Multi-monitor verification
- [ ] Position clamping to active window bounds

### Quick Actions
- [ ] Contextual Quick Actions component
- [ ] Settings action
- [ ] Reminder action (placeholder until Phase 6)
- [ ] Todo action (opens Todo panel)
- [ ] Content-aware positioning
- [ ] Stable hover transition with bridge zone
- [ ] Delayed hide (250ms timer)
- [ ] Suppression during window movement
- [ ] Independent icon-size property
- [ ] Smooth opacity/scale animations
- [ ] No-flicker behavior

### Completion Criteria
- Main desktop surface reaches polished daily-usable state
- Quick Actions stable as frozen Python reference
- Layout behavior predictable after restart

---

## Phase 6 — Settings System

### Tasks
- [ ] Settings domain/schema (typed snapshot)
- [ ] Versioned settings storage (schema version tracking)
- [ ] Safe defaults for all settings
- [ ] Migration mechanism (v1→v2→v3)
- [ ] Corruption recovery (`.corrupt` backup)
- [ ] Separate user preferences vs device-specific settings
- [ ] Clock settings UI (visibility, font, color, bold, scale)
- [ ] Date settings UI
- [ ] Battery settings UI
- [ ] Layout settings UI
- [ ] Quick Actions settings UI
- [ ] Notification settings UI (visual, sound, TTS, cooldown)
- [ ] Global silent mode
- [ ] Always-on-top setting
- [ ] Startup registration (Windows Run key)
- [ ] Global scale (75%–150%)
- [ ] Per-module scale controls
- [ ] Live visual updates
- [ ] Reset-to-default behavior
- [ ] Settings persistence verification (INI round-trip)

### Completion Criteria
- All modules configurable through one coherent UI
- Settings survive restart safely
- UI changes apply immediately

---

## Phase 7 — Todo V1

### Data and Domain
- [ ] Finalize Todo V1 data model
- [ ] SQLite repository via `drift`
- [ ] Schema migrations
- [ ] Priority model (Low/Normal/High)
- [ ] Task state transitions (Active/Completed/Cancelled/Trashed)
- [ ] Due/overdue rules
- [ ] Ordering rules
- [ ] Retention policy
- [ ] Trash/restore/permanent-delete

### UI
- [ ] Todo panel/page
- [ ] Task cards (with priority color strip, status watermark)
- [ ] New Task dialog
- [ ] Edit Task dialog
- [ ] Description support
- [ ] Date/time input
- [ ] Priority selection
- [ ] Completed state
- [ ] Overdue state
- [ ] Cancelled state
- [ ] Trash state
- [ ] Search (title/description)
- [ ] Turkish search normalization
- [ ] Today/Tomorrow/Week/Completed filters
- [ ] Useful empty states
- [ ] Stable scrolling and model updates
- [ ] Visual customization
- [ ] TodoModel–SQLite–UI integration
- [ ] Subtask/checklist support

### Completion Criteria
- Todo reaches functional parity with intended scope
- Sorting and state transitions covered by tests
- UI polished and professional

---

## Phase 8 — Reminder V1 Completion

### Core
- [ ] Reminder model finalized
- [ ] SQLite repository via `drift`
- [ ] Reminder scheduler (Dart Timer-based)
- [ ] One-time reminders
- [ ] Daily recurrence
- [ ] Weekly recurrence
- [ ] Missed reminder recovery
- [ ] Duplicate firing prevention
- [ ] Application-restart recovery
- [ ] Enable/disable behavior
- [ ] Snooze (5/10/60 minutes)
- [ ] Remaining-time formatting (Turkish)
- [ ] Safe malformed-data handling

### UI
- [ ] Reminder list UI
- [ ] Add Reminder dialog
- [ ] Edit Reminder dialog
- [ ] Reminder cards
- [ ] Active/completed/missed states
- [ ] Validation
- [ ] Non-disruptive popup behavior

### Voice / TTS
- [ ] Native/offline TTS strategy (flutter_tts)
- [ ] Optional TTS
- [ ] Voice selection
- [ ] Spoken-text preview
- [ ] Non-blocking execution
- [ ] Respect silent mode

### Completion Criteria
- Reminder V1 complete and reliable across restarts
- Recurrence and snooze tested
- No duplicate notifications

---

## Phase 9 — Advanced Todo Features & UI Redesign

### Tasks
- [ ] Drag-and-drop reordering
- [ ] Task tags/labels
- [ ] Project/category grouping
- [ ] Archiving old tasks
- [ ] Quick-add command bar
- [ ] UI redesign: left vertical color strip with priority text
- [ ] UI redesign: dynamic status icons (!, hourglass, check)
- [ ] UI redesign: title + truncated description with tooltip
- [ ] UI redesign: diagonal watermarks ("SÜRESİ GEÇTİ", etc.)
- [ ] UI redesign: cancelled state grays out and moves to bottom
- [ ] UI redesign: right action buttons with hover tooltips
- [ ] UI redesign: gray rounded input fields
- [ ] UI redesign: subtask list input with free formatting
- [ ] Quick Actions visual redesign (horizontal icons above modules)
- [ ] Quick Actions icon assets

### Completion Criteria
- Professional, modern Todo experience
- Data integrity maintained during complex transitions

---

## Phase 10 — Alarm Module
- [ ] Alarm domain model
- [ ] Alarm repository
- [ ] Alarm scheduling
- [ ] Daily recurrence
- [ ] Alarm sounds
- [ ] Alarm popup
- [ ] Enable/disable behavior
- [ ] Reminder vs Alarm semantics defined

---

## Phase 11 — Unified Notifications, Tray, and Lifecycle
- [ ] Notification coordinator
- [ ] Visual notifications
- [ ] Sound and TTS routing
- [ ] Silent mode
- [ ] Cooldown and duplicate suppression
- [ ] Battery/Reminder/Alarm alert integration
- [ ] System tray icon
- [ ] Show/hide DeskPilot
- [ ] New Reminder/Todo/Settings actions
- [ ] Single-instance behavior
- [ ] Run at startup
- [ ] Clean shutdown and state persistence

---

## Phase 12 — Localization Foundation
- [ ] Central localization architecture
- [ ] All user-facing strings in translation resources
- [ ] Turkish V1 text review
- [ ] English foundation
- [ ] Arabic/RTL architecture check

---

## Phase 13 — UI/UX Visual Overhaul
- [ ] Modern color palettes (light/dark modes)
- [ ] Enhanced typography hierarchy
- [ ] Glassmorphism/Acrylic effects
- [ ] Component-level polish (buttons, textfields, checkboxes)
- [ ] Golden ratio spacing in cards
- [ ] Elegant scrollbars
- [ ] Micro-animations
- [ ] Smooth transitions
- [ ] Spring/bounce animations

---

## Phase 14 — Performance, Stability, Quality Gate
- [ ] Cold/warm startup measurement
- [ ] Idle CPU/memory benchmarks
- [ ] Multi-monitor/DPI/sleep tests
- [ ] Corrupted settings/record tests
- [ ] Unit tests for critical domain logic
- [ ] Integration tests for persistence
- [ ] License review
- [ ] Dead code removal

---

## Phase 15 — Desktop V1 Release
- [ ] Feature freeze
- [ ] Final UI/UX polish
- [ ] Packaging and installer
- [ ] Versioning and release notes
- [ ] Clean installation test
- [ ] Desktop V1 tagged

---

## Post-V1 (Must not block V1)
- Phase 16: Shared Account and Sync Architecture
- Phase 17: Mobile Client (Flutter + Dart)
- Phase 18: Web Client (TypeScript + React)
- Phase 19: Cross-Platform Product Maturity

---

## Immediate Next Task
1. Proceed to Phase 5: Layout System and Quick Actions
