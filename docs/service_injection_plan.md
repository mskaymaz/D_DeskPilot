# Service Injection Plan

Current service creation lives in `WindowRuntimeMixin`.

Goal: keep runtime behavior stable while making services injectable later.

Safe migration path:

- Keep `_servisleri_baslat()` as the single service setup entry point.
- Introduce an optional `service_factory` argument on `DeskPilotWindow`.
- Move default constructors into a small factory object or function.
- Tests can pass fake services through that factory.
- Do not change service lifetimes or timer startup in the same patch.
