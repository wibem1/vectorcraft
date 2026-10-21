"""Actual native GUI process, actual TCP, actual MCP bridge; no engine/control mocks."""
import contextlib
import json
import os
from pathlib import Path
import socket
import subprocess
import tempfile
import time
import unittest
from unittest.mock import patch
import app_connection as connection
import vectorcraft_chat as app


@unittest.skipUnless(os.environ.get('VC_CHAT_NATIVE_APP'), 'Requires actual native VectorCraft and virtual display')
class NativeStartupTests(unittest.TestCase):
    def test_chat_starts_native_app_and_edits_same_triangle(self):
        executable=str(Path(os.environ['VC_CHAT_NATIVE_APP']).resolve())
        processes=[]
        original_popen=subprocess.Popen
        def capture(command,**kwargs):
            process=original_popen(command,**kwargs)
            if str(Path(command[0]).resolve())==executable:processes.append(process)
            return process
        with tempfile.TemporaryDirectory() as directory,contextlib.ExitStack() as stack:
            base=Path(directory)
            for key,value in {'APP_DIR':base,'SETTINGS':base/'settings.json','HISTORY':base/'history.json','COSTS':base/'costs.json','KEY_FILE':base/'key'}.items():
                stack.enter_context(patch.object(app,key,value))
            stack.enter_context(patch.dict(os.environ,{'VECTORCRAFT_APP':executable,'VECTORCRAFT_CONFIG_DIR':str(base/'native-profile'),'VECTORCRAFT_NO_PREFS':'1','OPENROUTER_API_KEY':''}))
            stack.enter_context(patch.object(connection.subprocess,'Popen',side_effect=capture))
            stack.enter_context(patch.object(app.messagebox,'askyesno',return_value=True))
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
                actual=app.control('engine.execute',{'command':'document.node','params':{'id':target,'summary':True}},port)
                self.assertAlmostEqual(actual['rotation'],30)
                self.assertEqual(actual['anchors'],3);self.assertTrue(actual['closed'])
                self.assertEqual(gui.session_spend_usd,0)
                self.assertEqual(app.read_json(app.SETTINGS,{})['vectorcraft_app'],executable)
                report={'status':'PASS','transport':'actual native TCP and CLI MCP --connect','native_launches':len(processes),'port':port,'triangle_id':target,'node':actual,'model_cost_usd':gui.session_spend_usd}
                Path('native-startup-report.json').write_text(json.dumps(report,indent=2))
                # Take the actual chat window for layout inspection; the X display is test-only.
                root.update()
                subprocess.run(['import','-window',str(root.winfo_id()),'native-chat.png'],check=False,timeout=10)
                print('PASS NATIVE: Chat auto-start, protocol readiness, single instance, real remote triangle/30-degree rotation, zero model cost',flush=True)
            finally:
                root.destroy()
                for process in processes:
                    if process.poll() is None:
                        process.terminate()
                        try:process.wait(timeout=10)
                        except subprocess.TimeoutExpired:process.kill();process.wait(timeout=5)
