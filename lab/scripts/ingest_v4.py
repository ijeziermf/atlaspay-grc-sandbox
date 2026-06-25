"""
AtlasPay Sandbox — v4 FINAL ingestion.

Strategy:
  - For Classifications: Add a Classification Type first (via the in-form 'Add' button),
    THEN add Classifications referencing it. Use button.save-btn selector for Save.
  - For Risks: First configure Risk Calculation Method + Risk Appetite via Settings modal,
    then add risks via Actions -> Add -> save-btn.
  - For Policies / BCPs / Vendors / Incidents: All use the 'Add item' purple button.

Every form interaction ends with .save-btn (the real selector discovered by
inspecting the live DOM after Save click).
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

LOG = DOCS / "16-v4-ingestion.md"
LOG.write_text("# AtlasPay Sandbox — v4 ingestion (save-btn + classification type first)\n\n")

def log(msg=""):
    ts = time.strftime("%H:%M:%S")
    line = f"[{ts}] {msg}\n" if msg else "\n"
    with LOG.open("a") as f:
        f.write(line)
    print(line.rstrip())

def shot(page, name):
    path = SHOTS / f"{name}.png"
    page.screenshot(path=str(path), full_page=True)
    log(f"  -> {path.name}")

def close_modal(page, max_tries=3):
    for _ in range(max_tries):
        try:
            x = page.locator(".modal .close, .modal button[aria-label='Close'], .modal button.btn-close").first
            if x.is_visible(timeout=1000):
                x.click()
                time.sleep(1)
                return
        except Exception:
            pass
        try:
            page.keyboard.press("Escape")
            time.sleep(0.5)
        except Exception:
            pass

def click_save_btn(page):
    """Click the actual Eramba Save button (.save-btn)."""
    selectors = [
        ".modal button.save-btn",
        "button.save-btn",
        ".modal button.btn-primary.save-btn",
    ]
    for sel in selectors:
        try:
            btn = page.locator(sel).first
            if btn.is_visible(timeout=3000):
                btn.click()
                page.wait_for_load_state("networkidle", timeout=15000)
                time.sleep(2)
                return True
        except Exception:
            continue
    return False

# AtlasPay data
ATLASPAY_RISKS = [
    {"id": "R-01", "title": "Phishing Attacks", "value": "20"},
    {"id": "R-02", "title": "Access Control Weakness", "value": "12"},
    {"id": "R-03", "title": "Logging and Monitoring Gaps", "value": "9"},
    {"id": "R-04", "title": "Incident Response Planning and Testing", "value": "12"},
    {"id": "R-05", "title": "Third-Party and Vendor Risk Management", "value": "12"},
    {"id": "R-06", "title": "Security Awareness and Training", "value": "10"},
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
    # STEP 0: ENABLE RISK CALCULATION METHOD
    # ============================================================
    log("STEP 0: Enable Risk Calculation Method")
    page.goto(ERAMBA_URL + "/risks", wait_until="networkidle", timeout=30000)
    time.sleep(3)
    try:
        page.locator("button[aria-label='Settings']").first.click()
        time.sleep(1)
        page.locator("a:has-text('Calculation Method')").first.click()
        page.wait_for_load_state("networkidle", timeout=15000)
        time.sleep(3)
        # The modal has an "Enable" toggle — click it
        # Find the toggle in the General tab
        toggle = page.locator(".modal input[type=checkbox]").first
        if toggle.count() > 0 and not toggle.is_checked():
            # The label next to the checkbox toggles it
            label = page.locator(".modal label").filter(has_text="Enable").first
            if label.count() > 0:
                label.click()
                log("  toggled Enable")
            else:
                # Try clicking the parent label or switch element
                page.evaluate("""() => {
                    const cb = document.querySelector('.modal input[type=checkbox]');
                    if (cb && !cb.checked) cb.click();
                }""")
                log("  toggled Enable via JS")
            time.sleep(1)
        if click_save_btn(page):
            log("  saved Calculation Method")
        close_modal(page)
    except Exception as e:
        log(f"  ERROR: {e}")
    log("")

    # ============================================================
    # STEP 1: ENABLE RISK APPETITE (similar pattern)
    # ============================================================
    log("STEP 1: Configure Risk Appetite")
    page.goto(ERAMBA_URL + "/risks", wait_until="networkidle", timeout=30000)
    time.sleep(3)
    try:
        page.locator("button[aria-label='Settings']").first.click()
        time.sleep(1)
        page.locator("a:has-text('Risk Appetite')").first.click()
        page.wait_for_load_state("networkidle", timeout=15000)
        time.sleep(3)
        # Just save with defaults
        if click_save_btn(page):
            log("  saved Risk Appetite")
        close_modal(page)
    except Exception as e:
        log(f"  ERROR: {e}")
    log("")

    # ============================================================
    # STEP 2: ADD CLASSIFICATION TYPES (Impact + Likelihood)
    # These are needed before Classifications can reference them
    # ============================================================
    log("STEP 2: Add Classification Types (Impact, Likelihood)")
    page.goto(ERAMBA_URL + "/risks/classifications", wait_until="networkidle", timeout=30000)
    time.sleep(3)

    classification_types = ["Impact", "Likelihood"]

    for ct_name in classification_types:
        try:
            log(f"\n  Adding classification type: {ct_name}")
            page.locator("a.dropdown-toggle:has-text('Actions')").first.click()
            time.sleep(1)
            page.locator(".dropdown-menu a:has-text('Add')").first.click()
            page.wait_for_load_state("networkidle", timeout=15000)
            time.sleep(2)
            # Fill name
            try:
                page.locator(".modal input[name=name]").first.fill(ct_name)
                log(f"    filled name={ct_name}")
            except Exception as e:
                log(f"    WARN name: {e}")
            shot(page, f"900-classtype-{ct_name}-form")
            if click_save_btn(page):
                log(f"    added")
            else:
                log(f"    WARN: save failed")
        except Exception as e:
            log(f"  ERROR: {e}")
        close_modal(page)
        page.goto(ERAMBA_URL + "/risks/classifications", wait_until="networkidle", timeout=30000)
        time.sleep(2)

    shot(page, "901-classtypes-after")
    log("")

    # ============================================================
    # STEP 3: ADD 5 CLASSIFICATIONS (Impact type)
    # ============================================================
    log("STEP 3: Add Classifications (Critical/High/Medium/Low/Very Low)")
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
        try:
            log(f"\n  Adding classification: {cls['name']} (value={cls['value']})")
            page.locator("a.dropdown-toggle:has-text('Actions')").first.click()
            time.sleep(1)
            page.locator(".dropdown-menu a:has-text('Add')").first.click()
            page.wait_for_load_state("networkidle", timeout=15000)
            time.sleep(2)
            # Pick Classification Type = "Impact" (first option after adding types)
            try:
                sel = page.locator(".modal select[name=risk_classification_type_id]").first
                opts = sel.evaluate("el => Array.from(el.options).map(o => ({value: o.value, text: o.text}))")
                log(f"    type options: {[(o['value'], o['text']) for o in opts]}")
                # Find Impact option
                impact_opt = next((o for o in opts if "impact" in o["text"].lower()), None)
                if impact_opt:
                    sel.select_option(value=impact_opt["value"])
                    log(f"    selected type=Impact ({impact_opt['value']})")
                elif opts and opts[0]["value"]:
                    sel.select_option(value=opts[0]["value"])
                    log(f"    selected first option")
            except Exception as e:
                log(f"    WARN type: {e}")
            try:
                page.locator(".modal input[name=name]").first.fill(cls['name'])
            except Exception:
                pass
            try:
                page.locator(".modal input[name=value]").first.fill(cls['value'])
            except Exception:
                pass
            shot(page, f"910-classification-{cls['name']}-form")
            if click_save_btn(page):
                log(f"    added")
            else:
                log(f"    WARN: save failed")
        except Exception as e:
            log(f"  ERROR: {e}")
        close_modal(page)
        page.goto(ERAMBA_URL + "/risks/classifications", wait_until="networkidle", timeout=30000)
        time.sleep(2)

    shot(page, "911-classifications-final")
    log("")

    # ============================================================
    # STEP 4: ADD RISKS
    # ============================================================
    log("STEP 4: Add Risks (R-01 through R-06)")
    for risk in ATLASPAY_RISKS:
        try:
            log(f"\n  Adding risk {risk['id']}: {risk['title']}")
            page.goto(ERAMBA_URL + "/risks", wait_until="networkidle", timeout=30000)
            time.sleep(3)
            # Try both UX patterns: Actions->Add OR Add item button
            actions = page.locator("a.dropdown-toggle:has-text('Actions')").first
            if actions.is_visible(timeout=3000):
                actions.click()
                time.sleep(1)
                page.locator(".dropdown-menu a:has-text('Add')").first.click()
            else:
                add_btn = page.locator("button:has-text('Add item')").first
                if add_btn.is_visible(timeout=3000):
                    add_btn.click()
                else:
                    log(f"    WARN: no Add button")
                    continue
            page.wait_for_load_state("networkidle", timeout=15000)
            time.sleep(2)
            # Fill title
            for fname in ["title", "name"]:
                try:
                    inp = page.locator(f".modal input[name={fname}]").first
                    if inp.count() > 0:
                        inp.fill(f"[{risk['id']}] {risk['title']}")
                        log(f"    filled {fname}")
                        break
                except Exception:
                    continue
            shot(page, f"920-risk-{risk['id']}-form")
            if click_save_btn(page):
                results["risks"].append(risk['id'])
                log(f"    added")
            else:
                results["errors"].append(f"risk {risk['id']}: save failed")
        except Exception as e:
            log(f"  ERROR: {e}")
            results["errors"].append(f"risk {risk['id']}: {e}")
        close_modal(page)

    shot(page, "921-risks-final")
    log("")

    # ============================================================
    # STEP 5: ADD POLICIES (uses Add item button)
    # ============================================================
    log("STEP 5: Add Policies (4)")
    for pol in ATLASPAY_POLICIES:
        try:
            log(f"\n  Adding policy: {pol}")
            page.goto(ERAMBA_URL + "/security-policies", wait_until="networkidle", timeout=30000)
            time.sleep(3)
            # Try both
            actions = page.locator("a.dropdown-toggle:has-text('Actions')").first
            if actions.is_visible(timeout=3000):
                actions.click()
                time.sleep(1)
                page.locator(".dropdown-menu a:has-text('Add')").first.click()
            else:
                add_btn = page.locator("button:has-text('Add item')").first
                if add_btn.is_visible(timeout=3000):
                    add_btn.click()
                else:
                    log(f"    WARN: no Add")
                    continue
            page.wait_for_load_state("networkidle", timeout=15000)
            time.sleep(2)
            for fname in ["title", "name"]:
                try:
                    inp = page.locator(f".modal input[name={fname}]").first
                    if inp.count() > 0:
                        inp.fill(pol)
                        log(f"    filled {fname}")
                        break
                except Exception:
                    continue
            shot(page, f"930-policy-form")
            if click_save_btn(page):
                results["policies"].append(pol)
                log(f"    added")
            else:
                results["errors"].append(f"policy {pol}: save failed")
        except Exception as e:
            log(f"  ERROR: {e}")
            results["errors"].append(f"policy {pol}: {e}")
        close_modal(page)

    shot(page, "931-policies-final")
    log("")

    # ============================================================
    # STEP 6: ADD CONTINUITY PLANS
    # ============================================================
    log("STEP 6: Add Continuity Plans (4)")
    for cp in ATLASPAY_CONTINUITY:
        try:
            log(f"\n  Adding BCP: {cp}")
            page.goto(ERAMBA_URL + "/business-continuity-plans", wait_until="networkidle", timeout=30000)
            time.sleep(3)
            actions = page.locator("a.dropdown-toggle:has-text('Actions')").first
            if actions.is_visible(timeout=3000):
                actions.click()
                time.sleep(1)
                page.locator(".dropdown-menu a:has-text('Add')").first.click()
            else:
                add_btn = page.locator("button:has-text('Add item')").first
                if add_btn.is_visible(timeout=3000):
                    add_btn.click()
                else:
                    continue
            page.wait_for_load_state("networkidle", timeout=15000)
            time.sleep(2)
            for fname in ["title", "name"]:
                try:
                    inp = page.locator(f".modal input[name={fname}]").first
                    if inp.count() > 0:
                        inp.fill(cp)
                        break
                except Exception:
                    continue
            shot(page, f"940-bcp-form")
            if click_save_btn(page):
                results["continuity"].append(cp)
                log(f"    added")
            else:
                results["errors"].append(f"BCP {cp}: save failed")
        except Exception as e:
            results["errors"].append(f"BCP {cp}: {e}")
        close_modal(page)

    shot(page, "941-bcp-final")
    log("")

    # ============================================================
    # STEP 7: ADD VENDORS
    # ============================================================
    log("STEP 7: Add Vendors (7)")
    for ven in ATLASPAY_VENDORS:
        try:
            log(f"\n  Adding vendor: {ven}")
            page.goto(ERAMBA_URL + "/third-parties", wait_until="networkidle", timeout=30000)
            time.sleep(3)
            actions = page.locator("a.dropdown-toggle:has-text('Actions')").first
            if actions.is_visible(timeout=3000):
                actions.click()
                time.sleep(1)
                page.locator(".dropdown-menu a:has-text('Add')").first.click()
            else:
                add_btn = page.locator("button:has-text('Add item')").first
                if add_btn.is_visible(timeout=3000):
                    add_btn.click()
                else:
                    continue
            page.wait_for_load_state("networkidle", timeout=15000)
            time.sleep(2)
            for fname in ["name", "title"]:
                try:
                    inp = page.locator(f".modal input[name={fname}]").first
                    if inp.count() > 0:
                        inp.fill(ven)
                        break
                except Exception:
                    continue
            shot(page, f"950-vendor-form")
            if click_save_btn(page):
                results["vendors"].append(ven)
                log(f"    added")
            else:
                results["errors"].append(f"vendor {ven}: save failed")
        except Exception as e:
            results["errors"].append(f"vendor {ven}: {e}")
        close_modal(page)

    shot(page, "951-vendors-final")
    log("")

    # ============================================================
    # STEP 8: ADD INCIDENT
    # ============================================================
    log("STEP 8: Add Sample Incident")
    try:
        page.goto(ERAMBA_URL + "/security-incidents", wait_until="networkidle", timeout=30000)
        time.sleep(3)
        actions = page.locator("a.dropdown-toggle:has-text('Actions')").first
        if actions.is_visible(timeout=3000):
            actions.click()
            time.sleep(1)
            page.locator(".dropdown-menu a:has-text('Add')").first.click()
        else:
            add_btn = page.locator("button:has-text('Add item')").first
            if add_btn.is_visible(timeout=3000):
                add_btn.click()
        page.wait_for_load_state("networkidle", timeout=15000)
        time.sleep(2)
        for fname in ["title", "name"]:
            try:
                inp = page.locator(f".modal input[name={fname}]").first
                if inp.count() > 0:
                    inp.fill(ATLASPAY_INCIDENT)
                    break
            except Exception:
                continue
        shot(page, "960-incident-form")
        if click_save_btn(page):
            results["incidents"].append(ATLASPAY_INCIDENT)
            log(f"    added")
    except Exception as e:
        results["errors"].append(f"incident: {e}")
    close_modal(page)
    shot(page, "961-incidents-final")
    log("")

    # ============================================================
    # SUMMARY
    # ============================================================
    log("=" * 70)
    log("INGESTION SUMMARY (v4)")
    log("=" * 70)
    log(f"  Risks:        {len(results['risks'])} / 6  ({results['risks']})")
    log(f"  Policies:     {len(results['policies'])} / 4  ({results['policies']})")
    log(f"  Continuity:   {len(results['continuity'])} / 4  ({results['continuity']})")
    log(f"  Vendors:      {len(results['vendors'])} / 7  ({results['vendors']})")
    log(f"  Incidents:    {len(results['incidents'])} / 1  ({results['incidents']})")
    if results["errors"]:
        log(f"\n  Errors ({len(results['errors'])}):")
        for err in results["errors"]:
            log(f"    - {err}")

    with (DOCS / "17-v4-results.json").open("w") as f:
        json.dump(results, f, indent=2)

    browser.close()
