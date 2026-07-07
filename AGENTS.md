# D_DeskPilot AGENTS

## Purpose
Working rules only. Product architecture is documented in `CORE.md`; task tracking is based on `MyTaskTr.md` and `MyTaskTrEd.md`.

## SPP
- Analyze first.
- One safe patch at a time.
- Verify syntax before delivery.
- No unnecessary refactoring.
- Do not make automatic fixes, edits, commits, pushes, or cleanup unless the user explicitly asks for that step.
- Work only in the user-specified area; do not inspect or change unrelated modules without explicit permission.
- Let the user drive each stage step by step.

## Economic Token
- Keep responses under 3 lines unless requested.
- No long explanations.
- No unsolicited examples or visuals.

## Runtime Commands
- `bismillah` or `eko`: strict scoped mode.
- `banaver`: deliver requested artifact only.
- `temizle`: reset current working context.

## Document Roles
- `AGENTS.md`: working rules.
- `CORE.md`: product architecture.
- `STATE.md`: current project state.
- `Task.md`: upstream/reference roadmap.
- `MyTaskTr.md`: permanent Turkish master roadmap; keep its structure and items intact.
- `MyTaskTrEd.md`: active working checklist; remove headings/items from this file as they are completed.
