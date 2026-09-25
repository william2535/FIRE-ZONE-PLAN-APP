# As-Fit CAD reference rules and field-speed target

This document is a living reference bank for the long-term Zone Sketch / Circuit Builder goal:

> An engineer should be able to walk a site with a phone/tablet, capture the final fire alarm installation extremely quickly, and locally produce an As-Fitted drawing that is visually and operationally comparable with a careful desktop CAD drawing.

This is not permission to copy another company’s proprietary drawing, logo, title block or artwork. Public examples are used to extract general engineering-document conventions and workflow ideas only.

## Evidence categories

Every rule added to the product from external research should be labelled mentally as one of:

1. **Verified requirement** — supported by an authoritative/current standard, scheme or official guidance available to the developer.
2. **Industry drawing convention** — repeatedly observed in professional UK fire-alarm As-Fitted drawings/services.
3. **Zone Sketch product preference** — chosen because it improves field speed, clarity or consistency.

Never present an industry convention or product preference as a British Standard requirement without an authoritative source.

## Initial public reference set — September 2026

### QDOS — As-Fitted Drawings
Source: https://www.qdos.biz/our-services/fire-safety-plan-services/asfitted-drawings/

Useful generic observations:

- Actual cable routes matter; a schematic showing device order alone is not enough for a proper system layout record.
- Device order and real-world cable route both need to remain understandable.
- When multiple cables run together they can be drawn separately with enough visual spacing to identify each cable.
- Drawings should show control panels, repeater panels and associated power supplies.
- Different device types should have distinct symbols and a key/legend.
- Equipment needing routine attention, such as isolators and remote indicators, should be locatable.
- Cable type, size and actual route are useful handover/fault-finding information.

### Fire Alarm CAD — As-Fitted Diagrams
Source: https://www.firealarmcad.co.uk/as-fitted-diagrams

Useful generic observations:

- Professional handover drawings commonly include control/indicating equipment, supplies, devices, isolators, junction boxes and cable routes.
- Cable sizes/types and a legend/key are normal professional drawing content.
- Company/project information is normally presented in a structured drawing frame/title area rather than scattered on the plan.
- Clear CAD redraws favour restrained base-building graphics with the fire system visually dominant.

### CADZONE — As-Fitted Drawings
Source: https://www.cadzone.co.uk/as-fitted.html

Useful generic observations:

- A professional title panel includes project/client information.
- Devices are commonly identified with loop/address information.
- Standardised symbols and a comprehensive legend make the drawing self-explanatory.
- Cable routes are explicit.
- Sound-level readings may be recorded where relevant.
- As-Fitted output is expected to be clear enough for handover, audits and future maintenance.

### FIRE3D — fire alarm design software
Source: https://www.fire3ddesign.com/

Useful product/workflow observations:

- Professional outputs can be generated automatically from structured project data rather than redrawn manually for every document.
- Device references can cross-reference an equipment/device schedule.
- Legends can be generated from drawing content.
- A single structured model can generate an engineering drawing, As-Fitted drawing, zone plan, device totals and other documents.
- Real-time coverage/design assistance demonstrates the value of keeping meaningful device metadata rather than treating symbols as decorative marks.

### Public fire-alarm layout example used in licensing documentation
Source: https://councillors.herefordshire.gov.uk/documents/s50126707/Appendix%202.pdf

Useful generic observations visible in the drawing:

- Formal title blocks commonly include drawing status, project/site, floor/title, date, scale, drawing number, revision and responsibility fields.
- A legend identifies detector/device variants and cable notation.
- Drawing status such as **AS FITTED** is visually explicit.
- Cable specification can be stated in the legend.
- Separate sheets/floors retain consistent graphic language.

## Visual target — what “CAD quality” should mean in Zone Sketch

The goal is not to imitate AutoCAD’s interface. The goal is to make the exported engineering document look as deliberate as a good CAD drawing while the field interaction remains dramatically faster.

### Base plan hierarchy

- Building/wall geometry should normally be neutral grey/black and lower visual priority than the alarm system.
- Fire-alarm devices and routes must remain immediately traceable.
- Imported raster/PDF background should support adjustable fade/opacity for working and a separate export treatment.
- Export should avoid photographic/background noise where the engineer has traced a clean plan and chooses a clean-plan output.
- Provide a clear distinction between building fabric, alarm devices, alarm routes, annotations and title/legend information.

### Route appearance

- Final cable geometry should be orthogonal/grid-clean unless a deliberate exception is explicitly recorded.
- Real route intent is more important than shortest-route aesthetics.
- Avoid micro-legs, near-zero segments, unexplained stair-stepping and accidental reversals.
- Routes should not run through device text or title/legend content.
- Device entry/exit should look intentional and consistent.
- Parallel cables must use stable lane spacing rather than being drawn exactly on top of one another.
- Different circuit colours may run in parallel with enough gap to remain independently readable.
- A true crossing must be visually distinguishable from a junction or parallel run; explicit Bridge Mode should render an unmistakable jump/bridge treatment.
- Cross-floor or off-sheet continuation should use clear continuation markers rather than lines disappearing without explanation.

### Device appearance

- Symbol size should be consistent at export scale.
- Each device type should be visually distinct without relying only on colour.
- A device may carry concise metadata such as loop/address/reference where appropriate.
- Labels should avoid covering walls, cable, nearby devices and one another.
- Dense areas should use automatic label-side selection/offset/fan-out rather than becoming unreadable.
- Panels, repeaters, PSUs, junction boxes, isolators and remote indicators should be representable as first-class device/equipment types.

### Automatic legend

Generate a legend from what is actually used on the drawing.

Possible legend content:

- device symbols used on this floor/drawing;
- circuit/loop colour or line-type meaning;
- bridge/jump notation;
- cable type/size where stored;
- cross-floor continuation notation;
- optional abbreviation key.

Avoid huge generic legends full of unused symbols unless the user explicitly chooses a company-standard legend.

### Professional title block

Long-term export should support a proper title block containing configurable fields such as:

- company logo/name;
- client;
- site;
- site address;
- project/reference;
- drawing title;
- floor/building/block;
- drawing status (`AS FITTED`, `SURVEY`, `DESIGN`, etc.);
- drawing number;
- revision;
- issue date;
- drawn by;
- checked by;
- approved by where applicable;
- paper size;
- scale or `NTS` where appropriate;
- notes/cable specification.

The title block should be templated and automatic, not manually rebuilt for every job.

### Revision control

Support a simple revision table or revision metadata:

- revision code;
- date;
- description;
- author/checker where required.

The field workflow should make “updated after alteration” quick rather than forcing a new drawing from scratch.

## Data model target

A premium As-Fit should be generated from structured site data, not merely a flattened canvas.

Each circuit should eventually be capable of storing:

- circuit/loop identifier;
- conventional/addressable type;
- colour/style;
- panel origin;
- ordered device membership;
- actual cable route geometry;
- cable type;
- cable size;
- optional containment/path note;
- bridge crossings;
- floor transitions;
- manual adjustments;
- validation state.

Each device should eventually be capable of storing:

- stable ID;
- symbol/device class;
- loop/circuit;
- address/reference;
- zone;
- floor;
- position;
- optional location text;
- optional make/model;
- optional note;
- optional sound level or other commissioning value when useful.

The export should derive labels, schedules and legends from this model.

## “As good as CAD, much faster on site” workflow rules

### One-thumb/common-action rule

Frequent site actions should normally take one gesture or no more than two taps.

Do not bury common field actions in modal dialogs.

Examples:

- place next smoke;
- change device type;
- duplicate device;
- increment next address;
- start/continue circuit;
- undo last placement/leg;
- edit a local cable section;
- mark a bridge;
- add an isolator/junction;
- add a note.

### Auto-increment and sequence assistance

For addressable work, investigate optional rapid entry where:

- selecting a loop establishes the next address/reference;
- placing/capturing the next device can auto-increment;
- user can quickly override/skips addresses;
- duplicate address warnings are immediate;
- route order and address order are shown separately rather than falsely assuming they are always identical.

### Favourite device strip

Keep the engineer’s most-used devices one tap away.

Allow job/company templates such as:

- Smoke;
- Heat;
- Multi;
- MCP;
- Sounder;
- Sounder beacon/VAD;
- I/O;
- Isolator;
- Remote indicator;
- FAP/Repeater/PSU;
- Junction box.

The exact set should be configurable rather than forcing every possible symbol onto the screen.

### Smart label placement

A CAD-like export should not require the engineer to manually nudge every label.

Develop deterministic label placement that can:

- try preferred positions around a device;
- avoid nearby device circles;
- avoid cable lines;
- avoid wall/room text where practical;
- use leaders only when necessary;
- preserve consistent offsets;
- reflow after zoom/export without changing underlying device position.

### Circuit lane packing

Where multiple routes share a corridor/containment path:

- detect broadly parallel runs;
- assign stable visual lanes;
- keep a consistent gap;
- avoid lane order randomly swapping after redraw;
- preserve circuit identity by colour/label;
- make local manual override possible.

This should make dense As-Fits look deliberately drafted instead of coincidentally overlaid.

### Cross-floor continuity

For multi-floor buildings, add explicit tools for cable transitions such as:

- `TO 1F` / `FROM GF`;
- riser ID;
- loop/circuit ID;
- continuation reference.

A circuit must be traceable across floors without guessing.

### Quick corrections beat rerouting

The manual route editor is essential to CAD parity.

The engineer should be able to:

- draw a better local route;
- keep satisfying rough live feedback;
- clean/simplify on release;
- delete old local segment;
- validate;
- continue work.

A bad corner should take seconds to repair, not require rebuilding an entire loop.

## Export target

### Near-term

- high-resolution PNG/PDF suitable for office handover;
- consistent title block;
- generated legend;
- crisp labels;
- project/floor metadata;
- circuit routes exactly matching the current validated route model.

### Premium target

Investigate **vector-first export** (SVG and/or vector PDF) rather than relying only on a huge raster canvas.

Reasons:

- lines stay crisp at print/zoom;
- text stays sharp;
- title blocks look like professional CAD output;
- file sizes can be smaller for line drawings;
- office users can inspect/repurpose output more easily.

If DXF/DWG interoperability is later added, treat it as an export/interchange layer rather than forcing the field UI to behave like desktop CAD.

### Paper/layout presets

Long-term export should support at least common engineering sheet choices such as:

- A4;
- A3;
- portrait/landscape;
- fit-to-sheet;
- user-defined drawing frame/template.

Do not claim true scale unless plan calibration/scale data actually supports it.

## Automatic pre-export quality gate

Before producing a final As-Fitted drawing, automatically inspect for:

- circuit marked complete but topology invalid;
- missing assigned device;
- orphan route fragment;
- duplicate/zero-length route geometry;
- unintentional crossing;
- unresolved Bridge state;
- duplicate address/reference where relevant;
- missing panel origin;
- cable disappearing at floor boundary without continuation marker;
- label overlap severe enough to impair reading;
- missing legend entry for a visible symbol;
- title block missing required project fields selected by the template;
- stale route after survey-device movement;
- As-Fit geometry different from the active circuit model.

Warnings should be specific and tappable where possible so the engineer can jump straight to the problem.

## CAD-parity benchmark drawings

Maintain synthetic benchmark projects that represent different real jobs:

1. **Small office conventional** — simple radial wiring, few zones.
2. **School / multi-block addressable** — many rooms, dense devices, long loop.
3. **Warehouse/industrial** — long cable runs, beams/I-O/isolators, sparse large spaces.
4. **Dense corridor/hotel** — many devices close together, labels and parallel routes.
5. **Multi-floor loop** — riser transitions and continuation markers.
6. **Messy retrofit** — imported noisy plan, odd routes, manual corrections and junction boxes.

For each benchmark, generate the As-Fit repeatedly and compare:

- route clarity;
- label collisions;
- line overlaps;
- legend completeness;
- title block completeness;
- device count/order;
- export consistency;
- print readability;
- time/gesture count required to create it.

The benchmark output should become more professional over time, not merely gain more features.

## Field-speed metrics

Where practical measure usability with counts, not impressions only.

Examples:

- taps/gestures to place 20 common devices;
- time/gestures to wire a 20-device loop;
- time to correct one ugly dogleg;
- number of manual label moves required before export;
- number of fields manually re-entered between floors;
- time from opening a finished project to exported As-Fit;
- number of validation errors caught before export.

Every major workflow pass should ask: **does this make a competent engineer faster on a real site?**

## Continuous external-reference research loop

During substantial future premium-hardening passes, do not only inspect our own app.

Where web access is available:

1. Review several current public fire-alarm As-Fitted examples and professional CAD/service pages.
2. Prefer UK/non-domestic examples relevant to BS 5839 workflows.
3. Include a mix of conventional, addressable, small, dense and multi-floor/large-site examples where possible.
4. Also inspect modern fire-alarm design/drawing software for workflow ideas.
5. Extract **general rules**, not proprietary artwork.
6. Compare those rules against current Zone Sketch output.
7. Add only ideas that improve field speed, clarity, maintainability or handover quality.
8. Add tests/benchmark checks for adopted behaviours where practical.
9. Record useful sources and the generic lesson in this document.
10. Revisit the bank periodically; do not assume a 2026 screenshot is forever best practice.

Do not blindly clone competitors. The product advantage should be that Zone Sketch combines the clarity of desktop CAD with a much faster engineer-first onsite workflow and strong offline/local operation.

## Offline/local-first acceptance goal

Core field use should not require an internet connection once the app/build is installed and the project/background is available locally.

Target:

- create/open project offline;
- place/edit devices offline;
- route/edit circuits offline;
- save/autosave offline;
- validate offline;
- generate As-Fit offline;
- export/share a local file without server-side rendering.

Cloud sync can be optional later; it must not become a dependency for basic site work.

## Definition of success

The long-term test is simple:

> Give a competent fire-alarm engineer a tablet and a finished installation. Can they produce a clean, traceable, professional As-Fitted drawing locally before leaving site, quickly enough that sending marked-up paper back to an office CAD technician feels unnecessarily slow for ordinary jobs?

Circuit Builder, Survey and As-Fit work should keep moving toward that target on every premium-hardening pass.
