#!/usr/bin/env python3
"""Small, bounded client for VectorCraft's *existing* local control protocol.

This module does not contact any LLM, install anything, or mutate the document
when reading. A higher-level chat client may use it, but must implement its own
user-intent, state freshness and budget gates. Never expose port 7979 publicly.
"""
import json
import socket
from typing import Any


class VectorCraftControlError(RuntimeError):
    pass


def exchange(method: str, params: dict[str, Any] | None = None, *,
             host: str = "127.0.0.1", port: int = 7979, timeout: float = 8.0) -> Any:
    if host != "127.0.0.1":
        raise ValueError("only the local VectorCraft control service is permitted")
    if not 1 <= port <= 65535 or not 0 < timeout <= 60:
        raise ValueError("invalid port or timeout")
    request = json.dumps({"id": 1, "method": method, "params": params or {}},
                         separators=(",", ":"), ensure_ascii=False).encode("utf-8") + b"\n"
    if len(request) > 1024 * 1024:
        raise ValueError("control request too large")
    with socket.create_connection((host, port), timeout=timeout) as connection:
        connection.settimeout(timeout)
        connection.sendall(request)
        received = bytearray()
        while len(received) < 2 * 1024 * 1024:
            block = connection.recv(min(4096, 2 * 1024 * 1024 - len(received)))
            if not block:
                raise VectorCraftControlError("connection closed before response")
            received.extend(block)
            if b"\n" in block:
                break
    line = bytes(received).split(b"\n", 1)[0]
    try:
        response = json.loads(line.decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as exc:
        raise VectorCraftControlError("invalid control response") from exc
    if response.get("id") != 1:
        raise VectorCraftControlError("control response ID mismatch")
    if response.get("ok") is not True:
        raise VectorCraftControlError(str(response.get("error", "control request failed")))
    return response.get("result")


def document_summary(*, port: int = 7979, depth: int = 0, child_limit: int = 12) -> Any:
    """Retrieve current document state, never full geometry by default."""
    if depth < 0 or depth > 3 or child_limit < 0 or child_limit > 64:
        raise ValueError("document summary bounds exceeded")
    return exchange("document.inspect", {"depth": depth, "childLimit": child_limit}, port=port)


def current_command(command: str, params: dict[str, Any], *, port: int = 7979) -> Any:
    """Execute one authorized engine command. The caller must verify its result.

    A timeout is ambiguous: no automatic retry, because the command may have
    finished after the reply deadline.
    """
    if not command or not isinstance(params, dict):
        raise ValueError("command and parameters are required")
    return exchange("engine.execute", {"command": command, "params": params}, port=port)
