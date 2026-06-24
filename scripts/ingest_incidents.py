"""AtlasPay incident ingestion — Phase 0b Task 4.

Ingest 1 sample incident (phishing scenario linked to R-01).
"""

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
import ca_api


def main() -> int:
    compliance = ca_api.find_by("folders", name="Compliance")
    if not compliance:
        print("FAIL: Compliance folder not found.")
        return 1
    folder_id = compliance["id"]

    incident_name = "Phishing — Credential Capture (R-01 trigger)"

    existing = ca_api.find_by("incidents", name=incident_name)
    if existing:
        print(f"[skip] Phishing incident already exists (id={existing.get('id')})")
        return 0

    r01 = ca_api.find_by("risk-scenarios", name="R-01: Privileged Account Compromise")
    r01_id = r01.get("id") if r01 else None

    # CISO Assistant Incident enums (verified from Django model):
    #   status:   new | ongoing | resolved | closed | dismissed
    #   severity: 1=Critical, 2=Major, 3=Moderate, 4=Minor, 5=Low, 6=unknown
    #   type:     free text (kept "phishing")
    payload = {
        "name": incident_name,
        "description": (
            "Targeted phishing email sent to a privileged user (Database Admin). "
            "User clicked link, entered credentials on attacker-controlled lookalike "
            "domain. Credentials were immediately used to attempt a database "
            "dump. Detected by UEBA anomaly (impossible travel + bulk query "
            "volume). Contained within 18 minutes via session revocation + IP "
            "block. No PII exfiltrated (query was intercepted mid-execution). "
            "Linked to R-01 (Privileged Account Compromise) as the realized "
            "scenario."
        ),
        "type": "phishing",
        "severity": 3,           # Moderate
        "status": "resolved",     # was 'contained' — not a valid choice
        "open_date": "2026-06-22",
        "folder": folder_id,
        "ref_id": "INC-001",
        "linked_risk_scenarios": [r01_id] if r01_id else [],
    }
    status, body = ca_api.post("incidents/", payload)
    if status not in (200, 201):
        print(f"[FAIL] INC-001: HTTP {status} -- {str(body)[:300]}")
        return 1
    print(f"[create] INC-001: id={body.get('id')} (linked to R-01)")
    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
