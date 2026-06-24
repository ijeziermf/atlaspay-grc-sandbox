"""AtlasPay entities (vendors) ingestion — Phase 0b Task 3.

Ingest 7 vendors as composite entities. CA v3.18.3 vendors = entities + contracts + solutions.
"""

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
import ca_api

ENTITIES = [
    {
        "ref": "V-01",
        "name": "Cloud Provider (Sandbox)",
        "description": "Primary cloud infrastructure (AWS production environment, multi-region).",
        "inherent_risk_tier": "high",
        "category": "Infrastructure",
        "contracts_count": 1,
    },
    {
        "ref": "V-02",
        "name": "Payment Gateway (Sandbox)",
        "description": "Card processing and network tokenization gateway. PCI-DSS scope.",
        "inherent_risk_tier": "high",
        "category": "Payments",
        "contracts_count": 1,
    },
    {
        "ref": "V-03",
        "name": "Identity Provider (Sandbox)",
        "description": "Customer authentication (SSO, MFA, passwordless). Critical auth path.",
        "inherent_risk_tier": "high",
        "category": "Identity",
        "contracts_count": 1,
    },
    {
        "ref": "V-04",
        "name": "Application Platform (Sandbox)",
        "description": "Application runtime platform (Kubernetes, service mesh, CI/CD).",
        "inherent_risk_tier": "medium",
        "category": "Platform",
        "contracts_count": 1,
    },
    {
        "ref": "V-05",
        "name": "Monitoring Tools (Sandbox)",
        "description": "Observability stack (metrics, logs, traces, alerting).",
        "inherent_risk_tier": "medium",
        "category": "Observability",
        "contracts_count": 1,
    },
    {
        "ref": "V-06",
        "name": "Finance Systems (Sandbox)",
        "description": "General ledger, accounts payable/receivable, financial reporting.",
        "inherent_risk_tier": "medium",
        "category": "Finance",
        "contracts_count": 1,
    },
    {
        "ref": "V-07",
        "name": "Data Warehouse (Sandbox)",
        "description": "Analytics data warehouse with PII for BI and ML workloads.",
        "inherent_risk_tier": "low",
        "category": "Analytics",
        "contracts_count": 1,
    },
]


def main() -> int:
    compliance = ca_api.find_by("folders", name="Compliance")
    if not compliance:
        print("FAIL: Compliance folder not found.")
        return 1
    folder_id = compliance["id"]

    print(f"=== Ingesting {len(ENTITIES)} entities (vendors) ===")
    print(f"  folder_id (Compliance): {folder_id}")
    for ent in ENTITIES:
        existing = ca_api.find_by("entities", name=ent["name"])
        if existing:
            print(f"  [skip] {ent['ref']}: already exists (id={existing.get('id')})")
            continue
        payload = {
            "name": ent["name"],
            "description": ent["description"],
            "ref_id": ent["ref"],
            "folder": folder_id,
            "category": ent["category"],
        }
        status, body = ca_api.post("entities/", payload)
        if status not in (200, 201):
            print(f"  [FAIL] {ent['ref']} entity: HTTP {status} -- {str(body)[:300]}")
            continue
        ent_id = body.get("id")
        print(f"  [create] {ent['ref']} entity: id={ent_id}")

        existing_contract = ca_api.find_by("contracts", name=f"{ent['name']} - MSA")
        if not existing_contract:
            contract_payload = {
                "name": f"{ent['name']} - MSA",
                "description": f"Master Services Agreement for {ent['name']}. Inherent risk tier: {ent['inherent_risk_tier']}.",
                "ref_id": f"{ent['ref']}-MSA",
                "folder": folder_id,
                "entity": ent_id,
                "category": "MSA",
            }
            c_status, c_body = ca_api.post("contracts/", contract_payload)
            if c_status in (200, 201):
                print(f"    [create] {ent['ref']} contract: MSA (id={c_body.get('id')})")
            else:
                print(f"    [FAIL] {ent['ref']} contract: HTTP {c_status} -- {str(c_body)[:200]}")
    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
