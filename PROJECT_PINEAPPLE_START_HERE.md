# 🍍 OPERATION PINEAPPLE — START HERE

**If you are resuming this project after a chat reset, tool crash, or time away: start with this file.**

## Current working branch

`project-pineapple-v058`

Do **not** start by guessing from old chat messages. Read this file, then read `.github/PROJECT_PINEAPPLE_CHECKPOINT.md`, then inspect the latest CI for the branch head.

## Latest known-good major milestone

**Pineapple v0.58 — Manual Editor Core Green**

Last fully proven green app milestone:

`6fbd5639df51c6b2b6be892a104c210df47519c2`

Current web-milestone candidate after synchronising the visible v0.58 label across all generated app copies:

`f941d9fdf98c453708556e5eef8d7907d34d0ae0`

This START HERE checkpoint commit intentionally triggers the normal Pineapple CI against that candidate before web promotion.

At the proven green milestone:

- inline JavaScript parser: PASS
- clean browser startup: PASS
- Circuit Builder routing compatibility: PASS
- aggressive-touch / capture transition: PASS
- manual editor end-to-end regression: PASS
- draft-first Pencil/Bin splice: PASS
- bridge-locality bookkeeping: PASS
- ROUTE OPEN protection: PASS
- Undo / Redo: PASS
- Done validation and save: PASS
- cleanup regression: PASS
- Smart Route compatibility: PASS
- protected 24/7 verification: PASS
- generated HTML copy equality: PASS

A real Bridge-mode coordinate-shadowing defect is also repaired in both generator source and generated app: bridge crossings use `hit` as the callback variable so numeric canvas height `h` is preserved.

## LIVE WEB STATE

- Stable web branch: `main`
- Current Pineapple v0.58 candidate: pending final CI before promotion
- After promotion, record the exact deployed `main` SHA here immediately.

## NEXT EXACT STEP

1. Confirm normal Pineapple editor/routing/capture CI is green on this checkpointed v0.58 candidate.
2. Promote the known-good milestone to `main` for real-device web testing.
3. Record the deployed `main` SHA here and in `.github/PROJECT_PINEAPPLE_CHECKPOINT.md`.
4. Continue on Pineapple with a dedicated real-crossing Bridge regression and phone/tablet break-testing.

## Continuous-save rule

Operation Pineapple must never rely on chat state alone.

- Commit every meaningful logical change to `project-pineapple-v058` as it is completed.
- Commit before risky structural edits.
- Update `.github/PROJECT_PINEAPPLE_CHECKPOINT.md` whenever the active blocker, test result, or next step changes materially.
- Keep this START HERE file short and current: branch, latest known-good milestone, live-web state and next exact step.
- Prefer small reproducible changes over one giant unsaved edit.
- Never leave a long investigation only in conversation history.

## Web milestone rule

The web app is a **milestone surface**, not the scratch branch.

When a major milestone is reached:

1. all relevant Pineapple CI must be green;
2. protected 24/7 verification must remain green;
3. generated app copies must agree;
4. publish/merge the known-good milestone to `main` so the web app receives it;
5. immediately record the deployed `main` commit here and in the checkpoint;
6. continue experimental work on the Pineapple branch rather than using the live web app as the scratchpad.

This gives two layers:

- **Pineapple branch:** continuous saved development/checkpoints.
- **Web app / `main`:** stable major milestones that are useful to test on real iPhone/Android hardware.

## How to recognise a major milestone

Publish to web when a coherent chunk is genuinely usable, for example:

- routing generation materially improved and regression-tested;
- manual editor reaches a stable end-to-end state;
- a major mobile interaction overhaul is green;
- a substantial new mode/feature is complete enough for real-device testing;
- a release candidate is ready for hands-on testing.

Do **not** publish every tiny diagnostic/test-only commit to the web app.

## Safety invariant

The protected 24/7 company/demo build must remain unchanged unless the user explicitly asks to change it.
