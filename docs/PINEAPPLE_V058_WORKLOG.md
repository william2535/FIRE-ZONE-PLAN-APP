# Project Pineapple v0.58 worklog

## Active branch

`project-pineapple-v058`

## First reproduced defect — post-capture rubber-band leg

Real tablet report: after a detector is captured during a continuous route, the next live leg can shoot a long distance away and follow the thumb before settling.

Deterministic reproduction added in `tests/circuit-capture-transition-v058.cjs`.

Broken v0.57 measurement on small-tablet replay:

- field-grid step: **15.78 px**
- actual new thumb travel after capture: about **12 px**
- generated live tail: **126.27 px**
- state after the jump: `routing-normal`

This proves the issue is a raw-input -> drawn-geometry handoff defect, not merely excessive saved-route corner noise.

## Root cause

Swept corridor hit detection correctly captures a detector even when a sparse/fast raw pointer sample has already travelled well beyond it. v0.57 resets the saved geometry to the detector centre but then feeds the absolute overshot raw pointer coordinate into the next-leg geometry engine. The pre-capture overshoot is therefore incorrectly interpreted as movement belonging to the new leg.

## Structural fix currently on branch

Generated app commit: `862b7d70fa505767b33574b9979284721fa458e4`.

- raw pointer coordinates remain untouched for swept device detection;
- each detector capture records a detector-relative geometry offset against the raw pointer position at capture;
- the next drawn leg begins at the captured detector and advances from **post-capture raw movement**, rather than inheriting pre-capture overshoot;
- a small `departing-device` state separates device capture from ordinary routing;
- no maximum-line-length clipping or hit-corridor weakening was used;
- all four app HTML copies are generated from the same patched source.

## Immediate validation gate

Re-run the deterministic capture-transition test on tablet and iPhone. It must show the post-capture live tail remaining locally anchored after tiny movement, while later deliberate movement still extends the route and all existing swept-hit behaviour remains intact.

After that:

1. promote the new regression into `tests/run-regressions.cjs`;
2. run v0.57 aggressive-touch/state/hardening compatibility gates;
3. update the main continuity brief;
4. continue Project Pineapple into the manual Pencil/Bin/Bridge/cleanup editor rather than stopping at this one fix.
