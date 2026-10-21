import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("policy", Path(__file__).with_name("ai_client_cost_policy.py"))
policy = importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name] = policy
spec.loader.exec_module(policy)


class PolicyTests(unittest.TestCase):
    def test_small_toolkit_not_full_catalog(self):
        catalog = [{"name": n, "inputSchema": {"type": "object"}} for n in
                   ["draw_shape", "draw_path", "doc_inspect", "command_batch", "command_list", "render_preview"]]
        selected = policy.pick_tools(catalog, "draw")
        self.assertEqual({t["name"] for t in selected},
                         {"draw_shape", "draw_path", "doc_inspect", "command_batch"})
        self.assertNotIn("command_list", {t["name"] for t in selected})

    def test_visual_view_on_demand(self):
        catalog = [{"name": n} for n in ["draw_shape", "render_preview", "doc_inspect"]]
        self.assertEqual({t["name"] for t in policy.pick_tools(catalog, "visual")},
                         {"render_preview", "doc_inspect"})

    def test_document_never_sends_entire_scene(self):
        snapshot = {"name": "Mandala", "revision": 9, "selection": [12],
                    "nodes": [{"id": i, "geometry": "x" * 200} for i in range(1026)]}
        result = policy.compact_document(snapshot, selected_ids=[12])
        self.assertNotIn("nodes", result)
        self.assertEqual(result["requested_object_ids"], [12])

    def test_cost_limit_and_settlement(self):
        gate = policy.CostGate()
        gate.reserve(max_cost_usd="0.06", eur_per_usd="1")
        self.assertEqual(gate.reserved_eur, "0.06")
        with self.assertRaises(ValueError):
            gate.reserve(max_cost_usd="0.05", eur_per_usd="1")
        gate.settle(actual_cost_usd="0.02", eur_per_usd="1", reserved_cost_eur="0.06")
        self.assertEqual(gate.spent_eur, "0.02")
        self.assertEqual(gate.reserved_eur, "0.00")

    def test_refuse_unpriced_model(self):
        with self.assertRaises(ValueError):
            policy.CostGate().reserve(max_cost_usd="", eur_per_usd="1")


if __name__ == "__main__":
    unittest.main()
