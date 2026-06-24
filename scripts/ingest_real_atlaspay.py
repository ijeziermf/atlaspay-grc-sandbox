"""
AtlasPay Sandbox — REAL data ingestion driver.

Uses the real Eramba CE routes discovered in scripts/explore_risk_subpages.py:
  /risks, /risks/classifications, /risks/threats, /risks/vulnerabilities
  /security-policies, /business-continuity-plans
  /third-parties, /security-incidents
  /compliance-managements, /compliance-package-regulators
  /program-scopes

Settings modals (Classification Types, Calculation Method, Risk Appetite) are
opened via the Settings button on /risks (data-yjs-request=crud/showForm).
"""
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path.home() / "Documents" / "IfeSec" / "Projects" / "atlaspay-grc-sandbox"
SHOTS = ROOT / "screenshots"
DOCS = ROOT / "docs"
SHOTS.mkdir(parents=True, exist_ok=True)
DOCS.mkdir(parents=True, exist_ok=True)

ERAMBA_URL = "https://localhost:8443"
USER, PASS = "admin", "8950Fourth"

LOG = DOCS / "07-real-ingestion.md"
LOG.write_text("# AtlasPay Sandbox — Real data ingestion run\n\n")
def log(msg=""):
    ts = time.strftime("%H:%M:%S")
    line = f"[{ts}] {msg}\n" if msg else "\n"
    with LOG.open("a") as f:
        f.write(line)
    print(line.rstrip())

def shot(page, name, full=True):
    path = SHOTS / f"{name}.png"
    page.screenshot(path=str(path), full_page=full)
    log(f"  -> {path.name} ({path.stat().st_size // 1024} KB)")

# AtlasPay data — extracted from source-data/extracted/*.txt
ATLASPAY_RISKS = [
    {"id": "R-01", "title": "Phishing Attacks", "inherent": 20, "residual": 6,
     "owner": "IT Security Manager", "treatment": "Mitigate",
     "desc": "Phishing identified as high-priority risk due to likelihood and impact on financial systems. Source: AtlasPay-Risk-Assessment R-01."},
    {"id": "R-02", "title": "Access Control Weakness", "inherent": 12, "residual": 6,
     "owner": "Identity & Access Lead", "treatment": "Mitigate",
     "desc": "Inconsistent least privilege enforcement and limited access approval documentation. Source: AtlasPay-Risk-Assessment R-02."},
    {"id": "R-03", "title": "Logging and Monitoring Gaps", "inherent": 9, "residual": 6,
     "owner": "Security Operations Lead", "treatment": "Mitigate",
     "desc": "Insufficient centralized logging impacting incident detection. Source: AtlasPay-Risk-Assessment R-03."},
    {"id": "R-04", "title": "Incident Response Planning and Testing", "inherent": 12, "residual": 6,
     "owner": "Incident Response Coordinator", "treatment": "Mitigate",
     "desc": "Gaps in IR documentation, approval, and testing. Source: AtlasPay-Risk-Assessment R-04."},
    {"id": "R-05", "title": "Third-Party and Vendor Risk Management", "inherent": 12, "residual": 6,
     "owner": "Vendor Risk Manager", "treatment": "Mitigate",
     "desc": "Lack of formal TPRM and monitoring. Source: AtlasPay-Risk-Assessment R-05."},
    {"id": "R-06", "title": "Security Awareness and Training", "inherent": 10, "residual": 6,
     "owner": "Security Awareness Lead", "treatment": "Mitigate",
     "desc": "Generalized training with limited effectiveness measurement. Source: AtlasPay-Risk-Assessment R-06."},
]

ATLASPAY_POLICIES = [
    {"title": "Access Control & Privileged Access Policy", "type": "Access Control", "linked_risks": "R-02"},
    {"title": "Incident Response Policy", "type": "Incident Response", "linked_risks": "R-01, R-04"},
    {"title": "Security Awareness & Acceptable Use Policy", "type": "Awareness", "linked_risks": "R-06"},
    {"title": "Third-Party Risk Management Policy", "type": "Vendor Risk", "linked_risks": "R-05"},
]

ATLASPAY_CONTINUITY = [
    {"function": "Payment Processing", "mtpd": "24 hours", "rto": "4 hours", "rpo": "Near-real-time", "deps": "Cloud provider, payment gateway", "priority": "Critical"},
    {"function": "Customer Account Access", "mtpd": "48 hours", "rto": "8 hours", "rpo": "24 hours", "deps": "Identity provider, application platform", "priority": "High"},
    {"function": "Fraud Monitoring", "mtpd": "24 hours", "rto": "4 hours", "rpo": "Near-real-time", "deps": "Monitoring tools, transaction data", "priority": "Critical"},
    {"function": "Financial Reporting", "mtpd": "72 hours", "rto": "24 hours", "rpo": "24 hours", "deps": "Finance systems, data warehouse", "priority": "Medium"},
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
    "summary": "Sample incident for sandbox. Finance team member received phishing email impersonating CFO requesting urgent wire transfer. User reported within 30 minutes. No funds transferred. Demonstrates the IR process (linked to R-01 + R-04).",
}

# =========================================================================
log("=" * 70)
log("AtlasPay Sandbox — REAL data ingestion")
log("=" * 70)
log(f"Risks: {len(ATLASPAY_RISKS)}, Policies: {len(ATLASPAY_POLICIES)}, ")
log(f"Continuity: {len(ATLASPAY_CONTINUITY)}, Vendors: {len(ATLASPAY_VENDORS)}, ")
log(f"Incidents: 1")
log("")

results = {
    "risks_added": 0,
    "policies_added": 0,
    "continuity_added": 0,
    "vendors_added": 0,
    "incidents_added": 0,
    "classifications_added": 0,
    "errors": [],
}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--ignore-certificate-errors", "--no-sandbox"])
    ctx = browser.new_context(ignore_https_errors=True, viewport={"width": 1440, "height": 900})
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
    # STEP 1: ADD CLASSIFICATIONS (5 levels matching the AtlasPay scoring)
    # ============================================================
    log("STEP 1: Add Risk Classifications (5 levels: Critical/High/Medium/Low/Very Low)")
    page.goto(ERAMBA_URL + "/risks/classifications", wait_until="networkidle", timeout=30000)
    time.sleep(3)
    shot(page, "200-classifications-empty")

    classifications = [
        {"name": "Critical", "value": "20"},
        {"name": "High", "value": "12"},
        {"name": "Medium", "value": "8"},
        {"name": "Low", "value": "4"},
        {"name": "Very Low", "value": "2"},
    ]

    for cls in classifications:
        try:
            log(f"  Adding classification: {cls['name']} (value={cls['value']})")
            add_btn = page.get_by_role("button", name="Add", exact=False).first
            if not add_btn.is_visible(timeout=3000):
                # Try add link
                add_btn = page.get_by_role("link", name="Add", exact=False).first
            add_btn.click(timeout=5000)
            page.wait_for_load_state("networkidle", timeout=15000)
            time.sleep(2)
            # Fill name and value
            try:
                page.locator("input[name=name]").first.fill(cls['name'])
            except Exception:
                log(f"    WARN: no name input found")
            try:
                page.locator("input[name=value]").first.fill(cls['value'])
            except Exception:
                log(f"    WARN: no value input found")
            # Submit
            try:
                page.get_by_role("button", name="Save", exact=False).first.click(timeout=5000)
            except Exception:
                try:
                    page.locator("button[type=submit]").first.click(timeout=5000)
                except Exception as e:
                    log(f"    WARN: could not submit: {e}")
            page.wait_for_load_state("networkidle", timeout=15000)
            time.sleep(2)
            results["classifications_added"] += 1
            log(f"    added OK")
        except Exception as e:
            log(f"    ERROR: {e}")
            results["errors"].append(f"classification {cls['name']}: {e}")
    shot(page, "201-classifications-after")
    log("")

    # ============================================================
    # STEP 2: ADD RISKS (6 AtlasPay risks)
    # ============================================================
    log("STEP 2: Add Risks (R-01 through R-06)")
    page.goto(ERAMBA_URL + "/risks", wait_until="networkidle", timeout=30000)
    time.sleep(3)

    for risk in ATLASPAY_RISKS:
        try:
            log(f"  Adding risk {risk['id']}: {risk['title']}")
            add_btn = page.get_by_role("link", name="Add", exact=False).first
            if not add_btn.is_visible(timeout=3000):
                add_btn = page.get_by_role("button", name="Add", exact=False).first
            add_btn.click(timeout=5000)
            page.wait_for_load_state("networkidle", timeout=15000)
            time.sleep(2)
            # Fill the form
            try:
                page.locator("input[name=title]").first.fill(f"[{risk['id']}] {risk['title']}")
            except Exception:
                try:
                    page.locator("input[name=name]").first.fill(f"[{risk['id']}] {risk['title']}")
                except Exception as e:
                    log(f"    WARN: no title input: {e}")
            # Description / body
            for fname in ["description", "body", "details"]:
                try:
                    page.locator(f"textarea[name={fname}]").first.fill(risk['desc'])
                    log(f"    filled {fname}")
                    break
                except Exception:
                    continue
            # Save
            try:
                page.get_by_role("button", name="Save", exact=False).first.click(timeout=5000)
                page.wait_for_load_state("networkidle", timeout=15000)
                time.sleep(2)
                results["risks_added"] += 1
                log(f"    added OK")
            except Exception as e:
                log(f"    WARN: save: {e}")
                results["errors"].append(f"risk {risk['id']} save: {e}")
        except Exception as e:
            log(f"    ERROR: {e}")
            results["errors"].append(f"risk {risk['id']}: {e}")
    shot(page, "210-risks-after")
    log("")

    # ============================================================
    # STEP 3: ADD POLICIES
    # ============================================================
    log("STEP 3: Add Policies (4)")
    page.goto(ERAMBA_URL + "/security-policies", wait_until="networkidle", timeout=30000)
    time.sleep(3)

    for pol in ATLASPAY_POLICIES:
        try:
            log(f"  Adding policy: {pol['title']}")
            add_btn = page.get_by_role("link", name="Add", exact=False).first
            if not add_btn.is_visible(timeout=3000):
                add_btn = page.get_by_role("button", name="Add", exact=False).first
            add_btn.click(timeout=5000)
            page.wait_for_load_state("networkidle", timeout=15000)
            time.sleep(2)
            for fname in ["title", "name"]:
                try:
                    page.locator(f"input[name={fname}]").first.fill(pol['title'])
                    break
                except Exception:
                    continue
            try:
                page.get_by_role("button", name="Save", exact=False).first.click(timeout=5000)
                page.wait_for_load_state("networkidle", timeout=15000)
                time.sleep(2)
                results["policies_added"] += 1
                log(f"    added OK")
            except Exception as e:
                log(f"    WARN: save: {e}")
                results["errors"].append(f"policy {pol['title']} save: {e}")
        except Exception as e:
            log(f"    ERROR: {e}")
            results["errors"].append(f"policy {pol['title']}: {e}")
    shot(page, "220-policies-after")
    log("")

    # ============================================================
    # STEP 4: ADD CONTINUITY PLANS
    # ============================================================
    log("STEP 4: Add Continuity Plans (4 critical functions)")
    page.goto(ERAMBA_URL + "/business-continuity-plans", wait_until="networkidle", timeout=30000)
    time.sleep(3)

    for cp in ATLASPAY_CONTINUITY:
        try:
            log(f"  Adding continuity plan: {cp['function']}")
            add_btn = page.get_by_role("link", name="Add", exact=False).first
            if not add_btn.is_visible(timeout=3000):
                add_btn = page.get_by_role("button", name="Add", exact=False).first
            add_btn.click(timeout=5000)
            page.wait_for_load_state("networkidle", timeout=15000)
            time.sleep(2)
            title = f"{cp['function']} (RTO={cp['rto']}, RPO={cp['rpo']}, MTPD={cp['mtpd']})"
            for fname in ["title", "name"]:
                try:
                    page.locator(f"input[name={fname}]").first.fill(title)
                    break
                except Exception:
                    continue
            try:
                page.get_by_role("button", name="Save", exact=False).first.click(timeout=5000)
                page.wait_for_load_state("networkidle", timeout=15000)
                time.sleep(2)
                results["continuity_added"] += 1
                log(f"    added OK")
            except Exception as e:
                log(f"    WARN: save: {e}")
                results["errors"].append(f"continuity {cp['function']} save: {e}")
        except Exception as e:
            log(f"    ERROR: {e}")
            results["errors"].append(f"continuity {cp['function']}: {e}")
    shot(page, "230-bcp-after")
    log("")

    # ============================================================
    # STEP 5: ADD VENDORS
    # ============================================================
    log("STEP 5: Add Vendors (7)")
    page.goto(ERAMBA_URL + "/third-parties", wait_until="networkidle", timeout=30000)
    time.sleep(3)

    for ven in ATLASPAY_VENDORS:
        try:
            log(f"  Adding vendor: {ven['name']}")
            add_btn = page.get_by_role("link", name="Add", exact=False).first
            if not add_btn.is_visible(timeout=3000):
                add_btn = page.get_by_role("button", name="Add", exact=False).first
            add_btn.click(timeout=5000)
            page.wait_for_load_state("networkidle", timeout=15000)
            time.sleep(2)
            for fname in ["name", "title"]:
                try:
                    page.locator(f"input[name={fname}]").first.fill(ven['name'])
                    break
                except Exception:
                    continue
            try:
                page.get_by_role("button", name="Save", exact=False).first.click(timeout=5000)
                page.wait_for_load_state("networkidle", timeout=15000)
                time.sleep(2)
                results["vendors_added"] += 1
                log(f"    added OK")
            except Exception as e:
                log(f"    WARN: save: {e}")
                results["errors"].append(f"vendor {ven['name']} save: {e}")
        except Exception as e:
            log(f"    ERROR: {e}")
            results["errors"].append(f"vendor {ven['name']}: {e}")
    shot(page, "240-vendors-after")
    log("")

    # ============================================================
    # STEP 6: ADD INCIDENT
    # ============================================================
    log("STEP 6: Add Sample Incident (phishing scenario)")
    page.goto(ERAMBA_URL + "/security-incidents", wait_until="networkidle", timeout=30000)
    time.sleep(3)
    try:
        log(f"  Adding incident: {ATLASPAY_INCIDENT['title']}")
        add_btn = page.get_by_role("link", name="Add", exact=False).first
        if not add_btn.is_visible(timeout=3000):
            add_btn = page.get_by_role("button", name="Add", exact=False).first
        add_btn.click(timeout=5000)
        page.wait_for_load_state("networkidle", timeout=15000)
        time.sleep(2)
        for fname in ["title", "name"]:
            try:
                page.locator(f"input[name={fname}]").first.fill(ATLASPAY_INCIDENT['title'])
                break
            except Exception:
                continue
        try:
            page.get_by_role("button", name="Save", exact=False).first.click(timeout=5000)
            page.wait_for_load_state("networkidle", timeout=15000)
            time.sleep(2)
            results["incidents_added"] = 1
            log("    added OK")
        except Exception as e:
            log(f"    WARN: save: {e}")
            results["errors"].append(f"incident save: {e}")
    except Exception as e:
        log(f"  ERROR: {e}")
        results["errors"].append(f"incident: {e}")
    shot(page, "250-incidents-after")
    log("")

    # ============================================================
    # FINAL SUMMARY
    # ============================================================
    log("=" * 70)
    log("INGESTION SUMMARY")
    log("=" * 70)
    log(f"  Classifications added: {results['classifications_added']} / 5")
    log(f"  Risks added:           {results['risks_added']} / 6")
    log(f"  Policies added:        {results['policies_added']} / 4")
    log(f"  Continuity plans:      {results['continuity_added']} / 4")
    log(f"  Vendors added:         {results['vendors_added']} / 7")
    log(f"  Incidents added:       {results['incidents_added']} / 1")
    if results["errors"]:
        log(f"\n  Errors ({len(results['errors'])}):")
        for err in results["errors"]:
            log(f"    - {err}")
    log("")

    # Save results as JSON
    with (DOCS / "08-ingestion-results.json").open("w") as f:
        json.dump(results, f, indent=2)
    log("Results saved to docs/08-ingestion-results.json")

    browser.close()
