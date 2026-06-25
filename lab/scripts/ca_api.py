#!/usr/bin/env python3
"""
ca_api.py — minimal CISO Assistant REST client for the AtlasPay GRC migration.

Loads TOKEN/API_URL from the MCP .env file (no secrets in argv).
Provides:
    get(endpoint, params=None)         -> (status, json-or-text)
    post(endpoint, payload)            -> (status, json-or-text)
    patch(endpoint, payload)           -> (status, json-or-text)
    count(endpoint, params=None)       -> int
    all(endpoint, params=None)         -> list
    get_obj(endpoint, params=None)     -> dict|None  (first matching, used for "exists" check)
    find_by(endpoint, name)            -> dict|None
    post_if_absent(endpoint, name, payload, name_field='name') -> ('created'|'exists', obj)
"""
from __future__ import annotations
import json, os, ssl, sys
from pathlib import Path
from urllib import request, parse, error

ENV_PATH = Path.home() / "Documents/IfeSec/Tools/ciso-assistant-community/cli/.mcp.env"
API_URL  = ""
TOKEN    = ""
VERIFY   = False


def load_env() -> None:
    """Read TOKEN/API_URL/VERIFY_CERTIFICATE from the MCP .env file."""
    global API_URL, TOKEN, VERIFY
    for line in ENV_PATH.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip()
        if k == "TOKEN":
            TOKEN = v
        elif k == "API_URL":
            API_URL = v.rstrip("/")
        elif k == "VERIFY_CERTIFICATE":
            VERIFY = v.lower() in ("true", "1", "yes", "on")


load_env()


def _req(method: str, endpoint: str, payload: dict | None = None, params: dict | None = None):
    # Ensure single slash between API_URL and endpoint
    e = endpoint if endpoint.startswith("/") else "/" + endpoint
    url = f"{API_URL}{e}"
    if params:
        url += "?" + parse.urlencode(params, doseq=True)
    data = None
    headers = {"Authorization": f"Token {TOKEN}", "Accept": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    ctx = None if VERIFY else ssl._create_unverified_context()
    req = request.Request(url, data=data, headers=headers, method=method)
    try:
        with request.urlopen(req, timeout=60, context=ctx) as r:
            body = r.read().decode("utf-8", errors="replace")
            return r.status, (json.loads(body) if body and body[0] in "{[" else body)
    except error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        try:
            return e.code, json.loads(body)
        except Exception:
            return e.code, body
    except Exception as e:
        return 0, f"EXC: {e!r}"


def get(endpoint: str, params: dict | None = None):
    return _req("GET", endpoint, params=params)


def post(endpoint: str, payload: dict):
    return _req("POST", endpoint, payload=payload)


def patch(endpoint: str, payload: dict):
    return _req("PATCH", endpoint, payload=payload)


def count(endpoint: str, params: dict | None = None) -> int:
    """Use the API's paginated 'count' if present, else len(list)."""
    s, d = get(endpoint, params={**(params or {}), "limit": 1})
    if s != 200:
        return -1
    if isinstance(d, dict) and "count" in d:
        return int(d["count"])
    if isinstance(d, list):
        return len(d)
    return -1


def all_results(endpoint: str, params: dict | None = None, page_size: int = 200) -> list:
    """Fetch all results, following DRF pagination."""
    s, d = get(endpoint, params={**(params or {}), "limit": page_size})
    if s != 200:
        return []
    if isinstance(d, dict) and "results" in d:
        out = list(d["results"])
        nxt = d.get("next")
        while nxt:
            # nxt may be a relative path like /api/stored-libraries/?limit=50&offset=50
            # or a full URL. Strip "/api" prefix so _req can prepend it once.
            if nxt.startswith("http://") or nxt.startswith("https://"):
                path = nxt.split(API_URL, 1)[-1]
            else:
                path = nxt
            # _req adds "/" before the path; if path already starts with "/api/", strip it
            if path.startswith("/api/"):
                path = path[len("/api"):]  # leaves "/stored-libraries/?..."
            q = dict(parse.parse_qsl(parse.urlparse(nxt).query))
            s2, d2 = get(path, params=q)
            if s2 != 200 or not isinstance(d2, dict):
                break
            out.extend(d2.get("results", []))
            nxt = d2.get("next")
        return out
    if isinstance(d, list):
        return d
    return []


def find_by(endpoint: str, name: str, name_field: str = "name", folder: str | None = None) -> dict | None:
    """Find a record by name (case-insensitive exact match)."""
    for r in all_results(endpoint, params={"limit": 500}):
        if str(r.get(name_field, "")).strip().lower() == str(name).strip().lower():
            if folder is None or r.get("folder") in (folder, None):
                return r
    return None


def post_if_absent(endpoint: str, name: str, payload: dict, name_field: str = "name") -> tuple[str, dict | None]:
    existing = find_by(endpoint, name, name_field=name_field)
    if existing:
        return "exists", existing
    s, d = post(endpoint, payload)
    if s in (200, 201):
        return "created", (d if isinstance(d, dict) else None)
    return "error", {"status": s, "response": d, "sent": payload}


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("op", choices=["count", "list", "probe", "raw-get", "raw-post"])
    ap.add_argument("endpoint")
    ap.add_argument("--payload", help="JSON payload string")
    ap.add_argument("--params", help="JSON params string")
    args = ap.parse_args()
    if args.op == "count":
        print(count(args.endpoint, json.loads(args.params) if args.params else None))
    elif args.op == "list":
        rs = all_results(args.endpoint, json.loads(args.params) if args.params else None)
        for r in rs:
            print(json.dumps(r, default=str))
    elif args.op == "raw-get":
        s, d = get(args.endpoint, json.loads(args.params) if args.params else None)
        print(s, json.dumps(d, default=str)[:2000])
    elif args.op == "raw-post":
        s, d = post(args.endpoint, json.loads(args.payload))
        print(s, json.dumps(d, default=str)[:2000])
    else:
        s, d = get(args.endpoint, json.loads(args.params) if args.params else None)
        print(s, json.dumps(d, default=str)[:2000])


if __name__ == "__main__":
    main()
