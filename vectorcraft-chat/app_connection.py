"""Find/start the native app and verify its loopback control protocol before editing."""
import contextlib
import errno
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import time
import uuid


class ConnectionFailure(RuntimeError):
    pass


class MissingApplication(ConnectionFailure):
    pass


def command_ids(catalog):
    entries = catalog.get('commands', catalog) if isinstance(catalog, dict) else catalog
    if isinstance(entries, dict):
        return set(entries)
    if isinstance(entries, list):
        return {item['id'] for item in entries if isinstance(item, dict) and isinstance(item.get('id'), str)}
    return set()


def probe(port, timeout=1.0):
    """None only for an unused port. Occupied/incompatible ports never cause a launch."""
    if type(port) is not int or not 1 <= port <= 65535:
        raise ConnectionFailure('Ungültiger VectorCraft-Port (1–65535).')
    ident = uuid.uuid4().hex
    request = {'id': ident, 'method': 'engine.commands', 'params': {}}
    try:
        sock = socket.create_connection(('127.0.0.1', port), timeout=timeout)
    except ConnectionRefusedError:
        return None
    except TimeoutError as exc:
        # Windows may time out instead of returning ECONNREFUSED on an unused loopback port.
        # A successful exclusive bind confirms absence; an occupied/filtered port stays an error.
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as check:
                if hasattr(socket, 'SO_EXCLUSIVEADDRUSE'):
                    check.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
                check.bind(('127.0.0.1', port))
        except OSError:
            raise ConnectionFailure(f'Port {port} ist belegt oder blockiert; keine bestätigte VectorCraft-Verbindung. Kein zweiter Prozess gestartet.') from exc
        return None
    except OSError as exc:
        if exc.errno in (errno.ECONNREFUSED, 10061):
            return None
        raise ConnectionFailure('Lokaler VectorCraft-Port nicht erreichbar: '+str(exc)) from exc
    try:
        with sock:
            sock.settimeout(timeout)
            sock.sendall((json.dumps(request)+'\n').encode())
            data = bytearray()
            deadline = time.monotonic()+timeout
            while b'\n' not in data:
                remaining = deadline-time.monotonic()
                if remaining <= 0:
                    raise TimeoutError('Protokollantwort fehlt')
                sock.settimeout(remaining)
                chunk = sock.recv(65536)
                if not chunk:
                    raise ValueError('Verbindung vor der Antwort geschlossen')
                data.extend(chunk)
                if len(data)>8_000_000:
                    raise ValueError('Protokollantwort zu groß')
            reply = json.loads(data.partition(b'\n')[0])
            if not isinstance(reply, dict) or reply.get('id') != ident or reply.get('ok') is not True:
                raise ValueError('Ungültige Protokollantwort')
            catalog = reply.get('result')
            if not {'path.create', 'object.rotate', 'document.node'} <= command_ids(catalog):
                raise ValueError('Kein passender VectorCraft-Befehlskatalog')
            return catalog
    except (OSError, ValueError) as exc:
        raise ConnectionFailure(f'Port {port} ist belegt, antwortet aber nicht als VectorCraft: {exc}. Kein zweiter Prozess gestartet.') from exc


def normalize_executable(value):
    if not value:
        return None
    path = Path(value).expanduser()
    if path.suffix.casefold() == '.app':
        for name in ('vectorcraft', 'VectorCraft'):
            binary = path/'Contents'/'MacOS'/name
            if binary.is_file():
                return binary.resolve()
        return None
    if path.is_file():
        return path.resolve()
    return None


def find_application(saved_path=None):
    # Explicit selections take priority. If they disappeared, automatic locations are still tried.
    candidates = [saved_path, os.environ.get('VECTORCRAFT_APP')]
    directory = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__).resolve().parent
    candidates += [directory/'vectorcraft.exe', directory/'vectorcraft', directory/'VectorCraft.app']
    if sys.platform == 'win32':
        for root in (os.environ.get('ProgramFiles'), os.environ.get('ProgramFiles(x86)')):
            if root:
                candidates += [Path(root)/'VectorCraft'/'vectorcraft.exe']
        local = os.environ.get('LOCALAPPDATA')
        if local:
            candidates += [Path(local)/'Programs'/'VectorCraft'/'vectorcraft.exe', Path(local)/'VectorCraft'/'vectorcraft.exe']
    elif sys.platform == 'darwin':
        candidates += [Path('/Applications/VectorCraft.app'), Path.home()/'Applications'/'VectorCraft.app']
    candidates += [shutil.which('vectorcraft')]
    for value in candidates:
        path = normalize_executable(value)
        if path:
            return path
    return None


@contextlib.contextmanager
def startup_lock(path, deadline):
    """Serialize launch decisions across Chat instances; keep the lock file's inode stable."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a+b') as stream:
        stream.seek(0, os.SEEK_END)
        if stream.tell() == 0:
            stream.write(b'0'); stream.flush()
        locked = False
        try:
            while not locked:
                try:
                    stream.seek(0)
                    if sys.platform == 'win32':
                        import msvcrt
                        msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
                    else:
                        import fcntl
                        fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    locked = True
                except OSError:
                    if time.monotonic() >= deadline:
                        raise ConnectionFailure('Ein anderer Chat startet VectorCraft noch; bitte erneut verbinden.') from None
                    time.sleep(0.1)
            yield
        finally:
            if locked:
                stream.seek(0)
                if sys.platform == 'win32':
                    import msvcrt
                    msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def ensure_connection(port, app_dir, saved_path=None, timeout=40):
    """Reuse a verified native app, or launch once and wait for a verified response."""
    catalog = probe(port)
    if catalog is not None:
        return {'catalog': catalog, 'started': False, 'path': None, 'process': None}
    app_dir = Path(app_dir)
    deadline = time.monotonic()+timeout
    with startup_lock(app_dir/'vectorcraft-start.lock', deadline):
        catalog = probe(port)
        if catalog is not None:
            return {'catalog': catalog, 'started': False, 'path': None, 'process': None}
        executable = find_application(saved_path)
        if executable is None:
            raise MissingApplication('VectorCraft wurde nicht gefunden. Bitte die installierte Anwendung einmal auswählen.')
        options = dict(stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, close_fds=True)
        if sys.platform == 'win32':
            options['creationflags'] = getattr(subprocess, 'CREATE_NO_WINDOW', 0x08000000)
        else:
            options['start_new_session'] = True
        log_path = app_dir/'vectorcraft-start.log'
        try:
            with log_path.open('ab') as log:
                process = subprocess.Popen([str(executable), '--control', str(port)], stderr=log, **options)
        except OSError as exc:
            raise ConnectionFailure('VectorCraft konnte nicht gestartet werden: '+str(exc)) from exc
        while time.monotonic() < deadline:
            try:
                catalog = probe(port, timeout=min(1.0, max(0.05, deadline-time.monotonic())))
            except ConnectionFailure:
                # A child may bind before its first UI frame can answer control messages.
                catalog = None
            if catalog is not None:
                return {'catalog': catalog, 'started': True, 'path': str(executable), 'process': process}
            if process.poll() is not None:
                raise ConnectionFailure(f'VectorCraft wurde beim Start beendet (Code {process.returncode}). Details: {log_path}')
            time.sleep(0.2)
        # Do not kill a native app: it may still be opening or holding a document.
        raise ConnectionFailure(f'VectorCraft antwortet nach {timeout:g} Sekunden nicht. Bitte erneut verbinden; Details: {log_path}')
