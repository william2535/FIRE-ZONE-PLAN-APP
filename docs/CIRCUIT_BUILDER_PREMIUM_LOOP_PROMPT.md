# Circuit Builder continuous premium-hardening prompt

This is the canonical reusable prompt for repeatedly improving Circuit Builder across future ChatGPT sessions.

It deliberately wraps and extends the existing feature-specific prompt rather than replacing solved requirements.

---

# CONTINUE CIRCUIT BUILDER — CONTINUOUS PREMIUM HARDENING LOOP

Repository:
`william2535/FIRE-ZONE-PLAN-APP`

## FIRST ACTION — ALWAYS DO THIS

Read, in this order:

1. `docs/CIRCUIT_BUILDER_CONTINUITY.md`
2. `docs/CIRCUIT_BUILDER_NEXT_PROMPT.md`
3. this file: `docs/CIRCUIT_BUILDER_PREMIUM_LOOP_PROMPT.md`

Then inspect current `main`, recent Circuit Builder commits, open/merged PRs, current regression tests, deployed version and latest successful/failed workflow runs.

Treat the continuity brief as the source of truth for what is already solved.

Do NOT restart completed work.

Do NOT assume the last chat finished cleanly.

If the previous run stopped halfway through something, continue from the exact recorded branch/commit/test state.

If this session is interrupted or must stop, update `docs/CIRCUIT_BUILDER_CONTINUITY.md` BEFORE finishing with:

- current branch;
- latest commit;
- exact change already completed;
- tests passed;
- tests failed;
- failure cause if known;
- temporary diagnostics still present;
- next exact command/action;
- unresolved product/UX question, if any.

The next session must be able to resume without guessing.

---

# PRIMARY PRINCIPLE

Do not work like this:

`bug -> patch -> green test -> stop`

Work like this:

`baseline -> attack -> find weakness -> reproduce -> fix -> add permanent regression -> compare -> full suite -> fresh-eyes audit -> find next weakness -> repeat`

A requested feature or bug fix is only the START of the pass.

After the requested work is stable, continue looking for closely related defects, rough edges, confusing interactions, visual problems, state inconsistencies, geometry weaknesses and performance problems.

The objective is for Circuit Builder to become progressively harder to break every time this prompt is run.

Every meaningful real or synthetic failure discovered should ideally become one of:

- a permanent deterministic regression test;
- a route-quality metric/budget;
- a validation rule;
- a UI-state invariant;
- a documented known limitation if it cannot safely be fixed yet.

Do not merely fix the screenshot in front of you.

Improve the SYSTEM that allowed it.

---

# CONTINUOUS ITERATION RULE

Within each development session, work in repeated improvement cycles.

Do not stop after the first successful CI run if there is still useful test/audit time available.

Run at least the following sequence:

## Cycle A — Requested work

Implement the currently recorded highest-priority user bug/features from the continuity brief and `CIRCUIT_BUILDER_NEXT_PROMPT.md`.

For the present generation this includes the transient detector-capture long-leg bug and the manual route-edit / Bridge / cleanup work unless the continuity brief records them as complete.

## Cycle B — Extreme routing abuse

Attack the newly changed routing/editor behaviour with adversarial deterministic traces and real browser interaction.

Fix genuine weaknesses found and convert them into tests.

## Cycle C — Whole-screen fresh-eyes audit

Ignore the implementation you just wrote and behave like a new user trying to break Circuit Builder.

Inspect the whole Circuit Builder workflow, not only the changed function.

## Cycle D — Premium polish pass

Look for things that are not technically broken but make the app feel cheaper, less predictable, slower or less coherent than it should.

Examples:

- awkward touch target;
- unclear selected state;
- abrupt geometry jump;
- button wrapping badly;
- stale hint text;
- inconsistent spacing;
- unnecessary modal;
- route colour ambiguity;
- ugly micro-corner;
- controls covering the drawing;
- completion state that appears late;
- destructive action with poor feedback;
- animation that feels laggy;
- desktop behaviour that works but tablet behaviour feels cramped.

Make sensible improvements where they are low-risk and closely related to the current work.

## Cycle E — Re-attack after the fixes

Replay the SAME deterministic traces from before the changes and compare results.

Then add fresh adversarial traces designed specifically around whatever you just changed.

Repeat cycles B-E while new material defects are still being found.

A good stopping condition for a session is:

- requested work complete;
- no known critical/high routing corruption remains;
- full regression suite green;
- Android build green;
- WebKit/Safari-engine checks green where practical;
- at least TWO consecutive fresh-eyes/extreme-stress passes find no new material defect requiring code changes;
- remaining findings are documented as low-risk polish/backlog rather than silently ignored.

If tools/session limits stop the run before that point, record the exact continuation point in the continuity brief instead of pretending the pass is complete.

---

# EXTREME STRESS TEST MATRIX

Do not rely on neat Playwright mouse movement.

Use deterministic recorded/generated traces with fixed seeds so the same abuse can be replayed release after release.

Maintain at least these classes:

1. clean/slow;
2. realistic rough;
3. abusive stress;
4. sparse high-speed swipe;
5. capture-then-overshoot;
6. zig-zag/reversal abuse;
7. long sweeping multi-device pass;
8. near-miss/undershoot;
9. dense-device route;
10. long-session edit/undo abuse.

Where randomness helps generate variation, use fixed seeds and print/store the seed with failures.

Suggested permanent deterministic seeds can include values such as `1337`, `424242` and `9001`, but preserve any existing project seeds rather than replacing them unnecessarily.

Every important trace should be replayable.

---

# VIEWPORT / DEVICE MATRIX

Exercise at minimum:

- small iPhone portrait;
- larger iPhone portrait;
- typical Android portrait;
- small tablet portrait;
- tablet landscape;
- desktop landscape.

Also test geometry at:

- Fit / 1x;
- modest zoom;
- high zoom;
- zoom changed mid-operation;
- viewport resize/rotation mid-operation.

Do not treat a desktop pass as evidence that touch layout is good.

---

# POINTER / GESTURE ABUSE

Repeatedly test:

- very slow deliberate drag;
- very fast swipe;
- sparse pointer events;
- uneven event timing;
- diagonal motion;
- shaky hand noise;
- repeated small reversals;
- large reversal;
- overshoot after detector capture;
- undershoot then correction;
- abrupt 90-degree change;
- repeated direction changes;
- passing multiple devices in one pointer segment;
- thumb leaving and re-entering target area;
- pointer cancel;
- second finger arriving unexpectedly;
- pinch beginning during/after routing;
- third pointer where applicable;
- browser/app blur;
- visibility change;
- viewport resize;
- switching circuit mid-state;
- leaving Circuit Builder and reopening.

The routing engine must behave safely even when human input is ugly.

---

# DEVICE CAPTURE / NEW-LEG TRANSITION TORTURE TEST

The real tablet bug proves this transition deserves its own permanent torture suite.

After every captured device, deliberately test:

- zero additional movement;
- 1-3 px movement;
- immediate 100+ px movement;
- same event/sample batch continuing far past the detector;
- immediate reversal;
- diagonal departure;
- departure parallel with old leg;
- fast departure toward another device;
- capture two devices rapidly;
- capture near viewport edge;
- capture while zoomed;
- capture immediately before resize/blur.

Assert that:

- the new live leg starts from the captured device;
- stale pre-capture coordinates do not become the new origin;
- preview length is justified by actual post-capture movement;
- saved geometry remains deterministic;
- no giant border/rubber-band line appears;
- device capture remains reliable.

Any future recurrence becomes a permanent release blocker.

---

# MANUAL EDITOR TORTURE TEST

Once the manual route editor exists, repeatedly attack it with:

- cable -> cable;
- cable -> device;
- device -> cable;
- device -> device;
- draw replacement before deleting old section;
- delete old section before repairing;
- delete nearest detector accidentally — this must NOT delete the detector;
- edit first leg;
- edit middle leg;
- edit final leg;
- edit addressable return;
- edit around FAP;
- edit near another colour;
- edit parallel to another colour;
- edit across another cable with Bridge OFF;
- repeat with Bridge ON;
- toggle Bridge rapidly;
- exit Edit with Bridge ON;
- reopen and verify safe default;
- low cleanup strength;
- default cleanup strength;
- maximum cleanup strength;
- extremely shaky pencil;
- very fast pencil;
- diagonal pencil;
- tiny pencil stroke;
- very long pencil stroke;
- 50+ repeated edit/delete/undo/redo operations;
- save/reload during an open edit;
- switch zone while edit is open;
- viewport resize mid-pencil;
- Fit mid-edit;
- zoom mid-edit.

The editor must never silently leave corrupt topology.

---

# LONG-SESSION / FATIGUE TEST

Add or maintain at least one deterministic long-session simulation.

It should perform many operations in one session, for example:

- build several circuits;
- route dozens/hundreds of devices;
- switch circuits repeatedly;
- zoom/fit repeatedly;
- edit/delete sections repeatedly;
- toggle Bridge repeatedly;
- undo/redo repeatedly;
- save/reload at intervals;
- generate As-Fit more than once;
- return to editing;
- regenerate As-Fit.

Watch for:

- geometry growth;
- duplicate points;
- orphan fragments;
- event-listener duplication;
- stale drag state;
- stale hover state;
- memory/performance degradation;
- progressively slower redraw;
- completion counters drifting;
- route colours becoming incorrect;
- undo history corruption;
- saved state diverging from visible state.

A feature that works once but degrades after 30 operations is not finished.

---

# DENSE / UGLY REAL-WORLD PLANS

Synthetic empty canvases are insufficient.

Use dense layouts with:

- detectors close together;
- detectors near walls;
- many 90-degree route choices;
- several coloured zones visible;
- cables running beside each other;
- intentional bridge crossing;
- FAP near another device;
- devices close to screen edges;
- long routes across a large plan;
- awkward return path.

Look for state/geometry bugs that only appear when the screen is busy.

---

# ROUTE-QUALITY METRICS

For deterministic traces, record where practical:

- raw pointer sample count;
- captured device count;
- saved route point count;
- saved segment count;
- corner count;
- very short leg count;
- immediate reversal count;
- duplicate-point count;
- zero-length segment count;
- self-intersection count;
- explicit bridge count;
- orphan fragment count;
- total route length;
- simplified-equivalent route length;
- route-length ratio;
- completion/topology validity;
- render/save/reload equivalence.

Keep historical benchmark output where useful.

Compare BEFORE and AFTER using the same trace.

Do not claim an improvement merely because one screenshot looks cleaner.

Do not tighten a metric just to look good.

Do not loosen a metric to make CI pass.

If an intentional new behaviour legitimately changes a metric, document why.

---

# REGRESSION PROMOTION RULE

Every genuine defect found during stress testing should be treated as follows:

1. isolate the smallest deterministic reproduction;
2. make the test fail on the broken implementation;
3. fix the root cause;
4. prove the new test passes;
5. run the old suite;
6. keep the new test permanently unless there is a strong reason not to.

Do not fix a stress-test failure only inside the stress script.

The application behaviour must improve.

A previously fixed bug reappearing should be considered more serious than a brand-new minor bug.

---

# PREMIUM FEEL AUDIT

After correctness, inspect how Circuit Builder FEELS.

Check:

- touch targets large enough without stealing nearby touches;
- active tool unmistakable;
- destructive tool unmistakable;
- Edit/Bridge/Route Open/Complete states visually distinct;
- no sudden unexplained geometry jumps;
- route follows finger promptly;
- committed route looks cleaner than live input;
- no stale ghost route;
- no unnecessary flashing/flickering;
- controls do not cover the exact area being edited;
- left circuit list remains understandable at tablet width;
- phone layout does not become a stack of tiny buttons;
- Fit behaves predictably;
- Undo/Redo state updates immediately;
- bridge rendering is legible without being visually huge;
- different-colour lanes remain easy to follow;
- hints are useful and disappear appropriately;
- completion feedback feels rewarding but not obstructive;
- reset/delete actions are difficult to trigger accidentally;
- disabled states explain themselves where needed;
- typography/spacing match the rest of Zone Sketch;
- no debug-looking text leaks into production UI.

Prefer small coherent refinements over adding random features.

Premium means predictable, responsive and deliberate — not simply more controls.

---

# PERFORMANCE / RESPONSIVENESS

Watch for regressions in:

- pointermove cost;
- redraw frequency;
- route simplification cost;
- hit-corridor scanning;
- dense device count;
- many saved circuits;
- edit-mode hit testing;
- bridge rendering;
- As-Fit generation.

Avoid doing expensive global topology work on every raw pointer event if it can safely happen at commit/release.

Keep live interaction responsive.

Use raw input detail for hit detection while deferring expensive cleanup/validation where practical.

---

# STATE INVARIANTS

Treat these as hard invariants unless a documented feature explicitly changes them:

- no detector silently disappears from its circuit;
- no circuit silently becomes electrically merged with another colour;
- different-colour visual adjacency does not equal topology merge;
- complete means topology actually validates;
- open/broken edit cannot masquerade as complete;
- explicit bridge is distinguishable from normal adjacency/crossing;
- Bridge OFF cannot silently save a crossing as valid;
- undo restores exact prior state;
- save/reload preserves exact valid geometry;
- As-Fit uses current edited geometry;
- finite coordinates only;
- no orphan segments after successful validation;
- no zero-length/duplicate segments after successful validation;
- current active circuit only is edited unless UI explicitly selects another one.

Add assertions for these where practical.

---

# FAILURE TRIAGE

When a test fails, classify it before changing code:

- real app defect;
- real test defect;
- stale expectation from intentional new behaviour;
- timing/resource flake;
- environment/tooling failure;
- CI packaging/delivery failure.

Do not call a real app failure flaky without evidence.

Do not weaken the regression because the implementation is inconvenient to fix.

If it is a runner/resource problem, make the runner deterministic/serial rather than lowering behavioural standards.

---

# SAFE SCOPE EXPANSION

You ARE encouraged to make additional improvements discovered through testing when they are:

- close to Circuit Builder;
- clearly beneficial;
- low/medium risk;
- testable;
- consistent with the product direction.

Examples:

- fixing a stale status label discovered while routing;
- improving touch target spacing uncovered on small iPhone;
- making Undo state correct after route deletion;
- cleaning duplicate geometry created by the new editor;
- improving lane separation when stress testing dense coloured routes.

Do NOT use the mandate as an excuse to rewrite unrelated Zone Plan/Survey features or destabilise working parts of the app.

Protect the 24/7 build and unrelated modes.

---

# VERSION / DELIVERY DISCIPLINE

For non-trivial changes:

- use a dedicated branch;
- keep commits understandable;
- run deterministic focused tests first;
- run full serial regression suite;
- run WebKit/Safari-engine coverage where practical;
- build Android;
- inspect artifacts/logs;
- use a PR;
- merge only when stable;
- verify the post-merge main workflow too.

Do not call the release complete merely because the PR workflow was green.

Verify `main` after merge.

Do not leave diagnostic workflows/scripts cluttering the repository unless they are intentionally useful permanent tooling.

---

# CONTINUITY / SELF-HANDOFF LOOP

At the end of EVERY meaningful improvement batch, update `docs/CIRCUIT_BUILDER_CONTINUITY.md`.

Do not wait until the very end of a huge session.

Record progress incrementally so an interruption loses as little as possible.

Recommended checkpoints:

- after baseline/reproduction;
- after root-cause fix;
- after manual editor milestone;
- after new stress tests;
- after full regression pass;
- after PR merge;
- after post-merge verification.

The continuity file should always answer:

1. What is currently on `main`?
2. What branch is active, if any?
3. What problem are we solving right now?
4. What has been proven?
5. What failed?
6. What is the next exact action?
7. What should NOT be redone?

This is what makes the workflow reusable across repeated ChatGPT sessions.

---

# DO NOT STOP AT “NOT BAD”

A pass is not finished simply because:

- the screenshot looks better;
- one manual test worked;
- one viewport worked;
- the requested bug is hidden;
- the feature technically exists;
- CI happened to go green once.

Continue until the interaction is robust under abuse and the surrounding UX has had a genuine polish pass.

When the extreme tests expose another weakness, treat that as the next task automatically unless it requires a product decision from the user or would dangerously expand scope.

When that weakness is fixed, replay the entire relevant test set again.

Then attack it again from another angle.

This repetitive loop is intentional.

Each run should leave Circuit Builder with:

- fewer reproducible defects;
- more permanent coverage;
- cleaner geometry;
- stronger state guarantees;
- more predictable touch behaviour;
- better mobile/tablet UX;
- a clearer continuity record than when the run began.

The goal is compounding reliability and polish over many passes.

---

# ONE-LINE USER CONTINUATION COMMAND

If the conversation is interrupted, the user can send only:

> Continue the Circuit Builder premium hardening loop from GitHub.

On receiving that instruction:

- read the three files listed at the top;
- inspect current repository/CI state;
- resume from the exact continuity checkpoint;
- finish the current task;
- then continue the stress-test -> improve -> regression -> polish loop;
- update continuity repeatedly as progress is made.

Do not ask the user to re-explain already-recorded requirements.
