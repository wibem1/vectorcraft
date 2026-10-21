"""Integration test against installed VectorCraft engine in an isolated MCP process."""
import json
import subprocess
from pathlib import Path
from unittest.mock import patch
import vc_workflow as vc
from mandala import Mandala, placement
import math


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
            selected=w.inspect_selection()
            assert selected['name']==first['name']
            w.begin(expected=selected)
            after_edit=vc.read_state()
            ids=w.pending['ids']
            assert after_edit['symbols']['symbols'][0]['instances']==1
            cmd('paint.setFill', {'color':'#0066ff', 'ids':ids})
            cmd('select.set', {'ids':[]})
            w.validate(require_selection=False)
            cmd('select.set', {'ids':ids})
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
            m=Mandala(vc.read_state, cmd)
            selection=w.inspect_selection()
            config={'count':4,'radius':80,'angle':0,'cx':200,'cy':200,'radial':True}
            originals=vc.nodes(after['document'])
            m.start(selection, config)
            assert len(m.session['owned'])==4
            first_ids=set(map(int,m.session['owned']))
            for i,node in originals.items():
                if node['kind']['type']=='symbolinstance': assert vc.nodes(vc.read_state()['document'])[i]==node
            config.update(count=6,radius=90,angle=30)
            m.update(config)
            final=vc.read_state()
            ns=vc.nodes(final['document'])
            assert not first_ids & ns.keys()
            assert len([n for n in ns.values() if n['kind']['type']=='symbolinstance'])==8
            base=m.session['source']['kind']['xf']
            for index,key in enumerate(m.session['owned']):
                xf=ns[int(key)]['kind']['xf']
                theta=2*math.pi*index/6-math.pi/2
                assert abs(xf[4]-(200+90*math.cos(theta)))<1e-7
                assert abs(xf[5]-(200+90*math.sin(theta)))<1e-7
                phi=2*math.pi*index/6+math.radians(30)
                assert abs(xf[0]-(math.cos(phi)*base[0]-math.sin(phi)*base[1]))<1e-7
            # A failing batch must restore the copies instead of partially removing them.
            before_failure=vc.read_state()
            try:
                cmd('command.batch',{'commands':[{'command':'edit.clear','params':{'ids':list(map(int,m.session['owned']))}},
                                                {'command':'not.a.command','params':{}}]})
                raise AssertionError('failed batch unexpectedly accepted')
            except RuntimeError: pass
            assert vc.digest(before_failure['document'])==vc.digest(vc.read_state()['document'])
            # The entire latest live update is one undo step.
            cmd('edit.undo')
            restored=vc.read_state()
            assert first_ids <= vc.nodes(restored['document']).keys()
            try:
                m.update(config)
                raise AssertionError('undo was not detected')
            except vc.ControlError: pass
            m.finish()
            assert m.session is None
            Path('work/mandala-engine-test.json').write_text(json.dumps({'test':'real engine / headless MCP',
                'note':'UI tab metadata supplied by adapter; no user document touched',
                'config':config,'after_update':final,'after_undo':restored,'events':m.events},ensure_ascii=False,indent=2),encoding='utf-8')
            print('PASS: radial copies, live count/radius/rotation, old copies replaced, originals retained, batch rollback, one-step undo and guard.')
    finally:
        p.terminate()
        p.wait(timeout=10)


if __name__=='__main__': run()
