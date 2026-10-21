# VectorCraft Chat

Development branch: `main`. Version remains **0.3.1-dev**; no new release.

Standalone Python/Tk chat for the local VectorCraft control port (default 7979). Full application source, OS launchers, regression tests and the real-engine integration test are now in this directory.

## Run

Python 3 with Tkinter, the native VectorCraft application and `vectorcraft-cli` are required. Open `START-Windows.vbs` (without a console), `START-Mac.command`, or run `python vectorcraft_chat.py`. Chat probes the local control protocol and reuses a running instance, or starts VectorCraft itself with `--control 7979`. Construction remains disabled until the application and document are ready. If discovery fails, select the installed executable once; its path is saved. Existing documents are preserved. Use **VectorCraft starten / verbinden** to retry after a connection error.

Set `VECTORCRAFT_APP` for a nonstandard native installation and `VECTORCRAFT_CLI` if the CLI cannot be found beside it or on PATH. These are source launchers. Tested portable Windows/macOS Intel candidates including Python/Tk, engine and CLI are linked below; signed installers remain open work. Automatic native startup verification is recorded in the [startup log](docs/STARTUP-2026-10-21.md).

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

## Verified native Windows and macOS checkpoint

Application source `1df86ea1`: [Windows and macOS native integration PASS](https://github.com/wibem1/vectorcraft/actions/runs/39672716335), plus [Linux real-engine regression PASS](https://github.com/wibem1/vectorcraft/actions/runs/39672716402). Actual GUI/CLI builds, one application launch, reuse, document preservation, triangle ID 2, 30° rotation, native follow-up move, OS launch failure, key storage, diagnostics and provider-fixture accounting are verified. Windows MCP bridges now launch without a console. [Actual DPAPI and isolated macOS Keychain CRUD PASS](https://github.com/wibem1/vectorcraft/actions/runs/39673786475).

[Windows/macOS initial App layout PASS](https://github.com/wibem1/vectorcraft/actions/runs/39677833630): unobscured screenshots visually inspected with the production theme; key masked and main controls visible. These separate initial-state snapshots make no engine/provider calls. Combined native-flow captures are partly obscured by the native window. Positive provider completions in native tests are local HTTP fixtures; [live probe](https://github.com/wibem1/vectorcraft/actions/runs/39673176326) reports NOT_CONFIGURED because the repository has no test key. This is not a paid live completion success.

Test hosts: Windows Server 2025 x64 with DX12 software rendering, macOS 15.7.9 Intel with Metal, Linux/Xvfb with OpenGL/Vulkan. Signed installers, positive live completion, general constructions and a provider-enforced EUR cap remain open. Tested portable Chat candidates are linked below. The current macOS GUI package ships its CLI separately; install both for source use. See [platform log](docs/PLATFORMS-2026-10-21.md) and [complete evidence](docs/test-results/2026-10-21-native-platforms.json). No release; version remains 0.3.1-dev.

## Verified standalone CI candidates

The [frozen package workflow](https://github.com/wibem1/vectorcraft/actions/runs/39682760797) **passed on Windows x64 and macOS Intel**, source `6ba2c2c1`. Python/Tk, Chat, the actual native engine and its CLI are included. Both actual windowed executables ran the real native triangle/ID/30-degree/follow-up suite, secret store CRUD, model selection, diagnostic redaction and cost accounting. Each also passed automatic bundled binary discovery, the actual public OpenRouter HTTPS catalog (468 models) and actual HTTP 401 with an invalid key. Positive completions remain a local HTTP fixture; external model charge was zero.

- [Windows candidate ZIP artifact](https://github.com/wibem1/vectorcraft/actions/runs/39682760797/artifacts/12385539120): extract the complete folder; entry is `VectorCraftChat.exe`.
- [macOS Intel candidate ZIP artifact](https://github.com/wibem1/vectorcraft/actions/runs/39682760797/artifacts/12385928869): preserve the complete `VectorCraftChat.app`; engine and CLI are inside it.

These are tested CI candidates, not a release or general installation approval. Windows is unsigned; macOS has an ad hoc signature verified in CI, without Developer ID/notarization. Actions artifacts expire; source/build scripts and [full verification JSON](docs/test-results/2026-10-21-frozen-candidates.json) remain in Git. The independent [uploaded archive audit](https://github.com/wibem1/vectorcraft/actions/runs/39687971880) also passed: every shipped executable matches its tested SHA256, macOS execute permissions and license notices are present. See the [step-by-step package log](docs/PACKAGES-2026-10-21.md). Version remains **0.3.1-dev**, no release.
