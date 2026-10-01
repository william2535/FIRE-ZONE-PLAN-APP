# Add multiple devices

Open **Add device → Add multiple devices** in Survey mode. Enter quantities for one or several device types, then select **Add devices**. The same action is in **Plan symbols** and respects the current system and mode: Fire plan mode still offers only its existing plan symbols.

The batch is placed in clear, spaced positions near the current view. Small batches prefer finger-sized gaps; larger batches use the available plan grid. Select / move activates automatically, so each device can be dragged into position. Devices are not grouped. Use pinch zoom for crowded plans. If the batch extends beyond the view, the floor is fitted to the screen.

- Up to 100 devices per batch, with whole-number quantities and no partial additions when space is insufficient.
- Uses the current symbol colour and size. Existing equipment stays in place.
- Every device gets a new stable ID and the normal floor model. No equipment, cable, zone or door association is guessed or copied.
- Record state starts as **Not recorded**. Batch placement does not imply a survey or onsite verification.
- Undo removes the batch in one step; redo retains its IDs. Later individual moves use the existing editor, routing, autosave, backup and export behaviour.
- Beam devices are added as ordinary beam symbols; their default appearance does not document a measured direction or range.

`tests/batch-devices.cjs` covers all four systems, mixed quantities, validation, 100-device insertion, independent movement, route attachment, undo/redo, reload, backup output and five viewport sizes. The existing regression runner includes it, and the system workflow also runs it in WebKit.
