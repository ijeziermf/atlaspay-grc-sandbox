#!/usr/bin/env bash
# AtlasPay GRC Data Ingestion — Phase 0b
# Scope: Ingest 22 records into CISO Assistant v3.18.3
# - 6 risk-scenarios (R-01..R-06)
# - 4 policies (ACC-01, IR-01, SA-01, TPRM-01)
# - 7 entities (vendors) + 7 contracts
# - 1 incident (phishing from R-01)
# - 4 assets with recovery_objective + recovery_point_objective (BCPs as assets)
#
# BCP encoding: business-continuity-plans is NOT in v3.18.3 OSS. Encode each
# BCP as an asset with recovery_objective + recovery_point_objective custom
# fields. This preserves the operational data (RTO/RPO) within the live system.
#
# Prerequisites: Phase 0a complete (domain tree, perimeters, frameworks, matrix)
# Run: cd ~/Documents/IfeSec/Projects/atlaspay-grc-sandbox && ./ingest_data.sh

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== AtlasPay GRC Data Ingestion — Phase 0b ==="
echo "Working dir: $SCRIPT_DIR"
echo ""

# Verify prerequisites
echo "[prereq] Verifying Phase 0a complete..."
python3 - <<'PYEOF'
import urllib.request, json, ssl, sys
from pathlib import Path
env_path = Path("/Users/ifeanyi/Documents/IfeSec/Tools/ciso-assistant-community/cli/.mcp.env")
TOKEN = ""
for line in env_path.read_text().splitlines():
    if line.startswith("TOKEN="):
        TOKEN = line.split("=", 1)[1].strip().strip('"').strip("'")
        break
if not TOKEN:
    print(f"[prereq FAIL] TOKEN not found in {env_path}")
    sys.exit(1)
ctx = ssl._create_unverified_context()
checks = {
    'folders': 6,           # Global + AtlasPay + Engineering + Operations + Finance + Compliance
    'perimeters': 5,         # 3 existing + 2 new
    'risk-matrices': 1,      # new AtlasPay 5x5
    'loaded-libraries': 55,  # 52 default + 3 frameworks
}
all_ok = True
for ep, expected in checks.items():
    req = urllib.request.Request(f'https://localhost:8443/api/{ep}/?limit=1',
                                 headers={'Authorization': f'Token {TOKEN}'})
    d = json.loads(urllib.request.urlopen(req, context=ctx, timeout=10).read())
    actual = d.get('count', 0)
    status = "OK" if actual >= expected else "FAIL"
    print(f"  {ep}: {actual} (expected >= {expected}) {status}")
    if actual < expected:
        all_ok = False
if not all_ok:
    print("\n[prereq FAIL] Phase 0a not complete. Run scripts/phase0a_foundation.py first.")
    sys.exit(1)
print("[prereq OK] Phase 0a complete. Proceeding with data ingestion.")
PYEOF

echo ""
echo "[1/5] Ingesting 6 risk-scenarios..."
python3 scripts/ingest_risk_scenarios.py

echo ""
echo "[2/5] Ingesting 4 policies..."
python3 scripts/ingest_policies.py

echo ""
echo "[3/5] Ingesting 7 entities (vendors)..."
python3 scripts/ingest_entities.py

echo ""
echo "[4/5] Ingesting 1 incident..."
python3 scripts/ingest_incidents.py

echo ""
echo "[5/5] Ingesting 4 assets (BCPs encoded)..."
python3 scripts/ingest_assets_bcps.py

echo ""
echo "=== Verification (independent urllib GET) ==="
python3 scripts/verify_phase_0b.py

echo ""
echo "=== Phase 0b complete ==="
