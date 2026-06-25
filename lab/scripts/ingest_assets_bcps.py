"""AtlasPay assets (with BCPs encoded as recovery fields) — Phase 0b Task 5.

business-continuity-plans endpoint does NOT exist in CISO Assistant v3.18.3 OSS.
Encode each of the 4 critical-function BCPs as an asset with:
- recovery_objective (RTO)
- recovery_point_objective (RPO)

This preserves the BCP data in the live system within the closest available model.
"""

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
import ca_api

# 4 critical-function BCPs from AtlasPay-Risk-Profile-BCP__Atlaspay_Business_Continuity_Plan.pdf
BCP_AS_ASSETS = [
    {
        "ref": "BCP-01",
        "name": "Payment Processing (Critical Function)",
        "description": (
            "Real-time payment authorization and settlement. Critical function "
            "for AtlasPay. RTO: 1 hour. RPO: 5 minutes. "
            "Recovery: multi-region active-active, automated failover, payment "
            "gateway retry queue, fraud-monitoring system independent failover."
        ),
        "type": "BCP",
        "business_value": "critical",
        "is_business_function": True,
        "rto": "1 hour",
        "rpo": "5 minutes",
        "folder_name": "Operations",
    },
    {
        "ref": "BCP-02",
        "name": "Customer Account Access (Critical Function)",
        "description": (
            "Customer-facing login, balance, transaction history. Critical "
            "function. RTO: 4 hours. RPO: 15 minutes. "
            "Recovery: read-only fallback during write-replica rebuild, customer "
            "notification via status page, support queue for urgent issues."
        ),
        "type": "BCP",
        "business_value": "critical",
        "is_business_function": True,
        "rto": "4 hours",
        "rpo": "15 minutes",
        "folder_name": "Operations",
    },
    {
        "ref": "BCP-03",
        "name": "Fraud Monitoring (Critical Function)",
        "description": (
            "Real-time fraud detection and transaction blocking. Critical "
            "function. RTO: 30 minutes. RPO: 0 (no transaction loss; decision "
            "latency acceptable). Recovery: model serving in 2 AZs, fallback "
            "rule-based system, manual review for transactions during outage."
        ),
        "type": "BCP",
        "business_value": "critical",
        "is_business_function": True,
        "rto": "30 minutes",
        "rpo": "0",
        "folder_name": "Operations",
    },
    {
        "ref": "BCP-04",
        "name": "Financial Reporting (Critical Function)",
        "description": (
            "Daily/weekly financial reports, regulatory reporting. Critical "
            "function (regulatory). RTO: 24 hours. RPO: 4 hours. "
            "Recovery: overnight reconciliation jobs rerunnable, regulatory "
            "reports have submission windows with regulator."
        ),
        "type": "BCP",
        "business_value": "critical",
        "is_business_function": True,
        "rto": "24 hours",
        "rpo": "4 hours",
        "folder_name": "Finance",
    },
]


def main() -> int:
    print(f"=== Ingesting {len(BCP_AS_ASSETS)} assets (BCPs encoded with disaster_recovery_objectives JSON) ===")
    for bcp in BCP_AS_ASSETS:
        folder = ca_api.find_by("folders", name=bcp["folder_name"])
        if not folder:
            print(f"  [WARN] {bcp['ref']}: folder '{bcp['folder_name']}' not found, skipping")
            continue
        folder_id = folder["id"]

        existing = ca_api.find_by("assets", name=bcp["name"])
        if existing:
            print(f"  [skip] {bcp['ref']}: already exists (id={existing.get('id')})")
            continue

        # CISO Assistant Asset has `disaster_recovery_objectives` JSONField (verified via
        # backend Django model probe). BCP data encoded there. No native
        # recovery_objective / recovery_point_objective fields exist.
        # Asset.type enum is only "PR" (Primary) or "SP" (Support). BCPs are primary.
        payload = {
            "name": bcp["name"],
            "description": bcp["description"],
            "type": "PR",
            "business_value": bcp["business_value"],
            "is_business_function": bcp["is_business_function"],
            "ref_id": bcp["ref"],
            "folder": folder_id,
            "disaster_recovery_objectives": {
                "rto": bcp["rto"],
                "rpo": bcp["rpo"],
                "ref": bcp["ref"],
                "recovery_strategy": bcp["description"].split("Recovery: ")[-1] if "Recovery: " in bcp["description"] else "",
            },
        }
        try:
            status, body = ca_api.post("assets/", payload)
            if status not in (200, 201):
                print(f"  [FAIL] {bcp['ref']}: HTTP {status} -- {str(body)[:300]}")
                continue
            print(f"  [create] {bcp['ref']}: id={body.get('id')} (RTO={bcp['rto']}, RPO={bcp['rpo']})")
        except Exception as e:
            print(f"  [FAIL] {bcp['ref']}: {e}")
    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
