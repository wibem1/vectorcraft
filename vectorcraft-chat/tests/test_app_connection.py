import contextlib
import json
import os
from pathlib import Path
import socket
import socketserver
import tempfile
import threading
import time
import unittest
from unittest.mock import Mock, patch
import app_connection as conn

CATALOG=[{'id':x} for x in ('path.create','object.rotate','document.node')]

@contextlib.contextmanager
def endpoint(mode='valid'):
    class Handler(socketserver.StreamRequestHandler):
        def handle(self):
            req=json.loads(self.rfile.readline())
            reply={'id':req['id'],'ok':True,'result':CATALOG}
            if mode=='wrong_id':reply['id']='wrong'
            if mode=='unrelated':reply['result']=[{'id':'hello'}]
            if mode=='malformed':self.wfile.write(b'not json\n');return
            if mode=='silent':time.sleep(0.2);return
            self.wfile.write((json.dumps(reply)+'\n').encode())
    class Server(socketserver.ThreadingTCPServer):
        allow_reuse_address=True
        daemon_threads=True
    with Server(('127.0.0.1',0),Handler) as server:
        thread=threading.Thread(target=lambda:server.serve_forever(poll_interval=0.01),daemon=True);thread.start()
        try:yield server.server_address[1]
        finally:server.shutdown();thread.join(timeout=2)

class ProtocolTests(unittest.TestCase):
    def test_actual_tcp_handshake_and_reuse(self):
        with endpoint() as port,tempfile.TemporaryDirectory() as directory,patch.object(conn.subprocess,'Popen') as launch:
            self.assertEqual(conn.probe(port),CATALOG)
            ready=conn.ensure_connection(port,directory)
            self.assertFalse(ready['started']);launch.assert_not_called()
    def test_wrong_service_or_invalid_id_never_launches(self):
        for mode in ('wrong_id','unrelated','malformed'):
            with self.subTest(mode=mode),endpoint(mode) as port,tempfile.TemporaryDirectory() as directory,patch.object(conn.subprocess,'Popen') as launch:
                with self.assertRaisesRegex(conn.ConnectionFailure,'belegt'):conn.ensure_connection(port,directory)
                launch.assert_not_called()
    def test_silent_port_has_bounded_timeout(self):
        with endpoint('silent') as port:
            started=time.monotonic()
            with self.assertRaises(conn.ConnectionFailure):conn.probe(port,timeout=0.05)
            self.assertLess(time.monotonic()-started,1)
    def test_unused_and_invalid_port(self):
        with socket.socket() as sock:
            sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
        self.assertIsNone(conn.probe(port))
        for value in (0,65536,True,'7979'):
            with self.assertRaises(conn.ConnectionFailure):conn.probe(value)

class LifecycleTests(unittest.TestCase):
    def test_launch_then_wait_and_serialize(self):
        with tempfile.TemporaryDirectory() as directory:
            process=Mock();process.poll.return_value=None
            with patch.object(conn,'probe',side_effect=[None,None,None,CATALOG]),patch.object(conn,'find_application',return_value=Path(directory)/'vectorcraft'),patch.object(conn.subprocess,'Popen',return_value=process) as launch,patch.object(conn.time,'sleep'):
                ready=conn.ensure_connection(7979,directory)
            self.assertTrue(ready['started']);self.assertEqual(ready['process'],process)
            self.assertEqual(launch.call_args.args[0], [str(Path(directory)/'vectorcraft'),'--control','7979'])
            self.assertNotIn('shell',launch.call_args.kwargs)
    def test_missing_app(self):
        with tempfile.TemporaryDirectory() as directory,patch.object(conn,'probe',return_value=None),patch.object(conn,'find_application',return_value=None):
            with self.assertRaises(conn.MissingApplication):conn.ensure_connection(7979,directory)
    def test_child_exits(self):
        process=Mock(returncode=42);process.poll.return_value=42
        with tempfile.TemporaryDirectory() as directory,patch.object(conn,'probe',return_value=None),patch.object(conn,'find_application',return_value=Path('vectorcraft')),patch.object(conn.subprocess,'Popen',return_value=process):
            with self.assertRaisesRegex(conn.ConnectionFailure,'Code 42'):conn.ensure_connection(7979,directory)
            process.kill.assert_not_called()
    def test_timeout_does_not_kill_or_retry_launch(self):
        process=Mock();process.poll.return_value=None
        with tempfile.TemporaryDirectory() as directory,patch.object(conn,'probe',return_value=None),patch.object(conn,'find_application',return_value=Path('vectorcraft')),patch.object(conn.subprocess,'Popen',return_value=process) as launch:
            with self.assertRaisesRegex(conn.ConnectionFailure,'antwortet'):conn.ensure_connection(7979,directory,timeout=0.02)
            self.assertEqual(launch.call_count,1);process.kill.assert_not_called()
    def test_existing_instance_appears_while_waiting_for_lock(self):
        with tempfile.TemporaryDirectory() as directory,patch.object(conn,'probe',side_effect=[None,CATALOG]),patch.object(conn.subprocess,'Popen') as launch:
            ready=conn.ensure_connection(7979,directory);self.assertFalse(ready['started']);launch.assert_not_called()
    def test_windows_suppresses_console(self):
        with tempfile.TemporaryDirectory() as directory,patch.object(conn.sys,'platform','win32'),patch.object(conn,'startup_lock',return_value=contextlib.nullcontext()),patch.object(conn,'probe',side_effect=[None,None,CATALOG]),patch.object(conn,'find_application',return_value=Path('vectorcraft.exe')),patch.object(conn.subprocess,'Popen') as launch:
            conn.ensure_connection(7979,directory)
            self.assertTrue(launch.call_args.kwargs['creationflags'] & 0x08000000)
            self.assertNotIn('start_new_session',launch.call_args.kwargs)
    def test_windows_discovery_and_saved_path(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'VectorCraft'/'vectorcraft.exe';path.parent.mkdir();path.touch()
            with patch.object(conn.sys,'platform','win32'),patch.dict(os.environ,{'ProgramFiles':directory,'VECTORCRAFT_APP':''}),patch.object(conn.shutil,'which',return_value=None):
                self.assertEqual(conn.find_application(),path.resolve())
                self.assertEqual(conn.find_application(str(path)),path.resolve())
    def test_macos_bundle_discovery(self):
        with tempfile.TemporaryDirectory() as directory:
            bundle=Path(directory)/'VectorCraft.app';exe=bundle/'Contents'/'MacOS'/'vectorcraft';exe.parent.mkdir(parents=True);exe.touch()
            with patch.object(conn.sys,'platform','darwin'):
                self.assertEqual(conn.find_application(str(bundle)),exe.resolve())
    def test_lock_serializes_threads(self):
        with tempfile.TemporaryDirectory() as directory:
            lock=Path(directory)/'startup.lock';entered=threading.Event();finished=threading.Event()
            def other():
                with conn.startup_lock(lock,time.monotonic()+2):entered.set()
                finished.set()
            with conn.startup_lock(lock,time.monotonic()+2):
                worker=threading.Thread(target=other);worker.start();self.assertFalse(entered.wait(0.1))
            self.assertTrue(finished.wait(2));worker.join();self.assertTrue(entered.is_set())

class StartupReadinessTests(unittest.TestCase):
    def test_child_bound_port_but_not_ready_yet(self):
        process=Mock();process.poll.return_value=None
        with tempfile.TemporaryDirectory() as directory,patch.object(conn,'probe',side_effect=[None,None,conn.ConnectionFailure('not ready'),CATALOG]),patch.object(conn,'find_application',return_value=Path('vectorcraft')),patch.object(conn.subprocess,'Popen',return_value=process) as launch,patch.object(conn.time,'sleep'):
            self.assertTrue(conn.ensure_connection(7979,directory)['started'])
            self.assertEqual(launch.call_count,1)
