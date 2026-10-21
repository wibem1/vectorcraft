import copy
import unittest
from unittest.mock import patch
from vc_workflow import Workflow, ControlError, read_state, valid_ids


def fixture():
    return {'document': {'symbols': [{'name': 'Blatt', 'art': {'color': 'red'}}],
            'layers': [{'id': 1, 'kind': {'type': 'layer', 'children': [
                {'id': 2, 'kind': {'type': 'symbolinstance', 'symbol': 'Blatt'}},
                {'id': 3, 'kind': {'type': 'symbolinstance', 'symbol': 'Blatt'}}]}}]},
            'identity': {'active': 0, 'title': 'Test', 'path': None, 'documents': ['Test']},
            'overview': {'revision': 1, 'selection': [2]},
            'symbols': {'symbols': [{'name': 'Blatt', 'instances': 2}]}}


class Fake:
    def __init__(self):
        self.state = fixture()
        self.calls = []
        self.saved = []
        self.w = Workflow(lambda: copy.deepcopy(self.state), self.execute, lambda p: self.saved.append(copy.deepcopy(p)))

    def execute(self, name, params):
        self.calls.append((name, params))
        self.state['overview']['revision'] += 1
        children = self.state['document']['layers'][0]['kind']['children']
        if name == 'symbol.edit':
            children[0] = {'id': 4, 'kind': {'type': 'path'}}
            self.state['overview']['selection'] = [4]
            return {'name': 'Blatt', 'ids': [4]}
        children[0] = {'id': 5, 'kind': {'type': 'symbolinstance', 'symbol': 'Blatt'}}
        self.state['document']['symbols'][0]['art'] = {'color': 'blue'}
        self.state['overview']['selection'] = [5]
        return {'name': 'Blatt', 'id': 5}


class WorkflowTests(unittest.TestCase):
    def test_automatic_detection_and_begin(self):
        f=Fake()
        selected=f.w.inspect_selection()
        self.assertEqual(selected['name'], 'Blatt')
        self.assertEqual(f.calls, [])
        f.w.begin(expected=selected)
        self.assertEqual(f.w.pending['name'], 'Blatt')
        self.assertEqual(f.calls[0], ('symbol.edit', {'id':2}))

    def test_changed_selection_after_confirmation_rejected(self):
        f=Fake(); selected=f.w.inspect_selection()
        f.state['overview']['selection']=[3]
        with self.assertRaises(ControlError): f.w.begin(expected=selected)
        self.assertEqual(f.calls, [])

    def test_changed_geometry_after_detection_rejected(self):
        f=Fake(); selected=f.w.inspect_selection()
        f.state['document']['layers'][0]['name']='changed'
        with self.assertRaises(ControlError): f.w.begin(expected=selected)
        self.assertEqual(f.calls, [])

    def test_detection_explains_wrong_object(self):
        for kind in ('path', 'group'):
            f=Fake(); f.state['document']['layers'][0]['kind']['children'][0]['kind']={'type':kind}
            with self.assertRaises(ControlError): f.w.inspect_selection()
            self.assertEqual(f.calls, [])
            self.assertEqual(f.w.events[-1]['objects'][0]['kind'],kind)

    def test_reselect_guard_accepts_only_valid_session(self):
        f=Fake(); f.w.begin()
        f.state['overview']['selection']=[]
        f.w.validate(require_selection=False)
        f.state['identity']['active']=1
        with self.assertRaises(ControlError): f.w.validate(require_selection=False)

    def test_two_steps(self):
        f = Fake(); f.w.begin('Blatt')
        self.assertEqual(len(f.calls), 1)
        self.assertEqual(f.w.pending['status'], 'editing')
        f.w.apply()
        self.assertEqual(f.calls[1], ('symbol.update', {'name': 'Blatt', 'ids': [4]}))
        self.assertIsNone(f.w.pending)
        self.assertEqual(f.saved[0]['status'], 'uncertain')
        self.assertTrue(f.w.events[-1]['definition_changed'])

    def test_preflight_rejections(self):
        for selection in ([], [2, 3], [999], [1]):
            with self.subTest(selection=selection):
                f=Fake(); f.state['overview']['selection']=selection
                with self.assertRaises(ControlError): f.w.begin('Blatt')
                self.assertEqual(f.calls, [])
        f=Fake()
        with self.assertRaises(ControlError): f.w.begin('Falsch')
        self.assertEqual(f.calls, [])

    def test_update_guards(self):
        for mutation in ('selection', 'document', 'definition', 'deleted', 'undo', 'instance'):
            with self.subTest(mutation=mutation):
                f=Fake(); f.w.begin('Blatt')
                if mutation=='selection': f.state['overview']['selection']=[3]
                if mutation=='document': f.state['identity']['active']=1
                if mutation=='definition': f.state['document']['symbols'][0]['art']={}
                if mutation=='deleted': f.state['document']['layers'][0]['kind']['children'].pop(0)
                if mutation=='undo': f.state['overview']['revision']=0
                if mutation=='instance': f.state['document']['layers'][0]['kind']['children'][0]['kind']['type']='symbolinstance'
                with self.assertRaises(ControlError): f.w.apply()
                self.assertEqual(len(f.calls), 1)
                self.assertEqual(f.w.pending['status'], 'editing')

    def test_timeout_never_retries(self):
        f=Fake(); f.w.begin('Blatt')
        def timeout(*args): raise ControlError('timeout: still running')
        f.w.execute=timeout
        with self.assertRaises(ControlError): f.w.apply()
        self.assertEqual(f.w.pending['status'], 'uncertain')
        with self.assertRaises(ControlError): f.w.apply()
        with self.assertRaises(ControlError): f.w.begin('Blatt')

    def test_invalid_edit_result_locks(self):
        for result in (None, {}, {'name':'Blatt', 'ids':[]}, {'name':'Anders','ids':[4]}):
            f=Fake(); f.w.execute=lambda *args: result
            with self.assertRaises(ControlError): f.w.begin('Blatt')
            self.assertEqual(f.w.pending['status'], 'uncertain')

    def test_post_read_failure_keeps_lock(self):
        f=Fake(); f.w.begin('Blatt')
        original=f.w.read; count=0
        def read():
            nonlocal count
            count+=1
            if count>1: raise ControlError('connection lost')
            return original()
        f.w.read=read
        with self.assertRaises(ControlError): f.w.apply()
        self.assertEqual(f.w.pending['status'], 'uncertain')

    def test_storage_failure_prevents_mutation(self):
        f=Fake()
        def fail(p): raise OSError('disk full')
        f.w.save=fail
        with self.assertRaises(OSError): f.w.begin('Blatt')
        self.assertEqual(f.calls, [])

    def test_invalid_ids(self):
        for ids in ([], [True], [1,1], [-1], ['4'], None): self.assertFalse(valid_ids(ids))

    def test_non_atomic_read_rejected(self):
        before={'revision':1, 'selection':[2], 'title':'Test'}
        after={**before,'revision':2}
        ui={'activeDocument':0, 'documents':[{'title':'Test'}]}
        with patch('vc_workflow.call', side_effect=[ui,before,after,ui]), patch('vc_workflow.command', side_effect=[fixture()['document'],{}]):
            with self.assertRaises(ControlError): read_state()


if __name__=='__main__': unittest.main(verbosity=2)

