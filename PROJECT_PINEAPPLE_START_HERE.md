# 🍍 OPERATION PINEAPPLE — START HERE

**If you are resuming this project after a chat reset, tool crash, or time away: start with this file.**

## Current working branch

`project-pineapple-v058`

Do **not** start by guessing from old chat messages. Read this file, then read `.github/PROJECT_PINEAPPLE_CHECKPOINT.md`, then inspect the latest CI for the branch head.

## Latest deployed major milestone

**Pineapple v0.58 — Manual Editor Core Green**

Stable web branch: `main`

Core web-app milestone merge:

`89eee3561d652f510458a172151d1d1cdb849dfd`

Milestone PR: `#3 — Publish Pineapple v0.58 web milestone`

The exact pre-merge Pineapple checkpoint that passed the original release gates was:

`5f4ec568487216648151f1cc84f0a6283649c2d8`

The v0.58 manual editor includes Pencil, Bin, Undo, Redo, Bridge, Cleanup and Done, with persisted edit drafts and As-Fit protection while a route is open.

## Latest known-green development hardening point

**TESTED APP/TEST HEAD:** `ea7b0255b6e01d195f36b286f4e69e909a83f12a`

On that exact development checkpoint:

- manual editor lane: PASS
- routing compatibility lane: PASS
- aggressive-touch / capture transition lane: PASS
- protected 24/7 verification: PASS
- inline parser and browser startup: PASS
- dedicated real-crossing Bridge persistence regression: PASS
- multi-viewport Manual Edit stress: PASS
- committed rough Pencil/Bin splice at 1× zoom: PASS
- committed shaky/direction-changing Pencil/Bin splice at 6× zoom: PASS
- Smart Route compatibility: PASS
- generated HTML copy equality: PASS

The 1× and 6× gesture regression now performs actual saved route surgery: stage replacement → Bin old span → validate → Done. Test-fixture false alarms were corrected without unnecessary product-code changes.

## LIVE WEB STATE

- **CORE WEB APP:** `main/index.html` = v0.58 with the manual editor present.
- **BETA PORTAL DELIVERY FIX:** PR `#5`, merged as `34af3e5737c2b1607c09073904df6c69dad373cb`.
- **FRESH UNCACHED WEB LAUNCHER:** `main/web-v058.html`.
- Fresh-launch PR: `#6 — Publish fresh v0.58 web launcher`.
- Fresh-launch main commit: `406dfdcc0bec0507825a0da9635147975b9bd7b1`.
- Public real-device entry point: `https://william2535.github.io/FIRE-ZONE-PLAN-APP/web-v058.html`.
- `web-v058.html` redirects to `index.html?pineapple=v058&fresh=<timestamp>` on every load.
- The portal explicitly shows **Web v0.58 · Android v0.57**.
- The current packaged Android release remains **v0.57** until a separate v0.58 APK is built and released.
- **DEVELOPMENT / CONTINUOUS SAVE:** `project-pineapple-v058`.

## Branch reconciliation warning

Before the next publication, reconcile `project-pineapple-v058` with current `main`.

Do not assume the commits missing from Pineapple are harmless delivery-only changes. Inspect the exact commit/file differences first, then preserve both sides deliberately.

## NEXT EXACT STEP

1. Continue on `project-pineapple-v058`, not `main`.
2. Inspect every current `main`-only commit/file change that Pineapple is missing.
3. Reconcile `main` into Pineapple carefully while preserving the green editor/routing/capture state and the live delivery/version-launcher work.
4. Rerun all three Pineapple lanes after reconciliation.
5. Do **not** publish a new web milestone just because test coverage improved; wait for a coherent product milestone.
6. Before any future promotion, verify Pages, `index.html`, `beta.html`, visible version labels and the fresh launcher together.

## Continuous-save rule

Operation Pineapple must never rely on chat state alone.

- Commit every meaningful logical change to `project-pineapple-v058` as it is completed.
- Commit before risky structural edits.
- Update `.github/PROJECT_PINEAPPLE_CHECKPOINT.md` whenever the active blocker, test result, deployment result or next step changes materially.
- Keep this START HERE file short and current.
- Prefer small reproducible changes over one giant unsaved edit.
- Never leave a long investigation only in conversation history.

## Web milestone rule

The web app is a **milestone surface**, not the scratch branch.

When a major milestone is reached:

1. all relevant Pineapple CI must be green;
2. protected 24/7 verification must remain green;
3. generated app copies must agree;
4. reconcile current `main` into development if branches have diverged;
5. publish/merge only a known-good coherent milestone to `main`;
6. verify the actual Pages deployment/run and, where practical, its artifact;
7. verify `index.html`, `beta.html`, visible version labels and launch URLs;
8. update the fresh launcher when appropriate;
9. immediately record the deployed web state here and in the checkpoint;
10. continue experimental work on Pineapple rather than using the live web app as the scratchpad.

Do **not** publish every diagnostic/test-only commit to the web app.

## Safety invariant

The protected 24/7 company/demo build must remain unchanged unless the user explicitly asks to change it.
