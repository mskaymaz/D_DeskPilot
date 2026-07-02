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
