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
- In `eko` or `bismillah` mode, keep normal replies to one short status line unless the user asks for detail.
- Avoid repeated progress narration; use tool calls directly when the requested step is clear.
- No long explanations.
- No unsolicited examples or visuals.

## Runtime Commands
- `bismillah` or `eko`: strict scoped mode.
- In strict scoped mode: execute only the explicitly requested scope, do not scan unrelated files, do not broaden searches or changes, and do not perform automatic fixes.
- In strict scoped mode: do not continue to adjacent tasks, commits, pushes, cleanup, or refactors unless the user explicitly asks for that exact step.
- `banaver`: deliver requested artifact only.
- `temizle`: reset current working context.

## Document Roles
- `AGENTS.md`: working rules.
- `CORE.md`: product architecture.
- `STATE.md`: current project state.
- `Task.md`: upstream/reference roadmap.
- `MyTaskTr.md`: permanent Turkish master roadmap; keep its structure and items intact.
- `MyTaskTrEd.md`: active working checklist; remove headings/items from this file as they are completed.
