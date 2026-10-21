"""Small deterministic geometry core for VectorCraft Chat. No API calls."""
from __future__ import annotations
import math

def triangle_points(cx: float = 300, cy: float = 260, radius: float = 105):
    if not all(math.isfinite(x) for x in (cx, cy, radius)) or radius <= 0:
        raise ValueError("Triangle geometry must be finite and radius positive")
    return [[round(cx + radius * math.cos(-math.pi/2 + i*2*math.pi/3), 3),
             round(cy + radius * math.sin(-math.pi/2 + i*2*math.pi/3), 3)]
            for i in range(3)]

def verify_selected_target(document: dict, target_id: int) -> None:
    """Fail closed if the live document does not confirm exactly one target."""
    if not isinstance(target_id, int) or isinstance(target_id, bool):
        raise ValueError("Invalid object ID")
    selected = document.get("selection")
    if not isinstance(selected, list):
        raise ValueError("Missing selection")
    ids = [item.get("id") if isinstance(item, dict) else item for item in selected]
    if ids != [target_id]:
        raise ValueError("Selected object differs from requested target")

def triangle_tool_arguments(points=None):
    pts = triangle_points() if points is None else points
    if len(pts) != 3 or any(len(p) != 2 or not all(isinstance(x, (int,float)) and math.isfinite(x) for x in p) for p in pts):
        raise ValueError("Exactly three finite 2D points required")
    return {"points": pts, "closed": True, "stroke": "#263e56", "strokeWidth": 2}
