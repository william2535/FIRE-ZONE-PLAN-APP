# Maps and As-Fits — Stage 1

Use **Project → Maps & As-Fits**, or **Properties → Record state / As-Fit** for a selected item. This is an additive foundation in the shared editor; Fire, Security, CCTV and Access Control keep their existing models and tools.

## Records and issue workflow

- Devices, doors, circuit routes, connections, pinned photos/notes, plan notes and Security runs carry an optional `recordState` object. The states are `notRecorded`, `existing`, `proposed`, `installed`, `removed` and `verified`.
- Old items default to **Not recorded**. Circuit completion and device commissioning do not imply onsite verification. A verified record requires the engineer's name and explicit onsite confirmation; its content fingerprint, time and name are retained.
- Changes to a verified item, including movement of a connection/circuit endpoint, clear current verification and prompt another onsite check. Earlier evidence remains in revision entries and previously issued snapshots. Copying a door to a new floor does not copy its verification.
- Letter badges supplement restrained colours: E existing, P proposed, I installed, R removed, V verified. Unmarked items have no recorded state. View filters never delete records and never limit exports. Hidden items are excluded from selection and connection hit targets.
- Revision notes and automatic item creation/edit/deletion entries are project-level records. The entered drawing engineer name supplies attribution when available; blank names remain explicitly unrecorded. Times are from the device clock, not an authenticated server.
- **Issue As-Fit snapshot** requires a unique revision, issuer and issue note. It copies every floor and all current states into `issuedAsFits[].project`, excluding earlier snapshots to avoid recursive growth. Open circuit edits block issue. Issuing does not set any item to verified.
- Issued JSON, CSV and PDF are generated from the stored copy. Editing or undoing the working plan does not replace issued copies. Standard editable backups include revision history and every issued snapshot. The standard JSON format/version and device/floor IDs remain unchanged.
- Standard drawing exports include state badges and a key. Circuit routes are included in survey/As-Fit drawings. CSV records retain IDs, floor references, state, attribution, routes and revision notes. JSON retains the full editable data and photo bytes; PDFs/images are visual records, not editable backups.

## UK source review

Checked 1 October 2026 using the following primary sources. These establish applicable subject areas and current publications; they do not constitute a clause-by-clause assessment of the paid standards.

| Area | Authoritative source | Use in this stage |
| --- | --- | --- |
| Non-domestic fire alarms | [BSI: BS 5839-1 current release](https://landingpage.bsigroup.com/LandingPage/Undated?UPI=000000000000862786) — BS 5839-1:2025 | Keep recorded survey evidence separate from engineering approval. No compliance label is inferred from drawing completion. |
| Intruder / hold-up | [BSI: PD 6662 current release](https://landingpage.bsigroup.com/LandingPage/Undated?UPI=000000000019994009) — PD 6662:2017 | Preserve installation records and references; no grading/certification inference. |
| CCTV | [BSI security systems catalogue](https://knowledge.bsigroup.com/categories/security-systems) — BS EN IEC 62676-4:2025 | Preserve the existing camera/network records and routes. No new image-performance threshold claims. |
| Access control | [NSI: NCP 109 Issue 4 update](https://www.nsi.org.uk/nsi-code-of-practice-ncp-109-issue-4-supporting-nsi-installers-with-guidance-on-the-latest-access-control-system-standards/) and [NSI: March 2026 guide announcement](https://www.nsi.org.uk/security-vs-safety-guide-to-the-new-ncp-109-issue-4/) | Keep existing door and connection evidence. Documentation prompts are not a safe-egress assessment or a compliance certificate. |

These record states are app workflow terms, not a claim that a standard mandates this exact schema. Engineers must use the applicable standard, specification and site strategy for their actual work.

## Checks and boundaries

`node tests/maps-asfit-stage1.cjs` exercises old-project defaults, explicit verification, endpoint-change invalidation, revision/issue persistence, multi-floor photo/route retention, duplicate and backup paths, filtered exports, issued PDF/JSON and five viewport sizes. Run `BROWSER=webkit node tests/maps-asfit-stage1.cjs` for the WebKit pass. It is included in `tests/run-regressions.cjs`.

Validated locally: 49/49 regression files, focused Stage 1 test in Chromium and WebKit, inline parser, current v0.63 release gate, four-copy byte equality and `.github/verify_247_protected.py`. Local browser harness used Playwright 1.51.1 because the preinstalled 1.62.1 browser CDN download was unavailable; CI retains the repository’s pinned 1.62.1 runtime.

- All four app HTML mirrors ship the feature. The existing main-branch Android workflow rebuilds and publishes its v0.63 APK after its regression/build gates; no new version number is introduced by this stage.
- Snapshots are retained copies in a local editable database, not signed, tamper-proof audit records. Whole-project duplicates preserve evidence as copied records; they do not independently re-verify the installation.
- Snapshot photo data increases backup size. Issue is blocked before the complete project exceeds 30 MiB, within the existing 32 MiB import limit. Save failures remain visible and the issued JSON can be exported directly.
- Exports include all states; the engineer must resolve proposed/removed/unverified entries and document the issue scope. Importing an issued JSON creates an editable working copy of that issue.
- No new system-specific design rules, certificates, commissioning forms, calibrated dimensions or standards certification are implemented in Stage 1.
