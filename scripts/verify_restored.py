"""Verify the restored Eramba + acos population actually serves data."""
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path.home() / "Documents" / "IfeSec" / "Projects" / "atlaspay-grc-sandbox"
SHOTS = ROOT / "screenshots"
ERAMBA_URL = "https://localhost:8443"
USER, PASS = "admin", "8950Fourth"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--ignore-certificate-errors", "--no-sandbox"])
    ctx = browser.new_context(ignore_https_errors=True, viewport={"width": 1440, "height": 900})
    page = ctx.new_page()

    page.goto(ERAMBA_URL + "/login", wait_until="networkidle", timeout=60000)
    time.sleep(2)
    page.locator("input[name=login]").fill(USER)
    page.locator("input[name=password]").fill(PASS)
    page.locator("button[name=submit]").click()
    page.wait_for_selector("a:has-text('Dashboard')", timeout=30000)
    time.sleep(5)
    page.screenshot(path=str(SHOTS / "1500-restored-dashboard.png"), full_page=True)

    # Check that no internal error is shown
    body = page.evaluate("() => document.body.innerText")
    has_internal_error = "An Internal Error Has Occurred" in body
    print(f"Internal error on dashboard: {has_internal_error}")

    pages_to_capture = [
        ("/risks", "1501-restored-risks.png", "Risks"),
        ("/risks/classifications", "1502-restored-classifications.png", "Classifications"),
        ("/security-policies", "1503-restored-policies.png", "Policies"),
        ("/business-continuity-plans", "1504-restored-bcps.png", "BCPs"),
        ("/third-parties", "1505-restored-vendors.png", "Vendors"),
        ("/security-incidents", "1506-restored-incidents.png", "Incidents"),
    ]

    for path, fname, label in pages_to_capture:
        page.goto(ERAMBA_URL + path, wait_until="domcontentloaded", timeout=30000)
        time.sleep(8)
        page.screenshot(path=str(SHOTS / fname), full_page=True)

        body = page.evaluate("() => document.body.innerText")
        has_err = "An Internal Error Has Occurred" in body
        rows = page.evaluate("""() => {
            const trs = Array.from(document.querySelectorAll('table tbody tr')).filter(r => r.offsetWidth > 0 && r.innerText.trim().length > 5);
            return trs.length;
        }""")
        first = page.evaluate("""() => {
            const trs = Array.from(document.querySelectorAll('table tbody tr')).filter(r => r.offsetWidth > 0 && r.innerText.trim().length > 5);
            return trs.length > 0 ? trs[0].innerText.replace(/\\n/g, ' | ').slice(0, 150) : null;
        }""")
        print(f"  {label}: rows={rows} err={has_err}")
        if first:
            print(f"    first: {first}")

    browser.close()
