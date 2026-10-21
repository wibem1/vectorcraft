import io
import json
import os
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch
import vectorcraft_chat as app
from cost_control import admit, estimate


class Response:
    def __init__(self, value): self.value=value
    def __enter__(self): return io.BytesIO(json.dumps(self.value).encode())
    def __exit__(self, *args): pass


class ProviderTests(unittest.TestCase):
    def test_selected_model_key_output_limit_and_usage(self):
        def request(req, **kw):
            self.assertEqual(req.get_header('Authorization'),'Bearer dummy-test-key')
            payload=json.loads(req.data)
            self.assertEqual(payload['model'],'chosen/model')
            self.assertEqual(payload['max_tokens'],123)
            self.assertEqual(payload['usage'],{'include':True})
            return Response({'choices':[{'message':{'content':'Hallo'}}],'usage':{'cost':0.001}})
        with patch('urllib.request.urlopen',side_effect=request):
            text,usage=app.api_chat('dummy-test-key','chosen/model',[{'role':'user','content':'Hallo'}],123)
        self.assertEqual(text,'Hallo');self.assertEqual(usage['cost'],0.001)

    def test_401_explained_without_key(self):
        err=urllib.error.HTTPError('https://openrouter.ai',401,'unauthorized',{},io.BytesIO(b''))
        with patch('urllib.request.urlopen',side_effect=err):
            with self.assertRaisesRegex(RuntimeError,'HTTP 401'):
                app.api_chat('dummy-test-key','model',[])

    def test_timeout_no_retry(self):
        with patch('urllib.request.urlopen',side_effect=TimeoutError('timeout')) as call:
            with self.assertRaises(TimeoutError):app.api_chat('dummy-test-key','model',[])
            self.assertEqual(call.call_count,1)

    def test_empty_choices_and_error_response(self):
        for response in ({'choices':[]},{'error':{'message':'provider failed'}}):
            with patch('urllib.request.urlopen',return_value=Response(response)):
                with self.assertRaises((ValueError,RuntimeError)):
                    app.api_chat('dummy-test-key','model',[])

    def test_dynamic_model_catalog(self):
        with patch('urllib.request.urlopen',return_value=Response({'data':[{'id':'new/model','pricing':{'prompt':'0'}}]})):
            self.assertIn('pricing',app.model_catalog('')['new/model'])

    def test_secret_roundtrip_actual_platform(self):
        # A CI user's ephemeral OS store on Windows; temporary restricted file on Linux.
        if os.sys.platform=='darwin':self.skipTest('Avoid touching login keychain in unit tests')
        with tempfile.TemporaryDirectory() as d:
            with patch.object(app,'APP_DIR',Path(d)),patch.object(app,'KEY_FILE',Path(d)/'key'):
                app.save_secret('dummy-test-key-ä');self.assertEqual(app.load_secret(),'dummy-test-key-ä')
                app.save_secret('');self.assertEqual(app.load_secret(),'')
                if os.sys.platform!='win32':self.assertEqual((Path(d)/'key').stat().st_mode & 0o777,0o600)

    def test_diagnostic_redacts_secrets(self):
        value=app.safe_error('Bearer dummy-test-key sk-or-v1-secret123')
        self.assertNotIn('dummy-test-key',value);self.assertNotIn('secret123',value)
        app.event('test','Bearer dummy-test-key');self.assertNotIn('dummy-test-key',app.DIAG_EVENTS[-1]['info'])

    def test_destructive_and_file_actions_rejected(self):
        for method,params in [('engine.execute',{'command':'file.new'}),('engine.execute',{'command':'script.run'}),('ui.render',{'path':'x.png'})]:
            with self.assertRaises(ValueError):
                app.parse_actions('<vc_actions>'+json.dumps({'actions':[{'method':method,'params':params}]})+'</vc_actions>')


class CostTests(unittest.TestCase):
    model={'context_length':200000,'pricing':{'prompt':'0.000001','completion':'0.000002','request':'0'}}
    messages=[{'role':'user','content':'Hallo'}]
    def test_euro_conversion_and_reservation(self):
        reserve=admit(self.model,self.messages,2000,0,0.10,0.92)
        self.assertGreater(reserve,0)
        with self.assertRaisesRegex(ValueError,'überschritten'):
            admit(self.model,self.messages,2000,0.10,0.10,1.2)
    def test_nan_infinite_negative_and_unknown_costs(self):
        for value in ('nan','inf','-1'):
            with self.assertRaises(ValueError):admit(self.model,self.messages,2000,0,value,1)
        with self.assertRaises(ValueError):estimate({'pricing':{}},self.messages,2000)
        with self.assertRaises(ValueError):estimate(dict(self.model,pricing=dict(self.model['pricing'],image='1')),self.messages,2000)
    def test_atomic_settings_do_not_include_key(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'settings.json';app.save_json(path,{'model':'a/new-model'})
            self.assertEqual(app.read_json(path,{}),{'model':'a/new-model'})
            self.assertNotIn('key',path.read_text())
            self.assertFalse(path.with_suffix('.json.tmp').exists())


@unittest.skipUnless(os.environ.get('VC_CHAT_LIVE_HTTP')=='1','Live HTTP enabled only in CI')
class LivePublicOpenRouterTests(unittest.TestCase):
    def test_current_public_model_catalog(self):
        models=app.model_catalog('')
        self.assertGreater(len(models),10)
        self.assertTrue(any('pricing' in model for model in models.values()))
    def test_real_unauthorized_response(self):
        with self.assertRaisesRegex(RuntimeError,'HTTP 401'):
            app.api_chat('invalid-vectorcraft-ci-key','nonexistent/model',[{'role':'user','content':'test'}],1)


class InputAndLedgerTests(unittest.TestCase):
    def test_invalid_options(self):
        for port,budget in [('abc','0.1'),('0','0.1'),('65536','0.1'),('7979','nan'),('7979','inf'),('7979','-1')]:
            with self.assertRaises(ValueError):app.validated_options(port,budget)
        self.assertEqual(app.validated_options('7979','0,10'),(7979,0.1))
    def test_broken_ledger_never_resets_costs(self):
        with tempfile.TemporaryDirectory() as d,patch.object(app,'COSTS',Path(d)/'costs.json'):
            self.assertEqual(app.stored_spend(),0)
            for content in ('broken','{}','{"spent_usd":"nan"}'):
                app.COSTS.write_text(content)
                with self.assertRaises((ValueError,KeyError)):app.stored_spend()
            app.COSTS.write_text('{"spent_usd":0.031}')
            self.assertEqual(app.stored_spend(),0.031)
