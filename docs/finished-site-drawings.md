# Finished site drawings

As fit drawings no longer include bridge humps. Bridge still permits intentional
cable crossings in the circuit editor, and its metadata remains saved.

After **Complete circuits → As-Fit**, reopening As fit mode (including after a
reload or floor switch) opens the saved drawing directly. **← Circuits** returns
to the route controls, where **View As fit drawing** reopens it without generating
another record. An incomplete route, open edit, changed device position, or
changed circuit set prevents a stale drawing from opening as finished.

On Home, **View finished drawings** appears on a fire project when every floor has:

- Zone areas for its recorded zones.
- Surveyed field devices.
- A saved As fit covering the current, complete circuits without open edits or
  changed device positions.

Zones and Survey do not have explicit completion flags, so the button uses this
existing drawing data. The existing confirmation allowing an As fit with
unassigned surveyed devices is preserved.

The button opens a read-only viewer with a floor selector and three drawings:

- **Zones - for customer**
- **Survey - for engineer**
- **As fit - for record**

Each drawing can be enlarged. Viewing a site's drawings does not switch the
active project or modify its contents. The As fit uses the same rendering as the
circuit preview and PNG export. Completion does not change item verification or
issued-record history.

Focused checks: `node tests/asfit-saved-preview.cjs` and
`node tests/finished-project-drawings.cjs`. Both are included in the regression
runner.
