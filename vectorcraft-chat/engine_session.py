"""Verified edits shared by the chat UI and the real-engine integration test."""
import json
import math


def decode(result):
    if isinstance(result.get('structuredContent'), dict):
        return result['structuredContent']
    for item in result.get('content', []):
        if item.get('type') == 'text':
            try:
                value = json.loads(item.get('text', ''))
                if isinstance(value, dict):
                    return value
            except ValueError:
                pass
    raise ValueError('MCP liefert kein auswertbares Objekt')


def object_ids(document):
    found = set()
    def walk(value, parent=''):
        if isinstance(value, dict):
            if parent in ('layers', 'children', 'objects') and type(value.get('id')) is int:
                found.add(value['id'])
            for key, child in value.items():
                if key not in ('selection', 'history'):
                    walk(child, key)
        elif isinstance(value, list):
            for child in value:
                walk(child, parent)
    walk(document)
    return found


def command(client, name, params):
    return decode(client.tool('run_command', {'command': name, 'params': params}))


def node(client, target):
    value = command(client, 'document.node', {'id': target, 'summary': True})
    if value.get('id') != target:
        raise ValueError('Objekt-ID nicht im aktuellen Dokument bestätigt')
    return value


def create_triangle(client, params):
    before = object_ids(decode(client.tool('inspect_document', {'depth': 64})))
    reply = decode(client.tool('draw_path', params))
    target = reply.get('id')
    after = object_ids(decode(client.tool('inspect_document', {'depth': 64})))
    if type(target) is not int or after - before != {target}:
        raise ValueError('Neues Dreieck nicht eindeutig im Dokument bestätigt')
    actual = node(client, target)
    if actual.get('anchors') != 3 or actual.get('closed') is not True:
        raise ValueError('Neues Objekt ist kein geschlossenes Dreieck')
    return target


def transform_object(client, target, name, params):
    if name not in ('object.rotate', 'object.move', 'object.scale'):
        raise ValueError('Nicht unterstützte Folgeänderung')
    before = node(client, target)
    command(client, 'select.set', {'ids': [target]})
    doc = decode(client.tool('inspect_document', {'depth': 0}))
    if doc.get('selection') != [target]:
        raise ValueError('Auswahl stimmt nicht mit dem Zielobjekt überein')
    command(client, name, params)
    after = node(client, target)
    if before == after:
        raise ValueError('Keine Änderung am Zielobjekt nachweisbar')
    if name == 'object.rotate':
        actual = (after.get('rotation', 0) - before.get('rotation', 0)) % 360
        if not math.isclose(actual, params['angle'] % 360, abs_tol=1e-7):
            raise ValueError('Drehwinkel nicht bestätigt')
    return after
