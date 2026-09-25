# Project Pineapple — Live Checkpoint

This file is the durable handoff for the ongoing Pineapple work. Update it at every meaningful milestone, before risky edits, and after important CI results so work can resume immediately after a chat/tool crash.

## Current branch

- Branch: `project-pineapple-v058`
- Current checkpoint-triggering head: `bd1404121a81eea04459ce5468044b260653a482` — `Checkpoint repaired Pineapple editor parser break`
- Repaired app commit immediately below it: `2a35764842c87fa897064b0d9a2e7117f9b5923a` — `Fix manual editor anchor parser break`
- Protected 24/7 build must remain unchanged.

## Current objective

Continue the v0.58 Circuit Builder / manual editor hardening work without waiting for repeated user prompts. The target is a polished, predictable routing/editor system, not a narrow threshold patch.

## What is already established

- Aggressive-touch / capture-transition work is still green after the editor parser repair.
- The branch contains a real manual editor implementation: Edit, Pencil/Bin, Undo/Redo, Bridge, Cleanup, Done validation, persisted `editDraft`, As-Fit blocking for unfinished edits, bridge rendering, staged replacement/splice, and crossing/overlap validation.
- A concrete editor defect was found earlier: deleting one local cable section could remove bridge metadata too broadly on the same detector-to-detector leg.
- Bridge-locality regression work and local bridge bookkeeping changes are already on the branch and must be preserved.

## Parser blocker — repaired

The former failure was `SyntaxError: Unexpected token ')'` at final `})();`.

Exact root cause was `cbEditAnchorAt()` missing the brace that closes its outer leg loop before `return best`:

- bad: `...d:q.d}}return best}`
- correct: `...d:q.d}}}return best}`

Repair source/workflow:

- `.github/pineapple_v058_editor_syntax_fix.py`
- `.github/workflows/pineapple-v058-editor-syntax-fix.yml`
- syntax-repair workflow run `36196044447`: PASS
- generated repair commit `2a35764842c87fa897064b0d9a2e7117f9b5923a`

The source editor generator was also repaired so it will not regenerate the malformed function.

## Post-repair CI on `bd140412...`

Normal workflows were deliberately retriggered by the API-authored checkpoint commit because the repair workflow's own `GITHUB_TOKEN` commit does not recursively launch the normal push workflows.

### Green gates

- Capture transition run `36196268805`: **PASS**
- Routing compatibility run `36196268726`: **PASS**
- Protected 24/7 verification inside manual-editor run: **PASS**
- Current inline JavaScript parser gate: **PASS** (`2 inline script(s) parse cleanly`)

### Current manual-editor blocker

Manual editor workflow run `36196268753`: **FAIL**
Job `108272700311`.

The app now genuinely starts:

`STARTUP_STATE {"ready":true,"title":"Zone Sketch by Will Flood v0.57 — Fire & Security Field Workspace","hasEditor":false,...}`

Failure is no longer a parser/browser crash. Startup test now fails only because it reports:

- `manual editor API missing after startup`
- `hasEditor: false`

The next task is to determine whether:

1. the editor implementation is present and working inside the app IIFE but the startup test expects an unnecessary global/test API; or
2. the editor bootstrap/exposure step was genuinely omitted, so the editor cannot be entered at runtime.

Do not weaken the test until this distinction is proven.

## Exact syntax diagnostic history retained

A deterministic historical hunk bisect remains in CI as `continue-on-error` and intentionally continues to show the original `c8b76...` hunk 6 / `cbEditAnchorAt` historical defect. This is diagnostic history, not a current-app parse failure.

## Immediate next steps

1. Inspect `tests/circuit-editor-startup-v058.cjs` to see precisely what `hasEditor` means.
2. Inspect current `index.html` / editor generator for the corresponding editor bootstrap/API exposure.
3. If the editor is present but the test wrongly assumes IIFE-local functions must be globals, change the test to assert real UI/behaviour or expose a deliberately narrow test hook only if that is already the project pattern.
4. If the editor bootstrap is actually missing, repair it through the reproducible editor patch/hotfix path and synchronize all four app copies.
5. Re-run manual-editor CI until startup + editor behaviour + bridge locality execute.
6. Then address the first real editor behaviour defect. Specifically audit `cbEditFinishStroke()` because its crossing-map callback appears to shadow the canvas-height parameter `h`, potentially passing the crossing object into `cbPxBoard` as height.
7. Keep capture/routing/24-7/generated-copy gates green throughout.
8. Continue deliberate phone/tablet editor break-testing once deterministic CI is green.

## Pineapple continuity rule

- Save meaningful progress to the branch continuously.
- Update this checkpoint before risky structural edits.
- Update it after important CI outcomes or whenever the active blocker changes.
- Prefer small reproducible patch/generator commits over unsaved broad changes.
- Never leave a long investigation existing only in chat state.
