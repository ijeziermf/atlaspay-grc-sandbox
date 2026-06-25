"""AtlasPay risk-scenarios ingestion — Phase 0b Task 1.

Ingest 6 risks R-01..R-06 from the AtlasPay SOC 2 Readiness PDF.
Uses ca_api.py REST client. Each risk needs:
- name (R-XX)
- description
- inherent_score (1-25)
- residual_score (1-25)
- treatment (mitigate, accept, transfer, avoid)
- folder_id (AtlasPay/Compliance)
- risk_matrix_id (the 5x5 matrix from Phase 0a)
- linked controls (NIST CSF, ISO 27001)

Source: ~/Documents/IfeSec/Projects/atlaspay-grc-sandbox/source-data/extracted/AtlasPay-Risk-Assessment__AtlasPay_SOC_2_Readiness.txt
"""

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
import ca_api  # module-level functions, not a class

# AtlasPay risks from the SOC 2 Readiness PDF
RISKS = [
    {
        "ref": "R-01",
        "name": "Privileged Account Compromise",
        "description": (
            "Adversary obtains credentials of a privileged user (DBA, DevOps, "
            "Cloud admin) through phishing, credential reuse, or insider threat. "
            "Impact: full database exfiltration, fraud transaction injection, "
            "audit log tampering. Likelihood: high (prevalence of phishing + "
            "credential reuse in payments industry)."
        ),
        "inherent_score": 20,  # CRITICAL (Likelihood 4 × Impact 5)
        "residual_score": 8,   # MEDIUM after PAM + MFA + JIT access
        "treatment": "mitigate",
        "category": "Access Control",
        "nist_csf": "PR.AC-1, PR.AC-4, PR.AC-7",
        "iso27001": "A.5.16, A.8.2, A.8.5",
    },
    {
        "ref": "R-02",
        "name": "Payment Data Exfiltration via API",
        "description": (
            "Attacker exploits IDOR or broken authentication in payment APIs "
            "to extract cardholder data or PII at scale. Impact: PCI-DSS breach, "
            "card brand fines, customer churn. Likelihood: medium (requires "
            "specific bug discovery)."
        ),
        "inherent_score": 16,  # HIGH (Likelihood 4 × Impact 4)
        "residual_score": 6,   # LOW after WAF + rate limiting + authn tightening
        "treatment": "mitigate",
        "category": "Data Security",
        "nist_csf": "PR.DS-2, PR.DS-5, DE.CM-1",
        "iso27001": "A.8.26, A.8.28, A.5.31",
    },
    {
        "ref": "R-03",
        "name": "Ransomware on Production Database Host",
        "description": (
            "Ransomware encrypts primary PostgreSQL host; payments halt for "
            "duration of recovery. Impact: complete business stoppage, RTO "
            "breach. Likelihood: medium (depends on phishing + unpatched "
            "vulnerability)."
        ),
        "inherent_score": 15,  # HIGH (Likelihood 3 × Impact 5)
        "residual_score": 9,   # MEDIUM after immutable backups + EDR + network segmentation
        "treatment": "mitigate",
        "category": "Resilience",
        "nist_csf": "PR.IP-4, PR.IP-9, RC.RP-1",
        "iso27001": "A.8.13, A.5.30, A.8.7",
    },
    {
        "ref": "R-04",
        "name": "Third-Party SaaS Breach (Vendor Compromise)",
        "description": (
            "Critical SaaS vendor (KYC provider, fraud scoring, identity "
            "provider) is compromised; downstream impact on AtlasPay payment "
            "flows and customer trust. Impact: service disruption + reputational. "
            "Likelihood: high (industry-wide breach frequency)."
        ),
        "inherent_score": 12,  # HIGH (Likelihood 4 × Impact 3)
        "residual_score": 6,   # LOW after TPRM + contractual SLAs + redundancy
        "treatment": "mitigate",
        "category": "Third-Party Risk",
        "nist_csf": "GV.SC-3, GV.SC-4, ID.SC-3",
        "iso27001": "A.5.19, A.5.21, A.5.23",
    },
    {
        "ref": "R-05",
        "name": "Insider Threat (Malicious Employee)",
        "description": (
            "Disgruntled employee with legitimate access exfiltrates customer "
            "data or commits fraud. Impact: data loss + financial + reputational. "
            "Likelihood: medium (industry baseline)."
        ),
        "inherent_score": 12,  # HIGH (Likelihood 3 × Impact 4)
        "residual_score": 6,   # LOW after DLP + UEBA + least privilege + exit process
        "treatment": "mitigate",
        "category": "Access Control",
        "nist_csf": "PR.AC-4, PR.DS-1, DE.CM-3",
        "iso27001": "A.5.18, A.8.16, A.8.15",
    },
    {
        "ref": "R-06",
        "name": "Insufficient Audit Logging",
        "description": (
            "Critical actions (admin changes, transaction reversals, permission "
            "grants) are not logged or logs are not retained. Impact: SOC 2 "
            "finding, inability to investigate fraud. Likelihood: medium (common "
            "in fast-growing orgs)."
        ),
        "inherent_score": 10,  # MEDIUM (Likelihood 5 × Impact 2)
        "residual_score": 4,   # LOW after centralized logging + 1yr retention + alerting
        "treatment": "mitigate",
        "category": "Logging & Monitoring",
        "nist_csf": "PR.PT-1, DE.AE-2, DE.CM-1",
        "iso27001": "A.8.15, A.8.16, A.5.28",
    },
]


def find_or_create_risk_scenario(risk: dict, matrix_id: str, folder_id: str) -> dict:
    """Create a risk-scenario via POST /api/risk-scenarios/, idempotent by ref+name."""
    existing = ca_api.find_by("risk-scenarios", name=risk["name"])
    if existing:
        print(f"  [skip] {risk['ref']}: already exists (id={existing.get('id')})")
        return existing

    payload = {
        "name": f"{risk['ref']}: {risk['name']}",
        "description": risk["description"],
        "inherent_level": risk["inherent_score"],
        "residual_level": risk["residual_score"],
        "treatment": risk["treatment"],
        "ref_id": risk["ref"],
        "folder": folder_id,
        "risk_matrix": matrix_id,
        "category": risk["category"],
    }
    status, body = ca_api.post("risk-scenarios/", payload)
    if status not in (200, 201):
        print(f"  [FAIL] {risk['ref']}: HTTP {status} -- {str(body)[:300]}")
        return {"error": body, "status": status}
    print(f"  [create] {risk['ref']}: id={body.get('id')} (inherent={risk['inherent_score']} -> residual={risk['residual_score']})")
    return body


def main() -> int:
    matrices = ca_api.count("risk-matrices")
    if matrices < 1:
        print(f"FAIL: risk-matrices count = {matrices}, expected >= 1. Run Phase 0a first.")
        return 1
    matrix_obj = ca_api.find_by("risk-matrices", name="AtlasPay 5x5")
    if not matrix_obj:
        print("FAIL: AtlasPay 5x5 matrix not found. Run Phase 0a first.")
        return 1
    matrix_id = matrix_obj["id"]

    compliance = ca_api.find_by("folders", name="Compliance")
    if not compliance:
        print("FAIL: Compliance folder not found. Run Phase 0a first.")
        return 1
    folder_id = compliance["id"]

    # Risk-scenarios require a parent risk_assessment container.
    # Hermes created this via Django ORM (REST write path has the
    # get_name_translated setter bug). See PHASE_0_LESSONS_LEARNED.md.
    ra = ca_api.find_by("risk-assessments", name="AtlasPay SOC 2 Readiness Risk Assessment")
    if not ra:
        print("FAIL: parent RiskAssessment not found. Create via Django ORM first.")
        return 1
    ra_id = ra["id"]

    print(f"=== Ingesting {len(RISKS)} risk-scenarios ===")
    print(f"  matrix_id: {matrix_id}")
    print(f"  folder_id (Compliance): {folder_id}")
    print(f"  parent risk_assessment: {ra_id}")
    for risk in RISKS:
        existing = ca_api.find_by("risk-scenarios", name=risk["name"])
        if existing:
            print(f"  [skip] {risk['ref']}: already exists (id={existing.get('id')})")
            continue
        payload = {
            "name": f"{risk['ref']}: {risk['name']}",
            "description": risk["description"],
            "inherent_level": risk["inherent_score"],
            "residual_level": risk["residual_score"],
            "treatment": risk["treatment"],
            "ref_id": risk["ref"],
            "folder": folder_id,
            "risk_matrix": matrix_id,
            "risk_assessment": ra_id,
            "category": risk["category"],
        }
        status, body = ca_api.post("risk-scenarios/", payload)
        if status not in (200, 201):
            print(f"  [FAIL] {risk['ref']}: HTTP {status} -- {str(body)[:300]}")
            continue
        print(f"  [create] {risk['ref']}: id={body.get('id')} (inherent={risk['inherent_score']} -> residual={risk['residual_score']})")
    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
