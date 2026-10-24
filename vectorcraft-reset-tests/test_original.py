"""Gratis-Regression des Originalprogramms vom 14.10.; kein nativer Engine-Test."""
import json
import socketserver
import threading
import unittest
import zipimport
from pathlib import Path

ARCHIVE = Path(__file__).resolve().parents[1] / "vectorcraft-reset" / "VectorCraft-Mandala-Zentriert-v2.zip"
original = zipimport.zipimporter(str(ARCHIVE)).load_module("vectorcraft_mandala_zentriert")


class Handler(socketserver.StreamRequestHandler):
    def handle(self):
        for line in self.rfile:
            request = json.loads(line)
            result = {"id": 12} if request["method"] == "engine.execute" else [{"id": "path.create"}]
            self.wfile.write((json.dumps({"id": request["id"], "result": result}) + "\n").encode())


class TestOriginal(unittest.TestCase):
    def test_has_command(self):
        self.assertTrue(original.has_command([{"id": "path.create"}], "path.create"))
        self.assertFalse(original.has_command([{"id": "path.create"}], "object.rotate"))

    def test_result_id(self):
        self.assertEqual(original.result_id({"id": 42}), 42)
        with self.assertRaises(RuntimeError):
            original.result_id({})

    def test_original_vc_transport(self):
        with socketserver.ThreadingTCPServer(("127.0.0.1", 0), Handler) as server:
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            vc = original.VC("127.0.0.1", server.server_address[1])
            try:
                self.assertEqual(vc.exec("path.create", {"d": "M 0 0 L 1 0 L 0 1 Z"})["id"], 12)
                self.assertEqual(vc.call("engine.commands"), [{"id": "path.create"}])
                self.assertEqual(vc.trace[0]["command"], "path.create")
            finally:
                vc.close()
                server.shutdown()
                thread.join()


if __name__ == "__main__":
    unittest.main()
