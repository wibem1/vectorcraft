"""Actual native GUI process, actual TCP, actual MCP bridge; no engine/control mocks."""
import contextlib
import json
import http.server
import threading
import urllib.request
import urllib.parse
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch
import app_connection as connection
import vectorcraft_chat as app


@contextlib.contextmanager
def isolated_keychain(base):
    if sys.platform != 'darwin':
        yield
        return
    path=str(base/'chat-ci.keychain-db')
    password=os.urandom(24).hex()
    subprocess.run(['security','create-keychain','-p',password,path],check=True,capture_output=True)
    try:
        subprocess.run(['security','unlock-keychain','-p',password,path],check=True,capture_output=True)
        with patch.dict(os.environ,{'VECTORCRAFT_CHAT_KEYCHAIN':path}):
            yield
    finally:
        subprocess.run(['security','delete-keychain',path],check=True,capture_output=True)


def capture_chat(root):
    root.lift();root.update()
    time.sleep(0.2);root.update()
    if sys.platform.startswith('linux'):
        subprocess.run(['import','-window',str(root.winfo_id()),'native-chat.png'],check=True,timeout=10)
    else:
        from PIL import ImageGrab
        x,y=root.winfo_rootx(),root.winfo_rooty()
        ImageGrab.grab(bbox=(x,y,x+root.winfo_width(),y+root.winfo_height())).save('native-chat.png')


def fail_modal(*args):
    raise AssertionError('Unexpected error dialog: '+str(args))


@unittest.skipUnless(os.environ.get('VC_CHAT_NATIVE_APP'), 'Requires actual native VectorCraft and virtual display')
class NativeStartupTests(unittest.TestCase):
    def test_chat_starts_native_app_and_edits_same_triangle(self):
        executable=str(Path(os.environ['VC_CHAT_NATIVE_APP']).resolve())
        processes=[]
        original_popen=subprocess.Popen
        def capture(command,**kwargs):
            if sys.platform=='win32' and Path(command[0]).stem=='vectorcraft-cli':
                self.assertTrue(kwargs.get('creationflags',0) & subprocess.CREATE_NO_WINDOW,'MCP bridge must not open a console')
            process=original_popen(command,**kwargs)
            if str(Path(command[0]).resolve())==executable:processes.append(process)
            return process
        with tempfile.TemporaryDirectory() as directory,contextlib.ExitStack() as stack:
            base=Path(directory)
            stack.enter_context(isolated_keychain(base))
            for key,value in {'APP_DIR':base,'SETTINGS':base/'settings.json','HISTORY':base/'history.json','COSTS':base/'costs.json','KEY_FILE':base/'key'}.items():
                stack.enter_context(patch.object(app,key,value))
            stack.enter_context(patch.dict(os.environ,{'VECTORCRAFT_APP':executable,'VECTORCRAFT_CONFIG_DIR':str(base/'native-profile'),'VECTORCRAFT_NO_PREFS':'1','OPENROUTER_API_KEY':''}))
            stack.enter_context(patch.object(connection.subprocess,'Popen',side_effect=capture))
            stack.enter_context(patch.object(app.messagebox,'askyesno',return_value=True))
            stack.enter_context(patch.object(app.messagebox,'showerror',side_effect=fail_modal))
            stack.enter_context(patch.object(app.filedialog,'askopenfilename',side_effect=AssertionError('Installed app must be found without a dialog')))
            with socket.socket() as sock:
                sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
            app.save_json(app.SETTINGS,{'port':port,'max_eur':0.1,'model':'unused-model'})
            root=app.tk.Tk()
            gui=None
            try:
                gui=app.App(root)
                self.assertEqual(str(gui.send_button['state']),'disabled')
                gui.entry.insert('1.0','Konstruiere ein Dreieck');gui.send()
                self.assertFalse(gui.pending)
                gui.entry.delete('1.0','end')
                def wait(condition,seconds=65):
                    deadline=time.monotonic()+seconds
                    while not condition():
                        root.update()
                        if gui.last_error and not gui.busy:raise AssertionError(gui.last_error)
                        if time.monotonic()>deadline:raise AssertionError('Native startup/UI deadline expired: '+gui.status.get())
                        time.sleep(0.01)
                    root.update()
                wait(lambda:gui.connected)
                self.assertEqual(len(processes),1)
                reused=connection.ensure_connection(port,base)
                self.assertFalse(reused['started']);self.assertEqual(len(processes),1)
                self.assertIsInstance(app.control('document.inspect',{'depth':0},port),dict)
                self.assertTrue(app.mcp_executable())
                for prompt in ('Konstruiere ein Dreieck','Drehe es um 30 Grad'):
                    gui.entry.insert('1.0',prompt);gui.send()
                    self.assertTrue(gui.pending)
                    gui.execute();wait(lambda:not gui.busy and gui.q.empty())
                    self.assertFalse(gui.pending)
                    if prompt.startswith('Konstruiere'):target=gui.last_triangle_id
                    else:self.assertEqual(gui.last_triangle_id,target)
                def inspect_node(ident):
                    return app.control('engine.execute',{'command':'document.node','params':{'id':ident,'summary':True}},port)
                triangle_before=inspect_node(target)
                paths=[{'points':[[20,20],[80,20],[80,70],[20,70]],'closed':True,'fill':'#00aa44'},
                       {'points':[[100,20],[120,40],[140,20],[160,40],[180,20]],'closed':False,'stroke':'#113355'}]
                from engine_session import object_ids
                before_ids=object_ids(app.control('document.inspect',{'depth':64},port))
                _,gui.pending=app.parse_actions('<vc_actions>'+json.dumps({'actions':[{'method':'mcp.draw_path','params':p} for p in paths]})+'</vc_actions>')
                gui.execute();wait(lambda:not gui.busy and gui.q.empty())
                added=object_ids(app.control('document.inspect',{'depth':64},port))-before_ids
                self.assertEqual(len(added),2)
                self.assertEqual(inspect_node(target),triangle_before)
                rectangle=next(i for i in added if inspect_node(i).get('anchors')==4)
                line=next(i for i in added if inspect_node(i).get('anchors')==5)
                line_before=inspect_node(line)
                # Actual independent engine edit between chat turns, no simulation.
                app.control('engine.execute',{'command':'select.set','params':{'ids':[rectangle]}},port)
                app.control('engine.execute',{'command':'object.move','params':{'dx':7,'dy':9}},port)
                manually_edited=inspect_node(rectangle)
                gui.pending=[{'method':'engine.execute','params':{'command':'object.move','params':{'id':rectangle,'dx':13,'dy':-4}}}]
                gui.execute();wait(lambda:not gui.busy and gui.q.empty())
                edited=inspect_node(rectangle)
                self.assertAlmostEqual(edited['bounds']['x']-manually_edited['bounds']['x'],13)
                self.assertAlmostEqual(edited['bounds']['y']-manually_edited['bounds']['y'],-4)
                self.assertEqual(inspect_node(line),line_before)
                self.assertEqual(inspect_node(target),triangle_before)
                self.assertEqual(gui.last_triangle_id,target)
                actual=app.control('engine.execute',{'command':'document.node','params':{'id':target,'summary':True}},port)
                self.assertAlmostEqual(actual['rotation'],30)
                self.assertEqual(actual['anchors'],3);self.assertTrue(actual['closed'])
                self.assertFalse(app.ensure_document(port))
                self.assertEqual(app.control('engine.execute',{'command':'document.node','params':{'id':target,'summary':True}},port),actual)
                self.assertEqual(gui.session_spend_usd,0)
                self.assertEqual(app.read_json(app.SETTINGS,{})['vectorcraft_app'],executable)
                # The OS itself must reject an invalid executable, without a fake child process.
                invalid=base/('invalid.exe' if sys.platform=='win32' else 'invalid-app')
                invalid.write_bytes(b'Invalid native executable\n');invalid.chmod(0o755)
                with socket.socket() as sock:
                    sock.bind(('127.0.0.1',0));unused=sock.getsockname()[1]
                with self.assertRaisesRegex(connection.ConnectionFailure,'konnte nicht gestartet'):
                    connection.ensure_connection(unused,base,str(invalid),timeout=5)
                # Exercise the actual provider HTTP/JSON code and the native engine together.
                # Only OpenRouter's remote endpoint is redirected to a local HTTP fixture.
                # This is explicitly not a paid live OpenRouter completion.
                requests=[]
                model='fixture/native-integration'
                answer='Verschieben <vc_actions>{"actions":[{"method":"engine.execute","params":{"command":"object.move","params":{"dx":17,"dy":-11}}}]}</vc_actions>'
                class Provider(http.server.BaseHTTPRequestHandler):
                    def log_message(self,*args):pass
                    def reply(self,value):
                        body=json.dumps(value).encode()
                        self.send_response(200);self.send_header('Content-Type','application/json')
                        self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
                    def do_GET(self):
                        requests.append(('GET',self.path,None,self.headers.get('Authorization')))
                        self.reply({'data':[{'id':model,'context_length':200000,'pricing':{'prompt':'0.0000001','completion':'0.0000002'}}]})
                    def do_POST(self):
                        payload=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                        requests.append(('POST',self.path,payload,self.headers.get('Authorization')))
                        self.reply({'choices':[{'message':{'content':answer}}],'usage':{'cost':0.0002,'total_tokens':40}})
                server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Provider)
                server.daemon_threads=True
                thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
                original_urlopen=urllib.request.urlopen
                def redirect(request,**kwargs):
                    self.assertEqual(urllib.parse.urlsplit(request.full_url).netloc,'openrouter.ai')
                    path=urllib.parse.urlsplit(request.full_url).path
                    local=urllib.request.Request(f'http://127.0.0.1:{server.server_port}'+path,data=request.data,headers=dict(request.header_items()),method=request.get_method())
                    return original_urlopen(local,**kwargs)
                try:
                    with patch.object(urllib.request,'urlopen',side_effect=redirect):
                        gui.key.set('dummy-native-key');gui.store_key()
                        self.assertEqual(app.load_secret(),'dummy-native-key')
                        gui.refresh_models();wait(lambda:not gui.busy and gui.q.empty())
                        self.assertEqual(gui.models,[model]);gui.model.set(model)
                        gui.entry.insert('1.0','Verschiebe das Objekt etwas nach rechts');gui.send()
                        wait(lambda:not gui.busy and gui.q.empty())
                        self.assertEqual(len(gui.pending),1)
                        post=[r for r in requests if r[0]=='POST']
                        self.assertEqual(len(post),1)
                        self.assertEqual(post[0][1],'/api/v1/chat/completions')
                        self.assertEqual(post[0][2]['model'],model)
                        self.assertEqual(post[0][2]['max_tokens'],2000)
                        self.assertIn(str(target),post[0][2]['messages'][0]['content'])
                        self.assertEqual(post[0][3],'Bearer dummy-native-key')
                        before=actual['bounds']
                        app.control('engine.execute',{'command':'select.set','params':{'ids':[]}},port)
                        gui.execute();wait(lambda:not gui.busy and gui.q.empty())
                        actual=app.control('engine.execute',{'command':'document.node','params':{'id':target,'summary':True}},port)
                        self.assertEqual(gui.last_triangle_id,target)
                        self.assertAlmostEqual(actual['rotation'],30)
                        self.assertAlmostEqual(actual['bounds']['x']-before['x'],17)
                        self.assertAlmostEqual(actual['bounds']['y']-before['y'],-11)
                        self.assertAlmostEqual(gui.session_spend_usd,0.0002)
                        self.assertAlmostEqual(app.stored_spend(),0.0002)
                        diagnostic=base/'diagnostic.json'
                        with patch.object(app.filedialog,'asksaveasfilename',return_value=str(diagnostic)):
                            gui.export_diagnostic()
                        self.assertNotIn('dummy-native-key',diagnostic.read_text())
                        self.assertEqual(json.loads(diagnostic.read_text())['settings']['model'],model)
                        app.save_secret('');self.assertEqual(app.load_secret(),'')
                finally:
                    server.shutdown();server.server_close();thread.join(timeout=5)
                self.assertIsNone(processes[0].poll(),'Native application must still be running')
                report={'status':'PASS','platform':sys.platform,'transport':'actual native TCP and CLI MCP --connect','provider':'local HTTP fixture using actual OpenRouter request/response code; no paid live completion','native_launches':len(processes),'port':port,'triangle_id':target,'node':actual,'fixture_accounted_cost_usd':gui.session_spend_usd,'actual_provider_charge_usd':0,'provider_http_requests':len(requests),'multi_object_paths_and_explicit_target':True,'manual_edit_preserved':True,'unrelated_objects_preserved':True,'os_rejected_invalid_executable':True,'key_store':'isolated actual macOS Keychain' if sys.platform=='darwin' else ('actual Windows DPAPI' if sys.platform=='win32' else 'restricted Linux file'),'secret_roundtrip_and_delete':True}
                Path('native-startup-report.json').write_text(json.dumps(report,indent=2))
                # Take the actual chat window for layout inspection; the X display is test-only.
                capture_chat(root)
                print('PASS NATIVE: Chat auto-start, protocol readiness, single instance, real remote triangle/30-degree rotation/move, provider HTTP fixture, zero external model charge',flush=True)
            finally:
                root.destroy()
                for process in processes:
                    if process.poll() is None:
                        process.terminate()
                        try:process.wait(timeout=10)
                        except subprocess.TimeoutExpired:process.kill();process.wait(timeout=5)
                log=base/'vectorcraft-start.log'
                if log.exists():
                    Path('native-startup.log').write_bytes(log.read_bytes())
                    print('NATIVE STARTUP STDERR:\n'+connection.log_tail(log,12000),flush=True)
