import copy
import math
import unittest
from mandala import Mandala, settings, placement
from vc_workflow import Workflow, nodes
from legacy import ControlError, digest
from test_workflow import fixture


CONFIG={'count':4,'radius':100,'angle':0,'cx':200,'cy':200,'radial':True}


class Engine:
    def __init__(self):
        self.state=fixture()
        for n in self.state['document']['layers'][0]['kind']['children']:
            n['kind']['xf']=[2,0,0,3,50,60]
        self.calls=[]
        self.next_id=10
        self.saved=[]
        self.m=Mandala(lambda:copy.deepcopy(self.state),self.execute,lambda s:self.saved.append(copy.deepcopy(s)))
        self.w=Workflow(lambda:copy.deepcopy(self.state))

    def execute(self,name,params):
        self.calls.append((name,copy.deepcopy(params)))
        self.state['overview']['revision']+=1
        children=self.state['document']['layers'][0]['kind']['children']
        results=[]
        for step in params['commands']:
            p=step['params']
            if step['command']=='edit.clear':
                children[:]=[n for n in children if n['id'] not in p['ids']]
                results.append({})
            elif step['command']=='select.set': results.append({'ids':p['ids']})
            else:
                source=copy.deepcopy(nodes(self.state['document'])[p['ids'][0]])
                source['id']=self.next_id;self.next_id+=1
                a,b,c,d,e,f=p['matrix'];u,v,w,x,y,z=source['kind']['xf']
                source['kind']['xf']=[a*u+c*v,b*u+d*v,a*w+c*x,b*w+d*x,a*y+c*z+e,b*y+d*z+f]
                children.append(source);results.append({'ids':[source['id']]})
        return {'results':results}

    def start(self):self.m.start(self.w.inspect_selection(),CONFIG)


class MandalaTests(unittest.TestCase):
    def test_linked_copies_replace_only_owned(self):
        e=Engine();original=copy.deepcopy(e.state['document']);e.start()
        ids=set(map(int,e.m.session['owned']))
        self.assertEqual(len(ids),4)
        self.assertEqual(e.saved[0]['status'],'uncertain')
        e.m.update({**CONFIG,'count':6,'radius':180,'angle':45})
        ns=nodes(e.state['document'])
        self.assertFalse(ids & ns.keys())
        for i,n in nodes(original).items():
            if n['kind']['type']=='symbolinstance':self.assertEqual(ns[i],n)
        self.assertEqual(len(e.m.session['owned']),6)
        self.assertEqual(e.calls[0][0],'command.batch')

    def test_manual_changes_guard(self):
        for change in ('copy','source','definition','document','deleted'):
            with self.subTest(change=change):
                e=Engine();e.start();ns=nodes(e.state['document'])
                if change=='copy':ns[int(next(iter(e.m.session['owned'])))]['opacity']=0.5
                if change=='source':ns[2]['kind']['xf'][4]+=1
                if change=='definition':e.state['document']['symbols'][0]['art']={}
                if change=='document':e.state['identity']['active']=1
                if change=='deleted':e.state['document']['layers'][0]['kind']['children'].pop()
                with self.assertRaises(ControlError):e.m.update({**CONFIG,'radius':150})
                self.assertEqual(len(e.calls),1)

    def test_timeout_locks_and_never_retries(self):
        e=Engine();e.start()
        def fail(*args):raise ControlError('timeout')
        e.m.execute=fail
        with self.assertRaises(ControlError):e.m.update({**CONFIG,'count':5})
        self.assertEqual(e.m.session['status'],'uncertain')
        with self.assertRaises(ControlError):e.m.update(CONFIG)

    def test_storage_failure_prevents_batch(self):
        e=Engine()
        def fail(*args):raise OSError('disk full')
        e.m.save=fail
        with self.assertRaises(OSError):e.start()
        self.assertEqual(e.calls,[])

    def test_same_config_is_read_only(self):
        e=Engine();e.start();e.m.update(CONFIG)
        self.assertEqual(len(e.calls),1)

    def test_finish_preserves_document(self):
        e=Engine();e.start();before=copy.deepcopy(e.state)
        e.m.finish()
        self.assertEqual(e.state,before)
        self.assertIsNone(e.m.session)

    def test_cancelled_detection_stale_guard(self):
        e=Engine();selection=e.w.inspect_selection()
        e.state['overview']['revision']+=1
        with self.assertRaises(ControlError):e.m.start(selection,CONFIG)
        self.assertEqual(e.calls,[])

    def test_positions_and_rotation(self):
        c=settings(CONFIG)
        m=placement(c,0,[2,0,0,3,50,60])
        self.assertAlmostEqual(m[4]+50,200)
        self.assertAlmostEqual(m[5]+60,100)
        m=placement(c,1,[2,0,0,3,50,60])
        self.assertAlmostEqual(m[0],0)
        self.assertAlmostEqual(m[1],1)
        m=placement({**c,'radial':False},1,[2,0,0,3,50,60])
        self.assertEqual(m[:4],[1,0,0,1])

    def test_invalid_settings(self):
        for key,value in [('count',1),('count',73),('count','2.5'),('radius',float('nan')),('radius',-1),('angle',181)]:
            with self.subTest(key=key,value=value):
                with self.assertRaises((ControlError,ValueError)):settings({**CONFIG,key:value})

    def test_malformed_response_locks(self):
        e=Engine();e.m.execute=lambda *args:{}
        with self.assertRaises(ControlError):e.start()
        self.assertEqual(e.m.session['status'],'uncertain')


if __name__=='__main__':unittest.main(verbosity=2)
