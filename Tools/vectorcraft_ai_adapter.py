#!/usr/bin/env python3
"""Experimental cost-gated VectorCraft chat adapter (separate from v0.1.3).

Requires OPENROUTER_API_KEY and the *running* local VectorCraft control service.
No background work, persistent secrets, or hidden retries. Does not claim to
replace the user's existing graphical chat client.
"""
from __future__ import annotations

import argparse
from decimal import Decimal
import json
import os
import urllib.request

from ai_client_cost_policy import CostGate
from vectorcraft_local_bridge import document_summary, current_command

SYSTEM = (
    "Du steuerst eine Vektorgrafik mit lokalen Befehlen. "
    "Antworte ausschließlich mit JSON: entweder "
    '{"action":"draw","command":"shape.polygon","params":{"cx":160,"cy":160,"radius":70,"sides":3}} '
    'oder {"action":"clarify","text":"..."} oder {"action":"answer","text":"..."}. '
    "Nutze für geometrische Standardformen nur shape.polygon, shape.rectangle, "
    "shape.ellipse, shape.star, shape.line. Kein Javascript und keine Listen "
    "der verfügbaren Engine-Befehle. Verwende den aktuellen Dokumentstand."
)
ALLOWED = frozenset({"shape.polygon", "shape.rectangle", "shape.ellipse", "shape.star", "shape.line"})
MAX_REPLY = 20000


def model_reply(*, key: str, model: str, messages: list[dict], max_tokens: int,
                transport=None) -> tuple[dict, dict]:
    """Single bounded OpenRouter call; no automatic retries."""
    if not key or not model:
        raise ValueError("API key and model are required")
    payload = json.dumps({"model": model, "messages": messages,
                          "max_tokens": max_tokens, "temperature": 0.2,
                          "response_format": {"type": "json_object"}}).encode("utf-8")
    request = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=payload, method="POST",
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
    )
    if transport is None:
        transport = urllib.request.urlopen
    with transport(request, timeout=45) as response:
        body = response.read(1024 * 1024 + 1)
    if len(body) > 1024 * 1024:
        raise ValueError("OpenRouter reply too large")
    result = json.loads(body)
    message = result["choices"][0]["message"]
    content = message["content"]
    if not isinstance(content, str) or len(content) > MAX_REPLY:
        raise ValueError("model response missing or too large")
    return json.loads(content), result.get("usage") or {}


def bounded_action(action: dict) -> tuple[str, dict] | None:
    if not isinstance(action, dict):
        raise ValueError("invalid action")
    kind = action.get("action")
    if kind in ("answer", "clarify"):
        if not isinstance(action.get("text"), str):
            raise ValueError("missing answer text")
        return None
    if kind != "draw" or action.get("command") not in ALLOWED:
        raise ValueError("unsupported AI command; document unchanged")
    params = action.get("params")
    if not isinstance(params, dict) or len(json.dumps(params)) > 4000:
        raise ValueError("invalid geometry parameters")
    # Only plain JSON values; the local engine validates geometric constraints.
    return action["command"], params


def one_turn(*, instruction: str, model: str, key: str, port: int,
             budget: CostGate, max_request_usd: str, eur_per_usd: str,
             max_output_tokens: int = 350, llm=model_reply,
             inspect=document_summary, execute=current_command) -> dict:
    """One user turn with a fresh local state. Never automatically repeat edits."""
    if not instruction.strip() or len(instruction) > 4000:
        raise ValueError("instruction must be 1..4000 characters")
    # Reserve before a paid request; provided USD cap must be a credible external
    # worst-case estimate, NOT a quote inferred from actual tokens alone.
    from decimal import Decimal
    reserved = str(Decimal(max_request_usd) * Decimal(eur_per_usd))
    budget.reserve(max_cost_usd=max_request_usd, eur_per_usd=eur_per_usd)
    # Read-only local inspection happens BEFORE contacting the LLM.
    try:
        document = inspect(port=port, depth=0, child_limit=12)
        if not isinstance(document, dict):
            raise ValueError("invalid document summary")
        context = {k:document[k] for k in ("artboards","selection","name","revision")
                   if k in document}
        if len(json.dumps(context)) > 8000:
            raise ValueError("document context too large")
        messages = [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": json.dumps({"request": instruction, "document": context},
                                                 ensure_ascii=False)},
        ]
        action, usage = llm(key=key, model=model, messages=messages,
                            max_tokens=max_output_tokens)
        # Settle the request before attempting any drawing.
        # Cost availability is necessary for reliable accounting.
        cost_usd = usage.get("cost")
        if cost_usd is None:
            raise ValueError("provider did not return a USD cost; drawing withheld")
        budget.settle(actual_cost_usd=str(cost_usd), eur_per_usd=eur_per_usd,
                      reserved_cost_eur=reserved)
        operation = bounded_action(action)
        if operation is None:
            return {"status": action["action"], "message": action["text"], "usage": usage}
        command, params = operation
        result = execute(command, params, port=port)
        return {"status": "executed", "command": command, "result": result, "usage": usage}
    except Exception:
        # A request without settled provider billing remains reserved: safe
        # against spending the same budget again while settlement is unknown.
        raise


def main() -> None:
    parser = argparse.ArgumentParser(description="Experimental single-turn VectorCraft KI adapter")
    parser.add_argument("instruction")
    parser.add_argument("--model", required=True)
    parser.add_argument("--port", type=int, default=7979)
    parser.add_argument("--budget-eur", default="0.10")
    parser.add_argument("--max-request-usd", required=True,
                        help="Conservative externally determined maximum price for this one request")
    parser.add_argument("--eur-per-usd", required=True,
                        help="Conservative EUR per USD exchange rate, supplied by operator")
    args = parser.parse_args()
    budget = CostGate(max_eur=args.budget_eur)
    result = one_turn(instruction=args.instruction, model=args.model,
                      key=os.environ.get("OPENROUTER_API_KEY", ""), port=args.port,
                      budget=budget, max_request_usd=args.max_request_usd,
                      eur_per_usd=args.eur_per_usd)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
