"""Read-only verification of the archived project files; no live-app commands."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[3])
    args = parser.parse_args()
    root = args.repo.resolve()
    manifest = json.loads((root / 'projects/chatgpt-work/FILE_MANIFEST.json').read_text(encoding='utf-8'))
    failures = []
    for entry in manifest['files']:
        path = (root / entry['path']).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            failures.append(entry['path'] + ': missing or outside repository')
            continue
        data = path.read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()
        if len(data) != entry['bytes'] or hashlib.sha256(data).hexdigest() != entry['sha256'] or blob != entry['git_blob_sha1']:
            failures.append(entry['path'] + ': checksum mismatch')
        if path.suffix == '.zip':
            with zipfile.ZipFile(path) as archive:
                broken = archive.testzip()
                if broken:
                    failures.append(entry['path'] + ': corrupt ZIP member ' + broken)
    if failures:
        raise SystemExit('\n'.join(failures))
    print('Verified ' + str(len(manifest['files'])) + ' files: size, SHA-256, Git blob ID and ZIP CRCs.')


if __name__ == '__main__':
    main()
