"""
AtlasPay Sandbox — REAL data ingestion driver v2.

WORKS WITH: the real Eramba CE UX pattern:
  1. Navigate to the list URL (e.g., /risks/classifications)
  2. Click the "Actions" dropdown (a.dropdown-toggle)
  3. Click "Add" inside the dropdown
  4. Fill the form (real field names discovered via inspect_classifications.py)
  5. Submit via "Save" or the submit button

Form fields per section discovered via DOM inspection:
  /risks/classifications: select[name=risk_classification_type_id], input[name=name],
                          textarea[name=criteria], input[name=value]
  /risks/threats: TBD
  /risks/vulnerabilities: TBD
  /risks: TBD (after Classifications are configured)
  /security-policies: TBD
  /business-continuity-plans: TBD
  /third-parties: TBD
  /security-incidents: TBD
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

LOG = DOCS / "09-v2-ingestion.md"
LOG.write_text("# AtlasPay Sandbox — v2 ingestion (Actions dropdown pattern)\n\n")
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

def open_add_form(page, label="this section"):
    """Navigate via Actions -> Add. Returns (inputs_dict, success_bool)."""
    log(f"  Opening Add form for {label}")
    # Click the Actions dropdown (a.dropdown-toggle)
    actions = page.locator("a.dropdown-toggle:has-text('Actions')").first
    if not actions.is_visible(timeout=5000):
        log(f"    WARN: 'Actions' dropdown not visible")
        return {}, False
    actions.click()
    time.sleep(1)
    # Click Add in the dropdown
    add_item = page.locator(".dropdown-menu a:has-text('Add')").first
    if not add_item.is_visible(timeout=3000):
        log(f"    WARN: 'Add' item not in dropdown")
        page.keyboard.press("Escape")
        return {}, False
    add_item.click()
    page.wait_for_load_state("networkidle", timeout=15000)
    time.sleep(2)
    # Snapshot inputs
    inputs = page.evaluate("""
        () => Array.from(document.querySelectorAll('input, select, textarea')).filter(el => el.getBoundingClientRect().width > 0).map(el => ({
            tag: el.tagName.toLowerCase(),
            type: el.type || '',
            name: el.name || '',
            id: el.id || '',
            placeholder: el.placeholder || '',
            value: el.value || ''
        }))
    """)
    log(f"    form has {len(inputs)} fields:")
    for i in inputs:
        log(f"      <{i['tag']}> type={i['type']} name={i['name']} id={i['id']} value='{i['value'][:30]}'")
    return {i['name']: i for i in inputs if i['name']}, True

def submit_form(page):
    """Click the Save / Submit button on the open form."""
    # Eramba modals have a Save button typically as button[type=submit] or btn-primary
    candidates = [
        "button[type=submit]",
        "button.btn-primary",
        "button:has-text('Save')",
        "button:has-text('Submit')",
        "input[type=submit]",
    ]
    for sel in candidates:
        try:
            loc = page.locator(sel).first
            if loc.is_visible(timeout=2000):
                log(f"    submitting via {sel}")
                loc.click()
                page.wait_for_load_state("networkidle", timeout=15000)
                time.sleep(2)
                return True
        except Exception:
            continue
    log(f"    WARN: could not find submit button")
    return False

# AtlasPay data
ATLASPAY_RISKS = [
    {"id": "R-01", "title": "Phishing Attacks", "inherent": 20, "residual": 6,
     "desc": "Phishing identified as high-priority risk due to likelihood and impact on financial systems and sensitive data. Source: AtlasPay-Risk-Assessment R-01."},
    {"id": "R-02", "title": "Access Control Weakness", "inherent": 12, "residual": 6,
     "desc": "Inconsistent least privilege enforcement and limited access approval documentation. Source: AtlasPay-Risk-Assessment R-02."},
    {"id": "R-03", "title": "Logging and Monitoring Gaps", "inherent": 9, "residual": 6,
     "desc": "Insufficient centralized logging impacting incident detection and response. Source: AtlasPay-Risk-Assessment R-03."},
    {"id": "R-04", "title": "Incident Response Planning and Testing", "inherent": 12, "residual": 6,
     "desc": "Gaps in IR documentation, approval, and testing of response procedures. Source: AtlasPay-Risk-Assessment R-04."},
    {"id": "R-05", "title": "Third-Party and Vendor Risk Management", "inherent": 12, "residual": 6,
     "desc": "Lack of formal TPRM and ongoing monitoring program. Source: AtlasPay-Risk-Assessment R-05."},
    {"id": "R-06", "title": "Security Awareness and Training", "inherent": 10, "residual": 6,
     "desc": "Generalized training with limited effectiveness measurement. Source: AtlasPay-Risk-Assessment R-06."},
]

ATLASPAY_POLICIES = [
    {"title": "Access Control & Privileged Access Policy"},
    {"title": "Incident Response Policy"},
    {"title": "Security Awareness & Acceptable Use Policy"},
    {"title": "Third-Party Risk Management Policy"},
]

ATLASPAY_CONTINUITY = [
    {"title": "Payment Processing BCP", "rto": "4 hours", "rpo": "Near-real-time", "mtpd": "24 hours"},
    {"title": "Customer Account Access BCP", "rto": "8 hours", "rpo": "24 hours", "mtpd": "48 hours"},
    {"title": "Fraud Monitoring BCP", "rto": "4 hours", "rpo": "Near-real-time", "mtpd": "24 hours"},
    {"title": "Financial Reporting BCP", "rto": "24 hours", "rpo": "24 hours", "mtpd": "72 hours"},
]

ATLASPAY_VENDORS = [
    {"name": "Cloud Provider (Sandbox)"},
    {"name": "Payment Gateway (Sandbox)"},
    {"name": "Identity Provider (Sandbox)"},
    {"name": "Application Platform (Sandbox)"},
    {"name": "Monitoring Tools (Sandbox)"},
    {"name": "Finance Systems (Sandbox)"},
    {"name": "Data Warehouse (Sandbox)"},
]

ATLASPAY_INCIDENT = {"title": "Sample Phishing Incident - Finance Department"}

# ============================================================
log("=" * 70)
log("AtlasPay Sandbox — REAL data ingestion v2 (Actions dropdown)")
log("=" * 70)
log("")

results = {
    "classifications": [],
    "risks": [],
    "policies": [],
    "continuity": [],
    "vendors": [],
    "incidents": [],
    "errors": [],
}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--ignore-certificate-errors", "--no-sandbox"])
    ctx = browser.new_context(ignore_https_errors=True, viewport={"width": 1440, "height": 900})
    page = ctx.new_page()

    # LOGIN
    log("LOGIN")
    page.goto(ERAMBA_URL + "/login", wait_until="networkidle", timeout=60000)
    time.sleep(2)
    page.locator("input[name=login]").fill(USER)
    page.locator("input[name=password]").fill(PASS)
    page.locator("button[name=submit]").click()
    page.wait_for_selector("a:has-text('Dashboard')", timeout=30000)
    time.sleep(3)
    log(f"  logged in")
    log("")

    # ============================================================
    # STEP 1: CLASSIFICATIONS
    # ============================================================
    log("STEP 1: Add Risk Classifications")
    page.goto(ERAMBA_URL + "/risks/classifications", wait_until="networkidle", timeout=30000)
    time.sleep(3)

    classifications = [
        {"name": "Critical", "value": "20"},
        {"name": "High", "value": "12"},
        {"name": "Medium", "value": "8"},
        {"name": "Low", "value": "4"},
        {"name": "Very Low", "value": "2"},
    ]

    for cls in classifications:
        log(f"\n  Adding classification: {cls['name']} (value={cls['value']})")
        inputs, ok = open_add_form(page, "classifications")
        if not ok:
            results["errors"].append(f"classification {cls['name']}: form not open")
            continue
        try:
            if "name" in inputs:
                page.locator("input[name=name]").first.fill(cls['name'])
            if "value" in inputs:
                page.locator("input[name=value]").first.fill(cls['value'])
            # Default the classification_type to "Impact" (first option) if available
            if "risk_classification_type_id" in inputs:
                sel = page.locator("select[name=risk_classification_type_id]").first
                opts = sel.evaluate("el => Array.from(el.options).map(o => o.value + ':' + o.text)")
                log(f"      classification_type options: {opts}")
                # Pick the first non-empty value
                if opts:
                    sel.select_option(index=0)
            shot(page, f"400-classification-{cls['name']}-form")
            if submit_form(page):
                results["classifications"].append(cls['name'])
                log(f"    added")
            else:
                results["errors"].append(f"classification {cls['name']}: submit failed")
        except Exception as e:
            log(f"    ERROR: {e}")
            results["errors"].append(f"classification {cls['name']}: {e}")
        # Close any open modal by navigating away
        page.goto(ERAMBA_URL + "/risks/classifications", wait_until="networkidle", timeout=30000)
        time.sleep(2)

    shot(page, "401-classifications-final")
    log("")

    # ============================================================
    # STEP 2: RISKS
    # ============================================================
    log("STEP 2: Add Risks (R-01 through R-06)")
    page.goto(ERAMBA_URL + "/risks", wait_until="networkidle", timeout=30000)
    time.sleep(3)
    shot(page, "410-risks-pre")

    for risk in ATLASPAY_RISKS:
        log(f"\n  Adding risk {risk['id']}: {risk['title']}")
        inputs, ok = open_add_form(page, f"risk {risk['id']}")
        if not ok:
            results["errors"].append(f"risk {risk['id']}: form not open")
            continue
        try:
            # Fill the title-like field
            title_filled = False
            for fname in ["title", "name"]:
                if fname in inputs:
                    page.locator(f"input[name={fname}]").first.fill(f"[{risk['id']}] {risk['title']}")
                    title_filled = True
                    log(f"      filled {fname}='[{risk['id']}] {risk['title']}'")
                    break
            if not title_filled:
                log(f"      WARN: no title/name field found")
            # Fill description
            for fname in ["description", "body", "details"]:
                if fname in inputs:
                    try:
                        page.locator(f"textarea[name={fname}]").first.fill(risk['desc'])
                        log(f"      filled {fname}")
                        break
                    except Exception:
                        continue
            shot(page, f"411-risk-{risk['id']}-form")
            if submit_form(page):
                results["risks"].append(risk['id'])
                log(f"    added")
            else:
                results["errors"].append(f"risk {risk['id']}: submit failed")
        except Exception as e:
            log(f"    ERROR: {e}")
            results["errors"].append(f"risk {risk['id']}: {e}")
        page.goto(ERAMBA_URL + "/risks", wait_until="networkidle", timeout=30000)
        time.sleep(2)

    shot(page, "412-risks-final")
    log("")

    # ============================================================
    # STEP 3: POLICIES
    # ============================================================
    log("STEP 3: Add Policies (4)")
    page.goto(ERAMBA_URL + "/security-policies", wait_until="networkidle", timeout=30000)
    time.sleep(3)

    for pol in ATLASPAY_POLICIES:
        log(f"\n  Adding policy: {pol['title']}")
        inputs, ok = open_add_form(page, f"policy {pol['title']}")
        if not ok:
            results["errors"].append(f"policy {pol['title']}: form not open")
            continue
        try:
            for fname in ["title", "name"]:
                if fname in inputs:
                    page.locator(f"input[name={fname}]").first.fill(pol['title'])
                    log(f"      filled {fname}")
                    break
            shot(page, f"421-policy-form")
            if submit_form(page):
                results["policies"].append(pol['title'])
                log(f"    added")
            else:
                results["errors"].append(f"policy {pol['title']}: submit failed")
        except Exception as e:
            log(f"    ERROR: {e}")
            results["errors"].append(f"policy {pol['title']}: {e}")
        page.goto(ERAMBA_URL + "/security-policies", wait_until="networkidle", timeout=30000)
        time.sleep(2)

    shot(page, "422-policies-final")
    log("")

    # ============================================================
    # STEP 4: CONTINUITY PLANS
    # ============================================================
    log("STEP 4: Add Continuity Plans (4)")
    page.goto(ERAMBA_URL + "/business-continuity-plans", wait_until="networkidle", timeout=30000)
    time.sleep(3)

    for cp in ATLASPAY_CONTINUITY:
        log(f"\n  Adding continuity plan: {cp['title']}")
        inputs, ok = open_add_form(page, f"BCP {cp['title']}")
        if not ok:
            results["errors"].append(f"BCP {cp['title']}: form not open")
            continue
        try:
            for fname in ["title", "name"]:
                if fname in inputs:
                    page.locator(f"input[name={fname}]").first.fill(cp['title'])
                    log(f"      filled {fname}")
                    break
            # Fill RTO/RPO/MTPD if those fields exist
            for fname, val in [("rto", cp['rto']), ("rpo", cp['rpo']), ("mtpd", cp['mtpd'])]:
                if fname in inputs:
                    try:
                        page.locator(f"input[name={fname}]").first.fill(val)
                        log(f"      filled {fname}={val}")
                    except Exception:
                        pass
            shot(page, f"431-bcp-form")
            if submit_form(page):
                results["continuity"].append(cp['title'])
                log(f"    added")
            else:
                results["errors"].append(f"BCP {cp['title']}: submit failed")
        except Exception as e:
            log(f"    ERROR: {e}")
            results["errors"].append(f"BCP {cp['title']}: {e}")
        page.goto(ERAMBA_URL + "/business-continuity-plans", wait_until="networkidle", timeout=30000)
        time.sleep(2)

    shot(page, "432-bcp-final")
    log("")

    # ============================================================
    # STEP 5: VENDORS
    # ============================================================
    log("STEP 5: Add Vendors (7)")
    page.goto(ERAMBA_URL + "/third-parties", wait_until="networkidle", timeout=30000)
    time.sleep(3)

    for ven in ATLASPAY_VENDORS:
        log(f"\n  Adding vendor: {ven['name']}")
        inputs, ok = open_add_form(page, f"vendor {ven['name']}")
        if not ok:
            results["errors"].append(f"vendor {ven['name']}: form not open")
            continue
        try:
            for fname in ["name", "title"]:
                if fname in inputs:
                    page.locator(f"input[name={fname}]").first.fill(ven['name'])
                    log(f"      filled {fname}")
                    break
            shot(page, f"441-vendor-form")
            if submit_form(page):
                results["vendors"].append(ven['name'])
                log(f"    added")
            else:
                results["errors"].append(f"vendor {ven['name']}: submit failed")
        except Exception as e:
            log(f"    ERROR: {e}")
            results["errors"].append(f"vendor {ven['name']}: {e}")
        page.goto(ERAMBA_URL + "/third-parties", wait_until="networkidle", timeout=30000)
        time.sleep(2)

    shot(page, "442-vendors-final")
    log("")

    # ============================================================
    # STEP 6: INCIDENT
    # ============================================================
    log("STEP 6: Add Sample Incident")
    page.goto(ERAMBA_URL + "/security-incidents", wait_until="networkidle", timeout=30000)
    time.sleep(3)

    log(f"\n  Adding incident: {ATLASPAY_INCIDENT['title']}")
    inputs, ok = open_add_form(page, "incident")
    if ok:
        try:
            for fname in ["title", "name"]:
                if fname in inputs:
                    page.locator(f"input[name={fname}]").first.fill(ATLASPAY_INCIDENT['title'])
                    break
            shot(page, "451-incident-form")
            if submit_form(page):
                results["incidents"].append(ATLASPAY_INCIDENT['title'])
                log(f"    added")
        except Exception as e:
            log(f"    ERROR: {e}")
            results["errors"].append(f"incident: {e}")

    shot(page, "452-incidents-final")
    log("")

    # ============================================================
    # SUMMARY
    # ============================================================
    log("=" * 70)
    log("INGESTION SUMMARY (v2)")
    log("=" * 70)
    log(f"  Classifications added: {len(results['classifications'])} / 5")
    for c in results['classifications']:
        log(f"    - {c}")
    log(f"  Risks added:           {len(results['risks'])} / 6")
    for r in results['risks']:
        log(f"    - {r}")
    log(f"  Policies added:        {len(results['policies'])} / 4")
    for p in results['policies']:
        log(f"    - {p}")
    log(f"  Continuity added:      {len(results['continuity'])} / 4")
    for c in results['continuity']:
        log(f"    - {c}")
    log(f"  Vendors added:         {len(results['vendors'])} / 7")
    for v in results['vendors']:
        log(f"    - {v}")
    log(f"  Incidents added:       {len(results['incidents'])} / 1")
    for i in results['incidents']:
        log(f"    - {i}")
    if results["errors"]:
        log(f"\n  Errors ({len(results['errors'])}):")
        for err in results["errors"]:
            log(f"    - {err}")

    with (DOCS / "10-v2-results.json").open("w") as f:
        json.dump(results, f, indent=2)
    log("\nResults saved to docs/10-v2-results.json")

    browser.close()
