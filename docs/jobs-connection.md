# Jobs companion connection

This web-only companion supports the automatic editing workflow in [Jobs PR #1](https://github.com/william2535/Jobs/pull/1): Jobs opens this application's real editor with a working project; **Save to Jobs** returns the updated editable envelope and actual engine-rendered survey PNGs. It uses the current `ZoneSketchByWill` version 1 format and the existing importer, local save and rendering functions.

The receiver is a single insertion inside the main `index.html` engine closure. Normal launches have no connection fragment and return immediately without adding controls or changing project behaviour. Android assets and standalone HTML copies are intentionally unchanged for this initial web integration. Existing licences are unchanged.

## Deployment and use

The connection becomes available only after the companion branch is merged and this web `index.html` is deployed. A draft PR is not a live deployment. Jobs must also deploy its matching opener and local revision-saving implementation. The [Jobs protocol and setup documentation](https://github.com/william2535/Jobs/blob/feat/offline-jobs-mvp/integrations/zone-sketch/README.md) is the companion contract; [transport implementation](https://github.com/william2535/Jobs/blob/feat/offline-jobs-mvp/src/zone-handoff.js) defines the Jobs side.

Launch through Jobs **Edit site**. The opener sends `jobsOrigin` and a random `session` in the URL fragment; project data stays out of the URL and is transferred through `postMessage`. The trusted origin in this deployment is exactly `https://william2535.github.io`. GitHub Pages repository paths share that origin; this does not isolate one repository from another on that host. A separate origin can be configured if that separation is required.

Both sides validate the exact origin, window identity, session, protocol `jobs-zonesketch` and version `1`. The receiver waits for the existing project database, validates the received envelope, saves the prior drawing and activates a separate local editing copy. Site-only sessions have null job/revision identifiers; visit sessions include both.

**Save to Jobs** first saves that engine copy locally, then renders each working floor using the existing survey PNG renderer and sends the envelope plus included images. Only a successful Jobs local-save acknowledgement displays **Saved in Jobs**. Failed or missing acknowledgements retain an identical-request retry. Editing a different native Zone Sketch project blocks return to the pinned Jobs site, including checks around asynchronous saves/rendering. Repeated load messages do not reset edits. Back to Jobs warns before returning with unacknowledged changes.

The handoff limits are 32 MiB per editable project, 8 MiB per preview and 25 MiB for all previews. Survey PNGs include source headers/legends; Jobs displays the full image without applying incompatible coordinate overlays. Device editing/results remain linked through stable source floor/device IDs.

## Verification and limits

Verified with synthetic data against reviewed base `dca2eff063f52a9980c2aed255879a65cc579379` using the independently maintained Jobs tests:

```sh
# Run from the Jobs checkout, pointing at an unmodified reviewed Zone Sketch source.
ZONE_SKETCH_REFERENCE=/path/to/FIRE-ZONE-PLAN-APP/index.html node tests/zone-bridge-source.mjs
ZONE_SKETCH_REFERENCE=/path/to/FIRE-ZONE-PLAN-APP/index.html node tests/zone-bridge-jobs.mjs
```

The first checks real engine automatic import, original drawing controls, two returned floor PNGs/four assets, repeated load, forged-source rejection, missing-acknowledgement retry and blocking an unrelated project return. The second builds Jobs separately and exercises site-only and visit handoffs, preserving site/job/asset IDs, recorded results and previous revisions, then reopening/exporting the returned PNGs offline at a 390 px Jobs viewport. These tests create temporary instrumented runtimes and never copy customer records into either repository.

Jobs' saved plans, observations and exports remain available offline after its own offline preparation. This separate web editor currently has no service-worker installation: cold launching its remote page offline is not promised. An already loaded editor uses local drawing/storage and browser messaging. Native Android handoff, a bundled offline web deployment, broader physical-device validation and compliance certification are outside this companion change.
