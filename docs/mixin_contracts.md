# Window Mixin Contracts

These mixins are composed by `core_window.DeskPilotWindow`.

- `WindowInitMixin`: creates shared labels, layouts, quick actions, free-window refs, drag state, and blink state.
- `WindowRuntimeMixin`: creates timers, services, popup registries, and context-menu wiring.
- `WindowSettingsMixin`: expects labels/layouts/free-window refs from init and `settings` from the main window.
- `WindowMouseMixin`: expects `settings`, `drag_pos`, `quick_actions`, and battery/time/date row widgets.
- `WindowTopmostMixin`: expects `_keep_top_timer`, `settings`, and QWidget visibility/window methods.
- `WindowLifecycleMixin`: expects `_update_keep_on_top()` from `WindowTopmostMixin`.

New mixin code should document any required `self.*` fields here before use.
