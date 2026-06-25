"""AtlasPay policies ingestion — Phase 0b Task 2.

Ingest 4 policies ACC-01, IR-01, SA-01, TPRM-01 from the Cyber-Security-Policy-Library.
"""

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
import ca_api

POLICIES = [
    {
        "ref": "ACC-01",
        "name": "Access Control & Privileged Access Policy",
        "description": (
            "Governs identification, authentication, authorization, and "
            "privileged access across AtlasPay production systems. Covers "
            "least-privilege, MFA, JIT access for admins, quarterly access "
            "reviews, and break-glass procedures."
        ),
        "category": "policy",
        "csf_function": "protect",
        "status": "active",
        "priority": 2,
        "next_review": "2027-06-22",
        "iso27001": "A.5.16, A.5.17, A.5.18, A.8.2, A.8.3, A.8.5",
    },
    {
        "ref": "IR-01",
        "name": "Incident Response Policy",
        "description": (
            "Defines detection, triage, containment, eradication, and recovery "
            "procedures for security incidents. Includes severity classification, "
            "escalation paths, customer notification triggers (state breach "
            "notification laws), and post-incident review requirements."
        ),
        "category": "policy",
        "csf_function": "respond",
        "status": "active",
        "priority": 1,
        "next_review": "2027-06-22",
        "iso27001": "A.5.24, A.5.25, A.5.26, A.5.27, A.5.28",
    },
    {
        "ref": "SA-01",
        "name": "Security Awareness & Acceptable Use Policy",
        "description": (
            "Annual security awareness training, phishing simulations, "
            "acceptable use of corporate assets, BYOD rules, and incident "
            "reporting obligations for all employees and contractors."
        ),
        "category": "policy",
        "csf_function": "protect",
        "status": "active",
        "priority": 2,
        "next_review": "2027-06-22",
        "iso27001": "A.5.10, A.5.11, A.6.3, A.6.8",
    },
    {
        "ref": "TPRM-01",
        "name": "Third-Party Risk Management Policy",
        "description": (
            "Vendor onboarding risk tiering, inherent/ residual risk assessment, "
            "annual reassessment cadence, contractual security requirements, "
            "ongoing monitoring (security ratings, breach disclosure), and "
            "offboarding data return/destruction requirements."
        ),
        "category": "policy",
        "csf_function": "govern",
        "status": "active",
        "priority": 2,
        "next_review": "2027-06-22",
        "iso27001": "A.5.19, A.5.20, A.5.21, A.5.22, A.5.23",
    },
]


def main() -> int:
    compliance = ca_api.find_by("folders", name="Compliance")
    if not compliance:
        print("FAIL: Compliance folder not found.")
        return 1
    folder_id = compliance["id"]

    print(f"=== Ingesting {len(POLICIES)} policies ===")
    print(f"  folder_id (Compliance): {folder_id}")
    for pol in POLICIES:
        existing = ca_api.find_by("policies", name=pol["name"])
        if existing:
            print(f"  [skip] {pol['ref']}: already exists (id={existing.get('id')})")
            continue
        # Enum values verified from Django model:
        #   category: policy | process | technical | physical | procedure
        #   status:   to_do | in_progress | on_hold | active | degraded | deprecated | --
        #   priority: 1-4 (P1 highest)
        #   csf_function: govern | identify | protect | detect | respond | recover
        payload = {
            "name": pol["name"],
            "description": pol["description"],
            "status": pol["status"],
            "priority": pol["priority"],
            "csf_function": pol["csf_function"],
            "next_review_date": pol["next_review"],
            "ref_id": pol["ref"],
            "folder": folder_id,
            "category": pol["category"],
        }
        status, body = ca_api.post("policies/", payload)
        if status not in (200, 201):
            print(f"  [FAIL] {pol['ref']}: HTTP {status} -- {str(body)[:300]}")
            continue
        print(f"  [create] {pol['ref']}: id={body.get('id')}")
    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
