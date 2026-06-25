"""
AtlasPay Sandbox — REAL data ingestion driver v3 (FINAL).

Complete pattern (verified working):
  1. Navigate to list URL
  2. Click "Actions" dropdown (a.dropdown-toggle) -> Click "Add"
  3. Fill form via real field names discovered via DOM inspection
  4. Click "Save" (button[type=submit] or button.btn-primary)

For Risk Settings modals (Calculation Method, Risk Appetite, etc.):
  1. Click "Settings" button on /risks (aria-label='Settings')
  2. Click the desired submenu item (modal trigger)
  3. Toggle "Enable" and Save
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

LOG = DOCS / "11-v3-ingestion.md"
LOG.write_text("# AtlasPay Sandbox — v3 final ingestion run\n\n")
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

def close_open_modal(page):
    """Close any open modal by clicking the X or pressing Escape multiple times."""
    for _ in range(3):
        try:
            page.keyboard.press("Escape")
            time.sleep(0.5)
        except Exception:
            pass
    # Also try clicking the X close button
    try:
        x = page.locator(".modal .close, .modal button[aria-label='Close'], .modal .btn-close").first
        if x.is_visible(timeout=1000):
            x.click()
            time.sleep(1)
    except Exception:
        pass

def add_via_actions_dropdown(page, section_label, fill_fn):
    """Open the Actions dropdown on a list page, click Add, run fill_fn(form), submit."""
    log(f"\n  ADD: {section_label}")
    try:
        # Open Actions dropdown
        actions = page.locator("a.dropdown-toggle:has-text('Actions')").first
        if not actions.is_visible(timeout=5000):
            # Fallback: try 'Add item' button (used on /security-policies, /third-parties)
            add_btn = page.locator("button:has-text('Add item')").first
            if add_btn.is_visible(timeout=3000):
                add_btn.click()
                page.wait_for_load_state("networkidle", timeout=15000)
                time.sleep(2)
                return fill_fn_and_submit(page, section_label, fill_fn)
            log(f"    WARN: no Actions dropdown or Add item button")
            return False
        actions.click()
        time.sleep(1)
        # Click Add
        add_link = page.locator(".dropdown-menu a:has-text('Add')").first
        if not add_link.is_visible(timeout=3000):
            log(f"    WARN: no Add link in dropdown")
            page.keyboard.press("Escape")
            return False
        add_link.click()
        page.wait_for_load_state("networkidle", timeout=15000)
        time.sleep(2)
        return fill_fn_and_submit(page, section_label, fill_fn)
    except Exception as e:
        log(f"    ERROR: {e}")
        return False

def fill_fn_and_submit(page, section_label, fill_fn):
    """Run the fill function and submit."""
    try:
        inputs = page.evaluate("""
            () => Array.from(document.querySelectorAll('.modal input, .modal select, .modal textarea')).filter(el => el.getBoundingClientRect().width > 0).map(el => ({
                tag: el.tagName.toLowerCase(),
                type: el.type || '',
                name: el.name || '',
                id: el.id || '',
                placeholder: el.placeholder || '',
                value: el.value || ''
            }))
        """)
        log(f"    form has {len(inputs)} fields")
        for i in inputs[:10]:
            log(f"      <{i['tag']}> name={i['name']} id={i['id']} type={i['type']}")
        # Run fill function
        if fill_fn:
            fill_fn(page, inputs)
        # Submit
        for sel in ["button.btn-primary:has-text('Save')",
                    ".modal button[type=submit]",
                    "button:has-text('Save')",
                    "button:has-text('Submit')",
                    "input[type=submit]"]:
            try:
                btn = page.locator(sel).first
                if btn.is_visible(timeout=2000):
                    btn.click()
                    page.wait_for_load_state("networkidle", timeout=15000)
                    time.sleep(2)
                    log(f"    submitted")
                    return True
            except Exception:
                continue
        log(f"    WARN: no submit button found")
        return False
    except Exception as e:
        log(f"    ERROR: {e}")
        return False

# ============================================================
# AtlasPay data (REAL values from extracted PDFs)
# ============================================================
ATLASPAY_RISKS = [
    {"id": "R-01", "title": "Phishing Attacks", "value": "20",
     "desc": "Phishing identified as high-priority risk due to likelihood and impact on financial systems. Source: AtlasPay-Risk-Assessment R-01. Treatment: MFA + phishing simulations."},
    {"id": "R-02", "title": "Access Control Weakness", "value": "12",
     "desc": "Inconsistent least privilege enforcement. Source: AtlasPay-Risk-Assessment R-02. Treatment: RBAC + access reviews."},
    {"id": "R-03", "title": "Logging and Monitoring Gaps", "value": "9",
     "desc": "Insufficient centralized logging. Source: AtlasPay-Risk-Assessment R-03. Treatment: SIEM + alerting."},
    {"id": "R-04", "title": "Incident Response Planning and Testing", "value": "12",
     "desc": "Gaps in IR documentation and testing. Source: AtlasPay-Risk-Assessment R-04. Treatment: IR plan + tabletop exercises."},
    {"id": "R-05", "title": "Third-Party and Vendor Risk Management", "value": "12",
     "desc": "Lack of formal TPRM. Source: AtlasPay-Risk-Assessment R-05. Treatment: TPRM program + periodic reviews."},
    {"id": "R-06", "title": "Security Awareness and Training", "value": "10",
     "desc": "Generalized training with limited measurement. Source: AtlasPay-Risk-Assessment R-06. Treatment: Role-based training + phishing sim."},
]

ATLASPAY_POLICIES = [
    "Access Control & Privileged Access Policy",
    "Incident Response Policy",
    "Security Awareness & Acceptable Use Policy",
    "Third-Party Risk Management Policy",
]

ATLASPAY_CONTINUITY = [
    "Payment Processing BCP",
    "Customer Account Access BCP",
    "Fraud Monitoring BCP",
    "Financial Reporting BCP",
]

ATLASPAY_VENDORS = [
    "Cloud Provider (Sandbox)",
    "Payment Gateway (Sandbox)",
    "Identity Provider (Sandbox)",
    "Application Platform (Sandbox)",
    "Monitoring Tools (Sandbox)",
    "Finance Systems (Sandbox)",
    "Data Warehouse (Sandbox)",
]

ATLASPAY_INCIDENT = "Sample Phishing Incident - Finance Department"

results = {"risks": [], "policies": [], "continuity": [], "vendors": [], "incidents": [], "errors": []}

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
    log("  logged in")
    log("")

    # ============================================================
    # STEP 1: CONFIGURE RISK CALCULATION METHOD (enable)
    # ============================================================
    log("STEP 1: Enable Risk Calculation Method (Single Matrix - Addition)")
    page.goto(ERAMBA_URL + "/risks", wait_until="networkidle", timeout=30000)
    time.sleep(3)
    try:
        page.locator("button[aria-label='Settings']").first.click()
        time.sleep(1)
        page.locator("a:has-text('Calculation Method')").first.click()
        page.wait_for_load_state("networkidle", timeout=15000)
        time.sleep(2)
        # Find the Enable toggle
        enable_switch = page.locator(".modal input[type=checkbox]").first
        if enable_switch.count() > 0:
            checked = enable_switch.is_checked()
            log(f"  Enable toggle: checked={checked}")
            if not checked:
                # Click the toggle wrapper
                toggle_label = page.locator(".modal label:has-text('Enable')").first
                if toggle_label.count() > 0:
                    toggle_label.click()
                    log("  clicked Enable label")
                else:
                    enable_switch.click(force=True)
                    log("  clicked Enable input (force)")
                time.sleep(1)
        shot(page, "700-calc-method-modal")
        # Save
        page.locator(".modal button:has-text('Save'), .modal button.btn-primary").first.click()
        page.wait_for_load_state("networkidle", timeout=15000)
        time.sleep(2)
        log("  saved Calculation Method")
    except Exception as e:
        log(f"  ERROR: {e}")
        results["errors"].append(f"calc method: {e}")
    close_open_modal(page)
    log("")

    # ============================================================
    # STEP 2: CONFIGURE RISK APPETITE
    # ============================================================
    log("STEP 2: Configure Risk Appetite")
    page.goto(ERAMBA_URL + "/risks", wait_until="networkidle", timeout=30000)
    time.sleep(3)
    try:
        page.locator("button[aria-label='Settings']").first.click()
        time.sleep(1)
        page.locator("a:has-text('Risk Appetite')").first.click()
        page.wait_for_load_state("networkidle", timeout=15000)
        time.sleep(2)
        # Dump inputs
        inputs = page.evaluate("""
            () => Array.from(document.querySelectorAll('.modal input, .modal select, .modal textarea')).filter(el => el.getBoundingClientRect().width > 0).map(el => ({
                tag: el.tagName.toLowerCase(),
                type: el.type || '',
                name: el.name || '',
                id: el.id || '',
                placeholder: el.placeholder || '',
                value: el.value || ''
            }))
        """)
        log(f"  Risk Appetite modal has {len(inputs)} fields:")
        for i in inputs[:15]:
            log(f"    <{i['tag']}> name={i['name']} id={i['id']} type={i['type']} value='{i['value'][:30]}'")
        shot(page, "701-risk-appetite-modal")
        # Try to save without changes
        page.locator(".modal button:has-text('Save'), .modal button.btn-primary").first.click()
        page.wait_for_load_state("networkidle", timeout=15000)
        time.sleep(2)
        log("  saved Risk Appetite (defaults)")
    except Exception as e:
        log(f"  ERROR: {e}")
        results["errors"].append(f"risk appetite: {e}")
    close_open_modal(page)
    log("")

    # ============================================================
    # STEP 3: ADD RISKS (6)
    # ============================================================
    log("STEP 3: Add Risks (R-01 through R-06)")
    for risk in ATLASPAY_RISKS:
        page.goto(ERAMBA_URL + "/risks", wait_until="networkidle", timeout=30000)
        time.sleep(3)

        def fill_risk(p, inputs, risk=risk):
            log(f"      Filling risk {risk['id']}")
            try:
                if "title" in [i['name'] for i in inputs]:
                    p.locator("input[name=title]").first.fill(f"[{risk['id']}] {risk['title']}")
                elif "name" in [i['name'] for i in inputs]:
                    p.locator("input[name=name]").first.fill(f"[{risk['id']}] {risk['title']}")
                # Description
                for fname in ["description", "body", "details"]:
                    if fname in [i['name'] for i in inputs]:
                        try:
                            p.locator(f"textarea[name={fname}]").first.fill(risk['desc'])
                        except Exception:
                            pass
                        break
                # Residual/treatment if exists
                for fname in ["residual_score", "treatment", "residual_risk"]:
                    if fname in [i['name'] for i in inputs]:
                        try:
                            p.locator(f"input[name={fname}]").first.fill(risk['value'])
                        except Exception:
                            pass
            except Exception as e:
                log(f"      fill error: {e}")

        if add_via_actions_dropdown(page, f"risk {risk['id']}", fill_risk):
            results["risks"].append(risk['id'])
            shot(page, f"710-risk-{risk['id']}")
        else:
            results["errors"].append(f"risk {risk['id']}")
        close_open_modal(page)
    log("")

    # ============================================================
    # STEP 4: ADD POLICIES (4) — uses "Add item" button
    # ============================================================
    log("STEP 4: Add Policies (4)")
    for pol_title in ATLASPAY_POLICIES:
        page.goto(ERAMBA_URL + "/security-policies", wait_until="networkidle", timeout=30000)
        time.sleep(3)

        def fill_policy(p, inputs, pol_title=pol_title):
            log(f"      Filling policy: {pol_title}")
            try:
                if "title" in [i['name'] for i in inputs]:
                    p.locator("input[name=title]").first.fill(pol_title)
                elif "name" in [i['name'] for i in inputs]:
                    p.locator("input[name=name]").first.fill(pol_title)
            except Exception as e:
                log(f"      fill error: {e}")

        if add_via_actions_dropdown(page, f"policy {pol_title}", fill_policy):
            results["policies"].append(pol_title)
            shot(page, f"720-policy-{pol_title[:20]}")
        else:
            results["errors"].append(f"policy {pol_title}")
        close_open_modal(page)
    log("")

    # ============================================================
    # STEP 5: ADD CONTINUITY PLANS (4)
    # ============================================================
    log("STEP 5: Add Continuity Plans (4)")
    for cp_title in ATLASPAY_CONTINUITY:
        page.goto(ERAMBA_URL + "/business-continuity-plans", wait_until="networkidle", timeout=30000)
        time.sleep(3)

        def fill_cp(p, inputs, cp_title=cp_title):
            log(f"      Filling continuity plan: {cp_title}")
            try:
                if "title" in [i['name'] for i in inputs]:
                    p.locator("input[name=title]").first.fill(cp_title)
                elif "name" in [i['name'] for i in inputs]:
                    p.locator("input[name=name]").first.fill(cp_title)
            except Exception as e:
                log(f"      fill error: {e}")

        if add_via_actions_dropdown(page, f"BCP {cp_title}", fill_cp):
            results["continuity"].append(cp_title)
            shot(page, f"730-bcp-{cp_title[:20]}")
        else:
            results["errors"].append(f"BCP {cp_title}")
        close_open_modal(page)
    log("")

    # ============================================================
    # STEP 6: ADD VENDORS (7)
    # ============================================================
    log("STEP 6: Add Vendors (7)")
    for ven_name in ATLASPAY_VENDORS:
        page.goto(ERAMBA_URL + "/third-parties", wait_until="networkidle", timeout=30000)
        time.sleep(3)

        def fill_ven(p, inputs, ven_name=ven_name):
            log(f"      Filling vendor: {ven_name}")
            try:
                if "name" in [i['name'] for i in inputs]:
                    p.locator("input[name=name]").first.fill(ven_name)
                elif "title" in [i['name'] for i in inputs]:
                    p.locator("input[name=title]").first.fill(ven_name)
            except Exception as e:
                log(f"      fill error: {e}")

        if add_via_actions_dropdown(page, f"vendor {ven_name}", fill_ven):
            results["vendors"].append(ven_name)
            shot(page, f"740-vendor-{ven_name[:20]}")
        else:
            results["errors"].append(f"vendor {ven_name}")
        close_open_modal(page)
    log("")

    # ============================================================
    # STEP 7: ADD INCIDENT
    # ============================================================
    log("STEP 7: Add Sample Incident")
    page.goto(ERAMBA_URL + "/security-incidents", wait_until="networkidle", timeout=30000)
    time.sleep(3)

    def fill_inc(p, inputs):
        log(f"      Filling incident: {ATLASPAY_INCIDENT}")
        try:
            if "title" in [i['name'] for i in inputs]:
                p.locator("input[name=title]").first.fill(ATLASPAY_INCIDENT)
            elif "name" in [i['name'] for i in inputs]:
                p.locator("input[name=name]").first.fill(ATLASPAY_INCIDENT)
        except Exception as e:
            log(f"      fill error: {e}")

    if add_via_actions_dropdown(page, "incident", fill_inc):
        results["incidents"].append(ATLASPAY_INCIDENT)
        shot(page, "750-incident")
    else:
        results["errors"].append("incident")
    close_open_modal(page)
    log("")

    # ============================================================
    # FINAL SUMMARY
    # ============================================================
    log("=" * 70)
    log("INGESTION SUMMARY (v3)")
    log("=" * 70)
    log(f"  Risks:        {len(results['risks'])} / 6  ({results['risks']})")
    log(f"  Policies:     {len(results['policies'])} / 4  ({results['policies']})")
    log(f"  Continuity:   {len(results['continuity'])} / 4  ({results['continuity']})")
    log(f"  Vendors:      {len(results['vendors'])} / 7  ({results['vendors']})")
    log(f"  Incidents:    {len(results['incidents'])} / 1  ({results['incidents']})")
    log(f"  Errors:       {len(results['errors'])}")
    for err in results["errors"]:
        log(f"    - {err}")

    with (DOCS / "12-v3-results.json").open("w") as f:
        json.dump(results, f, indent=2)

    browser.close()
