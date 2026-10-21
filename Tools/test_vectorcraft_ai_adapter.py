import importlib.util
import sys
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("vc_adapter", Path(__file__).with_name("vectorcraft_ai_adapter.py"))
sys.path.insert(0, str(Path(__file__).parent))
adapter = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = adapter
spec.loader.exec_module(adapter)


class AdapterTests(unittest.TestCase):
    def test_triangle_with_fresh_document_state_and_cost(self):
        calls = []
        def inspect(**kwargs):
            calls.append("inspect")
            return {"selection": [], "artboards": [{"width": 600, "height": 600}],
                    "layers": [{"objects": "not forwarded"}]}
        def llm(**kwargs):
            calls.append("llm")
            body = kwargs["messages"][1]["content"]
            self.assertNotIn("layers", body)
            self.assertIn("artboards", body)
            return ({"action":"draw", "command":"shape.polygon",
                     "params":{"cx":160,"cy":160,"radius":70,"sides":3}},
                    {"cost":0.001,"prompt_tokens":350,"completion_tokens":70})
        def execute(command, params, **kwargs):
            calls.append("execute")
            self.assertEqual(params["sides"], 3)
            return {"id": 24}
        gate = adapter.CostGate()
        result = adapter.one_turn(instruction="Zeichne ein Dreieck", model="mock",
                                  key="TEST", port=7979, budget=gate, max_request_usd="0.01",
                                  eur_per_usd="1", inspect=inspect, llm=llm, execute=execute)
        self.assertEqual(result["status"], "executed")
        self.assertEqual(calls, ["inspect", "llm", "execute"])
        self.assertEqual(gate.spent_eur, "0.001")

    def test_over_budget_refuses_before_state_and_llm(self):
        def forbidden(**kwargs):
            self.fail("over-budget request must not run")
        with self.assertRaises(ValueError):
            adapter.one_turn(instruction="Dreieck",model="mock",key="X",port=7979,
                             budget=adapter.CostGate(),max_request_usd="0.11",
                             eur_per_usd="1",inspect=forbidden,llm=forbidden,execute=forbidden)

    def test_unknown_action_does_not_draw(self):
        with self.assertRaises(ValueError):
            adapter.bounded_action({"action":"draw","command":"file.delete",
                                    "params":{}})

    def test_no_provider_cost_means_no_draw(self):
        def model(**kwargs):
            return ({"action":"draw","command":"shape.polygon","params":{"sides":3}}, {})
        def forbidden(*args, **kwargs):
            self.fail("no drawing without provider cost")
        with self.assertRaises(ValueError):
            adapter.one_turn(instruction="Dreieck",model="mock",key="X",port=7979,
                             budget=adapter.CostGate(),max_request_usd="0.01",eur_per_usd="1",
                             inspect=lambda **kw: {"selection":[]},llm=model,execute=forbidden)


if __name__ == "__main__":
    unittest.main()
