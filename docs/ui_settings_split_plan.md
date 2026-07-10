# ui_settings Split Plan

`ui_settings.py` is large, but currently stable. Split only before adding new settings.

Suggested order:

- Move help text and help-window positioning to `ui_settings_help.py`.
- Move preview handlers to `ui_settings_preview.py`.
- Move task priority table logic to `ui_settings_priorities.py`.
- Keep `SettingsDialog` as the coordinator and public entry point.
- After each move, run `py_compile` and a settings-dialog smoke test.
