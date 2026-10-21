"""Frozen app entry; CI verifies public HTTPS without a valid provider key."""
import contextlib
import json
import os
from pathlib import Path
import sys
import traceback
from unittest.mock import patch


def self_test(output):
    from packaged_check import run
    output = Path(output).resolve()
    code = run(output)
    if code:
        return code
    with (output/'packaged-network.log').open('w', encoding='utf-8') as log:
        with contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
            try:
                import app_connection
                directory = Path(sys.executable).resolve().parent
                suffix = '.exe' if sys.platform == 'win32' else ''
                with patch.dict(os.environ, {'VECTORCRAFT_APP': '', 'VECTORCRAFT_CLI': ''}), \
                     patch.object(app, 'SETTINGS', output/'nonexistent-settings.json'):
                    if app_connection.find_application() != directory/('vectorcraft'+suffix):
                        raise RuntimeError('Automatic bundled engine discovery failed')
                    if Path(app.mcp_executable()).resolve() != directory/('vectorcraft-cli'+suffix):
                        raise RuntimeError('Automatic bundled CLI discovery failed')
                models = app.model_catalog('')
                if len(models) <= 10:
                    raise RuntimeError('Public model catalog missing')
                try:
                    app.api_chat('invalid-vectorcraft-ci-key', 'nonexistent/model',
                                 [{'role': 'user', 'content': 'test'}], 1)
                except RuntimeError as exc:
                    if 'HTTP 401' not in str(exc):
                        raise
                else:
                    raise RuntimeError('Unauthorized request was unexpectedly accepted')
                report = {'status': 'PASS', 'public_models': len(models),
                          'unauthorized_http': 401, 'automatic_bundled_discovery': True,
                          'valid_key_used': False, 'positive_live_completion': False,
                          'actual_provider_charge_usd': 0}
                code = 0
            except Exception:
                traceback.print_exc(file=log)
                report = {'status': 'FAIL', 'positive_live_completion': False}
                code = 1
            (output/'packaged-network.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    return code


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == '--self-test':
        output = Path(sys.argv[2]).resolve()
        output.mkdir(parents=True, exist_ok=True)
        with (output/'bootstrap.log').open('w', encoding='utf-8') as log:
            with contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
                try:
                    import vectorcraft_chat as app
                    code = self_test(output)
                except Exception:
                    traceback.print_exc(file=log)
                    code = 1
        raise SystemExit(code)
    import vectorcraft_chat as app
    root = app.tk.Tk()
    app.ttk.Style().theme_use('clam')
    app.App(root)
    root.mainloop()
