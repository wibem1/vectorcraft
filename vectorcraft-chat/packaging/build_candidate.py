"""Build portable CI candidate, including native engine and MCP CLI. No release."""
from pathlib import Path
import shutil
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
for name in ('LICENSE-MIT', 'LICENSE-APACHE', 'NOTICE'):
    shutil.copy2(repo/name, bundle/name)
shutil.copy2(chat/'packaging/CANDIDATE.md', bundle/'CANDIDATE.md')
if sys.platform == 'darwin':
    subprocess.run(['codesign', '--force', '--deep', '--sign', '-', str(bundle)], check=True)
executable = binaries/('VectorCraftChat'+suffix)
subprocess.run([str(executable), '--self-test', str(repo/'packaged-evidence')], check=True, timeout=300)
# CI upload only follows successful frozen execution. Archives preserve macOS modes/symlinks.
if sys.platform == 'darwin':
    subprocess.run(['ditto', '-c', '-k', '--sequesterRsrc', '--keepParent', str(bundle),
                    str(repo/'candidate/VectorCraftChat-macos-intel.zip')], check=True)
else:
    shutil.make_archive(str(repo/'candidate/VectorCraftChat-windows-x64'), 'zip', bundle.parent, bundle.name)
