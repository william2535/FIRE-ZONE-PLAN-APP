# Completed steps and saved drawings

Every Home project card has **Show completed steps**, including Fire, Additional
work, CCTV, Intruder and Access Control sites. The viewer shows three paper
cards together at the top of the screen:

- The plan or Building layout **for customer**.
- Survey or Add devices **for engineer**.
- As fit **for record**.

Opening the viewer starts with one paper in the middle. It separates into the
three cards above; tap an available card to open its full drawing beneath them.
The cards remain together on portrait phones. A zoom bar beneath the selected
drawing lets you drag from **100%** (Fit) to **500%**. Use **−** and **+** for small
adjustments, scroll or pan around the enlarged paper, and tap **Fit** to see the
whole drawing again. Resizing the screen keeps the current zoom and inspected
area; choosing another step or floor resets to Fit. Reduced-motion settings show
the final cards immediately.

Availability is determined separately for each floor and step. Fresh Fire's
customer drawing requires zone areas; Additional work and the other disciplines
use the building or imported plan. Additional work may also document only an
existing cable reference. The engineer drawing requires surveyed devices (or
configured Access doors). A step without drawing data stays visible and says
**Not completed** instead of presenting a blank finished drawing.

Fire's record drawing uses the saved As-fit and its current route validation.
Incomplete or edited routes and changed endpoint positions do not open as a
finished record. For CCTV, Intruder and Access Control, the record card opens the
latest issued As-fit snapshot for the selected floor, with its saved revision.
It does not turn the working drawing into an issued record.

The existing saved As-fit preview remains available when reopening As-fit mode,
without pressing Complete circuits again. As-fit drawings omit bridge editing
humps and other temporary controls.

Viewing drawings does not change the active project, floor, device references,
verification states or issue history. Closing or changing floors cancels pending
animation and rendering, and releases preview canvases.

Focused checks: `tests/finished-project-drawings.cjs` and
`tests/asfit-saved-preview.cjs`. The completed-steps checks cover Chromium and
WebKit on phone viewports, all disciplines, partial completion, animation,
read-only viewing, issued snapshots, real zoom-bar gestures, phone resizing,
Fit/reset behaviour and reopening.
