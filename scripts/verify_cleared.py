"""Clear cache via UI then take fresh screenshots."""
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
    time.sleep(5)  # let the dashboard fully load

    pages_to_capture = [
        ("/dashboard", "1300-dashboard.png", "Dashboard"),
        ("/risks", "1301-risks.png", "Risks"),
        ("/risks/classifications", "1302-classifications.png", "Classifications"),
        ("/security-policies", "1303-policies.png", "Policies"),
        ("/business-continuity-plans", "1304-bcps.png", "BCPs"),
        ("/third-parties", "1305-vendors.png", "Vendors"),
        ("/security-incidents", "1306-incidents.png", "Incidents"),
    ]

    for path, fname, label in pages_to_capture:
        # Hard reload to bust cache
        page.goto("about:blank")
        time.sleep(1)
        page.goto(ERAMBA_URL + path, wait_until="domcontentloaded", timeout=30000)
        time.sleep(10)  # wait for AJAX to load
        page.screenshot(path=str(SHOTS / fname), full_page=True)

        # Count actual visible rows in the data table
        row_data = page.evaluate("""() => {
            const trs = Array.from(document.querySelectorAll('table tbody tr'))
                .filter(r => r.offsetWidth > 0 && r.innerText.trim().length > 5);
            return {
                count: trs.length,
                first: trs.length > 0 ? trs[0].innerText.replace(/\\n/g, ' | ').slice(0, 200) : null,
                empty: document.body.innerText.includes('No content to display') ||
                       document.body.innerText.includes('Configure Risk Settings')
            };
        }""")
        print(f"  {label}: count={row_data['count']} empty={row_data['empty']}")
        if row_data['first']:
            print(f"    first: {row_data['first'][:150]}")

    browser.close()
