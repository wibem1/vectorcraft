from pathlib import Path
p=Path('work/app/vectorcraft_experiment.py');s=p.read_text(encoding='utf-8-sig')
s=s.replace('from vc_workflow import Workflow, read_state','from vc_workflow import Workflow, read_state\nfrom mandala import Mandala, settings')
s=s.replace("VERSION = '0.4.2'","VERSION = '0.5'").replace('Symbol-Experiment 0.4.2','Symbol-Experiment 0.5').replace("endswith('0.4.2')","endswith('0.5')")
s=s.replace('        self.worker = None','''        self.mandala = Mandala(read_state, legacy.command, self.save_mandala)
        self.m_count = tk.StringVar(value='12')
        self.m_radius = tk.StringVar(value='160')
        self.m_angle = tk.StringVar(value='0')
        self.m_cx = tk.StringVar(value='400')
        self.m_cy = tk.StringVar(value='400')
        self.m_radial = tk.BooleanVar(value=True)
        self.m_live = tk.BooleanVar(value=True)
        self.m_job = None
        self.m_dirty = False
        self.worker = None''',1)
s=s.replace("        symbol = ttk.Frame(tabs, padding=8)","        radial = ttk.Frame(tabs, padding=8)\n        tabs.add(radial, text='Mandala · Live')\n        self.build_mandala(radial)\n        symbol = ttk.Frame(tabs, padding=8)")
s=s.replace("        except Exception as exc:\n            self.workflow.pending", "        except Exception as exc:\n            self.workflow.pending",1)
pos=s.index('        root.after(80, self.poll)')
s=s[:pos]+'''        try:
            path = self.storage / 'mandala.json'
            if path.exists():
                self.mandala.session = json.loads(path.read_text(encoding='utf-8'))
                if self.mandala.session:
                    self.mandala.session['status'] = 'uncertain'
                    self.m_live.set(False)
        except Exception as exc:
            self.mandala.session = {'status': 'uncertain'}
            self.m_live.set(False)
            self.log('Mandala-Sitzung nicht lesbar: ' + str(exc))
''' +s[pos:]
s=s.replace("        else:\n            text = self.user_hint\n        self.status_text", """        elif self.mandala.session:
            m = self.mandala.session
            if m['status'] == 'active':
                text = f'Mandala „{m["name"]}“ · ' + ('Live aktiv: Regler bewegen.' if self.m_live.get() else 'Live pausiert. „Aktualisieren“ übernimmt die Werte.')
            else:
                text = 'Mandala-Ergebnis unklar. Diagnose exportieren, Zeichnung prüfen und „Steuerung beenden“ anklicken.'
        else:
            text = self.user_hint
        self.status_text""")
s=s.replace("self.edit_button.configure(state='disabled' if self.busy or p else 'normal')", "self.edit_button.configure(state='disabled' if self.busy or p or self.mandala.session else 'normal')")
s=s.replace("        self.apply_button.configure(state='normal' if not self.busy and p and p['status'] == 'editing' else 'disabled')", """        self.apply_button.configure(state='normal' if not self.busy and p and p['status'] == 'editing' else 'disabled')
        self.m_start.configure(state='disabled' if self.busy or p or self.mandala.session else 'normal')
        self.m_update.configure(state='normal' if not self.busy and not p and self.mandala.session and self.mandala.session['status']=='active' else 'disabled')
        self.m_finish.configure(state='normal' if not self.busy and self.mandala.session else 'disabled')""")
s=s.replace("                    self.last_error = error\n                    self.user_hint", """                    self.last_error = error
                    if label.startswith('Mandala'):
                        self.m_live.set(False)
                        self.m_dirty = False
                        messagebox.showinfo('Mandala angehalten', error)
                    self.user_hint""")
s=s.replace("        if self.workflow.pending:\n            self.log('Andere Schreibaktionen", "        if self.mandala.session:\n            self.log('Bitte zuerst im Mandala-Reiter die Steuerung beenden. Das Mandala bleibt erhalten.')\n            return False\n        if self.workflow.pending:\n            self.log('Andere Schreibaktionen",1)
s=s.replace("'actions': self.audit,", "'mandala': self.mandala.session, 'mandala_events': self.mandala.events, 'actions': self.audit,")
s=s.replace("initialfile='VectorCraft-Diagnose-0.4.json'", "initialfile='VectorCraft-Diagnose-0.5.json'")
s=s.replace("        if self.workflow.pending and not messagebox.askyesno('Offene Bearbeitung',", "        if self.mandala.session and not messagebox.askyesno('Mandala-Steuerung', 'Beim Schließen bleiben alle Instanzen erhalten. Nach einem Neustart wird diese Steuerung gesperrt; es wird nichts automatisch verändert. Jetzt schließen?'):\n            return\n        if self.workflow.pending and not messagebox.askyesno('Offene Bearbeitung',")
s=s.replace("            assert app.edit_button.winfo_width()>100", "            assert 'Mandala starten' in labels\n            assert app.m_start.winfo_width()>80")
pos=s.index('    def save_pending(self, pending):')
s=s[:pos]+'''    def build_mandala(self, frame):
        ttk.Label(frame, text='Ein Symbol in VectorCraft auswählen, dann „Mandala starten“.').pack(anchor='w')
        actions = ttk.Frame(frame)
        actions.pack(fill='x', pady=5)
        self.m_start = ttk.Button(actions, text='Mandala starten', command=self.mandala_start)
        self.m_start.pack(side='left', padx=(0, 6))
        self.m_update = ttk.Button(actions, text='Aktualisieren', command=self.mandala_update)
        self.m_update.pack(side='left', padx=(0, 6))
        self.m_finish = ttk.Button(actions, text='Steuerung beenden', command=self.mandala_finish)
        self.m_finish.pack(side='left')
        grid = ttk.Frame(frame)
        grid.pack(fill='x')
        grid.columnconfigure(2, weight=1)
        for row, (label, variable, low, high) in enumerate([
                ('Anzahl', self.m_count, 2, 72), ('Radius', self.m_radius, 0, 2000), ('Motivdrehung °', self.m_angle, -180, 180)]):
            ttk.Label(grid, text=label).grid(row=row, column=0, sticky='w')
            ttk.Spinbox(grid, textvariable=variable, from_=low, to=high, width=7).grid(row=row, column=1, padx=8, pady=2)
            ttk.Scale(grid, from_=low, to=high, command=lambda value, var=variable: var.set(str(round(float(value))))).grid(row=row, column=2, sticky='ew')
            scale = grid.grid_slaves(row=row, column=2)[0]
            scale.set(float(variable.get()))
        center = ttk.Frame(frame)
        center.pack(fill='x', pady=4)
        for label, variable in [('Mitte X', self.m_cx), ('Y', self.m_cy)]:
            ttk.Label(center, text=label).pack(side='left')
            ttk.Entry(center, textvariable=variable, width=8).pack(side='left', padx=(5, 12))
        ttk.Checkbutton(center, text='Motive mitdrehen', variable=self.m_radial).pack(side='left')
        ttk.Checkbutton(frame, text='Live aktualisieren (ändert die Zeichnung)', variable=self.m_live, command=self.live_toggled).pack(anchor='w')
        for variable in (self.m_count, self.m_radius, self.m_angle, self.m_cx, self.m_cy, self.m_radial):
            variable.trace_add('write', lambda *args: self.schedule_mandala())

    def mandala_config(self):
        return settings({'count': self.m_count.get(), 'radius': self.m_radius.get(), 'angle': self.m_angle.get(),
                         'cx': self.m_cx.get(), 'cy': self.m_cy.get(), 'radial': self.m_radial.get()})

    def save_mandala(self, value):
        atomic_json(self.storage / 'mandala.json', value)

    def mandala_start(self):
        if not self.allow_other_write():
            return
        def inspect():
            selection = self.workflow.inspect_selection()
            current = read_state()
            if current['document'].get('artboards'):
                rect = current['document']['artboards'][0]['rect']
                selection['center'] = [(rect['x0']+rect['x1'])/2, (rect['y0']+rect['y1'])/2]
            return selection
        def detected(selection):
            if 'center' in selection:
                self.m_cx.set(f'{selection["center"][0]:g}')
                self.m_cy.set(f'{selection["center"][1]:g}')
            config = self.mandala_config()
            if not messagebox.askyesno('Mandala starten',
                    f'Vorlage: „{selection["name"]}“.\\n\\n{config["count"]} neue, verknüpfte Instanzen werden erzeugt. Die Vorlage bleibt erhalten. '
                    'Danach ändern die Regler dieses Mandala direkt.\\n\\nBitte mit einer gespeicherten Testkopie arbeiten. Starten?'):
                return
            self.m_dirty = False
            self.work('Mandala starten', lambda: self.mandala.start(selection, config))
        self.work('Mandala-Vorlage erkennen', inspect, detected)

    def schedule_mandala(self):
        if self.m_job is not None:
            self.root.after_cancel(self.m_job)
            self.m_job = None
        if self.mandala.session and self.mandala.session['status']=='active' and self.m_live.get():
            self.m_dirty = True
            self.m_job = self.root.after(400, self.flush_mandala)

    def flush_mandala(self):
        self.m_job = None
        if self._closed or not self.m_dirty or not self.m_live.get():
            return
        if self.busy:
            self.m_job = self.root.after(150, self.flush_mandala)
            return
        self.m_dirty = False
        self.mandala_update()

    def live_toggled(self):
        if self.m_live.get():
            self.schedule_mandala()
        else:
            self.m_dirty = False
            if self.m_job is not None:
                self.root.after_cancel(self.m_job)
                self.m_job = None
        self.refresh()

    def mandala_update(self):
        if not self.available() or self.workflow.pending:
            return
        try:
            config = self.mandala_config()
        except Exception as exc:
            self.m_live.set(False)
            self.m_dirty = False
            self.user_hint = str(exc)
            self.log(str(exc))
            messagebox.showinfo('Werte prüfen', str(exc))
            self.refresh()
            return
        self.work('Mandala aktualisieren', lambda: self.mandala.update(config))

    def mandala_finish(self):
        if not self.available() or not self.mandala.session:
            return
        if self.mandala.session['status']!='active' and not messagebox.askyesno('Unklares Ergebnis',
                'Bitte zuerst Diagnose exportieren und Zeichnung prüfen. Nur die Steuerungszuordnung beenden? Alle Objekte bleiben erhalten.'):
            return
        self.m_dirty = False
        if self.m_job is not None:
            self.root.after_cancel(self.m_job)
            self.m_job = None
        def done(result):
            self.user_hint = result
        self.work('Mandala-Steuerung beenden', self.mandala.finish, done)

''' +s[pos:]
p.write_text(s,encoding='utf-8')
