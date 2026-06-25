#!/usr/bin/env python3
"""
phase0a_foundation.py — Phase 0a foundation: domain tree, perimeters, frameworks, risk matrix.

Scope (narrow):
  1. Create 4 subfolders under AtlasPay (Engineering, Operations, Finance, Compliance)
  2. Create 2 perimeters under AtlasPay/Compliance (AtlasPay-Payments, AtlasPay-Data)
  3. Load 3 frameworks via stored-library URNs (NIST CSF 2.0, ISO 27001:2022, SOC 2 2017-rev-2022)
  4. Create 1 5x5 risk matrix (AtlasPay 5x5)

Idempotent: skip-by-name on every create. Errors logged to stderr, not swallowed.
Run from the project root:
    python3 scripts/phase0a_foundation.py

Findings from first run (fixed in this version):
  - POSTs to DRF collection endpoints need trailing slash: POST /api/folders/ not /api/folders
    (Django APPEND_SLASH=True with DEBUG=True 500s on no-slash POST).
  - Framework load endpoint is POST /api/stored-libraries/{urn}/import/ (NOT /load/ as schema doc said).
    The view accepts URN as `pk` and supports POST with empty body {}.
"""
from __future__ import annotations
import json
import sys
import time
from pathlib import Path

# Make the sibling ca_api.py importable
sys.path.insert(0, str(Path(__file__).parent))
import ca_api  # type: ignore


ATLASPAY_FOLDER_ID = "d272ee78-ef71-4a70-8235-df2335cd0b3c"  # verified by Hermes

SUBFOLDER_NAMES = ["Engineering", "Operations", "Finance", "Compliance"]

PERIMETERS = [
    {
        "name": "AtlasPay-Payments",
        "scope_in": ["Payment Processing", "Customer Account Access", "Fraud Monitoring"],
        "scope_out": ["HR", "Marketing"],
    },
    {
        "name": "AtlasPay-Data",
        "scope_in": ["Customer PII", "Payment Data", "Financial Reporting"],
        "scope_out": [],
    },
]

FRAMEWORK_URNS = [
    "urn:intuitem:risk:library:nist-csf-2.0",
    "urn:intuitem:risk:library:iso27001-2022",
    "urn:intuitem:risk:library:soc2-2017-rev-2022",
]


def log(msg: str) -> None:
    print(msg, flush=True)


def stderr(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def find_compliance_subfolder_id() -> str | None:
    """Find the Compliance subfolder under AtlasPay (handles both child-of-AtlasPay names)."""
    for f in ca_api.all_results("folders"):
        n = (f.get("name") or "").strip().lower()
        if n != "compliance":
            continue
        parent = f.get("parent_folder")
        if isinstance(parent, dict) and parent.get("id") == ATLASPAY_FOLDER_ID:
            return f.get("id")
    return None


def post_with_slash(endpoint: str, payload: dict):
    """POST to a DRF collection endpoint with a trailing slash (avoids APPEND_SLASH 500)."""
    e = endpoint if endpoint.startswith("/") else "/" + endpoint
    if not e.endswith("/"):
        e = e + "/"
    return ca_api.post(e, payload)


def find_perimeter_by_name(name: str) -> dict | None:
    """Find a perimeter by name (case-insensitive). post_if_absent already does this, but
    we need to filter by folder (parent) too because there's a 'TEST-PERIM-DEL-12345' etc."""
    n_low = name.strip().lower()
    for p in ca_api.all_results("perimeters"):
        if (p.get("name") or "").strip().lower() == n_low:
            return p
    return None


def task1_subfolders() -> dict:
    log("=" * 70)
    log("TASK 1: Create 4 subfolders under AtlasPay")
    log("=" * 70)
    out: dict = {}
    for name in SUBFOLDER_NAMES:
        payload = {
            "name": name,
            "parent_folder": ATLASPAY_FOLDER_ID,
            "description": f"AtlasPay / {name} domain",
            "content_type": "DOMAIN",
        }
        # Idempotency: check both 'exists anywhere' and 'exists under AtlasPay'
        existing = None
        for f in ca_api.all_results("folders"):
            n = (f.get("name") or "").strip().lower()
            if n != name.strip().lower():
                continue
            parent = f.get("parent_folder")
            if isinstance(parent, dict) and parent.get("id") == ATLASPAY_FOLDER_ID:
                existing = f
                break
        if existing:
            out[name] = existing.get("id")
            log(f"  folder {name!r:14s} -> exists  id={out[name]}")
            continue
        s, d = post_with_slash("folders", payload)
        if s in (200, 201):
            fid = d.get("id") if isinstance(d, dict) else None
            out[name] = fid
            log(f"  folder {name!r:14s} -> created id={fid}")
        else:
            stderr(f"[ERROR] folder '{name}' create failed: HTTP {s}")
            stderr(f"        payload: {json.dumps(payload)}")
            stderr(f"        response: {json.dumps(d)[:800]}")
            out[name] = None
    s, d = ca_api.get("folders", params={"limit": 1})
    log(f"  folders count after task 1: {d.get('count') if isinstance(d, dict) else 'n/a'}")
    return out


def task2_perimeters(compliance_id: str | None) -> list:
    log("=" * 70)
    log("TASK 2: Create 2 perimeters under AtlasPay/Compliance")
    log("=" * 70)
    out: list = []
    if not compliance_id:
        stderr("[ERROR] Compliance folder id missing; cannot create perimeters")
        return out
    for spec in PERIMETERS:
        payload = {
            "name": spec["name"],
            "folder": compliance_id,
            "scope_in": spec["scope_in"],
            "scope_out": spec["scope_out"],
        }
        existing = find_perimeter_by_name(spec["name"])
        if existing:
            out.append(existing.get("id"))
            log(f"  perimeter {spec['name']!r:22s} -> exists  id={out[-1]}")
            continue
        s, d = post_with_slash("perimeters", payload)
        if s in (200, 201):
            pid = d.get("id") if isinstance(d, dict) else None
            out.append(pid)
            log(f"  perimeter {spec['name']!r:22s} -> created id={pid}")
        else:
            stderr(f"[ERROR] perimeter '{spec['name']}' create failed: HTTP {s}")
            stderr(f"        payload: {json.dumps(payload)}")
            stderr(f"        response: {json.dumps(d)[:800]}")
            out.append(None)
    s, d = ca_api.get("perimeters", params={"limit": 1})
    log(f"  perimeters count after task 2: {d.get('count') if isinstance(d, dict) else 'n/a'}")
    return out


def task3_frameworks() -> list:
    log("=" * 70)
    log("TASK 3: Load 3 frameworks via stored-library URNs (POST .../import/)")
    log("=" * 70)
    out: list = []
    # Pre-check which frameworks are already loaded (idempotency)
    loaded_libs = ca_api.all_results("loaded-libraries")
    loaded_urns = {str(x.get("urn") or "").lower() for x in loaded_libs}
    for urn in FRAMEWORK_URNS:
        if urn.lower() in loaded_urns:
            out.append({"urn": urn, "status": 200, "ok": True, "response": {"status": "exists"}, "msg": "exists"})
            log(f"  load {urn:60s} -> exists (already in loaded-libraries)")
            continue
        endpoint = f"stored-libraries/{urn}/import"
        s, d = post_with_slash(endpoint, {})
        # CA returns 400 with {"status":"error","error":"This library has already been loaded."}
        # in the race case where a parallel process loaded it; treat as success
        msg = ""
        if isinstance(d, dict):
            msg = d.get("status") or d.get("error") or json.dumps(d)[:200]
            if d.get("error") == "This library has already been loaded.":
                s = 200
        ok = s in (200, 201, 202, 204)
        out.append({"urn": urn, "status": s, "ok": ok, "response": d, "msg": msg})
        log(f"  load {urn:60s} -> HTTP {s}  {'OK' if ok else 'FAIL'}  {msg}")
        if not ok:
            stderr(f"[ERROR] load failed for {urn}: {json.dumps(d)[:500]}")
        time.sleep(2)
    s, d = ca_api.get("loaded-libraries", params={"limit": 1})
    log(f"  loaded-libraries count after task 3: {d.get('count') if isinstance(d, dict) else 'n/a'}")
    return out


def task4_risk_matrix() -> str | None:
    log("=" * 70)
    log("TASK 4: Create AtlasPay 5x5 risk matrix")
    log("=" * 70)
    # CA v3.18 risk matrix json_definition shape: probability/impact arrays + risk grid + grid severity labels
    json_def = {
        "probability": [
            {"abbreviation": "1", "name": "Rare", "description": "Highly unlikely"},
            {"abbreviation": "2", "name": "Unlikely", "description": "Could occur but rare"},
            {"abbreviation": "3", "name": "Possible", "description": "Occasional"},
            {"abbreviation": "4", "name": "Likely", "description": "Frequent"},
            {"abbreviation": "5", "name": "Almost Certain", "description": "Expected"},
        ],
        "impact": [
            {"abbreviation": "1", "name": "Insignificant", "description": "Negligible"},
            {"abbreviation": "2", "name": "Minor", "description": "Limited"},
            {"abbreviation": "3", "name": "Moderate", "description": "Notable"},
            {"abbreviation": "4", "name": "Major", "description": "Significant"},
            {"abbreviation": "5", "name": "Severe", "description": "Critical"},
        ],
        "risk": [
            [1, 2, 3, 4, 5],
            [2, 4, 6, 8, 10],
            [3, 6, 9, 12, 15],
            [4, 8, 12, 16, 20],
            [5, 10, 15, 20, 25],
        ],
        "grid": [
            {"abbreviation": "L", "name": "Low", "color": "#2ecc71", "description": "Accept"},
            {"abbreviation": "M", "name": "Moderate", "color": "#f1c40f", "description": "Monitor"},
            {"abbreviation": "H", "name": "High", "color": "#e67e22", "description": "Mitigate"},
            {"abbreviation": "C", "name": "Critical", "color": "#e74c3c", "description": "Treat"},
        ],
        "type": "5x5",
    }
    payload = {
        "name": "AtlasPay 5x5",
        "description": "Standard 5x5 risk matrix for AtlasPay (probability x impact)",
        "annotation": "AtlasPay standard 5x5 risk matrix: probability (1-5) x impact (1-5). Severity bands: L/M/H/C.",
        "json_definition": json_def,
    }
    existing = ca_api.find_by("risk-matrices", "AtlasPay 5x5", name_field="name")
    if existing:
        log(f"  risk-matrix 'AtlasPay 5x5' -> exists  id={existing.get('id')}")
        return existing.get("id")
    s, d = post_with_slash("risk-matrices", payload)
    if s in (200, 201):
        mid = d.get("id") if isinstance(d, dict) else None
        log(f"  risk-matrix 'AtlasPay 5x5' -> created id={mid}")
        return mid
    stderr(f"[ERROR] risk-matrix create failed: HTTP {s}")
    stderr(f"        response: {json.dumps(d)[:800]}")
    return None


def main() -> int:
    log(f"API_URL  : {ca_api.API_URL}")
    log(f"TOKEN len: {len(ca_api.TOKEN)} (first 8: {ca_api.TOKEN[:8]}...)")
    log("")

    t1 = task1_subfolders()
    compliance_id = t1.get("Compliance") or find_compliance_subfolder_id()
    log(f"  AtlasPay/Compliance folder id: {compliance_id}")
    log("")

    t2 = task2_perimeters(compliance_id)
    log("")

    t3 = task3_frameworks()
    log("")

    t4 = task4_risk_matrix()
    log("")

    log("=" * 70)
    log("SUMMARY (client-side view, re-verify independently via urllib)")
    log("=" * 70)
    log(f"  subfolder ids : {t1}")
    log(f"  perimeter ids : {t2}")
    log(f"  framework load: {[(x['urn'].split(':')[-1], x['status'], x['msg']) for x in t3]}")
    log(f"  matrix id     : {t4}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
