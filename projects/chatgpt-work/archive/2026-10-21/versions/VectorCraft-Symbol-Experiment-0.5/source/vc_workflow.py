"""Guarded symbol workflow; no automatic mutation retries."""
import copy
import json
from datetime import datetime
from legacy import command, call, digest, changes, ControlError


def nodes(doc):
    out = {}
    def visit(n):
        out[n['id']] = n
        for child in n.get('kind', {}).get('children', []):
            visit(child)
    for layer in doc['layers']:
        visit(layer)
    return out


def definition(doc, name):
    found = [s for s in doc.get('symbols', []) if s.get('name') == name]
    if len(found) != 1:
        raise ControlError('Zielsymbol fehlt oder ist nicht eindeutig.')
    return digest(found[0])


def identity(ui, overview):
    return {'active': ui['activeDocument'], 'documents': [d['title'] for d in ui['documents']],
            'path': overview.get('path'), 'title': overview['title']}


def read_state():
    ui = call('ui.inspect')
    before = call('document.inspect', {'depth': 0})
    doc = command('document.json')
    symbols = command('symbol.list')
    after = call('document.inspect', {'depth': 0})
    ui_after = call('ui.inspect')
    if (before['revision'] != after['revision'] or before['selection'] != after['selection']
            or identity(ui, before) != identity(ui_after, after)):
        raise ControlError('Dokument wurde während der Prüfung verändert. Bearbeitung kurz pausieren und erneut prüfen.')
    if not isinstance(doc, dict) or not isinstance(doc.get('layers'), list):
        raise ControlError('Unbekanntes Dokumentformat; Schreibzugriff gesperrt.')
    return {'document': doc, 'symbols': symbols, 'overview': after, 'identity': identity(ui_after, after)}


class Workflow:
    def __init__(self, read=read_state, execute=command, save=lambda pending: None):
        self.read, self.execute, self.save = read, execute, save
        self.pending = None
        self.events = []

    def record(self, event, **data):
        self.events.append({'time': datetime.now().isoformat(), 'event': event, **copy.deepcopy(data)})

    def checkpoint(self):
        self.save(self.pending)

    def inspect_selection(self):
        old = self.read()
        selected = old['overview']['selection']
        ns = nodes(old['document'])
        self.record('selection_checked', selection=selected,
                    objects=[{'id': i, 'kind': ns.get(i, {}).get('kind', {}).get('type'),
                              'symbol': ns.get(i, {}).get('kind', {}).get('symbol')} for i in selected])
        if not selected:
            raise ControlError('Es ist nichts ausgewählt. Klicke in VectorCraft einmal auf ein Symbol in deiner Zeichnung und danach hier auf „Symbol bearbeiten“.')
        if len(selected) != 1:
            raise ControlError('Es sind mehrere Objekte ausgewählt. Klicke in VectorCraft auf eine freie Stelle und danach auf genau ein Symbol.')
        node = ns.get(selected[0], {})
        kind = node.get('kind', {})
        if kind.get('type') != 'symbolinstance':
            if kind.get('type') == 'group':
                raise ControlError('Du hast eine Gruppe ausgewählt. Wähle in VectorCraft eine einzelne Symbolinstanz innerhalb der Gruppe aus und versuche es erneut.')
            raise ControlError('Die ausgewählte Form ist kein verknüpftes Symbol. Wähle eines der wiederholten Symbole in deiner Zeichnung aus. Falls die Form noch nie ein Symbol war, kannst du sie unter „Weitere Funktionen“ mit „Symbol aus Auswahl“ umwandeln.')
        name = kind.get('symbol')
        definition(old['document'], name)
        return {'name': name, 'id': selected[0], 'identity': old['identity'],
                'revision': old['overview']['revision'], 'document_hash': digest(old['document'])}

    def begin(self, name=None, expected=None):
        if self.pending:
            raise ControlError('Eine Symbolbearbeitung ist bereits offen. Erst übernehmen oder Sitzung verwerfen.')
        old = self.read()
        selected = old['overview']['selection']
        ns = nodes(old['document'])
        if len(selected) != 1 or selected[0] not in ns:
            raise ControlError('Bitte genau eine Symbolinstanz direkt auswählen (keine Gruppe).')
        node = ns[selected[0]]
        kind = node['kind']
        if name is None:
            name = kind.get('symbol')
        if kind.get('type') != 'symbolinstance' or kind.get('symbol') != name:
            raise ControlError('Die ausgewählte Instanz gehört nicht zum eingegebenen Symbolnamen.')
        if expected is not None and (selected[0] != expected['id'] or name != expected['name']
                or old['identity'] != expected['identity'] or old['overview']['revision'] != expected['revision']
                or digest(old['document']) != expected['document_hash']):
            raise ControlError('Die Auswahl oder Zeichnung hat sich seit der Erkennung geändert. Klicke erneut auf „Symbol bearbeiten“. Es wurde nichts verändert.')
        self.pending = {'name': name, 'ids': [], 'identity': old['identity'],
                        'definition': definition(old['document'], name), 'revision': old['overview']['revision'],
                        'status': 'uncertain'}
        self.checkpoint()  # Must be durable before sending the write.
        self.record('before_edit', state=old)
        try:
            result = self.execute('symbol.edit', {'id': selected[0]})
            self.record('edit_response', result=result)
            if (not isinstance(result, dict) or result.get('name') != name
                    or not valid_ids(result.get('ids'))):
                raise ControlError('Ungültige Antwort nach symbol.edit. Zustand unklar; keine automatische Wiederholung.')
            self.pending['ids'] = result['ids']
            new = self.read()
            if new['identity'] != old['identity'] or definition(new['document'], name) != self.pending['definition']:
                raise ControlError('Dokument oder Definition während symbol.edit gewechselt.')
            ns = nodes(new['document'])
            if any(i not in ns or ns[i]['kind']['type'] == 'symbolinstance' for i in result['ids']):
                raise ControlError('Zurückgegebene Bearbeitungsgeometrie fehlt.')
            self.pending.update(status='editing', revision=new['overview']['revision'])
            self.checkpoint()
            self.record('after_edit', state=new)
            return 'Geometrie jetzt in VectorCraft bearbeiten. Danach Schritt 2 ausführen.'
        except Exception as exc:
            self.record('edit_error', error=str(exc))
            raise

    def validate(self, require_selection=True):
        p = self.pending
        if not p or p['status'] != 'editing':
            raise ControlError('Keine sicher bestätigte Bearbeitung offen. Bei unklarem Ergebnis Diagnose exportieren und Dokument prüfen.')
        current = self.read()
        if current['identity'] != p['identity'] or current['overview']['revision'] < p['revision']:
            raise ControlError('Dokumentwechsel oder zurückgesetzte Revision erkannt. Übernahme gesperrt.')
        if definition(current['document'], p['name']) != p['definition']:
            raise ControlError('Die gemeinsame Definition wurde inzwischen verändert. Übernahme gesperrt.')
        ns = nodes(current['document'])
        if any(i not in ns for i in p['ids']):
            raise ControlError('Bearbeitungsobjekt fehlt (gelöscht, aufgehoben oder rückgängig gemacht). Übernahme gesperrt.')
        if any(ns[i]['kind']['type'] in ('symbolinstance', 'layer') for i in p['ids']):
            raise ControlError('Bearbeitungsobjekte sind keine freie Geometrie mehr.')
        if require_selection and set(current['overview']['selection']) != set(p['ids']):
            raise ControlError('Die bearbeitete Form ist gerade nicht ausgewählt. Klicke hier auf „Bearbeitete Form auswählen“ und danach auf „Änderung übernehmen“.')
        return current

    def apply(self):
        old = self.validate()
        p = copy.deepcopy(self.pending)
        self.pending['status'] = 'uncertain'
        self.checkpoint()
        self.record('before_update', state=old, target=p)
        try:
            result = self.execute('symbol.update', {'name': p['name'], 'ids': p['ids']})
            self.record('update_response', result=result)
            if not isinstance(result, dict) or result.get('name') != p['name'] or not valid_ids([result.get('id')]):
                raise ControlError('Ungültige Update-Antwort; Ergebnis unklar. Nicht erneut senden.')
            new = self.read()
            if new['identity'] != p['identity']:
                raise ControlError('Dokument während der Übernahme gewechselt; Ergebnis prüfen.')
            node = nodes(new['document']).get(result['id'], {})
            if node.get('kind', {}).get('symbol') != p['name']:
                raise ControlError('Ergebnisinstanz konnte nicht bestätigt werden.')
            self.record('after_update', state=new, document_changes=changes(old['document'], new['document']),
                        definition_changed=definition(new['document'], p['name']) != p['definition'])
            self.pending = None
            self.checkpoint()
            return 'symbol.update bestätigt. Gemeinsame Definition übernommen; Instanzen bitte auch visuell prüfen.'
        except Exception as exc:
            self.record('update_error', error=str(exc))
            raise


def valid_ids(ids):
    return isinstance(ids, list) and bool(ids) and all(type(i) is int and i > 0 for i in ids) and len(set(ids)) == len(ids)

