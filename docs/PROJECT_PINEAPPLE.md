# PROJECT PINEAPPLE

## Trigger phrase

**Project Pineapple**

This phrase is the short command for the full continuous Zone Sketch / Circuit Builder CAD-parity premium-development loop.

If the user says only **"Project Pineapple"**, or clearly says to start/continue Project Pineapple, do NOT ask them to restate the project requirements.

Immediately recover the project from GitHub and begin the process below.

## Required recovery order

Read, in this order:

1. `docs/PROJECT_PINEAPPLE.md`
2. `docs/CIRCUIT_BUILDER_CONTINUITY.md`
3. `docs/CIRCUIT_BUILDER_NEXT_PROMPT.md`
4. `docs/CIRCUIT_BUILDER_PREMIUM_LOOP_PROMPT.md`
5. `docs/AS_FIT_CAD_REFERENCE_RULES.md`
6. `docs/CIRCUIT_BUILDER_CAD_PARITY_LOOP.md`

Then inspect current `main`, recent Circuit Builder commits/PRs, current deployed version, regression tests and recent workflow status.

The repository is the persistent source of truth. Do not restart work already recorded as complete.

## What Project Pineapple means

Project Pineapple is not one bug fix or one feature request.

It means continuously push Zone Sketch toward this product goal:

> A competent fire-alarm engineer should be able to walk a real site with a phone/tablet and locally produce a professional As-Fitted drawing fast enough for site use, with output approaching the clarity and finish of a careful desktop CAD handover drawing, without requiring the office to redraw rough marked-up plans.

The app should be faster and simpler than CAD to operate while progressively approaching CAD-quality output.

## Automatic work loop

When Project Pineapple starts, follow this loop repeatedly:

`recover context -> baseline -> inspect real professional references -> extreme stress test -> identify weakness -> reproduce -> add failing deterministic regression -> fix root cause -> compare before/after -> full regression suite -> WebKit/Safari where practical -> Android build -> CAD-quality audit -> field-speed audit -> fresh-eyes whole-workflow audit -> premium polish -> attack again -> repeat`

Do not stop at the first green CI run if useful work remains.

Every genuine defect found should preferably become a permanent regression, validation rule, metric, invariant or documented limitation.

Do not merely fix one screenshot. Improve the system that allowed the defect.

## Current known priority work

Always defer to `CIRCUIT_BUILDER_CONTINUITY.md` for the exact current state, but at the time Project Pineapple was created the recorded next-generation priorities included:

- reproduce/fix the transient long live cable leg that can shoot from a newly captured detector and follow the thumb before settling;
- professional local route editing with Pencil, Bin, Undo, Redo and Done/Validate;
- `EDITING · ROUTE OPEN` state for temporarily broken manual edits;
- 90-degree / Smart Grid final geometry;
- live rough/responsive pencil feedback with post-release cleanup;
- bend-cleaning strength slider;
- explicit circular Bridge Mode toggle;
- intentional bridge/jump rendering;
- different-colour cable lanes able to run neatly beside one another while remaining topologically separate;
- deterministic aggressive-touch and long-session stress tests;
- repeated whole-screen polish rather than narrow bug patches.

## Extreme stress requirement

Project Pineapple should actively try to break the app.

At minimum keep attacking:

- clean/slow input;
- realistic rough input;
- deliberately abusive input;
- sparse high-speed swipes;
- shaky/zig-zag input;
- overshoot and undershoot;
- accidental reversals;
- abrupt direction changes;
- diagonal sweeps;
- several devices crossed in one movement;
- screen-edge interactions;
- pointer cancel;
- second/third pointer;
- pinch/zoom during operations;
- Fit during operations;
- viewport resize/rotation;
- blur/app switching;
- save/reload;
- repeated route/edit/delete/undo/redo cycles;
- dense multi-colour drawings;
- large device counts;
- repeated As-Fit regeneration;
- long-session degradation.

Use deterministic/fixed-seed traces where possible so failures are replayable release after release.

Record route-quality/data-integrity metrics where useful, including points, segments, corners, short legs, reversals, duplicate points, zero-length segments, intersections, bridges, orphan fragments, route length ratio, device capture and validation state.

## Real As-Fitted/CAD reference mining

On substantial Project Pineapple passes, use current public web references where available.

Inspect actual fire-alarm As-Fitted examples, drawings, PDFs and professional CAD outputs where legally/publicly accessible.

Study general engineering-document conventions such as:

- actual cable routing;
- multiple cable lane spacing;
- device/loop/address labels;
- isolators, PSUs, repeaters, junctions and remote indicators;
- crossing vs connection treatment;
- risers/cross-floor continuation;
- legends;
- title blocks;
- revisions;
- device and circuit schedules;
- line weights;
- label placement;
- print readability;
- vector output.

Do not copy logos, proprietary title blocks or copyrighted artwork. Extract general drafting rules and workflow ideas.

Record useful generic findings in `docs/AS_FIT_CAD_REFERENCE_RULES.md`.

## Field-speed rule

CAD-quality output must not come at the cost of CAD-speed input.

Continuously ask:

- can this be one tap instead of three?;
- can existing project data fill this automatically?;
- can addresses/references auto-increment?;
- can the legend/title block/schedules generate automatically?;
- can labels position themselves?;
- can repeated cable paths form automatic lanes?;
- can the engineer complete this comfortably on a tablet while walking site?;
- can core work stay local/offline?;

Do not ask the engineer to type information the app already knows.

## CAD-parity output direction

Continue pushing toward professional exports, including where practical:

- clean high-resolution As-Fit;
- vector SVG;
- vector PDF;
- dynamic legend;
- title block;
- revision data;
- loop/device references;
- device/circuit schedules;
- smart label collision avoidance;
- cross-floor continuation;
- print/paper layout;
- export validation.

Do not turn the field UI into mini-AutoCAD. Keep complexity in the engine/exporter and keep onsite interaction quick.

## Benchmark projects

Maintain/expand deterministic benchmark jobs such as:

1. small conventional office;
2. school / multi-block addressable system;
3. warehouse / industrial system;
4. dense hotel/corridor system;
5. multi-floor/riser loop;
6. messy retrofit/imported plan.

Use them to measure regressions and manual cleanup required.

## Premium stopping condition

A strong Project Pineapple session should ideally stop only when:

- current recorded priority work is complete or precisely handed off;
- no known critical/high corruption remains;
- focused deterministic tests pass;
- full regression suite passes;
- Android build passes;
- WebKit/Safari-engine checks pass where practical;
- representative As-Fit output has been inspected;
- CAD-quality and field-speed audits have been performed;
- at least two consecutive fresh-eyes/extreme passes find no new material defect requiring immediate code changes;
- continuity documentation is current.

If tool/session limits interrupt the work, update the continuity brief with the exact branch, commit, tests, failure and next action. Do not pretend the pass is finished.

## Continuity rule

Update `docs/CIRCUIT_BUILDER_CONTINUITY.md` at meaningful checkpoints, not only at the very end.

Useful checkpoints include:

- after reproduction/baseline;
- after root-cause fix;
- after a major editor/output milestone;
- after new stress tests;
- after full regression;
- after PR merge;
- after post-merge verification.

Future sessions must be able to resume without the user repeating anything.

## Short command

The user should only need to say:

> **Project Pineapple**

That means: recover from GitHub, continue from the exact current state, and run the full continuous premium/CAD-parity hardening process automatically.