# Project Pineapple v0.58 worklog

## Active branch

`project-pineapple-v058`

## First reproduced defect — post-capture rubber-band leg

Real tablet report: after a detector is captured during a continuous route, the next live leg can shoot a long distance away and follow the thumb before settling.

Deterministic reproduction added in `tests/circuit-capture-transition-v058.cjs` and promoted into the permanent serial regression list.

Broken v0.57 measurement on small-tablet replay:

- field-grid step: **15.78 px**
- actual new thumb travel after capture: about **12 px**
- generated live tail: **126.27 px**
- state after the jump: `routing-normal`

This proves the issue is a raw-input -> drawn-geometry handoff defect, not merely excessive saved-route corner noise.

## Root cause

Swept corridor hit detection correctly captures a detector even when a sparse/fast raw pointer sample has already travelled well beyond it. v0.57 resets the saved geometry to the detector centre but then feeds the absolute overshot raw pointer coordinate into the next-leg geometry engine. The pre-capture overshoot is therefore incorrectly interpreted as movement belonging to the new leg.

## First structural fix and why it was rejected

Generated app commit `862b7d70fa505767b33574b9979284721fa458e4` used a detector-relative geometry offset for the whole following leg.

Focused capture-transition result:

- tablet false tail: **126.27 px -> 0 px** after the same tiny post-capture movement;
- iPhone false tail: **0 px**;
- swept detector capture remained intact.

However the wider aggressive-touch gate correctly rejected this version. Keeping the offset for the whole leg distorted later route geometry: the noisy 10-case replay produced **162 corners and 48 self-intersections**, violating existing v0.57 quality gates.

The regression was treated as a real application defect, not as a flaky/obsolete test; thresholds were not weakened.

## Refined structural fix currently generated

Generated app commit: `10f5a3b0e155e85794528e411df8649777a4fccf`.

Instead of keeping a fixed offset for an entire leg, v0.58 now uses a **bounded virtual pointer** immediately after detector capture:

- raw coordinates remain untouched for swept device detection;
- the virtual drawn pointer starts at the detector centre;
- only actual raw movement after capture advances it;
- it catches back up toward the physical thumb at a bounded rate based on new raw travel;
- once caught up, ordinary v0.57 geometry resumes with no persistent offset;
- `departing-device` remains an explicit transition state;
- there is still no arbitrary maximum-leg clipping and no reduced hit corridor.

This is intended to remove the rubber-band jump without shifting the rest of the next cable leg.

## Current validation gate

A normal GitHub-originated checkpoint commit now triggers both:

1. `Pineapple v0.58 capture transition` — the dedicated tablet/iPhone reproduction;
2. `Pineapple v0.58 routing compatibility` — v0.57 routing-state, aggressive-touch, hardening, return-magnet and v0.58 capture tests.

Do not continue to the manual editor until both the dedicated transition test and the existing route-quality gates accept the refined transition.

After they pass:

1. update the main continuity brief with the measured before/after and rejected first approach;
2. continue Project Pineapple into the manual Pencil/Bin/Bridge/cleanup editor;
3. preserve the new transition regression permanently;
4. later run the full serial suite, WebKit/Safari-engine coverage and Android build before PR merge.
