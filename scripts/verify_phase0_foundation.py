#!/usr/bin/env python3
"""
verify_phase0_foundation.py — independent verification of Phase 0 foundation
via stdlib urllib only. Does NOT import scripts/ca_api.py or use any of its
helpers; reads TOKEN/API_URL directly from the .mcp.env file.

Checks the four Phase 0 foundation deliverables:
  (1) Domain tree subfolders under AtlasPay
  (2) 2 perimeters under Compliance
  (3) 3 frameworks loaded (NIST CSF 2.0, ISO 27001:2022, SOC 2)
  (4) one 5x5 risk matrix with a populated json_definition
"""
from __future__ import annotations

import json
import ssl
import sys
from urllib import error, parse, request

ENV_PATH = "/Users/ifeanyi/Documents/IfeSec/Tools/ciso-assistant-community/cli/.mcp.env"


def load_env():
    env = {}
    with open(ENV_PATH) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    if "API_URL" not in env or "TOKEN" not in env:
        raise SystemExit(f"FATAL: API_URL or TOKEN missing from {ENV_PATH}")
    return env["API_URL"].rstrip("/"), env["TOKEN"]


API_URL, TOKEN = load_env()
CTX = ssl._create_unverified_context()


def raw_get(path, params=None):
    url = API_URL + path
    if params:
        url += "?" + parse.urlencode(params, doseq=True)
    req = request.Request(
        url,
        headers={
            "Authorization": f"Token {TOKEN}",
            "Accept": "application/json",
        },
    )
    try:
        with request.urlopen(req, timeout=30, context=CTX) as r:
            body = r.read().decode("utf-8", errors="replace")
            return r.status, json.loads(body) if body and body[0] in "{[" else body
    except error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace")[:400]
    except Exception as e:
        return 0, f"EXC: {e!r}"


def all_pages(path, params=None, page_size=200):
    """DRF pagination helper. Returns (list_of_results, http_status)."""
    out = []
    p = dict(params or {})
    p["limit"] = page_size
    s, d = raw_get(path, p)
    if s != 200:
        return out, s
    if isinstance(d, dict) and "results" in d:
        out.extend(d["results"])
        nxt = d.get("next")
        while nxt:
            # nxt may be absolute URL or relative path; for our API it's relative
            if nxt.startswith("http"):
                path2 = nxt.split(API_URL, 1)[-1]
            else:
                path2 = nxt
            q = dict(parse.parse_qsl(parse.urlparse(nxt).query))
            s2, d2 = raw_get(path2, q)
            if s2 != 200 or not isinstance(d2, dict):
                break
            out.extend(d2.get("results", []))
            nxt = d2.get("next")
    elif isinstance(d, list):
        out.extend(d)
    return out, s


def _fk_id(value):
    """Normalize a FK field that may be either a bare UUID string or
    a nested {str, id} dict (CA REST serialization)."""
    if value is None:
        return None
    if isinstance(value, dict):
        return value.get("id")
    return value


def main():
    results = {}

    # (1) DOMAIN TREE SUBFOLDERS UNDER AtlasPay
    print("=" * 70)
    print("(1) DOMAIN TREE SUBFOLDERS UNDER AtlasPay")
    print("=" * 70)
    folders, s = all_pages("/folders/")
    atlaspay = next((f for f in folders if f.get("name") == "AtlasPay"), None)
    if not atlaspay:
        print("  ✗ FAIL: AtlasPay root folder not present")
        results["folders"] = False
    else:
        atlaspay_id = atlaspay.get("id")
        sub = [f for f in folders if _fk_id(f.get("parent_folder")) == atlaspay_id]
        names = sorted(f["name"] for f in sub)
        print(f"  AtlasPay folder id      = {atlaspay_id}")
        print(f"  AtlasPay content_type   = {atlaspay.get('content_type')}")
        print(f"  Subfolders (count={len(sub)}):")
        for n in names:
            print(f"    - {n}")
        results["folders"] = len(sub) >= 1 and atlaspay.get("content_type") == "DOMAIN"
        print(f"  Result: {'✓ PASS' if results['folders'] else '✗ FAIL'}")

    # (2) 2 PERIMETERS UNDER Compliance
    print()
    print("=" * 70)
    print("(2) 2 PERIMETERS UNDER Compliance")
    print("=" * 70)
    compliance = next((f for f in folders if f.get("name") == "Compliance"), None) if folders else None
    if not compliance:
        print("  ✗ FAIL: Compliance folder not present")
        results["perimeters"] = False
    else:
        perimeters, ps = all_pages("/perimeters/")
        compl_perims = [p for p in perimeters if _fk_id(p.get("folder")) == compliance.get("id")]
        print(f"  Compliance folder id    = {compliance.get('id')}")
        print(f"  Perimeters under Compliance (count={len(compl_perims)}):")
        for p in sorted(compl_perims, key=lambda x: x["name"]):
            print(f"    - {p['name']}  (id={p['id']})")
        results["perimeters"] = len(compl_perims) == 2
        print(f"  Result: {'✓ PASS' if results['perimeters'] else '✗ FAIL'}")

    # (3) 3 FRAMEWORKS LOADED (NIST CSF 2.0, ISO 27001:2022, SOC 2)
    print()
    print("=" * 70)
    print("(3) 3 FRAMEWORKS LOADED VIA URN")
    print("=" * 70)
    libs, ls = all_pages("/loaded-libraries/", page_size=200)
    targets = [
        ("nist-csf-2.0",       "urn:intuitem:risk:library:nist-csf-2.0"),
        ("iso27001-2022",      "urn:intuitem:risk:library:iso27001-2022"),
        ("soc2-2017-rev-2022", "urn:intuitem:risk:library:soc2-2017-rev-2022"),
    ]
    found = {}
    for lib in libs:
        urn = (lib.get("urn") or "").lower()
        name = (lib.get("name") or "").lower()
        for slug, full_urn in targets:
            # match by URN suffix or by normalized name
            if full_urn.endswith(slug) and (
                urn.endswith(slug) or slug in name.replace(" ", "-") or slug in name.replace("/", "-")
            ):
                found[slug] = lib
    print(f"  Total loaded libraries: {len(libs)}")
    for slug, full_urn in targets:
        if slug in found:
            lib = found[slug]
            print(f"  ✓ {full_urn}")
            print(f"      name = {lib.get('name')!r}")
            print(f"      urn  = {lib.get('urn')}")
            print(f"      id   = {lib.get('id')}")
        else:
            print(f"  ✗ {full_urn}  NOT FOUND")
    results["frameworks"] = len(found) == 3
    print(f"  Result: {'✓ PASS' if results['frameworks'] else '✗ FAIL'}")

    # (4) ONE 5x5 RISK MATRIX with populated json_definition
    print()
    print("=" * 70)
    print("(4) ONE 5x5 RISK MATRIX (populated)")
    print("=" * 70)
    matrices, ms = all_pages("/risk-matrices/")
    matrix_ok = False
    matrix_details = {}
    if len(matrices) == 0:
        print("  ✗ FAIL: zero risk matrices")
    elif len(matrices) > 1:
        print(f"  ✗ FAIL: expected 1 risk matrix, found {len(matrices)}")
    else:
        m = matrices[0]
        jd = m.get("json_definition")
        # REST returns json_definition as a string; parse it
        if isinstance(jd, str):
            try:
                jd = json.loads(jd)
            except Exception as e:
                jd = {"_parse_error": str(e)}
        prob = jd.get("probability", []) if isinstance(jd, dict) else []
        imp = jd.get("impact", []) if isinstance(jd, dict) else []
        risk = jd.get("risk", []) if isinstance(jd, dict) else []
        grid = jd.get("grid", []) if isinstance(jd, dict) else []
        print(f"  Name: {m.get('name')!r}")
        print(f"  id:   {m.get('id')}")
        print(f"  json_definition keys: {list(jd.keys()) if isinstance(jd, dict) else type(jd).__name__}")
        print(f"  probability levels: {len(prob)}  -> ids: {[p.get('id') for p in prob]}")
        print(f"  impact levels:      {len(imp)}  -> ids: {[i.get('id') for i in imp]}")
        print(f"  risk levels:        {len(risk)}  -> ids: {[r.get('id') for r in risk]}")
        if grid:
            print(f"  grid: {len(grid)} rows x {len(grid[0]) if grid else 0} cols")
            for i, row in enumerate(grid):
                print(f"      prob={i}: {row}")
        matrix_ok = len(prob) == 5 and len(imp) == 5 and len(risk) == 5 and len(grid) == 5
        matrix_details = {
            "id": m.get("id"),
            "name": m.get("name"),
            "prob_count": len(prob),
            "imp_count": len(imp),
            "risk_count": len(risk),
            "grid_rows": len(grid),
            "grid_cols": len(grid[0]) if grid else 0,
        }
        if not matrix_ok:
            print("  ✗ FAIL: matrix not properly populated")
        else:
            print("  ✓ PASS: 5x5 matrix fully populated")
    results["risk_matrix"] = matrix_ok
    results["matrix_details"] = matrix_details

    # SUMMARY
    print()
    print("=" * 70)
    print("PHASE 0 FOUNDATION VERIFICATION SUMMARY")
    print("=" * 70)
    labels = {
        "folders":     "(1) AtlasPay subfolders",
        "perimeters":  "(2) 2 perimeters under Compliance",
        "frameworks":  "(3) 3 frameworks via URN",
        "risk_matrix": "(4) 5x5 risk matrix (populated)",
    }
    all_ok = True
    for k, label in labels.items():
        v = results.get(k)
        status = "✓ PASS" if v else "✗ FAIL"
        if not v:
            all_ok = False
        print(f"  {status}  {label}")
    print()
    print(f"OVERALL: {'✓ ALL FOUR DELIVERABLES VERIFIED' if all_ok else '✗ AT LEAST ONE FAILED'}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
