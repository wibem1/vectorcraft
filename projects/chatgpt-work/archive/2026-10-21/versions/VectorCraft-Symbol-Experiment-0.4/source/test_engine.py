"""Integration test against installed VectorCraft engine in an isolated MCP process."""
import json
import subprocess
from pathlib import Path
from unittest.mock import patch
import vc_workflow as vc


def run():
    p = subprocess.Popen([r'C:\Program Files\VectorCraft\vectorcraft-cli.exe', 'mcp', '--headless'],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         text=True, encoding='utf-8')
    seq = 0
    def rpc(method, params):
        nonlocal seq
        seq += 1
        p.stdin.write(json.dumps({'jsonrpc':'2.0', 'id':seq, 'method':method, 'params':params})+'\n')
        p.stdin.flush()
        reply=json.loads(p.stdout.readline())
        if 'error' in reply: raise RuntimeError(reply['error'])
        return reply['result']
    def cmd(name, params=None):
        r=rpc('tools/call', {'name':'command_run', 'arguments':{'id':name, 'params':params or {}}})
        if r.get('isError'): raise RuntimeError(r)
        text=''.join(x['text'] for x in r['content'] if x['type']=='text')
        return json.loads(text)
    def call(method, params=None):
        if method=='ui.inspect': return {'activeDocument':0, 'documents':[{'title':'Integration 0.4'}]}
        if method=='document.inspect': return cmd(method, params)
        raise AssertionError(method)
    try:
        rpc('initialize', {'protocolVersion':'2024-11-05', 'capabilities':{}, 'clientInfo':{'name':'symbol-test','version':'0.4'}})
        cmd('file.new', {'title':'Integration 0.4', 'width':400, 'height':400})
        cmd('shape.rectangle', {'x':20,'y':20,'width':30,'height':40})
        first=cmd('symbol.new', {'name':'Test-Blatt'})
        cmd('symbol.place', {'name':first['name'], 'x':150,'y':150})
        with patch('vc_workflow.command', cmd), patch('vc_workflow.call', call):
            w=vc.Workflow(read=vc.read_state, execute=cmd)
            before=vc.read_state()
            w.begin(first['name'])
            after_edit=vc.read_state()
            ids=w.pending['ids']
            assert after_edit['symbols']['symbols'][0]['instances']==1
            cmd('paint.setFill', {'color':'#0066ff', 'ids':ids})
            w.validate()
            result=w.apply()
            after=vc.read_state()
            assert after['symbols']['symbols'][0]['instances']==2
            assert vc.definition(before['document'], first['name'])!=vc.definition(after['document'], first['name'])
            assert w.pending is None
            assert len([n for n in vc.nodes(after['document']).values() if n['kind']['type']=='symbolinstance'])==2
            report={'test':'installed VectorCraft CLI / headless MCP', 'result':result,
                    'note':'Real engine; ui.inspect tab metadata is supplied by test adapter. No existing user document modified.',
                    'before':before, 'after_edit':after_edit, 'after':after, 'events':w.events}
            Path('work/engine-test.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
            print('PASS: real symbol.edit -> paint.setFill -> symbol.update, definition changed, 2 linked instances retained.')
    finally:
        p.terminate()
        p.wait(timeout=10)


if __name__=='__main__': run()
