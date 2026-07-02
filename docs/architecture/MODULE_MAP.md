# DeskPilot Module Map

## Entry
- DeskPilot.py: application startup

## Core
- core_window.py: main floating clock/window behavior
- core_settings.py: settings persistence/defaults
- pencere_araclari.py: shared window helpers
- pencere_navigasyon.py: window navigation helpers
- pencere_guncelleme.py: window update helpers

## Services
- pil_servisi.py: battery service
- bildirim_servisi.py: notification service
- log_servisi.py: logging
- gorev_servisi.py: todo service
- hatirlatici_servisi.py: reminder service

## UI
- ui_settings.py: settings UI
- ui_ayarlar_formlar.py: settings forms
- sistem_tepsisi.py: tray UI
- serbest_pencere.py: free floating window
- serbest_duzen.py: free layout
- kart.py: card UI
- gorev_arayuzu.py: todo UI
- hatirlatici_*.py: reminder UI

## Refactor Priority
1. core_window.py
2. ui_settings.py
3. kart.py
4. gorev_arayuzu.py
5. storage/settings services

## File Size Rule
- Target: every Python file should stay under 500 lines.
- Ideal range: 200-350 lines.
- Temporary exception: up to 700 lines only during active refactor.
- Files above 500 lines must be listed as refactor candidates.
## Single Responsibility Rule
- One file = one primary responsibility.
- UI, business logic and persistence must not be mixed.
- Shared code belongs in reusable services/helpers.
- New features should extend existing modules before creating new ones.
## Dependency Rule
- UI -> Services -> Models.
- Models must not depend on UI.
- Services must not depend on UI widgets.
- Core modules may be shared by all layers.
## Naming Rule
- Code identifiers: English (ASCII only).
- User interface: Turkish (UTF-8).
- One class per file whenever practical.
- File names use snake_case.
- Public APIs should remain stable during refactoring.
## Backward Compatibility Rule
- Refactoring must not change user-visible behavior.
- Every refactor step must end with a successful py_compile.
- Manual verification is required before the next refactor step.
- Refactor first, optimize later.
