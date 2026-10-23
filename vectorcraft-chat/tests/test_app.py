import unittest, socket, json, threading
from vectorcraft_chat import parse_actions, control, App
class Tests(unittest.TestCase):
 def test_chat(self):
  self.assertEqual(parse_actions('Gute Idee.'),('Gute Idee.',[]))
 def test_actions(self):
  out,a=parse_actions('Text <vc_actions>{"actions":[{"method":"engine.execute","params":{"command":"object.move","params":{"id":2,"dx":1,"dy":2}}}]}</vc_actions>')
  self.assertEqual((out,a[0]['params']['command']),('Text','object.move'))
 def test_reject(self):
  with self.assertRaises(ValueError):parse_actions('<vc_actions>{"actions":[{"method":"app.quit"}]}</vc_actions>')

 def test_partial_actions_rejected(self):
  with self.assertRaisesRegex(ValueError,'Unvollständiger Aktionsblock'):
   parse_actions('<vc_actions>{"actions":[{"method":"engine.execute"')
 def test_action_reply_survives_complete_block(self):
  txt='Vorschlag <vc_actions>{"actions":[{"method":"engine.execute","params":{"command":"shape.rectangle","params":{"x":5,"y":7,"width":30,"height":15}}}]}</vc_actions>'
  answer,actions=parse_actions(txt)
  self.assertEqual(answer,'Vorschlag')
  self.assertEqual(actions[0]['params']['command'],'shape.rectangle')

 def test_api_chat_exposes_finish_reason_without_extra_call(self):
  from unittest.mock import patch
  import io
  import vectorcraft_chat as vc
  response={'choices':[{'finish_reason':'length','message':{'content':'<vc_actions>{"actions":['}}],'usage':{'cost':0.001,'total_tokens':4005}}
  with patch.object(vc.urllib.request,'urlopen',return_value=io.BytesIO(json.dumps(response).encode())) as call:
   content,usage=vc.api_chat('test-key','test-model',[{'role':'user','content':'test'}],max_tokens=4000)
  self.assertEqual(usage['_finish_reason'],'length')
  self.assertEqual(usage['cost'],0.001)
  self.assertEqual(call.call_count,1)
  with self.assertRaisesRegex(ValueError,'Unvollständiger Aktionsblock'):
   parse_actions(content)
 def test_api_chat_normal_completion(self):
  from unittest.mock import patch
  import io
  import vectorcraft_chat as vc
  response={'choices':[{'finish_reason':'stop','message':{'content':'Fertig'}}],'usage':{'cost':0.002}}
  with patch.object(vc.urllib.request,'urlopen',return_value=io.BytesIO(json.dumps(response).encode())):
   content,usage=vc.api_chat('test-key','test-model',[{'role':'user','content':'test'}])
  self.assertEqual((content,usage['_finish_reason']),('Fertig','stop'))
 def test_ids(self):
  self.assertEqual(App.extract_ids({'commands':[{'id':'a'},{'id':'b'}]}),{'a','b'})
 def test_protocol(self):
  sock=socket.socket();sock.bind(('127.0.0.1',0));sock.listen(1);port=sock.getsockname()[1]
  def server():
   c,_=sock.accept();payload=c.recv(4096);req=json.loads(payload);c.sendall((json.dumps({'id':req['id'],'ok':True,'result':{'hello':req['method']}})+'\n').encode());c.close();sock.close()
  t=threading.Thread(target=server);t.start()
  self.assertEqual(control('ui.inspect',{},port),{'hello':'ui.inspect'});t.join()


class RegressionTests(unittest.TestCase):
 def test_invalid_json_action_is_safe(self):
  with self.assertRaisesRegex(ValueError,'NICHTS ausgeführt'):
   parse_actions('<vc_actions>{"actions":[{"method":"engine.execute","params":{"command":"path.rect"}}</vc_actions>')
 def test_secret_is_not_in_settings(self):
  from vectorcraft_chat import SETTINGS, KEY_FILE
  self.assertNotEqual(SETTINGS,KEY_FILE)
 def test_model_list_without_live_http(self):
  from unittest.mock import patch
  import io
  from vectorcraft_chat import list_models
  class Response:
   def __enter__(self):return io.BytesIO(b'{"data":[{"id":"z/test"},{"id":"a/test"}]}')
   def __exit__(self,*args):pass
  with patch('urllib.request.urlopen',return_value=Response()):
   self.assertEqual(list_models(''),['a/test','z/test'])

class Version020Tests(unittest.TestCase):
 def test_triangle_catalog_selection(self):
  from vectorcraft_chat import select_commands
  catalog=[{'id':'path.create','params':'points'}, {'id':'app.quit'},{'id':'document.inspect'},{'id':'object.delete'}]+[{'id':f'unrelated.{n}'} for n in range(1026)]
  ids=[x['id'] for x in select_commands(catalog,'Konstruiere ein Dreieck')]
  self.assertIn('path.create',ids)
  self.assertNotIn('app.quit',ids)
  self.assertLessEqual(len(ids),22)
 def test_truncated_actions(self):
  with self.assertRaisesRegex(ValueError,'Unvollständiger'):
   parse_actions('Text <vc_actions>{"actions": []}')
 def test_raw_json_rejected_as_actions(self):
  answer,actions=parse_actions('{"actions":[{"method":"engine.execute"}]}')
  self.assertEqual(actions,[])
 def test_reject_string_actions(self):
  with self.assertRaises(ValueError):parse_actions('<vc_actions>{"actions":"hi"}</vc_actions>')

class MCPRegressionTests(unittest.TestCase):
 def test_triangle_geometry(self):
  import math
  from vectorcraft_chat import triangle_points, detect_triangle
  points=triangle_points()
  self.assertEqual(len(points),3)
  lengths=[math.dist(points[i],points[(i+1)%3]) for i in range(3)]
  self.assertLess(max(lengths)-min(lengths),0.003)
  self.assertTrue(detect_triangle('Konstruiere ein Dreieck'))
  self.assertFalse(detect_triangle('Was ist ein Dreieck?'))
 def test_mcp_transport_and_draw_path(self):
  import tempfile,sys,os
  from pathlib import Path
  from vectorcraft_chat import MCPClient, triangle_points
  fake='''import sys,json
for ln in sys.stdin:
 r=json.loads(ln)
 if 'id' not in r:continue
 if r['method']=='initialize':res={'protocolVersion':'2025-06-18','capabilities':{'tools':{}},'serverInfo':{'name':'mock','version':'1'}}
 elif r['method']=='tools/call':
  assert r['params']['name']=='draw_path'
  assert r['params']['arguments']['closed'] is True
  assert len(r['params']['arguments']['points'])==3
  res={'content':[{'type':'text','text':'created a closed path'}]}
 else:res={}
 sys.stdout.write(json.dumps({'jsonrpc':'2.0','id':r['id'],'result':res})+'\\n');sys.stdout.flush()
'''
  with tempfile.TemporaryDirectory() as d:
   script=Path(d)/'fake.py';script.write_text(fake)
   from unittest.mock import patch
   original=__import__('subprocess').Popen
   def popen(command,**kw):return original([sys.executable,str(script)],**kw)
   with patch('vectorcraft_chat.subprocess.Popen',side_effect=popen):
    with MCPClient('mock.exe') as c:
     reply=c.tool('draw_path',{'points':triangle_points(),'closed':True})
   self.assertIn('created',reply['content'][0]['text'])

class FollowupRotationTests(unittest.TestCase):
 def test_rotation_intent(self):
  from vectorcraft_chat import rotate_request_degrees
  self.assertEqual(rotate_request_degrees('Drehe das Dreieck um 30 Grad'),30)
  self.assertEqual(rotate_request_degrees('Rotiere das Dreieck -15°'),-15)
  self.assertIsNone(rotate_request_degrees('Zeichne ein Dreieck'))
  self.assertIsNone(rotate_request_degrees('Drehe den Kreis um 30 Grad'))
 def test_mcp_inspection_selection_and_identity(self):
  from vectorcraft_chat import parse_mcp_inspection,inspection_selection,document_has_object
  data={'selection':[{'id':17}],'artboards':[{'layers':[{'children':[{'id':17,'kind':'Path'}]}]}]}
  reply={'content':[{'type':'text','text':json.dumps(data)}]}
  doc=parse_mcp_inspection(reply)
  self.assertEqual(inspection_selection(doc),[17])
  self.assertTrue(document_has_object(doc,17))
  self.assertFalse(document_has_object(doc,18))
 def test_unrecognized_inspection_fails_closed(self):
  from vectorcraft_chat import parse_mcp_inspection,inspection_selection,document_has_object
  doc=parse_mcp_inspection({'content':[{'type':'text','text':'not json'}]})
  self.assertEqual(inspection_selection(doc),[])
  self.assertFalse(document_has_object(doc,123))

class ExplicitTargetRegressionTests(unittest.TestCase):
 def test_explicit_target_is_not_redirected_to_last_triangle(self):
  from vectorcraft_chat import uses_verified_triangle_target
  action={'method':'engine.execute','params':{'command':'object.move','params':{'id':93,'dx':17,'dy':-11}}}
  self.assertFalse(uses_verified_triangle_target(action,2))
  action['params']['params']['id']=2
  self.assertTrue(uses_verified_triangle_target(action,2))
 def test_legacy_triangle_transform_without_id(self):
  from vectorcraft_chat import uses_verified_triangle_target
  action={'method':'engine.execute','params':{'command':'object.rotate','params':{'angle':30}}}
  self.assertTrue(uses_verified_triangle_target(action,2))
  self.assertFalse(uses_verified_triangle_target(action,None))
 def test_explicit_id_is_validated_as_integer(self):
  from vectorcraft_chat import uses_verified_triangle_target
  action={'method':'engine.execute','params':{'command':'object.scale','params':{'id':99,'factor':2}}}
  self.assertFalse(uses_verified_triangle_target(action,2))
  action['params']['params']['id']=2
  self.assertTrue(uses_verified_triangle_target(action,2))
 def test_other_commands_not_redirected(self):
  from vectorcraft_chat import uses_verified_triangle_target
  action={'method':'engine.execute','params':{'command':'path.create','params':{}}}
  self.assertFalse(uses_verified_triangle_target(action,2))

if __name__=="__main__":unittest.main()

class QualifiedRequestTests(unittest.TestCase):
 def test_local_shortcuts_do_not_discard_constraints(self):
  from vectorcraft_chat import detect_triangle, rotate_request_degrees
  for request in ('Konstruiere ein Dreieck und einen Kreis', 'Zeichne ein rotes Dreieck', 'Erstelle drei Dreiecke', 'Konstruiere ein Dreieck mit Seiten 3, 4, 5', 'Mach kein Dreieck'):
   self.assertFalse(detect_triangle(request), request)
  for request in ('Drehe Objekt 93 um 30 Grad', 'Drehe das zweite Dreieck um 30 Grad', 'Drehe es um 30 Grad und verschiebe es', 'Drehe alle Objekte um 30 Grad'):
   self.assertIsNone(rotate_request_degrees(request), request)
 def test_budget_above_ten_cents_rejected(self):
  from vectorcraft_chat import validated_options
  with self.assertRaises(ValueError): validated_options('7979', '0.11')

class PathValidationTests(unittest.TestCase):
 def test_invalid_path_rejected_before_execution(self):
  for params in ({'points':[[0,0],[1,float('nan')]]}, {'points':[[0,0],[1,1]],'closed':True}, {'points':[[0,0],[1,1]],'file':'x'}, {'points':[[0,0],[1,1]],'strokeWidth':-1}):
   with self.assertRaises(ValueError):
    parse_actions('<vc_actions>'+json.dumps({'actions':[{'method':'mcp.draw_path','params':params}]})+'</vc_actions>')
 def test_general_path_accepted(self):
  _, actions=parse_actions('<vc_actions>'+json.dumps({'actions':[{'method':'mcp.draw_path','params':{'points':[[0,0],[1,0],[1,1],[0,1]],'closed':True}}]})+'</vc_actions>')
  self.assertEqual(len(actions),1)

class ModelTargetTests(unittest.TestCase):
 def test_missing_or_noninteger_target_rejected(self):
  for params in ({'dx':1}, {'id':True,'dx':1}, {'id':'93','dx':1}):
   with self.assertRaisesRegex(ValueError,'Objekt-ID'):
    parse_actions('<vc_actions>'+json.dumps({'actions':[{'method':'engine.execute','params':{'command':'object.move','params':params}}]})+'</vc_actions>')
