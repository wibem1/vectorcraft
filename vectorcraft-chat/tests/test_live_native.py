"""Opt-in real OpenRouter -> production chat -> native engine release gate.
No fixture provider, at most two zero-priced completions per platform; no retry.
"""
import contextlib
import json
import os
from pathlib import Path
import socket
import tempfile
import time
import unittest
from unittest.mock import patch
import vectorcraft_chat as app
from cost_control import money
from engine_session import object_ids


@unittest.skipUnless(os.environ.get('VC_CHAT_LIVE_NATIVE')=='1', 'Separate live native release gate')
class LiveNativeTests(unittest.TestCase):
    def test_actual_construction_and_followup(self):
        report={'status':'NOT_CONFIGURED','requests':0,'provider':'actual OpenRouter','platform':os.sys.platform}
        output=Path('live-native-report.json')
        root=None;gui=None
        try:
            key=os.environ.get('OPENROUTER_API_KEY','').strip()
            if not key:raise RuntimeError('OPENROUTER_API_KEY missing; release blocked; zero requests')
            executable=os.environ.get('VC_CHAT_NATIVE_APP','')
            if not executable or not Path(executable).is_file():raise RuntimeError('Actual native executable missing')
            catalog=app.model_catalog(key)
            candidates=[]
            for ident,model in catalog.items():
                pricing=model.get('pricing',{})
                if not ident.endswith(':free') or model.get('architecture',{}).get('output_modalities')!=['text']:
                    continue
                if not {'prompt','completion'} <= pricing.keys():continue
                try:
                    if all(money(v)==0 for v in pricing.values()):candidates.append(ident)
                except ValueError:continue
            if not candidates:raise RuntimeError('No confirmed zero-price text model; no request')
            model=sorted(candidates)[0];report['model']=model
            original_api=app.api_chat
            def counted_api(*args,**kwargs):
                if report['requests']>=2:raise AssertionError('Live request cap exceeded')
                # Re-check the selected model immediately before each real request.
                price=app.model_catalog(key)[model]['pricing']
                if not {'prompt','completion'}<=price.keys() or not all(money(v)==0 for v in price.values()):
                    raise AssertionError('Model no longer zero-priced; no request')
                report['requests']+=1
                answer,usage=original_api(*args,**kwargs)
                if usage.get('cost') is None or money(usage['cost'])!=0:
                    raise AssertionError('Zero charge not confirmed; no retry')
                return answer,usage
            with tempfile.TemporaryDirectory() as d,contextlib.ExitStack() as stack:
                base=Path(d)
                for name,value in {'APP_DIR':base,'SETTINGS':base/'settings.json','HISTORY':base/'history.json','COSTS':base/'costs.json'}.items():
                    stack.enter_context(patch.object(app,name,value))
                stack.enter_context(patch.dict(os.environ,{'VECTORCRAFT_APP':str(Path(executable).resolve()),'VECTORCRAFT_CONFIG_DIR':str(base/'native'),'VECTORCRAFT_NO_PREFS':'1'}))
                stack.enter_context(patch.object(app,'api_chat',side_effect=counted_api))
                stack.enter_context(patch.object(app.messagebox,'askyesno',return_value=True))
                def fail_dialog(*args):raise AssertionError('Unexpected application dialog')
                for name in ('showerror','showwarning'):
                    stack.enter_context(patch.object(app.messagebox,name,side_effect=fail_dialog))
                stack.enter_context(patch.object(app.filedialog,'askopenfilename',side_effect=fail_dialog))
                with socket.socket() as sock:
                    sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
                app.save_json(app.SETTINGS,{'port':port,'model':model,'max_eur':0.1})
                root=app.tk.Tk();gui=app.App(root)
                def wait(condition):
                    deadline=time.monotonic()+120
                    while not condition():
                        root.update()
                        if gui.last_error and not gui.busy:raise AssertionError(gui.last_error)
                        if time.monotonic()>deadline:raise AssertionError('Live native deadline expired; no retry')
                        time.sleep(0.02)
                    root.update()
                wait(lambda:gui.connected)
                before=object_ids(app.control('document.inspect',{'depth':64},port))
                gui.entry.insert('1.0','Zeichne genau ein blaues geschlossenes Dreieck mit den Eckpunkten (100,100), (260,100), (180,240). Verwende mcp.draw_path.');gui.send()
                wait(lambda:not gui.busy and gui.q.empty())
                self.assertEqual(len(gui.pending),1)
                self.assertEqual(gui.pending[0]['method'],'mcp.draw_path')
                gui.execute();wait(lambda:not gui.busy and gui.q.empty())
                added=object_ids(app.control('document.inspect',{'depth':64},port))-before
                self.assertEqual(len(added),1);target=added.pop()
                def node():return app.control('engine.execute',{'command':'document.node','params':{'id':target,'summary':True}},port)
                created=node();self.assertEqual(created['anchors'],3);self.assertTrue(created['closed'])
                app.control('ui.screenshot',{'path':str(Path('live-native-construction.png').resolve())},port)
                gui.entry.insert('1.0',f'Drehe ausschließlich Objekt {target} um 30 Grad mit object.rotate.');gui.send()
                wait(lambda:not gui.busy and gui.q.empty())
                self.assertEqual(len(gui.pending),1)
                self.assertEqual(gui.pending[0]['params']['command'],'object.rotate')
                self.assertEqual(gui.pending[0]['params']['params']['id'],target)
                gui.execute();wait(lambda:not gui.busy and gui.q.empty())
                edited=node();self.assertEqual(edited['id'],created['id'])
                self.assertAlmostEqual((edited['rotation']-created['rotation'])%360,30)
                self.assertEqual(object_ids(app.control('document.inspect',{'depth':64},port)),before|{target})
                app.control('ui.screenshot',{'path':str(Path('live-native-followup.png').resolve())},port)
                self.assertEqual(report['requests'],2);self.assertEqual(gui.session_spend_usd,0)
                report.update(status='PASS',target_id=target,rotation_degrees=30,actual_cost_usd=0)
        except Exception as exc:
            report.update(status='FAIL',error=app.safe_error(exc));raise
        finally:
            if root is not None:root.destroy()
            if gui is not None and gui.native_process is not None:
                gui.native_process.terminate()
                try:gui.native_process.wait(timeout=10)
                except Exception:gui.native_process.kill()
            output.write_text(json.dumps(report,indent=2))
