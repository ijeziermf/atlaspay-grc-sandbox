"""AtlasPay Phase 0b verification — independent API count via raw urllib.

This script does NOT use ca_api.py. It opens fresh urllib connections and
re-GETs each model count. Hermes COO can compare this output to the ca_api
results to detect client-vs-server state divergence.
"""

import json
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path


ENV_PATH = Path("/Users/ifeanyi/Documents/IfeSec/Tools/ciso-assistant-community/cli/.mcp.env")
EXPECTED_COUNTS = {
    "folders": 6,                  # Global + AtlasPay + 4 subfolders
    "perimeters": 5,                # 3 existing + 2 new (Payments, Data)
    "risk-scenarios": 6,            # R-01..R-06
    "policies": 4,                  # ACC-01, IR-01, SA-01, TPRM-01
    "entities": 7,                  # V-01..V-07
    "contracts": 7,                 # 1 MSA per entity
    "incidents": 1,                 # INC-001 phishing
    "assets": 4,                    # 4 BCPs encoded as assets
    "loaded-libraries": 55,         # 52 default + 3 frameworks
    "risk-matrices": 1,             # 5x5
}


def get_token() -> str:
    for line in ENV_PATH.read_text().splitlines():
        if line.startswith("TOKEN="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise RuntimeError("TOKEN not found in .mcp.env")


def count(endpoint: str, token: str, ctx: ssl.SSLContext) -> int:
    url = f"https://localhost:8443/api/{endpoint}/?limit=1"
    req = urllib.request.Request(url, headers={"Authorization": f"Token {token}"})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            d = json.loads(resp.read())
            return d.get("count", 0)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"  [ERROR] {endpoint}: HTTP {e.code} -- {body[:200]}")
        return -1
    except Exception as e:
        print(f"  [ERROR] {endpoint}: {e}")
        return -1


def main() -> int:
    token = get_token()
    ctx = ssl._create_unverified_context()

    print("=== Phase 0b Verification (independent urllib, raw) ===")
    print(f"{'Model':<25} {'Actual':>8} {'Expected':>10} {'Status':>8}")
    print("-" * 55)
    all_ok = True
    for ep, expected in EXPECTED_COUNTS.items():
        actual = count(ep, token, ctx)
        if actual < 0:
            status = "ERROR"
            all_ok = False
        elif actual >= expected:
            status = "OK"
        else:
            status = "SHORT"
            all_ok = False
        print(f"{ep:<25} {actual:>8} {expected:>10} {status:>8}")
    print("-" * 55)
    print("RESULT:", "PASS" if all_ok else "PARTIAL/FAIL")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
