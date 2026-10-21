from pathlib import Path
p=Path('work/app/vectorcraft_experiment.py');s=p.read_text(encoding='utf-8-sig')
s=s.replace("VERSION = '0.4.1'","VERSION = '0.4.2'").replace('Symbol-Experiment 0.4.1','Symbol-Experiment 0.4.2').replace("endswith('0.4.1')","endswith('0.4.2')")
s=s.replace("        self.last_error = None", "        self.last_error = None\n        self.user_hint = 'Klicke in VectorCraft ein Symbol an. Danach hier auf „Symbol bearbeiten“ klicken.'\n        self.detected_name = tk.StringVar(value='Der Symbolname wird automatisch erkannt.')",1)
s=s.replace("tabs.add(tools, text='Diagnose / Werkzeuge')", "tabs.add(tools, text='Weitere Funktionen')")
s=s.replace("        ttk.Label(name_row, text='Symbolname:').pack(side='left')\n        ttk.Entry(name_row, textvariable=self.name, width=24).pack(side='left', padx=6)", "        ttk.Label(name_row, textvariable=self.detected_name).pack(anchor='w')")
s=s.replace("text='2 · Änderung auf alle Instanzen übernehmen'", "text='2 · Änderung übernehmen (für alle Instanzen)'")
s=s.replace("ttk.Button(actions, text='Bearbeitungszustand prüfen', command=self.validate_session)", "ttk.Button(actions, text='Bearbeitete Form auswählen', command=self.select_edit_geometry)")
s=s.replace("        for row in [", "        names = ttk.Frame(tools)\n        names.pack(fill='x', pady=2)\n        ttk.Label(names, text='Symbolname für Zusatzfunktionen:').pack(side='left')\n        ttk.Entry(names, textvariable=self.name, width=20).pack(side='left', padx=5)\n        for row in [",1)
s=s.replace("[('Referenz speichern', self.snapshot)", "[('Bearbeitungszustand prüfen', self.validate_session)],\n            [('Referenz speichern', self.snapshot)",1)
s=s.replace("text = f'Bearbeitung offen: {p[\"name\"]} · Objekt-IDs {p[\"ids\"]}. In VectorCraft bearbeiten, dann diese Objekte auswählen und Schritt 2 anklicken.'", "text = f'„{p[\"name\"]}“ ist bereit zum Bearbeiten. Ändere die Form in VectorCraft. Danach auf „Bearbeitete Form auswählen“ und „Änderung übernehmen“ klicken.'")
s=s.replace("text = 'Bereit · Schritt 1: genau eine Symbolinstanz auswählen und deren Symbolnamen eingeben.'", "text = self.user_hint")
s=s.replace("                    self.last_error = error\n                    self.log", "                    self.last_error = error\n                    self.user_hint = error\n                    if label in ('Auswahl erkennen', 'Symbol bearbeiten', 'Änderung übernehmen', 'Bearbeitete Form auswählen'):\n                        messagebox.showinfo('Hinweis', error)\n                    self.log")
a=s.index('        name = self.name.get().strip()',s.index('    def edit_symbol(self):'));b=s.index('\n    def apply_symbol(self):',a)
s=s[:a]+'''        def detected(selection):
            self.name.set(selection['name'])
            self.detected_name.set('Erkanntes Symbol: ' + selection['name'])
            if not messagebox.askyesno('Symbol bearbeiten',
                    f'Erkannt: „{selection["name"]}“.\\n\\nDu kannst diese Form danach in VectorCraft verändern. '
                    'Mit „Änderung übernehmen“ werden später alle zugehörigen Instanzen aktualisiert.\\n\\n'
                    'Bitte mit einer gespeicherten Testkopie arbeiten. Jetzt bearbeiten?'):
                return
            self.work('Symbol bearbeiten', lambda: self.workflow.begin(expected=selection))
        self.work('Auswahl erkennen', self.workflow.inspect_selection, detected)
''' + s[b:]
s=s.replace("f'Die bearbeiteten Objekte {p[\"ids\"]} ersetzen die gemeinsame Definition von „{p[\"name\"]}“. '", "f'Deine Änderung an „{p[\"name\"]}“ wird jetzt auf alle zugehörigen Instanzen übertragen. '")
s=s.replace("self.work('Änderung auf alle Instanzen übernehmen', self.workflow.apply)", "self.work('Änderung übernehmen', self.workflow.apply, self.applied)")
a=s.index('    def validate_session(self):')
s=s[:a]+'''    def applied(self, result):
        self.user_hint = 'Fertig. Die Änderung wurde übernommen. Prüfe die Instanzen in VectorCraft und speichere die Testkopie.'
        messagebox.showinfo('Änderung übernommen', self.user_hint)

    def select_edit_geometry(self):
        def run():
            current = self.workflow.validate(require_selection=False)
            result = legacy.command('select.set', {'ids': self.workflow.pending['ids']})
            self.workflow.record('edit_geometry_selected', result=result)
            return 'Die bearbeitete Form ist in VectorCraft ausgewählt. Jetzt kannst du die Änderung übernehmen.'
        self.work('Bearbeitete Form auswählen', run)

''' + s[a:]
s=s.replace("assert '2 · Änderung auf alle Instanzen übernehmen' in labels", "assert '2 · Änderung übernehmen (für alle Instanzen)' in labels")
p.write_text(s,encoding='utf-8')
