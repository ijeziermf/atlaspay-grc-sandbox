"""
AtlasPay Sandbox — full data ingestion driver.

Drives Eramba CE to ingest real AtlasPay data from the existing GitHub repos:

  1. Configure Risk Settings (Classifications, Risk Calculations, Risk Appetite)
  2. Create AtlasPay Sandbox organisation
  3. Activate SOC 2 (TSC 2017) framework
  4. Ingest 6 risks from AtlasPay-Risk-Assessment (R-01..R-06)
  5. Ingest 4 policies from Cyber-Security-Policy-Library
  6. Ingest 4 critical functions from AtlasPay BCP as continuity plans
  7. Create anonymized vendor records
  8. Create one sample incident (phishing scenario)

Each step screenshots + logs to docs/. Real AtlasPay data is in source-data/.
"""
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path.home() / "Documents" / "IfeSec" / "Projects" / "atlaspay-grc-sandbox"
SHOTS = ROOT / "screenshots"
DOCS = ROOT / "docs"
SRC = ROOT / "source-data" / "extracted"
SHOTS.mkdir(parents=True, exist_ok=True)
DOCS.mkdir(parents=True, exist_ok=True)

ERAMBA_URL = "https://localhost:8443"
USER = "admin"
PASS = "8950Fourth"

LOG = DOCS / "03-data-ingestion.md"
LOG.write_text("")

def log(msg=""):
    ts = time.strftime("%H:%M:%S")
    line = f"[{ts}] {msg}\n" if msg else "\n"
    with LOG.open("a") as f:
        f.write(line)
    print(line.rstrip())

def shot(page, name, full=True):
    path = SHOTS / f"{name}.png"
    page.screenshot(path=str(path), full_page=full)
    kb = path.stat().st_size // 1024
    log(f"  -> {path.name} ({kb} KB)")

# ===== AtlasPay data (extracted from source-data/) =====
ATLASPAY_RISKS = [
    {
        "id": "R-01",
        "title": "Phishing Attacks",
        "inherent_impact": 5, "inherent_likelihood": 4,  # 20 - highest
        "residual_impact": 3, "residual_likelihood": 2,   # 6 - post-MFA
        "treatment": "Mitigate",
        "owner_role": "IT Security Manager",
        "description": (
            "Phishing was identified as a high-priority risk due to its likelihood and "
            "potential impact on financial systems and sensitive data. AtlasPay implemented "
            "multi-factor authentication for all finance and privileged user accounts and "
            "deployed phishing simulation exercises to improve employee awareness and response. "
            "Source: AtlasPay-Risk-Assessment (R-01)"
        ),
        "treatment_plan": (
            "Maintain MFA on all finance and privileged accounts. Continue quarterly phishing "
            "simulations. Track click rates and reporting rates. Review MFA enrollment monthly."
        ),
    },
    {
        "id": "R-02",
        "title": "Access Control Weakness",
        "inherent_impact": 4, "inherent_likelihood": 3,  # 12
        "residual_impact": 3, "residual_likelihood": 2,  # 6
        "treatment": "Mitigate",
        "owner_role": "Identity & Access Lead",
        "description": (
            "Access control deficiencies due to inconsistent enforcement of least privilege and "
            "limited documentation of access approvals. Source: AtlasPay-Risk-Assessment (R-02)"
        ),
        "treatment_plan": (
            "Formalize role-based access definitions. Implement documented approval workflow "
            "for privileged access grants. Conduct quarterly access reviews for high-risk roles."
        ),
    },
    {
        "id": "R-03",
        "title": "Logging and Monitoring Gaps",
        "inherent_impact": 3, "inherent_likelihood": 3,  # 9
        "residual_impact": 3, "residual_likelihood": 2,  # 6
        "treatment": "Mitigate",
        "owner_role": "Security Operations Lead",
        "description": (
            "Insufficient centralized logging and monitoring capabilities impact incident "
            "detection and response. Source: AtlasPay-Risk-Assessment (R-03)"
        ),
        "treatment_plan": (
            "Implement centralized log aggregation (SIEM). Define alerting thresholds for "
            "high-risk events (auth failures, privilege escalation, data egress)."
        ),
    },
    {
        "id": "R-04",
        "title": "Incident Response Planning and Testing",
        "inherent_impact": 4, "inherent_likelihood": 3,  # 12
        "residual_impact": 3, "residual_likelihood": 2,  # 6
        "treatment": "Mitigate",
        "owner_role": "Incident Response Coordinator",
        "description": (
            "Gaps in incident response readiness related to documentation, approval, and testing "
            "of response procedures. Source: AtlasPay-Risk-Assessment (R-04)"
        ),
        "treatment_plan": (
            "Finalize and formally approve the incident response plan. Define escalation paths. "
            "Conduct semi-annual tabletop exercises to validate response effectiveness."
        ),
    },
    {
        "id": "R-05",
        "title": "Third-Party and Vendor Risk Management",
        "inherent_impact": 4, "inherent_likelihood": 3,  # 12
        "residual_impact": 3, "residual_likelihood": 2,  # 6
        "treatment": "Mitigate",
        "owner_role": "Vendor Risk Manager",
        "description": (
            "Vendor risk due to lack of formal third-party risk assessment and monitoring. "
            "Source: AtlasPay-Risk-Assessment (R-05)"
        ),
        "treatment_plan": (
            "Implement structured TPRM program with security questionnaires and minimum-security "
            "requirements. Periodic reviews of high-risk vendors. Annual SOC 2 / equivalent "
            "evidence collection."
        ),
    },
    {
        "id": "R-06",
        "title": "Security Awareness and Training",
        "inherent_impact": 5, "inherent_likelihood": 2,  # 10
        "residual_impact": 3, "residual_likelihood": 2,  # 6
        "treatment": "Mitigate",
        "owner_role": "Security Awareness Lead",
        "description": (
            "Reliance on generalized training and limited effectiveness measurement. "
            "Source: AtlasPay-Risk-Assessment (R-06)"
        ),
        "treatment_plan": (
            "Implement role-based security awareness training. Conduct monthly phishing "
            "simulations. Track training completion and click rates by role."
        ),
    },
]

ATLASPAY_POLICIES = [
    {
        "title": "Access Control & Privileged Access Policy",
        "version": "1.0",
        "policy_type": "Access Control",
        "owner_role": "Identity & Access Lead",
        "linked_risks": ["R-02"],
        "summary": (
            "Defines least-privilege access, role-based access control (RBAC), privileged access "
            "management (PAM), and quarterly access review requirements. Maps to NIST 800-53 AC "
            "family and ISO 27001 A.5.15-A.5.18. Source: Cyber-Security-Policy-Library"
        ),
    },
    {
        "title": "Incident Response Policy",
        "version": "1.0",
        "policy_type": "Incident Response",
        "owner_role": "Incident Response Coordinator",
        "linked_risks": ["R-01", "R-04"],
        "summary": (
            "Defines incident classification, escalation paths, response procedures, and "
            "post-incident review. Covers phishing, malware, data breach, and third-party "
            "incidents. Maps to NIST 800-53 IR family. Source: Cyber-Security-Policy-Library"
        ),
    },
    {
        "title": "Security Awareness & Acceptable Use Policy",
        "version": "1.0",
        "policy_type": "Awareness",
        "owner_role": "Security Awareness Lead",
        "linked_risks": ["R-06"],
        "summary": (
            "Defines acceptable use of company systems, data handling requirements, and the "
            "annual security awareness training program. Maps to NIST 800-53 AT and PL families. "
            "Source: Cyber-Security-Policy-Library"
        ),
    },
    {
        "title": "Third-Party Risk Management Policy",
        "version": "1.0",
        "policy_type": "Vendor Risk",
        "owner_role": "Vendor Risk Manager",
        "linked_risks": ["R-05"],
        "summary": (
            "Defines vendor onboarding security assessment, ongoing monitoring, contract "
            "security requirements, and incident notification obligations. Maps to NIST 800-53 SR "
            "family. Source: Cyber-Security-Policy-Library"
        ),
    },
]

ATLASPAY_CONTINUITY = [
    {
        "function": "Payment Processing",
        "mtpd": "24 hours", "rto": "4 hours", "rpo": "Near-real-time",
        "dependencies": "Cloud provider, payment gateway",
        "owner_role": "Director of Payments",
        "priority": "Critical",
    },
    {
        "function": "Customer Account Access",
        "mtpd": "48 hours", "rto": "8 hours", "rpo": "24 hours",
        "dependencies": "Identity provider, application platform",
        "owner_role": "Director of Customer Experience",
        "priority": "High",
    },
    {
        "function": "Fraud Monitoring",
        "mtpd": "24 hours", "rto": "4 hours", "rpo": "Near-real-time",
        "dependencies": "Monitoring tools, transaction data",
        "owner_role": "Fraud Operations Manager",
        "priority": "Critical",
    },
    {
        "function": "Financial Reporting",
        "mtpd": "72 hours", "rto": "24 hours", "rpo": "24 hours",
        "dependencies": "Finance systems, data warehouse",
        "owner_role": "Controller",
        "priority": "Medium",
    },
]

ATLASPAY_VENDORS = [
    {"name": "Cloud Provider (Sandbox)", "service": "Infrastructure (IaaS)", "criticality": "Critical"},
    {"name": "Payment Gateway (Sandbox)", "service": "Payment processing", "criticality": "Critical"},
    {"name": "Identity Provider (Sandbox)", "service": "Identity / SSO", "criticality": "High"},
    {"name": "Application Platform (Sandbox)", "service": "Application hosting", "criticality": "High"},
    {"name": "Monitoring Tools (Sandbox)", "service": "SIEM / monitoring", "criticality": "High"},
    {"name": "Finance Systems (Sandbox)", "service": "ERP / accounting", "criticality": "Medium"},
    {"name": "Data Warehouse (Sandbox)", "service": "Analytics / reporting", "criticality": "Medium"},
]

ATLASPAY_INCIDENT = {
    "title": "Sample Phishing Incident — Finance Department",
    "severity": "High",
    "category": "Phishing",
    "linked_risk": "R-01",
    "summary": (
        "Sample incident for sandbox demonstration. A finance team member received a phishing "
        "email impersonating the CFO requesting an urgent wire transfer. The user reported the "
        "email to IT within 30 minutes. No funds were transferred. The incident is used as the "
        "test case for the IR plan and tabletop exercise (per R-04). Source: derived from "
        "AtlasPay-Risk-Assessment R-01 treatment narrative."
    ),
}

# =========================================================================
log("=" * 70)
log("AtlasPay Sandbox — full data ingestion")
log("=" * 70)
log(f"Source data: {SRC}")
log(f"  Risks: {len(ATLASPAY_RISKS)} from AtlasPay-Risk-Assessment")
log(f"  Policies: {len(ATLASPAY_POLICIES)} from Cyber-Security-Policy-Library")
log(f"  Continuity plans: {len(ATLASPAY_CONTINUITY)} from AtlasPay BCP")
log(f"  Vendors: {len(ATLASPAY_VENDORS)} (anonymized for sandbox)")
log(f"  Incidents: {len([ATLASPAY_INCIDENT])} (phishing sample)")
log("")

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--ignore-certificate-errors", "--no-sandbox"],
    )
    ctx = browser.new_context(
        ignore_https_errors=True,
        viewport={"width": 1440, "height": 900},
        locale="en-US",
        timezone_id="America/New_York",
    )
    page = ctx.new_page()

    # ---- LOGIN ----
    log("LOGIN")
    page.goto(ERAMBA_URL + "/login", wait_until="networkidle", timeout=60000)
    time.sleep(2)
    page.locator("input[name=login]").fill(USER)
    page.locator("input[name=password]").fill(PASS)
    page.locator("button[name=submit]").click()
    page.wait_for_selector("a:has-text('Dashboard')", timeout=30000)
    time.sleep(3)
    log(f"  logged in, URL: {page.url}")
    log("")

    # ============================================================
    # STEP 1: RISK SETTINGS CONFIG
    # ============================================================
    log("STEP 1: Configure Risk Settings")
    log("  -> /settings/risk-classifications")
    page.goto(ERAMBA_URL + "/settings/risk-classifications",
              wait_until="networkidle", timeout=30000)
    time.sleep(2)
    shot(page, "20-risk-classifications-empty")

    # Try to add a classification
    try:
        add = page.get_by_role("link", name="Add", exact=False).first
        if add.is_visible(timeout=3000):
            log("  Clicking 'Add' on classifications")
            add.click()
            page.wait_for_load_state("networkidle", timeout=15000)
            time.sleep(2)
            shot(page, "21-classifications-add-form")
            # Fill name + value
            try:
                page.locator("input[name=name]").first.fill("Critical")
                log("    filled name=Critical")
            except Exception as e:
                log(f"    WARN: name fill: {e}")
            try:
                page.locator("input[name=value]").first.fill("20")
                log("    filled value=20")
            except Exception as e:
                log(f"    WARN: value fill: {e}")
            shot(page, "22-classifications-form-filled")
            # Submit
            try:
                page.get_by_role("button", name="Save", exact=False).first.click(timeout=5000)
                page.wait_for_load_state("networkidle", timeout=15000)
                time.sleep(2)
                log("    submitted")
            except Exception as e:
                log(f"    WARN: save: {e}")
            shot(page, "23-classifications-after-save")
    except Exception as e:
        log(f"  WARN: could not find Add button: {e}")
    log("")

    # Risk Calculations
    log("STEP 1b: Risk Calculations")
    page.goto(ERAMBA_URL + "/settings/risk-calculations",
              wait_until="networkidle", timeout=30000)
    time.sleep(2)
    shot(page, "24-risk-calculations")
    log("")

    # Risk Appetite
    log("STEP 1c: Risk Appetite")
    page.goto(ERAMBA_URL + "/settings/risk-appetite",
              wait_until="networkidle", timeout=30000)
    time.sleep(2)
    shot(page, "25-risk-appetite")
    log("")

    # ============================================================
    # STEP 2: CREATE ATLASPAY SANDBOX ORGANIZATION
    # ============================================================
    log("STEP 2: Create AtlasPay Sandbox Organization")
    page.goto(ERAMBA_URL + "/program-scopes",
              wait_until="networkidle", timeout=30000)
    time.sleep(2)
    shot(page, "30-program-scopes-empty")

    try:
        add = page.get_by_role("link", name="Add", exact=False).first
        if add.is_visible(timeout=3000):
            log("  Clicking 'Add'")
            add.click()
            page.wait_for_load_state("networkidle", timeout=15000)
            time.sleep(2)
            shot(page, "31-program-scopes-add-form")
            # Form inspection
            inputs = page.evaluate("""
                () => Array.from(document.querySelectorAll('input, select, textarea')).map(el => ({
                    tag: el.tagName.toLowerCase(),
                    type: el.type || '',
                    name: el.name || '',
                    id: el.id || '',
                    placeholder: el.placeholder || '',
                    value: el.value || '',
                    label: (el.labels && el.labels[0]) ? el.labels[0].innerText : ''
                }))
            """)
            for inp in inputs[:20]:
                log(f"    <{inp['tag']} name={inp['name']} id={inp['id']} label={inp['label'][:30]!r}>")
    except Exception as e:
        log(f"  WARN: {e}")
    log("")

    # ============================================================
    # STEP 3: ACTIVATE SOC 2 FRAMEWORK
    # ============================================================
    log("STEP 3: Activate SOC 2 framework")
    page.goto(ERAMBA_URL + "/compliance-managements",
              wait_until="networkidle", timeout=30000)
    time.sleep(2)
    shot(page, "40-compliance-empty")

    # Look at compliance packages
    page.goto(ERAMBA_URL + "/compliance-package-regulators",
              wait_until="networkidle", timeout=30000)
    time.sleep(2)
    shot(page, "41-compliance-packages")
    log("")

    # ============================================================
    # STEP 4: INGEST RISKS
    # ============================================================
    log("STEP 4: Ingest risks into /risks")
    page.goto(ERAMBA_URL + "/risks", wait_until="networkidle", timeout=30000)
    time.sleep(2)
    shot(page, "50-risks-empty")

    # Try to add the first risk to verify the form works
    try:
        add = page.get_by_role("link", name="Add", exact=False).first
        if add.is_visible(timeout=3000):
            add.click()
            page.wait_for_load_state("networkidle", timeout=15000)
            time.sleep(2)
            shot(page, "51-risks-add-form")
            # Form inspection
            inputs = page.evaluate("""
                () => Array.from(document.querySelectorAll('input, select, textarea')).map(el => ({
                    tag: el.tagName.toLowerCase(),
                    type: el.type || '',
                    name: el.name || '',
                    id: el.id || '',
                    placeholder: el.placeholder || '',
                    value: el.value || '',
                    label: (el.labels && el.labels[0]) ? el.labels[0].innerText : ''
                }))
            """)
            log(f"  Add form has {len(inputs)} input/select/textarea elements")
            for inp in inputs[:30]:
                log(f"    <{inp['tag']} name={inp['name']} type={inp['type']} id={inp['id']} label={inp['label'][:40]!r}>")
    except Exception as e:
        log(f"  WARN: {e}")
    log("")

    # ============================================================
    # STEP 5: INGEST POLICIES
    # ============================================================
    log("STEP 5: Ingest policies into /security-policies")
    page.goto(ERAMBA_URL + "/security-policies",
              wait_until="networkidle", timeout=30000)
    time.sleep(2)
    shot(page, "60-policies-empty")

    try:
        add = page.get_by_role("link", name="Add", exact=False).first
        if add.is_visible(timeout=3000):
            add.click()
            page.wait_for_load_state("networkidle", timeout=15000)
            time.sleep(2)
            shot(page, "61-policies-add-form")
            inputs = page.evaluate("""
                () => Array.from(document.querySelectorAll('input, select, textarea')).map(el => ({
                    tag: el.tagName.toLowerCase(),
                    type: el.type || '',
                    name: el.name || '',
                    id: el.id || '',
                    placeholder: el.placeholder || '',
                    value: el.value || '',
                    label: (el.labels && el.labels[0]) ? el.labels[0].innerText : ''
                }))
            """)
            log(f"  Add form has {len(inputs)} input elements")
            for inp in inputs[:30]:
                log(f"    <{inp['tag']} name={inp['name']} type={inp['type']} label={inp['label'][:40]!r}>")
    except Exception as e:
        log(f"  WARN: {e}")
    log("")

    # ============================================================
    # STEP 6: INGEST CONTINUITY PLANS
    # ============================================================
    log("STEP 6: Ingest continuity plans")
    page.goto(ERAMBA_URL + "/business-continuity-plans",
              wait_until="networkidle", timeout=30000)
    time.sleep(2)
    shot(page, "70-bcp-empty")

    try:
        add = page.get_by_role("link", name="Add", exact=False).first
        if add.is_visible(timeout=3000):
            add.click()
            page.wait_for_load_state("networkidle", timeout=15000)
            time.sleep(2)
            shot(page, "71-bcp-add-form")
            inputs = page.evaluate("""
                () => Array.from(document.querySelectorAll('input, select, textarea')).map(el => ({
                    tag: el.tagName.toLowerCase(),
                    type: el.type || '',
                    name: el.name || '',
                    id: el.id || '',
                    label: (el.labels && el.labels[0]) ? el.labels[0].innerText : ''
                }))
            """)
            log(f"  Add form has {len(inputs)} input elements")
            for inp in inputs[:30]:
                log(f"    <{inp['tag']} name={inp['name']} type={inp['type']} label={inp['label'][:40]!r}>")
    except Exception as e:
        log(f"  WARN: {e}")
    log("")

    # ============================================================
    # STEP 7: VENDORS
    # ============================================================
    log("STEP 7: Create vendor records")
    page.goto(ERAMBA_URL + "/third-parties",
              wait_until="networkidle", timeout=30000)
    time.sleep(2)
    shot(page, "80-third-parties-empty")

    try:
        add = page.get_by_role("link", name="Add", exact=False).first
        if add.is_visible(timeout=3000):
            add.click()
            page.wait_for_load_state("networkidle", timeout=15000)
            time.sleep(2)
            shot(page, "81-third-parties-add-form")
            inputs = page.evaluate("""
                () => Array.from(document.querySelectorAll('input, select, textarea')).map(el => ({
                    tag: el.tagName.toLowerCase(),
                    type: el.type || '',
                    name: el.name || '',
                    id: el.id || '',
                    label: (el.labels && el.labels[0]) ? el.labels[0].innerText : ''
                }))
            """)
            log(f"  Add form has {len(inputs)} input elements")
            for inp in inputs[:30]:
                log(f"    <{inp['tag']} name={inp['name']} type={inp['type']} label={inp['label'][:40]!r}>")
    except Exception as e:
        log(f"  WARN: {e}")
    log("")

    # ============================================================
    # STEP 8: INCIDENTS
    # ============================================================
    log("STEP 8: Create sample incident")
    page.goto(ERAMBA_URL + "/security-incidents",
              wait_until="networkidle", timeout=30000)
    time.sleep(2)
    shot(page, "90-incidents-empty")

    try:
        add = page.get_by_role("link", name="Add", exact=False).first
        if add.is_visible(timeout=3000):
            add.click()
            page.wait_for_load_state("networkidle", timeout=15000)
            time.sleep(2)
            shot(page, "91-incidents-add-form")
            inputs = page.evaluate("""
                () => Array.from(document.querySelectorAll('input, select, textarea')).map(el => ({
                    tag: el.tagName.toLowerCase(),
                    type: el.type || '',
                    name: el.name || '',
                    id: el.id || '',
                    label: (el.labels && el.labels[0]) ? el.labels[0].innerText : ''
                }))
            """)
            log(f"  Add form has {len(inputs)} input elements")
            for inp in inputs[:30]:
                log(f"    <{inp['tag']} name={inp['name']} type={inp['type']} label={inp['label'][:40]!r}>")
    except Exception as e:
        log(f"  WARN: {e}")
    log("")

    log("=" * 70)
    log("Inspection complete. All Add forms visited; selectors documented.")
    log("Next pass will fill them with real AtlasPay data.")
    log("=" * 70)
    browser.close()
