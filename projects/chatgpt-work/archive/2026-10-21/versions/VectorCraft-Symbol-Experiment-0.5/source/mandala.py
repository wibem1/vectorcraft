"""Linked radial copies, rebuilt in one rollback-capable engine batch."""
import copy
import math
from vc_workflow import nodes, definition, valid_ids
from legacy import ControlError, digest


def settings(value):
    try:
        count = int(value['count'])
    except (ValueError, TypeError, OverflowError) as exc:
        raise ControlError('Bitte eine ganze Anzahl zwischen 2 und 72 wählen.') from exc
    if str(count) != str(value['count']) or not 2 <= count <= 72:
        raise ControlError('Bitte eine ganze Anzahl zwischen 2 und 72 wählen.')
    out = {'count': count, 'radial': bool(value['radial'])}
    for key in ('radius', 'angle', 'cx', 'cy'):
        try:
            out[key] = float(value[key])
        except (ValueError, TypeError) as exc:
            raise ControlError('Bitte gültige Zahlen für Radius, Drehung und Mittelpunkt eingeben.') from exc
        if not math.isfinite(out[key]):
            raise ControlError('Die Werte müssen endliche Zahlen sein.')
    if not 0 <= out['radius'] <= 2000 or not -180 <= out['angle'] <= 180 or max(abs(out['cx']), abs(out['cy'])) > 100000:
        raise ControlError('Radius: 0–2000, Drehung: −180–180 Grad; Mittelpunkt innerhalb ±100000.')
    return out


def placement(config, index, source):
    theta = 2 * math.pi * index / config['count']
    phi = (theta if config['radial'] else 0) + math.radians(config['angle'])
    co, si = math.cos(phi), math.sin(phi)
    x = config['cx'] + config['radius'] * math.cos(theta - math.pi / 2)
    y = config['cy'] + config['radius'] * math.sin(theta - math.pi / 2)
    sx, sy = source[4:6]
    return [co, si, -si, co, x - co*sx + si*sy, y - si*sx - co*sy]


class Mandala:
    def __init__(self, read, execute, save=lambda value: None):
        self.read, self.execute, self.save = read, execute, save
        self.session = None
        self.events = []

    def record(self, event, **data):
        self.events.append({'event': event, **copy.deepcopy(data)})
        self.events = self.events[-100:]

    def start(self, selection, config):
        if self.session:
            raise ControlError('Eine Mandala-Steuerung ist bereits offen. Zuerst beenden.')
        config = settings(config)
        current = self.read()
        if (current['identity'] != selection['identity'] or current['overview']['revision'] != selection['revision']
                or digest(current['document']) != selection['document_hash']
                or current['overview']['selection'] != [selection['id']]):
            raise ControlError('Die Zeichnung oder Auswahl hat sich geändert. Bitte erneut „Mandala starten“ anklicken.')
        source = nodes(current['document'])[selection['id']]
        xf = source.get('kind', {}).get('xf')
        if not isinstance(xf, list) or len(xf) != 6 or not all(type(x) in (int, float) and math.isfinite(x) for x in xf):
            raise ControlError('Die ausgewählte Instanz hat keine gültige Position.')
        self.session = {'identity': current['identity'], 'name': selection['name'], 'source': source,
                        'definition': definition(current['document'], selection['name']),
                        'revision': current['overview']['revision'], 'owned': {}, 'status': 'active', 'config': None}
        self.update(config)
        return f'Mandala mit {config["count"]} verknüpften Instanzen erstellt. Die Regler sind jetzt aktiv.'

    def validate(self):
        s = self.session
        if not s or s['status'] != 'active':
            raise ControlError('Die Mandala-Steuerung ist nicht aktiv oder ihr Ergebnis ist unklar. Diagnose exportieren und Steuerung beenden.')
        current = self.read()
        ns = nodes(current['document'])
        if current['identity'] != s['identity'] or current['overview']['revision'] < s['revision']:
            raise ControlError('Dokumentwechsel erkannt. Live-Steuerung wurde angehalten.')
        if definition(current['document'], s['name']) != s['definition']:
            raise ControlError('Das Symbol wurde inzwischen verändert. Bitte die Steuerung beenden und das Mandala bei Bedarf neu starten.')
        if ns.get(s['source']['id']) != s['source']:
            raise ControlError('Die Vorlage wurde verschoben, bearbeitet oder gelöscht. Live-Steuerung wurde angehalten.')
        if any(int(i) not in ns or digest(ns.get(int(i))) != h for i, h in s['owned'].items()):
            raise ControlError('Das Mandala wurde in VectorCraft manuell geändert oder rückgängig gemacht. Live-Steuerung wurde angehalten; deine Änderungen bleiben erhalten.')
        return current

    def update(self, value):
        config = settings(value)
        current = self.validate()
        s = self.session
        if s['config'] == config:
            return 'Einstellungen unverändert.'
        steps = []
        old_ids = [int(i) for i in s['owned']]
        if old_ids:
            steps.append({'command': 'edit.clear', 'params': {'ids': old_ids}})
        steps.append({'command': 'select.set', 'params': {'ids': [s['source']['id']]}})
        copy_offset = len(steps)
        for i in range(config['count']):
            steps.append({'command': 'object.transform', 'params': {'ids': [s['source']['id']], 'copy': True,
                         'matrix': placement(config, i, s['source']['kind']['xf'])}})
        s['status'] = 'uncertain'
        self.save(s)
        self.record('before_batch', config=config, old_ids=old_ids, before_hash=digest(current['document']))
        try:
            result = self.execute('command.batch', {'label': 'Mandala interaktiv', 'commands': steps})
            self.record('batch_response', result=result)
            results = result.get('results', []) if isinstance(result, dict) else []
            if len(results) != len(steps):
                raise ControlError('Die Antwort der Mandala-Aktualisierung ist unvollständig. Ergebnis unklar; Live-Steuerung gestoppt.')
            new_ids = []
            for row in results[copy_offset:]:
                ids = row.get('ids') if isinstance(row, dict) else None
                if not valid_ids(ids) or len(ids) != 1:
                    raise ControlError('Neue Mandala-Instanzen konnten nicht sicher zugeordnet werden.')
                new_ids.extend(ids)
            if len(set(new_ids)) != config['count'] or s['source']['id'] in new_ids or set(new_ids) & set(old_ids):
                raise ControlError('Ungültige Zuordnung der Mandala-Instanzen.')
            after = self.read()
            ns = nodes(after['document'])
            if (after['identity'] != s['identity'] or ns.get(s['source']['id']) != s['source']
                    or definition(after['document'], s['name']) != s['definition']
                    or any(i in ns for i in old_ids)
                    or any(ns.get(i, {}).get('kind', {}).get('symbol') != s['name'] for i in new_ids)):
                raise ControlError('Die Mandala-Aktualisierung konnte nicht bestätigt werden. Live-Steuerung gestoppt.')
            s.update(owned={str(i): digest(ns[i]) for i in new_ids}, config=config,
                     revision=after['overview']['revision'], status='active')
            self.save(s)
            self.record('after_batch', ids=new_ids, after_hash=digest(after['document']))
            return f'Mandala aktualisiert: {config["count"]} Motive, Radius {config["radius"]:g}, Drehung {config["angle"]:g}°.'
        except Exception as exc:
            s['status'] = 'uncertain'
            self.record('batch_error', error=str(exc))
            raise

    def finish(self):
        self.save(None)
        self.record('finished', session=self.session)
        self.session = None
        return 'Steuerung beendet. Alle Instanzen bleiben in VectorCraft erhalten.'
