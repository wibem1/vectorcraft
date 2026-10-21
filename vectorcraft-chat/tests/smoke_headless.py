#!/usr/bin/env python3
"""Live smoke test against the real VectorCraft CLI MCP headless engine.

Run: python vectorcraft-chat/tests/smoke_headless.py path/to/vectorcraft-cli
No OpenRouter key or GUI required. Fails closed if an object cannot be identified.
"""
import json
import os
import select
import subprocess
import sys
import time

class MCP:
    def __init__(self, binary):
        self.proc = subprocess.Popen([binary, "mcp", "--headless"], stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                     bufsize=0)
        self.serial = 0
        self.incoming = bytearray()
    def call(self, method, params, timeout=45):
        self.serial += 1
        ident = self.serial
        payload = {"jsonrpc":"2.0","id":ident,"method":method,"params":params}
        self.proc.stdin.write((json.dumps(payload)+"\n").encode("utf-8"))
        self.proc.stdin.flush()
        until = time.monotonic()+timeout
        while True:
            remaining = until-time.monotonic()
            if remaining <= 0:
                raise RuntimeError("MCP timeout at "+method)
            while b"\n" not in self.incoming:
                ready, _, _ = select.select([self.proc.stdout],[],[],remaining)
                if not ready:
                    raise RuntimeError("MCP timeout at "+method)
                chunk = os.read(self.proc.stdout.fileno(),65536)
                if not chunk:
                    raise RuntimeError("MCP process exited unexpectedly")
                self.incoming.extend(chunk)
                remaining = until-time.monotonic()
                if remaining <= 0:
                    raise RuntimeError("MCP timeout at "+method)
            line, _, rest = self.incoming.partition(b"\n")
            self.incoming = bytearray(rest)
            response = json.loads(line)
            if response.get("id") != ident:
                if "id" not in response:  # notifications
                    continue
                raise RuntimeError("MCP response ID mismatch")
            if "error" in response:
                raise RuntimeError(str(response["error"]))
            result = response.get("result", {})
            if result.get("isError"):
                raise RuntimeError("MCP tool error: "+json.dumps(result)[:1200])
            return result
    def tool(self, name, args):
        result = self.call("tools/call",{"name":name,"arguments":args})
        contents=result.get("content",[])
        output=[]
        for item in contents:
            if item.get("type")=="text":
                txt=item.get("text","")
                try: output.append(json.loads(txt))
                except ValueError: output.append(txt)
        return output[0] if len(output)==1 else output
    def close(self):
        if self.proc.poll() is None:
            self.proc.terminate()
            try: self.proc.wait(timeout=4)
            except subprocess.TimeoutExpired: self.proc.kill()

def nodes(value):
    """Collect IDs from documented inspection's layer tree, ignoring selection."""
    found=set()
    def walk(obj, parent=""):
        if isinstance(obj,dict):
            if parent in ("layers","children","objects") and type(obj.get("id")) is int:
                found.add(obj["id"])
            for k,v in obj.items():
                if k not in ("selection","history"):
                    walk(v,k)
        elif isinstance(obj,list):
            for v in obj: walk(v,parent)
    walk(value)
    return found

def selection_ids(value):
    if isinstance(value,dict):
        sel=value.get("selection")
        if isinstance(sel,list):
            return [i.get("id") if isinstance(i,dict) else i for i in sel]
        for v in value.values():
            s=selection_ids(v)
            if s is not None: return s
    return None

def main(binary):
    m=MCP(binary)
    try:
        m.call("initialize",{"protocolVersion":"2025-06-18",
                             "capabilities":{},"clientInfo":{"name":"vc-chat-ci","version":"0.1"}})
        m.proc.stdin.write((json.dumps({"jsonrpc":"2.0","method":"notifications/initialized"})+"\n").encode("utf-8"))
        m.proc.stdin.flush()
        before=m.tool("inspect_document",{"depth":5})
        print("Initial inspection OK",flush=True)
        drawn=m.tool("draw_path",{"points":[[300,155],[390,310],[210,310]],
                                   "closed":True,"fill":"none","stroke":"#000000",
                                   "strokeWidth":2})
        after=m.tool("inspect_document",{"depth":5})
        old=nodes(before); new=nodes(after)-old
        if len(new)!=1:
            raise RuntimeError(f"Expected exactly one new object; got {sorted(new)}; draw reply={str(drawn)[:500]}")
        target=next(iter(new))
        print("Created new object ID",target,flush=True)
        selected=m.tool("run_command",{"command":"select.set","params":{"ids":[target]}})
        checked=m.tool("inspect_document",{"depth":5})
        if selection_ids(checked)!=[target]:
            raise RuntimeError(f"Selection mismatch: {selection_ids(checked)}; reply={str(selected)[:250]}")
        geometry_before=m.tool("run_command",{"command":"document.node","params":{"id":target}})
        m.tool("run_command",{"command":"object.rotate","params":{"angle":30}})
        geometry_after=m.tool("run_command",{"command":"document.node","params":{"id":target}})
        if geometry_before == geometry_after:
            raise RuntimeError("Rotation did not change the target object's model")
        rotated=m.tool("inspect_document",{"depth":5})
        if target not in nodes(rotated):
            raise RuntimeError("Target object disappeared after rotation")
        print("PASS: path created, ID selected, object model changed after rotation, ID persisted",flush=True)
        print("LIMIT: exact geometric angle and rendered appearance not yet asserted",flush=True)
    finally:
        m.close()

if __name__=="__main__":
    if len(sys.argv)!=2:
        sys.exit("Usage: smoke_headless.py /path/to/vectorcraft-cli")
    main(sys.argv[1])
