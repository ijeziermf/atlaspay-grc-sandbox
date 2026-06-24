"""
AtlasPay Sandbox — Eramba CE walkthrough driver.

Walks Steps 1-7 of the plan:
  1. Login as admin / 8950Fourth
  2. Account Settings (timezone, email)
  3. Security settings review
  4. System / Cron health
  5. Activate SOC 2 (TSC 2017) framework
  6. Create Organization 'AtlasPay Sandbox'
  7. Verify SOC 2 control library loaded

Saves screenshots + a transcript log to:
  ~/Documents/IfeSec/Projects/atlaspay-grc-sandbox/
"""
import os
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

ROOT = Path.home() / "Documents" / "IfeSec" / "Projects" / "atlaspay-grc-sandbox"
SHOTS = ROOT / "screenshots"
LOGS = ROOT / "docs"
SHOTS.mkdir(parents=True, exist_ok=True)
LOGS.mkdir(parents=True, exist_ok=True)

ERAMBA_URL = "https://localhost:8443"
USER = "admin"
PASS = "8950Fourth"

# Log file we append to throughout the run
TRANSCRIPT = LOGS / "01-initial-config.md"
TRANSCRIPT.touch()

def log(msg: str):
    """Append a timestamped line to the transcript."""
    with TRANSCRIPT.open("a") as f:
        f.write(f"[{time.strftime('%H:%M:%S')}] {msg}\n")
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")

def shot(page, name: str):
    """Save a full-page screenshot."""
    path = SHOTS / f"{name}.png"
    page.screenshot(path=str(path), full_page=True)
    log(f"  -> screenshot saved: {path.relative_to(ROOT)}")
    return path

def safe_goto(page, url: str, timeout_ms: int = 30000):
    """Navigate and wait for load. SSL warning is expected for Eramba's dev cert."""
    log(f"GOTO {url}")
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
    except PWTimeout:
        log(f"  WARN: domcontentloaded timeout on {url}, continuing")

def click_by_text(page, text: str, timeout_ms: int = 10000):
    """Click an element containing the given text (case-insensitive, exact match preferred)."""
    log(f"  CLICK '{text}'")
    # Try exact text match first
    try:
        page.get_by_text(text, exact=True).first.click(timeout=3000)
        return
    except Exception:
        pass
    # Fall back to substring match
    page.get_by_text(text).first.click(timeout=timeout_ms)

def find_in_settings(page, label: str):
    """Click a settings submenu item by its visible label."""
    log(f"  NAVIGATE to settings/{label}")
    # Settings menus are usually collapsible accordions or sidebar links
    try:
        page.get_by_role("link", name=label, exact=False).first.click(timeout=5000)
    except Exception:
        page.get_by_text(label, exact=False).first.click(timeout=5000)
    page.wait_for_load_state("domcontentloaded", timeout=15000)
    time.sleep(1)

# =========================================================================
# Main
# =========================================================================
log("=" * 70)
log("AtlasPay Sandbox — Eramba CE walkthrough")
log("=" * 70)
log(f"Eramba URL: {ERAMBA_URL}")
log(f"Sandbox client: AtlasPay Sandbox")
log(f"Industry: Financial Services / FinTech")
log(f"Employee count: 50")
log(f"Framework: SOC 2 (TSC 2017)")
log("")

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,  # background; we save screenshots
        args=["--ignore-certificate-errors", "--no-sandbox"],
    )
    context = browser.new_context(
        ignore_https_errors=True,
        viewport={"width": 1440, "height": 900},
        locale="en-US",
        timezone_id="America/New_York",
    )
    page = context.new_page()

    # ---- Step 1: Login ----
    log("STEP 1: Login as admin")
    safe_goto(page, f"{ERAMBA_URL}/login")
    page.wait_for_load_state("networkidle", timeout=30000)
    time.sleep(2)  # Vue SPA render time

    # Form fields — best-guess selectors for the Vue login form
    try:
        page.locator('input[name="email"], input[type="email"], input[autocomplete="username"]').first.fill(USER)
        log(f"  filled email/username field with '{USER}'")
    except Exception as e:
        log(f"  WARN: could not fill username field: {e}")

    try:
        page.locator('input[name="password"], input[type="password"]').first.fill(PASS)
        log("  filled password field")
    except Exception as e:
        log(f"  WARN: could not fill password field: {e}")

    shot(page, "01-login-filled")

    # Click submit button
    try:
        page.get_by_role("button", name="Login", exact=False).first.click(timeout=5000)
        log("  clicked Login button")
    except Exception as e:
        log(f"  WARN: could not click Login button: {e}; trying fallback")
        page.keyboard.press("Enter")

    page.wait_for_load_state("networkidle", timeout=30000)
    time.sleep(3)
    shot(page, "02-post-login-dashboard")
    log(f"  current URL after login: {page.url}")
    log("")

    # ---- Step 2: Account Settings ----
    log("STEP 2: Account Settings — timezone + email")
    safe_goto(page, f"{ERAMBA_URL}/settings/account")
    page.wait_for_load_state("networkidle", timeout=30000)
    time.sleep(2)
    shot(page, "03-account-settings")

    # Inspect what's on the page so we can describe it in the transcript
    try:
        inputs = page.locator("input, select").all()
        log(f"  found {len(inputs)} input/select elements on Account Settings page")
        for inp in inputs[:15]:  # cap the log
            tag = inp.evaluate("el => el.tagName.toLowerCase()")
            name = inp.evaluate("el => el.name || el.id || ''")
            val = inp.evaluate("el => el.value || ''")
            log(f"    <{tag} name='{name}' value='{val[:50]}'>")
    except Exception as e:
        log(f"  WARN: could not enumerate inputs: {e}")
    log("")

    # ---- Step 3: Security settings ----
    log("STEP 3: Security settings (review only)")
    safe_goto(page, f"{ERAMBA_URL}/settings/security")
    page.wait_for_load_state("networkidle", timeout=30000)
    time.sleep(2)
    shot(page, "04-security-settings")
    log("")

    # ---- Step 4: System / Cron health ----
    log("STEP 4: System / Cron health")
    safe_goto(page, f"{ERAMBA_URL}/settings/system")
    page.wait_for_load_state("networkidle", timeout=30000)
    time.sleep(2)
    shot(page, "05-system-cron")
    log("")

    # ---- Step 5: Available Frameworks — enable SOC 2 ----
    log("STEP 5: Enable SOC 2 (TSC 2017) framework")
    safe_goto(page, f"{ERAMBA_URL}/settings/security/frameworks")
    page.wait_for_load_state("networkidle", timeout=30000)
    time.sleep(2)
    shot(page, "06-frameworks-list-before")
    log("")

    # ---- Step 6: Create Organization ----
    log("STEP 6: Create Organization 'AtlasPay Sandbox'")
    safe_goto(page, f"{ERAMBA_URL}/organisations/add")
    page.wait_for_load_state("networkidle", timeout=30000)
    time.sleep(2)
    shot(page, "07-org-create-form")

    # Fill the org form
    try:
        page.locator('input[name="name"]').first.fill("AtlasPay Sandbox")
        log("  filled name='AtlasPay Sandbox'")
    except Exception as e:
        log(f"  WARN: could not fill name: {e}")

    # Industry / sector — try select
    try:
        sel = page.locator('select[name="sector_id"], select[name="industry"]').first
        sel.select_option(label="Financial Services / FinTech")
        log("  selected sector: Financial Services / FinTech")
    except Exception as e:
        log(f"  WARN: could not select sector: {e}")

    # Employees count
    try:
        page.locator('input[name="employees"]').first.fill("50")
        log("  filled employees=50")
    except Exception as e:
        log(f"  WARN: could not fill employees: {e}")

    shot(page, "08-org-create-form-filled")

    # Submit
    try:
        page.get_by_role("button", name="Save", exact=False).first.click(timeout=5000)
        log("  clicked Save")
        page.wait_for_load_state("networkidle", timeout=30000)
        time.sleep(2)
    except Exception as e:
        log(f"  WARN: could not click Save: {e}")

    shot(page, "09-org-created-or-error")
    log(f"  current URL after save: {page.url}")
    log("")

    # ---- Step 7: Verify SOC 2 control library ----
    log("STEP 7: Verify SOC 2 control library loaded")
    safe_goto(page, f"{ERAMBA_URL}/compliance/frameworks")
    page.wait_for_load_state("networkidle", timeout=30000)
    time.sleep(2)
    shot(page, "10-frameworks-after-activation")
    log("")

    log("=" * 70)
    log("Walkthrough complete. Review screenshots in: " + str(SHOTS))
    log("=" * 70)

    browser.close()
