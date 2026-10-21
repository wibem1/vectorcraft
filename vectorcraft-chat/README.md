# VectorCraft Chat

Development branch: `main`. Version remains **0.3.1-dev**; no new release.

Standalone Python/Tk chat for the local VectorCraft control port (default 7979). Full application source, OS launchers, regression tests and the real-engine integration test are now in this directory.

## Run

Python 3 with Tkinter and an installed `vectorcraft-cli` are required. Set `VECTORCRAFT_CLI` if the CLI is not on PATH or in the standard Windows installation directory. Start VectorCraft with `--control 7979`, then use `START-Windows.cmd`, `START-Mac.command`, or `python vectorcraft_chat.py`.

A triangle request is planned locally with no model cost. Confirm its execution in the chat. Its ID is obtained from the actual engine reply and checked against the document tree and three closed anchors. Follow-up rotation uses that same ID and verifies the resulting angle. General model-generated moves, rotations and scales also reselect and verify the recorded triangle.

## OpenRouter and costs

The model list and prices are loaded dynamically from OpenRouter. API keys are kept outside settings and diagnostics: Windows DPAPI, macOS Keychain, or a Linux file restricted to its owner. The selected model is submitted explicitly; tests inspect the request payload.

Before a paid text request, current model pricing, prompt size, output cap (2,000 tokens), accumulated spending and the configured USD/EUR factor are checked. Unknown prices or unsupported extra fees block the request. A conservative reservation is saved **before** sending; actual reported costs replace it before action parsing. Missing billing, connection errors and timeouts retain the reservation. Restarting or opening a new chat does not reset costs. The default conversion factor is 0.92 EUR/USD, a configurable estimate in settings, not a live exchange quote.

**The local budget is a conservative admission check, not a guaranteed provider-side euro charge cap.** Pricing changes, tokenizer and billing behavior remain external. No successful paid OpenRouter completion is claimed without an actual authorized test key. CI checks the real public model API and rejection of an invalid key; completion payloads and errors use controlled fixtures.

## Test evidence

See [session log](docs/SESSION-2026-10-21.md) and [real-engine test](docs/HEADLESS-ENGINE-TEST.md).

- Regression: `PYTHONPATH=vectorcraft-chat python -m unittest discover -s vectorcraft-chat/tests -v` from repo root.
- Actual engine: `python vectorcraft-chat/tests/smoke_headless.py target/release/vectorcraft-cli` after release compilation.
- Tk callbacks + real engine: run `test_ui_real_engine.py` under Xvfb with `VC_CHAT_REAL_CLI` pointing to the compiled binary.

The UI integration test uses the actual engine for edits and controlled HTTP replies for the model. This distinction is intentional and recorded in logs. Source-package historical notes live in `docs/source-package/`.

## Verified checkpoint, 21 October 2026

Application commit `5629006`: [actual engine and Tk interaction PASS](https://github.com/wibem1/vectorcraft/actions/runs/39624046757). [Windows/Linux regressions and public OpenRouter HTTP PASS](https://github.com/wibem1/vectorcraft/actions/runs/39624046765); macOS still queued at documentation time. All 37 unique Linux tests were exercised across the regression, live HTTP and Tk steps. See [TODO](TODO.md) for the remaining release blockers. No release was published.
