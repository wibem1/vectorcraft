"""Build portable CI candidate, including native engine and MCP CLI. No release."""
from pathlib import Path
import shutil
import hashlib
import json
import subprocess
import sys

repo = Path(__file__).resolve().parents[2]
chat = repo/'vectorcraft-chat'
subprocess.run([sys.executable, '-m', 'PyInstaller', '--noconfirm', '--clean',
                '--onedir', '--windowed', '--noupx', '--icon', 'NONE',
                '--name', 'VectorCraftChat', '--paths', str(chat/'tests'),
                '--hidden-import', 'test_native_startup',
                '--distpath', str(repo/'candidate'), '--workpath', str(repo/'build/chat'),
                '--specpath', str(repo/'build/chat'), str(chat/'vectorcraft_chat.py')], check=True)
if sys.platform == 'darwin':
    bundle = repo/'candidate/VectorCraftChat.app'
    binaries = bundle/'Contents/MacOS'
else:
    bundle = repo/'candidate/VectorCraftChat'
    binaries = bundle
suffix = '.exe' if sys.platform == 'win32' else ''
for name in ('vectorcraft', 'vectorcraft-cli'):
    shutil.copy2(repo/'target/release'/(name+suffix), binaries/(name+suffix))
documents = bundle/'Contents/Resources/ChatDocs' if sys.platform == 'darwin' else bundle
documents.mkdir(parents=True, exist_ok=True)
for name in ('LICENSE-MIT', 'LICENSE-APACHE', 'NOTICE'):
    shutil.copy2(repo/name, documents/name)
shutil.copy2(chat/'packaging/CANDIDATE.md', documents/'CANDIDATE.md')
if sys.platform == 'darwin':
    subprocess.run(['codesign', '--force', '--deep', '--sign', '-', str(bundle)], check=True)
    subprocess.run(['codesign', '--verify', '--deep', '--strict', str(bundle)], check=True)
executable = binaries/('VectorCraftChat'+suffix)
evidence = repo/'packaged-evidence'
evidence.mkdir(parents=True, exist_ok=True)
manifest = {'source_sha': __import__('os').environ.get('GITHUB_SHA'),
            'platform': sys.platform, 'release': False, 'sha256': {}}
for binary in (executable, binaries/('vectorcraft'+suffix), binaries/('vectorcraft-cli'+suffix)):
    manifest['sha256'][binary.name] = hashlib.file_digest(binary.open('rb'), 'sha256').hexdigest()
(evidence/'bundle-manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
subprocess.run([str(executable), '--self-test', str(repo/'packaged-evidence')], check=True, timeout=300)
# CI upload only follows successful frozen execution. Archives preserve macOS modes/symlinks.
if sys.platform == 'darwin':
    subprocess.run(['ditto', '-c', '-k', '--sequesterRsrc', '--keepParent', str(bundle),
                    str(repo/'candidate/VectorCraftChat-macos-intel.zip')], check=True)
else:
    shutil.make_archive(str(repo/'candidate/VectorCraftChat-windows-x64'), 'zip', bundle.parent, bundle.name)
