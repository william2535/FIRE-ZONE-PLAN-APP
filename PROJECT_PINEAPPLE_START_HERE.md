# 🍍 OPERATION PINEAPPLE — START HERE

**If you are resuming this project after a chat reset, tool crash, or time away: start with this file.**

## Current working branch

`project-pineapple-v058`

Do **not** start by guessing from old chat messages. Read this file, then read `.github/PROJECT_PINEAPPLE_CHECKPOINT.md`, then inspect the latest CI for the branch head.

## Latest deployed major milestone

**Pineapple v0.58 — Manual Editor Core Green**

Stable web branch: `main`

Deployed web milestone commit:

`89eee3561d652f510458a172151d1d1cdb849dfd`

Milestone PR: `#3 — Publish Pineapple v0.58 web milestone`

The exact pre-merge Pineapple checkpoint that passed the release gates was:

`5f4ec568487216648151f1cc84f0a6283649c2d8`

Release-gate results on that checkpoint:

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
- visible browser/app title: v0.58

A real Bridge-mode coordinate-shadowing defect is also repaired in both generator source and generated app: bridge crossings use `hit` as the callback variable so numeric canvas height `h` is preserved.

## LIVE WEB STATE

- **LIVE STABLE WEB:** `main` @ `89eee3561d652f510458a172151d1d1cdb849dfd`
- **DEVELOPMENT / CONTINUOUS SAVE:** `project-pineapple-v058`
- Never assume the Pineapple branch is live. Only a recorded major-milestone promotion to `main` is the live web state.

## NEXT EXACT STEP

1. Continue on `project-pineapple-v058`, not `main`.
2. Add a dedicated real-crossing Bridge regression.
3. Prove bridge marker coordinates are finite and survive staged replacement, splice, Done/save, reopen and redraw.
4. Break-test manual editing across small iPhone, large iPhone, Android phone, small tablet and landscape/desktop viewports, including zoomed-in/out and awkward/fast/shaky input.
5. Keep routing/capture/editor/protected-24-7/generated-copy gates green.
6. At the next coherent green major milestone, promote that checkpoint to `main` and replace the LIVE STABLE WEB SHA above.

## Continuous-save rule

Operation Pineapple must never rely on chat state alone.

- Commit every meaningful logical change to `project-pineapple-v058` as it is completed.
- Commit before risky structural edits.
- Update `.github/PROJECT_PINEAPPLE_CHECKPOINT.md` whenever the active blocker, test result, or next step changes materially.
- Keep this START HERE file short and current: working branch, live-web SHA, latest known-good milestone and next exact step.
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
- **Web app / `main`:** stable major milestones for real iPhone/Android testing.

## What counts as a major milestone

Publish to web when a coherent chunk is genuinely usable, for example:

- routing generation materially improved and regression-tested;
- manual editor reaches a stable end-to-end state;
- a major mobile interaction overhaul is green;
- a substantial new mode/feature is complete enough for real-device testing;
- a release candidate is ready for hands-on testing.

Do **not** publish every tiny diagnostic/test-only commit to the web app.

## Safety invariant

The protected 24/7 company/demo build must remain unchanged unless the user explicitly asks to change it.
