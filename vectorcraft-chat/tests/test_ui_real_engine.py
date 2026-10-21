"""Tk callbacks against the actual headless engine; HTTP replies are controlled fixtures."""
import contextlib
import json
import os
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch
import vectorcraft_chat as app
from engine_session import command, node, decode


@unittest.skipUnless(os.environ.get('VC_CHAT_REAL_CLI'), 'Requires real CLI and X display in CI')
class ActualEngineUITests(unittest.TestCase):
    def test_complete_chat_callbacks(self):
        with tempfile.TemporaryDirectory() as directory, app.MCPClient(os.environ['VC_CHAT_REAL_CLI'], headless=True) as client:
            command(client, 'file.new', {})
            base=Path(directory)
            prices={'test/model':{'id':'test/model','context_length':200000,'pricing':{'prompt':'0.000001','completion':'0.000002'}}}
            def control(method,params=None,port=7979):
                if method=='document.inspect':return decode(client.tool('inspect_document',params or {}))
                if method=='engine.commands':return {'commands':[{'id':'object.move','params':'{dx,dy}'}]}
                if method=='engine.execute':return command(client,params['command'],params.get('params',{}))
                raise AssertionError(method)
            with contextlib.ExitStack() as stack:
                for key,value in {'APP_DIR':base,'SETTINGS':base/'settings.json','HISTORY':base/'history.json','COSTS':base/'costs.json','KEY_FILE':base/'key'}.items():
                    stack.enter_context(patch.object(app,key,value))
                stack.enter_context(patch.object(app,'control',side_effect=control))
                stack.enter_context(patch.object(app,'MCPClient',side_effect=lambda *a,**k:contextlib.nullcontext(client)))
                stack.enter_context(patch.object(app,'mcp_executable',return_value='actual-engine-injected'))
                stack.enter_context(patch.object(app.messagebox,'askyesno',return_value=True))
                stack.enter_context(patch.object(app.messagebox,'showwarning'))
                stack.enter_context(patch.object(app,'model_catalog',return_value=prices))
                root=app.tk.Tk()
                try:
                    gui=app.App(root);root.update()
                    self.assertGreaterEqual(root.winfo_width(),420)
                    self.assertGreaterEqual(root.winfo_height(),360)
                    def wait():
                        deadline=time.monotonic()+20
                        while gui.busy or not gui.q.empty():
                            if time.monotonic()>deadline:raise AssertionError('UI callback timeout')
                            root.update();time.sleep(0.01)
                        root.update()
                    def send(text):
                        gui.entry.insert('1.0',text);gui.send();wait()
                    gui.inspect();wait();self.assertEqual(gui.command_ids,{'object.move'})
                    send('Konstruiere ein Dreieck');self.assertEqual(len(gui.pending),1)
                    gui.execute();wait();target=gui.last_triangle_id
                    self.assertIsInstance(target,int);self.assertFalse(gui.pending)
                    command(client,'select.set',{'ids':[]})
                    send('Drehe es um 30 Grad');gui.execute();wait()
                    self.assertAlmostEqual(node(client,target).get('rotation',0),30)
                    gui.key.set('dummy-test-key');gui.store_key();self.assertEqual(app.load_secret(),'dummy-test-key')
                    gui.refresh_models();wait();self.assertEqual(gui.models,['test/model'])
                    gui.model.set('test/model')
                    answer='Verschieben <vc_actions>{"actions":[{"method":"engine.execute","params":{"command":"object.move","params":{"dx":10,"dy":5}}}]}</vc_actions>'
                    before=node(client,target)['bounds']
                    with patch.object(app,'api_chat',return_value=(answer,{'cost':0.0002,'total_tokens':40})) as http:
                        send('Verschiebe das Dreieck etwas nach rechts')
                        self.assertEqual(http.call_args.args[1],'test/model')
                        self.assertEqual(len(gui.pending),1)
                    command(client,'select.set',{'ids':[]})
                    gui.execute();wait()
                    after=node(client,target)['bounds']
                    self.assertAlmostEqual(after['x']-before['x'],10)
                    self.assertAlmostEqual(after['y']-before['y'],5)
                    self.assertAlmostEqual(gui.session_spend_usd,0.0002)
                    with patch.object(app,'api_chat',return_value=('<vc_actions>{bad}</vc_actions>',{'cost':0.0003})):
                        send('Erkläre die Konstruktion')
                    self.assertFalse(gui.pending)
                    self.assertAlmostEqual(gui.session_spend_usd,0.0005)
                    self.assertAlmostEqual(app.read_json(app.COSTS,{})['spent_usd'],0.0005)
                    diag=base/'diagnostic.json'
                    with patch.object(app.filedialog,'asksaveasfilename',return_value=str(diag)):
                        gui.export_diagnostic()
                    self.assertNotIn('dummy-test-key',diag.read_text())
                    self.assertEqual(json.loads(diag.read_text())['settings']['model'],'test/model')
                    gui.save_settings();self.assertNotIn('dummy-test-key',app.SETTINGS.read_text())
                    print('PASS UI: actual triangle/rotation/move, selected model, key, diagnostic, costs including parser failure',flush=True)
                finally:
                    root.destroy()
