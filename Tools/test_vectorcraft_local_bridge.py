import importlib.util
import json
from pathlib import Path
import socket
import sys
import threading
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("bridge", Path(__file__).with_name("vectorcraft_local_bridge.py"))
bridge = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = bridge
spec.loader.exec_module(bridge)


class FakeConnection:
    def __init__(self, response):
        self.response = response
        self.sent = b""
    def __enter__(self): return self
    def __exit__(self, *args): pass
    def settimeout(self, value): pass
    def sendall(self, data): self.sent += data
    def recv(self, number):
        response, self.response = self.response, b""
        return response


class BridgeTests(unittest.TestCase):
    def test_compact_document_inspection_without_catalogue(self):
        fake = FakeConnection(b'{"id":1,"ok":true,"result":{"selection":[4]}}\n')
        with patch.object(bridge.socket, "create_connection", return_value=fake):
            value = bridge.document_summary()
        request = json.loads(fake.sent)
        self.assertEqual(request["method"], "document.inspect")
        self.assertEqual(request["params"], {"depth": 0, "childLimit": 12})
        self.assertEqual(value["selection"], [4])
        self.assertNotIn("engine.commands", fake.sent.decode())

    def test_explicit_geometry_operation(self):
        fake = FakeConnection(b'{"id":1,"ok":true,"result":{"id":19}}\n')
        with patch.object(bridge.socket, "create_connection", return_value=fake):
            result = bridge.current_command("shape.polygon", {"cx": 90, "cy": 90, "sides": 3, "radius": 50})
        self.assertEqual(result, {"id": 19})
        self.assertEqual(json.loads(fake.sent)["params"]["params"]["sides"], 3)

    def test_failure_has_no_hidden_retry(self):
        fake = FakeConnection(b'{"id":1,"ok":false,"error":"still running"}\n')
        with patch.object(bridge.socket, "create_connection", return_value=fake) as connect:
            with self.assertRaises(bridge.VectorCraftControlError):
                bridge.current_command("shape.polygon", {"sides": 3})
        self.assertEqual(connect.call_count, 1)

    def test_reject_remote_address(self):
        with self.assertRaises(ValueError):
            bridge.exchange("document.inspect", host="example.org")


if __name__ == "__main__":
    unittest.main()
