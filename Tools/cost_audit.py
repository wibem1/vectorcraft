#!/usr/bin/env python3
"""Offline OpenRouter usage auditor. No network access, no prompts or keys in output."""
import argparse
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path


def summarize(data):
    entries = data.get("usage", [])
    result = {"requests": len(entries), "prompt_tokens": 0, "completion_tokens": 0,
              "total_tokens": 0, "cost_usd": "0", "models": [], "warnings": []}
    total = Decimal("0")
    for number, item in enumerate(entries, 1):
        usage = item.get("usage", {})
        prompt = usage.get("prompt_tokens")
        completion = usage.get("completion_tokens")
        billed = usage.get("cost")
        if not isinstance(prompt, int) or prompt < 0 or not isinstance(completion, int) or completion < 0:
            result["warnings"].append(f"request {number}: missing or invalid token counts")
            continue
        result["prompt_tokens"] += prompt
        result["completion_tokens"] += completion
        result["total_tokens"] += prompt + completion
        if usage.get("total_tokens") != prompt + completion:
            result["warnings"].append(f"request {number}: token total differs")
        try:
            amount = Decimal(str(billed))
            if not amount.is_finite() or amount < 0:
                raise InvalidOperation()
            total += amount
        except (InvalidOperation, TypeError, ValueError):
            result["warnings"].append(f"request {number}: cost missing or invalid")
        model = item.get("model")
        if model and model not in result["models"]:
            result["models"].append(model)
    result["cost_usd"] = str(total)
    if result["requests"]:
        result["average_prompt_tokens"] = result["prompt_tokens"] / result["requests"]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("diagnostic_json", type=Path)
    parser.add_argument("--max-prompt-tokens", type=int, default=4000,
                        help="Warning threshold for average input tokens per request, not a hard API limit")
    args = parser.parse_args()
    report = summarize(json.loads(args.diagnostic_json.read_text(encoding="utf-8-sig")))
    if report.get("average_prompt_tokens", 0) > args.max_prompt_tokens:
        report["warnings"].append("average input tokens exceed audit threshold; inspect client prompt assembly")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
