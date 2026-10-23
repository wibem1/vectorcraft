"""Kostenlose Protokoll-Fixture; kein echter VectorCraft-Nachweis."""
import json
import socketserver
import threading
import unittest

from vectorcraft_control import VectorCraft, angle_of, object_id, run


class Fixture(socketserver.StreamRequestHandler):
    def handle(self):
        angle = 0
        created = False
        for line in self.rfile:
            request = json.loads(line)
            if request["method"] == "engine.commands":
                result = ["file.new", "path.create", "document.node", "object.rotate"]
            else:
                spec = request["params"]
                command = spec["command"]
                if command == "file.new":
                    result = {"ok": True}
                elif command == "path.create":
                    created = True
                    result = {"id": 7}
                elif command == "document.node":
                    result = {"id": 7, "anchors": 3, "closed": True}
                    if angle:
                        result["rotation"] = angle
                elif command == "object.rotate" and created and spec["params"]["id"] == 7:
                    angle += spec["params"]["angle"]
                    result = {"ok": True}
                else:
                    result = {"error": "Unexpected command"}
            self.wfile.write((json.dumps({"id": request["id"], "result": result}) + "\n").encode())


class ControlTests(unittest.TestCase):
    def test_invalid_ids(self):
        for item in ({}, {"id": True}, {"id": 0}, {"id": "bad"}):
            with self.assertRaises(RuntimeError):
                object_id(item)

    def test_zero_angle_omitted(self):
        self.assertEqual(angle_of({}), 0)

    def test_tcp_fixture(self):
        with socketserver.ThreadingTCPServer(("127.0.0.1", 0), Fixture) as server:
            worker = threading.Thread(target=server.serve_forever, daemon=True)
            worker.start()
            try:
                client = VectorCraft(server.server_address[1])
                try:
                    run(client, execute=True)
                finally:
                    client.close()
            finally:
                server.shutdown()
                worker.join(timeout=3)


if __name__ == "__main__":
    unittest.main()
