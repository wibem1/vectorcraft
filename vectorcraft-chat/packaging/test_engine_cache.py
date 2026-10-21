"""Cache integrity tests; byte fixtures are not engine integration evidence."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import engine_cache


class CacheIntegrityTests(unittest.TestCase):
    def test_verified_restore_and_corruption_rejection(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            target = repo/'target/release'
            target.mkdir(parents=True)
            suffix = '.exe' if os.name == 'nt' else ''
            for name in ('vectorcraft', 'vectorcraft-cli'):
                (target/(name+suffix)).write_bytes(b'cache byte fixture')
            with patch.object(engine_cache, 'REPO', repo), patch.object(engine_cache, 'CACHE', repo/'cache'), patch.object(engine_cache, 'fingerprint', return_value='native-source'):
                engine_cache.save()
                engine_cache.restore()
                (repo/'cache'/('vectorcraft-cli'+suffix)).write_bytes(b'corrupted')
                (target/('vectorcraft'+suffix)).write_bytes(b'keep existing')
                with self.assertRaisesRegex(ValueError, 'digest mismatch'):
                    engine_cache.restore()
                self.assertEqual((target/('vectorcraft'+suffix)).read_bytes(), b'keep existing')

    def test_source_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            cache = Path(temporary)
            (cache/'manifest.json').write_text('{"fingerprint":"old-source","sha256":{}}')
            with patch.object(engine_cache, 'CACHE', cache), patch.object(engine_cache, 'fingerprint', return_value='new-source'):
                with self.assertRaisesRegex(ValueError, 'source/environment mismatch'):
                    engine_cache.restore()

    def test_chat_commits_preserve_fingerprint_native_changes_invalidate(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            def git(*args):
                subprocess.run(['git', *args], cwd=repo, check=True, capture_output=True)
            git('init')
            git('config', 'user.name', 'Cache test')
            git('config', 'user.email', 'cache-test@example.invalid')
            (repo/'engine.rs').write_text('native v1')
            (repo/'vectorcraft-chat').mkdir()
            (repo/'vectorcraft-chat/app.py').write_text('chat v1')
            git('add', '.')
            git('commit', '-m', 'initial fixture')
            with patch.object(engine_cache, 'REPO', repo):
                first = engine_cache.fingerprint()
                (repo/'vectorcraft-chat/app.py').write_text('chat v2')
                git('add', '.')
                git('commit', '-m', 'chat fixture update')
                self.assertEqual(engine_cache.fingerprint(), first)
                (repo/'engine.rs').write_text('native v2')
                git('add', '.')
                git('commit', '-m', 'native fixture update')
                self.assertNotEqual(engine_cache.fingerprint(), first)


if __name__ == '__main__':
    unittest.main()
