# Circuit Builder continuous CAD-parity loop

This is the highest-level reusable instruction for future development sessions.

Use this when the goal is not merely to fix the current bug, but to keep pushing Zone Sketch toward a premium local fire-alarm CAD replacement for ordinary site As-Fitted work.

---

# CONTINUE ZONE SKETCH / CIRCUIT BUILDER — CAD-PARITY PREMIUM LOOP

Repository:
`william2535/FIRE-ZONE-PLAN-APP`

## FIRST ACTION — ALWAYS RECOVER CONTEXT

Read these files in order:

1. `docs/CIRCUIT_BUILDER_CONTINUITY.md`
2. `docs/CIRCUIT_BUILDER_NEXT_PROMPT.md`
3. `docs/CIRCUIT_BUILDER_PREMIUM_LOOP_PROMPT.md`
4. `docs/AS_FIT_CAD_REFERENCE_RULES.md`
5. this file

Then inspect current `main`, recent commits/PRs, latest test suite, current deployed version and workflow status.

Do not redo solved work.

If a prior session stopped halfway through something, resume from the exact recorded branch/commit/test state.

Before any long tool run that could be interrupted, update the continuity brief when useful so progress is not lost.

---

# PRODUCT NORTH STAR

The target is:

> A competent fire-alarm engineer should be able to walk a site with a phone/tablet and locally produce a professional As-Fitted drawing that is clear enough to rival a careful desktop CAD handover drawing for ordinary jobs — without sending rough marked-up plans back to the office for redrawing.

Do not copy another company's artwork or proprietary template.

Instead, study professional fire-alarm As-Fitted drawings and extract the engineering-document rules that make them clear, traceable and professional.

The field workflow should be dramatically faster than desktop CAD even if the export looks similarly deliberate.

---

# THIS IS A CONTINUOUS LOOP, NOT A FEATURE CHECKLIST

Do not work as:

`requested bug -> patch -> green CI -> stop`

Work as:

`recover -> baseline -> external reference study -> attack -> reproduce -> fix -> regression -> CAD-quality audit -> field-speed audit -> whole-app audit -> re-attack -> repeat`

After requested work is complete, continue finding the next material weakness while useful session/tool budget remains.

Every genuine defect should ideally become a permanent regression.

Every genuinely useful CAD convention adopted should become either:

- a rendering rule;
- a data-model rule;
- a validation rule;
- an export rule;
- a field-speed rule;
- a benchmark acceptance check.

---

# EXTERNAL REFERENCE MINING — REQUIRED ON SUBSTANTIAL PASSES

When web research is available, actively review current public examples rather than designing only from memory.

Search for and inspect a mix of:

- UK fire-alarm As-Fitted drawings;
- addressable loop layouts;
- conventional system layouts;
- school/office/hotel/industrial examples;
- dense multi-circuit drawings;
- multi-floor/riser drawings;
- professional fire-alarm CAD services;
- modern fire-alarm design software;
- public handover/system-layout examples.

Where possible, inspect actual images/PDF pages, not just marketing text.

For each useful reference, ask:

1. What makes the drawing immediately understandable?
2. How are cable routes shown?
3. How are multiple cables shown when they share a path?
4. How are devices labelled?
5. How are loop/address references shown?
6. How are isolators, PSUs, repeaters, junctions and remote indicators represented?
7. How is a cable crossing distinguished from a connection?
8. How are floor/riser transitions represented?
9. How is the legend organised?
10. What is in the title block?
11. What information is repeated unnecessarily?
12. What could Zone Sketch automate better than CAD?
13. What would be annoying to enter manually on site?
14. What can be inferred/generated from existing structured data?

Extract general conventions only.

Do not reproduce logos, proprietary title blocks or copyrighted drawings inside the app.

Record useful generic findings and sources in `docs/AS_FIT_CAD_REFERENCE_RULES.md`.

If a claimed standards requirement cannot be verified from an authoritative/current source, label it as an industry convention or product preference rather than a standard requirement.

---

# CAD-QUALITY OUTPUT AUDIT

On each significant pass, generate or inspect at least one representative As-Fit and judge it as an engineering drawing, not merely an app screenshot.

Check:

- base plan hierarchy;
- line weights;
- circuit readability;
- route cleanliness;
- actual route fidelity;
- device order readability;
- device symbol consistency;
- loop/address references;
- label collisions;
- route/text collisions;
- route/device-entry appearance;
- parallel cable lane spacing;
- different-colour route separation;
- bridge/crossing clarity;
- continuation/off-sheet/riser clarity;
- panel/repeater/PSU visibility;
- isolator/junction visibility;
- legend completeness;
- unused legend clutter;
- title block completeness;
- project/floor/drawing naming;
- revision information;
- export sharpness;
- print readability;
- consistency across floors.

Ask: **Would this look normal and credible if it arrived in a fire-alarm handover pack from a CAD department?**

If not, identify why and improve the system rather than hand-polishing one example.

---

# FIELD-SPEED AUDIT

CAD parity is useless if the engineer becomes slow.

For every new feature, ask:

- how many taps does this add?
- can the same result be inferred?
- can a default be remembered?
- can metadata auto-increment?
- can a favourite be one tap away?
- can a modal be avoided?
- can the action happen while walking the site?
- can it work comfortably with one thumb?
- can it be undone instantly?
- can it work offline?

Measure representative workflows where practical.

Benchmark examples:

- place 20 common devices;
- build a 20-device addressable loop;
- correct one ugly cable dogleg;
- add loop/address references;
- add an isolator/junction;
- create a cross-floor continuation;
- produce a finished As-Fit from an already surveyed floor;
- revise an existing drawing after one site alteration.

Track gesture/tap count and elapsed scripted interaction time where meaningful.

Prefer automation that removes repetitive office-CAD work.

---

# AUTOMATION OPPORTUNITIES TO KEEP INVESTIGATING

Without blindly adding features, repeatedly assess whether the structured project model can automatically provide:

- loop/address labels;
- sequential address suggestions;
- duplicate-address warnings;
- device reference numbering;
- dynamic used-symbol legend;
- circuit key;
- cable type/size legend notes;
- title block;
- project/floor metadata;
- device schedule;
- circuit schedule;
- device totals;
- revision information;
- cross-floor continuation labels;
- route lane packing;
- smart label positions;
- automatic label collision avoidance;
- drawing frame/paper orientation;
- As-Fit status;
- validation report;
- export filename.

Do not ask the engineer to type information the app already knows.

---

# VECTOR / PRINT QUALITY TARGET

Do not accept 'large PNG looks okay' as the permanent ceiling.

Continue investigating vector-first export where practical:

- SVG;
- vector PDF;
- later DXF/interchange if useful.

Acceptance goals:

- cable lines remain crisp when zoomed;
- text remains sharp;
- symbols remain clean;
- title block looks engineered;
- print output is professional;
- no screen-resolution artefacts;
- the exported geometry exactly matches the validated circuit model.

Keep raster export as a useful fallback, not necessarily the final premium format.

---

# BENCHMARK PROJECT BANK

Maintain deterministic synthetic projects representing real-world jobs.

At minimum aim for:

1. small conventional office;
2. school/multi-block addressable;
3. warehouse/industrial;
4. dense corridor/hotel;
5. multi-floor/riser loop;
6. messy retrofit imported plan.

Every major As-Fit/export pass should use several of these, not one pretty demo.

Capture measurable checks such as:

- label overlap count;
- route overlap count;
- unresolved crossing count;
- tiny-leg count;
- orphan fragment count;
- duplicate address count;
- missing legend entry count;
- missing title field count;
- device count/order integrity;
- export/reload equivalence;
- number of manual cleanup operations required.

Where screenshot comparison is useful, keep deterministic viewport/export settings so regressions are visible.

---

# EXTREME ROUTING / EDITING STRESS

All previous aggressive-touch and premium-loop requirements remain active.

Continue testing:

- clean/slow;
- rough realistic;
- abusive;
- sparse high-speed;
- overshoot;
- undershoot;
- reversals;
- diagonal sweeps;
- multi-device swipes;
- detector-capture transition;
- pointer cancel;
- second/third pointer;
- pinch;
- zoom/fit mid-operation;
- resize/rotation;
- app blur/reopen;
- long sessions;
- manual edit/delete;
- Bridge mode;
- different-colour lane adjacency;
- save/reload;
- As-Fit regeneration.

Do not reduce route-quality thresholds merely to make new features pass.

---

# AS-FIT DATA INTEGRITY

Treat the project as structured engineering data, not a picture.

Hard invariants should increasingly include:

- every visible final circuit belongs to one explicit circuit/loop;
- device assignment is stable;
- route order is stable;
- visible adjacency never merges circuits;
- explicit bridges are distinguishable from joins;
- all complete circuits validate;
- edited routes are the routes exported;
- moved survey devices invalidate/rebuild stale route geometry safely;
- cross-floor continuation is traceable;
- label metadata matches device metadata;
- legend matches visible content;
- saved and reloaded project reproduces the same engineering drawing.

---

# LOCAL / OFFLINE-FIRST RULE

Core field workflow should continue to work locally without a network once the app/project/background is available.

The engineer should be able to:

- open/create project;
- place devices;
- route circuits;
- edit circuits;
- validate;
- save/autosave;
- generate As-Fit;
- export final file;

without requiring cloud rendering.

Optional cloud features may exist later, but must not undermine core offline site use.

---

# WHOLE PRODUCT FRESH-EYES AUDIT

Do not limit the audit to Circuit Builder if the target workflow crosses Survey -> Circuit Builder -> As-Fit.

Test the whole engineer journey:

1. create/open project;
2. import/trace plan;
3. create/select floor;
4. place devices in Survey;
5. edit/move devices;
6. enter Circuit Builder;
7. build circuit;
8. correct route manually;
9. add bridge/parallel lane where needed;
10. validate;
11. generate As-Fit;
12. inspect labels/legend/title block;
13. export;
14. close/reopen;
15. modify one device/route;
16. regenerate/export revision.

Look for friction between modes, stale data, duplicate entry and visual inconsistency.

---

# PREMIUM SELF-IMPROVEMENT LOOP

After the targeted task and first full green test run:

1. generate/inspect benchmark drawings;
2. compare them with current professional public references;
3. identify the biggest remaining gap in either clarity, field speed or reliability;
4. choose one low/medium-risk high-value improvement;
5. implement it;
6. add deterministic checks;
7. rerun focused + full tests;
8. repeat while material improvements continue to emerge.

Do not add random features for the sake of iteration.

Prioritise improvements that move the product toward:

- faster site capture;
- cleaner As-Fit output;
- fewer manual corrections;
- stronger data integrity;
- better offline reliability;
- easier handover/maintenance readability.

---

# STOPPING CONDITION

A strong session ends only when:

- recorded priority work is complete or precisely handed off;
- no known critical/high data or routing corruption remains;
- focused deterministic tests pass;
- full regression suite passes;
- Android build passes;
- WebKit/Safari-engine coverage passes where practical;
- representative As-Fit benchmark output has been reviewed;
- at least one field-speed/CAD-quality audit has been performed;
- two consecutive fresh-eyes/extreme passes find no new material defect requiring immediate code changes;
- continuity documentation is current.

If session/tool limits intervene first, update the continuity brief with the exact next step instead of declaring completion.

---

# CONTINUITY UPDATE REQUIREMENT

At meaningful checkpoints update `docs/CIRCUIT_BUILDER_CONTINUITY.md` with:

- current version;
- branch/commit;
- requested feature/bug status;
- new defects found by stress testing;
- root causes;
- new regressions added;
- benchmark/CAD-quality findings;
- external reference lessons adopted;
- field-speed findings;
- tests/build status;
- exact next action.

Also update `docs/AS_FIT_CAD_REFERENCE_RULES.md` when a new external reference produces a useful general rule.

The repository, not chat memory, is the persistent source of truth.

---

# ONE-LINE RESUME COMMAND

If the user says:

> **Continue the Zone Sketch CAD-parity premium loop from GitHub.**

read the files listed at the top and resume without asking them to restate existing requirements.
