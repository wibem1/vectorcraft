#!/usr/bin/env python3
"""Real-engine integration: the same MCP client and edit functions as the chat."""
import json
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from vectorcraft_chat import MCPClient, triangle_points
from engine_session import command, create_triangle, transform_object, node, decode, object_ids


def check_bounds(actual, points):
    xs, ys = zip(*points)
    expected = dict(x=min(xs), y=min(ys), width=max(xs)-min(xs), height=max(ys)-min(ys))
    for key, value in expected.items():
        if not math.isclose(actual['bounds'][key], value, abs_tol=1e-6):
            raise AssertionError(f'{key}: {actual["bounds"][key]} != {value}')


def rotate(points, angle):
    theta = math.radians(-angle)  # VectorCraft: CCW, document y down
    c, s = math.cos(theta), math.sin(theta)
    return [[c*x-s*y, s*x+c*y] for x, y in points]


def main(binary):
    report = {'engine': 'actual vectorcraft-cli mcp --headless', 'steps': []}
    with MCPClient(binary, headless=True) as client:
        command(client, 'file.new', {})
        points = triangle_points()
        target = create_triangle(client, dict(points=points, closed=True, fill='#bcdfea', stroke='#263e56', strokeWidth=2))
        report['object_id'] = target
        check_bounds(node(client, target), points)
        steps = [('object.rotate', {'angle': 30, 'origin': [0, 0]}),
                 ('object.move', {'dx': 17, 'dy': -11}),
                 ('object.scale', {'sx': 125, 'sy': 125, 'origin': [0, 0]}),
                 ('object.rotate', {'angle': -15, 'origin': [0, 0]})]
        for name, params in steps:
            actual = transform_object(client, target, name, params)
            if name == 'object.rotate':
                points = rotate(points, params['angle'])
            elif name == 'object.move':
                points = [[x+params['dx'], y+params['dy']] for x, y in points]
            else:
                points = [[x*1.25, y*1.25] for x, y in points]
            check_bounds(actual, points)
            if actual['anchors'] != 3 or not actual['closed']:
                raise AssertionError('Triangle topology changed')
            report['steps'].append({'command': name, 'params': params, 'verified_node': actual})
            print('PASS', name, params, 'same object ID', target, flush=True)
        # Selection may be changed manually between turns. Always reselect the recorded ID.
        command(client, 'select.set', {'ids': []})
        actual = transform_object(client, target, 'object.move', {'dx': 1, 'dy': 2})
        points = [[x+1, y+2] for x, y in points]
        check_bounds(actual, points)
        report['steps'].append({'command': 'reselect and move', 'verified_node': actual})
        doc = decode(client.tool('inspect_document', {'depth': 64}))
        if target not in object_ids(doc):
            raise AssertionError('Object identity lost')
        # Real render, requiring actual PNG bytes in the MCP image response.
        image = client.tool('screenshot', {})
        import base64
        pngs = [base64.b64decode(x['data'], validate=True) for x in image.get('content', []) if x.get('type') == 'image']
        if not pngs or not pngs[0].startswith(b'\x89PNG\r\n\x1a\n'):
            raise AssertionError('No valid PNG rendered')
        Path('headless-triangle.png').write_bytes(pngs[0])
        report['render_png_bytes'] = len(pngs[0])
        report['status'] = 'PASS'
    Path('headless-report.json').write_text(json.dumps(report, indent=2))
    print('PASS: exact bounds, 30 degree rotation, repeated edits, identity, reselect, real PNG')


if __name__ == '__main__':
    main(sys.argv[1])
