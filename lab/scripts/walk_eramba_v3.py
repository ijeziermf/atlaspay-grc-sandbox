"""
AtlasPay Sandbox — Eramba CE walkthrough driver v3 (FINAL).

REAL selectors discovered via inspect_eramba.py:
  - Username input:  name='login'
  - Password input:  name='password'
  - Submit button:   name='submit' (or aria-label='Sign in')

After login, the SPA keeps /login in the URL bar for a moment but actually
shows the dashboard with the full sidebar. We must wait for nav links to be
visible before screenshotting.

REAL route paths:
  /dashboard
  /risks                         (Asset Risks)
  /third-party-risks             (Third Party Risks)
  /security-policies             (Policies)
  /compliance-managements        (Compliance Analysis / Frameworks)
  /security-incidents            (Incidents)
  /business-continuity-plans     (BCP)
  /settings/system/general       (System & Maintenance)
  /settings/authentication/general
  /settings/access-management/users
  /settings/app-configuration/appearance

Enterprise-gated (upgrade CTA, not navigable):
  Online Assessments, Awareness Programs, Account Reviews
"""
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path.home() / "Documents" / "IfeSec" / "Projects" / "atlaspay-grc-sandbox"
SHOTS = ROOT / "screenshots"
DOCS = ROOT / "docs"
SHOTS.mkdir(parents=True, exist_ok=True)
DOCS.mkdir(parents=True, exist_ok=True)

ERAMBA_URL = "https://localhost:8443"
USER = "admin"
PASS = "8950Fourth"

LOG = DOCS / "01-initial-config.md"
LOG.write_text("")  # start fresh

def log(msg: str):
    ts = time.strftime("%H:%M:%S")
    line = f"[{ts}] {msg}\n"
    with LOG.open("a") as f:
        f.write(line)
    print(line.rstrip())

def shot(page, name: str):
    """Save full-page screenshot. Waits until the page has actual content."""
    # Wait for either an h1 or a known sidebar link to be visible
    try:
        page.wait_for_selector("a:has-text('Dashboard')", timeout=10000)
    except Exception:
        pass
    path = SHOTS / f"{name}.png"
    page.screenshot(path=str(path), full_page=True)
    kb = path.stat().st_size // 1024
    log(f"  -> {path.name} ({kb} KB)")

# =========================================================================
log("=" * 70)
log("AtlasPay Sandbox — Eramba CE walkthrough v3")
log("=" * 70)
log(f"URL: {ERAMBA_URL}")
log(f"Sandbox: AtlasPay Sandbox | FinTech | 50 emp | SOC 2 (TSC 2017)")
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

    # ===== STEP 1: LOGIN =====
    log("STEP 1: Login")
    page.goto(ERAMBA_URL + "/login", wait_until="networkidle", timeout=60000)
    time.sleep(2)

    log("  Filling input[name=login]")
    page.locator("input[name=login]").fill(USER)
    log("  Filling input[name=password]")
    page.locator("input[name=password]").fill(PASS)
    shot(page, "01-login-filled")

    log("  Clicking button[name=submit] / 'Sign in'")
    page.locator("button[name=submit], button[aria-label='Sign in']").first.click()
    # Wait for the post-login DOM (Dashboard link visible)
    page.wait_for_selector("a:has-text('Dashboard')", timeout=30000)
    time.sleep(3)
    log(f"  URL after login: {page.url}")
    shot(page, "02-dashboard")
    log("")

    # ===== STEP 2: ACCOUNT SETTINGS =====
    log("STEP 2: Account Settings")
    # No direct "Account" link in the sidebar; use the II avatar top-right
    log("  Clicking user avatar (button text='II')")
    try:
        page.get_by_role("button", name="II").first.click(timeout=5000)
        time.sleep(1)
        shot(page, "03-user-menu-open")
    except Exception as e:
        log(f"  WARN: could not click avatar: {e}")
        # Fall back to direct URL
        log("  Falling back to /settings/authentication/general")
        page.goto(ERAMBA_URL + "/settings/authentication/general",
                  wait_until="networkidle", timeout=30000)
        time.sleep(2)
        shot(page, "03-authentication-general")

    # Try to find profile/account in the dropdown
    for label in ["Profile", "Account", "My Account", "Account Settings"]:
        try:
            page.get_by_role("link", name=label, exact=False).first.click(timeout=3000)
            log(f"  Clicked dropdown link '{label}'")
            page.wait_for_load_state("networkidle", timeout=15000)
            time.sleep(2)
            shot(page, f"03-account-after-{label.lower().replace(' ', '-')}")
            break
        except Exception:
            continue
    log("")

    # ===== STEP 3: SECURITY SETTINGS =====
    log("STEP 3: Security / Authentication settings (review only)")
    page.goto(ERAMBA_URL + "/settings/authentication/general",
              wait_until="networkidle", timeout=30000)
    time.sleep(2)
    shot(page, "04-authentication-general")
    log("")

    # ===== STEP 4: SYSTEM / CRON =====
    log("STEP 4: System & Maintenance")
    page.goto(ERAMBA_URL + "/settings/system/general",
              wait_until="networkidle", timeout=30000)
    time.sleep(2)
    shot(page, "05-system-maintenance")
    log("")

    # ===== STEP 5: COMPLIANCE / FRAMEWORKS =====
    log("STEP 5: Compliance Analysis (frameworks live here)")
    page.goto(ERAMBA_URL + "/compliance-managements",
              wait_until="networkidle", timeout=30000)
    time.sleep(2)
    shot(page, "06-compliance-analysis")
    log("")

    # ===== STEP 6: ORGANISATIONS — create the sandbox =====
    log("STEP 6: Create Organisation 'AtlasPay Sandbox'")
    # Find the right org-creation URL by visiting the section first
    page.goto(ERAMBA_URL + "/program-scopes",
              wait_until="networkidle", timeout=30000)
    time.sleep(2)
    shot(page, "07-program-scopes")
    # Look for "Add" button
    try:
        add = page.get_by_role("link", name="Add", exact=False).first
        if add.is_visible(timeout=3000):
            log("  Clicking 'Add' on program scopes")
            add.click()
            page.wait_for_load_state("networkidle", timeout=15000)
            time.sleep(2)
            shot(page, "07b-program-scopes-add-form")
    except Exception as e:
        log(f"  WARN: no Add button: {e}")
    log("")

    # ===== STEP 7: ASSETS / RISKS — capture structure =====
    log("STEP 7: Risks (the data we will populate from AtlasPay repo)")
    page.goto(ERAMBA_URL + "/risks", wait_until="networkidle", timeout=30000)
    time.sleep(2)
    shot(page, "08-risks-list-empty")
    log("")

    # ===== STEP 8: POLICIES =====
    log("STEP 8: Policies (we will populate from Cyber-Security-Policy-Library)")
    page.goto(ERAMBA_URL + "/security-policies",
              wait_until="networkidle", timeout=30000)
    time.sleep(2)
    shot(page, "09-policies-list-empty")
    log("")

    # ===== STEP 9: BUSINESS CONTINUITY =====
    log("STEP 9: Continuity Plans (link to AtlasPay-Risk-Profile-BCP)")
    page.goto(ERAMBA_URL + "/business-continuity-plans",
              wait_until="networkidle", timeout=30000)
    time.sleep(2)
    shot(page, "10-bcp-list-empty")
    log("")

    # ===== STEP 10: INCIDENTS =====
    log("STEP 10: Security Incidents")
    page.goto(ERAMBA_URL + "/security-incidents",
              wait_until="networkidle", timeout=30000)
    time.sleep(2)
    shot(page, "11-incidents-list-empty")
    log("")

    # ===== STEP 11: SETTINGS / ABOUT — verify build version =====
    log("STEP 11: About (verify CE build)")
    page.goto(ERAMBA_URL + "/settings/about",
              wait_until="networkidle", timeout=30000)
    time.sleep(2)
    shot(page, "12-about")
    log("")

    log("=" * 70)
    log("Walkthrough v3 complete")
    log("=" * 70)

    browser.close()
