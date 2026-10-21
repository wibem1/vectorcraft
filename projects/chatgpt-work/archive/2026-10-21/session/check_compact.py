import sys,tempfile
sys.path.insert(0,'work/app')
import tkinter as tk
from tkinter import ttk
from vectorcraft_experiment import App
r=tk.Tk()
with tempfile.TemporaryDirectory(dir='work',ignore_cleanup_errors=True) as d:
 a=App(r,d)
 r.geometry('620x480');r.update()
 def walk(w):
  yield w
  for c in w.winfo_children():yield from walk(c)
 tabs=next(w for w in walk(r) if isinstance(w,ttk.Notebook))
 for tab in tabs.tabs():
  tabs.select(tab);r.update()
  for w in walk(r):
   if isinstance(w,ttk.Button) and w.winfo_viewable():
    assert w.winfo_rootx()+w.winfo_width()<=r.winfo_rootx()+r.winfo_width(),w.cget('text')
    assert w.winfo_rooty()+w.winfo_height()<=r.winfo_rooty()+r.winfo_height(),w.cget('text')
  assert a.logbox.winfo_height()>=60
 print('PASS: both tabs, all visible buttons within 620x480; log remains usable.')
 r.destroy()
