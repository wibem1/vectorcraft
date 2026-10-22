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


def validate_path(params):
    if not isinstance(params, dict) or set(params)-{'points','closed','fill','stroke','strokeWidth'}:
        raise ValueError('Pfadparameter nicht unterstützt')
    points=params.get('points')
    if not isinstance(points,list) or not 2 <= len(points) <= 512:
        raise ValueError('Pfad benötigt 2 bis 512 Punkte')
    for point in points:
        if not isinstance(point,list) or len(point)!=2 or any(type(v) not in (int,float) or not math.isfinite(v) or abs(v)>1000000 for v in point):
            raise ValueError('Ungültige Pfadkoordinate')
    if type(params.get('closed',False)) is not bool:
        raise ValueError('closed muss ein Wahrheitswert sein')
    if params.get('closed') and len(points)<3:
        raise ValueError('Geschlossener Pfad benötigt mindestens drei Punkte')
    for key in ('fill','stroke'):
        if key in params:
            import re
            if not isinstance(params[key],str) or not re.fullmatch(r'#[0-9a-fA-F]{6}',params[key]):
                raise ValueError('Pfadfarbe benötigt #RRGGBB')
    width=params.get('strokeWidth',1)
    if type(width) not in (int,float) or not math.isfinite(width) or not 0 <= width <= 10000:
        raise ValueError('Ungültige Strichbreite')


def create_path(client, params):
    validate_path(params)
    before = object_ids(decode(client.tool('inspect_document', {'depth': 64})))
    reply = decode(client.tool('draw_path', params))
    target = reply.get('id')
    after = object_ids(decode(client.tool('inspect_document', {'depth': 64})))
    if type(target) is not int or after - before != {target}:
        raise ValueError('Neuer Pfad nicht eindeutig im Dokument bestätigt')
    actual = node(client, target)
    if actual.get('anchors') != len(params['points']) or actual.get('closed') != params.get('closed', False):
        raise ValueError('Neuer Pfad stimmt nicht mit den angeforderten Punkten überein')
    return target


def create_triangle(client, params):
    if len(params.get('points', [])) != 3 or params.get('closed') is not True:
        raise ValueError('Dreieck benötigt drei Punkte und einen geschlossenen Pfad')
    return create_path(client, params)

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
