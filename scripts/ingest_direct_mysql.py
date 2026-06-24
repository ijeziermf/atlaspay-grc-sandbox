"""
AtlasPay Sandbox — DIRECT MySQL ingestion.

Bypasses the Eramba UI entirely. Inserts records straight into the MySQL
database. The Eramba app reads from the same MySQL, so the records will
appear in the UI immediately.

This is the path that works.
"""
import json
import subprocess
import time
from datetime import datetime, date, timedelta
from pathlib import Path

ROOT = Path.home() / "Documents" / "IfeSec" / "Projects" / "atlaspay-grc-sandbox"
DOCS = ROOT / "docs"
SHOTS = ROOT / "screenshots"
DOCS.mkdir(parents=True, exist_ok=True)

PWD = "Your_DB_user_P@ssw0rd"
MYSQL_CMD = ["docker", "compose", "exec", "-T", "mysql", "mysql",
             "-udocker", f"-p{PWD}", "docker", "-N", "-B"]

def mysql_exec(sql, fetch=False):
    """Execute a SQL statement (or statements) via docker exec."""
    r = subprocess.run(
        MYSQL_CMD + ["-e", sql],
        capture_output=True, text=True, cwd="/Users/ifeanyi/eramba"
    )
    if r.returncode != 0:
        print(f"  SQL ERR: {r.stderr[:200]}")
        return None
    return r.stdout.strip() if fetch else r.returncode

def esc(s):
    """Escape a string for SQL."""
    if s is None:
        return "NULL"
    return "'" + str(s).replace("'", "''") + "'"

# ============================================================
# AtlasPay data (REAL values from extracted PDFs)
# ============================================================
ATLASPAY_RISKS = [
    {"id": "R-01", "title": "Phishing Attacks", "residual": 20,
     "desc": "Phishing identified as high-priority risk due to likelihood and impact on financial systems and sensitive data. Source: AtlasPay-Risk-Assessment R-01. Treatment: MFA + phishing simulations."},
    {"id": "R-02", "title": "Access Control Weakness", "residual": 12,
     "desc": "Inconsistent least privilege enforcement and limited access approval documentation. Source: AtlasPay-Risk-Assessment R-02. Treatment: RBAC + access reviews."},
    {"id": "R-03", "title": "Logging and Monitoring Gaps", "residual": 9,
     "desc": "Insufficient centralized logging impacting incident detection and response. Source: AtlasPay-Risk-Assessment R-03. Treatment: Centralized logging + SIEM."},
    {"id": "R-04", "title": "Incident Response Planning and Testing", "residual": 12,
     "desc": "Gaps in IR documentation, approval, and testing of response procedures. Source: AtlasPay-Risk-Assessment R-04. Treatment: IR plan + tabletop exercises."},
    {"id": "R-05", "title": "Third-Party and Vendor Risk Management", "residual": 12,
     "desc": "Lack of formal TPRM and ongoing monitoring program. Source: AtlasPay-Risk-Assessment R-05. Treatment: TPRM program + periodic reviews."},
    {"id": "R-06", "title": "Security Awareness and Training", "residual": 10,
     "desc": "Generalized training with limited effectiveness measurement. Source: AtlasPay-Risk-Assessment R-06. Treatment: Role-based training + phishing sim."},
]

ATLASPAY_POLICIES = [
    {"index": "ACC-01", "title": "Access Control & Privileged Access Policy",
     "desc": "Defines requirements for access control, least privilege, and privileged access management. Source: Cyber-Security-Policy-Library."},
    {"index": "IR-01", "title": "Incident Response Policy",
     "desc": "Defines incident classification, response procedures, and reporting requirements. Source: Cyber-Security-Policy-Library."},
    {"index": "SA-01", "title": "Security Awareness & Acceptable Use Policy",
     "desc": "Defines security awareness training requirements and acceptable use of company systems. Source: Cyber-Security-Policy-Library."},
    {"index": "TPRM-01", "title": "Third-Party Risk Management Policy",
     "desc": "Defines vendor onboarding, risk assessment, and ongoing monitoring requirements. Source: Cyber-Security-Policy-Library."},
]

ATLASPAY_CONTINUITY = [
    {"title": "Payment Processing BCP", "rto": "4 hours", "rpo": "Near-real-time", "mtpd": "24 hours",
     "objective": "Restore payment processing capability within 4 hours of disruption."},
    {"title": "Customer Account Access BCP", "rto": "8 hours", "rpo": "24 hours", "mtpd": "48 hours",
     "objective": "Restore customer account access within 8 hours of disruption."},
    {"title": "Fraud Monitoring BCP", "rto": "4 hours", "rpo": "Near-real-time", "mtpd": "24 hours",
     "objective": "Restore fraud monitoring within 4 hours of disruption."},
    {"title": "Financial Reporting BCP", "rto": "24 hours", "rpo": "24 hours", "mtpd": "72 hours",
     "objective": "Restore financial reporting capability within 24 hours of disruption."},
]

ATLASPAY_VENDORS = [
    {"name": "Cloud Provider (Sandbox)", "desc": "Primary cloud infrastructure provider for the AtlasPay sandbox."},
    {"name": "Payment Gateway (Sandbox)", "desc": "Payment processing gateway integration."},
    {"name": "Identity Provider (Sandbox)", "desc": "SSO and identity federation for the AtlasPay application."},
    {"name": "Application Platform (Sandbox)", "desc": "Application runtime platform (PaaS)."},
    {"name": "Monitoring Tools (Sandbox)", "desc": "Infrastructure and application monitoring SaaS."},
    {"name": "Finance Systems (Sandbox)", "desc": "Finance and accounting system of record."},
    {"name": "Data Warehouse (Sandbox)", "desc": "Analytics data warehouse for reporting."},
]

ATLASPAY_INCIDENT = {"title": "Sample Phishing Incident - Finance Department",
                     "desc": "Phishing email reported by Finance team member. Investigating scope and impact."}

NOW = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
NEXT_REVIEW = (date.today() + timedelta(days=90)).isoformat()
PUBLISHED = (date.today() - timedelta(days=30)).isoformat()
OPEN_DATE = date.today().isoformat()

results = {
    "classification_types_added": 0,
    "classifications_updated": 0,
    "risks": [],
    "policies": [],
    "continuity": [],
    "vendors": [],
    "incidents": [],
    "errors": [],
}

print("=" * 70)
print("AtlasPay Sandbox — Direct MySQL Ingestion")
print("=" * 70)

# ============================================================
# STEP 1: CLASSIFICATION TYPES (Impact + Likelihood)
# ============================================================
print("\n[1] Classification Types")
# Check if already exist
existing = mysql_exec("SELECT name FROM risk_classification_types;", fetch=True) or ""
if "Impact" not in existing:
    sql = f"INSERT INTO risk_classification_types (name, created, modified) VALUES ('Impact', '{NOW}', '{NOW}');"
    rc = mysql_exec(sql)
    print(f"  Impact: rc={rc}")
    results["classification_types_added"] += 1
if "Likelihood" not in existing:
    sql = f"INSERT INTO risk_classification_types (name, created, modified) VALUES ('Likelihood', '{NOW}', '{NOW}');"
    rc = mysql_exec(sql)
    print(f"  Likelihood: rc={rc}")
    results["classification_types_added"] += 1

# Get the Impact classification type ID
type_id_str = mysql_exec("SELECT id FROM risk_classification_types WHERE name='Impact' LIMIT 1;", fetch=True)
impact_type_id = int(type_id_str) if type_id_str else None
print(f"  Impact type_id = {impact_type_id}")

# ============================================================
# STEP 2: UPDATE EXISTING CLASSIFICATIONS WITH TYPE FK
# ============================================================
print("\n[2] Classifications (update type FK)")
classifications = [
    ("Critical", 20),
    ("High", 12),
    ("Medium", 8),
    ("Low", 4),
    ("Very Low", 2),
]
for name, value in classifications:
    if impact_type_id:
        sql = f"UPDATE risk_classifications SET risk_classification_type_id = {impact_type_id} WHERE name = {esc(name)};"
        rc = mysql_exec(sql)
        print(f"  {name}: rc={rc}")
        results["classifications_updated"] += 1

# ============================================================
# STEP 3: RISKS
# ============================================================
print("\n[3] Risks")
for risk in ATLASPAY_RISKS:
    title_with_id = f"[{risk['id']}] {risk['title']}"
    # Check if already exists
    existing_risks = mysql_exec(f"SELECT id FROM risks WHERE title={esc(title_with_id)};", fetch=True) or ""
    if existing_risks:
        print(f"  {risk['id']}: already exists (id={existing_risks})")
        results["risks"].append(risk['id'])
        continue
    sql = f"""INSERT INTO risks
        (title, threats, vulnerabilities, description, residual_score,
         risk_score, risk_score_formula, residual_risk, residual_risk_formula,
         review, expired, exceptions_issues, controls_issues, control_in_design,
         expired_reviews, risk_above_appetite, workflow_status, created, modified, deleted)
        VALUES (
            {esc(title_with_id)},
            'Phishing campaigns, credential stuffing, social engineering',
            'Lack of MFA, untrained staff, email gateway gaps',
            {esc(risk['desc'])},
            {risk['residual']},
            {risk['residual']},
            'residual_score * 1',
            {float(risk['residual'])},
            'residual * 1',
            '{NEXT_REVIEW}', 0, 0, 0, 0, 0, 0, 0, '{NOW}', '{NOW}', 0
        );"""
    rc = mysql_exec(sql)
    if rc == 0:
        results["risks"].append(risk['id'])
        print(f"  {risk['id']}: added")
    else:
        results["errors"].append(f"risk {risk['id']}")

# ============================================================
# STEP 4: POLICIES
# ============================================================
print("\n[4] Policies")
for pol in ATLASPAY_POLICIES:
    existing = mysql_exec(f"SELECT id FROM security_policies WHERE `index`={esc(pol['index'])};", fetch=True) or ""
    if existing:
        print(f"  {pol['index']}: already exists (id={existing})")
        results["policies"].append(pol['index'])
        continue
    sql = f"""INSERT INTO security_policies
        (`index`, short_description, description, use_attachments, document_type,
         version, published_date, next_review_date, permission, ldap_groups_required,
         status, expired_reviews, workflow_status, created, modified, deleted)
        VALUES (
            {esc(pol['index'])},
            {esc(pol['title'])},
            {esc(pol['desc'])},
            0, 'policy', '1.0',
            '{PUBLISHED}', '{NEXT_REVIEW}', 'private', 0,
            1, 0, 0, '{NOW}', '{NOW}', 0
        );"""
    rc = mysql_exec(sql)
    if rc == 0:
        results["policies"].append(pol['index'])
        print(f"  {pol['index']}: added")
    else:
        results["errors"].append(f"policy {pol['index']}")

# ============================================================
# STEP 5: CONTINUITY PLANS
# ============================================================
print("\n[5] Continuity Plans")
for cp in ATLASPAY_CONTINUITY:
    existing = mysql_exec(f"SELECT id FROM business_continuity_plans WHERE title={esc(cp['title'])};", fetch=True) or ""
    if existing:
        print(f"  {cp['title']}: already exists (id={existing})")
        results["continuity"].append(cp['title'])
        continue
    sql = f"""INSERT INTO business_continuity_plans
        (title, objective, audit_metric, audit_success_criteria, launch_criteria,
         opex, capex, resource_utilization, regular_review, audit_calendar_type,
         audits_all_done, audits_last_missing, audits_last_passed, audits_improvements,
         ongoing_corrective_actions, workflow_status, created, modified, deleted)
        VALUES (
            {esc(cp['title'])},
            {esc(cp['objective'])},
            'RTO: {cp['rto']}, RPO: {cp['rpo']}, MTPD: {cp['mtpd']}',
            'Restore within RTO',
            'Plan approved and tested',
            0, 0, 0,
            '{NEXT_REVIEW}', 0,
            0, 0, 0, 0, 0, 0,
            '{NOW}', '{NOW}', 0
        );"""
    rc = mysql_exec(sql)
    if rc == 0:
        results["continuity"].append(cp['title'])
        print(f"  {cp['title']}: added")
    else:
        results["errors"].append(f"BCP {cp['title']}")

# ============================================================
# STEP 6: VENDORS
# ============================================================
print("\n[6] Vendors")
for ven in ATLASPAY_VENDORS:
    existing = mysql_exec(f"SELECT id FROM third_parties WHERE name={esc(ven['name'])};", fetch=True) or ""
    if existing:
        print(f"  {ven['name']}: already exists (id={existing})")
        results["vendors"].append(ven['name'])
        continue
    sql = f"""INSERT INTO third_parties
        (name, description, security_incident_count, security_incident_open_count,
         service_contract_count, workflow_status, _hidden, created, modified, deleted)
        VALUES (
            {esc(ven['name'])},
            {esc(ven['desc'])},
            0, 0, 0, 0, 0,
            '{NOW}', '{NOW}', 0
        );"""
    rc = mysql_exec(sql)
    if rc == 0:
        results["vendors"].append(ven['name'])
        print(f"  {ven['name']}: added")
    else:
        results["errors"].append(f"vendor {ven['name']}")

# ============================================================
# STEP 7: INCIDENT
# ============================================================
print("\n[7] Incident")
existing = mysql_exec(f"SELECT id FROM security_incidents WHERE title={esc(ATLASPAY_INCIDENT['title'])};", fetch=True) or ""
if existing:
    print(f"  Incident: already exists (id={existing})")
    results["incidents"].append(ATLASPAY_INCIDENT['title'])
else:
    sql = f"""INSERT INTO security_incidents
        (title, description, reporter, victim, open_date, expired, type,
         auto_close_incident, lifecycle_incomplete, ongoing_incident,
         workflow_status, created, modified, deleted)
        VALUES (
            {esc(ATLASPAY_INCIDENT['title'])},
            {esc(ATLASPAY_INCIDENT['desc'])},
            'Finance Team Lead',
            'Finance Department',
            '{OPEN_DATE}', 0, 'phishing',
            0, 1, 0, 0,
            '{NOW}', '{NOW}', 0
        );"""
    rc = mysql_exec(sql)
    if rc == 0:
        results["incidents"].append(ATLASPAY_INCIDENT['title'])
        print(f"  Incident: added")
    else:
        results["errors"].append("incident")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 70)
print("INGESTION SUMMARY (Direct MySQL)")
print("=" * 70)
print(f"  Classification Types: {results['classification_types_added']} / 2")
print(f"  Classifications Updated: {results['classifications_updated']} / 5")
print(f"  Risks:        {len(results['risks'])} / 6")
print(f"  Policies:     {len(results['policies'])} / 4")
print(f"  Continuity:   {len(results['continuity'])} / 4")
print(f"  Vendors:      {len(results['vendors'])} / 7")
print(f"  Incidents:    {len(results['incidents'])} / 1")
if results["errors"]:
    print(f"\n  Errors ({len(results['errors'])}):")
    for err in results["errors"]:
        print(f"    - {err}")

# Verify by counting what's actually in the DB
print("\n=== Verification (record counts in DB) ===")
for table in ['risks', 'security_policies', 'business_continuity_plans', 'third_parties', 'security_incidents', 'risk_classifications', 'risk_classification_types']:
    count = mysql_exec(f"SELECT COUNT(*) FROM {table} WHERE deleted = 0;", fetch=True)
    print(f"  {table}: {count}")

with (DOCS / "18-direct-mysql-results.json").open("w") as f:
    json.dump(results, f, indent=2)
print(f"\nResults saved to docs/18-direct-mysql-results.json")
