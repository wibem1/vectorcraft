# Live Repeat container editing

Branch: `live-repeat-editing`. Test build: `0.11.0-live-repeat.1`.

Select a Repeat and choose Object > Repeat > Edit Repeat Contents, double-click
with Selection, or enter Isolation Mode from the Layers menu. Newly drawn and
pasted objects use the Repeat as their insertion parent. Escape exits. Paths
and groups can be moved or copied into the Repeat through Layers; sublayers
remain layer-only. Source members use the existing delete, arrange and grouping
commands and their ordinary undo transactions.

In editing mode source art is visible at its document coordinates. Generated
instances are dimmed previews. Selection and marquee reach source art only.
Outside editing, the Repeat renders normally and stays a live object.

The arrangement holds a `reference_bounds` rectangle independently of source
bounds. It controls radial placement, grid spacing and flip axes, while actual
source bounds continue to measure the artwork and its copies. New content does
not recalculate the arrangement. Changing repeat kind establishes a new reference.
Whole-object transforms move both source and reference. Old native files without
the optional reference still open; mutable container access captures the old
bounds before the source changes. Native save retains the reference.

Regression coverage lives in engine pattern/layer tests, doc pattern tests,
render isolation tests, native profile tests and Layers panel tests.
The branch Windows workflow runs workspace quality gates, Windows tests, an
optimized native test build (the project's development profile, with debug info
disabled), then starts the executable and exercises drawing, copying,
reordering, deleting, undo/redo, save/reopen and screenshots for all three kinds.
Only successful runs upload a portable app. Failed runs retain diagnostic evidence.

Start.cmd opens loopback control port 17979. The prerelease executable itself
uses its own adjacent profile even when started directly. Diagnose.cmd captures
document/UI inspection, full native document data, screenshot, build identity,
self-test report and rotated logs into a local ZIP. When the app is unavailable,
existing logs are still captured. Nothing is sent. The installed original,
normal profile, default/release branches and file associations are untouched.
