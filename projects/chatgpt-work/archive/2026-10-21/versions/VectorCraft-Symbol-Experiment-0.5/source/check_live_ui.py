from pathlib import Path
import sys
import tempfile
import time
import threading
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).parent))
import tkinter as tk
from vectorcraft_experiment import App
from test_mandala import Engine

root=tk.Tk()
root.withdraw()
with tempfile.TemporaryDirectory(dir='work',ignore_cleanup_errors=True) as directory:
    app=App(root,directory)
    root.update()
    engine=Engine();engine.start()
    app.mandala=engine.m
    app.m_count.set('4');app.m_radius.set('100');app.m_angle.set('0')
    app.m_cx.set('200');app.m_cy.set('200')
    entered=threading.Event();release=threading.Event()
    execute=engine.m.execute
    def slow(name,params):
        entered.set()
        assert release.wait(5)
        return execute(name,params)
    engine.m.execute=slow
    def pump_until(predicate,timeout=4):
        end=time.monotonic()+timeout
        while time.monotonic()<end:
            root.update()
            if predicate():return
            time.sleep(.01)
        raise AssertionError('GUI update timed out')
    app.m_count.set('5')
    app.mandala_update()
    pump_until(entered.is_set)
    # Changes made while an earlier update is in flight must not be lost.
    for count in range(6,16):app.m_count.set(str(count))
    app.m_radius.set('123')
    release.set()
    pump_until(lambda:not app.busy and engine.m.session['config']['count']==15)
    assert engine.m.session['config']['radius']==123
    assert len(engine.calls)==3, len(engine.calls)  # start, in-flight update, latest values
    app.m_live.set(False);app.live_toggled()
    app.m_count.set('20')
    end=time.monotonic()+.6
    while time.monotonic()<end:root.update();time.sleep(.01)
    assert len(engine.calls)==3
    # A pending live update must not run inside the close confirmation dialog.
    app.m_live.set(True);app.live_toggled()
    app.m_count.set('21')
    with patch('vectorcraft_experiment.messagebox.askyesno', return_value=False):
        app.close()
    assert app.m_job is None and not app.m_live.get()
    before=engine.state.copy()
    app.mandala_finish()
    pump_until(lambda:not app.busy and engine.m.session is None)
    assert len(engine.calls)==3
    app._closed=True
    root.destroy()
print('PASS: GUI coalesces slider changes, retains latest values during in-flight update, pauses live mode and ends without document writes.')
