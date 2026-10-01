# Circuit Builder next-pass master prompt

## Active pass — 1 October 2026: stable cable lanes and touch recovery

Starting main: `b335f81be4e64ad8ccd8fb27f818bd63ad486595` (wall-mounted MCP/panel placement). Current request is Circuit Builder reliability and neat adjacent cables of different colours.

Reproduced before editing: other-colour circuits were absent from the pairing candidates; changing paired rows created a diagonal; Done trapped valid partial circuits in Edit; cancelling a touch discarded reached devices. The new deterministic suite failed five of six baseline cases. A real 320px phone workflow also exposed a zero-length paired tail whose next extension moved the perpendicular connector into a diagonal.

Repairs: use the existing pairing engine for other-colour routes and Pencil, retain the chosen lane through wobble, step past occupied lanes, preserve orthogonal connectors even after a zero-length tail, checkpoint reached devices on cancel/lost capture, allow Done on a valid partial sequence without claiming completion, check endpoint/device continuity, pan empty space with one finger when zoomed, and give routing/edit controls 44px touch targets. Routes remain ordinary saved leg points; no circuit memberships or old routes are rewritten. Bridge still represents an actual crossing.

New coverage: `tests/circuit-lanes.cjs` and `tests/circuit-field-workflow.cjs` (320/390/412px phones, tablet portrait/landscape and desktop; routing, interruption, resume, partial Edit/Done, pan, endpoints, export, reload, project duplication, backup import, missing devices). Existing cancel stress expectation deliberately changes from discarding reached devices to preserving and resuming them. No other regression expectations are weakened. No protected-demo edits.

Validation checkpoint: syntax, protected-demo and release checks pass; seven deterministic lane/recovery cases pass. Full regression and six-layout browser run are in progress. The first browser backup failure was a fixture error (numeric zone numbers; the real model requires strings), corrected without changing import validation. Next: finish full tests, inspect exported/phone render, synchronize all mirrors, publish and verify Pages plus current CI/WebKit/Android results.


## Active pass — 27 September 2026: mobile editor interruption safety

Development branch: `project-pineapple-v058`. Starting checkpoint: `3fc08209f638d02ddfbde844706d1de39114ba2d`; current live milestone is web v0.58 / packaged Android v0.57.

Completed work from earlier passes: post-capture rubber-band fix, draft-first Pencil/Bin/Bridge/Cleanup/Done editor, real Bridge persistence, mobile/zoom gesture stress, and reconciliation with main through `37bb435`. Do not redo those implementations. The historical requirements below remain acceptance criteria.

This active pass reproduced two production defects before changing code: view/app interruption left a live editor stroke/tap armed, and an out-and-back Bin drag was mistaken for a deliberate deletion tap. The baseline input-state regression failed 3 of 4 assertions. Both are fixed locally (4/4 pass), with explicit lost-pointer-capture recovery and mode-specific hints added. Earlier staged replacements are preserved.

Second audit: reproduced and fixed a stale LOOP CLOSED counter while the editor has an open route; it now follows EDITING / ROUTE OPEN / REPLACEMENT READY. Local production-function regression is 5/5. First browser run on `a2a4b5c8` passed the interruptions and 30 history cycles but failed reload because the synthetic fixture had no named project; the fixture now uses the real project activation path. Prior editor/Bridge/mobile/zoom tests remained green.

Third audit: on `46ca44a6`, the editor/routing/capture lanes and new WebKit interruption/reload test passed. Full suite had only the pre-existing v0.58 title allow-list failure. Reproduced two further lifecycle defects: switching circuits retained the old editor session, and a confirmed survey rebuild retained obsolete editDraft/bridges. Both fixed; local production-function checks 7/7. Circuit list completion ticks now respect editing status. Browser regression extended to switch away/back and rebuild.

Validation pending: new Chromium/WebKit interruption/30-cycle/save-reload/As-Fit regression, full serial suite (now including all v0.58 editor gates), Android build, visual audit and second fresh-eyes pass. No new public milestone yet. If interrupted, inspect current branch CI and fix failures before promotion; do not describe this as the premium loop being complete.

Continuation rule confirmed by Will: keep making useful improvements within the session after the first green CI run, and update this brief, NEXT_PROMPT, START_HERE and the checkpoint at meaningful steps. Do not end a pass merely by recording an unspecified future task.


Use this prompt to resume the next Circuit Builder development pass in a fresh chat or after an interrupted response.

---

CONTINUE CIRCUIT BUILDER — RED ROUTING BUG + MANUAL EDIT / BRIDGE PASS

Repository:
`william2535/FIRE-ZONE-PLAN-APP`

FIRST ACTION — DO NOT SKIP:

Read `docs/CIRCUIT_BUILDER_CONTINUITY.md` first.

Then inspect current `main`, recent Circuit Builder commits, current routing/editor tests and deployed version. Treat the continuity brief as the source of truth and do not restart solved work.

If this run is interrupted or you are about to stop, UPDATE `docs/CIRCUIT_BUILDER_CONTINUITY.md` with the exact last completed step, current branch/commit, test status, failures, unresolved issue and next action before replying.

Do not treat this as a narrow patch. The result should feel like the next polished generation of Circuit Builder.

## JOB 1 — REPRODUCE AND FIX THE REAL TABLET RED-BUG FIRST

Observed real-world symptom:

When a newly captured detector starts the next outgoing route, a very long temporary cable leg can shoot outward and follow the thumb, almost like a border/rubber-band line. It happens fast and appears to settle/place when the user moves away or the next routing state commits.

Do not hide this by clipping line length or simply changing a threshold.

Reproduce it first using automated aggressive pointer traces where practical.

Specifically investigate the transition immediately AFTER DEVICE CAPTURE:

- stale `lastPointer`;
- stale `routeInput`;
- stale `intentPoint`;
- first post-capture render tail;
- capture guard handoff;
- pending/committed corner state;
- route-axis reset;
- old pre-capture coordinates leaking into the new leg;
- sparse events immediately after a device hit;
- one pointer segment capturing a detector and then moving far beyond it in the same event/sample batch.

Create a deterministic regression that proves the first live preview after capture stays anchored to the newly captured device and cannot generate a huge provisional leg without deliberate movement.

Test this at:

- small iPhone portrait;
- large iPhone portrait;
- typical Android portrait;
- small tablet;
- tablet/desktop landscape;
- fit view;
- zoomed in;
- fast swipe;
- rough swipe;
- overshoot/reversal;
- several devices passed rapidly.

Preserve v0.57 Smart Route behaviour, swept hit detection, raw/rendered geometry separation, state machine, return magnet and current successful aggressive-touch characteristics.

## JOB 2 — ADD PROFESSIONAL LOCAL ROUTE EDITING

The engineer must be able to fix one ugly corner/dogleg without rebuilding the whole circuit.

The interaction should feel like the existing Zone Plan edit/erase tools, not CAD control-point editing.

### UI

Expose Edit in BOTH places:

1. pencil/edit control beside each zone/circuit in the left Circuit Builder list;
2. Edit control beside the canvas `- / Fit / +` controls for the current circuit.

In Edit mode also expose:

- Pencil;
- Bin/Delete;
- Undo;
- Redo;
- Done / Validate;
- Bridge Mode circular toggle;
- compact cleaning-options dropdown with a bend-cleaning slider.

Keep all controls usable on phone portrait and tablet landscape without covering important cable/device geometry.

## PENCIL BEHAVIOUR

The pencil can start or finish on ANY existing cable section or device.

Support:

- cable -> cable;
- device -> cable;
- cable -> device;
- device -> device.

Workflow:

1. Enter Edit.
2. Touch cable or device.
3. Draw replacement route.
4. While finger is DOWN, keep the live line immediate and fairly literal/rough so it tracks the thumb responsively and keeps the satisfying visual feedback.
5. Use Smart Grid / orthogonal routing principles for final geometry.
6. Finish on cable or device.
7. On finger release, apply the configured cleanup pass.
8. Keep the new route.
9. Use Bin to remove the old ugly corner/section.
10. Press Done.
11. Validate topology before returning the circuit to COMPLETE.

Do not continuously over-smooth the live pencil stroke. Cleanup belongs primarily at commit/release.

## BEND CLEANING SLIDER

Add a dropdown/options control at the top of Edit mode containing a slider controlling post-release cleanup strength.

Default behaviour should be conservative, roughly targeting repeated 2+ unnecessary small bends/stair-steps in a row rather than rewriting every intentional corner.

Low setting:
- preserve more intentional detail.

Default:
- remove obvious repeated micro-doglegs / stair-stepping.

High setting:
- simplify more aggressively while preserving anchors, devices, topology and intended route direction.

Requirements:

- deterministic;
- endpoints never drift away from chosen cable/device anchors;
- no zero-length segments;
- no duplicate points;
- no accidental immediate reversals;
- no simplification through devices;
- no simplification through invalid obstacles/crossings;
- no topology change merely to reduce point count.

Live stroke remains rough/responsive; cleanup happens when the stroke is committed.

## BIN / DELETE TOOL

Model the interaction on Zone Plan erase behaviour, but Circuit Builder deletion must be local cable surgery.

One intentional tap should remove ONE cable segment/local section.

Do NOT:

- delete a detector;
- delete the entire detector-to-detector leg;
- delete the whole circuit.

Use a forgiving but bounded cable hit target.

Prefer cable over nearby device because this tool edits route geometry only.

Push undo state before deletion.

Where useful, highlight the selected cable section before/during deletion so the destructive target is obvious.

Allow repeated local deletion after the replacement route has been drawn.

## EDITING · ROUTE OPEN STATE

Deletion may temporarily break the circuit.

When broken:

- remove/withhold COMPLETE;
- clearly show `EDITING · ROUTE OPEN`;
- disable valid As-Fit completion for that circuit;
- preserve device assignments/circuit identity;
- let the user continue drawing repairs;
- Done must reject invalid/open topology.

When repaired and validated, Done restores normal completed state.

## BRIDGE MODE

Add a compact circular Bridge Mode toggle at the side of the canvas/edit controls.

Default OFF.

Bridge OFF:
- retain normal collision/no-crossing behaviour.

Bridge ON:
- allow the active pencil route to intentionally cross existing cable.

Rules:

- same behaviour for conventional and addressable modes;
- active state visually unmistakable;
- crossing intent stored explicitly;
- accidental crossing with Bridge OFF must never silently become a bridge;
- bridge state should not remain active unexpectedly after leaving/resetting edit mode unless there is a very deliberate UX reason.

For rendering, prefer a small clear cable-jump/bridge hump at the crossing if readable at mobile/tablet zoom. Do not represent an intentional bridge as two ambiguous plain intersecting lines.

Bridge crossings must render consistently in Circuit Builder and As-Fit and survive save/reload.

## DIFFERENT-COLOUR CABLES MAY RUN TOGETHER

Different zone/circuit colours may magnet/snap alongside each other in parallel.

This is desirable.

When two different-colour routes approach each other:

- allow a parallel magnetic snap/lane behaviour;
- maintain a small visual gap so both colours remain clearly distinguishable;
- adjacency is NOT a crossing;
- adjacency must NOT electrically/topologically merge the circuits;
- editing one colour must not alter the other;
- only use Bridge Mode when actually crossing through/over another route, not merely running beside it.

Extend the existing paired/twin-cable visual philosophy rather than overlapping two strokes exactly.

## UNDO / REDO

Undo and Redo must be directly available in Edit mode and cover:

- pencil commit;
- post-release cleanup result;
- segment deletion;
- bridge geometry commits;
- repeated edit/delete cycles;
- restoration of completion / `EDITING · ROUTE OPEN` state.

Undo should restore exact prior topology.

## DONE / VALIDATE

Done must explicitly validate before restoring COMPLETE.

Check at minimum:

- all assigned devices are still connected correctly;
- FAP relationship is valid;
- conventional/addressable completion rules remain valid;
- no orphan cable fragments;
- no duplicate/zero-length segments;
- no unintended normal-mode crossings;
- explicit bridges are valid and represented correctly;
- stored coordinates finite;
- saved/reloaded geometry identical;
- As-Fit receives edited geometry, not stale pre-edit geometry.

If invalid, remain in `EDITING · ROUTE OPEN` and state what still needs repair.

## REQUIRED DETERMINISTIC STRESS TESTS

Do not test one happy-path example.

Add permanent regressions for at least:

### Red transient-leg bug
- detector captured then almost no movement;
- detector captured then immediate fast movement;
- capture + overshoot + reversal;
- several rapid captures;
- sparse pointer sampling;
- first preview frame anchored at the new device;
- no stale-coordinate giant provisional segment.

### Manual route editing
- replace simple 90-degree corner;
- replace ugly multi-step dogleg;
- draw replacement before deleting old route;
- cable -> cable;
- device -> cable;
- cable -> device;
- device -> device;
- delete exactly one segment;
- delete near detector;
- edit FAP/first leg;
- edit last leg;
- addressable return edit;
- conventional edit;
- addressable edit;
- temporary `EDITING · ROUTE OPEN` state;
- Done rejects open route;
- repair then Done restores complete;
- shaky pencil;
- very fast pencil swipe;
- overshoot;
- undershoot;
- repeated direction changes;
- diagonal finger motion;
- sparse events;
- 1x;
- high zoom;
- zoom -> Fit while editing;
- viewport resize/rotation;
- phone portrait;
- small tablet;
- landscape;
- Undo;
- Redo;
- repeated draw/delete cycles;
- save/reload;
- reopen edited circuit;
- As-Fit generation from edited circuit.

### Cleanup slider
- live stroke not aggressively rewritten while finger is down;
- low/default/high settings deterministic;
- progressively stronger simplification;
- anchors preserved;
- topology preserved;
- device hits preserved;
- no new crossing/orphan introduced.

### Bridge Mode
- OFF blocks/avoids crossing conventional;
- OFF blocks/avoids crossing addressable;
- ON permits explicit bridge conventional;
- ON permits explicit bridge addressable;
- bridge survives save/reload;
- bridge appears correctly in As-Fit;
- editing/deleting around bridge stays valid;
- bridge mode does not leak unexpectedly into future normal edits.

### Different-colour adjacent cable
- parallel snap beside different colour;
- visible lane gap at normal zoom;
- visible lane gap at high zoom;
- circuits remain topologically independent;
- edit one colour without touching the other;
- distinguish parallel adjacency from real crossing;
- dense multi-colour routes remain readable.

## MEASURE ROUTE QUALITY

Where practical record before/after metrics:

- route points;
- segments;
- corners;
- tiny legs;
- immediate reversals;
- self-intersections;
- bridge crossings;
- orphan fragments;
- devices connected;
- total route length versus simplified equivalent;
- completion validity.

Do not weaken existing regression thresholds merely to obtain green CI.

## FRESH-EYES AUDIT AFTER THE REQUESTED WORK

Once the red bug and editor work, audit the entire Circuit Builder again rather than stopping.

Actively inspect/test:

- Circuit Builder home;
- left circuit/zone list;
- zone switching;
- pencil controls;
- canvas edit controls;
- addressable device highlighting;
- conventional Zone Challenge;
- completed circuits;
- incomplete circuits;
- editing-open circuits;
- Undo/Redo;
- Reset;
- zoom controls;
- Fit;
- pinch where practical;
- sound/progress UI;
- completion card;
- switching circuits mid-edit;
- route persistence;
- stale survey invalidation;
- circuit deletion;
- As-Fit generation;
- As-Fit export;
- phone portrait;
- tablet landscape;
- desktop landscape;
- dense multi-colour routes;
- bridge crossings;
- cleanup dropdown/slider.

Look specifically for:

- giant transient live legs after capture;
- controls obscuring routes;
- stale COMPLETE ticks;
- wrong colours;
- inactive circuit accidentally edited;
- route hit areas too aggressive/too small;
- geometry changing after redraw;
- state lost after reload;
- accidental bridge persistence;
- adjacent coloured routes collapsing visually;
- old route still influencing newly edited geometry;
- route corruption after many edit/undo cycles.

## DELIVERY RULES

For this pass:

- use a dedicated branch;
- reproduce before fixing;
- add deterministic regressions;
- run complete serial regression suite;
- run WebKit/Safari-engine tests where practical;
- build Android;
- inspect any failure rather than rerunning until green;
- merge only when stable;
- do not weaken existing tests;
- preserve the protected 24/7 build.

Before finishing, update `docs/CIRCUIT_BUILDER_CONTINUITY.md` with:

- version/commit;
- exact fix for the red bug;
- manual editor architecture;
- bridge behaviour;
- cleanup-slider behaviour;
- tests added;
- test results;
- anything still unresolved;
- next recommended action.

The goal is not merely that the editor technically works.

The finished Circuit Builder should let an engineer route aggressively, get immediate satisfying feedback, then tidy one imperfect local section in seconds without rebuilding the circuit or fighting the interface.
