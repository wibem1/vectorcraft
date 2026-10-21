# VectorCraft Chat

Development branch: `main`. Version remains **0.3.1-dev**; no new release.

Standalone Python/Tk chat for the local VectorCraft control port (default 7979). Full application source, OS launchers, regression tests and the real-engine integration test are now in this directory.

## Run

Python 3 with Tkinter, the native VectorCraft application and `vectorcraft-cli` are required. Open `START-Windows.vbs` (without a console), `START-Mac.command`, or run `python vectorcraft_chat.py`. Chat probes the local control protocol and reuses a running instance, or starts VectorCraft itself with `--control 7979`. Construction remains disabled until the application and document are ready. If discovery fails, select the installed executable once; its path is saved. Existing documents are preserved. Use **VectorCraft starten / verbinden** to retry after a connection error.

Set `VECTORCRAFT_APP` for a nonstandard native installation and `VECTORCRAFT_CLI` if the CLI cannot be found beside it or on PATH. These are source launchers; installable application packages remain open work. Automatic native startup verification is recorded in the [startup log](docs/STARTUP-2026-10-21.md).

A first blank document is created only after native UI state confirms that no document is open and no file is being opened. Existing documents are preserved.

A triangle request is planned locally with no model cost. Confirm its execution in the chat. Its ID is obtained from the actual engine reply and checked against the document tree and three closed anchors. Follow-up rotation uses that same ID and verifies the resulting angle. General model-generated moves, rotations and scales also reselect and verify the recorded triangle.

## OpenRouter and costs

The model list and prices are loaded dynamically from OpenRouter. API keys are kept outside settings and diagnostics: Windows DPAPI, macOS Keychain, or a Linux file restricted to its owner. The selected model is submitted explicitly; tests inspect the request payload.

Before a paid text request, current model pricing, prompt size, output cap (2,000 tokens), accumulated spending and the configured USD/EUR factor are checked. An unconfirmed document or command catalog stops the request before any provider call or cost reservation. Unknown prices or unsupported extra fees block the request. A conservative reservation is saved **before** sending; actual reported costs replace it before action parsing. Missing billing, connection errors and timeouts retain the reservation. Restarting or opening a new chat does not reset costs. The default conversion factor is 0.92 EUR/USD, a configurable estimate in settings, not a live exchange quote.

**The local budget is a conservative admission check, not a guaranteed provider-side euro charge cap.** Pricing changes, tokenizer and billing behavior remain external. No successful paid OpenRouter completion is claimed without an actual authorized test key. CI checks the real public model API and rejection of an invalid key; completion payloads and errors use controlled fixtures.

## Test evidence

See [session log](docs/SESSION-2026-10-21.md) and [real-engine test](docs/HEADLESS-ENGINE-TEST.md).

- Regression: `PYTHONPATH=vectorcraft-chat python -m unittest discover -s vectorcraft-chat/tests -v` from repo root.
- Actual engine: `python vectorcraft-chat/tests/smoke_headless.py target/release/vectorcraft-cli` after release compilation.
- Tk callbacks + real engine: run `test_ui_real_engine.py` under Xvfb with `VC_CHAT_REAL_CLI` pointing to the compiled binary.
- Actual native startup: run `test_native_startup.py` under Xvfb with `VC_CHAT_NATIVE_APP` pointing to the compiled GUI. This drives real TCP/MCP and a local HTTP provider fixture, without engine mocks.

The UI integration test uses the actual engine for edits and controlled HTTP replies for the model. This distinction is intentional and recorded in logs. Source-package historical notes live in `docs/source-package/`.

## Verified checkpoint, 21 October 2026

Application commit `c97651bb`: [actual native startup, engine geometry and provider HTTP-fixture integration PASS](https://github.com/wibem1/vectorcraft/actions/runs/39663769616), both OpenGL and Vulkan. Chat starts the GUI once, creates its initial document, reuses the instance, preserves triangle ID 2 through 30° rotation and a model-proposed (17, -11) move, and verifies key storage, selected model, diagnostics and cost accounting. External model charge: zero; positive completion is a local HTTP fixture.

[Windows, Linux and macOS regressions PASS](https://github.com/wibem1/vectorcraft/actions/runs/39663769551), 62 tests discovered per platform with explicitly documented skips. Linux separately passes real public OpenRouter catalog/401 checks and both actual-engine UI suites. Actual Windows/macOS native GUI startup and macOS login-Keychain roundtrip remain open. No successful paid live completion or guaranteed provider-side euro cap is claimed. The captured Chat PNG is partly occluded by the native window, so it does not establish visual layout quality.

See [TODO](TODO.md), [startup analysis](docs/STARTUP-2026-10-21.md) and [native evidence](docs/test-results/2026-10-21-native-startup.json). No release was published.
