# Qt Strategy

DeskPilot standardizes on PySide6.

- `requirements.txt` includes PySide6 only.
- New UI code should import PySide6 directly.
- Existing PyQt6 fallback blocks are legacy compatibility code.
- Do not add new PyQt6 fallbacks unless PyQt6 is also added to supported dependencies.
