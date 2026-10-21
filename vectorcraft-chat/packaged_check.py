"""Explicit CI-only entry into the same native integration suite in a frozen app."""
import contextlib
import json
import os
from pathlib import Path
import sys
import traceback
import unittest


def run(output):
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    with (output/'packaged-check.log').open('w', encoding='utf-8') as log:
        with contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
            try:
                if not getattr(sys, 'frozen', False):
                    raise RuntimeError('Packaged check requires the actual frozen executable')
                directory = Path(sys.executable).resolve().parent
                suffix = '.exe' if sys.platform == 'win32' else ''
                engine = directory/('vectorcraft'+suffix)
                cli = directory/('vectorcraft-cli'+suffix)
                if not engine.is_file() or not cli.is_file():
                    raise FileNotFoundError('Bundled native engine or CLI missing')
                # The suite isolates app settings, keys, documents and cost ledger.
                os.environ['VC_CHAT_NATIVE_APP'] = str(engine)
                os.environ['VECTORCRAFT_CLI'] = str(cli)
                os.chdir(output)
                import test_native_startup
                suite = unittest.defaultTestLoader.loadTestsFromTestCase(test_native_startup.NativeStartupTests)
                result = unittest.TextTestRunner(stream=log, verbosity=2).run(suite)
                passed = result.wasSuccessful() and result.testsRun > 0 and not result.skipped
                report = {'status': 'PASS' if passed else 'FAIL', 'frozen': True,
                          'executable': str(Path(sys.executable).resolve()),
                          'engine': str(engine), 'cli': str(cli),
                          'tests_run': result.testsRun, 'skipped': len(result.skipped)}
            except Exception:
                traceback.print_exc(file=log)
                passed = False
                report = {'status': 'FAIL', 'frozen': bool(getattr(sys, 'frozen', False))}
            (output/'packaged-check.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    return 0 if passed else 1
