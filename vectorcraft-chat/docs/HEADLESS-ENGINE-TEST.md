# Actual VectorCraft engine verification

Updated 2026-10-21. No release is made by this workflow.

The earlier smoke test **did pass** in Actions run [39620575062](https://github.com/wibem1/vectorcraft/actions/runs/39620575062), original job 119292609606. Its log confirmed object ID 2, successful selection and changed model after rotation. Its explicit limitation was no exact geometric-angle assertion. A real rerun was requested in this development session: job 119298453828 also completed successfully.

The extended test replaces that limited test and imports the same `MCPClient`, `create_triangle` and `transform_object` used by the Chat app. It starts `vectorcraft-cli mcp --headless` compiled from the actual Rust repository; no engine simulator is involved.

Assertions:

1. Create a closed triangle; check the draw reply ID against the before/after actual layer tree and three closed anchors.
2. Rotate the same ID by 30°; compare reported rotation and bounds with independent analytical calculations in document coordinates.
3. Move, scale uniformly, rotate by -15°, and move again after explicitly clearing the selection. Assert bounds, triangle topology and object identity throughout.
4. Render actual PNG bytes through the engine. Upload PNG and the machine-readable node report as `vectorcraft-chat-engine-evidence`.
5. Drive actual Tk callbacks under a virtual display: create, rotate, request a model-generated move, execute it after clearing the selection, verify geometry. Check selected model, key save/load, diagnostic exclusion of secrets and accounting even when action parsing fails. HTTP responses in this UI test are controlled fixtures.

The workflow runs on pushes affecting `vectorcraft-chat/**`, so app changes cannot silently bypass this gate. Full engine and app test results must be checked for the final commit. A successful build alone does not count as successful interaction.

The repository-wide Rust gate `cargo xtask ci` has not been run locally in this session; no Rust engine source was modified. Headless release compilation is performed in Actions. The separate Chat workflow tests Linux, Windows and macOS and actual public OpenRouter HTTP calls without a paid key.

## Verified final application checkpoint

[Run 39624046757](https://github.com/wibem1/vectorcraft/actions/runs/39624046757), commit `5629006d6d0886a95abc17d0258246c35c92c127`: **all steps passed**, including actual-engine Tk callbacks. The strengthened test also preserved an intervening edit to target ID 2 while leaving a different selected object ID 3 unchanged. Machine report: [2026-10-21-headless.json](test-results/2026-10-21-headless.json). PNG/report artifact: [12355504814](https://github.com/wibem1/vectorcraft/actions/runs/39624046757/artifacts/12355504814).

This establishes the tested interaction sequence, not unrestricted model behavior or a released app. See TODO for outstanding launch, macOS, packaging and billing guarantees.
