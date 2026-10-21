"""VectorCraft Symbol-Experiment 0.4, Windows portable application."""
import json
import os
import queue
import sys
import threading
import tempfile
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import legacy
from vc_workflow import Workflow, read_state
from mandala import Mandala, settings

VERSION = '0.5'
HOME = Path(os.environ.get('LOCALAPPDATA', str(Path.home()))) / 'VectorCraft-Symbol-Experiment-0.4'


def atomic_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(dir=path.parent, prefix='.writing-', suffix='.json')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


class App(legacy.App):
    def __init__(self, root, storage=HOME):
        self.storage = Path(storage)
        self.messages = queue.Queue()
        self.workflow = Workflow(save=self.save_pending)
        self.status_text = tk.StringVar(value='Bereit · Schritt 1: eine Symbolinstanz auswählen.')
        self.audit = []
        self.last_error = None
        self.user_hint = 'Klicke in VectorCraft ein Symbol an. Danach hier auf „Symbol bearbeiten“ klicken.'
        self.detected_name = tk.StringVar(value='Der Symbolname wird automatisch erkannt.')
        self.mandala = Mandala(read_state, legacy.command, self.save_mandala)
        self.m_count = tk.StringVar(value='12')
        self.m_radius = tk.StringVar(value='160')
        self.m_angle = tk.StringVar(value='0')
        self.m_cx = tk.StringVar(value='400')
        self.m_cy = tk.StringVar(value='400')
        self.m_radial = tk.BooleanVar(value=True)
        self.m_live = tk.BooleanVar(value=True)
        self.m_job = None
        self.m_dirty = False
        self.m_center_custom = False
        self.m_center_loading = False
        self.worker = None
        super().__init__(root)
        root.title('VectorCraft Symbol-Experiment 0.5')
        # Reuse the existing actions and state, with a compact two-tab layout.
        root.winfo_children()[0].destroy()
        width = min(720, max(540, root.winfo_screenwidth() - 80))
        height = min(600, max(420, root.winfo_screenheight() - 120))
        root.geometry(f'{width}x{height}')
        root.minsize(min(620, width), min(480, height))
        frame = ttk.Frame(root, padding=10)
        frame.pack(fill='both', expand=True)
        ttk.Label(frame, text='VectorCraft · Symbol-Experiment 0.5', font=('', 12, 'bold')).pack(anchor='w')
        top = ttk.Frame(frame)
        top.pack(fill='x', pady=(5, 6))
        ttk.Button(top, text='Verbindung', command=self.check).pack(side='left', padx=(0, 6))
        ttk.Button(top, text='Bericht exportieren', command=self.export).pack(side='left')
        tabs = ttk.Notebook(frame)
        tabs.pack(fill='x')
        radial = ttk.Frame(tabs, padding=8)
        tabs.add(radial, text='Mandala · Live')
        self.build_mandala(radial)
        symbol = ttk.Frame(tabs, padding=8)
        tools = ttk.Frame(tabs, padding=8)
        tabs.add(symbol, text='Symbol bearbeiten')
        tabs.add(tools, text='Weitere Funktionen')
        name_row = ttk.Frame(symbol)
        name_row.pack(fill='x', pady=(0, 6))
        ttk.Label(name_row, textvariable=self.detected_name).pack(anchor='w')
        self.edit_button = ttk.Button(symbol, text='1 · Symbol bearbeiten', command=self.edit_symbol)
        self.edit_button.pack(fill='x', pady=2)
        self.apply_button = ttk.Button(symbol, text='2 · Änderung übernehmen (für alle Instanzen)', command=self.apply_symbol)
        self.apply_button.pack(fill='x', pady=2)
        actions = ttk.Frame(symbol)
        actions.pack(fill='x', pady=(6, 0))
        ttk.Button(actions, text='Bearbeitete Form auswählen', command=self.select_edit_geometry).pack(side='left', padx=(0, 6))
        ttk.Button(actions, text='Sitzung verwerfen …', command=self.discard_session).pack(side='left')
        ttk.Label(symbol, text='Nur an einer gespeicherten Testkopie arbeiten.', foreground='#555').pack(anchor='w', pady=(5, 0))
        names = ttk.Frame(tools)
        names.pack(fill='x', pady=2)
        ttk.Label(names, text='Symbolname für Zusatzfunktionen:').pack(side='left')
        ttk.Entry(names, textvariable=self.name, width=20).pack(side='left', padx=5)
        for row in [
            [('Bearbeitungszustand prüfen', self.validate_session)],
            [('Referenz speichern', self.snapshot), ('Änderungen prüfen', self.diff), ('Symbolstatus lesen', self.symbol_status)],
            [('Symbol aus Auswahl', self.new_symbol), ('12 Instanzen', self.ring), ('Alter symbol.replace-Test …', self.replace_symbol)]
        ]:
            line = ttk.Frame(tools)
            line.pack(fill='x', pady=2)
            for text, action in row:
                ttk.Button(line, text=text, command=action).pack(side='left', padx=(0, 5))
        params = ttk.Frame(tools)
        params.pack(fill='x', pady=6)
        for title, value in [('Mittelpunkt X:', self.cx), ('Y:', self.cy), ('Radius:', self.radius)]:
            ttk.Label(params, text=title).pack(side='left')
            ttk.Entry(params, textvariable=value, width=7).pack(side='left', padx=(4, 8))
        ttk.Checkbutton(tools, text='Alle 2 Sekunden vergleichen (nur lesen)', variable=self.auto).pack(anchor='w')
        status = ttk.Label(frame, textvariable=self.status_text, wraplength=660, foreground='#174b76')
        status.pack(fill='x', pady=6)
        status.bind('<Configure>', lambda event: status.configure(wraplength=max(200, event.width)))
        ttk.Label(frame, text='Änderungsprotokoll:').pack(anchor='w')
        self.logbox = legacy.scrolledtext.ScrolledText(frame, height=7, width=45, wrap='word')
        self.logbox.pack(fill='both', expand=True)
        try:
            path = self.storage / 'pending.json'
            if path.exists():
                self.workflow.pending = json.loads(path.read_text(encoding='utf-8'))
                if self.workflow.pending:
                    self.workflow.pending['status'] = 'uncertain'
                    self.log('Offene Sitzung aus vorherigem Start: Übernahme gesperrt. Diagnose exportieren und Dokument prüfen; keine automatische Fortsetzung.')
        except Exception as exc:
            self.workflow.pending = {'status': 'uncertain', 'name': '?', 'ids': []}
            self.last_error = str(exc)
            self.log('Sitzungsdatei nicht lesbar. Schreibzugriff gesperrt: ' + str(exc))
        try:
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
        root.after(80, self.poll)
        self.refresh()

    def build_mandala(self, frame):
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
        self.m_scales = []
        for row, (label, variable, low, high) in enumerate([
                ('Anzahl', self.m_count, 2, 72), ('Radius', self.m_radius, 0, 2000), ('Motivdrehung °', self.m_angle, -180, 180)]):
            ttk.Label(grid, text=label).grid(row=row, column=0, sticky='w')
            ttk.Spinbox(grid, textvariable=variable, from_=low, to=high, width=7).grid(row=row, column=1, padx=8, pady=2)
            slider_value = tk.DoubleVar(value=float(variable.get()))
            self.m_scales.append(slider_value)
            ttk.Scale(grid, from_=low, to=high, variable=slider_value,
                      command=lambda value, var=variable: var.set(str(round(float(value))))).grid(row=row, column=2, sticky='ew')
            def sync(*args, var=variable, slider=slider_value):
                try:
                    number = float(var.get())
                    if legacy.math.isfinite(number): slider.set(number)
                except ValueError:
                    pass
            variable.trace_add('write', sync)
        center = ttk.Frame(frame)
        center.pack(fill='x', pady=4)
        for label, variable in [('Mitte X', self.m_cx), ('Y', self.m_cy)]:
            ttk.Label(center, text=label).pack(side='left')
            ttk.Entry(center, textvariable=variable, width=8).pack(side='left', padx=(5, 12))
        ttk.Checkbutton(center, text='Motive mitdrehen', variable=self.m_radial).pack(side='left')
        ttk.Checkbutton(frame, text='Live aktualisieren (ändert die Zeichnung)', variable=self.m_live, command=self.live_toggled).pack(anchor='w')
        for variable in (self.m_count, self.m_radius, self.m_angle, self.m_cx, self.m_cy, self.m_radial):
            variable.trace_add('write', lambda *args: self.schedule_mandala())
        for variable in (self.m_cx, self.m_cy):
            variable.trace_add('write', self.center_changed)

    def center_changed(self, *args):
        if not self.m_center_loading:
            self.m_center_custom = True

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
            if 'center' in selection and not self.m_center_custom:
                self.m_center_loading = True
                try:
                    self.m_cx.set(f'{selection["center"][0]:g}')
                    self.m_cy.set(f'{selection["center"][1]:g}')
                finally:
                    self.m_center_loading = False
            try:
                config = self.mandala_config()
            except Exception as exc:
                self.user_hint = str(exc)
                messagebox.showinfo('Werte prüfen', str(exc))
                return
            if not messagebox.askyesno('Mandala starten',
                    f'Vorlage: „{selection["name"]}“.\n\n{config["count"]} neue, verknüpfte Instanzen werden erzeugt. Die Vorlage bleibt erhalten. '
                    'Danach ändern die Regler dieses Mandala direkt.\n\nBitte mit einer gespeicherten Testkopie arbeiten. Starten?'):
                return
            self.m_dirty = False
            self.work('Mandala starten', lambda: self.mandala.start(selection, config))
        self.work('Mandala-Vorlage erkennen', inspect, detected)

    def schedule_mandala(self):
        if self.m_job is not None:
            self.root.after_cancel(self.m_job)
            self.m_job = None
        if self.mandala.session and (self.mandala.session['status']=='active' or self.busy) and self.m_live.get():
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

    def save_pending(self, pending):
        atomic_json(self.storage / 'pending.json', pending)

    def refresh(self):
        p = self.workflow.pending
        if self.busy:
            text = 'Prüfung/Befehl läuft. Bitte in VectorCraft kurz nicht weiterarbeiten.'
        elif p:
            if p['status'] == 'editing':
                text = f'„{p["name"]}“ ist bereit zum Bearbeiten. Ändere die Form in VectorCraft. Danach auf „Bearbeitete Form auswählen“ und „Änderung übernehmen“ klicken.'
            else:
                text = 'ERGEBNIS UNKLAR · Schreibzugriff gesperrt. Diagnose exportieren, Dokument prüfen. Kein Befehl wird automatisch wiederholt.'
        elif self.mandala.session:
            m = self.mandala.session
            if m['status'] == 'active':
                text = f'Mandala „{m["name"]}“ · ' + ('Live aktiv: Regler bewegen.' if self.m_live.get() else 'Live pausiert. „Aktualisieren“ übernimmt die Werte.')
            else:
                text = 'Mandala-Ergebnis unklar. Diagnose exportieren, Zeichnung prüfen und „Steuerung beenden“ anklicken.'
        else:
            text = self.user_hint
        self.status_text.set(text)
        self.edit_button.configure(state='disabled' if self.busy or p or self.mandala.session else 'normal')
        self.apply_button.configure(state='normal' if not self.busy and p and p['status'] == 'editing' else 'disabled')
        self.m_start.configure(state='disabled' if self.busy or p or self.mandala.session else 'normal')
        self.m_update.configure(state='normal' if not self.busy and not p and self.mandala.session and self.mandala.session['status']=='active' else 'disabled')
        self.m_finish.configure(state='normal' if not self.busy and self.mandala.session else 'disabled')

    def work(self, label, func, callback=None):
        if self.busy:
            self.log('Bitte warten: ein Vorgang läuft bereits.')
            return
        self.busy = True
        self.refresh()
        def job():
            try:
                value = func()
                self.messages.put((label, value, None, callback))
            except Exception as exc:
                self.messages.put((label, None, str(exc), None))
        self.worker = threading.Thread(target=job, daemon=True)
        self.worker.start()

    def poll(self):
        if self._closed:
            return
        try:
            while True:
                label, value, error, callback = self.messages.get_nowait()
                self.busy = False
                self.audit.append({'action': label, 'result': value, 'error': error})
                if error:
                    self.last_error = error
                    if label.startswith('Mandala'):
                        self.m_live.set(False)
                        self.m_dirty = False
                        messagebox.showinfo('Mandala angehalten', error)
                    self.user_hint = error
                    if label in ('Auswahl erkennen', 'Symbol bearbeiten', 'Änderung übernehmen', 'Bearbeitete Form auswählen'):
                        messagebox.showinfo('Hinweis', error)
                    self.log('FEHLER · ' + label + ': ' + error)
                else:
                    self.log('OK · ' + label + ': ' + legacy.compact(value, 350))
                    if callback:
                        try:
                            callback(value)
                        except Exception as exc:
                            self.last_error = str(exc)
                            self.log('Auswertungsfehler: ' + str(exc))
                self.refresh()
        except queue.Empty:
            pass
        self.root.after(80, self.poll)

    def available(self):
        if self.busy:
            self.log('Bitte laufenden Vorgang abwarten.')
            return False
        return True

    def allow_other_write(self):
        if not self.available():
            return False
        if self.mandala.session:
            self.log('Bitte zuerst im Mandala-Reiter die Steuerung beenden. Das Mandala bleibt erhalten.')
            return False
        if self.workflow.pending:
            self.log('Andere Schreibaktionen sind während einer offenen/unklaren Symbolbearbeitung gesperrt.')
            return False
        return True

    def edit_symbol(self):
        if not self.allow_other_write():
            return
        def detected(selection):
            self.name.set(selection['name'])
            self.detected_name.set('Erkanntes Symbol: ' + selection['name'])
            if not messagebox.askyesno('Symbol bearbeiten',
                    f'Erkannt: „{selection["name"]}“.\n\nDu kannst diese Form danach in VectorCraft verändern. '
                    'Mit „Änderung übernehmen“ werden später alle zugehörigen Instanzen aktualisiert.\n\n'
                    'Bitte mit einer gespeicherten Testkopie arbeiten. Jetzt bearbeiten?'):
                return
            self.work('Symbol bearbeiten', lambda: self.workflow.begin(expected=selection))
        self.work('Auswahl erkennen', self.workflow.inspect_selection, detected)

    def apply_symbol(self):
        if not self.available():
            return
        p = self.workflow.pending
        if not p or p['status'] != 'editing':
            self.log('Keine bestätigte Bearbeitung offen.')
            return
        if not messagebox.askyesno('Schritt 2 · Alle Instanzen aktualisieren',
                f'Deine Änderung an „{p["name"]}“ wird jetzt auf alle zugehörigen Instanzen übertragen. '
                'Alle verknüpften Instanzen werden aktualisiert.\n\nNur die Bearbeitungsobjekte auswählen. '
                'Während des Aufrufs nicht weiterarbeiten. Jetzt übernehmen?'):
            return
        self.work('Änderung übernehmen', self.workflow.apply, self.applied)

    def applied(self, result):
        self.user_hint = 'Fertig. Die Änderung wurde übernommen. Prüfe die Instanzen in VectorCraft und speichere die Testkopie.'
        messagebox.showinfo('Änderung übernommen', self.user_hint)

    def select_edit_geometry(self):
        def run():
            current = self.workflow.validate(require_selection=False)
            result = legacy.command('select.set', {'ids': self.workflow.pending['ids']})
            self.workflow.record('edit_geometry_selected', result=result)
            return 'Die bearbeitete Form ist in VectorCraft ausgewählt. Jetzt kannst du die Änderung übernehmen.'
        self.work('Bearbeitete Form auswählen', run)

    def validate_session(self):
        def run():
            value = self.workflow.validate()
            self.workflow.record('manual_validation', state=value)
            return 'Zustand gültig; Geometrie-IDs und gemeinsame Definition geprüft.'
        self.work('Bearbeitungszustand prüfen', run)

    def discard_session(self):
        if not self.available() or not self.workflow.pending:
            return
        if not messagebox.askyesno('Sitzung verwerfen',
                'Dies löscht nur die Sitzungszuordnung im Testprogramm. Es macht keine Dokumentänderung rückgängig. '
                'Die aufgelöste Geometrie bleibt bestehen.\n\nBei unklarem Ergebnis zuerst Diagnose exportieren und VectorCraft prüfen. '
                'Zum Rückgängigmachen die passenden Schritte in VectorCraft verwenden. Sitzung jetzt verwerfen?'):
            return
        try:
            self.save_pending(None)
            self.workflow.record('session_discarded', pending=self.workflow.pending)
            self.workflow.pending = None
            self.refresh()
        except OSError as exc:
            self.log('Sitzung konnte nicht verworfen werden: ' + str(exc))

    def new_symbol(self):
        if self.allow_other_write():
            super().new_symbol()

    def ring(self):
        if self.allow_other_write():
            super().ring()

    def replace_symbol(self):
        if self.allow_other_write() and messagebox.askyesno('Alter Diagnosetest',
                'symbol.replace tauscht die Symbolzuordnung ausgewählter Instanzen. Es definiert kein Symbol neu. '
                'Der alte Test bleibt zum Vergleich verfügbar. Trotzdem öffnen?'):
            super().replace_symbol()

    def export(self):
        if not self.available():
            return
        path = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[('JSON', '*.json')], initialfile='VectorCraft-Diagnose-0.5.json')
        if not path:
            return
        report = {'version': VERSION, 'pending': self.workflow.pending, 'events': self.workflow.events,
                  'mandala': self.mandala.session, 'mandala_events': self.mandala.events, 'actions': self.audit, 'last_error': self.last_error, 'legacy_report': self.last_report,
                  'reference': self.base, 'protocol': '127.0.0.1:7979',
                  'notice': 'Enthält Dokumentgeometrie und Titel. Vor Weitergabe prüfen. Abfragen sind nicht atomar; keine visuelle Erfolgsgarantie.'}
        try:
            atomic_json(Path(path), report)
            self.log('Diagnose gespeichert: ' + path)
        except Exception as exc:
            self.last_error = str(exc)
            self.log('Diagnose konnte nicht gespeichert werden: ' + str(exc))

    def close(self):
        if self.busy:
            messagebox.showwarning('Vorgang läuft', 'Bitte den laufenden Aufruf abwarten. Sein Ergebnis könnte bereits das Dokument verändern.')
            return
        self.m_live.set(False)
        self.m_dirty = False
        if self.m_job is not None:
            self.root.after_cancel(self.m_job)
            self.m_job = None
        self.refresh()
        if self.mandala.session and not messagebox.askyesno('Mandala-Steuerung', 'Beim Schließen bleiben alle Instanzen erhalten. Nach einem Neustart wird diese Steuerung gesperrt; es wird nichts automatisch verändert. Jetzt schließen?'):
            return
        if self.workflow.pending and not messagebox.askyesno('Offene Bearbeitung',
                'Eine Symbolbearbeitung ist offen oder unklar. Sie wird beim Neustart gesperrt. Vorher Diagnose exportieren? '
                '\n\nTrotzdem schließen?'):
            return
        super().close()


def main():
    root = tk.Tk()
    if '--smoke-test' in sys.argv:
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as directory:
            app = App(root, directory)
            root.update()
            assert root.title().endswith('0.5')
            labels=[]
            def collect(widget):
                if isinstance(widget, ttk.Button): labels.append(widget.cget('text'))
                for child in widget.winfo_children(): collect(child)
            collect(root)
            assert 'Symbol aus Auswahl' in labels and '12 Instanzen' in labels
            assert '1 · Symbol bearbeiten' in labels
            assert '2 · Änderung übernehmen (für alle Instanzen)' in labels
            assert app.apply_button.instate(['disabled'])
            assert app.name.get()=='Mandala-Blatt'
            assert 'Mandala starten' in labels
            assert app.m_start.winfo_width()>80
            assert root.winfo_width()<=720 and root.winfo_height()<=600
            root.after(200, root.destroy)
            root.mainloop()
    else:
        lock=None
        try:
            import msvcrt
            HOME.mkdir(parents=True, exist_ok=True)
            lock=open(HOME/'application.lock', 'a+b')
            if lock.tell()==0:
                lock.write(b'0'); lock.flush()
            lock.seek(0)
            msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
        except OSError as exc:
            messagebox.showerror('Start gesperrt', 'Das Programm läuft bereits oder der Sitzungsordner ist nicht beschreibbar.\n'+str(exc))
            root.destroy()
            return
        try:
            App(root)
            root.mainloop()
        finally:
            if lock: lock.close()


if __name__ == '__main__':
    main()

