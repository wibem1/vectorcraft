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

VERSION = '0.4'
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
        self.worker = None
        super().__init__(root)
        root.title('VectorCraft Symbol-Experiment 0.4')
        root.geometry('1120x830')
        root.minsize(1000, 720)
        frame = root.winfo_children()[0]
        frame.winfo_children()[0].configure(text='VectorCraft · Symbol-Experiment 0.4')
        # Replace the old experimental action with the explicit two-step workflow.
        diagnostics = frame.winfo_children()[4]
        for widget in diagnostics.winfo_children():
            widget.destroy()
        self.edit_button = ttk.Button(diagnostics, text='1 · Symbol bearbeiten', command=self.edit_symbol)
        self.edit_button.pack(side='left', padx=(0, 8))
        self.apply_button = ttk.Button(diagnostics, text='2 · Änderung auf alle Instanzen übernehmen', command=self.apply_symbol)
        self.apply_button.pack(side='left', padx=(0, 8))
        ttk.Button(diagnostics, text='Symbolstatus lesen', command=self.symbol_status).pack(side='left')
        flow = ttk.Frame(frame)
        flow.pack(fill='x', before=frame.winfo_children()[5], pady=6)
        ttk.Label(flow, textvariable=self.status_text, wraplength=1040, foreground='#174b76').pack(anchor='w')
        ttk.Label(flow, text='Nur an einer gespeicherten Testkopie arbeiten. Schritt 1 löst eine Instanz auf; Schritt 2 ersetzt die gemeinsame Definition.', wraplength=1040).pack(anchor='w', pady=3)
        actions = ttk.Frame(flow)
        actions.pack(anchor='w')
        ttk.Button(actions, text='Bearbeitungszustand prüfen', command=self.validate_session).pack(side='left', padx=(0, 8))
        ttk.Button(actions, text='Sitzung verwerfen …', command=self.discard_session).pack(side='left', padx=(0, 8))
        ttk.Button(actions, text='Alter symbol.replace-Test …', command=self.replace_symbol).pack(side='left')
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
        root.after(80, self.poll)
        self.refresh()

    def save_pending(self, pending):
        atomic_json(self.storage / 'pending.json', pending)

    def refresh(self):
        p = self.workflow.pending
        if self.busy:
            text = 'Prüfung/Befehl läuft. Bitte in VectorCraft kurz nicht weiterarbeiten.'
        elif p:
            if p['status'] == 'editing':
                text = f'Bearbeitung offen: {p["name"]} · Objekt-IDs {p["ids"]}. In VectorCraft bearbeiten, dann diese Objekte auswählen und Schritt 2 anklicken.'
            else:
                text = 'ERGEBNIS UNKLAR · Schreibzugriff gesperrt. Diagnose exportieren, Dokument prüfen. Kein Befehl wird automatisch wiederholt.'
        else:
            text = 'Bereit · Schritt 1: genau eine Symbolinstanz auswählen und deren Symbolnamen eingeben.'
        self.status_text.set(text)
        self.edit_button.configure(state='disabled' if self.busy or p else 'normal')
        self.apply_button.configure(state='normal' if not self.busy and p and p['status'] == 'editing' else 'disabled')

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
        if self.workflow.pending:
            self.log('Andere Schreibaktionen sind während einer offenen/unklaren Symbolbearbeitung gesperrt.')
            return False
        return True

    def edit_symbol(self):
        if not self.allow_other_write():
            return
        name = self.name.get().strip()
        if not name:
            self.log('Bitte den exakten Symbolnamen eingeben.')
            return
        if not messagebox.askyesno('Schritt 1 · Symbol bearbeiten',
                f'Gespeicherte Testkopie geöffnet?\n\nEine ausgewählte Instanz von „{name}“ wird in freie Geometrie aufgelöst. '
                'Andere Instanzen bleiben bis Schritt 2 unverändert.\n\nWährend der Prüfung bitte weder Dokument noch Auswahl wechseln. Fortfahren?'):
            return
        self.work('Symbol bearbeiten', lambda: self.workflow.begin(name))

    def apply_symbol(self):
        if not self.available():
            return
        p = self.workflow.pending
        if not p or p['status'] != 'editing':
            self.log('Keine bestätigte Bearbeitung offen.')
            return
        if not messagebox.askyesno('Schritt 2 · Alle Instanzen aktualisieren',
                f'Die bearbeiteten Objekte {p["ids"]} ersetzen die gemeinsame Definition von „{p["name"]}“. '
                'Alle verknüpften Instanzen werden aktualisiert.\n\nNur die Bearbeitungsobjekte auswählen. '
                'Während des Aufrufs nicht weiterarbeiten. Jetzt übernehmen?'):
            return
        self.work('Änderung auf alle Instanzen übernehmen', self.workflow.apply)

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
        path = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[('JSON', '*.json')], initialfile='VectorCraft-Diagnose-0.4.json')
        if not path:
            return
        report = {'version': VERSION, 'pending': self.workflow.pending, 'events': self.workflow.events,
                  'actions': self.audit, 'last_error': self.last_error, 'legacy_report': self.last_report,
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
            assert root.title().endswith('0.4')
            labels=[]
            def collect(widget):
                if isinstance(widget, ttk.Button): labels.append(widget.cget('text'))
                for child in widget.winfo_children(): collect(child)
            collect(root)
            assert 'Symbol aus Auswahl' in labels and '12 Instanzen' in labels
            assert '1 · Symbol bearbeiten' in labels
            assert '2 · Änderung auf alle Instanzen übernehmen' in labels
            assert app.apply_button.instate(['disabled'])
            assert app.name.get()=='Mandala-Blatt'
            assert app.edit_button.winfo_width()>100
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

