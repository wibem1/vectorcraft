#!/usr/bin/env python3
"""Minimaler VectorCraft-TCP/JSON-Funktionstest; ohne externe Bibliotheken oder KI.

Standard: read-only. Mit --execute: neues Dokument, Dreieck, 30-Grad-Drehung.
Historische Mandala-Referenz bleibt unverändert.
"""
import argparse
import json
import math
import socket
import sys


class VectorCraft:
    def __init__(self, port=7979):
        self.sock = socket.create_connection(("127.0.0.1", port), timeout=5)
        self.sock.settimeout(10)
        self.buffer = b""
        self.seq = 0

    def close(self):
        self.sock.close()

    def call(self, method, params=None):
        self.seq += 1
        request = {"id": self.seq, "method": method, "params": params or {}}
        self.sock.sendall((json.dumps(request) + "\n").encode("utf-8"))
        while b"\n" not in self.buffer:
            chunk = self.sock.recv(65536)
            if not chunk:
                raise RuntimeError("VectorCraft hat die Verbindung geschlossen")
            self.buffer += chunk
            if len(self.buffer) > 2_000_000:
                raise RuntimeError("Antwort zu groß")
        line, self.buffer = self.buffer.split(b"\n", 1)
        answer = json.loads(line)
        if answer.get("id") != self.seq:
            raise RuntimeError("Falsche Antwort-ID")
        if answer.get("error"):
            raise RuntimeError(str(answer["error"]))
        result = answer.get("result", answer)
        if isinstance(result, dict) and (result.get("ok") is False or result.get("error")):
            raise RuntimeError(str(result))
        return result

    def execute(self, command, params=None):
        return self.call("engine.execute", {"command": command, "params": params or {}})


def object_id(result):
    if isinstance(result, dict):
        ident = result.get("id")
        if type(ident) is int and ident > 0:
            return ident
        if isinstance(result.get("result"), dict):
            return object_id(result["result"])
    raise RuntimeError("Keine gueltige Objekt-ID")


def angle_of(node):
    angle = node.get("rotation", 0)  # VectorCraft laesst Nullwinkel weg.
    if type(angle) not in (int, float) or not math.isfinite(angle):
        raise RuntimeError("Ungueltiger Drehwinkel")
    return float(angle)


def run(vc, execute=False):
    catalogue = vc.call("engine.commands")
    if not catalogue:
        raise RuntimeError("Leerer Befehlskatalog")
    print("Verbindung und Befehlskatalog: OK")
    if not execute:
        print("Keine Aenderung. --execute fuer den echten Dreiecktest.")
        return
    vc.execute("file.new", {"width": 800, "height": 600})
    created = vc.execute("path.create", {"d": "M 150 120 L 330 120 L 240 290 Z"})
    ident = object_id(created)
    before = vc.execute("document.node", {"id": ident, "summary": True})
    if before.get("anchors") != 3 or before.get("closed") is not True:
        raise RuntimeError("Kein geschlossenes Dreieck erzeugt")
    old_angle = angle_of(before)
    vc.execute("object.rotate", {"id": ident, "angle": 30})
    after = vc.execute("document.node", {"id": ident, "summary": True})
    if after.get("anchors") != 3 or after.get("closed") is not True:
        raise RuntimeError("Dreieck nach Drehung ungueltig")
    if after.get("id", ident) != ident:
        raise RuntimeError("Objekt-ID veraendert")
    if not math.isclose(angle_of(after)-old_angle, 30, abs_tol=1e-5):
        raise RuntimeError("Drehung nicht 30 Grad")
    print(f"PASS: Objekt {ident}, 30 Grad, Objektidentitaet erhalten")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=7979)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("Ungueltiger Port")
    vc = None
    try:
        vc = VectorCraft(args.port)
        run(vc, args.execute)
        return 0
    except (OSError, ValueError, RuntimeError) as exc:
        print("FEHLER:", exc, file=sys.stderr)
        return 1
    finally:
        if vc:
            vc.close()


if __name__ == "__main__":
    sys.exit(main())
