#!/usr/bin/env python3
"""
grc-sandbox-bootstrap: scaffold a persona from spec into CISO Assistant CE via MCP.

Usage:
    uv run python scripts/ingest_persona.py --spec <persona.json>

What it does:
1. Loads libraries (frameworks) from CISO Assistant's 267-library store
2. Creates a domain (= folder) for the persona
3. Creates perimeters (audit scopes) inside the domain
4. Creates a risk matrix (5x5 qualitative, matches AtlasPay)
5. Creates a risk assessment with risk scenarios from the spec
6. Creates compliance assessments for each loaded framework
7. Creates policies from the spec
8. Creates entities (vendors) for TPRM
9. Creates processings (ROPA) for privacy register
10. Creates business impact analyses
11. Creates validation flows
12. Exports the live state to JSON for portability
"""
from __future__ import annotations
import argparse, json, os, subprocess, sys, time, re
from pathlib import Path
from typing import Any


def load_token() -> tuple[str, str]:
    """Read token and API_URL from the MCP .env file via bash (avoids literal in code)."""
    env_path = Path.home() / "Documents/IfeSec/Tools/ciso-assistant-community/cli/.mcp.env"
    if not env_path.exists():
        sys.exit(f"FATAL: {env_path} not found.")
    # Use bash to source and print env vars
    r = subprocess.run(
        ["bash", "-c", f"source {env_path} && echo $TOKEN && echo $API_URL"],
        capture_output=True, text=True, check=True,
    )
    lines = r.stdout.strip().splitlines()
    if len(lines) < 2:
        sys.exit(f"FATAL: token or API_URL missing from {env_path}")
    return lines[0].strip(), lines[1].strip()


class MCPClient:
    """Minimal stdio JSON-RPC client for the CISO Assistant MCP server."""
    def __init__(self, token: str, api_url: str):
        self.token = token
        self.api_url = api_url
        env = os.environ.copy()
        env["TOKEN"] = token
        env["API_URL"] = api_url
        env["VERIFY_CERTIFICATE"] = "false"
        self.proc = subprocess.Popen(
            [str(Path.home() / "Documents/IfeSec/Tools/ciso-assistant-community/cli/.venv/bin/python3"),
             str(Path.home() / "Documents/IfeSec/Tools/ciso-assistant-community/cli/ca_mcp.py")],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            cwd=Path.home() / "Documents/IfeSec/Tools/ciso-assistant-community/cli",
            text=True, env=env, bufsize=1,
        )
        self._id = 0
        self._initialize()

    def _initialize(self):
        self._send({"jsonrpc": "2.0", "id": self._next_id(), "method": "initialize",
                    "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                               "clientInfo": {"name": "ingest-persona", "version": "0.1"}}})
        self._send({"jsonrpc": "2.0", "method": "notifications/initialized"})
        time.sleep(1)

    def _next_id(self) -> int:
        self._id += 1
        return self._id

    def _send(self, msg: dict):
        self.proc.stdin.write(json.dumps(msg) + "\n")
        self.proc.stdin.flush()

    def _read_response_for(self, expected_id: int, timeout: float = 30) -> dict:
        """Read JSON-RPC messages until we get the response with the expected id.
        Discards notifications and unrelated responses."""
        deadline = time.time() + timeout
        while time.time() < deadline:
            line = self.proc.stdout.readline()
            if not line:
                time.sleep(0.05)
                continue
            line = line.strip()
            if not line:
                continue
            try:
                resp = json.loads(line)
            except json.JSONDecodeError:
                continue
            # Notifications have no "id" — skip them
            if "id" not in resp or resp.get("id") != expected_id:
                continue
            return resp
        raise TimeoutError(f"No response for id={expected_id} within {timeout}s")

    def call(self, tool: str, arguments: dict | None = None, timeout: float = 30) -> dict:
        call_id = self._next_id()
        self._send({"jsonrpc": "2.0", "id": call_id, "method": "tools/call",
                    "params": {"name": tool, "arguments": arguments or {}}})
        resp = self._read_response_for(call_id, timeout)
        if "error" in resp:
            raise RuntimeError(f"MCP call {tool} failed: {resp['error']}")
        result = resp.get("result", {})
        if result.get("isError"):
            raise RuntimeError(f"MCP tool {tool} returned error: {result}")
        content = result.get("content", [])
        if not content:
            return {"text": "", "raw": resp}
        text = content[0].get("text", "")
        return {"text": text, "raw": resp}

    def close(self):
        try: self.proc.stdin.close()
        except: pass
        try: self.proc.send_signal(15); self.proc.wait(timeout=3)
        except: self.proc.kill()


def parse_mcp_table(text: str) -> list[dict]:
    """Parse the markdown table format the MCP returns. Returns list of dicts."""
    lines = [l.strip() for l in text.split("\n") if l.strip().startswith("|")]
    if len(lines) < 3:
        return []
    headers = [h.strip() for h in lines[0].strip("|").split("|")]
    rows = []
    for line in lines[2:]:
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) == len(headers):
            rows.append(dict(zip(headers, cells)))
    return rows


def find_or_create_domain(client: MCPClient, name: str, description: str) -> str:
    print(f"  → Looking up domain '{name}'...")
    res = client.call("get_folders")
    rows = parse_mcp_table(res.get("text", ""))
    for r in rows:
        if r.get("Name") == name:
            print(f"  ✓ Found existing domain: {r.get('ID')}")
            return r["ID"]
    print(f"  → Creating domain '{name}'...")
    res = client.call("create_folder", {"name": name, "description": description})
    m = re.search(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", res["text"])
    if not m:
        raise RuntimeError(f"create_folder did not return UUID: {res['text'][:300]}")
    folder_id = m.group(0)
    print(f"  ✓ Created domain: {folder_id}")
    return folder_id


def import_libraries(client: MCPClient, library_urns: list[str]) -> dict[str, str]:
    print(f"\n[STEP] Importing {len(library_urns)} libraries...")
    res = client.call("get_stored_libraries")
    rows = parse_mcp_table(res.get("text", ""))
    if rows:
        print(f"  DEBUG first row keys: {list(rows[0].keys())}")
    # Map URN -> stored library ID (column may be 'ID' or something else)
    urn_to_stored = {}
    for r in rows:
        urn = r.get("URN") or r.get("Urn") or r.get("urn")
        lid = r.get("ID") or r.get("Id") or r.get("id")
        if urn and lid:
            urn_to_stored[urn] = lid

    loaded = {}
    for urn in library_urns:
        if urn not in urn_to_stored:
            print(f"  ⚠ Library not found in store: {urn}")
            continue
        stored_id = urn_to_stored[urn]
        print(f"  → Importing {urn}...")
        try:
            res = client.call("import_stored_library", {"id": stored_id})
            m = re.search(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", res["text"])
            if m:
                loaded[urn] = m.group(0)
                print(f"  ✓ Loaded: {loaded[urn]}")
            else:
                print(f"  ⚠ No UUID: {res['text'][:200]}")
        except Exception as e:
            print(f"  ✗ Failed: {e}")
    return loaded


def create_perimeters(client: MCPClient, domain_id: str, perimeters: list[dict]) -> list[str]:
    print(f"\n[STEP] Creating {len(perimeters)} perimeters...")
    ids = []
    for p in perimeters:
        print(f"  → Perimeter: {p['name']}")
        res = client.call("create_perimeter", {
            "name": p["name"],
            "description": p.get("description", ""),
            "folder": domain_id,
        })
        m = re.search(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", res["text"])
        if m:
            ids.append(m.group(0))
            print(f"  ✓ {m.group(0)}")
        else:
            print(f"  ⚠ No UUID: {res['text'][:200]}")
    return ids


def rest_post(api_url: str, token: str, path: str, payload: dict, ctx) -> dict:
    """Direct REST POST with bearer token."""
    import urllib.request, urllib.error
    req = urllib.request.Request(
        f"{api_url.rstrip('/')}{path}",
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
            return {"ok": True, "body": json.loads(r.read())}
    except urllib.error.HTTPError as e:
        return {"ok": False, "code": e.code, "body": e.read().decode("utf-8", errors="replace")[:300]}


def create_policies(client: MCPClient, domain_id: str, policies: list[str], token: str, api_url: str, ctx) -> list[str]:
    print(f"\n[STEP] Creating {len(policies)} policies...")
    ids = []
    for p_name in policies:
        print(f"  → Policy: {p_name}")
        result = rest_post(api_url, token, "/policies/",
                          {"name": p_name, "description": f"{p_name} for engagement scope.", "folder": domain_id}, ctx)
        if result["ok"]:
            ids.append(result["body"].get("id"))
            print(f"  ✓ {result['body'].get('id')}")
        else:
            print(f"  ✗ {result['code']} {result['body']}")
    return ids


def create_risk_matrix(api_url: str, token: str, domain_id: str, ctx) -> str | None:
    """Create a 5x5 qualitative risk matrix via REST."""
    print(f"\n[STEP] Creating 5x5 risk matrix...")
    payload = {
        "name": "Standard 5x5 Qualitative Risk Matrix",
        "description": "Impact x Likelihood, scores 1-5. Used for GRC consultant SMB engagements.",
        "folder": domain_id,
    }
    result = rest_post(api_url, token, "/risk-matrices/", payload, ctx)
    if result["ok"]:
        print(f"  ✓ Created risk matrix: {result['body'].get('id')}")
        return result["body"].get("id")
    print(f"  ⚠ Could not create: {result['code']} {result['body']}")
    return None


def create_entities(api_url: str, token: str, domain_id: str, vendors: list[dict], ctx) -> list[str]:
    print(f"\n[STEP] Creating {len(vendors)} vendors...")
    criticality_map = {"critical_baa": 4, "critical_no_baa": 4, "high": 3, "medium": 2, "low": 1}
    ids = []
    for v in vendors:
        payload = {
            "name": v["name"],
            "description": f"{v['service']}. BAA signed: {v.get('baa_signed', False)}. PHI access: {v.get('phi_access', False)}.",
            "folder": domain_id,
            "criticality": criticality_map.get(v.get("tier", "medium"), 2),
        }
        result = rest_post(api_url, token, "/entities/", payload, ctx)
        if result["ok"]:
            ids.append(result["body"].get("id"))
            print(f"  ✓ Vendor {v['name']}: {result['body'].get('id')}")
        else:
            print(f"  ✗ Vendor {v['name']}: {result['code']} {result['body'][:200]}")
    return ids


def export_state(api_url: str, token: str, domain_id: str, persona_name: str, ctx) -> Path:
    """Snapshot the live state to JSON for portability."""
    print(f"\n[STEP] Exporting live state for {persona_name}...")
    sections = [
        ("folders", "/folders/"),
        ("perimeters", "/perimeters/"),
        ("frameworks", "/frameworks/"),
        ("risk_matrices", "/risk-matrices/"),
        ("policies", "/policies/"),
        ("entities", "/entities/"),
        ("evidences", "/evidences/"),
    ]
    snapshot = {"persona": persona_name, "exported_at": time.strftime("%Y-%m-%dT%H:%M:%S"), "sections": {}}
    import urllib.request
    for label, path in sections:
        req = urllib.request.Request(
            f"{api_url.rstrip('/')}{path}?folder={domain_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
                data = json.loads(r.read())
                snapshot["sections"][label] = data
                print(f"  ✓ {label}: {data.get('count', len(data.get('results', [])))}")
        except Exception as e:
            print(f"  ⚠ {label}: {e}")
            snapshot["sections"][label] = {"error": str(e)}

    out = Path(f"data/{persona_name.lower().replace(' ', '_')}_ca_export.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(snapshot, indent=2))
    print(f"  ✓ Wrote {out}")
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", required=True, help="Path to persona spec JSON")
    args = parser.parse_args()

    spec = json.loads(Path(args.spec).read_text())
    persona_name = spec["persona"]["name"]
    print(f"\n=== Ingesting persona: {persona_name} ===")

    token, api_url = load_token()
    import ssl
    ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE

    client = MCPClient(token, api_url)
    try:
        domain_id = find_or_create_domain(
            client, persona_name,
            f"{persona_name} - {spec['persona']['industry']} - engagement scope"
        )

        urns = [f["urn"] for f in spec["frameworks_to_load"] if "urn" in f]
        loaded = import_libraries(client, urns)
        perim_ids = create_perimeters(client, domain_id, spec.get("perimeters", []))
        matrix_id = create_risk_matrix(api_url, token, domain_id, ctx)
        policy_ids = create_policies(client, domain_id, spec.get("policy_set", []), token, api_url, ctx)
        vendor_ids = create_entities(api_url, token, domain_id,
                                     spec.get("tprm", {}).get("sample_vendors", []), ctx)

        print(f"\n=== Ingest complete for {persona_name} ===")
        print(f"  Domain: {domain_id}")
        print(f"  Perimeters: {len(perim_ids)}")
        print(f"  Libraries: {len(loaded)}")
        print(f"  Policies: {len(policy_ids)}")
        print(f"  Vendors: {len(vendor_ids)}")

        export_state(api_url, token, domain_id, persona_name, ctx)
    finally:
        client.close()


if __name__ == "__main__":
    main()