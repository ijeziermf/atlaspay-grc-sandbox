"""Final verification: take screenshots of all data pages in the live Eramba UI."""
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
    time.sleep(3)

    pages_to_capture = [
        ("/risks", "1100-risks-live.png", "Risks"),
        ("/risks/classifications", "1101-classifications-live.png", "Classifications"),
        ("/security-policies", "1102-policies-live.png", "Policies"),
        ("/business-continuity-plans", "1103-bcps-live.png", "BCPs"),
        ("/third-parties", "1104-vendors-live.png", "Vendors"),
        ("/security-incidents", "1105-incidents-live.png", "Incidents"),
    ]

    for path, fname, label in pages_to_capture:
        page.goto(ERAMBA_URL + path, wait_until="networkidle", timeout=30000)
        time.sleep(4)
        page.screenshot(path=str(SHOTS / fname), full_page=True)
        # Get count
        count = page.evaluate("""() => {
            const all = document.body.innerText;
            const m = all.match(/All items\\s*(\\d+)/);
            return m ? m[1] : 'unknown';
        }""")
        print(f"  {label}: count={count} -> {fname}")

    browser.close()
