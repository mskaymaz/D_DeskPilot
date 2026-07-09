# D_DeskPilot AGENTS

## Purpose
Working rules only. Product architecture is documented in `CORE.md`; task tracking is based on `MyTaskTr.md` and `MyTaskTrEd.md`.

## SPP
- User chooses task continuation and checklist marking; never inspect task/checklist markdown files or mark items unless the user explicitly asks for that exact step.
- Only after completing an explicitly requested operation, a short progress note may be recorded in the relevant markdown file for later continuity; for resuming that place, read only that relevant markdown file.
- Do not undo, revert, compensate for, or further modify any previous action unless the user explicitly asks for that exact operation, even if the previous action was mistaken.
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
- When `bismillah` or `eko` is active, work in "eko single item" / "eko single stage" mode: handle only one explicitly requested item or stage, then stop and report briefly.
- In `eko tek adım` / `eko tek madde` mode: execute only the explicitly requested scope; do not scan unrelated files, do not broaden the search/changes, and keep responses minimal (one-line status unless asked).
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
