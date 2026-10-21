"""Exact native-source binary cache; every candidate still runs actual engine tests."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

REPO = Path(__file__).resolve().parents[2]
CACHE = REPO/'native-cache'


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def fingerprint():
    # Include every tracked repository blob except Chat and workflow definitions.
    # This includes assets, manifests, external dependency revisions and build scripts.
    tree = subprocess.check_output(['git', 'ls-tree', '-r', 'HEAD'], cwd=REPO, text=True)
    lines = [line for line in tree.splitlines()
             if not line.split('\t', 1)[1].startswith(('vectorcraft-chat/', '.github/'))]
    environment = json.dumps({'rust': '1.95.0', 'platform': sys.platform,
                              'image': os.environ.get('ImageVersion'),
                              'arch': os.environ.get('RUNNER_ARCH')}, sort_keys=True)
    return hashlib.sha256(('\n'.join(lines)+'\n'+environment).encode()).hexdigest()


def save():
    CACHE.mkdir(parents=True, exist_ok=True)
    suffix = '.exe' if sys.platform == 'win32' else ''
    hashes = {}
    for name in ('vectorcraft', 'vectorcraft-cli'):
        name += suffix
        shutil.copy2(REPO/'target/release'/name, CACHE/name)
        hashes[name] = digest(CACHE/name)
    (CACHE/'manifest.json').write_text(json.dumps({'fingerprint': fingerprint(), 'sha256': hashes}, indent=2))


def restore():
    manifest = json.loads((CACHE/'manifest.json').read_text())
    if manifest['fingerprint'] != fingerprint():
        raise ValueError('Native cache source/environment mismatch')
    suffix = '.exe' if sys.platform == 'win32' else ''
    names = [name+suffix for name in ('vectorcraft', 'vectorcraft-cli')]
    if set(manifest['sha256']) != set(names):
        raise ValueError('Native cache binary list mismatch')
    # Verify all files before copying any executable.
    for name in names:
        if digest(CACHE/name) != manifest['sha256'][name]:
            raise ValueError('Native cached binary digest mismatch: '+name)
    target = REPO/'target/release'
    target.mkdir(parents=True, exist_ok=True)
    for name in names:
        shutil.copy2(CACHE/name, target/name)
    print('Restored exact native engine/CLI, SHA256 verified; real tests still mandatory')


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'fingerprint':
        value = fingerprint()
        print(value)
        with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as stream:
            stream.write('fingerprint='+value+'\n')
    elif mode == 'save':
        save()
    elif mode == 'restore':
        restore()
    else:
        raise ValueError('Unknown native cache operation')
