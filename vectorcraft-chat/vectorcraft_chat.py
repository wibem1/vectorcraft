#!/usr/bin/env python3
"""VectorCraft Chat: standalone local chat client; Python standard library only."""
import json, os, queue, socket, threading, urllib.request, urllib.error, tkinter as tk, traceback, time, re, sys, subprocess, base64, ctypes, uuid, shutil
from tkinter import ttk, messagebox, scrolledtext, filedialog
from pathlib import Path
from datetime import datetime
from engine_session import create_triangle, transform_object
from cost_control import admit, money
from app_connection import ensure_connection, MissingApplication, command_ids, normalize_executable

APP_DIR = Path.home()/'.vectorcraft-chat'
SETTINGS = APP_DIR/'settings.json'
HISTORY = APP_DIR/'history.json'
COSTS = APP_DIR/'costs.json'
MAX_OUTPUT = 10000
APP_VERSION = "0.3.1-dev"
DIAG_EVENTS = []

def event(kind, info):
    DIAG_EVENTS.append({"time":datetime.now().astimezone().isoformat(),"kind":kind,"info":safe_error(info)[:2000]})
    del DIAG_EVENTS[:-120]

SYSTEM = '''Du bist ein konstruktiver, deutschsprachiger Gesprächspartner und Zeichenassistent für VectorCraft. Sei bei einfachen Aufgaben selbstständig: Bei "Konstruiere ein Dreieck" wähle ein gleichseitiges Dreieck mit vernünftigen Standardmaßen. "egal" im anschließenden Gespräch bedeutet: entscheide die fehlenden Details selbst und führe den vorherigen Auftrag aus. Verlange keine unnötigen Spezifikationen.
Der aktuelle VectorCraft-Dokumentzustand und die zulässigen Befehle werden mitgegeben. Erfinde keine Befehlsnamen und keine Parameter. Kommandos wie path.rect ergeben KEIN Dreieck: verwende Pfaderstellung mit echten Eckpunkten anhand vorhandener dokumentierter Befehle. Wenn keine passenden Befehle bekannt sind, erkläre die konkrete Einschränkung.
Wenn der Nutzer eine einfache Figur wie ein Dreieck verlangt, konstruiere sie selbstständig. Die Antwort ist erst dann eine erledigte Konstruktion, wenn du ausführbare native Befehle vorschlägst. Bei bloßer Diskussion antworte normal. Bei Ausführungsauftrag gib eine kurze Erklärung und am Ende NUR einen korrekt abgeschlossenen Block dieses Formats aus:
<vc_actions>{"actions":[{"method":"engine.execute","params":{"command":"EXAKTE_COMMAND_ID","params":{}}}]}</vc_actions>
JSON muss syntaktisch valide sein (keine Kommentare, keine nachgestellten Kommas, keine Markdown-Codezäune). Maximal 12 Aktionen. Zulässige Methoden: engine.execute, document.inspect, ui.render, ui.inspect. Keine destruktiven, Reset-, Datei-Schreib- oder frei erfundenen Aktionen. Alle Änderungen müssen von der Person bestätigt werden.'''

# Secrets stay outside settings.json; on Windows they are DPAPI-encrypted per user.
KEY_FILE = APP_DIR/'openrouter.key'
def keychain_args():
    # An explicit keychain permits isolated native CI without touching the login store.
    path=os.environ.get('VECTORCRAFT_CHAT_KEYCHAIN','')
    return [path] if path else []

def save_secret(secret):
    APP_DIR.mkdir(mode=0o700,parents=True,exist_ok=True)
    if sys.platform=='win32':
        from ctypes import wintypes
        class BLOB(ctypes.Structure): _fields_=[('cbData',wintypes.DWORD),('pbData',ctypes.POINTER(ctypes.c_byte))]
        buf=ctypes.create_string_buffer(secret.encode('utf-8')); src=BLOB(len(secret.encode('utf-8')),ctypes.cast(buf,ctypes.POINTER(ctypes.c_byte))); dst=BLOB()
        ctypes.windll.crypt32.CryptProtectData.argtypes=[ctypes.POINTER(BLOB),wintypes.LPCWSTR,ctypes.POINTER(BLOB),ctypes.c_void_p,ctypes.c_void_p,wintypes.DWORD,ctypes.POINTER(BLOB)]
        if not ctypes.windll.crypt32.CryptProtectData(ctypes.byref(src),'VectorCraft Chat',None,None,None,0,ctypes.byref(dst)): raise OSError('Windows DPAPI konnte API-Key nicht schützen')
        try: KEY_FILE.write_bytes(ctypes.string_at(dst.pbData,dst.cbData))
        finally: ctypes.windll.kernel32.LocalFree(dst.pbData)
    elif sys.platform=='darwin':
        if not secret: subprocess.run(['security','delete-generic-password','-s','VectorCraftChat-OpenRouter']+keychain_args(),capture_output=True)
        else: subprocess.run(['security','add-generic-password','-U','-s','VectorCraftChat-OpenRouter','-a',os.getenv('USER','user'),'-w',secret]+keychain_args(),check=True,capture_output=True)
    else:
        descriptor=os.open(KEY_FILE,os.O_WRONLY|os.O_CREAT|os.O_TRUNC,0o600)
        with os.fdopen(descriptor,'w',encoding='utf8') as output:
            os.fchmod(output.fileno(),0o600)
            output.write(secret)
        event('security','Linux-Fallback: eingeschränkte Dateiberechtigung, kein OS-Schlüsselspeicher')
def load_secret():
    try:
        if sys.platform=='win32':
            if not KEY_FILE.exists():return ''
            from ctypes import wintypes
            class BLOB(ctypes.Structure):_fields_=[('cbData',wintypes.DWORD),('pbData',ctypes.POINTER(ctypes.c_byte))]
            data=KEY_FILE.read_bytes(); buf=ctypes.create_string_buffer(data); src=BLOB(len(data),ctypes.cast(buf,ctypes.POINTER(ctypes.c_byte))); dst=BLOB()
            ctypes.windll.crypt32.CryptUnprotectData.argtypes=[ctypes.POINTER(BLOB),ctypes.c_void_p,ctypes.POINTER(BLOB),ctypes.c_void_p,ctypes.c_void_p,wintypes.DWORD,ctypes.POINTER(BLOB)]
            if not ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(src),None,None,None,None,0,ctypes.byref(dst)):return ''
            try:return ctypes.string_at(dst.pbData,dst.cbData).decode('utf8')
            finally:ctypes.windll.kernel32.LocalFree(dst.pbData)
        if sys.platform=='darwin':
            r=subprocess.run(['security','find-generic-password','-s','VectorCraftChat-OpenRouter','-w']+keychain_args(),capture_output=True,text=True)
            return r.stdout.strip() if r.returncode==0 else ''
        return KEY_FILE.read_text(encoding='utf8') if KEY_FILE.exists() else ''
    except Exception as exc:
        event('key_load_error',type(exc).__name__);return ''

def model_catalog(api_key):
    headers={'User-Agent':'VectorCraftChat/'+APP_VERSION}
    if api_key:headers['Authorization']='Bearer '+api_key
    req=urllib.request.Request('https://openrouter.ai/api/v1/models',headers=headers)
    with urllib.request.urlopen(req,timeout=25) as response:data=json.load(response)
    entries=data.get('data',[])
    return {x['id']:x for x in entries if isinstance(x,dict) and isinstance(x.get('id'),str)}

def list_models(api_key):
    return sorted(model_catalog(api_key), key=str.casefold)

def safe_error(err):
    value=re.sub(r'Bearer\s+[^\s\"\']+', 'Bearer [versteckt]', str(err))
    value=re.sub(r'sk-or-[A-Za-z0-9_-]+', '[API-Key versteckt]', value)
    return value[:1200]

def read_json(path, default):
    try: return json.loads(path.read_text(encoding='utf8'))
    except (OSError, ValueError): return default

def save_json(path, obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    temporary=path.with_suffix(path.suffix+'.tmp')
    temporary.write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf8')
    temporary.replace(path)

def control(method, params=None, port=7979):
    request_id=uuid.uuid4().hex
    payload=json.dumps({'id':request_id,'method':method,'params':params or {}},ensure_ascii=False)+'\n'
    with socket.create_connection(('127.0.0.1',int(port)),timeout=5) as sock:
        sock.settimeout(75)
        sock.sendall(payload.encode('utf-8'))
        data=bytearray()
        while not data.endswith(b'\n'):
            part=sock.recv(65536)
            if not part: raise ConnectionError('VectorCraft hat die Verbindung geschlossen.')
            data.extend(part)
            if len(data)>8_000_000: raise ValueError('Antwort zu groß')
    resp=json.loads(data)
    if resp.get('id')!=request_id: raise ValueError('Antwort-ID stimmt nicht überein')
    if not resp.get('ok'): raise RuntimeError(resp.get('error','VectorCraft-Befehl fehlgeschlagen'))
    return resp.get('result')

def ensure_document(port):
    """Inspect native UI state: document.inspect errors when no document is open."""
    state=control('ui.inspect',{},port)
    if not isinstance(state,dict) or not isinstance(state.get('documents'),list):
        raise ConnectionError('VectorCraft hat keinen verwendbaren Dokumentstatus bestätigt.')
    documents=state['documents'];active=state.get('activeDocument')
    created=not documents and active is None
    if created:
        # Never race an asynchronous open or a native file dialog with a new document.
        if state.get('opening') != [] or state.get('fileDialog') is not None:
            raise ConnectionError('VectorCraft öffnet noch ein Dokument oder einen Dateidialog; bitte erneut verbinden.')
        control('engine.execute',{'command':'file.new','params':{}},port)
    elif type(active) is not int or not 0 <= active < len(documents):
        raise ConnectionError('VectorCraft hat kein aktives Dokument bestätigt.')
    document=control('document.inspect',{'depth':0},port)
    if not isinstance(document,dict) or not isinstance(document.get('layers'),list):
        raise ConnectionError('VectorCraft hat kein verwendbares Dokument bestätigt.')
    return created

def api_chat(api_key, model, messages, max_tokens=1400):
    if not api_key.strip():raise ValueError('Kein OpenRouter-Key vorhanden. Bitte erneut eintragen und speichern.')
    payload={'model':model,'messages':messages,'temperature':0.5,'max_tokens':max_tokens,'usage':{'include':True}}
    req=urllib.request.Request('https://openrouter.ai/api/v1/chat/completions',data=json.dumps(payload).encode(),headers={'Authorization':'Bearer '+api_key,'Content-Type':'application/json','HTTP-Referer':'http://localhost','X-Title':'VectorCraft Chat'},method='POST')
    try:
        with urllib.request.urlopen(req,timeout=100) as r: data=json.load(r)
    except urllib.error.HTTPError as e:
        details=e.read(500).decode('utf8','replace')
        if e.code==401: raise RuntimeError('OpenRouter HTTP 401: API-Key fehlt, ist ungültig oder wurde nicht akzeptiert. Bitte Key im Einstellungsfeld prüfen.')
        raise RuntimeError('OpenRouter HTTP '+str(e.code)+': '+details)
    if 'error' in data:raise RuntimeError('OpenRouter: '+safe_error(data['error']))
    choices=data.get('choices')
    if not isinstance(choices,list) or not choices:raise ValueError('OpenRouter lieferte keine Antwortauswahl')
    choice=choices[0].get('message',{}).get('content')
    if isinstance(choice,list): choice='\n'.join(str(p.get('text','')) for p in choice if isinstance(p,dict))
    event('api_response',f'content_chars={len(choice or chr(0))- (0 if choice else 1)}; tokens={data.get("usage",{}).get("total_tokens","?")}')
    return choice or '',data.get('usage',{})

def mcp_executable():
    """Path to bundled or installed VectorCraft CLI, never download executables."""
    custom = os.getenv('VECTORCRAFT_CLI', '').strip()
    guesses = [custom] if custom else []
    if sys.platform == 'win32':
        guesses += [str(Path(os.getenv('ProgramFiles', r'C:\Program Files'))/'VectorCraft'/'vectorcraft-cli.exe')]
    selected=normalize_executable(read_json(SETTINGS,{}).get('vectorcraft_app'))
    if selected:
        guesses += [str(selected.parent/('vectorcraft-cli.exe' if sys.platform=='win32' else 'vectorcraft-cli'))]
    if getattr(sys,'frozen',False):
        guesses += [str(Path(sys.executable).parent/('vectorcraft-cli.exe' if sys.platform=='win32' else 'vectorcraft-cli'))]
    guesses += [shutil.which('vectorcraft-cli') or '']
    return next((p for p in guesses if p and Path(p).is_file()), None)

class MCPClient:
    """Minimal MCP stdio client. A session is scoped to a single command batch."""
    def __init__(self, executable, remote_port=7979, headless=False):
        self.executable=executable; self.port=int(remote_port); self.process=None;self.seq=0;self.headless=headless
    def __enter__(self):
        args=[self.executable,'mcp']+(['--headless'] if self.headless else ['--connect',f'127.0.0.1:{self.port}'])
        options={'creationflags':subprocess.CREATE_NO_WINDOW} if sys.platform=='win32' else {}
        self.process=subprocess.Popen(args,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,bufsize=0,**options)
        try:
            self.request('initialize',{'protocolVersion':'2025-06-18','capabilities':{},'clientInfo':{'name':'VectorCraft Chat','version':APP_VERSION}})
            self.process.stdin.write((json.dumps({'jsonrpc':'2.0','method':'notifications/initialized'})+'\n').encode());self.process.stdin.flush()
            return self
        except BaseException:
            self.__exit__(None,None,None);raise
    def __exit__(self,*args):
        if self.process:
            try:self.process.stdin.close()
            except OSError:pass
            try:self.process.terminate(); self.process.wait(timeout=3)
            except (OSError,subprocess.TimeoutExpired):self.process.kill()
            finally:
                try:self.process.stdout.close()
                except OSError:pass
    def request(self,method,params):
        self.seq+=1; ident=self.seq
        packet=json.dumps({'jsonrpc':'2.0','id':ident,'method':method,'params':params},ensure_ascii=False)+'\n'
        self.process.stdin.write(packet.encode());self.process.stdin.flush()
        # Read on a thread to support Windows anonymous pipes and a finite timeout.
        recv=queue.Queue(maxsize=1)
        def reader():
            try:
                while True:
                    line=self.process.stdout.readline(8_000_001)
                    if len(line)>8_000_000:raise ValueError('MCP-Antwort zu groß')
                    if not line:raise ConnectionError('VectorCraft MCP wurde beendet')
                    result=json.loads(line)
                    if result.get('id')==ident:recv.put((True,result));break
            except Exception as exc:recv.put((False,exc))
        threading.Thread(target=reader,daemon=True).start()
        try:ok,payload=recv.get(timeout=70)
        except queue.Empty:raise TimeoutError('VectorCraft MCP antwortet nicht; Ergebnis ist ungewiss')
        if not ok:raise payload
        if 'error' in payload:raise RuntimeError(str(payload['error']))
        return payload.get('result',{})
    def tool(self,name,args):
        result=self.request('tools/call',{'name':name,'arguments':args})
        if result.get('isError'):raise RuntimeError('MCP '+name+': '+str(result.get('content',[]))[:700])
        return result

def triangle_points(cx=300,cy=260,radius=105):
    import math
    return [[round(cx+radius*math.cos(-math.pi/2+2*math.pi*i/3),3),round(cy+radius*math.sin(-math.pi/2+2*math.pi*i/3),3)] for i in range(3)]

def detect_triangle(text):
    t=text.casefold()
    return ('dreieck' in t or 'triangle' in t) and any(w in t for w in ('konstrui','zeichne','erzeuge','erstelle','mach'))

def rotate_request_degrees(text):
    """Only interpret an explicit request to rotate the previously drawn triangle."""
    import re
    t=text.casefold()
    if not any(x in t for x in ('dreh', 'rotier')) or any(x in t for x in ('kreis','rechteck','ellipse','circle')):
        return None
    m=re.search(r'([+-]?\d+(?:[.,]\d+)?)\s*(?:°|grad)', t)
    if not m:
        return None
    angle=float(m.group(1).replace(',','.'))
    if not -3600 <= angle <= 3600: raise ValueError('Drehwinkel außerhalb des erlaubten Bereichs')
    return angle

def parse_mcp_inspection(result):
    """Decode MCP tool content (JSON text or structured content)."""
    if isinstance(result,dict) and isinstance(result.get('structuredContent'),dict):
        return result['structuredContent']
    for item in result.get('content',[]) if isinstance(result,dict) else []:
        if isinstance(item,dict) and item.get('type')=='text':
            try:
                doc=json.loads(item.get('text',''))
                if isinstance(doc,dict):return doc
            except json.JSONDecodeError:pass
    return {}

def document_has_object(document,oid):
    """Fail closed unless the target exists in the reported layer tree or selection."""
    if oid in inspection_selection(document):return True
    def rec(value):
        if isinstance(value,dict):
            if value.get('id')==oid:return True
            return any(rec(v) for k,v in value.items() if k not in ('selection','history'))
        if isinstance(value,list):return any(rec(v) for v in value)
        return False
    return rec(document.get('artboards',document.get('layers',[])))

def inspection_selection(document):
    """Extract selected object IDs without guessing from a textual model reply."""
    if not isinstance(document,dict): return []
    value=document.get('selection',[])
    if isinstance(value,dict):value=value.get('ids',value.get('objects',[]))
    if not isinstance(value,list):return []
    ids=[]
    for item in value:
        if isinstance(item,(str,int)) and not isinstance(item,bool):ids.append(item)
        elif isinstance(item,dict) and isinstance(item.get('id'),(str,int)):ids.append(item['id'])
    return ids

ALLOWED_COMMANDS = frozenset(('path.create','shape.rectangle','shape.ellipse','shape.polygon',
    'object.move','object.rotate','object.scale','object.reflect','object.setProps',
    'select.set','paint.setFill','paint.setStroke','paint.strokeWidth'))

def parse_actions(content):
    start=content.find('<vc_actions>'); end=content.find('</vc_actions>')
    if start<0 and end<0:
        event('action_parser','no action tag; text_len='+str(len(content)))
        return content, []
    if start<0 or end<start: raise ValueError('Unvollständiger Aktionsblock der KI. Nichts wird ausgeführt.')
    if content.count('<vc_actions>')!=1 or content.count('</vc_actions>')!=1:
        raise ValueError('Mehrere Aktionsblöcke sind nicht zulässig')
    raw=content[start+12:end].strip()
    if len(raw)>16000:raise ValueError('Aktionsblock zu groß')
    try: spec=json.loads(raw)
    except json.JSONDecodeError as exc:
        event('invalid_actions',f'Position {exc.pos}: {exc.msg}; raw_length={len(raw)}')
        raise ValueError('Die KI hat ungültige Befehlsdaten zurückgegeben. Es wurde NICHTS ausgeführt. Bitte erneut versuchen oder anderes Modell wählen.') from exc
    if not isinstance(spec,dict):raise ValueError('Aktionsblock muss ein JSON-Objekt sein')
    actions=spec.get('actions',[])
    if not isinstance(actions,list) or len(actions)>12: raise ValueError('Ungültige Anzahl Aktionen')
    for item in actions:
        if not isinstance(item,dict) or item.get('method') not in ('engine.execute','document.inspect','ui.render','ui.inspect','mcp.draw_path') or not isinstance(item.get('params',{}),dict): raise ValueError('Ungültige VectorCraft-Aktion')
        item.setdefault('params',{})
        if item['method']=='engine.execute':
            if item['params'].get('command') not in ALLOWED_COMMANDS or not isinstance(item['params'].get('params',{}),dict):
                raise ValueError('Nicht zugelassener Engine-Befehl')
        if item['method']=='ui.render' and set(item['params'])-{'scale','artboard','data'}:
            raise ValueError('Render-Dateizugriffe sind nicht zulässig')
    return (content[:start]+content[end+13:]).strip(),actions

def select_commands(items,request,limit=22):
    """Small task-specific command menu to avoid multi-thousand-token catalogs."""
    words=str(request).casefold()
    geometric=any(x in words for x in ('dreieck','kreis','rechteck','polygon','rosette','mandala','linie','pfad','konstru','zeichn'))
    keys=('path','polygon','shape','point','anchor','geometry','object','document','layer','select','undo') if geometric else ('object','path','shape','layer','transform','document','select','color')
    scored=[]
    for it in items:
        if not isinstance(it,dict):continue
        identifier=str(it.get('id') or it.get('command') or '')
        if identifier not in ALLOWED_COMMANDS:continue
        lid=identifier.casefold()
        score=sum(3 for x in keys if x in lid)
        if 'dreieck' in words and any(x in lid for x in ('path','polygon','point','anchor')):score+=12
        if any(x in lid for x in ('delete','clear','reset','quit','export','save','script','batch','import')):continue
        if score:scored.append((score,lid,{'id':identifier,'params':it.get('params'),'label':it.get('label')}))
    scored.sort(key=lambda x:(-x[0],x[1]))
    return [x[2] for x in scored[:limit]]

def validated_options(port, budget):
    number=int(port)
    amount=money(str(budget).replace(',','.'))
    if not 1 <= number <= 65535 or amount<=0:
        raise ValueError('Port 1–65535 und positives endliches Budget erforderlich')
    return number,float(amount)

def stored_spend():
    if not COSTS.exists():return 0.0
    # A broken ledger must not silently reset the spending counter.
    value=json.loads(COSTS.read_text(encoding='utf8'))
    return float(money(value['spent_usd']))

class App:
    def __init__(self,root,auto_connect=True):
        self.root=root; root.title('VectorCraft Chat '+APP_VERSION); root.geometry('540x490');root.minsize(420,360)
        self.settings=read_json(SETTINGS,{'model':'google/gemini-2.5-flash','port':7979,'max_eur':0.10,'usd_to_eur':0.92});self.messages=read_json(HISTORY,[])
        self.pending=[];self.last_triangle_id=None;self.command_ids=set();self.busy=False;self.q=queue.Queue();self.session_spend_usd=0.0;self.cost_error=''
        try:self.session_spend_usd=stored_spend()
        except (OSError,ValueError,TypeError,KeyError):self.cost_error='Kostenprotokoll unlesbar; bezahlte Anfragen sind gesperrt. Diagnose speichern.'
        self.model=tk.StringVar(value=self.settings.get('model',''))
        self.port=tk.StringVar(value=str(self.settings.get('port',7979)))
        self.key=tk.StringVar(value=os.getenv('OPENROUTER_API_KEY') or load_secret())
        self.models=[];self.last_error='';self.last_operation='';self.total_usage=[]
        self.connected=False;self.connected_port=None;self.active_job='';self.native_process=None
        self.budget=tk.StringVar(value=str(self.settings.get('max_eur',0.10)))
        root.columnconfigure(0,weight=1)
        root.rowconfigure(1,weight=1)
        settings=ttk.Frame(root,padding=(7,6,7,2)); settings.grid(row=0,column=0,sticky='ew')
        settings.columnconfigure(1,weight=1)
        ttk.Label(settings,text='Modell').grid(row=0,column=0,sticky='w',padx=(0,5),pady=2)
        self.model_box=ttk.Combobox(settings,textvariable=self.model,values=[],state='normal');self.model_box.grid(row=0,column=1,columnspan=2,sticky='ew',pady=2)
        ttk.Button(settings,text='Modelle laden',command=self.refresh_models).grid(row=0,column=3,sticky='e',padx=(3,0))
        ttk.Label(settings,text='API-Key').grid(row=1,column=0,sticky='w',padx=(0,5),pady=2)
        ttk.Entry(settings,textvariable=self.key,show='*').grid(row=1,column=1,columnspan=2,sticky='ew',pady=2)
        ttk.Button(settings,text='Key speichern',command=self.store_key).grid(row=1,column=3,sticky='e',padx=(3,0))
        ttk.Label(settings,text='Port').grid(row=2,column=0,sticky='w',pady=2)
        ttk.Entry(settings,textvariable=self.port,width=7).grid(row=2,column=1,sticky='w',pady=2)
        ttk.Label(settings,text='Budget €').grid(row=2,column=2,sticky='e',padx=(8,4),pady=2)
        ttk.Entry(settings,textvariable=self.budget,width=7).grid(row=2,column=3,sticky='w',pady=2)
        self.connect_button=ttk.Button(settings,text='VectorCraft starten / verbinden',command=self.connect)
        self.connect_button.grid(row=3,column=0,columnspan=3,sticky='ew',pady=(3,4))
        ttk.Button(settings,text='Diagnose speichern',command=self.export_diagnostic).grid(row=3,column=3,sticky='e',padx=(3,0))
        self.chat=scrolledtext.ScrolledText(root,wrap='word',state='disabled',font=('Segoe UI',10),padx=10,pady=7,width=1,height=1); self.chat.grid(row=1,column=0,sticky='nsew',padx=7,pady=(0,3))
        self.chat.tag_config('user',foreground='#2576b7');self.chat.tag_config('assistant',foreground='#24815c');self.chat.tag_config('system',foreground='#8b6b18')
        self.entry=tk.Text(root,height=3,width=1,wrap='word',font=('Segoe UI',10));self.entry.grid(row=2,column=0,sticky='ew',padx=8,pady=(0,5))
        self.entry.bind('<Control-Return>',lambda e:self.send())
        buttons=ttk.Frame(root,padding=(8,0,8,4));buttons.grid(row=3,column=0,sticky='ew')
        self.send_button=ttk.Button(buttons,text='Senden',command=self.send);self.send_button.pack(side='left')
        self.exec_button=ttk.Button(buttons,text='Befehle ausführen',command=self.execute,state='disabled');self.exec_button.pack(side='left',padx=4)
        ttk.Button(buttons,text='Neuer Chat',command=self.clear).pack(side='right')
        self.status=tk.StringVar(value='Nicht verbunden · API-Key lokal speicherbar');ttk.Label(root,textvariable=self.status,padding=(8,0,8,5),wraplength=480).grid(row=4,column=0,sticky='ew')
        for m in self.messages[-50:]: self.write(m['role'],m['content'])
        root.after(100,self.pump)
        root.protocol('WM_DELETE_WINDOW',self.close)
        self.send_button.config(state='disabled')
        if auto_connect:root.after(200,self.connect)
    def write(self,role,text):
        self.chat.configure(state='normal');self.chat.insert('end', {'user':'Du','assistant':'KI','system':'VectorCraft'}.get(role,role)+': ',role);self.chat.insert('end',text+'\n\n');self.chat.configure(state='disabled');self.chat.see('end')
    def task(self,fn):
        if self.busy:return
        self.busy=True;self.send_button.config(state='disabled');self.exec_button.config(state='disabled');self.connect_button.config(state='disabled')
        threading.Thread(target=lambda:self.runner(fn),daemon=True).start()
    def runner(self,fn):
        try: self.q.put(('ok',fn()))
        except (ConnectionError,socket.timeout) as e:self.q.put(('connection_error',str(e)))
        except Exception as e:self.q.put(('error',str(e)))
    def pump(self):
        try:
            while True:
                kind,payload=self.q.get_nowait();self.busy=False;self.send_button.config(state='normal' if self.connected else 'disabled');self.connect_button.config(state='normal')
                if kind in ('error','connection_error'):
                    if self.active_job=='connect' or kind=='connection_error':
                        self.connected=False;self.command_ids=set();self.pending=[];self.send_button.config(state='disabled')
                    self.last_error=safe_error(payload);event('error',self.last_error)
                    self.write('system','Fehler: '+self.last_error);self.status.set('Fehler – Diagnose speichern möglich')
                elif isinstance(payload,tuple) and payload[0]=='choose_application':
                    self.active_job='';self.connected=False;self.status.set(payload[1]);self.write('system',payload[1])
                    selected=filedialog.askopenfilename(title='Installiertes VectorCraft auswählen',filetypes=[('VectorCraft','*.exe *.app'),('Alle Dateien','*')])
                    if selected:
                        self.settings['vectorcraft_app']=selected;save_json(SETTINGS,self.settings)
                        self.root.after(0,self.connect)
                elif isinstance(payload,tuple) and payload[0]=='connected':
                    _,result,port=payload
                    self.connected=True;self.connected_port=port;self.active_job='';self.command_ids=command_ids(result['catalog'])
                    self.native_process=result.get('process') or self.native_process
                    if result.get('path'):
                        self.settings['vectorcraft_app']=result['path'];save_json(SETTINGS,self.settings)
                    self.send_button.config(state='normal');self.last_error=''
                    self.status.set('Verbunden · VectorCraft '+('gestartet' if result['started'] else 'bereits geöffnet'))
                    self.write('system','VectorCraft ist verbunden. Du kannst mit der Konstruktion beginnen.')
                    event('connection_ready',f'port={port}; started={result["started"]}; document_created={result.get("document_created",False)}; commands={len(self.command_ids)}')
                elif isinstance(payload,tuple) and payload[0]=='chat':
                    _,text,actions,usage=payload;self.write('assistant',text)
                    self.messages.append({'role':'assistant','content':text});save_json(HISTORY,self.messages)
                    self.pending=actions
                    self.total_usage.append({'model':self.model.get(),'usage':usage,'time':datetime.now().isoformat()})
                    if actions:self.exec_button.config(state='normal');self.write('system',f'{len(actions)} Befehle vorgeschlagen. Erst nach Klick auf „ausführen“ werden sie an VectorCraft gesendet.');
                    # Costs are persisted in the worker before parsing; parser errors are charged too.
                    event('action_parser',f'actions={len(actions)}, text_chars={len(text)}')
                    self.status.set('KI · '+str(len(actions))+' Aktionen · Tokens '+str(usage.get('total_tokens','?'))+' · Kosten $'+format(self.session_spend_usd,'.4f'))
                elif isinstance(payload,tuple) and payload[0]=='models':
                    self.models=payload[1];self.model_box.configure(values=self.models);self.status.set(f'{len(self.models)} OpenRouter-Modelle geladen')
                elif isinstance(payload,tuple) and payload[0]=='inspect':
                    _,summary,ids=payload;self.command_ids=ids;self.status.set(f'Verbunden mit VectorCraft · {len(ids)} Befehle bekannt');self.write('system',summary)
                elif isinstance(payload,tuple) and payload[0]=='executed':
                    self.pending=[];self.write('system',payload[1]);self.status.set('Ausführung beendet – Dokument wurde erneut geprüft')
        except queue.Empty:pass
        self.root.after(100,self.pump)
    def store_key(self):
        key=self.key.get().strip()
        try:
            save_secret(key);self.status.set('OpenRouter-Key lokal gespeichert' if key else 'OpenRouter-Key gelöscht')
            event('key_saved','Key gespeichert: '+str(bool(key)))
        except Exception as e:messagebox.showerror('API-Key speichern',safe_error(e))
    def refresh_models(self):
        key=self.key.get().strip()
        self.status.set('Lade OpenRouter-Modellliste …')
        self.task(lambda:('models',list_models(key)))
    def export_diagnostic(self):
        path=filedialog.asksaveasfilename(title='Diagnose speichern',defaultextension='.json',filetypes=[('JSON-Diagnose','*.json')],initialfile='VectorCraft-Chat-Diagnose-'+datetime.now().strftime('%Y%m%d-%H%M%S')+'.json')
        if not path:return
        doc={'app_version':APP_VERSION,'timestamp':datetime.now().astimezone().isoformat(),'platform':sys.platform,'python':sys.version.split()[0], 'settings':{'model':self.model.get(),'port':self.port.get(),'max_eur':self.budget.get(),'key_present':bool(self.key.get().strip()),'key_saved':bool(load_secret())},'connection_ready':self.connected,'connected_port':self.connected_port,'native_app_configured':bool(self.settings.get('vectorcraft_app')),'connection_command_count':len(self.command_ids),'models_loaded':len(self.models),'last_error':self.last_error,'events':DIAG_EVENTS[-100:],'usage':self.total_usage[-30:],'pending_action_count':len(self.pending),'accounted_cost_usd':self.session_spend_usd,'cost_error':self.cost_error,'cost_policy':'conservative estimate; unresolved usage retains reservation; no provider-enforced EUR cap','history_messages':len(self.messages),'notes':'Keine API-Keys, keine Prompt-Texte und keine Dokumentinhalte gespeichert. Keine automatische Übertragung.'}
        Path(path).write_text(json.dumps(doc,ensure_ascii=False,indent=2),encoding='utf8')
        self.status.set('Diagnose gespeichert: '+Path(path).name)
    def connect(self):
        if self.busy:return
        try:port,_=validated_options(self.port.get(),self.budget.get())
        except ValueError:
            self.write('system','Bitte einen gültigen Port und ein positives Budget eintragen.');return
        self.save_settings();self.connected=False;self.connected_port=None;self.command_ids=set();self.pending=[];self.last_triangle_id=None
        self.active_job='connect';self.status.set('VectorCraft wird gesucht / verbunden …')
        saved_path=self.settings.get('vectorcraft_app')
        def job():
            try:
                result=ensure_connection(port,APP_DIR,saved_path)
                result['document_created']=ensure_document(port)
                return ('connected',result,port)
            except MissingApplication as exc:return ('choose_application',str(exc))
        self.task(job)
    def inspect(self):
        # Retained as a compatibility alias; the primary button now handles launch and reuse.
        self.connect()
    def connection_matches(self):
        try:port=int(self.port.get())
        except ValueError:return False
        return self.connected and self.connected_port==port
    @staticmethod
    def extract_ids(catalog):
        if isinstance(catalog,dict):
            entries=catalog.get('commands',catalog)
        else:entries=catalog
        if isinstance(entries,dict):return set(entries)
        if isinstance(entries,list):return {str(x.get('id',x.get('command'))) for x in entries if isinstance(x,dict) and (x.get('id') or x.get('command'))}
        return set()
    def send(self):
        prompt=self.entry.get('1.0','end').strip()
        if not prompt:return
        if not self.connection_matches():
            self.write('system','Bitte zuerst VectorCraft starten / verbinden.');return
        self.active_job='chat'
        key=self.key.get().strip()
        if not key and not (detect_triangle(prompt) or rotate_request_degrees(prompt) is not None):messagebox.showwarning('API-Key','Bitte OpenRouter API-Key eintragen.');return
        if self.busy:return
        try:
            validated_port,budget=validated_options(self.port.get(),self.budget.get())
        except ValueError:
            messagebox.showerror('Einstellungen','Bitte Port 1–65535 und ein positives endliches Kostenbudget eingeben.');return
        local_request=detect_triangle(prompt) or rotate_request_degrees(prompt) is not None
        if not local_request and self.cost_error:
            self.write('system',self.cost_error);return
        if not local_request and self.session_spend_usd*float(self.settings.get('usd_to_eur',0.92)) >= budget:
            messagebox.showwarning('Kosten','Die bisherigen Sitzungskosten erreichen das eingestellte Budget. Für weitere API-Anfragen bitte neues Budget festlegen.');return
        self.pending=[];self.exec_button.config(state='disabled')
        self.save_settings();self.entry.delete('1.0','end');self.write('user',prompt)
        angle=rotate_request_degrees(prompt)
        if angle is not None:
            if self.last_triangle_id is None:
                self.write('system','Kein bestätigtes Dreieck aus dieser Sitzung bekannt. Bitte zuerst eines erstellen und ausführen.');return
            self.messages.append({'role':'user','content':prompt});save_json(HISTORY,self.messages)
            self.pending=[{'method':'mcp.rotate_triangle','params':{'id':self.last_triangle_id,'angle':angle}}]
            self.exec_button.config(state='normal')
            self.write('assistant',f'Ich drehe das zuvor erzeugte Dreieck um {angle:g} Grad. Bitte mit „Befehle ausführen“ bestätigen.')
            event('rotation_plan','target_id='+str(self.last_triangle_id)+'; angle='+str(angle))
            return
        if detect_triangle(prompt):
            exe=mcp_executable()
            if not exe:
                self.write('system','VectorCraft CLI nicht gefunden. Installiere vectorcraft-cli.exe oder setze VECTORCRAFT_CLI. Es wurde nichts gezeichnet.')
                event('mcp_missing','vectorcraft-cli nicht gefunden');return
            self.messages.append({'role':'user','content':prompt});save_json(HISTORY,self.messages)
            self.pending=[{'method':'mcp.draw_path','params':{'points':triangle_points(),'closed':True,'fill':'#bcdfea','stroke':'#263e56','strokeWidth':2}}]
            self.exec_button.config(state='normal')
            self.write('assistant','Ich schlage ein gleichseitiges Dreieck vor. Mit „Befehle ausführen“ wird es als editierbarer Vektorpfad in VectorCraft angelegt.')
            event('triangle_plan','deterministic draw_path; cli_available=true')
            return
        self.messages.append({'role':'user','content':prompt});save_json(HISTORY,self.messages)
        self.pending=[]
        chosen_model=self.model.get().strip();chosen_port=int(self.port.get());exchange_rate=self.settings.get('usd_to_eur',0.92)
        def job():
            port=chosen_port
            try:
                event('vectorcraft','document.inspect started')
                doc=control('document.inspect',{'depth':1,'childLimit':10},port)
                if not isinstance(doc,dict):raise ValueError('Kein bestätigtes VectorCraft-Dokument')
                catalog=control('engine.commands',{},port)
                items=catalog.get('commands',[]) if isinstance(catalog,dict) else catalog
                if isinstance(items,dict):items=[dict(v,id=k) for k,v in items.items() if isinstance(v,dict)]
                if not isinstance(items,list):items=[]
                self.command_ids=self.extract_ids(catalog)
                if not self.command_ids:raise ValueError('Kein bestätigter VectorCraft-Befehlskatalog')
                relevant=select_commands(items,prompt)
                event('catalog',f'total={len(items)},selected={len(relevant)},ids={",".join(str(x.get("id")) for x in relevant[:12])}')
                target_context=''
                if self.last_triangle_id is not None:
                    target=control('engine.execute',{'command':'document.node','params':{'id':self.last_triangle_id,'summary':True}},port)
                    target_context='Zuletzt erzeugtes Dreieck (frisch geprüft): '+json.dumps(target,ensure_ascii=False)+'\n'
                context=target_context+'Dokument (gekürzt): '+json.dumps(doc,ensure_ascii=False)[:2500]+'\nVerfügbare Befehle (exakte IDs/Parameter): '+json.dumps(relevant,ensure_ascii=False)[:11000]
            except Exception as e:
                self.command_ids=set()
                event('vectorcraft_error',type(e).__name__+': '+safe_error(e)[:300])
                raise ConnectionError('VectorCraft-Dokument oder Befehle nicht bestätigt; keine kostenpflichtige Modellanfrage gesendet. '+safe_error(e)) from e
            history=self.messages[-8:]
            msgs=[{'role':'system','content':SYSTEM+'\n'+context}]+history
            event('api_request',f'model={chosen_model}, messages={len(msgs)}, context_chars={len(context)}')
            model=chosen_model
            catalog=model_catalog(key)
            if model not in catalog:raise ValueError('Modell nicht im aktuellen OpenRouter-Katalog')
            reserve=admit(catalog[model],msgs,2000,self.session_spend_usd,budget,exchange_rate)
            self.session_spend_usd+=reserve
            save_json(COSTS,{'spent_usd':self.session_spend_usd,'pending_reservation_usd':reserve})
            event('cost_admission',f'model={model}; reserve_usd={reserve:.6f}')
            # On timeout/transport error keep the reservation: the provider may have billed.
            content,usage=api_chat(key,model,msgs,max_tokens=2000)
            if usage.get('cost') is not None:
                charged=float(money(usage['cost']))
                self.session_spend_usd=max(0,self.session_spend_usd-reserve)+charged
                save_json(COSTS,{'spent_usd':self.session_spend_usd,'pending_reservation_usd':0})
                event('cost_settled',f'charged_usd={charged:.6f}')
            else:
                event('cost_unknown','Provider cost missing; reservation retained')
            answer,actions=parse_actions(content)
            if not actions and any(w in prompt.casefold() for w in ('konstruiere','zeichne','erstelle','erzeuge')):
                event('no_actions','Auftrag ohne ausführbare Aktion; model='+chosen_model)
                answer+='\n\n[Hinweis: Die KI hat keine ausführbare Konstruktion geliefert. Es wurde nichts gezeichnet.]'
            if actions and not self.command_ids:raise ValueError('Es liegt kein bestätigter VectorCraft-Befehlskatalog vor; Aktionen werden nicht übernommen.')
            for action in actions:
                if action['method']=='engine.execute' and action['params']['command'] not in self.command_ids:
                    raise ValueError('KI hat nicht existierenden Befehl vorgeschlagen: '+action['params']['command'])
            return ('chat',answer,actions,usage)
        self.task(job)
    def execute(self):
        actions=list(self.pending)
        if not actions or self.busy:return
        if not self.connection_matches():
            self.pending=[];self.exec_button.config(state='disabled');self.write('system','Verbindung nicht bestätigt. Bitte erneut verbinden.');return
        self.active_job='execute'
        if not messagebox.askyesno('VectorCraft ändern?',f'{len(actions)} vorgeschlagene Aktionen in VectorCraft ausführen?\nVorher bitte das Dokument speichern.'):return
        self.pending=[]
        port=int(self.port.get())
        def job():
            outcomes=[]
            before=control('document.inspect',{'depth':0,'childLimit':8},port)
            event('execution',f'start; actions={len(actions)}')
            for i,a in enumerate(actions,1):
                if a['method']=='engine.execute' and self.command_ids and a['params']['command'] not in self.command_ids:
                    raise ValueError('Befehl nicht im zuletzt geprüften Katalog: '+a['params']['command'])
                if a['method'] in ('mcp.draw_path','mcp.rotate_triangle'):
                    exe=mcp_executable()
                    if not exe:raise FileNotFoundError('vectorcraft-cli fehlt')
                    with MCPClient(exe,port) as client:
                        if a['method']=='mcp.draw_path':
                            self.last_triangle_id=create_triangle(client,a['params'])
                            result={'id':self.last_triangle_id,'verified':True}
                            event('triangle_created','verified_id='+str(self.last_triangle_id))
                        else:
                            target=a['params']['id']
                            result=transform_object(client,target,'object.rotate',{'angle':a['params']['angle']})
                            event('triangle_rotated','verified_id='+str(target)+'; angle='+str(a['params']['angle']))
                elif a['method']=='engine.execute' and a['params']['command'] in ('object.move','object.rotate','object.scale') and self.last_triangle_id is not None:
                    exe=mcp_executable()
                    if not exe:raise FileNotFoundError('vectorcraft-cli fehlt')
                    with MCPClient(exe,port) as client:
                        result=transform_object(client,self.last_triangle_id,a['params']['command'],a['params'].get('params',{}))
                else:
                    result=control(a['method'],a.get('params',{}),port)
                event('execution_step',f'index={i}; method={a["method"]}; command={a.get("params",{}).get("command","")}; success=true')
                outcomes.append(f'{i}. {a["method"]}: '+json.dumps(result,ensure_ascii=False)[:120])
            after=control('document.inspect',{'depth':0,'childLimit':8},port)
            changed=before!=after
            event('execution_verified',f'document_changed={changed}')
            return ('executed','Ausgeführt; Dokumentstatus verändert: '+('ja' if changed else 'nicht nachweisbar')+'\n'+'\n'.join(outcomes))
        self.task(job)
    def clear(self):
        if self.busy:return
        if not messagebox.askyesno('Neuer Chat','Gesprächsverlauf zurücksetzen?'):return
        self.messages=[];self.pending=[];self.last_triangle_id=None;save_json(HISTORY,[]);self.chat.configure(state='normal');self.chat.delete('1.0','end');self.chat.configure(state='disabled')
    def save_settings(self):
        try:port,budget=validated_options(self.port.get(),self.budget.get())
        except ValueError:return
        self.settings.update({'model':self.model.get(),'port':port,'max_eur':budget});save_json(SETTINGS,self.settings)
    def close(self):self.save_settings();self.root.destroy()
if __name__=='__main__':
    if len(sys.argv)==3 and sys.argv[1]=='--self-test':
        sys.modules['vectorcraft_chat']=sys.modules[__name__]
        from packaged_check import run
        raise SystemExit(run(sys.argv[2]))
    root=tk.Tk();ttk.Style().theme_use('clam');App(root);root.mainloop()
