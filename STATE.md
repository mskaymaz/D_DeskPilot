# DESKPILOTF STATE

## Project
**D_DeskPilotF**

## Repository
Remote: `https://github.com/mskaymaz/D_DeskPilotF`

## Current Phase
**Phase 4 — Battery Module** ✅ COMPLETE

<!-- BISMILLAH CHECKPOINT: Phase 4 – Complete -->

## Current Status
Phase 4 complete. Battery module working with WMI + SVG icon.

## Completed
- C++/Qt codebase removed from repository
- Git remote updated to `https://github.com/mskaymaz/D_DeskPilotF`
- Flutter project structure created (`lib/`, `test/`, `assets/`, `windows/`)
- `pubspec.yaml` configured with `window_manager`, `flutter_localizations`, `intl`, `riverpod`, `flutter_riverpod`, `flutter_svg`
- Design tokens: `lib/core/design_tokens/`
- Localization: `lib/core/localization/app_localizations.dart`, `l10n/`
- **Phase 2 — Clock Module:** IClockService, Timer-based, ClockNotifier, ClockWindow
- **Phase 3 — Date Module:** IDateService, Timer-based, DateNotifier, DateWindow (Gregorian + Hijri)
- **Phase 4 — Battery Module:**
  - `lib/domain/models/battery_model.dart` — BatterySettings, BatteryState, BatteryStatus
  - `lib/domain/services/battery_service.dart` — IBatteryService abstract interface
  - `lib/infrastructure/platform/battery_service_impl.dart` — WMI-based implementation with `-NoProfile`
  - `lib/application/providers/battery_provider.dart` — BatteryNotifier, StateNotifierProvider
  - `lib/presentation/screens/battery_window.dart` — BatteryWindow with lightning SVG icon on right side
  - `assets/images/lightning_icon.svg` added
- `flutter_svg: ^2.0.13` added to dependencies
- `assets/images/` declared in pubspec.yaml
- `flutter build windows --debug` produces working `desk_pilot_f.exe`
- Clock + Date + Battery displayed in transparent window
- Battery percentage now correctly shows via WMI `-NoProfile`
- Note: `INSTALL.vcxproj` fails — manually copy `build\flutter_assets\*` to `build\windows\x64\runner\Debug\data\` after build

## Documentation Status
- `DESKPILOT_PRODUCT_SPEC.md` — Updated for Flutter/Dart
- `PRODUCT_ARCHITECTURE_PRINCIPLES_AI_EN.md` — Retained
- `ARCHITECTURE.md` — Updated for Flutter/Dart
- `ROADMAP.md` — Updated for Flutter phases
- `README.md` — Updated for Flutter
- `AGENTS.md` — Updated for Flutter workflow

## Technology Stack
- **UI:** Flutter/Dart + Material 3 + Custom Design Tokens
- **State Management:** Riverpod
- **Persistence:** drift (SQLite) + Hive (lightweight settings)
- **Platform:** window_manager, tray_manager, flutter_tts, audioplayers
- **Build:** `flutter build` + `flutter create` Windows embedding
- **Testing:** flutter_test + mockito + drift testing utilities
- **Target Platform:** Windows (initial), macOS/Linux (future)

## Architecture Direction
```
Flutter UI (Presentation Layer)
    ↓ Riverpod State Management
    ↓ ViewModels / Presenters
    ↓ Application Services
    ↓ Domain Models (Dart)
    ↓ Repositories (drift/SQLite)
    ↓ Platform Plugins (window_manager, tray_manager, etc.)
```

## Important Product Rules
- Frozen Python DeskPilot defines intended behavior, not implementation
- Do not mechanically translate any previous code
- Flutter UI must not embed business logic
- Domain models must be pure Dart, testable without Flutter
- All user-facing text must be localization-ready
- Design Tokens must be consumed by all widgets
- File size limit: 400-450 lines soft, 700 hard
- D:\Code dışına yazma yok — bu kural kesin

## Development Workflow
SPP-style workflow:
1. Analyze and verify first
2. Work on one agreed task at a time
3. Keep changes focused
4. Avoid unrelated refactoring
5. Verify each implementation before continuing
6. Update `TASK.md` and `STATE.md` after meaningful milestones
7. Update `ROADMAP.md` when phase-level progress changes

## Immediate Next Steps
1. Proceed to Phase 1: Design System
2. Implement color/typography/spacing/radius design tokens
3. Create reusable base widgets

## AI Agent Continuation Instruction
Before modifying this repository, read in this order:
1. `AGENTS.md`
2. `STATE.md`
3. `TASK.md`
4. `ROADMAP.md`
5. `DESKPILOT_PRODUCT_SPEC.md`
6. `PRODUCT_ARCHITECTURE_PRINCIPLES_AI_EN.md`
7. `ARCHITECTURE.md`

Continue from the current state. Do not restart architectural interpretation unless a real conflict or new requirement requires a decision.

Communicate with the user in Turkish unless explicitly requested otherwise.

## Known Issues (2026-09-18, multi-window aşaması)
1. Renk seçim diyaloğu küçük modül pencerelerine sığmıyor: diyalog 260px, modül pencereleri 280-440px olduğu için renkler kırpılıyor. Çözüm adayı: diyalogu ayrı pencere olarak açmak veya modül penceresini geçici büyütmek.
2. Modül metinlerinin altında sarı çizgi artefaktı: kodda sarı çizgi çizen widget yok (grep ile doğrulandı), çoklu örnek ihtimali elendi (tek process ile test edildi). Nedeni bilinmiyor, evde incelenecek.
3. Modül pencerelerinde ince kenarlık/gölge kalıyor: `setAsFrameless` + `setHasShadow(false)` + `setResizable(false)` etkisiz.
4. `window_manager` boyutlandırma çağrıları (`setSize`, `maximize`) etkisiz: pencere Flutter varsayılanı 1280x720'de takılı kalıyor. Bu yüzden tek-pencereli düzenden vazgeçilip `desktop_multi_window` mimarisine geçildi (her modül kendi çerçevesiz penceresi + gizli kontrolcü pencere).
5. Sağ tık menüsüne "Uygulamadan çık" (`exit_app`) eklendi.

## Last Updated
2026-09-18 — Multi-window mimari + sağ tık renk ayarı + çıkış komutu. Bilinen hatalar yukarıda kayıtlı.

## IST-001 Denetim Hatırlatıcısı (27.11.2026)
> Yeni oturumda çalışmaya başlandığında önce aşağıdaki eksikler `IST-001` (`D:\Code\mskaymaz\istisare\istisareler\001-uygulama-anayasasi-ve-repo-mimarisi.md`) doğrultusunda ele alınır:
- [ ] Kodda `Eco-SDK` (`eco_device_id` + 7 günlük `/api/v1/telemetry/heartbeat`) entegrasyonu yapılacak.
- [ ] Eksik SSOT belgeleri tamamlanacak: `CORE.md`, `CHANGELOG.md` (`TASK.md` -> `tasks.md` hizalaması) ve `docs/kullanim_kilavuzu/{tr,en,ar}`.
- [ ] `test/widget_test.dart` (`DeskPilotApp` referans hatası) ve `flutter analyze` uyarıları temizlenecek.
