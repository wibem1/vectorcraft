import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("cost_audit", Path(__file__).with_name("cost_audit.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class AuditTests(unittest.TestCase):
    def test_observed_vectorcraft_diagnostic_totals(self):
        data = {"usage": [
            {"model": "google/gemini-3.8-flash", "usage": {"prompt_tokens": 9643, "completion_tokens": 1235, "total_tokens": 10878, "cost": 0.0118635}},
            {"model": "google/gemini-3.8-flash", "usage": {"prompt_tokens": 7623, "completion_tokens": 1396, "total_tokens": 9019, "cost": 0.01095225}},
        ]}
        report = mod.summarize(data)
        self.assertEqual(report["requests"], 2)
        self.assertEqual(report["prompt_tokens"], 17266)
        self.assertEqual(report["completion_tokens"], 2631)
        self.assertEqual(report["total_tokens"], 19897)
        self.assertEqual(report["cost_usd"], "0.02281575")
        self.assertFalse(report["warnings"])

    def test_missing_fields_are_not_silently_treated_as_zero(self):
        report = mod.summarize({"usage": [{"usage": {"prompt_tokens": 20, "completion_tokens": 5, "total_tokens": 80}}]})
        self.assertEqual(len(report["warnings"]), 2)
        self.assertEqual(report["cost_usd"], "0")


if __name__ == "__main__":
    unittest.main()
