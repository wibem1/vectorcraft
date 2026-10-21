#!/usr/bin/env python3
"""Pure, offline planning helpers for a future VectorCraft AI client.

No API calls, no changes to documents, no model-dependent guessing. The live
Python chat client must explicitly adopt these helpers before savings occur.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any

# Exact MCP tool names confirmed in crates/mcp/src/tools.rs.
BASIC_TOOLS = frozenset({"doc_inspect", "draw_shape", "draw_path", "command_batch"})
EDIT_TOOLS = frozenset({"doc_inspect", "command_run", "command_batch", "set_paint", "transform"})
VISUAL_TOOLS = frozenset({"doc_inspect", "render_preview"})
DISCOVERY_TOOLS = frozenset({"command_list", "command_run", "doc_inspect"})
MAX_SCHEMA_BYTES = 24000
MAX_CONTEXT_BYTES = 12000


def pick_tools(catalog: list[dict[str, Any]], profile: str = "draw") -> list[dict[str, Any]]:
    """Select only existing tool definitions; never invent a schema.

    Tool choice for this first client prototype is deliberately explicit:
    callers decide the profile (draw, edit, visual, discover).
    """
    profiles = {"draw": BASIC_TOOLS, "edit": EDIT_TOOLS,
                "visual": VISUAL_TOOLS, "discover": DISCOVERY_TOOLS}
    if profile not in profiles:
        raise ValueError("unknown profile: " + profile)
    chosen = [tool for tool in catalog if tool.get("name") in profiles[profile]]
    found = {tool.get("name") for tool in chosen}
    if not found:
        raise ValueError("no matching tools in MCP catalog")
    packed = json.dumps(chosen, ensure_ascii=False, separators=(",", ":")).encode()
    if len(packed) > MAX_SCHEMA_BYTES:
        raise ValueError("selected tool schema exceeds byte budget")
    return chosen


def compact_document(document: dict[str, Any], *, selected_ids: list[int] | None = None) -> dict[str, Any]:
    """Explicit allowlist: avoid sending full document geometry by default.

    This is only a view of an already queried summary, not a reconstruction of
    hidden geometry. The caller must fetch object details when required.
    """
    result = {key: document[key] for key in ("id", "name", "artboards", "selection", "history", "revision")
              if key in document}
    if selected_ids is not None:
        result["requested_object_ids"] = selected_ids[:32]
    payload = json.dumps(result, ensure_ascii=False, separators=(",", ":")).encode()
    if len(payload) > MAX_CONTEXT_BYTES:
        raise ValueError("summary exceeds context byte budget; request a shallower inspection")
    return result


@dataclass
class CostGate:
    """Conservative USD ledger; call site must explicitly supply current EUR/USD.

    A true cap needs a model cost ceiling and a conservative exchange rate.
    Unpriced or unbounded requests are refused, not silently sent.
    """
    max_eur: str = "0.10"
    spent_eur: str = "0"
    reserved_eur: str = "0"

    def reserve(self, *, max_cost_usd: str, eur_per_usd: str) -> None:
        from decimal import Decimal, InvalidOperation
        try:
            cost = Decimal(max_cost_usd) * Decimal(eur_per_usd)
            remaining = Decimal(self.max_eur) - Decimal(self.spent_eur) - Decimal(self.reserved_eur)
            if not cost.is_finite() or cost <= 0 or not remaining.is_finite() or cost > remaining:
                raise ValueError("insufficient or invalid budget")
            self.reserved_eur = str(Decimal(self.reserved_eur) + cost)
        except (InvalidOperation, TypeError):
            raise ValueError("model pricing and exchange rate required") from None

    def settle(self, *, actual_cost_usd: str, eur_per_usd: str, reserved_cost_eur: str) -> None:
        from decimal import Decimal
        actual = Decimal(actual_cost_usd) * Decimal(eur_per_usd)
        reserved = Decimal(reserved_cost_eur)
        if not actual.is_finite() or actual < 0 or not reserved.is_finite() or reserved <= 0:
            raise ValueError("invalid settlement")
        if actual > reserved:
            raise ValueError("provider cost exceeded reserved limit; disable further calls")
        self.reserved_eur = str(Decimal(self.reserved_eur) - reserved)
        self.spent_eur = str(Decimal(self.spent_eur) + actual)
