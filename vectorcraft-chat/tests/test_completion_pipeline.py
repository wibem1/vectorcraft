"""Exercise the production send worker, admission, settlement and parser together."""
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch
import vectorcraft_chat as app
from cost_control import estimate, MAX_COMPLETION_TOKENS


class CompletionPipelineTests(unittest.TestCase):
    model={'context_length':200000,'architecture':{'output_modalities':['text']},
           'pricing':{'prompt':'0.0000001','completion':'0.0000002'}}
    valid='<vc_actions>'+json.dumps({'actions':[{'method':'mcp.draw_path','params':{
        'points':[[10,10],[70,10],[40,60]],'closed':True,'fill':'#aabbcc'}}]})+'</vc_actions>'

    def run_worker(self, content, finish='stop', cost=0.001):
        gui=app.App.__new__(app.App)
        var=lambda v:SimpleNamespace(get=lambda:v)
        gui.entry=SimpleNamespace(get=lambda *a:'Zeichne ein blaues Dreieck',delete=Mock())
        gui.key=var('test-key');gui.port=var('7979');gui.budget=var('0.1');gui.model=var('test/model')
        gui.connected=True;gui.connected_port=7979;gui.busy=False;gui.cost_error=''
        gui.session_spend_usd=0;gui.settings={};gui.messages=[];gui.last_triangle_id=None
        gui.exec_button=SimpleNamespace(config=Mock());gui.write=Mock();gui.save_settings=Mock()
        jobs=[];gui.task=jobs.append
        with tempfile.TemporaryDirectory() as d, patch.object(app,'COSTS',Path(d)/'costs.json'),patch.object(app,'HISTORY',Path(d)/'history.json'):
            with patch.object(app,'control',side_effect=[{'layers':[]},{'commands':[{'id':'path.create'}]}]),patch.object(app,'model_catalog',return_value={'test/model':self.model}),patch.object(app,'api_chat',return_value=(content,{'cost':cost,'_finish_reason':finish})) as request:
                gui.send()
                self.assertEqual(len(jobs),1)
                try:
                    result=jobs[0]()
                except ValueError as exc:
                    result=exc
                self.assertEqual(request.call_count,1)
                self.assertEqual(request.call_args.kwargs['max_tokens'],MAX_COMPLETION_TOKENS)
                self.assertAlmostEqual(app.stored_spend(),cost)
        return result

    def test_valid_construction_reaches_actions_through_real_admission(self):
        result=self.run_worker(self.valid)
        self.assertEqual(result[0],'chat')
        self.assertEqual(result[2][0]['method'],'mcp.draw_path')

    def test_incomplete_and_invalid_replies_are_charged_without_retry(self):
        for content,finish in [(self.valid,'length'),(self.valid,'max_tokens'),
                (self.valid,None),(self.valid,'content_filter'),
                ('<vc_actions>{','stop'),('<vc_actions>bad</vc_actions>','stop')]:
            with self.subTest(finish=finish,content=content):
                self.assertIsInstance(self.run_worker(content,finish),ValueError)

    def test_admission_agrees_with_actual_output_limit(self):
        self.assertGreater(estimate(self.model,[{'content':'draw'}],MAX_COMPLETION_TOKENS),0)
        with self.assertRaises(ValueError):estimate(self.model,[{'content':'draw'}],MAX_COMPLETION_TOKENS+1)

    def test_ambiguous_json_rejected(self):
        for raw in ('{"actions":[],"actions":[]}','{"actions":[],"extra":true}',
                    '{"actions":[]}', '{"actions":[{"method":"ui.render","params":{"scale":NaN}}]}'):
            with self.subTest(raw=raw),self.assertRaises(ValueError):
                app.parse_actions('<vc_actions>'+raw+'</vc_actions>')

    def test_invalid_followup_rejected_before_any_execution(self):
        for cmd,params in [('object.move',{'id':2,'dx':1}),
                ('object.rotate',{'id':2,'angle':30,'copy':True}),
                ('object.rotate',{'id':2,'angle':30,'absolute':True}),
                ('object.scale',{'id':2,'factor':2}),('object.scale',{'id':2,'sx':0}),
                ('object.move',{'id':2,'dx':1e309,'dy':2})]:
            with self.subTest(cmd=cmd,params=params),self.assertRaises(ValueError):
                app.parse_actions('<vc_actions>'+json.dumps({'actions':[{'method':'engine.execute',
                    'params':{'command':cmd,'params':params}}]})+'</vc_actions>')
