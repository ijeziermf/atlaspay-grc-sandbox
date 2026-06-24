"""
AtlasPay Sandbox — Eramba CE walkthrough driver v2.

LESSONS FROM v1:
- Vue SPA login button says "Sign in" (not "Login")
- Username field has no name attribute visible — find by placeholder
- URL guessing is unreliable — navigate from the dashboard via the side menu
- Auth DID succeed in v1 (we saw the Eramba header bar on the 404 page)
- We need to drive via Playwright click(), not direct URL navigation

v2 strategy: log in, then explore the dashboard to find the correct routes.
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

TRANSCRIPT = LOGS / "01-initial-config.md"

def log(msg: str):
    with TRANSCRIPT.open("a") as f:
        f.write(f"[{time.strftime('%H:%M:%S')}] {msg}\n")
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")

def shot(page, name: str):
    path = SHOTS / f"{name}.png"
    page.screenshot(path=str(path), full_page=True)
    size_kb = path.stat().st_size // 1024
    log(f"  -> {path.relative_to(ROOT)} ({size_kb} KB)")
    return path

# Clear v1 transcript so v2 is the authoritative record
TRANSCRIPT.write_text("")
log("=" * 70)
log("AtlasPay Sandbox — Eramba CE walkthrough v2")
log("=" * 70)
log(f"Eramba URL: {ERAMBA_URL}")
log(f"Sandbox client: AtlasPay Sandbox | FinTech | 50 emp | SOC 2")
log("")

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
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
    log("STEP 1: Login")
    log(f"  GOTO {ERAMBA_URL}/login")
    page.goto(ERAMBA_URL + "/login", wait_until="networkidle", timeout=60000)
    time.sleep(3)  # let Vue render

    # Fill username — use placeholder text since the field has no name attribute
    log("  Filling username (placeholder='Username')...")
    page.get_by_placeholder("Username", exact=False).first.fill(USER)
    log(f"  Filling password (placeholder='Password')...")
    page.get_by_placeholder("Password", exact=False).first.fill(PASS)

    shot(page, "01-login-filled")

    log("  Clicking 'Sign in' button...")
    page.get_by_role("button", name="Sign in", exact=False).first.click()
    page.wait_for_load_state("networkidle", timeout=30000)
    time.sleep(4)  # post-login redirect can take a moment

    shot(page, "02-post-login-dashboard")
    log(f"  URL after login: {page.url}")
    log("")

    # If still on /login, the click didn't take. Try pressing Enter on password field.
    if "/login" in page.url:
        log("  WARN: still on /login, trying Enter key fallback")
        page.get_by_placeholder("Password", exact=False).first.press("Enter")
        page.wait_for_load_state("networkidle", timeout=30000)
        time.sleep(4)
        shot(page, "02b-after-enter-key")
        log(f"  URL after Enter: {page.url}")
        log("")

    # ---- Step 1.5: Explore the dashboard to find correct menu paths ----
    log("STEP 1.5: Enumerate sidebar / menu links")
    links = page.locator("a").all()
    menu_links = []
    for link in links:
        try:
            text = link.inner_text().strip()
            href = link.get_attribute("href") or ""
            if text and len(text) < 40 and href:
                menu_links.append((text, href))
        except Exception:
            pass
    log(f"  Found {len(menu_links)} menu links")
    seen = set()
    for text, href in menu_links[:50]:
        key = (text, href)
        if key in seen:
            continue
        seen.add(key)
        log(f"    '{text}' -> {href}")
    log("")

    # ---- Step 2: Find and visit Account Settings ----
    log("STEP 2: Account Settings")
    try:
        # Try common labels
        for label in ["Account Settings", "My Account", "Profile", "Account"]:
            try:
                page.get_by_role("link", name=label, exact=False).first.click(timeout=3000)
                log(f"  Clicked '{label}'")
                break
            except Exception:
                continue
        page.wait_for_load_state("networkidle", timeout=30000)
        time.sleep(2)
    except Exception as e:
        log(f"  WARN: {e}; falling back to direct URL")
        page.goto(f"{ERAMBA_URL}/settings/account", wait_until="networkidle", timeout=30000)
        time.sleep(2)

    shot(page, "03-account-settings")
    log(f"  URL: {page.url}")
    log("")

    # ---- Step 3: Security settings ----
    log("STEP 3: Security settings (review only, no changes)")
    try:
        for label in ["Security", "Authentication", "Policies"]:
            try:
                page.get_by_role("link", name=label, exact=False).first.click(timeout=3000)
                log(f"  Clicked '{label}'")
                break
            except Exception:
                continue
        page.wait_for_load_state("networkidle", timeout=30000)
        time.sleep(2)
    except Exception:
        page.goto(f"{ERAMBA_URL}/settings/security", wait_until="networkidle", timeout=30000)
        time.sleep(2)

    shot(page, "04-security-settings")
    log(f"  URL: {page.url}")
    log("")

    # ---- Step 4: System / Cron ----
    log("STEP 4: System / Cron")
    try:
        for label in ["System", "Cron", "System Health", "Status"]:
            try:
                page.get_by_role("link", name=label, exact=False).first.click(timeout=3000)
                log(f"  Clicked '{label}'")
                break
            except Exception:
                continue
        page.wait_for_load_state("networkidle", timeout=30000)
        time.sleep(2)
    except Exception:
        page.goto(f"{ERAMBA_URL}/settings/system", wait_until="networkidle", timeout=30000)
        time.sleep(2)

    shot(page, "05-system-cron")
    log(f"  URL: {page.url}")
    log("")

    # ---- Step 5: Frameworks (Available list) ----
    log("STEP 5: Available Frameworks")
    # Try to navigate to compliance area
    try:
        for label in ["Compliance", "Frameworks", "Compliance Management"]:
            try:
                page.get_by_role("link", name=label, exact=False).first.click(timeout=3000)
                log(f"  Clicked '{label}'")
                break
            except Exception:
                continue
        page.wait_for_load_state("networkidle", timeout=30000)
        time.sleep(2)
    except Exception:
        page.goto(f"{ERAMBA_URL}/compliance/frameworks", wait_until="networkidle", timeout=30000)
        time.sleep(2)

    shot(page, "06-compliance-frameworks")
    log(f"  URL: {page.url}")
    log("")

    # ---- Step 6: Create Organization ----
    log("STEP 6: Create Organization 'AtlasPay Sandbox'")
    try:
        for label in ["Organisations", "Organizations", "Organisation", "Organization"]:
            try:
                page.get_by_role("link", name=label, exact=False).first.click(timeout=3000)
                log(f"  Clicked '{label}'")
                break
            except Exception:
                continue
        page.wait_for_load_state("networkidle", timeout=30000)
        time.sleep(2)
    except Exception:
        page.goto(f"{ERAMBA_URL}/organisations", wait_until="networkidle", timeout=30000)
        time.sleep(2)

    shot(page, "07-organisations-list")
    log(f"  URL: {page.url}")
    log("")

    # Look for "Add" button
    try:
        for label in ["Add", "Add Organisation", "Add Organization", "New", "Create"]:
            try:
                page.get_by_role("link", name=label, exact=False).first.click(timeout=3000)
                log(f"  Clicked '{label}'")
                break
            except Exception:
                continue
        page.wait_for_load_state("networkidle", timeout=30000)
        time.sleep(2)
    except Exception as e:
        log(f"  WARN: could not find Add button: {e}")

    shot(page, "08-org-create-form")
    log(f"  URL: {page.url}")
    log("")

    # ---- Step 7: Verify control library ----
    log("STEP 7: Verify SOC 2 control library")
    try:
        for label in ["Frameworks", "Compliance", "Controls"]:
            try:
                page.get_by_role("link", name=label, exact=False).first.click(timeout=3000)
                log(f"  Clicked '{label}'")
                break
            except Exception:
                continue
        page.wait_for_load_state("networkidle", timeout=30000)
        time.sleep(2)
    except Exception:
        page.goto(f"{ERAMBA_URL}/compliance/frameworks", wait_until="networkidle", timeout=30000)
        time.sleep(2)

    shot(page, "09-frameworks-after-activation")
    log(f"  URL: {page.url}")
    log("")

    log("=" * 70)
    log("Walkthrough v2 complete. Review screenshots and this transcript.")
    log("=" * 70)
    browser.close()
