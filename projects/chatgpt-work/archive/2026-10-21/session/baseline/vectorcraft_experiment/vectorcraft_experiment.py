#!/usr/bin/env python3
"""VectorCraft Symbol-Experiment 0.3.1: dokumentierter Live-Control-Kanal; nur stdlib."""
import json, socket, hashlib, math, threading, tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from datetime import datetime

HOST,PORT='127.0.0.1',7979
MAX_CHANGES=120
class ControlError(Exception):pass

def call(method,params=None,timeout=20):
    req={'id':1,'method':method,'params':params or {}}
    try:
        with socket.create_connection((HOST,PORT),timeout=timeout) as s:
            s.settimeout(timeout);s.sendall((json.dumps(req,ensure_ascii=False)+'\n').encode('utf8'))
            buf=bytearray()
            while b'\n' not in buf:
                chunk=s.recv(65536)
                if not chunk:raise ControlError('VectorCraft hat die Verbindung geschlossen')
                buf.extend(chunk)
                if len(buf)>128*1024*1024:raise ControlError('Antwort ist zu groß')
            response=json.loads(buf.split(b'\n',1)[0])
    except (OSError,ValueError) as e:raise ControlError(str(e)) from e
    if not response.get('ok'):raise ControlError(str(response.get('error','Unbekannter Fehler')))
    return response.get('result')

def command(name,params=None):return call('engine.execute',{'command':name,'params':params or {}})
def canonical(x):return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def digest(x):return hashlib.sha256(canonical(x).encode('utf8')).hexdigest()
def compact(x,length=130):
    s=canonical(x)
    return s if len(s)<=length else s[:length]+'…'

def changes(old,new,path='',limit=MAX_CHANGES):
    """Struktureller, begrenzter JSON-Diff; keine Behauptung semantischer Zuordnung bei Array-Umsortierung."""
    out=[]
    def walk(a,b,p):
        if len(out)>=limit:return
        if a==b:return
        if isinstance(a,dict) and isinstance(b,dict):
            for k in sorted(a.keys()|b.keys()):
                q=p+'/'+str(k).replace('~','~0').replace('/','~1')
                if k not in a:out.append({'pfad':q,'art':'hinzugefügt','neu':b[k]})
                elif k not in b:out.append({'pfad':q,'art':'entfernt','alt':a[k]})
                else:walk(a[k],b[k],q)
                if len(out)>=limit:return
        elif isinstance(a,list) and isinstance(b,list):
            for i in range(max(len(a),len(b))):
                q=f'{p}/{i}'
                if i>=len(a):out.append({'pfad':q,'art':'hinzugefügt','neu':b[i]})
                elif i>=len(b):out.append({'pfad':q,'art':'entfernt','alt':a[i]})
                else:walk(a[i],b[i],q)
                if len(out)>=limit:return
        else:out.append({'pfad':p or '/','art':'geändert','alt':a,'neu':b})
    walk(old,new,path)
    return out

def state():
    # Nicht atomar: diese drei Aufrufe können bei simultaner Mausbearbeitung unterschiedliche Zeitpunkte erfassen.
    return {'document':command('document.json'),'symbols':command('symbol.list'),
            'overview':call('document.inspect',{'depth':0})}

class App:
    def __init__(self,root):
        self.root=root;root.title('VectorCraft Symbol-Experiment 0.3.1');root.geometry('870x675')
        self.base=None;self.busy=False;self.auto=tk.BooleanVar(value=False)
        self.last_report=None;self._closed=False;self._missed=0
        frame=ttk.Frame(root,padding=11);frame.pack(fill='both',expand=True)
        ttk.Label(frame,text='VectorCraft · Symbol- und Zustandsanalyse 0.3.1',font=('',14,'bold')).pack(anchor='w')
        ttk.Label(frame,text='Live-Control 127.0.0.1:7979 · keine KI-Kosten · schreibende Symbolbefehle nur nach ausdrücklichem Klick').pack(anchor='w',pady=(2,8))
        top=ttk.Frame(frame);top.pack(fill='x')
        for label,fn in [('Verbindung',self.check),('Referenz speichern',self.snapshot),('Änderungen prüfen',self.diff),('Bericht exportieren',self.export)]:
            ttk.Button(top,text=label,command=fn).pack(side='left',padx=(0,7),pady=3)
        middle=ttk.Frame(frame);middle.pack(fill='x',pady=(4,4))
        ttk.Label(middle,text='Symbolname:').pack(side='left');self.name=tk.StringVar(value='Mandala-Blatt')
        ttk.Entry(middle,textvariable=self.name,width=22).pack(side='left',padx=(4,8))
        ttk.Button(middle,text='Symbol aus Auswahl',command=self.new_symbol).pack(side='left',padx=3)
        ttk.Button(middle,text='12 Instanzen',command=self.ring).pack(side='left',padx=3)
        diagnostics=ttk.Frame(frame);diagnostics.pack(fill='x',pady=(4,4))
        ttk.Button(diagnostics,text='Symbol-Neudefinition testen',command=self.replace_symbol).pack(side='left',padx=(0,7))
        ttk.Button(diagnostics,text='Symbolstatus lesen',command=self.symbol_status).pack(side='left',padx=(0,7))
        ttk.Label(diagnostics,text='Neudefinition wirkt auf das in VectorCraft gewählte Symbol.').pack(side='left')
        params=ttk.Frame(frame);params.pack(fill='x',pady=(3,5))
        self.cx=tk.StringVar(value='400');self.cy=tk.StringVar(value='400');self.radius=tk.StringVar(value='160')
        for title,v in [('Mittelpunkt X:',self.cx),('Y:',self.cy),('Radius:',self.radius)]:
            ttk.Label(params,text=title).pack(side='left');ttk.Entry(params,textvariable=v,width=7).pack(side='left',padx=(4,12))
        ttk.Checkbutton(frame,text='Automatisch alle 2 Sekunden vergleichen (nur lesen)',variable=self.auto).pack(anchor='w',pady=4)
        ttk.Label(frame,text='Änderungsprotokoll (JSON-Pfade; Symboländerungen gesondert):').pack(anchor='w')
        self.logbox=scrolledtext.ScrolledText(frame,height=29,wrap='word');self.logbox.pack(fill='both',expand=True)
        ttk.Label(frame,text='Hinweis: Dokumentabfragen sind nicht atomar. Bei manuellen Änderungen während des Auslesens erneut prüfen. Array-Indizes sind keine stabilen Objekt-IDs.',foreground='#555').pack(anchor='w',pady=(5,0))
        root.after(2000,self.tick);root.protocol('WM_DELETE_WINDOW',self.close)
    def close(self):self._closed=True;self.root.destroy()
    def log(self,s):
        if self._closed:return
        self.logbox.insert('end',datetime.now().strftime('%H:%M:%S')+'  '+s+'\n');self.logbox.see('end')
    def work(self,label,func,callback=None):
        if self.busy:return
        self.busy=True
        def job():
            try:
                value=func()
                def finish():
                    if not self._closed:
                        self.log('✓ '+label+': '+str(value))
                        if callback:callback(value)
            except Exception as exc:
                msg=str(exc)
                def finish():
                    if not self._closed:self.log('✗ '+label+': '+msg)
            finally:
                def done():
                    if not self._closed:self.busy=False
                try:self.root.after(0,finish);self.root.after(0,done)
                except RuntimeError:pass
        threading.Thread(target=job,daemon=True).start()
    def check(self):self.work('Verbindung',lambda: 'Live-Control antwortet; '+compact(command('symbol.list'),230))
    def snapshot(self):
        def get():return state()
        def done(v):self.base=v;self.log('Referenz erfasst: '+digest(v)[:12])
        self.work('Referenz lesen',get,done)
    def diff(self):
        if self.base is None:self.log('Bitte zuerst Referenz speichern.');return
        def get():return state()
        def done(v):
            old=self.base;self.base=v
            report={'zeit':datetime.now().isoformat(timespec='seconds'),'vorher_hash':digest(old),
                    'nachher_hash':digest(v),'symbol_aenderungen':changes(old['symbols'],v['symbols'],'/symbols'),
                    'dokument_aenderungen':changes(old['document'],v['document'],'/document'),
                    'auswahl_und_uebersicht':changes(old['overview'],v['overview'],'/overview'),
                    'hinweis':'Struktureller Vergleich, nicht semantische Objektverfolgung; bei Listenverschiebungen können Indizes wechseln.'}
            self.last_report=report
            if report['vorher_hash']==report['nachher_hash']:
                if not self.auto.get():self.log('Keine Änderungen erkannt.')
                return
            categories=[('Symbole',report['symbol_aenderungen']),('Dokument',report['dokument_aenderungen']),('Auswahl/Übersicht',report['auswahl_und_uebersicht'])]
            self.log('ÄNDERUNG erkannt: '+', '.join(f'{name}: {len(items)}' for name,items in categories))
            for title,items in categories:
                for item in items[:12]:
                    self.log('  '+title+' '+item['art']+' '+item['pfad']+' '+
                             ('ALT '+compact(item['alt'])+' ' if 'alt' in item else '')+
                             ('NEU '+compact(item['neu']) if 'neu' in item else ''))
                if len(items)>12:self.log(f'  … {len(items)-12} weitere {title}-Änderungen im Exportbericht')
                if len(items)>=MAX_CHANGES:self.log('  WARNUNG: Diff auf '+str(MAX_CHANGES)+' Einträge begrenzt')
        self.work('Zustandsvergleich',get,done)
    def export(self):
        if self.last_report is None:self.log('Noch kein Änderungsbericht vorhanden.');return
        p=filedialog.asksaveasfilename(defaultextension='.json',filetypes=[('JSON','*.json')],initialfile='VectorCraft-Aenderungen.json')
        if not p:return
        try:
            with open(p,'w',encoding='utf8') as f:json.dump(self.last_report,f,ensure_ascii=False,indent=2)
            self.log('Bericht gespeichert: '+p)
        except OSError as e:self.log('Fehler beim Export: '+str(e))
    def new_symbol(self):
        n=self.name.get().strip()
        if not n:self.log('Symbolname fehlt.');return
        if not messagebox.askyesno('Symbol anlegen','Aus der aktuellen Auswahl ein Symbol erzeugen?'):return
        self.work('Symbol anlegen',lambda:command('symbol.new',{'name':n}))
    def symbol_status(self):
        def status():
            v=state()
            return {'symbol_list':v['symbols'],'document_keys':list(v['document']) if isinstance(v['document'],dict) else type(v['document']).__name__,
                    'revision':v['overview'].get('revision') if isinstance(v['overview'],dict) else None}
        self.work('Symbolstatus',status,lambda v:self.log(json.dumps(v,ensure_ascii=False,indent=2)[:5500]))
    def replace_symbol(self):
        name=self.name.get().strip()
        if not name:
            self.log('Bitte den Namen des zu ersetzenden Symbols eingeben.');return
        if not messagebox.askyesno('Symboldefinition ersetzen',
            f'TEST NUR AN EINER KOPIE!\n\nDie aktuell ausgewählte Geometrie soll das Symbol „{name}“ neu definieren.\n\n'
            'Bitte vorher in VectorCraft eine neue Form auswählen. Das Ziel wird ausdrücklich per name adressiert.\n\nFortfahren?'):
            return
        def run():
            old=state()
            symbols=old['symbols'].get('symbols',[]) if isinstance(old['symbols'],dict) else []
            matches=[x for x in symbols if x.get('name')==name]
            if len(matches)!=1:
                return {'aborted':f'Symbol „{name}“ nicht eindeutig vorhanden (Treffer: {len(matches)}).',
                        'before_symbol_list':old['symbols']}
            # Null Instanzen in symbol.list ist hier lediglich ein Warnsignal, kein zuverlässiger Nachweis.
            warning=('WARNUNG: symbol.list meldet 0 Instanzen für das Ziel. '
                     'Bitte prüfen, ob dieses Dokument die erwarteten Instanzen enthält.') if matches[0].get('instances')==0 else None
            error=None;result=None
            try:result=command('symbol.replace',{'name':name})
            except Exception as e:error=str(e)
            new=state()
            return {'test':'symbol.replace','target_name':name,'zeit':datetime.now().isoformat(timespec='seconds'),
                    'command_result':result,'command_error':error,'warning':warning,
                    'before_symbol_list':old['symbols'],'after_symbol_list':new['symbols'],
                    'before_document_hash':digest(old['document']),'after_document_hash':digest(new['document']),
                    'symbol_aenderungen':changes(old['symbols'],new['symbols'],'/symbols'),
                    'dokument_aenderungen':changes(old['document'],new['document'],'/document'),
                    'uebersicht_aenderungen':changes(old['overview'],new['overview'],'/overview'),
                    'hinweis':'Zustand unmittelbar vor/nach dem Aufruf; weitere Parameter oder Auswahl können erforderlich sein. Keine automatische Erfolgsgarantie.'}
        def finished(report):
            self.last_report=report;self.base=None
            if report.get('aborted'):
                self.log('TEST ABGEBROCHEN: '+report['aborted']);return
            if report.get('warning'):self.log(report['warning'])
            self.log('SYMBOL-TEST: '+('FEHLER: '+report['command_error'] if report['command_error'] else 'Befehl ohne Protokollfehler ausgeführt'))
            for key in ('symbol_aenderungen','dokument_aenderungen','uebersicht_aenderungen'):
                self.log(f'{key}: {len(report[key])} Unterschiede')
                for item in report[key][:8]:self.log('  '+item['pfad']+' '+item['art'])
            self.log('Bitte Bericht exportieren und hier anhängen. Zum Rückgängigmachen Strg+Z.')
        self.work('Symbol-Neudefinition',run,finished)
    def ring(self):
        try:
            n=self.name.get().strip();cx=float(self.cx.get());cy=float(self.cy.get());r=float(self.radius.get())
            if not n or not all(map(math.isfinite,[cx,cy,r])) or r<=0:raise ValueError
        except ValueError:self.log('Ungültiger Symbolname oder Maße.');return
        if not messagebox.askyesno('Instanzen erzeugen','12 Symbolinstanzen erzeugen? Vorher Dokument sichern.'):return
        def run():
            for j in range(12):
                a=2*math.pi*j/12
                command('symbol.place',{'name':n,'x':round(cx+r*math.cos(a),4),'y':round(cy+r*math.sin(a),4)})
            return '12 Instanzen erzeugt (ohne radiale Drehung)'
        self.work('Symbolinstanzen',run)
    def tick(self):
        if self._closed:return
        if self.auto.get() and self.base is not None and not self.busy:self.diff()
        self.root.after(2000,self.tick)

if __name__=='__main__':
    root=tk.Tk();App(root);root.mainloop()
